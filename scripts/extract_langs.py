import os
import csv
import zipfile
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
import json
import pandas as pd
import re

load_dotenv()

CASES_DIR = "../data/cases"
MODEL_NAME = "o3"

client = OpenAI(
  api_key='XXX'
)

def unzip_case(case_folder, temp_dir):
    zip_path = os.path.join(case_folder, f"{os.path.basename(case_folder)}_input.zip")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(temp_dir)
    # Return list of file paths
    all_files = []
    for root, _, files in os.walk(temp_dir):
        for fn in sorted(files):
            if fn.lower().endswith(('.py','.js','.jsx','.java','.cpp','.c','.ts','.tsx', '.html', '.erb', '.go', '.php', '.json', '.cs', '.txt', '.md', '.lock')):
                all_files.append(os.path.join(root, fn))
    return all_files


def load_file_blocks(file_paths):
    blocks = []
    for fp in file_paths:
        try: 
            with open(fp) as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(fp, encoding="latin-1", errors="replace") as f:
                content = f.read()
        fname = os.path.basename(fp)
        blocks.append(f"<< {fname} >>\n```\n{content}\n``   `\n")
    return "\n".join(blocks)

def call_openai(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
    #temperature=0
    )
    return response.choices[0].message.content

def load_patch(case_id: int, cases_root: str = "data/cases"):
    case_key   = f"case{case_id}"
    patch_path = os.path.join(cases_root, case_key, f"{case_key}.patch")

    """Return file *path* as str, trying several encodings and finally replacing bad bytes."""
    encodings = ("utf-8", "utf-8-sig", "latin-1", "utf-16", "utf-16-le", "utf-16-be")
    for enc in encodings:
        try:
            with open(patch_path, "r", encoding=enc) as fh:
                data = fh.read()
            return data
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            raise
    # Last‑chance fallback: read binary and replace undecodable chars
    with open(patch_path, "rb") as fh:
        raw = fh.read()
    return raw.decode("utf-8", errors="replace")

def process_cases(outputs_csv: str, cases_dir: str, out_csv: str):
    df = pd.read_csv(outputs_csv)
    df["language"] = ""

    SYSTEM_PROMPT = (
        "You are an expert software engineer. "
        "Patches, source files, and an explanation of the files are provided. From the code and the explanation, infer what programming languages are used, and return a comma‑separated list of all programming languages that are used. "
        "Use canonical names (e.g., Python, C, JavaScript, Shell). "
        "If multiple languages are present (aka like python calling into unsafe c code), list each exactly once, separated by commas (like python, c), "
        "in any order. Each language should be listed only once. Do not output anything else."
    )

    for idx, row in df.iterrows():
        if int(row["Case"]) == 1:
            continue
        if int(row["Case"]) == 105:
            continue
        if int(row["Case"]) == 147:
            continue

        if int(row["Case"]) >= 2 and int(row["Case"]) <= 104:
            case_id = int(row["Case"]) - 1
        elif int(row["Case"]) >= 106 and int(row["Case"]) <= 146:
            case_id = int(row["Case"]) - 2
        elif int(row["Case"]) >= 148 and int(row["Case"]) <= 177:
            case_id = int(row["Case"]) - 3
        
        case_key = 'case' + str(case_id)  # e.g. 'case1'
        case_folder = os.path.join(CASES_DIR, case_key)
        explanation = row["Description"]
        patch_text = load_patch(case_id)
        #print(f"patch_text: {patch_text}")

        with tempfile.TemporaryDirectory() as tmp:
                files = unzip_case(case_folder, tmp)
                file_blocks = load_file_blocks(files)
                print(f"[DEBUG] Found {len(files)} files for case {row['Case']}:")
                df.at[idx, "num_files"] = len(files)
                for f in files:
                    print("   └", os.path.basename(f))
                    print(f"[DEBUG] Assembled file_blocks length: {len(file_blocks)} chars")

        USER_PROMPT = (
            f"=== Patch ===\n{patch_text}\n\n=== Explanation ===\n{explanation}\n\n=== Files ===\n{file_blocks}\n"  # noqa: E501
            "\nList all languages:"
        )

        languages = ""
        try:
            languages = call_openai(SYSTEM_PROMPT, USER_PROMPT)
            #languages = "python, c"
            languages = re.sub(r'^\s*Languages?\s*:?\s*', '', languages, flags=re.IGNORECASE)
            languages = re.sub(r'^\s*-\s*', '', languages)
            languages = re.sub(r'[\"`\'()]', '', languages).lower().strip()
        except Exception as e:
            print(f"[WARN] {case_key}: LLM call failed – {e}")

        df.at[idx, "language"] = languages
        print(f"✓ {case_key}: {languages}")

    df.to_csv(out_csv, index=False)
    print(f"\nSaved augmented CSV to {out_csv}\n")

if __name__ == "__main__":
    process_cases(
        "../vader.csv",
        "../data/cases",
        "vader_lang.csv"
    )
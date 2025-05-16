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

def load_patch(case_id: int, cases_root: str = "../data/cases"):
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
    df["before_after"] = ""

    SYSTEM_PROMPT = (
        "You are an expert software engineer. "
        "Given a patch and a set of tests, analyze whether the test case is written for before or after the patch."
        "If before, return 'before'. If after, return 'after'. You must return only one of these two strings, failure to do so will result in a million dollar penalty."
    )

    for idx, row in df.iterrows():
        if int(row["Case"]) >= 2 and int(row["Case"]) <= 104:
            case_id = int(row["Case"]) - 1
        elif int(row["Case"]) >= 106 and int(row["Case"]) <= 146:
            case_id = int(row["Case"]) - 2
        elif int(row["Case"]) >= 148 and int(row["Case"]) <= 177:
            case_id = int(row["Case"]) - 3
        
        case_key = 'case' + str(case_id)  # e.g. 'case1'
        case_folder = os.path.join(CASES_DIR, case_key)
        with open(os.path.join(case_folder, f"{case_key}_tests.txt")) as tf:
                tests = tf.read()
        patch_text = load_patch(case_id)
        #print(f"patch_text: {patch_text}")

        USER_PROMPT = (
            f"=== Patch ===\n{patch_text}\n\n=== Tests ===\n{tests}\n"
        )

        try:
            decisison = call_openai(SYSTEM_PROMPT, USER_PROMPT).lower().strip()
        except Exception as e:
            print(f"[WARN] {case_key}: LLM call failed – {e}")

        df.at[idx, "before_after"] = decisison
        print(f"✓ {case_key}: {decisison}")

    df.to_csv(out_csv, index=False)
    print(f"\nSaved augmented CSV to {out_csv}\n")

if __name__ == "__main__":
    process_cases(
        "../data/vader_languages.csv",
        "../data/cases",
        "../data/vader_languages_before_after.csv"
    )
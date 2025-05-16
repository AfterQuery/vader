import os
import csv
import zipfile
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
import json
import anthropic
from google import genai
import pandas as pd

load_dotenv()

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#client = anthropic.Anthropic()
#client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
client = OpenAI(
  api_key=os.getenv("GROK_API_KEY"),
  base_url="https://api.x.ai/v1",
)

# Configuration
DATASET_CSV = "../data/dataset.csv"
CASES_DIR = "../data/cases"
MODEL_NAME = "grok-3-beta"
#"gemini-2.5-pro-preview-03-25", "claude-3-7-sonnet-20250219"
OUTPUT_CSV = f"data/llm_outputs/{MODEL_NAME}.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# Prompt templates
SYSTEM_TEMPLATE = """
You are a cybersecurity engineer.

For the very first case, you will receive:
- A vulnerability description
- The code files for inspection
- The patch
- Test case descriptions

For all following cases, you will receive only the code files.

**For each case, produce exactly one JSON object (and nothing else) with these four keys:**
{
  "cwe_id":      "CWE-XXX",
  "explanation": "A clear, concise technical explanation of the issue.",
  "patch":       "A Git-style patch that exactly matches the format of the patch example.",
  "test_plan":   ["step 1 description", "step 2 description", …]
}

**Requirements:**
1. Do **NOT** wrap the JSON in markdown or code fences.  
2. Do **NOT** include any extra keys or any commentary.  
3. Preserve all formatting inside the `"explanation"` and `"patch"` fields exactly as shown in the examples.  
"""

CASE_PROMPT_TEMPLATE = """
Case {case_id}:
Files:
{file_blocks}

Please identify the vulnerability, explain it, propose a patch, and outline test steps to validate your fix. 
Your patch must be in the form of a GitHub-generated patch, as shown in the example patch. 
Respond in JSON with keys: "cwe_id", "explanation", "patch", "test_plan".
"""

CONFIRM_PROMPT_TEMPLATE = """
First case ({case_id}):
Description:
{description}

Patch:
{patch}

Test Cases:
{tests}
"""


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

def call_anthropic(system_prompt: str, user_prompt: str) -> str:
    resp = client.beta.messages.create(
        model=MODEL_NAME,
        max_tokens=20000,
        thinking = {
            "type": "enabled",
            "budget_tokens": 8192
        },
        temperature=1,
        system=system_prompt,       # top‑level field, not in messages
        messages=[{
            "role": "user", 
            "content": user_prompt
        }],
        betas=["output-128k-2025-02-19"],
    )
    # Claude returns a list of content blocks; plain text is in .text
    return extract_all_text(resp)

def extract_all_text(resp) -> str:
    """Return the concatenated assistant text from a Claude beta response."""
    texts = []
    for blk in resp.content:
        if blk.type == "text":          # or isinstance(blk, BetaTextBlock)
            texts.append(blk.text)
    return "".join(texts)

def call_gemini(system_prompt: str, user_prompt: str) -> str:
    """
    One‑shot call to Gemini 2.5 Pro.
    Returns the assistant text (Gemini has no streaming yet in the Python SDK).
    """
    
    prompt_parts = [
        {"role": "system", "parts": [system_prompt]},
        {"role": "user",   "parts": [user_prompt]},
    ]
    response = client.models.generate_content(
        model = MODEL_NAME,
        contents = [
            {  
                "role": "user",
                "parts": [{"text": system_prompt}]
            },
            {
                "role": "user",
                "parts": [{"text": user_prompt}]
            },
        ],
    )

    # Gemini responses come back as a list of candidates; take the first
    return response.text

def main():
    df = pd.read_csv(DATASET_CSV)
    # df = df.iloc[[0]]
    df = df[75:]
    first = True

    with open(OUTPUT_CSV, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["case", "model", "response"])

    for index, row in df.iterrows():
        case_key = 'case' + str(row['Case'])  # e.g. 'case1'
        case_folder = os.path.join(CASES_DIR, case_key)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                files = unzip_case(case_folder, tmp)
                file_blocks = load_file_blocks(files)
                print(f"[DEBUG] Found {len(files)} files for case {row['Case']}:")
                for f in files:
                    print("   └", os.path.basename(f))
                    print(f"[DEBUG] Assembled file_blocks length: {len(file_blocks)} chars")
        
        except UnicodeDecodeError as e:
            print(f"[WARN] {case_key}: non-text file encountered → skipping LLM call")
            # append an empty-placeholder row
            with open(OUTPUT_CSV, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([str(row['Case']), MODEL_NAME, ""])
            continue
        # For the first case, send confirmation prompt
        if first:
            # Load patch and tests
            with open(os.path.join(case_folder, f"{case_key}.patch")) as pf:
                golden_patch = pf.read()
            with open(os.path.join(case_folder, f"{case_key}_tests.txt")) as tf:
                tests = tf.read()

            confirm_prompt = CONFIRM_PROMPT_TEMPLATE.format(
                case_id=row['Case'],
                description=row['Description'],
                patch=golden_patch,
                tests=tests
            )
            print(confirm_prompt)
            ack = call_openai(SYSTEM_TEMPLATE, confirm_prompt)
            # if 'ACK' not in ack:
            #     print(f"Did not receive ACK for first case: {ack}")
            #     return
            first = False

        # Build the main case prompt
        case_prompt = CASE_PROMPT_TEMPLATE.format(
            case_id=row['Case'],
            file_blocks=file_blocks
        )

        # Call the LLM
        output = call_openai(SYSTEM_TEMPLATE, case_prompt)

        # Append output to csv
        with open(OUTPUT_CSV, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([row["Case"], MODEL_NAME, output])

        print(f"Appended output for case {row['Case']} to {OUTPUT_CSV}")

if __name__ == '__main__':
    main()

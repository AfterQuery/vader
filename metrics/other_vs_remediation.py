#!/usr/bin/env python3
"""
Correlation between *-other and *-remediation columns
Example:
    python metrics/corr_other_vs_remediation.py --file data/graded.xlsx
"""
import argparse, pandas as pd, numpy as np
from scipy.stats import pearsonr

MODELS = [
    "claude-3.7-sonnet",
    "gemini-2.5-pro",
    "gpt-4.1",
    "gpt-4.5",
    "o3",
    "grok-3-beta",
]

def main(path: str):
    df = pd.read_excel(path, engine="openpyxl")

    rows = []
    for m in MODELS:
        col_other = f"{m}-other"
        col_rem   = f"{m}-remediation"
        if col_other not in df or col_rem not in df:
            print(f"⚠️  missing columns for {m} — skipped")
            continue

        # drop rows where either score is NaN
        tmp = df[[col_other, col_rem]].dropna()
        if len(tmp) < 2:        # need ≥2 points for correlation
            continue

        r, p = pearsonr(tmp[col_other], tmp[col_rem])

        # P(rem=0 | other=0)
        other_zero = tmp[tmp[col_other] == 0]
        prob = np.mean(other_zero[col_rem] == 0) if len(other_zero) else np.nan

        rows.append(
            dict(model=m,
                 n=len(tmp),
                 pearson=f"{r:.3f}",
                 p_value=f"{p:.3g}",
                 prob_rem0_given_other0=f"{prob:.2f}"))
    print(pd.DataFrame(rows))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="graded.xlsx path")
    args = ap.parse_args()
    main(args.file)

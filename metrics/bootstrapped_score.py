#!/usr/bin/env python3
# metrics/compute_scores.py
"""
Aggregate human ratings from graded.xlsx and print a leaderboard.

Example:
    python metrics/bootstrapped_score.py --file_path data/graded.xlsx \
           --bootstrap 1000 --seed 42
"""
import argparse, pandas as pd, numpy as np
from rating_metrics import bootstrap_mean_ci

MODELS = [
    "claude-3.7-sonnet",
    "gemini-2.5-pro",
    "gpt-4.1",
    "gpt-4.5",
    "o3",
    "grok-3-beta",
]

def main(file_path: str, n_boot: int, seed: int):
    df = pd.read_excel(file_path, engine="openpyxl")
    df = df[df["Case"] != 1]
    
    # -- report any entirely dropped cases (e.g. 105, 147) --
    all_cases = set(range(1, int(df["Case"].max()) + 1))
    present_cases = set(df["Case"].dropna().astype(int).unique())
    dropped = sorted(all_cases - present_cases)
    if dropped:
        print(f"Overall dropped cases (not in sheet): {dropped}")
    
    for m in MODELS:
        col = f"{m}-rating"
        missing_cases = df[df[col].isna()]["Case"].tolist()
        if missing_cases:
            print(f"{m}: {len(missing_cases)} missing → {missing_cases}")
    
    row147 = df[df["Case"] == 145]        # or "Case 145" if the column is a string
    print(row147[[f"{m}-rating" for m in MODELS]])
    
    leaderboard = []
    for m in MODELS:    
        col = f"{m}-rating"
        if col not in df.columns:
            raise KeyError(f"Missing column {col}")

        ratings = df[col].dropna().astype(float)
        mean, lo, hi = bootstrap_mean_ci(ratings, n_boot, seed)
        leaderboard.append({"model": m, "mean": mean, "ci_low": lo, "ci_high": hi,
                            "n_scored": len(ratings)})

    lb = pd.DataFrame(leaderboard).sort_values("mean", ascending=False)
    print("\n=== VADER Leaderboard (human‑rated 1‑10 scale) ===")
    print(lb.to_string(index=False, formatters={
        "mean": "{:.4f}".format,
        "ci_low": "{:.4f}".format,
        "ci_high": "{:.4f}".format
    }))

    # save to disk for plotting
    lb.to_csv("plots/leaderboard.csv", index=False)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file_path", required=True)
    p.add_argument("--bootstrap", type=int, default=1000)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    main(args.file_path, args.bootstrap, args.seed)

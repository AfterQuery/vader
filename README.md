# VADER: A Human-Evaluated Benchmark for Vulnerability Assessment, Detection, Explanation, and Remediation

### Quickstart: reproduce human‑rating leaderboard

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt           # pandas, numpy, matplotlib
python metrics/compute_scores.py --csv data/graded.csv
python plots/make_plots.py

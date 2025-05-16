import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../plots/leaderboard.csv")

plt.figure()
plt.errorbar(
    df["model"],
    df["mean"],
    yerr=[df["mean"] - df["ci_low"], df["ci_high"] - df["mean"]],
    fmt="o",
    capsize=6,           # horizontal caps at whisker ends
    linestyle="None"
)
plt.ylim(0, 10)          # 0–10 scale
plt.ylabel("Human Rating (0–10)")
plt.title("VADER Leaderboard – Mean ±95% CI")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig("../plots/leaderboard_ci.png", dpi=300)
plt.show()

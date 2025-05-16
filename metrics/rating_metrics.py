import numpy as np

def bootstrap_mean_ci(values, B=1000, seed=42, alpha=0.05):
    rng = np.random.default_rng(seed)
    vals = np.asarray(values)
    boots = [rng.choice(vals, size=len(vals), replace=True).mean() for _ in range(B)]
    lo, hi = np.percentile(boots, [100*alpha/2, 100*(1-alpha/2)])
    return vals.mean(), lo, hi  
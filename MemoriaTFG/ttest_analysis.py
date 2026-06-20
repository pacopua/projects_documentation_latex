#!/usr/bin/env python3
"""
T-test analysis on ExperimentosInfo.json
Comparisons:
  1. colbPowers vs baseline
  2. Opencode vs Claudecode
Metrics: total tool calls, total tokens, cyclomatic complexity, maintainability index

NOTE: n=3 per group. Welch's t-test results should be interpreted as indicative
only. With n=3, normality cannot be verified and power is very low.
Hedges' g is reported as the primary effect-size metric.
"""

import json
from pathlib import Path
from scipy import stats
import numpy as np

DATA_FILE = Path(__file__).parent / "ExperimentosInfo.json"


def hedges_g(a, b):
    """Hedges' g effect size with small sample bias correction."""
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return float("nan")
    
    var_a = np.var(a, ddof=1)
    var_b = np.var(b, ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var_a + (n2 - 1) * var_b) / (n1 + n2 - 2))
    
    if pooled_sd == 0:
        return float("nan")
        
    d = (np.mean(a) - np.mean(b)) / pooled_sd
    df = n1 + n2 - 2
    j = 1 - (3 / (4 * df - 1))
    
    return d * j


def effect_label(g, p=None):
    if np.isnan(g):
        return "n/a"
    mag = abs(g)
    if mag < 0.2:
        label = "trivial"
    elif mag < 0.5:
        label = "small"
    elif mag < 0.8:
        label = "medium"
    else:
        label = "large"
    if p is None or np.isnan(p) or p >= 0.05:
        label += " (ns)"
    return label


def extract_runs(data, task, tool, condition):
    """Return list of dicts with metrics for each run in a condition."""
    runs = []
    group = data[task][tool][condition]
    for run in group.values():
        entry = {
            "total_toolcalls": run["toolcalls"]["TOTAL"],
            "total_tokens": run["total_tokens"]["total"],
        }
        if "avg_cyclomatic_complexity" in run:
            entry["avg_cyclomatic_complexity"] = run["avg_cyclomatic_complexity"]
        if "mantainability_index" in run:
            entry["mantainability_index"] = run["mantainability_index"]
        runs.append(entry)
    return runs


def ttest_report(label, group_a, group_b, metric):
    """Run Welch's t-test + Hedges' g and print a formatted result line."""
    a = [r[metric] for r in group_a if metric in r]
    b = [r[metric] for r in group_b if metric in r]
    if len(a) < 2 or len(b) < 2:
        print(f"  {metric}: not enough data (n_a={len(a)}, n_b={len(b)})")
        return
    t, p = stats.ttest_ind(a, b, equal_var=False)
    g = hedges_g(a, b)
    mean_a, mean_b = np.mean(a), np.mean(b)
    sig = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
    print(f"  {metric}:")
    print(
        f"    mean_A={mean_a:.2f}  mean_B={mean_b:.2f} "
        f" t={t:.3f}  p={p:.4f}  {sig}"
        f"  |  g={g:+.2f} ({effect_label(g, p)})"
    )


def run_comparison(label_a, runs_a, label_b, runs_b, metrics):
    print(f"\n{'='*60}")
    print(f"  A: {label_a}  (n={len(runs_a)})")
    print(f"  B: {label_b}  (n={len(runs_b)})")
    print(f"{'='*60}")
    for metric in metrics:
        ttest_report(f"{label_a} vs {label_b}", runs_a, runs_b, metric)


def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    tasks = list(data.keys())
    tools = ["Opencode", "Claudecode"]
    conditions = ["colbPowers", "baseline"]
    base_metrics = ["total_toolcalls", "total_tokens"]
    quality_metrics = ["avg_cyclomatic_complexity", "mantainability_index"]

    print("=" * 60)
    print("  T-TEST ANALYSIS  (Welch's independent samples)")
    print("  WARNING: n=3 per group — interpret with caution.")
    print("  Hedges' g is the primary effect-size metric.")
    print("=" * 60)

    # ----------------------------------------------------------------
    # 1. colbPowers vs baseline  (per task × tool)
    # ----------------------------------------------------------------
    print("\n\n### 1. colbPowers vs baseline ###")
    for task in tasks:
        for tool in tools:
            runs_cp = extract_runs(data, task, tool, "colbPowers")
            runs_bl = extract_runs(data, task, tool, "baseline")
            has_quality = any("avg_cyclomatic_complexity" in r for r in runs_cp + runs_bl)
            metrics = base_metrics + (quality_metrics if has_quality else [])
            run_comparison(
                f"{task} / {tool} / colbPowers",
                runs_cp,
                f"{task} / {tool} / baseline",
                runs_bl,
                metrics,
            )

    # ----------------------------------------------------------------
    # 2. Opencode vs Claudecode  (per task × condition)
    # ----------------------------------------------------------------
    print("\n\n### 2. Opencode vs Claudecode ###")
    for task in tasks:
        for cond in conditions:
            runs_oc = extract_runs(data, task, "Opencode", cond)
            runs_cc = extract_runs(data, task, "Claudecode", cond)
            has_quality = any("avg_cyclomatic_complexity" in r for r in runs_oc + runs_cc)
            metrics = base_metrics + (quality_metrics if has_quality else [])
            run_comparison(
                f"{task} / Opencode / {cond}",
                runs_oc,
                f"{task} / Claudecode / {cond}",
                runs_cc,
                metrics,
            )

    # ----------------------------------------------------------------
    # 3. Pooled across tasks: colbPowers vs baseline
    # ----------------------------------------------------------------
    print("\n\n### 3. Pooled across all tasks — colbPowers vs baseline ###")
    for tool in tools:
        all_cp, all_bl = [], []
        for task in tasks:
            all_cp += extract_runs(data, task, tool, "colbPowers")
            all_bl += extract_runs(data, task, tool, "baseline")
        run_comparison(
            f"ALL tasks / {tool} / colbPowers",
            all_cp,
            f"ALL tasks / {tool} / baseline",
            all_bl,
            base_metrics,
        )

    print("\n\nNote: * p<0.05  ** p<0.01  *** p<0.001  ns=not significant")
    print(f"      g: trivial<0.2 | small<0.5 | medium<0.8 | large≥0.8")
    print(f"      (ns) = p≥0.05; effect size label unreliable without significance")
    print(f"      Sample sizes per group are small (n=3). With n=3 the minimum")
    print(f"      achievable p-value for a non-parametric test is 0.10, so")
    print(f"      Welch p-values should be treated as indicative only.\n")


if __name__ == "__main__":
    main()

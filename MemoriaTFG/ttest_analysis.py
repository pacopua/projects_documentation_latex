#!/usr/bin/env python3
"""
T-test analysis on ExperimentosInfo.json
Comparisons:
  1. colbPowers vs baseline
  2. Opencode vs Claudecode
Metrics: total tool calls, total tokens, cyclomatic complexity, maintainability index

NOTE: n=3 per group. Welch's t-test results should be interpreted as indicative
only. With n=3, normality cannot be verified and power is very low.
Cohen's d is reported as the primary effect-size metric.
"""

import json
from pathlib import Path
from scipy import stats
import numpy as np

DATA_FILE = Path(__file__).parent / "ExperimentosInfo.json"


def cohens_d(a, b):
    """Pooled Cohen's d effect size."""
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    pooled = np.sqrt((np.std(a, ddof=1) ** 2 + np.std(b, ddof=1) ** 2) / 2)
    if pooled == 0:
        return float("nan")
    return (np.mean(a) - np.mean(b)) / pooled


def effect_label(d):
    if np.isnan(d):
        return "n/a"
    d = abs(d)
    if d < 0.2:
        return "trivial"
    if d < 0.5:
        return "small"
    if d < 0.8:
        return "medium"
    return "large"


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
    """Run Welch's t-test + Cohen's d and print a formatted result line."""
    a = [r[metric] for r in group_a if metric in r]
    b = [r[metric] for r in group_b if metric in r]
    if len(a) < 2 or len(b) < 2:
        print(f"  {metric}: not enough data (n_a={len(a)}, n_b={len(b)})")
        return
    t, p = stats.ttest_ind(a, b, equal_var=False)
    d = cohens_d(a, b)
    mean_a, mean_b = np.mean(a), np.mean(b)
    sig = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
    print(f"  {metric}:")
    print(
        f"    mean_A={mean_a:.2f}  mean_B={mean_b:.2f} "
        f" t={t:.3f}  p={p:.4f}  {sig}"
        f"  |  d={d:+.2f} ({effect_label(d)})"
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
    print("  Cohen's d is the primary effect-size metric.")
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
    print(f"      d: trivial<0.2 | small<0.5 | medium<0.8 | large≥0.8")
    print(f"      Sample sizes per group are small (n=3). With n=3 the minimum")
    print(f"      achievable p-value for a non-parametric test is 0.10, so")
    print(f"      Welch p-values should be treated as indicative only.\n")


if __name__ == "__main__":
    main()

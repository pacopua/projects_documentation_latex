#!/usr/bin/env python3
"""
Generates:
  - results_figure.png  : bar charts + summary table (for Word/Docs/PDF)
  - results_table.tex   : LaTeX booktabs tables (for LaTeX memoria)
"""

import json
from pathlib import Path
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

matplotlib.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.dpi": 150,
})

DATA_FILE = Path(__file__).parent / "ExperimentosInfo.json"
OUT_PNG   = Path(__file__).parent / "graficos" / "ttest_analisis"/ "results_figure.png"
OUT_TEX   = Path(__file__).parent / "graficos" / "ttest_analisis"/ "results_table.tex"

# ── helpers ───────────────────────────────────────────────────────────────────

def extract_runs(data, task, tool, condition):
    runs = []
    for run in data[task][tool][condition].values():
        entry = {
            "total_toolcalls": run["toolcalls"]["TOTAL"],
            "total_tokens":    run["total_tokens"]["total"],
        }
        if "avg_cyclomatic_complexity" in run:
            entry["avg_cyclomatic_complexity"] = run["avg_cyclomatic_complexity"]
        if "mantainability_index" in run:
            entry["mantainability_index"] = run["mantainability_index"]
        runs.append(entry)
    return runs


def welch(a, b):
    if len(a) < 2 or len(b) < 2:
        return float("nan"), float("nan")
    return stats.ttest_ind(a, b, equal_var=False)


def sig_stars(p):
    if np.isnan(p):  return "n/a"
    if p < 0.001:    return "***"
    if p < 0.01:     return "**"
    if p < 0.05:     return "*"
    return "ns"


def fmt_mean(vals, metric):
    m = np.mean(vals)
    if metric == "total_tokens":
        return f"{m/1e6:.2f}M"
    return f"{m:.2f}"


def metric_label(m):
    return {
        "total_toolcalls":         "Total tool calls",
        "total_tokens":            "Total tokens (M)",
        "avg_cyclomatic_complexity": "Cyclomatic complexity",
        "mantainability_index":    "Maintainability index",
    }.get(m, m)


def scale_vals(vals, metric):
    if metric == "total_tokens":
        return [v / 1e6 for v in vals]
    return vals


# ── collect all results ────────────────────────────────────────────────────────

def build_results(data):
    tasks = list(data.keys())
    tools = ["Opencode", "Claudecode"]
    rows  = []

    # 1. colbPowers vs baseline per task × tool
    for task in tasks:
        for tool in tools:
            cp = extract_runs(data, task, tool, "colbPowers")
            bl = extract_runs(data, task, tool, "baseline")
            all_metrics = ["total_toolcalls", "total_tokens"]
            if any("avg_cyclomatic_complexity" in r for r in cp + bl):
                all_metrics += ["avg_cyclomatic_complexity", "mantainability_index"]
            for metric in all_metrics:
                a = [r[metric] for r in cp if metric in r]
                b = [r[metric] for r in bl if metric in r]
                t, p = welch(a, b)
                rows.append({
                    "comparison": f"{tool} – {task[:18]}",
                    "group":      "cp vs bl",
                    "metric":     metric,
                    "mean_a": np.mean(a) if a else float("nan"),
                    "mean_b": np.mean(b) if b else float("nan"),
                    "std_a":  np.std(a, ddof=1) if len(a) > 1 else 0,
                    "std_b":  np.std(b, ddof=1) if len(b) > 1 else 0,
                    "t": t, "p": p,
                    "label_a": "colbPowers",
                    "label_b": "baseline",
                })

    # 2. Opencode vs Claudecode per task × condition
    for task in tasks:
        for cond in ["colbPowers", "baseline"]:
            oc = extract_runs(data, task, "Opencode",   cond)
            cc = extract_runs(data, task, "Claudecode", cond)
            all_metrics = ["total_toolcalls", "total_tokens"]
            if any("avg_cyclomatic_complexity" in r for r in oc + cc):
                all_metrics += ["avg_cyclomatic_complexity", "mantainability_index"]
            for metric in all_metrics:
                a = [r[metric] for r in oc if metric in r]
                b = [r[metric] for r in cc if metric in r]
                t, p = welch(a, b)
                rows.append({
                    "comparison": f"{cond} – {task[:18]}",
                    "group":      "oc vs cc",
                    "metric":     metric,
                    "mean_a": np.mean(a) if a else float("nan"),
                    "mean_b": np.mean(b) if b else float("nan"),
                    "std_a":  np.std(a, ddof=1) if len(a) > 1 else 0,
                    "std_b":  np.std(b, ddof=1) if len(b) > 1 else 0,
                    "t": t, "p": p,
                    "label_a": "Opencode",
                    "label_b": "Claudecode",
                })

    # 3. Pooled colbPowers vs baseline
    for tool in tools:
        cp_all, bl_all = [], []
        for task in tasks:
            cp_all += extract_runs(data, task, tool, "colbPowers")
            bl_all += extract_runs(data, task, tool, "baseline")
        for metric in ["total_toolcalls", "total_tokens"]:
            a = [r[metric] for r in cp_all]
            b = [r[metric] for r in bl_all]
            t, p = welch(a, b)
            rows.append({
                "comparison": f"{tool} – Pooled",
                "group":      "cp vs bl (pooled)",
                "metric":     metric,
                "mean_a": np.mean(a), "mean_b": np.mean(b),
                "std_a":  np.std(a, ddof=1), "std_b": np.std(b, ddof=1),
                "t": t, "p": p,
                "label_a": "colbPowers", "label_b": "baseline",
            })
    return rows


# ── PNG figure ─────────────────────────────────────────────────────────────────

COLORS = {"colbPowers": "#4C72B0", "baseline": "#DD8452",
          "Opencode":   "#55A868", "Claudecode": "#C44E52"}

def make_bar_axes(ax, row):
    metric = row["metric"]
    scale  = 1e6 if metric == "total_tokens" else 1
    a_val  = row["mean_a"] / scale
    b_val  = row["mean_b"] / scale
    a_err  = row["std_a"]  / scale
    b_err  = row["std_b"]  / scale

    ca = COLORS.get(row["label_a"], "#4C72B0")
    cb = COLORS.get(row["label_b"], "#DD8452")

    bars = ax.bar([0, 1], [a_val, b_val], yerr=[a_err, b_err],
                  color=[ca, cb], width=0.5, capsize=4,
                  error_kw={"linewidth": 1.2})

    # significance bracket
    p   = row["p"]
    sig = sig_stars(p)
    y_max = max(a_val + a_err, b_val + b_err) * 1.12
    ax.set_ylim(0, y_max * 1.25)
    brace_y = y_max * 1.05
    ax.plot([0, 0, 1, 1], [brace_y * 0.97, brace_y, brace_y, brace_y * 0.97],
            color="black", linewidth=0.8)
    color_sig = "black" if sig == "ns" else "#c0392b"
    ax.text(0.5, brace_y * 1.02, sig, ha="center", va="bottom",
            fontsize=9, color=color_sig, fontweight="bold")

    ax.set_xticks([0, 1])
    ax.set_xticklabels([row["label_a"], row["label_b"]], rotation=15, ha="right")
    ax.set_ylabel(metric_label(metric), fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)


METRICS_ALL = [
    "total_toolcalls",
    "total_tokens",
    "avg_cyclomatic_complexity",
    "mantainability_index",
]


def _slug(text):
    """Convert a comparison label to a safe filename fragment."""
    return text.replace(" ", "_").replace("/", "_").replace("–", "-").replace("—", "-")


def make_bars_figure(rows, group_key, title, out_path, only_comparison=None):
    """Bar chart figure — one column per comparison, one row per metric.

    If only_comparison is given, restrict to that single comparison (single column).
    """
    subset      = [r for r in rows if r["group"] == group_key]
    if only_comparison:
        subset  = [r for r in subset if r["comparison"] == only_comparison]
    comparisons = sorted(set(r["comparison"] for r in subset))

    # Individual figures: metrics as columns (horizontal layout)
    # Combined figures:   comparisons as columns, metrics as rows (vertical layout)
    individual = only_comparison is not None
    if individual:
        n_rows, n_cols = 1, len(METRICS_ALL)
    else:
        n_rows, n_cols = len(METRICS_ALL), len(comparisons)

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(3.5 * n_cols, 3.2 * n_rows),
                             constrained_layout=True)
    # Normalise axes to always be 2-D array [row][col]
    if n_rows == 1 and n_cols == 1:
        axes = [[axes]]
    elif n_rows == 1:
        axes = [list(axes)]
    elif n_cols == 1:
        axes = [[axes[r]] for r in range(n_rows)]

    fig.suptitle(title, fontsize=12, fontweight="bold")

    if individual:
        comp = comparisons[0]
        for mi, metric in enumerate(METRICS_ALL):
            ax    = axes[0][mi]
            match = [r for r in subset if r["comparison"] == comp and r["metric"] == metric]
            if match:
                make_bar_axes(ax, match[0])
            else:
                ax.set_visible(False)
                continue
            ax.set_title(metric_label(metric), fontsize=9, fontweight="bold")
    else:
        for ci, comp in enumerate(comparisons):
            for mi, metric in enumerate(METRICS_ALL):
                ax    = axes[mi][ci]
                match = [r for r in subset if r["comparison"] == comp and r["metric"] == metric]
                if match:
                    make_bar_axes(ax, match[0])
                else:
                    ax.set_visible(False)
                    continue
                if mi == 0:
                    ax.set_title(comp, fontsize=9, fontweight="bold")

    fig.savefig(out_path, bbox_inches="tight")
    print(f"  Saved: {out_path}")
    plt.close(fig)


def make_table_figure(rows, group_key, title, col_a, col_b, out_path):
    """Summary table figure — means, t-stat, p-value, stars."""
    subset      = [r for r in rows if r["group"] == group_key]
    comparisons = sorted(set(r["comparison"] for r in subset))

    # Build cell data
    col_headers = ["Comparison", "Metric", f"Mean {col_a}", f"Mean {col_b}", "t", "p", "sig"]
    cell_data   = []
    for comp in comparisons:
        for metric in METRICS_ALL:
            match = [r for r in subset if r["comparison"] == comp and r["metric"] == metric]
            if not match:
                continue
            r = match[0]
            scale = 1e6 if metric == "total_tokens" else 1
            suffix = "M" if metric == "total_tokens" else ""
            ma = f"{r['mean_a']/scale:.2f}{suffix}"
            mb = f"{r['mean_b']/scale:.2f}{suffix}"
            t  = f"{r['t']:.3f}" if not np.isnan(r["t"]) else "—"
            p  = f"{r['p']:.4f}" if not np.isnan(r["p"]) else "—"
            cell_data.append([comp, metric_label(metric), ma, mb, t, p, sig_stars(r["p"])])

    n_rows = len(cell_data)
    fig_h  = max(2.5, 0.38 * n_rows + 1.0)
    fig, ax = plt.subplots(figsize=(13, fig_h))
    ax.axis("off")
    fig.suptitle(title, fontsize=12, fontweight="bold", y=1.02)

    tbl = ax.table(
        cellText=cell_data,
        colLabels=col_headers,
        loc="center",
        cellLoc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1, 1.4)

    # Style header row
    for col in range(len(col_headers)):
        tbl[0, col].set_facecolor("#2c3e50")
        tbl[0, col].set_text_props(color="white", fontweight="bold")

    # Colour significance column
    sig_col = len(col_headers) - 1
    for row_idx, row_data in enumerate(cell_data, start=1):
        sig = row_data[-1]
        color = {
            "***": "#f9ebea", "**": "#fdebd0", "*": "#fef9e7", "ns": "#ffffff"
        }.get(sig, "#ffffff")
        tbl[row_idx, sig_col].set_facecolor(color)
        # Alternate row shading
        bg = "#f2f3f4" if row_idx % 2 == 0 else "#ffffff"
        for col in range(len(col_headers) - 1):
            tbl[row_idx, col].set_facecolor(bg)
        tbl[row_idx, sig_col].set_facecolor(color)

    # Wider first two columns
    tbl.auto_set_column_width([0, 1])

    # Footer note — aligned to the left edge of the axes, not the figure
    ax.text(0.0, -0.02, "* p<0.05  ** p<0.01  *** p<0.001  ns = not significant",
            transform=ax.transAxes, fontsize=7.5, color="gray", va="top", ha="left")

    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    print(f"  Saved: {out_path}")
    plt.close(fig)


def make_png(rows):
    base = OUT_PNG.parent

    for group_key, prefix, title_combined, col_a, col_b in [
        ("cp vs bl", "cpbl",
         "colbPowers vs Baseline — bar charts by task & tool",
         "colbPowers", "baseline"),
        ("oc vs cc", "occc",
         "Opencode vs Claudecode — bar charts by condition & task",
         "Opencode", "Claudecode"),
    ]:
        # Combined figure (all comparisons)
        make_bars_figure(
            rows, group_key, title_combined,
            base / f"results_{prefix}_bars.png",
        )

        # Individual figure per comparison
        comparisons = sorted(set(r["comparison"] for r in rows if r["group"] == group_key))
        for comp in comparisons:
            slug = _slug(comp)
            make_bars_figure(
                rows, group_key,
                comp,
                base / f"results_{prefix}_bars_{slug}.png",
                only_comparison=comp,
            )

        # Summary table
        make_table_figure(
            rows, group_key,
            f"{col_a} vs {col_b} — summary table",
            col_a, col_b,
            base / f"results_{prefix}_table.png",
        )


# ── LaTeX table ────────────────────────────────────────────────────────────────

def make_latex(rows, data):
    tasks = list(data.keys())
    tools = ["Opencode", "Claudecode"]

    lines = [
        r"\usepackage{booktabs}",
        r"\usepackage{siunitx}",
        "",
        "% ---- Table 1: colbPowers vs Baseline ----",
        r"\begin{table}[ht]",
        r"  \centering",
        r"  \caption{Welch's \textit{t}-test results: colbPowers vs Baseline (n=3 per group).}",
        r"  \label{tab:ttest_cpbl}",
        r"  \begin{tabular}{llrrrl}",
        r"    \toprule",
        r"    Task & Tool & $\bar{x}_\text{cp}$ & $\bar{x}_\text{bl}$ & $t$ & $p$ \\",
        r"    \midrule",
    ]

    metric_groups = [
        ("total_toolcalls",           "Total tool calls"),
        ("total_tokens",              "Total tokens"),
        ("avg_cyclomatic_complexity", "Avg. cyclomatic complexity"),
        ("mantainability_index",      "Maintainability index"),
    ]

    for metric, mlabel in metric_groups:
        lines.append(f"    \\multicolumn{{6}}{{l}}{{\\textit{{{mlabel}}}}} \\\\")
        for task in tasks:
            for tool in tools:
                match = [r for r in rows
                         if r["group"] == "cp vs bl"
                         and metric in r["comparison"] + r["metric"]
                         and r["metric"] == metric
                         and task[:18] in r["comparison"]
                         and tool in r["comparison"]]
                if not match:
                    continue
                r  = match[0]
                ma = r["mean_a"]
                mb = r["mean_b"]
                if metric == "total_tokens":
                    ma_str = f"{ma/1e6:.2f}M"
                    mb_str = f"{mb/1e6:.2f}M"
                elif metric in ("avg_cyclomatic_complexity", "mantainability_index"):
                    ma_str = f"{ma:.2f}"
                    mb_str = f"{mb:.2f}"
                else:
                    ma_str = f"{ma:.1f}"
                    mb_str = f"{mb:.1f}"
                t_str = f"{r['t']:.3f}" if not np.isnan(r["t"]) else "—"
                p_val = r["p"]
                if np.isnan(p_val):
                    p_str = "—"
                elif p_val < 0.001:
                    p_str = r"$<$0.001***"
                elif p_val < 0.01:
                    p_str = f"{p_val:.3f}**"
                elif p_val < 0.05:
                    p_str = f"{p_val:.3f}*"
                else:
                    p_str = f"{p_val:.3f}"
                short_task = task.replace("ClassificationVisualization", "ClassVis")
                lines.append(f"    \\quad {short_task} & {tool} & {ma_str} & {mb_str} & {t_str} & {p_str} \\\\")
        lines.append(r"    \addlinespace")

    lines += [
        r"    \bottomrule",
        r"  \end{tabular}",
        r"  \begin{tablenotes}",
        r"    \small \item * $p<0.05$, ** $p<0.01$, *** $p<0.001$. ns = not significant.",
        r"  \end{tablenotes}",
        r"\end{table}",
        "",
        "% ---- Table 2: Opencode vs Claudecode ----",
        r"\begin{table}[ht]",
        r"  \centering",
        r"  \caption{Welch's \textit{t}-test results: Opencode vs Claudecode (n=3 per group).}",
        r"  \label{tab:ttest_occc}",
        r"  \begin{tabular}{llrrrl}",
        r"    \toprule",
        r"    Task & Condition & $\bar{x}_\text{OC}$ & $\bar{x}_\text{CC}$ & $t$ & $p$ \\",
        r"    \midrule",
    ]

    for metric, mlabel in metric_groups:
        lines.append(f"    \\multicolumn{{6}}{{l}}{{\\textit{{{mlabel}}}}} \\\\")
        for task in tasks:
            for cond in ["colbPowers", "baseline"]:
                match = [r for r in rows
                         if r["group"] == "oc vs cc"
                         and r["metric"] == metric
                         and task[:18] in r["comparison"]
                         and cond in r["comparison"]]
                if not match:
                    continue
                r  = match[0]
                ma = r["mean_a"]
                mb = r["mean_b"]
                if metric == "total_tokens":
                    ma_str = f"{ma/1e6:.2f}M"
                    mb_str = f"{mb/1e6:.2f}M"
                elif metric in ("avg_cyclomatic_complexity", "mantainability_index"):
                    ma_str = f"{ma:.2f}"
                    mb_str = f"{mb:.2f}"
                else:
                    ma_str = f"{ma:.1f}"
                    mb_str = f"{mb:.1f}"
                t_str = f"{r['t']:.3f}" if not np.isnan(r["t"]) else "—"
                p_val = r["p"]
                if np.isnan(p_val):
                    p_str = "—"
                elif p_val < 0.001:
                    p_str = r"$<$0.001***"
                elif p_val < 0.01:
                    p_str = f"{p_val:.3f}**"
                elif p_val < 0.05:
                    p_str = f"{p_val:.3f}*"
                else:
                    p_str = f"{p_val:.3f}"
                short_task = task.replace("ClassificationVisualization", "ClassVis")
                lines.append(f"    \\quad {short_task} & {cond} & {ma_str} & {mb_str} & {t_str} & {p_str} \\\\")
        lines.append(r"    \addlinespace")

    lines += [
        r"    \bottomrule",
        r"  \end{tabular}",
        r"  \begin{tablenotes}",
        r"    \small \item * $p<0.05$, ** $p<0.01$, *** $p<0.001$. ns = not significant.",
        r"  \end{tablenotes}",
        r"\end{table}",
    ]

    OUT_TEX.write_text("\n".join(lines))
    print(f"  Saved: {OUT_TEX}")


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    print("Building results...")
    rows = build_results(data)

    print("Generating PNG figures...")
    make_png(rows)

    print("Generating LaTeX tables...")
    make_latex(rows, data)

    print("\nDone.")


if __name__ == "__main__":
    main()

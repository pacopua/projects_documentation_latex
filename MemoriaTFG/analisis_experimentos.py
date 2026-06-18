"""
Análisis y visualización de resultados del experimento con el plugin code-review-graph.
Experimentos: Repo Existente (DCM/Dart) y ClassificationVisualization (radon/Python).
Ambos experimentos incluyen métricas de calidad de código.
Condiciones: colbPowers (con plugin) vs baseline (sin plugin), para Opencode y Claudecode.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ── colores ────────────────────────────────────────────────────────────────────
C_OPENCODE_PLUGIN   = "#2196F3"   # azul
C_OPENCODE_BASELINE = "#90CAF9"   # azul claro
C_CLAUDE_PLUGIN     = "#F44336"   # rojo
C_CLAUDE_BASELINE   = "#FFCDD2"   # rojo claro

OUTPUT_DIR = Path("graficos/comparisons")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── carga de datos ─────────────────────────────────────────────────────────────
with open("ExperimentosInfo.json", encoding="utf-8") as f:
    data = json.load(f)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def get_sessions(data, experiment, tool, condition):
    """Devuelve la lista de sesiones para una combinación dada."""
    return list(data[experiment][tool][condition].values())


def avg_field(sessions, *keys):
    """Media de un campo anidado (e.g. 'total_tokens', 'total')."""
    vals = []
    for s in sessions:
        obj = s
        for k in keys:
            obj = obj.get(k, {})
        if isinstance(obj, (int, float)):
            vals.append(obj)
    return np.mean(vals) if vals else np.nan


def avg_quality(sessions, field):
    vals = [s[field] for s in sessions if field in s]
    return np.mean(vals) if vals else np.nan


def avg_toolcalls_total(sessions):
    return avg_field(sessions, "toolcalls", "TOTAL")


def avg_subagent_count(sessions):
    vals = [len(s.get("subagents", {})) for s in sessions]
    return np.mean(vals) if vals else 0.0


def avg_crg_calls(sessions):
    vals = [s.get("code-review-graph_calls", 0) for s in sessions]
    return np.mean(vals) if vals else 0.0


def avg_orch_ratio(sessions):
    """Ratio tokens orquestador / total."""
    ratios = []
    for s in sessions:
        total = s.get("total_tokens", {}).get("total", 0)
        orch  = s.get("orchestrator_tokens", {}).get("total", 0)
        if total > 0:
            ratios.append(orch / total)
    return np.mean(ratios) if ratios else np.nan


def avg_cache_ratio(sessions):
    """Ratio tokens leídos de caché / total."""
    ratios = []
    for s in sessions:
        total = s.get("total_tokens", {}).get("total", 0)
        cr    = s.get("total_tokens", {}).get("cache", {}).get("read", 0)
        if total > 0:
            ratios.append(cr / total)
    return np.mean(ratios) if ratios else np.nan


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 1 – Métricas de calidad de código (ClassificationVisualization)
# ══════════════════════════════════════════════════════════════════════════════

def _plot_quality_single(exp, exp_label, tools, metrics, path):
    """Genera la figura 1×2 de métricas de calidad para un único experimento."""
    x = np.arange(len(tools))
    w = 0.35

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        f"Métricas de Calidad del Código — {exp_label}\n(con plugin vs. sin plugin)",
        fontsize=14, fontweight="bold"
    )

    for ax, (field, (title, subtitle, lower_better)) in zip(axes, metrics.items()):
        plugin_vals   = [avg_quality(get_sessions(data, exp, t, "colbPowers"), field) for t in tools]
        baseline_vals = [avg_quality(get_sessions(data, exp, t, "baseline"),   field) for t in tools]

        bars_p = ax.bar(x - w/2, plugin_vals,   w, color=[C_OPENCODE_PLUGIN,   C_CLAUDE_PLUGIN],
                        edgecolor="white", linewidth=1.2)
        bars_b = ax.bar(x + w/2, baseline_vals, w, color=[C_OPENCODE_BASELINE, C_CLAUDE_BASELINE],
                        edgecolor="white", linewidth=1.2)

        for bar in list(bars_p) + list(bars_b):
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.3, f"{h:.2f}",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")

        annotation_positions = []
        for pv, bv in zip(plugin_vals, baseline_vals):
            if not (np.isnan(pv) or np.isnan(bv)):
                annotation_positions.append(max(pv, bv) + 0.8)

        ax.set_title(f"{title}\n({subtitle})", fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(tools, fontsize=11)
        ax.set_ylabel(title.split()[0], fontsize=10)
        handles = [
            mpatches.Patch(color=C_OPENCODE_PLUGIN,   label="Opencode con plugin"),
            mpatches.Patch(color=C_OPENCODE_BASELINE, label="Opencode sin plugin"),
            mpatches.Patch(color=C_CLAUDE_PLUGIN,     label="Claudecode con plugin"),
            mpatches.Patch(color=C_CLAUDE_BASELINE,   label="Claudecode sin plugin"),
        ]
        ax.legend(handles=handles, fontsize=8)

        max_val = max([v for v in plugin_vals + baseline_vals if not np.isnan(v)], default=0)
        max_ann = max(annotation_positions) if annotation_positions else max_val
        ax.set_ylim(0, max_ann * 1.35)

        for i, (pv, bv) in enumerate(zip(plugin_vals, baseline_vals)):
            if np.isnan(pv) or np.isnan(bv):
                continue
            better = (pv < bv) if lower_better else (pv > bv)
            color  = "#2E7D32" if better else "#C62828"
            symbol = ("▼" if lower_better else "▲") if better else ("▲" if lower_better else "▼")
            ax.annotate(
                f"{symbol} {abs(pv - bv):.2f}",
                xy=(x[i], annotation_positions[i]),
                ha="center", fontsize=8, color=color, fontweight="bold"
            )

        ax.grid(axis="y", alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


def plot_quality_metrics():
    tools = ["Opencode", "Claudecode"]
    metrics = {
        "avg_cyclomatic_complexity": ("Complejidad Ciclomática Promedio", "lower is better", True),
        "mantainability_index":      ("Índice de Mantenibilidad Promedio",  "higher is better", False),
    }
    experiments = [
        ("Repo Existente",            "Repo Existente (DCM)",              "01_calidad_codigo_caso1.png"),
        ("ClassificationVisualization", "ClassificationVisualization (radon)", "01_calidad_codigo_caso2.png"),
    ]
    for exp, label, fname in experiments:
        _plot_quality_single(exp, label, tools, metrics, OUTPUT_DIR / fname)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 2 – Tokens totales por experimento / condición
# ══════════════════════════════════════════════════════════════════════════════

def plot_token_usage():
    experiments = ["Repo Existente", "ClassificationVisualization"]
    tools       = ["Opencode", "Claudecode"]
    conditions  = [("colbPowers", "Con plugin"), ("baseline", "Sin plugin")]

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("Uso Total de Tokens por Experimento y Condición", fontsize=14, fontweight="bold")

    x    = np.arange(len(tools))
    w    = 0.35
    cmap_p = [C_OPENCODE_PLUGIN,   C_CLAUDE_PLUGIN]
    cmap_b = [C_OPENCODE_BASELINE, C_CLAUDE_BASELINE]

    for ax, exp in zip(axes, experiments):
        plugin_vals   = [avg_field(get_sessions(data, exp, t, "colbPowers"), "total_tokens", "total") for t in tools]
        baseline_vals = [avg_field(get_sessions(data, exp, t, "baseline"),   "total_tokens", "total") for t in tools]

        bars_p = ax.bar(x - w/2, [v/1e6 for v in plugin_vals],   w,
                        label="Con plugin", color=cmap_p, edgecolor="white", linewidth=1.2)
        bars_b = ax.bar(x + w/2, [v/1e6 for v in baseline_vals], w,
                        label="Sin plugin", color=cmap_b, edgecolor="white", linewidth=1.2)

        for bar in list(bars_p) + list(bars_b):
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, f"{h:.1f}M",
                    ha="center", va="bottom", fontsize=8, fontweight="bold")

        ax.set_title(exp, fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(tools, fontsize=11)
        ax.set_ylabel("Tokens (millones)", fontsize=10)
        # Custom legend with proper color distinction
        handles = [
            mpatches.Patch(color=C_OPENCODE_PLUGIN, label="Opencode con plugin"),
            mpatches.Patch(color=C_OPENCODE_BASELINE, label="Opencode sin plugin"),
            mpatches.Patch(color=C_CLAUDE_PLUGIN, label="Claudecode con plugin"),
            mpatches.Patch(color=C_CLAUDE_BASELINE, label="Claudecode sin plugin"),
        ]
        ax.legend(handles=handles, fontsize=8, loc='upper left')
        ax.set_ylim(0, ax.get_ylim()[1] * 1.2)
        ax.grid(axis="y", alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    path = OUTPUT_DIR / "02_tokens_totales.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 3 – Desglose de tokens (input / output / cache_read) con plugin
# ══════════════════════════════════════════════════════════════════════════════

def plot_token_breakdown():
    experiments = ["Repo Existente", "ClassificationVisualization"]
    tools       = ["Opencode", "Claudecode"]
    conditions  = {"colbPowers": "Con plugin", "baseline": "Sin plugin"}

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Desglose de Tokens: Input / Output / Caché Leída", fontsize=14, fontweight="bold")

    components = [
        ("input",       "total_tokens", "input",  "#42A5F5"),
        ("output",      "total_tokens", "output", "#66BB6A"),
        ("cache_read",  "total_tokens", "cache",  "#FFA726"),
    ]

    for row, exp in enumerate(experiments):
        for col, (cond_key, cond_label) in enumerate(conditions.items()):
            ax = axes[row][col]
            x  = np.arange(len(tools))
            w  = 0.22
            offsets = np.array([-1, 0, 1]) * w

            for offset, (name, *path_and_color) in zip(offsets, components):
                path, color = path_and_color[:-1], path_and_color[-1]
                vals = []
                for t in tools:
                    sessions = get_sessions(data, exp, t, cond_key)
                    raw = [
                        s.get(path[0], {}).get(path[1], s.get(path[0], {}).get("cache", {}).get("read", 0))
                        if len(path) == 2 and path[1] != "cache"
                        else s.get(path[0], {}).get("cache", {}).get("read", 0)
                        for s in sessions
                    ]
                    vals.append(np.mean(raw) / 1e6 if raw else 0)

                bars = ax.bar(x + offset, vals, w, label=name, color=color,
                              edgecolor="white", linewidth=0.8)
                for bar in bars:
                    h = bar.get_height()
                    if h > 0.05:
                        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.1f}",
                                ha="center", va="bottom", fontsize=7)

            ax.set_title(f"{exp}\n{cond_label}", fontsize=10, fontweight="bold")
            ax.set_xticks(x)
            ax.set_xticklabels(tools, fontsize=10)
            ax.set_ylabel("Tokens (M)", fontsize=9)
            ax.legend(fontsize=8)
            ax.grid(axis="y", alpha=0.3)
            ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    path = OUTPUT_DIR / "03_desglose_tokens.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 4 – Tool calls totales y subagentes
# ══════════════════════════════════════════════════════════════════════════════

def plot_toolcalls_and_subagents():
    experiments = ["Repo Existente", "ClassificationVisualization"]
    tools       = ["Opencode", "Claudecode"]

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Tool Calls y Subagentes: Con plugin vs. Sin plugin", fontsize=14, fontweight="bold")

    x = np.arange(len(tools))
    w = 0.35
    cmap_p = [C_OPENCODE_PLUGIN,   C_CLAUDE_PLUGIN]
    cmap_b = [C_OPENCODE_BASELINE, C_CLAUDE_BASELINE]

    metrics_fns = [
        ("Tool Calls totales (orquestador)",  avg_toolcalls_total),
        ("Nº Subagentes por sesión (media)",  avg_subagent_count),
    ]

    for row, exp in enumerate(experiments):
        for col, (metric_name, fn) in enumerate(metrics_fns):
            ax = axes[row][col]
            pv = [fn(get_sessions(data, exp, t, "colbPowers")) for t in tools]
            bv = [fn(get_sessions(data, exp, t, "baseline"))   for t in tools]

            bars_p = ax.bar(x - w/2, pv, w, label="Con plugin",
                            color=cmap_p, edgecolor="white", linewidth=1.2)
            bars_b = ax.bar(x + w/2, bv, w, label="Sin plugin",
                            color=cmap_b, edgecolor="white", linewidth=1.2)

            for bar in list(bars_p) + list(bars_b):
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, h + 0.3, f"{h:.1f}",
                        ha="center", va="bottom", fontsize=9, fontweight="bold")

            ax.set_title(f"{exp}\n{metric_name}", fontsize=10, fontweight="bold")
            ax.set_xticks(x)
            ax.set_xticklabels(tools, fontsize=11)
            # Custom legend with proper color distinction
            handles = [
                mpatches.Patch(color=C_OPENCODE_PLUGIN, label="Opencode con plugin"),
                mpatches.Patch(color=C_OPENCODE_BASELINE, label="Opencode sin plugin"),
                mpatches.Patch(color=C_CLAUDE_PLUGIN, label="Claudecode con plugin"),
                mpatches.Patch(color=C_CLAUDE_BASELINE, label="Claudecode sin plugin"),
            ]
            ax.legend(handles=handles, fontsize=8)
            ax.set_ylim(0, ax.get_ylim()[1] * 1.2)
            ax.grid(axis="y", alpha=0.3)
            ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    path = OUTPUT_DIR / "04_toolcalls_subagentes.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 5 – Uso del code-review-graph
# ══════════════════════════════════════════════════════════════════════════════

def plot_crg_usage():
    experiments = ["Repo Existente", "ClassificationVisualization"]
    tools       = ["Opencode", "Claudecode"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Llamadas al Plugin code-review-graph por Condición", fontsize=14, fontweight="bold")

    x    = np.arange(len(tools))
    w    = 0.35
    cmap_p = [C_OPENCODE_PLUGIN,   C_CLAUDE_PLUGIN]
    cmap_b = [C_OPENCODE_BASELINE, C_CLAUDE_BASELINE]

    for ax, exp in zip(axes, experiments):
        pv = [avg_crg_calls(get_sessions(data, exp, t, "colbPowers")) for t in tools]
        bv = [avg_crg_calls(get_sessions(data, exp, t, "baseline"))   for t in tools]

        bars_p = ax.bar(x - w/2, pv, w, label="Con plugin",
                        color=cmap_p, edgecolor="white", linewidth=1.2)
        bars_b = ax.bar(x + w/2, bv, w, label="Sin plugin",
                        color=cmap_b, edgecolor="white", linewidth=1.2)

        for bar in list(bars_p) + list(bars_b):
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.03, f"{h:.1f}",
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

        ax.set_title(exp, fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(tools, fontsize=11)
        ax.set_ylabel("Llamadas al plugin (media)", fontsize=10)
        # Custom legend with proper color distinction
        handles = [
            mpatches.Patch(color=C_OPENCODE_PLUGIN, label="Opencode con plugin"),
            mpatches.Patch(color=C_OPENCODE_BASELINE, label="Opencode sin plugin"),
            mpatches.Patch(color=C_CLAUDE_PLUGIN, label="Claudecode con plugin"),
            mpatches.Patch(color=C_CLAUDE_BASELINE, label="Claudecode sin plugin"),
        ]
        ax.legend(handles=handles, fontsize=8)
        ax.set_ylim(0, max(max(pv), max(bv)) * 1.5 + 0.5)
        ax.grid(axis="y", alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    path = OUTPUT_DIR / "05_crg_llamadas.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 6 – Ratio caché / total y ratio orquestador / total
# ══════════════════════════════════════════════════════════════════════════════

def plot_efficiency_ratios():
    experiments = ["Repo Existente", "ClassificationVisualization"]
    tools       = ["Opencode", "Claudecode"]

    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    fig.suptitle("Ratios de Eficiencia: Caché y Distribución Orquestador/Subagentes",
                 fontsize=14, fontweight="bold")

    x    = np.arange(len(tools))
    w    = 0.35
    cmap_p = [C_OPENCODE_PLUGIN,   C_CLAUDE_PLUGIN]
    cmap_b = [C_OPENCODE_BASELINE, C_CLAUDE_BASELINE]

    metrics = [
        ("% Tokens servidos desde caché",        avg_cache_ratio),
        ("% Tokens usados por el orquestador",    avg_orch_ratio),
    ]

    for row, exp in enumerate(experiments):
        for col, (metric_name, fn) in enumerate(metrics):
            ax = axes[row][col]
            pv = [fn(get_sessions(data, exp, t, "colbPowers")) * 100 for t in tools]
            bv = [fn(get_sessions(data, exp, t, "baseline"))   * 100 for t in tools]

            bars_p = ax.bar(x - w/2, pv, w, label="Con plugin",
                            color=cmap_p, edgecolor="white", linewidth=1.2)
            bars_b = ax.bar(x + w/2, bv, w, label="Sin plugin",
                            color=cmap_b, edgecolor="white", linewidth=1.2)

            for bar in list(bars_p) + list(bars_b):
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, f"{h:.1f}%",
                        ha="center", va="bottom", fontsize=9, fontweight="bold")

            ax.set_title(f"{exp}\n{metric_name}", fontsize=10, fontweight="bold")
            ax.set_xticks(x)
            ax.set_xticklabels(tools, fontsize=11)
            ax.set_ylabel("% del total", fontsize=10)
            # Custom legend with proper color distinction
            handles = [
                mpatches.Patch(color=C_OPENCODE_PLUGIN, label="Opencode con plugin"),
                mpatches.Patch(color=C_OPENCODE_BASELINE, label="Opencode sin plugin"),
                mpatches.Patch(color=C_CLAUDE_PLUGIN, label="Claudecode con plugin"),
                mpatches.Patch(color=C_CLAUDE_BASELINE, label="Claudecode sin plugin"),
            ]
            ax.legend(handles=handles, fontsize=8)
            ax.set_ylim(0, 105)
            ax.grid(axis="y", alpha=0.3)
            ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    path = OUTPUT_DIR / "06_ratios_eficiencia.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 7 – Scatter: tokens vs calidad (ClassificationVisualization)
# ══════════════════════════════════════════════════════════════════════════════

def plot_tokens_vs_quality():
    experiments = ["Repo Existente", "ClassificationVisualization"]
    exp_labels  = ["Repo Existente (DCM)", "ClassificationVisualization (radon)"]
    tools = ["Opencode", "Claudecode"]

    quality_metrics = [
        ("avg_cyclomatic_complexity", "Complejidad Ciclomática (↓ mejor)"),
        ("mantainability_index",      "Índice Mantenibilidad (↑ mejor)"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(15, 14))
    fig.suptitle(
        "Tokens Usados vs. Calidad del Código",
        fontsize=14, fontweight="bold"
    )

    markers   = {"Opencode": "o", "Claudecode": "s"}
    palette_p = {"Opencode": C_OPENCODE_PLUGIN,   "Claudecode": C_CLAUDE_PLUGIN}
    palette_b = {"Opencode": C_OPENCODE_BASELINE,  "Claudecode": C_CLAUDE_BASELINE}

    for row, (exp, exp_label) in enumerate(zip(experiments, exp_labels)):
        for col, (field, ylabel) in enumerate(quality_metrics):
            ax = axes[row][col]
            for tool in tools:
                for cond_key, cond_label, palette in [
                    ("colbPowers", "con plugin",  palette_p),
                    ("baseline",   "sin plugin",  palette_b),
                ]:
                    sessions = get_sessions(data, exp, tool, cond_key)
                    tokens   = [s.get("total_tokens", {}).get("total", np.nan) / 1e6 for s in sessions]
                    quality  = [s.get(field, np.nan) for s in sessions]
                    ax.scatter(
                        tokens, quality,
                        marker=markers[tool],
                        color=palette[tool],
                        s=120, edgecolors="white", linewidths=1.5, zorder=3,
                        label=f"{tool} {cond_label}"
                    )
                    for i, (t, q) in enumerate(zip(tokens, quality)):
                        if not (np.isnan(t) or np.isnan(q)):
                            ax.annotate(f"{i+1}", (t, q), textcoords="offset points",
                                        xytext=(5, 4), fontsize=8, color=palette[tool])

            ax.set_xlabel("Tokens totales (millones)", fontsize=9)
            ax.set_ylabel(ylabel, fontsize=9)
            ax.set_title(f"{exp_label}\n{ylabel}", fontsize=9)
            ax.legend(fontsize=7, loc="best")
            ax.grid(alpha=0.3)
            ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    path = OUTPUT_DIR / "07_tokens_vs_calidad.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 8 – Resumen ejecutivo: mejora del plugin en calidad
# ══════════════════════════════════════════════════════════════════════════════

def _plot_delta_single(exp, exp_label, tools, metrics, path):
    """Genera la figura 1×2 de delta de calidad para un único experimento."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(
        f"Efecto del Plugin en la Calidad — {exp_label}\n"
        "(delta = plugin − baseline; verde = mejora, rojo = empeora)",
        fontsize=13, fontweight="bold"
    )

    for ax, (field, (label, lower_better)) in zip(axes, metrics.items()):
        deltas, bar_labels, colors = [], [], []
        for tool in tools:
            plugin_val   = avg_quality(get_sessions(data, exp, tool, "colbPowers"), field)
            baseline_val = avg_quality(get_sessions(data, exp, tool, "baseline"),   field)
            delta = plugin_val - baseline_val
            deltas.append(delta)
            bar_labels.append(tool)
            good = (delta < 0) if lower_better else (delta > 0)
            colors.append("#2E7D32" if good else "#C62828")

        bars = ax.barh(bar_labels, deltas, color=colors, edgecolor="white", linewidth=1.5, height=0.5)
        ax.axvline(0, color="black", linewidth=1.2, linestyle="--")

        for bar, val in zip(bars, deltas):
            x_pos = val + (0.02 if val >= 0 else -0.02)
            ha    = "left" if val >= 0 else "right"
            ax.text(x_pos, bar.get_y() + bar.get_height()/2,
                    f"{val:+.3f}", va="center", ha=ha, fontsize=11, fontweight="bold")

        ax.set_title(label, fontsize=11)
        ax.set_xlabel("Plugin − Baseline (media)", fontsize=10)
        ax.grid(axis="x", alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)
        ax.margins(y=0.15, x=0.15)

        verde = mpatches.Patch(color="#2E7D32", label="Mejora con plugin")
        rojo  = mpatches.Patch(color="#C62828", label="Empeora con plugin")
        ax.legend(handles=[verde, rojo], fontsize=9, loc="lower right")

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


def plot_summary_quality_delta():
    """Barras horizontales del delta del plugin en calidad, una figura por experimento."""
    tools = ["Opencode", "Claudecode"]
    metrics = {
        "avg_cyclomatic_complexity": ("Complejidad Ciclomática", True),
        "mantainability_index":      ("Índice de Mantenibilidad", False),
    }
    experiments = [
        ("Repo Existente",            "Repo Existente (DCM)",              "08_delta_calidad_caso1.png"),
        ("ClassificationVisualization", "ClassificationVisualization (radon)", "08_delta_calidad_caso2.png"),
    ]
    for exp, label, fname in experiments:
        _plot_delta_single(exp, label, tools, metrics, OUTPUT_DIR / fname)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 9 – Distribución de tool calls por tipo (top tools, colbPowers)
# ══════════════════════════════════════════════════════════════════════════════

def plot_toolcall_distribution():
    """Agrega los tool calls del orquestador para las sesiones con plugin."""
    experiments = ["Repo Existente", "ClassificationVisualization"]
    tools_list  = ["Opencode", "Claudecode"]
    ignore_keys = {"TOTAL"}

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Distribución de Tool Calls del Orquestador (Con Plugin)", fontsize=14, fontweight="bold")

    for row, exp in enumerate(experiments):
        for col, tool in enumerate(tools_list):
            ax = axes[row][col]
            sessions = get_sessions(data, exp, tool, "colbPowers")

            # acumular
            totals: dict = {}
            for s in sessions:
                for k, v in s.get("toolcalls", {}).items():
                    if k in ignore_keys:
                        continue
                    k_clean = k.lower()
                    totals[k_clean] = totals.get(k_clean, 0) + v

            if not totals:
                ax.set_visible(False)
                continue

            # top-10
            sorted_items = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:10]
            names  = [i[0] for i in sorted_items]
            values = [i[1] for i in sorted_items]

            # normalizar por número de sesiones
            n = len(sessions)
            values_norm = [v / n for v in values]

            colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(names)))[::-1]
            bars   = ax.barh(names[::-1], values_norm[::-1], color=colors[::-1],
                             edgecolor="white", linewidth=0.8)

            for bar, val in zip(bars, values_norm[::-1]):
                ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                        f"{val:.1f}", va="center", fontsize=8, fontweight="bold")

            ax.set_title(f"{exp} – {tool}", fontsize=11, fontweight="bold")
            ax.set_xlabel("Llamadas por sesión (media)", fontsize=9)
            ax.grid(axis="x", alpha=0.3)
            ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    path = OUTPUT_DIR / "09_distribucion_toolcalls.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# TABLA RESUMEN (texto)
# ══════════════════════════════════════════════════════════════════════════════

def print_summary_table():
    print("\n" + "="*80)
    print("RESUMEN NUMÉRICO")
    print("="*80)

    experiments = ["Repo Existente", "ClassificationVisualization"]
    tools       = ["Opencode", "Claudecode"]
    conditions  = [("colbPowers", "Plugin"), ("baseline", "Baseline")]

    for exp in experiments:
        print(f"\n-- {exp} ---------------------------------")
        has_quality = True

        header = f"{'Tool':<12} {'Condición':<10} {'Tokens(M)':>9} {'ToolCalls':>10} {'Subagentes':>11} {'CRG calls':>10}"
        if has_quality:
            header += f" {'CC avg':>8} {'MI avg':>8}"
        print(header)
        print("-" * (len(header)))

        for tool in tools:
            for cond_key, cond_label in conditions:
                sessions = get_sessions(data, exp, tool, cond_key)
                tok  = avg_field(sessions, "total_tokens", "total") / 1e6
                tc   = avg_toolcalls_total(sessions)
                subs = avg_subagent_count(sessions)
                crg  = avg_crg_calls(sessions)
                row  = f"{tool:<12} {cond_label:<10} {tok:>9.2f} {tc:>10.1f} {subs:>11.1f} {crg:>10.1f}"
                if has_quality:
                    cc = avg_quality(sessions, "avg_cyclomatic_complexity")
                    mi = avg_quality(sessions, "mantainability_index")
                    row += f" {cc:>8.2f} {mi:>8.2f}"
                print(row)

    print("\n" + "="*80 + "\n")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Generando gráficos en '{OUTPUT_DIR}/'...\n")

    print_summary_table()

    plot_quality_metrics()          # Fig 1 – CC y MI por herramienta/condición
    plot_token_usage()              # Fig 2 – tokens totales
    plot_token_breakdown()          # Fig 3 – desglose input/output/caché
    plot_toolcalls_and_subagents()  # Fig 4 – tool calls y subagentes
    plot_crg_usage()                # Fig 5 – uso del plugin
    plot_efficiency_ratios()        # Fig 6 – ratios caché y orquestador
    plot_tokens_vs_quality()        # Fig 7 – scatter tokens vs calidad
    plot_summary_quality_delta()    # Fig 8 – delta de mejora
    plot_toolcall_distribution()    # Fig 9 – distribución tool calls

    print("\nListo. Todos los gráficos guardados en la carpeta 'graficos/'.")

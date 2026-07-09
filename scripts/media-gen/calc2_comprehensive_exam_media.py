from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parents[2]
    / "frontend"
    / "public"
    / "assessments"
    / "calc2-comprehensive-review"
)

INK = "#344347"
MUTED = "#718085"
GRID = "#d8ddde"
BLUE = "#187f88"
RED = "#c75459"
FILL = "#b8ded9"
PAPER = "#f7f8f8"


def configure_axis(ax, xlim, ylim, title):
    ax.set_title(title, color=INK, fontsize=13, pad=10, fontweight="semibold")
    ax.set_facecolor(PAPER)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axhline(0, color=MUTED, linewidth=1.1)
    ax.axvline(0, color=MUTED, linewidth=1.1)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.tick_params(colors=MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)


def finish(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.patch.set_facecolor(PAPER)
    fig.savefig(
        OUTPUT_DIR / filename,
        format="svg",
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
        metadata={"Creator": "CIR Assessment Maker media generator", "Date": None},
    )
    plt.close(fig)


def blank_grid(filename, xlim, ylim, title):
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    configure_axis(ax, xlim, ylim, title)
    ax.set_xlabel("x", color=INK)
    ax.set_ylabel("y", color=INK, rotation=0, labelpad=10)
    finish(fig, filename)


def parabola_line_solution():
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    configure_axis(ax, (-4.5, 3.5), (-1, 12), "Solution: parabola and line region")
    x = np.linspace(-4.5, 3.5, 800)
    parabola = -(x**2) + 10
    line = x + 4
    region_x = np.linspace(-3, 2, 500)
    ax.fill_between(
        region_x,
        -(region_x**2) + 10,
        region_x + 4,
        color=FILL,
        alpha=0.85,
    )
    ax.plot(x, parabola, color=BLUE, linewidth=3, label=r"$y=-x^2+10$")
    ax.plot(x, line, color=RED, linewidth=3, label=r"$y=x+4$")
    ax.scatter([-3, 2], [1, 6], color=INK, s=55, zorder=5)
    ax.annotate("$(-3,1)$", (-3, 1), xytext=(-4.1, 2.2), color=INK)
    ax.annotate("$(2,6)$", (2, 6), xytext=(2.25, 7.0), color=INK)
    ax.legend(frameon=False, loc="lower center", ncol=2)
    finish(fig, "parabola-line-region-solution.svg")


def sqrt_line_solution():
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    configure_axis(ax, (-1, 14), (0, 6.5), "Solution: square-root and line region")
    x = np.linspace(-0.5, 14, 900)
    valid = x >= -0.5
    root = np.sqrt(2 * x[valid] + 1)
    line = x / 3 + 1
    region_x = np.linspace(0, 12, 500)
    ax.fill_between(
        region_x,
        np.sqrt(2 * region_x + 1),
        region_x / 3 + 1,
        color=FILL,
        alpha=0.85,
    )
    ax.plot(x[valid], root, color=BLUE, linewidth=3, label=r"$y=\sqrt{2x+1}$")
    ax.plot(x, line, color=RED, linewidth=3, label=r"$y=x/3+1$")
    ax.scatter([0, 12], [1, 5], color=INK, s=55, zorder=5)
    ax.annotate("$(0,1)$", (0, 1), xytext=(0.6, 0.45), color=INK)
    ax.annotate("$(12,5)$", (12, 5), xytext=(10.0, 5.55), color=INK)
    ax.legend(frameon=False, loc="upper left")
    finish(fig, "sqrt-line-region-solution.svg")


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.labelcolor": INK,
            "text.color": INK,
            "svg.hashsalt": "cir-calc2-comprehensive-review",
        }
    )
    blank_grid(
        "parabola-line-region-grid.svg",
        (-4.5, 3.5),
        (-1, 12),
        "Sketch the bounded region",
    )
    parabola_line_solution()
    blank_grid(
        "sqrt-line-region-grid.svg",
        (-1, 14),
        (0, 6.5),
        "Sketch the bounded region",
    )
    sqrt_line_solution()
    print(f"Generated comprehensive-review media in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

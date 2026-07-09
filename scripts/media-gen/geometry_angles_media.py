from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parents[2]
    / "frontend"
    / "public"
    / "assessments"
    / "geometry"
)

INK = "#344347"
MUTED = "#718085"
BLUE = "#187f88"
TEAL = "#25a494"
RED = "#c75459"
GOLD = "#c28b2c"
PAPER = "#f7f8f8"


def prepare_axis(ax, title):
    ax.set_title(title, color=INK, fontsize=12, pad=8, fontweight="semibold")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.05, 1.15)
    ax.set_aspect("equal")
    ax.axis("off")


def ray(ax, angle_degrees, color=INK, length=1):
    angle = np.deg2rad(angle_degrees)
    ax.plot(
        [0, length * np.cos(angle)],
        [0, length * np.sin(angle)],
        color=color,
        linewidth=2.8,
        solid_capstyle="round",
    )


def angle_arc(ax, start, end, radius=0.42, color=BLUE, label=None):
    ax.add_patch(
        Arc(
            (0, 0),
            2 * radius,
            2 * radius,
            angle=0,
            theta1=start,
            theta2=end,
            color=color,
            linewidth=2.4,
        )
    )
    if label:
        mid = np.deg2rad((start + end) / 2)
        ax.text(
            0.63 * np.cos(mid),
            0.63 * np.sin(mid),
            label,
            color=color,
            fontsize=10,
            ha="center",
            va="center",
        )


def save(fig, filename):
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


def angle_classification_examples():
    fig, axes = plt.subplots(1, 4, figsize=(10.6, 3.0))
    fig.suptitle(
        "Angle classification depends on degree measure",
        color=INK,
        fontsize=15,
        fontweight="semibold",
    )

    prepare_axis(axes[0], "Acute")
    ray(axes[0], 0)
    ray(axes[0], 45)
    angle_arc(axes[0], 0, 45, label="45°")
    axes[0].text(0, -0.82, "between 0° and 90°", color=MUTED, ha="center")

    prepare_axis(axes[1], "Right")
    ray(axes[1], 0)
    ray(axes[1], 90)
    axes[1].add_patch(
        Rectangle((0, 0), 0.28, 0.28, fill=False, edgecolor=TEAL, linewidth=2.2)
    )
    axes[1].text(0.52, 0.52, "90°", color=TEAL, ha="center")
    axes[1].text(0, -0.82, "exactly 90°", color=MUTED, ha="center")

    prepare_axis(axes[2], "Obtuse")
    ray(axes[2], 0)
    ray(axes[2], 125)
    angle_arc(axes[2], 0, 125, label="125°", color=RED)
    axes[2].text(0, -0.82, "between 90° and 180°", color=MUTED, ha="center")

    prepare_axis(axes[3], "Straight")
    ray(axes[3], 0)
    ray(axes[3], 180)
    angle_arc(axes[3], 0, 180, radius=0.38, label="180°", color=GOLD)
    axes[3].text(0, -0.82, "exactly 180°", color=MUTED, ha="center")

    fig.tight_layout(rect=(0, 0, 1, 0.88))
    save(fig, "angle-classification-examples.svg")


def angle_relationship_examples():
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 7.0))
    fig.suptitle(
        "Common angle-pair relationships",
        color=INK,
        fontsize=15,
        fontweight="semibold",
    )

    prepare_axis(axes[0, 0], "Adjacent angles")
    ray(axes[0, 0], 0)
    ray(axes[0, 0], 45, color=TEAL)
    ray(axes[0, 0], 110)
    angle_arc(axes[0, 0], 0, 45, radius=0.36, label="1")
    angle_arc(axes[0, 0], 45, 110, radius=0.52, label="2", color=RED)
    axes[0, 0].text(0, -0.86, "shared vertex and side", color=MUTED, ha="center")

    prepare_axis(axes[0, 1], "Complementary")
    ray(axes[0, 1], 0)
    ray(axes[0, 1], 30, color=TEAL)
    ray(axes[0, 1], 90)
    angle_arc(axes[0, 1], 0, 30, radius=0.36, label="30°")
    angle_arc(axes[0, 1], 30, 90, radius=0.52, label="60°", color=RED)
    axes[0, 1].text(0, -0.86, "30° + 60° = 90°", color=MUTED, ha="center")

    prepare_axis(axes[1, 0], "Supplementary")
    ray(axes[1, 0], 0)
    ray(axes[1, 0], 180)
    ray(axes[1, 0], 80, color=TEAL)
    angle_arc(axes[1, 0], 0, 80, radius=0.36, label="80°")
    angle_arc(axes[1, 0], 80, 180, radius=0.52, label="100°", color=RED)
    axes[1, 0].text(0, -0.86, "80° + 100° = 180°", color=MUTED, ha="center")

    prepare_axis(axes[1, 1], "Vertical angles and linear pairs")
    for angle in (35, 215):
        ray(axes[1, 1], angle)
    for angle in (145, 325):
        ray(axes[1, 1], angle)
    angle_arc(axes[1, 1], 35, 145, radius=0.42, label="110°", color=BLUE)
    angle_arc(axes[1, 1], 215, 325, radius=0.42, label="110°", color=BLUE)
    axes[1, 1].text(
        0,
        -0.86,
        "opposites match; neighbors sum to 180°",
        color=MUTED,
        ha="center",
        fontsize=9,
    )

    fig.tight_layout(rect=(0, 0, 1, 0.93))
    save(fig, "angle-pair-relationship-examples.svg")


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "text.color": INK,
            "svg.hashsalt": "cir-geometry-angle-media",
        }
    )
    angle_classification_examples()
    angle_relationship_examples()
    print(f"Generated angle media in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

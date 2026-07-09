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
    / "calc2-parametric-polar"
)

INK = "#344347"
MUTED = "#718085"
GRID = "#d8ddde"
BLUE = "#187f88"
TEAL = "#25a494"
RED = "#c75459"
GOLD = "#c28b2c"
FILL = "#b8ded9"
PAPER = "#f7f8f8"


def finish(fig, filename):
    fig.patch.set_facecolor(PAPER)
    fig.savefig(
        OUTPUT_DIR / filename,
        format="svg",
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
        metadata={"Creator": "CIR Assessment Maker media generator", "Date": None},
    )
    plt.close(fig)


def cartesian_ax(ax, title, equal=False):
    ax.set_title(title, color=INK, fontsize=13, pad=10, fontweight="semibold")
    ax.set_facecolor(PAPER)
    ax.axhline(0, color=MUTED, linewidth=1)
    ax.axvline(0, color=MUTED, linewidth=1)
    ax.grid(True, color=GRID, linewidth=0.8, alpha=0.8)
    ax.tick_params(colors=MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)
    if equal:
        ax.set_aspect("equal", adjustable="box")


def direction_arrow(ax, x, y, index, color=RED):
    start = max(0, min(index, len(x) - 2))
    ax.annotate(
        "",
        xy=(x[start + 1], y[start + 1]),
        xytext=(x[start], y[start]),
        arrowprops={"arrowstyle": "->", "color": color, "lw": 2.2},
    )


def derivative_components():
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    cartesian_ax(ax, "A Parametric Tangent Comes from Two Component Rates")
    t = np.linspace(-2.4, 2.6, 400)
    x = t + 0.3 * t**2
    y = 0.7 * t**2 - 0.2 * t
    ax.plot(x, y, color=BLUE, linewidth=3)
    t0 = 0.8
    x0 = t0 + 0.3 * t0**2
    y0 = 0.7 * t0**2 - 0.2 * t0
    dx = 1 + 0.6 * t0
    dy = 1.4 * t0 - 0.2
    scale = 0.75
    ax.scatter([x0], [y0], color=INK, s=45, zorder=5)
    ax.arrow(x0, y0, scale * dx, 0, width=0.015, color=GOLD, length_includes_head=True)
    ax.arrow(
        x0 + scale * dx,
        y0,
        0,
        scale * dy,
        width=0.015,
        color=RED,
        length_includes_head=True,
    )
    ax.arrow(
        x0,
        y0,
        scale * dx,
        scale * dy,
        width=0.018,
        color=TEAL,
        length_includes_head=True,
    )
    ax.text(x0 + 0.45 * scale * dx, y0 - 0.25, "horizontal rate", color=GOLD, ha="center")
    ax.text(x0 + scale * dx + 0.12, y0 + 0.45 * scale * dy, "vertical rate", color=RED)
    ax.text(x0 + 0.18 * scale * dx, y0 + 0.92 * scale * dy, "tangent direction", color=TEAL)
    ax.set_xlim(-2.2, 4.4)
    ax.set_ylim(-0.8, 4.8)
    finish(fig, "parametric-derivative-components.svg")


def concavity_and_second_derivative():
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.9), sharey=True)
    x = np.linspace(-2.2, 2.2, 300)
    for ax, sign, title in (
        (axes[0], 1, "Tangent slopes increase"),
        (axes[1], -1, "Tangent slopes decrease"),
    ):
        cartesian_ax(ax, title)
        y = sign * (0.45 * x**2) + (0.25 if sign > 0 else 2.6)
        ax.plot(x, y, color=BLUE, linewidth=3)
        for x0 in (-1.25, 0, 1.25):
            y0 = sign * 0.45 * x0**2 + (0.25 if sign > 0 else 2.6)
            slope = sign * 0.9 * x0
            segment = np.linspace(x0 - 0.45, x0 + 0.45, 20)
            ax.plot(segment, y0 + slope * (segment - x0), color=RED, linewidth=1.8)
            ax.scatter([x0], [y0], color=INK, s=24, zorder=4)
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-0.2, 3.3)
    fig.suptitle("Concavity Tracks How the Tangent Direction Changes", color=INK, fontsize=14, fontweight="semibold")
    fig.subplots_adjust(top=0.76, wspace=0.18)
    finish(fig, "parametric-second-derivative-concavity.svg")


def horizontal_vertical_tangents():
    fig, ax = plt.subplots(figsize=(6.2, 5))
    cartesian_ax(ax, "Horizontal and Vertical Tangent Locations", equal=True)
    theta = np.linspace(0, 2 * np.pi, 600)
    x = 2.6 * np.cos(theta)
    y = 1.7 * np.sin(theta)
    ax.plot(x, y, color=BLUE, linewidth=3)
    ax.plot([-1.1, 1.1], [1.7, 1.7], color=RED, linewidth=2.4)
    ax.plot([-1.1, 1.1], [-1.7, -1.7], color=RED, linewidth=2.4)
    ax.plot([2.6, 2.6], [-1.1, 1.1], color=GOLD, linewidth=2.4)
    ax.plot([-2.6, -2.6], [-1.1, 1.1], color=GOLD, linewidth=2.4)
    ax.scatter([0, 0, 2.6, -2.6], [1.7, -1.7, 0, 0], color=INK, s=35, zorder=5)
    ax.text(0, 2.02, "horizontal", color=RED, ha="center")
    ax.text(2.88, 0, "vertical", color=GOLD, va="center", rotation=90)
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-2.5, 2.5)
    finish(fig, "parametric-horizontal-vertical-tangents.svg")


def speed_and_arc_length():
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    cartesian_ax(ax, "Instantaneous Motion and Accumulated Path Length")
    t = np.linspace(0, 5.4, 500)
    x = t
    y = 0.55 * np.sin(1.35 * t) + 0.2 * t
    ax.plot(x, y, color=GRID, linewidth=7, solid_capstyle="round")
    ax.plot(x, y, color=BLUE, linewidth=3)
    cutoff = 305
    ax.plot(x[:cutoff], y[:cutoff], color=TEAL, linewidth=5, solid_capstyle="round")
    i = 305
    dx = 1
    dy = 0.55 * 1.35 * np.cos(1.35 * t[i]) + 0.2
    ax.arrow(x[i], y[i], 0.85 * dx, 0.85 * dy, color=RED, width=0.018, length_includes_head=True)
    ax.text(x[i] + 0.65, y[i] + 0.45, "velocity vector", color=RED)
    ax.text(1.35, 1.08, "distance accumulated along the path", color=TEAL)
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.8, 2.0)
    finish(fig, "parametric-speed-arc-length.svg")


def surface_revolution_axes():
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4.2))
    x = np.linspace(0.2, 3.5, 300)
    y = 0.55 + 0.55 * np.sqrt(x)
    for ax, axis_name in zip(axes, ("x-axis", "y-axis")):
        cartesian_ax(ax, f"Revolution about the {axis_name}")
        ax.plot(x, y, color=BLUE, linewidth=3)
        ax.fill_between(x, 0, y, color=FILL, alpha=0.32)
        if axis_name == "x-axis":
            j = 190
            ax.plot([x[j], x[j]], [0, y[j]], color=RED, linewidth=2.4)
            ax.text(x[j] + 0.1, y[j] / 2, "radius from x-axis", color=RED, rotation=90, va="center")
            ax.annotate("", xy=(3.0, -0.25), xytext=(2.2, -0.25), arrowprops={"arrowstyle": "->", "color": GOLD, "lw": 2})
        else:
            j = 190
            ax.plot([0, x[j]], [y[j], y[j]], color=RED, linewidth=2.4)
            ax.text(x[j] / 2, y[j] + 0.12, "radius from y-axis", color=RED, ha="center")
            ax.annotate("", xy=(-0.18, 1.9), xytext=(-0.18, 1.15), arrowprops={"arrowstyle": "->", "color": GOLD, "lw": 2})
        ax.set_xlim(-0.45, 4.0)
        ax.set_ylim(-0.45, 2.35)
    fig.suptitle("The Axis of Revolution Determines the Radius Factor", color=INK, fontsize=14, fontweight="semibold")
    fig.subplots_adjust(top=0.78, wspace=0.2)
    finish(fig, "parametric-surface-revolution-axes.svg")


def circle_ellipse_direction():
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 4.1))
    theta = np.linspace(0, 2 * np.pi, 600)
    for ax, a, b, title in (
        (axes[0], 2.0, 2.0, "Circle"),
        (axes[1], 2.7, 1.45, "Ellipse"),
    ):
        cartesian_ax(ax, title, equal=True)
        x = a * np.cos(theta)
        y = b * np.sin(theta)
        ax.plot(x, y, color=BLUE, linewidth=3)
        for fraction in (0.08, 0.34, 0.6, 0.84):
            direction_arrow(ax, x, y, int(fraction * (len(theta) - 2)))
        ax.scatter([a, 0, -a, 0], [0, b, 0, -b], color=INK, s=24, zorder=4)
        ax.set_xlim(-3.25, 3.25)
        ax.set_ylim(-2.6, 2.6)
    fig.suptitle("A Parameter Traces Position and Direction", color=INK, fontsize=14, fontweight="semibold")
    finish(fig, "parametric-circle-ellipse-direction.svg")


def line_segment_interpolation():
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    cartesian_ax(ax, "A Parameter Moves Between Two Endpoints")
    start = np.array([-2.0, -0.8])
    end = np.array([3.4, 2.2])
    ax.plot([start[0], end[0]], [start[1], end[1]], color=BLUE, linewidth=4)
    for value in (0, 0.25, 0.5, 0.75, 1):
        point = (1 - value) * start + value * end
        ax.scatter([point[0]], [point[1]], color=RED if value in (0, 1) else TEAL, s=48, zorder=4)
        ax.text(point[0], point[1] + 0.28, f"t={value:g}", color=INK, ha="center")
    ax.annotate("", xy=(1.45, 1.25), xytext=(0.65, 0.8), arrowprops={"arrowstyle": "->", "color": GOLD, "lw": 2.4})
    ax.text(start[0], start[1] - 0.4, "start", color=MUTED, ha="center")
    ax.text(end[0], end[1] - 0.4, "end", color=MUTED, ha="center")
    ax.set_xlim(-2.8, 4.2)
    ax.set_ylim(-1.6, 3.0)
    finish(fig, "parametric-line-segment-interpolation.svg")


def elimination_correspondence():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    cartesian_ax(ax, "Different Parameter Values Land on One Cartesian Curve")
    t = np.linspace(-2.2, 2.2, 500)
    x = t + 1
    y = t**2
    ax.plot(x, y, color=BLUE, linewidth=3)
    for value, color in ((-2, RED), (-1, GOLD), (0, TEAL), (1, GOLD), (2, RED)):
        px = value + 1
        py = value**2
        ax.scatter([px], [py], color=color, s=45, zorder=4)
        ax.text(px + 0.08, py + 0.25, f"t={value}", color=color)
    direction_arrow(ax, x, y, 120)
    direction_arrow(ax, x, y, 360)
    ax.text(2.35, 3.7, "Eliminating t keeps the traced path", color=INK, ha="center")
    ax.set_xlim(-1.7, 3.7)
    ax.set_ylim(-0.5, 5.4)
    finish(fig, "parametric-elimination-correspondence.svg")


def semicircle_elimination():
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    cartesian_ax(ax, "Upper Semicircle Traced as t Increases", equal=True)
    t = np.linspace(0, np.pi, 500)
    x = 3 * np.cos(t)
    y = 3 * np.sin(t)
    ax.plot(x, y, color=BLUE, linewidth=3.5)
    ax.scatter([3, 0, -3], [0, 3, 0], color=[RED, TEAL, RED], s=50, zorder=4)
    ax.text(3, -0.45, "t=0", color=RED, ha="center")
    ax.text(0, 3.25, "t=pi/2", color=TEAL, ha="center")
    ax.text(-3, -0.45, "t=pi", color=RED, ha="center")
    direction_arrow(ax, x, y, 95)
    direction_arrow(ax, x, y, 340)
    ax.set_xlim(-3.8, 3.8)
    ax.set_ylim(-0.8, 3.8)
    finish(fig, "parametric-semicircle-elimination.svg")


def particle_intersection():
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    cartesian_ax(ax, "Path Intersection Does Not Automatically Mean Collision")
    t1 = np.linspace(-2.3, 3.4, 600)
    x1 = t1
    y1 = t1**2
    t2 = np.linspace(-1.2, 2.3, 500)
    x2 = 3 * t2 - 2
    y2 = t2 + 2
    ax.plot(x1, y1, color=BLUE, linewidth=3, label="Particle A path")
    ax.plot(x2, y2, color=RED, linewidth=3, label="Particle B path")
    roots = np.roots([3, -1, -8])
    for root in roots:
        ax.scatter([root], [root**2], color=GOLD, s=65, edgecolor=INK, zorder=5)
    ax.scatter([1], [1], color=BLUE, s=48, zorder=5)
    ax.scatter([1], [3], color=RED, s=48, zorder=5)
    ax.plot([1, 1], [1, 3], color=MUTED, linestyle="--", linewidth=1.4)
    ax.text(1.15, 2.0, "same time, different positions", color=MUTED)
    ax.text(-1.85, 4.2, "geometric intersections", color=GOLD)
    ax.legend(frameon=False, loc="upper right")
    ax.set_xlim(-2.5, 4.2)
    ax.set_ylim(-0.5, 7.4)
    finish(fig, "parametric-particle-intersection.svg")


def derivative_analysis():
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    cartesian_ax(ax, "Tangents on x=t^2, y=t^3-3t")
    t = np.linspace(-2.0, 2.0, 800)
    x = t**2
    y = t**3 - 3 * t
    ax.plot(x, y, color=BLUE, linewidth=3)
    for value, label, color in ((-1, "horizontal", RED), (0, "vertical", GOLD), (1, "horizontal", RED)):
        px = value**2
        py = value**3 - 3 * value
        ax.scatter([px], [py], color=color, s=55, zorder=5)
        if value == 0:
            ax.plot([0, 0], [-1.0, 1.0], color=GOLD, linewidth=2.3)
            ax.text(0.15, 0, label, color=color, va="center")
        else:
            ax.plot([px - 0.75, px + 0.75], [py, py], color=RED, linewidth=2.3)
            ax.text(px + 0.15, py + 0.25, f"{label}, t={value}", color=color)
    ax.set_xlim(-0.45, 4.4)
    ax.set_ylim(-3.2, 3.2)
    finish(fig, "parametric-derivative-analysis.svg")


def cycloid_area():
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    cartesian_ax(ax, "Area Under One Cycloid Arch")
    t = np.linspace(0, 2 * np.pi, 800)
    x = t - np.sin(t)
    y = 1 - np.cos(t)
    ax.plot(x, y, color=BLUE, linewidth=3.2)
    ax.fill_between(x, 0, y, color=FILL, alpha=0.7)
    ax.scatter([0, np.pi, 2 * np.pi], [0, 2, 0], color=[RED, TEAL, RED], s=45, zorder=4)
    ax.text(0, -0.28, "t=0", color=RED, ha="center")
    ax.text(np.pi, 2.18, "t=pi", color=TEAL, ha="center")
    ax.text(2 * np.pi, -0.28, "t=2pi", color=RED, ha="center")
    direction_arrow(ax, x, y, 250)
    ax.text(np.pi, 0.55, "region accumulated by y dx", color=INK, ha="center")
    ax.set_xlim(-0.45, 6.75)
    ax.set_ylim(-0.5, 2.55)
    finish(fig, "parametric-cycloid-area.svg")


def involute_arc_length():
    fig, ax = plt.subplots(figsize=(6.7, 5.2))
    cartesian_ax(ax, "Arc Traced by the Parametric Involute", equal=True)
    t = np.linspace(0, np.pi, 800)
    x = np.cos(t) + t * np.sin(t)
    y = np.sin(t) - t * np.cos(t)
    ax.plot(x, y, color=GRID, linewidth=8, solid_capstyle="round")
    ax.plot(x, y, color=BLUE, linewidth=3.2)
    direction_arrow(ax, x, y, 210)
    direction_arrow(ax, x, y, 570)
    ax.scatter([x[0], x[-1]], [y[0], y[-1]], color=RED, s=50, zorder=4)
    ax.text(x[0] + 0.15, y[0] - 0.25, "t=0", color=RED)
    ax.text(x[-1] - 0.15, y[-1] + 0.2, "t=pi", color=RED, ha="right")
    ax.text(0.6, 2.1, "length follows the curve, not the endpoint chord", color=INK, ha="center")
    ax.set_xlim(-3.8, 2.0)
    ax.set_ylim(-1.0, 3.7)
    finish(fig, "parametric-involute-arc-length.svg")


def polar_area_between_curves():
    fig = plt.figure(figsize=(6.5, 6.0))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_title("Inside the Circle and Outside the Limacon", color=INK, fontsize=13, pad=18, fontweight="semibold")
    ax.set_facecolor(PAPER)
    theta = np.linspace(0, 2 * np.pi, 1400)
    circle = 3 * np.sin(theta)
    limacon = 1 + np.sin(theta)
    ax.plot(theta, circle, color=BLUE, linewidth=3, label=r"$r=3\sin\theta$")
    ax.plot(theta, limacon, color=RED, linewidth=3, label=r"$r=1+\sin\theta$")
    region_theta = np.linspace(np.pi / 6, 5 * np.pi / 6, 700)
    ax.fill_between(
        region_theta,
        1 + np.sin(region_theta),
        3 * np.sin(region_theta),
        color=FILL,
        alpha=0.82,
        label="target region",
    )
    ax.scatter([np.pi / 6, 5 * np.pi / 6], [1.5, 1.5], color=GOLD, s=42, zorder=5)
    ax.grid(True, color=GRID, alpha=0.8)
    ax.set_rticks([])
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, -0.16), ncol=2)
    finish(fig, "polar-area-between-curves.svg")


def polar_limacon_inner_loop():
    fig = plt.figure(figsize=(6.3, 6.0))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_title(r"Inner-Loop Limacon: $r=1-2\sin\theta$", color=INK, fontsize=13, pad=18, fontweight="semibold")
    ax.set_facecolor(PAPER)
    theta = np.linspace(0, 2 * np.pi, 1600)
    r = 1 - 2 * np.sin(theta)
    ax.plot(theta, r, color=BLUE, linewidth=3)
    roots = np.array([np.pi / 6, 5 * np.pi / 6])
    ax.scatter(roots, np.zeros_like(roots), color=RED, s=55, zorder=5)
    ax.annotate("pole crossings", xy=(np.pi / 6, 0.08), xytext=(0.08, 2.65), color=RED, arrowprops={"arrowstyle": "->", "color": RED})
    ax.grid(True, color=GRID, alpha=0.8)
    ax.set_rticks([])
    finish(fig, "polar-limacon-inner-loop.svg")


def polar_circle_intersections():
    fig = plt.figure(figsize=(6.4, 6.0))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_title("Two Polar Circles Share the Pole and One Nonzero Point", color=INK, fontsize=12.5, pad=18, fontweight="semibold")
    ax.set_facecolor(PAPER)
    theta = np.linspace(0, 2 * np.pi, 1600)
    r1 = 3 * np.sin(theta)
    r2 = 3 * np.cos(theta)
    ax.plot(theta, r1, color=BLUE, linewidth=3, label=r"$r=3\sin\theta$")
    ax.plot(theta, r2, color=RED, linewidth=3, label=r"$r=3\cos\theta$")
    nonzero_r = 3 * np.sqrt(2) / 2
    ax.scatter([np.pi / 4], [nonzero_r], color=GOLD, s=65, edgecolor=INK, zorder=5)
    ax.scatter([0], [0], color=INK, s=55, zorder=5)
    ax.text(np.pi / 4, nonzero_r + 0.38, "shared nonzero point", color=GOLD, ha="center")
    ax.grid(True, color=GRID, alpha=0.8)
    ax.set_rticks([])
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, -0.14), ncol=2)
    finish(fig, "polar-circle-intersections.svg")


def polar_tangent_negative_radius():
    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    cartesian_ax(ax, r"Tangent to $r=1-5\cos\theta$ at $\theta=\pi/4$", equal=True)

    theta = np.linspace(0, 2 * np.pi, 1800)
    radius = 1 - 5 * np.cos(theta)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color=BLUE, linewidth=3)

    theta0 = np.pi / 4
    radius0 = 1 - 5 * np.sqrt(2) / 2
    point_x = radius0 * np.cos(theta0)
    point_y = radius0 * np.sin(theta0)
    slope = (1 + 5 * np.sqrt(2)) / 49

    ray = np.linspace(-4.7, 4.7, 100)
    ax.plot(
        ray * np.cos(theta0),
        ray * np.sin(theta0),
        color=MUTED,
        linewidth=1.5,
        linestyle="--",
    )
    ax.annotate(
        "",
        xy=(3.25 * np.cos(theta0), 3.25 * np.sin(theta0)),
        xytext=(0, 0),
        arrowprops={"arrowstyle": "->", "color": GOLD, "lw": 2},
    )
    ax.text(2.45, 1.85, r"$\theta=\pi/4$ ray", color=GOLD, ha="center")

    tangent_x = np.linspace(point_x - 2.6, point_x + 2.8, 100)
    tangent_y = point_y + slope * (tangent_x - point_x)
    ax.plot(tangent_x, tangent_y, color=RED, linewidth=2.6, label="tangent line")
    ax.scatter([point_x], [point_y], color=RED, edgecolor=INK, s=75, zorder=5)
    ax.annotate(
        "negative r places the point\nopposite the named ray",
        xy=(point_x, point_y),
        xytext=(-5.6, -0.3),
        color=INK,
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1.5},
        ha="left",
    )
    ax.text(point_x - 0.1, point_y - 0.55, "evaluation point", color=RED, ha="center")

    ax.set_xlim(-6.2, 4.5)
    ax.set_ylim(-5.7, 5.1)
    ax.legend(frameon=False, loc="upper left")
    finish(fig, "polar-tangent-limacon-1-minus-5cos.svg")


def polar_cardioid_horizontal_vertical_tangents():
    fig, ax = plt.subplots(figsize=(7.4, 5.8))
    cartesian_ax(ax, r"Tangents on $r=1-\sin\theta$", equal=True)

    theta = np.linspace(0, 2 * np.pi, 1800)
    radius = 1 - np.sin(theta)
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), color=MUTED, linewidth=2)

    interval = np.linspace(-np.pi / 4, np.pi / 4, 500)
    interval_radius = 1 - np.sin(interval)
    ax.plot(
        interval_radius * np.cos(interval),
        interval_radius * np.sin(interval),
        color=BLUE,
        linewidth=4,
        label=r"traced for $-\pi/4\leq\theta\leq\pi/4$",
    )

    horizontal = (np.sqrt(3) / 4, 1 / 4)
    vertical = (3 * np.sqrt(3) / 4, -3 / 4)
    ax.plot(
        [horizontal[0] - 0.65, horizontal[0] + 0.65],
        [horizontal[1], horizontal[1]],
        color=RED,
        linewidth=2.6,
    )
    ax.plot(
        [vertical[0], vertical[0]],
        [vertical[1] - 0.65, vertical[1] + 0.65],
        color=GOLD,
        linewidth=2.6,
    )
    ax.scatter(
        [horizontal[0], vertical[0]],
        [horizontal[1], vertical[1]],
        color=[RED, GOLD],
        edgecolor=INK,
        s=75,
        zorder=5,
    )
    ax.annotate(
        r"horizontal: $\theta=\pi/6$",
        xy=horizontal,
        xytext=(-0.8, 0.95),
        arrowprops={"arrowstyle": "->", "color": RED},
        color=RED,
    )
    ax.annotate(
        r"vertical: $\theta=-\pi/6$",
        xy=vertical,
        xytext=(1.55, -1.65),
        arrowprops={"arrowstyle": "->", "color": GOLD},
        color=GOLD,
    )
    ax.set_xlim(-0.9, 2.25)
    ax.set_ylim(-2.15, 1.15)
    ax.legend(frameon=False, loc="lower left")
    finish(fig, "polar-cardioid-horizontal-vertical-tangents.svg")


def polar_limacon_total_area():
    fig, ax = plt.subplots(figsize=(7.2, 5.7))
    cartesian_ax(ax, r"Area enclosed by $r=9+3\cos\theta$", equal=True)

    theta = np.linspace(0, 2 * np.pi, 1800)
    radius = 9 + 3 * np.cos(theta)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.fill(x, y, color=FILL, alpha=0.65)
    ax.plot(x, y, color=BLUE, linewidth=3)

    upper = np.linspace(0, np.pi, 900)
    upper_radius = 9 + 3 * np.cos(upper)
    upper_x = np.concatenate(([0], upper_radius * np.cos(upper), [0]))
    upper_y = np.concatenate(([0], upper_radius * np.sin(upper), [0]))
    ax.fill(upper_x, upper_y, color=GOLD, alpha=0.28, label=r"$0\leq\theta\leq\pi$")
    ax.annotate(
        "reflect across the polar axis",
        xy=(-4.2, 4.4),
        xytext=(-6.8, 7.2),
        arrowprops={"arrowstyle": "->", "color": MUTED},
        color=INK,
        ha="left",
    )
    ax.text(3.5, 4.8, "upper half determines\nthe lower half", color=INK, ha="center")
    ax.set_xlim(-7.4, 12.8)
    ax.set_ylim(-10.3, 10.3)
    ax.legend(frameon=False, loc="lower right")
    finish(fig, "polar-limacon-9-plus-3cos-area.svg")


def polar_rose_one_leaf_area():
    fig, ax = plt.subplots(figsize=(6.7, 6.3))
    cartesian_ax(ax, r"One leaf of $r=6\sin(6\theta)$", equal=True)

    theta = np.linspace(0, 2 * np.pi, 4200)
    radius = 6 * np.sin(6 * theta)
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), color=MUTED, linewidth=1.8)

    leaf_theta = np.linspace(0, np.pi / 6, 500)
    leaf_radius = 6 * np.sin(6 * leaf_theta)
    leaf_x = np.concatenate(([0], leaf_radius * np.cos(leaf_theta), [0]))
    leaf_y = np.concatenate(([0], leaf_radius * np.sin(leaf_theta), [0]))
    ax.fill(leaf_x, leaf_y, color=FILL, alpha=0.9)
    ax.plot(leaf_radius * np.cos(leaf_theta), leaf_radius * np.sin(leaf_theta), color=BLUE, linewidth=3.5)
    maximum_theta = np.pi / 12
    ax.scatter(
        [6 * np.cos(maximum_theta)],
        [6 * np.sin(maximum_theta)],
        color=RED,
        edgecolor=INK,
        s=65,
        zorder=5,
    )
    ax.annotate(
        r"one leaf: $0\leq\theta\leq\pi/6$",
        xy=(5.2, 1.4),
        xytext=(6.0, 4.5),
        arrowprops={"arrowstyle": "->", "color": BLUE},
        color=BLUE,
        ha="center",
    )
    ax.text(6.0, -4.8, r"maximum radius at $\theta=\pi/12$", color=RED, ha="center")
    ax.set_xlim(-6.9, 7.8)
    ax.set_ylim(-6.9, 6.9)
    finish(fig, "polar-rose-6sin6theta-one-leaf.svg")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.labelcolor": INK,
            "text.color": INK,
            "svg.hashsalt": "cir-parametric-polar-media",
        }
    )

    derivative_components()
    concavity_and_second_derivative()
    horizontal_vertical_tangents()
    speed_and_arc_length()
    surface_revolution_axes()
    circle_ellipse_direction()
    line_segment_interpolation()
    elimination_correspondence()
    semicircle_elimination()
    particle_intersection()
    derivative_analysis()
    cycloid_area()
    involute_arc_length()
    polar_area_between_curves()
    polar_limacon_inner_loop()
    polar_circle_intersections()
    polar_tangent_negative_radius()
    polar_cardioid_horizontal_vertical_tangents()
    polar_limacon_total_area()
    polar_rose_one_leaf_area()

    print(f"Generated parametric/polar media in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

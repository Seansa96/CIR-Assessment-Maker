import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def setup_polar_ax(title):
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_title(title, fontsize=14, pad=18)
    ax.grid(True, linestyle="--", alpha=0.45)
    ax.set_rticks([])
    ax.set_facecolor("#fbfbfb")
    return fig, ax


def plot_family(filename, title, curves, rmax=None):
    theta = np.linspace(0, 2 * np.pi, 1600)
    fig, ax = setup_polar_ax(title)
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]
    for index, (label, fn) in enumerate(curves):
        r = fn(theta)
        ax.plot(theta, r, linewidth=2.5, color=colors[index % len(colors)], label=label)
    if rmax:
        ax.set_rlim(0, rmax)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=1, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, filename), format="svg")
    plt.close(fig)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plot_family(
        "polar-circles.svg",
        "Common Polar Circles",
        [
            (r"$r=3$", lambda t: np.full_like(t, 3.0)),
            (r"$r=4\cos\theta$", lambda t: 4 * np.cos(t)),
            (r"$r=4\sin\theta$", lambda t: 4 * np.sin(t)),
        ],
        rmax=4.5,
    )

    plot_family(
        "polar-cardioids.svg",
        "Cardioids",
        [
            (r"$r=2+2\cos\theta$", lambda t: 2 + 2 * np.cos(t)),
            (r"$r=2-2\cos\theta$", lambda t: 2 - 2 * np.cos(t)),
            (r"$r=2+2\sin\theta$", lambda t: 2 + 2 * np.sin(t)),
            (r"$r=2-2\sin\theta$", lambda t: 2 - 2 * np.sin(t)),
        ],
        rmax=4.5,
    )

    plot_family(
        "polar-limacons.svg",
        "Limacon Types",
        [
            (r"inner loop: $r=1+2\cos\theta$", lambda t: 1 + 2 * np.cos(t)),
            (r"dimpled: $r=2+3\cos\theta$", lambda t: 2 + 3 * np.cos(t)),
            (r"convex: $r=4+\cos\theta$", lambda t: 4 + np.cos(t)),
        ],
        rmax=5.5,
    )

    plot_family(
        "polar-roses.svg",
        "Rose Curves",
        [
            (r"$r=3\cos(3\theta)$", lambda t: 3 * np.cos(3 * t)),
            (r"$r=3\cos(4\theta)$", lambda t: 3 * np.cos(4 * t)),
        ],
        rmax=3.5,
    )

    plot_family(
        "polar-conics.svg",
        "Polar Conics with Focus at the Pole",
        [
            (r"ellipse: $r=\frac{2}{1+0.5\cos\theta}$", lambda t: 2 / (1 + 0.5 * np.cos(t))),
            (r"parabola: $r=\frac{2}{1+\cos\theta}$", lambda t: 2 / (1 + np.cos(t))),
            (r"hyperbola: $r=\frac{2}{1+1.4\cos\theta}$", lambda t: 2 / (1 + 1.4 * np.cos(t))),
        ],
        rmax=9,
    )


if __name__ == "__main__":
    main()

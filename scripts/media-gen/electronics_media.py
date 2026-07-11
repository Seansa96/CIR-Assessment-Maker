from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

OUTPUT_DIR = (
    Path(__file__).resolve().parents[2]
    / "frontend"
    / "public"
    / "assessments"
    / "electronics-and-circuits"
)

INK = "#344347"
MUTED = "#718085"
BLUE = "#187f88"
TEAL = "#25a494"
RED = "#c75459"
GOLD = "#c28b2c"
PAPER = "#f7f8f8"

def prepare_axis(ax, title=None):
    if title:
        ax.set_title(title, color=INK, fontsize=12, pad=8, fontweight="semibold")
    ax.set_aspect("equal")
    ax.axis("off")

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

def draw_opamp():
    fig, ax = plt.subplots(figsize=(4, 3))
    prepare_axis(ax, "Ideal Operational Amplifier")
    
    ax.set_xlim(-2, 4)
    ax.set_ylim(-3, 3)
    
    # Draw triangle
    triangle = patches.Polygon([[0, 2], [0, -2], [3, 0]], closed=True, fill=False, edgecolor=INK, linewidth=2)
    ax.add_patch(triangle)
    
    # Terminals
    ax.plot([-1.5, 0], [1, 1], color=INK, linewidth=2)   # Inverting (-)
    ax.plot([-1.5, 0], [-1, -1], color=INK, linewidth=2) # Non-inverting (+)
    ax.plot([3, 4], [0, 0], color=INK, linewidth=2)      # Output
    
    # Plus/Minus signs inside
    ax.text(0.3, 1, "-", color=INK, fontsize=16, ha="left", va="center", fontweight="bold")
    ax.text(0.3, -1, "+", color=INK, fontsize=16, ha="left", va="center", fontweight="bold")
    
    # Labels
    ax.text(-1.8, 1, "$v_-$", color=BLUE, fontsize=14, ha="right", va="center")
    ax.text(-1.8, -1, "$v_+$", color=BLUE, fontsize=14, ha="right", va="center")
    ax.text(4.2, 0, "$v_{out}$", color=RED, fontsize=14, ha="left", va="center")
    
    save(fig, "opamp-ideal.svg")

def draw_rc_response():
    fig, ax = plt.subplots(figsize=(5, 3.5))
    if "title":
        ax.set_title("First-Order RC Step Response", color=INK, fontsize=12, pad=8, fontweight="semibold")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(INK)
    ax.spines['left'].set_color(INK)
    ax.tick_params(colors=INK)
    
    t = np.linspace(0, 5, 200)
    v_c = 1 - np.exp(-t)
    
    ax.plot(t, v_c, color=BLUE, linewidth=2.5, label="$v_c(t)$")
    ax.axhline(1, color=MUTED, linestyle="--", linewidth=1.5, label="Final Value")
    
    # Mark time constant tau
    ax.plot([1, 1], [0, 1 - np.exp(-1)], color=RED, linestyle=":", linewidth=1.5)
    ax.text(1, -0.05, r"$\tau$", color=RED, fontsize=12, ha="center", va="top")
    ax.text(-0.1, 1 - np.exp(-1), "0.632", color=RED, fontsize=10, ha="right", va="center")
    
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1.1)
    ax.set_xlabel("Time $t/\\tau$", color=INK, fontsize=10)
    ax.set_ylabel("Voltage $v(t)/V_s$", color=INK, fontsize=10)
    ax.legend(frameon=False, loc="lower right")
    
    save(fig, "rc-step-response.svg")

def draw_rlc_response():
    fig, ax = plt.subplots(figsize=(5, 3.5))
    if "title":
        ax.set_title("RLC Natural Response", color=INK, fontsize=12, pad=8, fontweight="semibold")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(INK)
    ax.spines['left'].set_color(INK)
    ax.tick_params(colors=INK)
    
    t = np.linspace(0, 10, 500)
    # Underdamped
    v_under = np.exp(-0.3*t) * np.cos(2*t)
    # Critically damped
    v_crit = (1 + 2*t) * np.exp(-t)
    # Overdamped
    v_over = 1.2*np.exp(-0.5*t) - 0.2*np.exp(-2*t)
    
    ax.plot(t, v_under, color=BLUE, linewidth=2, label="Underdamped")
    ax.plot(t, v_crit, color=TEAL, linewidth=2, label="Critically Damped")
    ax.plot(t, v_over, color=GOLD, linewidth=2, label="Overdamped")
    
    ax.set_xlim(0, 10)
    ax.set_xlabel("Time $t$", color=INK, fontsize=10)
    ax.set_ylabel("Voltage $v(t)$", color=INK, fontsize=10)
    ax.legend(frameon=False, loc="upper right")
    
    save(fig, "rlc-natural-response.svg")

def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "text.color": INK,
        "svg.hashsalt": "cir-electronics-media",
    })
    draw_opamp()
    draw_rc_response()
    draw_rlc_response()
    print(f"Generated electronics media in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Output directory
out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/public/media/physics'))
os.makedirs(out_dir, exist_ok=True)

def generate_work_area_graph():
    # Generate data for a varying force F(x) = -0.5*(x-5)^2 + 15
    x = np.linspace(0, 10, 500)
    F = -0.5 * (x - 5)**2 + 15

    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plot the force curve
    ax.plot(x, F, color='#2c3e50', linewidth=2.5, label='F(x)')
    
    # Shade the area under the curve between x=2 and x=8
    x_fill = np.linspace(2, 8, 300)
    F_fill = -0.5 * (x_fill - 5)**2 + 15
    ax.fill_between(x_fill, 0, F_fill, color='#3498db', alpha=0.4, label='Work = Area')
    
    # Add vertical lines for boundaries
    ax.vlines(2, 0, -0.5*(2-5)**2 + 15, color='#2980b9', linestyle='--', linewidth=1.5)
    ax.vlines(8, 0, -0.5*(8-5)**2 + 15, color='#2980b9', linestyle='--', linewidth=1.5)
    
    # Labels and annotations
    ax.text(2, -1, '$x_i$', fontsize=14, ha='center')
    ax.text(8, -1, '$x_f$', fontsize=14, ha='center')
    ax.text(5, 7.5, 'Work ($W = \int F dx$)', fontsize=16, ha='center', color='#2c3e50', fontweight='bold')
    
    # Axes limits and labels
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 18)
    ax.set_xlabel('Position $x$ (m)', fontsize=14)
    ax.set_ylabel('Force $F_x$ (N)', fontsize=14)
    ax.set_title('Work as Area Under the Force-Position Curve', fontsize=16, pad=15)
    
    # Clean up spines (axes lines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    
    # Hide ticks
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Save the figure
    out_path = os.path.join(out_dir, 'work-area-graph.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

if __name__ == "__main__":
    print("Generating physics media...")
    generate_work_area_graph()
    print("Done.")

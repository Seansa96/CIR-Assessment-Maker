import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/public/media/physics/worked-examples'))
os.makedirs(out_dir, exist_ok=True)

def generate_moi_composite():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.axis('off')
    
    # Large circle
    circle = plt.Circle((0, 0), 1.5, fill=True, color='lightblue', ec='black', linewidth=2)
    ax.add_patch(circle)
    
    # Cutout hole 1
    hole1 = plt.Circle((0.75, 0), 0.5, fill=True, color='white', ec='black', linewidth=1.5)
    ax.add_patch(hole1)
    
    # Cutout hole 2
    hole2 = plt.Circle((-0.75, 0), 0.5, fill=True, color='white', ec='black', linewidth=1.5)
    ax.add_patch(hole2)
    
    # Center points
    ax.plot([0], [0], 'ko', markersize=5)
    ax.plot([0.75], [0], 'ko', markersize=3)
    ax.plot([-0.75], [0], 'ko', markersize=3)
    
    # Labels
    ax.text(0, 0.1, "O", fontsize=14, ha='center')
    ax.text(0.75, 0.1, "O_1", fontsize=10, ha='center')
    ax.text(-0.75, 0.1, "O_2", fontsize=10, ha='center')
    
    # Radius lines
    ax.plot([0, 0], [0, 1.5], 'k--')
    ax.text(-0.15, 0.75, "R", fontsize=14)
    
    out_path = os.path.join(out_dir, 'moi-composite.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

def generate_torque_pulley_fbd():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.axis('off')
    
    # Outer Pulley
    outer = plt.Circle((0, 0), 1.5, fill=False, color='black', linewidth=2)
    ax.add_patch(outer)
    
    # Inner Pulley
    inner = plt.Circle((0, 0), 0.8, fill=False, color='black', linewidth=2)
    ax.add_patch(inner)
    
    # Center
    ax.plot([0], [0], 'ko', markersize=5)
    
    # Force 1 on outer
    ax.annotate(r'$T_1$', xy=(1.5, 0), xytext=(1.5, -1.0),
                arrowprops=dict(facecolor='red', width=2, headwidth=8), fontsize=14)
    
    # Force 2 on inner
    ax.annotate(r'$T_2$', xy=(-0.8, 0), xytext=(-0.8, -1.5),
                arrowprops=dict(facecolor='blue', width=2, headwidth=8), fontsize=14)
                
    # Radii
    ax.plot([0, 1.5], [0, 0], 'k--')
    ax.text(0.75, 0.1, r'$R_1$', fontsize=12)
    
    ax.plot([0, -0.8], [0, 0], 'k--')
    ax.text(-0.4, 0.1, r'$R_2$', fontsize=12)
    
    # Axis of rotation
    ax.text(0.1, 0.1, "Axis", fontsize=12)
    
    out_path = os.path.join(out_dir, 'torque-pulley-fbd.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

def generate_rolling_incline_fbd():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 5)
    ax.axis('off')
    
    angle = np.radians(30)
    
    # Incline
    ax.plot([0, 5], [0, 0], 'k-', linewidth=3)
    ax.plot([0, 5*np.cos(angle)], [0, 5*np.sin(angle)], 'k-', linewidth=3)
    ax.plot([5*np.cos(angle), 5*np.cos(angle)], [0, 5*np.sin(angle)], 'k-', linewidth=1)
    
    # Arc for angle
    arc = patches.Arc((0, 0), 2, 2, angle=0, theta1=0, theta2=30, color='blue', linewidth=2)
    ax.add_patch(arc)
    ax.text(1.2, 0.2, r'$\theta$', fontsize=14, color='blue')
    
    # Object center
    cx, cy = 3, 3*np.tan(angle) + 0.8
    # Object (circle)
    circle = plt.Circle((cx, cy), 0.8, fill=False, color='black', linewidth=2)
    ax.add_patch(circle)
    ax.plot([cx], [cy], 'ko')
    
    # Contact point
    contact_x = cx + 0.8 * np.sin(angle)
    contact_y = cy - 0.8 * np.cos(angle)
    ax.plot([contact_x], [contact_y], 'ro', markersize=5)
    
    # Forces
    # Gravity (from cm)
    ax.annotate(r'$Mg$', xy=(cx, cy), xytext=(cx, cy - 2),
                arrowprops=dict(facecolor='green', width=2, headwidth=8), fontsize=14)
                
    # Normal (from contact point)
    ax.annotate(r'$F_N$', xy=(contact_x, contact_y), xytext=(contact_x - 1*np.sin(angle), contact_y + 1*np.cos(angle)),
                arrowprops=dict(facecolor='orange', width=2, headwidth=8), fontsize=14)
                
    # Friction (from contact point up incline)
    ax.annotate(r'$f_s$', xy=(contact_x, contact_y), xytext=(contact_x - 1.5*np.cos(angle), contact_y - 1.5*np.sin(angle)),
                arrowprops=dict(facecolor='red', width=2, headwidth=8), fontsize=14)
    
    out_path = os.path.join(out_dir, 'rolling-incline-fbd.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

if __name__ == "__main__":
    print("Generating worked example geometry...")
    generate_moi_composite()
    generate_torque_pulley_fbd()
    generate_rolling_incline_fbd()
    print("Done!")

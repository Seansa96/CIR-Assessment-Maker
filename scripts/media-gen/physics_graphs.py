import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def generate_kinematics_graphs(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Velocity-Time Graph (Constant Acceleration)
    t = np.linspace(0, 10, 100)
    v0 = 5
    a = 2
    v = v0 + a * t
    
    plt.figure(figsize=(5, 3.5))
    plt.plot(t, v, color='#1976d2', linewidth=3)
    plt.fill_between(t, v, alpha=0.2, color='#1976d2')
    plt.title('Velocity vs. Time (Constant Acceleration)', fontsize=12)
    plt.xlabel('Time (s)', fontsize=10)
    plt.ylabel('Velocity (m/s)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, 10)
    plt.ylim(0, 25)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'vt-graph-const-accel.svg'), format='svg')
    plt.close()

    # 2. Position-Time Graph (Constant Acceleration)
    x0 = 0
    x = x0 + v0 * t + 0.5 * a * t**2
    
    plt.figure(figsize=(5, 3.5))
    plt.plot(t, x, color='#d32f2f', linewidth=3)
    plt.title('Position vs. Time (Constant Acceleration)', fontsize=12)
    plt.xlabel('Time (s)', fontsize=10)
    plt.ylabel('Position (m)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, 10)
    plt.ylim(0, 160)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'xt-graph-const-accel.svg'), format='svg')
    plt.close()

    # 3. Position-Time Graph (Terminal Velocity / Drag)
    # x(t) = v_t * t - (v_t^2 / g) * (1 - e^(-g*t/v_t))
    vt = 20.0
    g = 9.81
    x_drag = vt * t - (vt**2 / g) * (1 - np.exp(-g * t / vt))
    
    plt.figure(figsize=(5, 3.5))
    plt.plot(t, x_drag, color='#388e3c', linewidth=3)
    plt.title('Position vs. Time (With Air Resistance)', fontsize=12)
    plt.xlabel('Time (s)', fontsize=10)
    plt.ylabel('Position (m)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, 10)
    plt.ylim(0, max(x_drag) + 10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'xt-graph-drag.svg'), format='svg')
    plt.close()

    print(f"Generated kinematics graphs in {output_dir}")

if __name__ == "__main__":
    generate_kinematics_graphs("../../data/media/physics/kinematics")

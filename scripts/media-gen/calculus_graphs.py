import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def generate_calculus_graphs(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Area Between Curves (y = 5x - x^2 and y = x)
    x = np.linspace(0, 5, 200)
    f = 5*x - x**2
    g = x
    
    plt.figure(figsize=(5, 4))
    plt.plot(x, f, color='#d32f2f', linewidth=2, label='f(x) = 5x - x²')
    plt.plot(x, g, color='#1976d2', linewidth=2, label='g(x) = x')
    
    # Fill between the curves where f(x) > g(x) (from x=0 to x=4)
    x_fill = np.linspace(0, 4, 100)
    plt.fill_between(x_fill, 5*x_fill - x_fill**2, x_fill, alpha=0.3, color='#9c27b0')
    
    plt.title('Area Between Curves', fontsize=12)
    plt.xlabel('x', fontsize=10)
    plt.ylabel('y', fontsize=10)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlim(-0.5, 5.5)
    plt.ylim(-1, 8)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'area-between-curves.svg'), format='svg')
    plt.close()

    # 2. Volume of Solid of Revolution (Disk Method conceptualization)
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')
    
    # Generate the surface of revolution (y = sqrt(x) from 0 to 4 around x-axis)
    u = np.linspace(0, 4, 50)
    v = np.linspace(0, 2*np.pi, 50)
    U, V = np.meshgrid(u, v)
    
    # X = u, Y = sqrt(u) * cos(v), Z = sqrt(u) * sin(v)
    X = U
    Y = np.sqrt(U) * np.cos(V)
    Z = np.sqrt(U) * np.sin(V)
    
    ax.plot_surface(X, Y, Z, color='#4fc3f7', alpha=0.7, edgecolor='none')
    
    # Draw a representative disk at x=2
    x_disk = 2
    r_disk = np.sqrt(x_disk)
    v_disk = np.linspace(0, 2*np.pi, 50)
    Y_disk = r_disk * np.cos(v_disk)
    Z_disk = r_disk * np.sin(v_disk)
    ax.plot(np.ones_like(v_disk)*x_disk, Y_disk, Z_disk, color='#d32f2f', linewidth=3, label='Representative Disk')
    
    ax.set_title('Volume of Solid of Revolution (Disk Method)')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'volume-solid-revolution.svg'), format='svg')
    plt.close()

    print(f"Generated calculus graphs in {output_dir}")

if __name__ == "__main__":
    generate_calculus_graphs("../../data/media/calculus-2")

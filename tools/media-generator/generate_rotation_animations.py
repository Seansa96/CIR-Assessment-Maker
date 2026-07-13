import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/public/media/physics/animations'))
os.makedirs(out_dir, exist_ok=True)

def generate_rotational_variables():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    
    # Draw circle
    circle = plt.Circle((0, 0), 1.0, fill=False, color='black', linewidth=2)
    ax.add_patch(circle)
    
    # Draw reference line
    ax.plot([0, 1.2], [0, 0], color='gray', linestyle='--')
    
    line, = ax.plot([], [], color='#e74c3c', linewidth=3)
    point, = ax.plot([], [], 'o', color='#3498db', markersize=10)
    arc, = ax.plot([], [], color='#2ecc71', linewidth=3)
    
    # Texts
    theta_text = ax.text(0.3, 0.1, r'$\theta$', fontsize=16)
    s_text = ax.text(1.1, 0.5, r'$s = r\theta$', fontsize=16, color='#2ecc71')
    r_text = ax.text(0.5, -0.15, r'$r$', fontsize=16, color='#e74c3c')
    
    def init():
        line.set_data([], [])
        point.set_data([], [])
        arc.set_data([], [])
        return line, point, arc, theta_text, s_text
        
    def animate(i):
        theta = i * (2 * np.pi / 60)
        # Radius line
        line.set_data([0, np.cos(theta)], [0, np.sin(theta)])
        # Point
        point.set_data([np.cos(theta)], [np.sin(theta)])
        
        # Arc
        t_arc = np.linspace(0, theta, 50)
        arc.set_data(1.05 * np.cos(t_arc), 1.05 * np.sin(t_arc))
        
        # Update text positions
        theta_text.set_position((0.2 * np.cos(theta/2), 0.2 * np.sin(theta/2)))
        s_text.set_position((1.2 * np.cos(theta/2), 1.2 * np.sin(theta/2)))
        
        return line, point, arc, theta_text, s_text

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=60, interval=50, blit=True)
    out_path = os.path.join(out_dir, 'rotational-variables.gif')
    ani.save(out_path, writer='pillow', fps=20)
    plt.close()
    print(f"Generated {out_path}")

def generate_rolling_motion():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-1, 9)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    
    # Ground
    ax.plot([-1, 9], [0, 0], color='black', linewidth=2)
    
    circle = plt.Circle((0, 1), 1.0, fill=False, color='blue', linewidth=2)
    ax.add_patch(circle)
    
    spoke, = ax.plot([], [], color='red', linewidth=2)
    cm_point, = ax.plot([], [], 'ko', markersize=6)
    path_line, = ax.plot([], [], color='gray', linestyle=':', linewidth=1.5)
    
    v_arrow = ax.annotate(r'$v_{cm}$', xy=(0, 1), xytext=(0, 1),
                          arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))
                          
    path_x, path_y = [], []
    
    def init():
        spoke.set_data([], [])
        cm_point.set_data([], [])
        path_line.set_data([], [])
        return spoke, cm_point, path_line, v_arrow
        
    def animate(i):
        # 0 to 2pi
        theta = i * (2 * np.pi / 40)
        x_c = theta # v = R*omega, so dx = R*dtheta, here R=1
        y_c = 1.0
        
        circle.center = (x_c, y_c)
        
        # Spoke rotates clockwise
        x_p = x_c + np.cos(-theta - np.pi/2)
        y_p = y_c + np.sin(-theta - np.pi/2)
        
        spoke.set_data([x_c, x_p], [y_c, y_p])
        cm_point.set_data([x_c], [y_c])
        
        path_x.append(x_p)
        path_y.append(y_p)
        path_line.set_data(path_x, path_y)
        
        v_arrow.xy = (x_c + 1.5, y_c)
        v_arrow.set_position((x_c, y_c))
        
        return circle, spoke, cm_point, path_line, v_arrow

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=40, interval=50, blit=False)
    out_path = os.path.join(out_dir, 'rolling-motion.gif')
    ani.save(out_path, writer='pillow', fps=20)
    plt.close()
    print(f"Generated {out_path}")

def generate_torque_lever():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(-1, 5)
    ax.set_ylim(-2, 2)
    ax.axis('off')
    
    # Pivot
    ax.plot([0], [0], 'k^', markersize=15)
    # Lever arm
    ax.plot([0, 3], [0, 0], color='gray', linewidth=8)
    
    r_text = ax.text(1.5, -0.3, r'$\vec{r}$', fontsize=16)
    
    # Force arrow
    force_arrow = ax.annotate(r'$\vec{F}$', xy=(3, 0), xytext=(3, 1),
                              arrowprops=dict(facecolor='red', width=2, headwidth=8))
                              
    tau_text = ax.text(0, 1, r'$\tau = rF \sin(\theta)$', fontsize=14)
    
    def animate(i):
        # angle goes from 0 to pi
        angle = i * (np.pi / 30)
        F_x = 3 + 1.5 * np.cos(angle)
        F_y = 1.5 * np.sin(angle)
        
        force_arrow.xy = (3, 0)
        force_arrow.set_position((F_x, F_y))
        
        tau_val = 3 * 1.5 * np.sin(angle)
        tau_text.set_text(fr'$\tau = {tau_val:.1f}$')
        
        return force_arrow, tau_text

    ani = animation.FuncAnimation(fig, animate, frames=31, interval=100, blit=False)
    out_path = os.path.join(out_dir, 'torque-lever.gif')
    ani.save(out_path, writer='pillow', fps=10)
    plt.close()
    print(f"Generated {out_path}")

def generate_angular_momentum():
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.axis('off')
    
    # draw disk
    theta = np.linspace(0, 2*np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.plot(x, y, 0, color='blue', alpha=0.5, linewidth=2)
    
    # z axis (axis of rotation)
    ax.plot([0,0], [0,0], [-1.5, 1.5], 'k--')
    
    point, = ax.plot([], [], [], 'ro', markersize=8)
    v_arrow = ax.quiver(0,0,0,0,0,0, color='green')
    L_arrow = ax.quiver(0,0,0,0,0,0, color='purple', linewidth=3)
    
    # Static text
    ax.text2D(0.05, 0.95, r'$\vec{L} = \vec{r} \times \vec{p}$', transform=ax.transAxes, fontsize=14)
    ax.text2D(0.05, 0.90, "Purple: Angular Momentum (L)\nGreen: Velocity (v)", transform=ax.transAxes, fontsize=10)
    
    def init():
        point.set_data([], [])
        point.set_3d_properties([])
        return point,
        
    def animate(i):
        nonlocal v_arrow, L_arrow
        t = i * (2 * np.pi / 40)
        px, py = np.cos(t), np.sin(t)
        
        point.set_data([px], [py])
        point.set_3d_properties([0])
        
        v_arrow.remove()
        v_arrow = ax.quiver(px, py, 0, -np.sin(t), np.cos(t), 0, color='green', length=0.8, arrow_length_ratio=0.3)
        
        L_arrow.remove()
        L_arrow = ax.quiver(0, 0, 0, 0, 0, 1.2, color='purple', length=1.0, arrow_length_ratio=0.2)
        
        # slowly rotate view
        ax.view_init(elev=20, azim=i*2)
        
        return point,

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=40, interval=50, blit=False)
    out_path = os.path.join(out_dir, 'angular-momentum-rhr.gif')
    ani.save(out_path, writer='pillow', fps=20)
    plt.close()
    print(f"Generated {out_path}")

if __name__ == "__main__":
    print("Generating rotation animations...")
    generate_rotational_variables()
    generate_rolling_motion()
    generate_torque_lever()
    generate_angular_momentum()
    print("Done!")

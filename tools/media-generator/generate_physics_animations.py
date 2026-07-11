import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Output directory
out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/public/media/physics'))
os.makedirs(out_dir, exist_ok=True)

def generate_wave_animation():
    fig, ax = plt.subplots(figsize=(8, 4))
    
    x = np.linspace(0, 4 * np.pi, 200)
    line, = ax.plot(x, np.sin(x), color='#e74c3c', linewidth=3)
    
    ax.set_xlim(0, 4 * np.pi)
    ax.set_ylim(-1.5, 1.5)
    
    # Hide spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    
    ax.set_xticks([])
    ax.set_yticks([])
    
    ax.set_title('Transverse Wave Oscillation', fontsize=14, pad=15)
    
    def init():
        line.set_ydata([np.nan] * len(x))
        return line,

    def animate(i):
        # Shift the wave by modifying the phase
        y = np.sin(x - i * 0.1)
        line.set_ydata(y)
        return line,

    # Create the animation object
    ani = animation.FuncAnimation(
        fig, animate, init_func=init, frames=63, interval=50, blit=True
    )
    
    out_path = os.path.join(out_dir, 'wave-animation.gif')
    
    # Save as GIF using pillow writer
    ani.save(out_path, writer='pillow', fps=20)
    plt.close()
    
    print(f"Generated {out_path}")

if __name__ == "__main__":
    print("Generating physics animations...")
    generate_wave_animation()
    print("Done.")

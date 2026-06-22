import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs(r'c:\Users\SeanS\Downloads\cir_app\data\media\physics', exist_ok=True)

# 1. PVA Graph
t = np.linspace(0, 5, 100)
# p(t) = t^3 - 6t^2 + 9t + 2
# v(t) = 3t^2 - 12t + 9
# a(t) = 6t - 12
p = t**3 - 6*t**2 + 9*t + 2
v = 3*t**2 - 12*t + 9
a = 6*t - 12

fig, axs = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
axs[0].plot(t, p, 'b', label='Position $x(t)$')
axs[0].set_ylabel('Position (m)')
axs[0].legend()
axs[0].grid(True)

axs[1].plot(t, v, 'g', label='Velocity $v(t) = \\frac{dx}{dt}$')
axs[1].axhline(0, color='k', linestyle='--', alpha=0.5)
axs[1].set_ylabel('Velocity (m/s)')
axs[1].legend()
axs[1].grid(True)

axs[2].plot(t, a, 'r', label='Acceleration $a(t) = \\frac{dv}{dt}$')
axs[2].axhline(0, color='k', linestyle='--', alpha=0.5)
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Acceleration ($m/s^2$)')
axs[2].legend()
axs[2].grid(True)

plt.suptitle('Position, Velocity, and Acceleration vs Time')
plt.tight_layout()
plt.savefig(r'c:\Users\SeanS\Downloads\cir_app\data\media\physics\pva-calculus-graph.png')
plt.close()

# 2. Terminal Velocity Graph
t = np.linspace(0, 10, 100)
v_terminal = 50
v = v_terminal * (1 - np.exp(-0.5 * t))

plt.figure(figsize=(8, 5))
plt.plot(t, v, 'b-', linewidth=2, label='Velocity')
plt.axhline(v_terminal, color='r', linestyle='--', label='Terminal Speed ($v_t$)')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity vs. Time with Air Resistance (Drag)')
plt.legend()
plt.grid(True)
plt.savefig(r'c:\Users\SeanS\Downloads\cir_app\data\media\physics\terminal-velocity-graph.png')
plt.close()

# 3. Work Area Under Curve
x = np.linspace(0, 5, 100)
F = np.sin(x) * 5 + 10  # Varying force

plt.figure(figsize=(8, 5))
plt.plot(x, F, 'k-', linewidth=2, label='Force $F(x)$')
plt.fill_between(x, F, color='skyblue', alpha=0.5, label='Work = $\\int F(x) dx$')
plt.xlabel('Position $x$ (m)')
plt.ylabel('Force $F$ (N)')
plt.title('Work as Area Under the Force-Position Curve')
plt.ylim(0, 20)
plt.legend()
plt.grid(True)
plt.savefig(r'c:\Users\SeanS\Downloads\cir_app\data\media\physics\work-area-graph.png')
plt.close()

# 4. Free-Body Diagram Example (Block on Incline)
plt.figure(figsize=(6, 6))
# Box
box_x = [-1, 1, 1, -1, -1]
box_y = [-1, -1, 1, 1, -1]
plt.plot(box_x, box_y, 'k-', linewidth=2)
# Forces
plt.annotate('', xy=(0, -3), xytext=(0, 0), arrowprops=dict(facecolor='red', shrink=0, width=2, headwidth=10))
plt.text(0.2, -2.5, 'Weight ($mg$)', color='red', fontsize=12)

plt.annotate('', xy=(0, 3), xytext=(0, 0), arrowprops=dict(facecolor='blue', shrink=0, width=2, headwidth=10))
plt.text(0.2, 2.5, 'Normal Force ($N$)', color='blue', fontsize=12)

plt.annotate('', xy=(3, 0), xytext=(0, 0), arrowprops=dict(facecolor='green', shrink=0, width=2, headwidth=10))
plt.text(2.2, 0.2, 'Applied Force ($F$)', color='green', fontsize=12)

plt.annotate('', xy=(-2, 0), xytext=(0, 0), arrowprops=dict(facecolor='orange', shrink=0, width=2, headwidth=10))
plt.text(-1.8, 0.2, 'Friction ($f$)', color='orange', fontsize=12)

plt.xlim(-4, 4)
plt.ylim(-4, 4)
plt.gca().set_aspect('equal', adjustable='box')
plt.title('Free-Body Diagram')
plt.axis('off')
plt.savefig(r'c:\Users\SeanS\Downloads\cir_app\data\media\physics\free-body-diagram-example.png')
plt.close()

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

out_dir = r"c:\Users\SeanS\Downloads\cir_app\frontend\public\media\geometry\circles"
os.makedirs(out_dir, exist_ok=True)

# 1. Inscribed Angle
fig, ax = plt.subplots(figsize=(4, 4))
circle = patches.Circle((0, 0), 1, edgecolor='black', facecolor='none', linewidth=2)
ax.add_patch(circle)

# Points A, B, C
A = (np.cos(np.radians(135)), np.sin(np.radians(135)))
B = (np.cos(np.radians(-45)), np.sin(np.radians(-45)))
C = (np.cos(np.radians(45)), np.sin(np.radians(45)))
O = (0, 0)

# Chords
plt.plot([B[0], A[0]], [B[1], A[1]], 'b-', linewidth=1.5)
plt.plot([B[0], C[0]], [B[1], C[1]], 'b-', linewidth=1.5)
# Radii
plt.plot([O[0], A[0]], [O[1], A[1]], 'r--', linewidth=1.5)
plt.plot([O[0], C[0]], [O[1], C[1]], 'r--', linewidth=1.5)

# Points
for pt, label in [(A, 'A'), (B, 'B'), (C, 'C'), (O, 'O')]:
    plt.plot(pt[0], pt[1], 'ko')
    plt.text(pt[0]*1.15, pt[1]*1.15, label, ha='center', va='center', fontsize=12)

# Angle
plt.text(B[0]*0.7, B[1]*0.7, '35°', ha='center', va='center', fontsize=10, color='blue')
plt.text(0, 0.2, '?', ha='center', va='center', fontsize=12, color='red')

ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "inscribed_angle.svg"), format='svg', transparent=True)
plt.close()


# 2. Intersecting Chords (Angles)
fig, ax = plt.subplots(figsize=(4, 4))
circle = patches.Circle((0, 0), 1, edgecolor='black', facecolor='none', linewidth=2)
ax.add_patch(circle)

A = (np.cos(np.radians(120)), np.sin(np.radians(120)))
B = (np.cos(np.radians(-60)), np.sin(np.radians(-60)))
C = (np.cos(np.radians(40)), np.sin(np.radians(40)))
D = (np.cos(np.radians(-140)), np.sin(np.radians(-140)))

plt.plot([A[0], B[0]], [A[1], B[1]], 'b-', linewidth=1.5)
plt.plot([C[0], D[0]], [C[1], D[1]], 'b-', linewidth=1.5)

for pt, label in [(A, 'A'), (B, 'B'), (C, 'C'), (D, 'D')]:
    plt.plot(pt[0], pt[1], 'ko')
    plt.text(pt[0]*1.15, pt[1]*1.15, label, ha='center', va='center', fontsize=12)

# Intersection X
# Line AB: passes through origin since -60 and 120 are opposite. Line CD passes through origin.
plt.plot(0, 0, 'ko')
plt.text(0.1, -0.1, 'X', ha='center', va='center', fontsize=12)

plt.text(0, 1.1, '40°', ha='center', va='bottom', fontsize=10, color='red')
plt.text(0, -1.1, '80°', ha='center', va='top', fontsize=10, color='red')

ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "intersecting_chords_angles.svg"), format='svg', transparent=True)
plt.close()


# 3. Sector Area
fig, ax = plt.subplots(figsize=(4, 4))
circle = patches.Circle((0, 0), 1, edgecolor='black', facecolor='none', linewidth=2)
ax.add_patch(circle)

wedge = patches.Wedge((0, 0), 1, 0, 45, facecolor='#ffcc99', edgecolor='orange', linewidth=2)
ax.add_patch(wedge)

plt.plot(0, 0, 'ko')
plt.text(0.4, 0.15, '45°', ha='center', va='center', fontsize=10)
plt.text(0.5, -0.1, 'r = 6 in', ha='center', va='top', fontsize=10)

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "sector_area.svg"), format='svg', transparent=True)
plt.close()


# 4. Segment Area
fig, ax = plt.subplots(figsize=(4, 4))
circle = patches.Circle((0, 0), 1, edgecolor='black', facecolor='none', linewidth=2)
ax.add_patch(circle)

# Segment shaded
theta = np.linspace(0, np.pi/2, 100)
x = np.cos(theta)
y = np.sin(theta)
plt.fill_between(x, 1-x, y, color='#a2d2ff')

plt.plot([0, 1], [0, 0], 'k-', linewidth=1.5)
plt.plot([0, 0], [0, 1], 'k-', linewidth=1.5)
plt.plot([1, 0], [0, 1], 'k-', linewidth=1.5)

plt.plot(0, 0, 'ko')
plt.text(0.1, 0.1, '90°', ha='center', va='center', fontsize=10)
plt.text(0.5, -0.1, '10 cm', ha='center', va='top', fontsize=10)

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "segment_area.svg"), format='svg', transparent=True)
plt.close()


# 5. Tangent Radius
fig, ax = plt.subplots(figsize=(5, 4))
circle = patches.Circle((0, 0), 1, edgecolor='black', facecolor='none', linewidth=2)
ax.add_patch(circle)

# Tangent line at bottom (0, -1)
plt.plot([-1, 3], [-1, -1], 'b-', linewidth=1.5)
plt.text(2.8, -1.2, 'L', ha='center', va='center', fontsize=12)

O = (0, 0)
T = (0, -1)
P = (2.4, -1)

plt.plot([O[0], T[0]], [O[1], T[1]], 'r--', linewidth=1.5)
plt.plot([O[0], P[0]], [O[1], P[1]], 'g-', linewidth=1.5)

for pt, label in [(O, 'O'), (T, 'T'), (P, 'P')]:
    plt.plot(pt[0], pt[1], 'ko')
    plt.text(pt[0], pt[1]+0.15 if label=='O' else pt[1]-0.15, label, ha='center', va='center', fontsize=12)

# Right angle symbol
plt.plot([0.1, 0.1, 0], [-1, -0.9, -0.9], 'k-', linewidth=1)

plt.text(-0.15, -0.5, '5', ha='right', va='center', fontsize=10)
plt.text(1.2, -1.15, '12', ha='center', va='top', fontsize=10)
plt.text(1.2, -0.3, '?', ha='center', va='bottom', fontsize=12, color='green')

ax.set_xlim(-1.2, 3)
ax.set_ylim(-1.5, 1.2)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "tangent_radius.svg"), format='svg', transparent=True)
plt.close()


# 6. Intersecting Chords Lengths
fig, ax = plt.subplots(figsize=(4, 4))
circle = patches.Circle((0, 0), 1, edgecolor='black', facecolor='none', linewidth=2)
ax.add_patch(circle)

A = (np.cos(np.radians(150)), np.sin(np.radians(150)))
B = (np.cos(np.radians(-30)), np.sin(np.radians(-30)))
C = (np.cos(np.radians(60)), np.sin(np.radians(60)))
D = (np.cos(np.radians(-120)), np.sin(np.radians(-120)))

plt.plot([A[0], B[0]], [A[1], B[1]], 'b-', linewidth=1.5)
plt.plot([C[0], D[0]], [C[1], D[1]], 'b-', linewidth=1.5)

for pt, label in [(A, 'A'), (B, 'B'), (C, 'C'), (D, 'D')]:
    plt.plot(pt[0], pt[1], 'ko')
    plt.text(pt[0]*1.15, pt[1]*1.15, label, ha='center', va='center', fontsize=12)

plt.plot(0, 0, 'ko')
plt.text(-0.1, 0.1, 'E', ha='center', va='center', fontsize=12)

plt.text(-0.4, 0.3, '4', ha='center', va='center', fontsize=10)
plt.text(0.4, -0.1, '6', ha='center', va='center', fontsize=10)
plt.text(0.2, 0.4, '3', ha='center', va='center', fontsize=10)
plt.text(-0.2, -0.4, '?', ha='center', va='center', fontsize=12, color='red')

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "intersecting_chords_lengths.svg"), format='svg', transparent=True)
plt.close()


# 7. Secant-Secant
fig, ax = plt.subplots(figsize=(5, 4))
circle = patches.Circle((0, 0), 1, edgecolor='black', facecolor='none', linewidth=2)
ax.add_patch(circle)

P = (-2, 0)
A = (np.cos(np.radians(160)), np.sin(np.radians(160)))
B = (np.cos(np.radians(20)), np.sin(np.radians(20)))
C = (np.cos(np.radians(200)), np.sin(np.radians(200)))
D = (np.cos(np.radians(-20)), np.sin(np.radians(-20)))

plt.plot([P[0], B[0]], [P[1], B[1]], 'b-', linewidth=1.5)
plt.plot([P[0], D[0]], [P[1], D[1]], 'b-', linewidth=1.5)

for pt, label in [(P, 'P'), (A, 'A'), (B, 'B'), (C, 'C'), (D, 'D')]:
    plt.plot(pt[0], pt[1], 'ko')
    plt.text(pt[0] if label=='P' else pt[0]*1.15, pt[1]-0.15 if label=='P' else pt[1]*1.15, label, ha='center', va='center', fontsize=12)

plt.text(-1.5, 0.25, '4', ha='center', va='center', fontsize=10)
plt.text(0, 0.45, '5', ha='center', va='center', fontsize=10)
plt.text(-1.5, -0.25, '3', ha='center', va='center', fontsize=10)
plt.text(0, -0.45, '?', ha='center', va='center', fontsize=12, color='red')

ax.set_xlim(-2.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "secant_secant.svg"), format='svg', transparent=True)
plt.close()


# 8. Tangent-Secant
fig, ax = plt.subplots(figsize=(5, 4))
circle = patches.Circle((0, 0), 1, edgecolor='black', facecolor='none', linewidth=2)
ax.add_patch(circle)

P = (-2.5, 1)
T = (0, 1)
A = (np.cos(np.radians(180)), np.sin(np.radians(180)))
B = (np.cos(np.radians(-60)), np.sin(np.radians(-60)))

plt.plot([P[0], T[0]], [P[1], T[1]], 'b-', linewidth=1.5)
plt.plot([P[0], B[0]], [P[1], B[1]], 'b-', linewidth=1.5)

for pt, label in [(P, 'P'), (T, 'T'), (A, 'A'), (B, 'B')]:
    plt.plot(pt[0], pt[1], 'ko')
    plt.text(pt[0]-0.15 if label=='P' else pt[0]*1.15, pt[1] if label=='P' else pt[1]*1.15, label, ha='center', va='center', fontsize=12)

plt.text(-1.25, 1.1, '6', ha='center', va='bottom', fontsize=10)
plt.text(-1.8, 0.4, '4', ha='center', va='center', fontsize=10)
plt.text(-0.5, -0.2, '?', ha='center', va='center', fontsize=12, color='red')

ax.set_xlim(-2.8, 1.2)
ax.set_ylim(-1.2, 1.5)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "tangent_secant.svg"), format='svg', transparent=True)
plt.close()

print("All 8 SVG images generated successfully.")

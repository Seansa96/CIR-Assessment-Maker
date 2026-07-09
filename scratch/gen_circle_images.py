import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Create directory
out_dir = r"c:\Users\SeanS\Downloads\cir_app\frontend\public\media\geometry\circles"
os.makedirs(out_dir, exist_ok=True)

# Image 1: Circle with circumference and area
fig, ax = plt.subplots(figsize=(4, 4))
circle = patches.Circle((0, 0), 1, edgecolor='#1f77b4', facecolor='#e6f2ff', linewidth=2, linestyle='--')
ax.add_patch(circle)

# Add center point and radius line
plt.plot(0, 0, 'ko')
plt.plot([0, 1], [0, 0], 'k-', linewidth=1.5)
plt.text(0.5, 0.05, 'r = ?', ha='center', va='bottom', fontsize=12)

# Add circumference text
plt.text(-0.8, 0.8, 'C = 31.4 m', ha='center', va='center', fontsize=12, color='#1f77b4', fontweight='bold')
plt.text(0, -0.4, 'Area = ?', ha='center', va='center', fontsize=12, color='#333333', fontweight='bold')

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "circle_circumference_area.svg"), format='svg', transparent=True)
plt.close()

# Image 2: Annulus (pool + deck)
fig, ax = plt.subplots(figsize=(5, 5))
outer_circle = patches.Circle((0, 0), 7, edgecolor='#8c564b', facecolor='#d4a373', linewidth=2)
inner_circle = patches.Circle((0, 0), 5, edgecolor='#1f77b4', facecolor='#a2d2ff', linewidth=2)

ax.add_patch(outer_circle)
ax.add_patch(inner_circle)

# Inner diameter
plt.plot([-5, 5], [0, 0], 'k--', linewidth=1.5)
plt.plot(0, 0, 'ko')
plt.text(0, 0.3, '10 m', ha='center', va='bottom', fontsize=12, fontweight='bold', backgroundcolor='#a2d2ff')

# Deck width
plt.plot([5, 7], [0, 0], 'k-', linewidth=2)
plt.text(6, 0.3, '2 m', ha='center', va='bottom', fontsize=12, fontweight='bold', backgroundcolor='#d4a373')

plt.text(0, -6, 'Wooden Deck', ha='center', va='center', fontsize=12, fontweight='bold', color='#4a3028')
plt.text(0, -2, 'Pool', ha='center', va='center', fontsize=12, fontweight='bold', color='#124a73')

ax.set_xlim(-7.5, 7.5)
ax.set_ylim(-7.5, 7.5)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "annulus_pool_deck.svg"), format='svg', transparent=True)
plt.close()

print("Images generated successfully.")

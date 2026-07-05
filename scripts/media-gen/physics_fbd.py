import os
import math

def generate_inclined_plane_fbd(filename, angle_deg=30):
    width = 400
    height = 300
    cx = 200
    cy = 150
    
    rad = math.radians(angle_deg)
    
    # Plane coordinates
    plane_width = 350
    px1 = cx - plane_width/2 * math.cos(rad)
    py1 = cy + plane_width/2 * math.sin(rad)
    px2 = cx + plane_width/2 * math.cos(rad)
    py2 = cy - plane_width/2 * math.sin(rad)
    
    # Box properties
    bw, bh = 80, 60
    # The box is centered at cx, cy, rotated by angle_deg
    # We will just use an SVG transform for the box
    
    svg = f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#d32f2f" />
        </marker>
        <marker id="arrow-blue" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#1976d2" />
        </marker>
        <marker id="arrow-green" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#388e3c" />
        </marker>
    </defs>
    
    <!-- Inclined Plane -->
    <line x1="{px1}" y1="{py1+bh/2}" x2="{px2}" y2="{py2+bh/2}" stroke="#757575" stroke-width="4" />
    <path d="M {px1} {py1+bh/2} L {px2} {py2+bh/2} L {px1} {py2+bh/2} Z" fill="#e0e0e0" opacity="0.5"/>
    
    <!-- Angle Arc -->
    <path d="M {px1+40} {py2+bh/2} A 40 40 0 0 0 {px1 + 40*math.cos(rad)} {py2+bh/2 - 40*math.sin(rad)}" fill="none" stroke="#757575" stroke-width="2" />
    <text x="{px1+45}" y="{py2+bh/2 - 10}" font-family="sans-serif" font-size="14" fill="#757575">θ</text>
    
    <!-- The Block -->
    <g transform="translate({cx}, {cy}) rotate({-angle_deg})">
        <rect x="{-bw/2}" y="{-bh/2}" width="{bw}" height="{bh}" fill="#ffcc80" stroke="#f57c00" stroke-width="3" />
        <circle cx="0" cy="0" r="4" fill="#d32f2f" />
        
        <!-- Normal Force -->
        <line x1="0" y1="0" x2="0" y2="-90" stroke="#1976d2" stroke-width="3" marker-end="url(#arrow-blue)" />
        <text x="5" y="-75" font-family="sans-serif" font-size="16" fill="#1976d2" font-weight="bold">F_N</text>
        
        <!-- Friction Force -->
        <line x1="0" y1="{bh/2}" x2="-70" y2="{bh/2}" stroke="#388e3c" stroke-width="3" marker-end="url(#arrow-green)" />
        <text x="-65" y="{bh/2 - 5}" font-family="sans-serif" font-size="16" fill="#388e3c" font-weight="bold">f_k</text>
    </g>
    
    <!-- Gravity (straight down, not rotated with the block) -->
    <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy+100}" stroke="#d32f2f" stroke-width="3" marker-end="url(#arrow)" />
    <text x="{cx+10}" y="{cy+85}" font-family="sans-serif" font-size="16" fill="#d32f2f" font-weight="bold">mg</text>
    
</svg>"""

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_inclined_plane_fbd("../../data/media/physics/kinematics/inclined-plane-fbd.svg", angle_deg=25)

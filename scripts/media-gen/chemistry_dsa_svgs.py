import os
import math

def generate_water_molecule_svg(output_path):
    svg = """<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
    <!-- Oxygen Atom -->
    <circle cx="150" cy="120" r="40" fill="#d32f2f" stroke="#b71c1c" stroke-width="3" />
    <text x="150" y="128" font-family="sans-serif" font-size="24" fill="white" font-weight="bold" text-anchor="middle">O</text>
    
    <!-- Left Hydrogen -->
    <line x1="150" y1="120" x2="80" y2="60" stroke="#757575" stroke-width="8" />
    <circle cx="80" cy="60" r="25" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="3" />
    <text x="80" y="68" font-family="sans-serif" font-size="20" fill="#424242" font-weight="bold" text-anchor="middle">H</text>
    
    <!-- Right Hydrogen -->
    <line x1="150" y1="120" x2="220" y2="60" stroke="#757575" stroke-width="8" />
    <circle cx="220" cy="60" r="25" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="3" />
    <text x="220" y="68" font-family="sans-serif" font-size="20" fill="#424242" font-weight="bold" text-anchor="middle">H</text>
    
    <!-- Angle Arc -->
    <path d="M 125 98 A 30 30 0 0 1 175 98" fill="none" stroke="#424242" stroke-width="2" stroke-dasharray="4" />
    <text x="150" y="85" font-family="sans-serif" font-size="14" fill="#424242" text-anchor="middle">104.5°</text>
</svg>"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path}")

def generate_bst_svg(output_path):
    svg = """<svg width="400" height="250" xmlns="http://www.w3.org/2000/svg">
    <style>
        .node { fill: #1976d2; stroke: #1565c0; stroke-width: 3; }
        .text { font-family: sans-serif; font-size: 18px; fill: white; font-weight: bold; text-anchor: middle; alignment-baseline: middle; }
        .edge { stroke: #757575; stroke-width: 3; }
    </style>
    
    <!-- Edges -->
    <line x1="200" y1="40" x2="100" y2="120" class="edge" />
    <line x1="200" y1="40" x2="300" y2="120" class="edge" />
    <line x1="100" y1="120" x2="50" y2="200" class="edge" />
    <line x1="100" y1="120" x2="150" y2="200" class="edge" />
    <line x1="300" y1="120" x2="250" y2="200" class="edge" />
    <line x1="300" y1="120" x2="350" y2="200" class="edge" />
    
    <!-- Nodes -->
    <!-- Root -->
    <circle cx="200" cy="40" r="20" class="node" />
    <text x="200" y="42" class="text">8</text>
    
    <!-- Level 1 -->
    <circle cx="100" cy="120" r="20" class="node" />
    <text x="100" y="122" class="text">3</text>
    
    <circle cx="300" cy="120" r="20" class="node" />
    <text x="300" y="122" class="text">10</text>
    
    <!-- Level 2 -->
    <circle cx="50" cy="200" r="20" class="node" />
    <text x="50" y="202" class="text">1</text>
    
    <circle cx="150" cy="200" r="20" class="node" />
    <text x="150" y="202" class="text">6</text>
    
    <circle cx="250" cy="200" r="20" class="node" />
    <text x="250" y="202" class="text">9</text>
    
    <circle cx="350" cy="200" r="20" class="node" />
    <text x="350" y="202" class="text">14</text>
</svg>"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_water_molecule_svg("../../data/media/chemistry/water-molecule.svg")
    generate_bst_svg("../../data/media/dsa/bst.svg")

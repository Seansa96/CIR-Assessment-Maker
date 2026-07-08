import os

out_dir = r"c:\Users\SeanS\Downloads\cir_app\frontend\public\assessments\trigonometry"
os.makedirs(out_dir, exist_ok=True)

def write_svg(filename, content):
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

svg1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="300" height="200">
    <polygon points="50,150 250,150 120,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="35" y="155" font-family="Arial" font-size="16" fill="#000">A</text>
    <text x="260" y="155" font-family="Arial" font-size="16" fill="#000">B</text>
    <text x="115" y="40" font-family="Arial" font-size="16" fill="#000">C</text>
    
    <text x="180" y="90" font-family="Arial" font-size="16" fill="#0284c7">a</text>
    <text x="70" y="90" font-family="Arial" font-size="16" fill="#0284c7">b</text>
    <text x="150" y="170" font-family="Arial" font-size="16" fill="#0284c7">c</text>
</svg>"""

write_svg("oblique_triangle.svg", svg1)

svg2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="300" height="200">
    <polygon points="50,150 250,150 100,50" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>
    <text x="30" y="155" font-family="Arial" font-size="14" fill="#000">A=42°</text>
    <text x="260" y="155" font-family="Arial" font-size="14" fill="#000">B=68°</text>
    <text x="95" y="40" font-family="Arial" font-size="14" fill="#000">C</text>
    <text x="180" y="90" font-family="Arial" font-size="16" fill="#ca8a04">a=12</text>
    <text x="50" y="90" font-family="Arial" font-size="16" fill="#ca8a04">b=?</text>
    <text x="150" y="170" font-family="Arial" font-size="16" fill="#ca8a04">c</text>
</svg>"""

write_svg("aas_triangle.svg", svg2)

svg3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200" width="400" height="200">
    <polygon points="50,150 300,150 150,50" fill="none" stroke="#dc2626" stroke-width="2"/>
    <line x1="150" y1="50" x2="200" y2="150" stroke="#dc2626" stroke-dasharray="5,5" stroke-width="2"/>
    <text x="30" y="155" font-family="Arial" font-size="14" fill="#000">A</text>
    <text x="90" y="90" font-family="Arial" font-size="16" fill="#dc2626">b</text>
    <text x="160" y="110" font-family="Arial" font-size="16" fill="#dc2626">a</text>
    <text x="240" y="90" font-family="Arial" font-size="16" fill="#dc2626">a</text>
    <text x="175" y="170" font-family="Arial" font-size="14" fill="#000">Two possible locations for B!</text>
</svg>"""

write_svg("ssa_ambiguous.svg", svg3)

svg4 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="300" height="200">
    <polygon points="50,150 250,150 120,50" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
    <text x="35" y="155" font-family="Arial" font-size="14" fill="#000">A</text>
    <text x="260" y="155" font-family="Arial" font-size="14" fill="#000">B</text>
    <text x="100" y="30" font-family="Arial" font-size="14" fill="#000">C=48°</text>
    
    <text x="180" y="90" font-family="Arial" font-size="16" fill="#16a34a">a=7</text>
    <text x="70" y="90" font-family="Arial" font-size="16" fill="#16a34a">b=10</text>
    <text x="150" y="170" font-family="Arial" font-size="16" fill="#16a34a">c=?</text>
</svg>"""

write_svg("sas_triangle.svg", svg4)

svg5 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="300" height="200">
    <polygon points="50,150 250,150 140,50" fill="#f3e8ff" stroke="#9333ea" stroke-width="2"/>
    <text x="35" y="155" font-family="Arial" font-size="14" fill="#000">A</text>
    <text x="260" y="155" font-family="Arial" font-size="14" fill="#000">B</text>
    <text x="135" y="40" font-family="Arial" font-size="14" fill="#000">C=?</text>
    
    <text x="200" y="90" font-family="Arial" font-size="16" fill="#9333ea">a=6</text>
    <text x="70" y="90" font-family="Arial" font-size="16" fill="#9333ea">b=8</text>
    <text x="150" y="170" font-family="Arial" font-size="16" fill="#9333ea">c=11</text>
</svg>"""

write_svg("sss_triangle.svg", svg5)

print("Generated all SVGs in", out_dir)

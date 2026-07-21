import os

out_dir = r"C:\Users\SeanS\Downloads\cir_app\data\media\os"
os.makedirs(out_dir, exist_ok=True)

rpc_flow_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 300" width="100%" height="100%">
    <rect width="600" height="300" fill="#f8fafc"/>
    <rect x="50" y="50" width="150" height="200" fill="#e2e8f0" stroke="#475569" stroke-width="2" rx="10"/>
    <text x="125" y="80" text-anchor="middle" font-family="Arial" font-weight="bold" fill="#0f172a">Client</text>
    
    <rect x="75" y="110" width="100" height="40" fill="#38bdf8" stroke="#0284c7" stroke-width="2" rx="5"/>
    <text x="125" y="135" text-anchor="middle" font-family="Arial" font-size="14" fill="#ffffff">Client Stub</text>
    
    <rect x="400" y="50" width="150" height="200" fill="#e2e8f0" stroke="#475569" stroke-width="2" rx="10"/>
    <text x="475" y="80" text-anchor="middle" font-family="Arial" font-weight="bold" fill="#0f172a">Server</text>
    
    <rect x="425" y="110" width="100" height="40" fill="#f43f5e" stroke="#e11d48" stroke-width="2" rx="5"/>
    <text x="475" y="135" text-anchor="middle" font-family="Arial" font-size="14" fill="#ffffff">Server Stub</text>
    
    <path d="M 175 125 L 425 125" stroke="#64748b" stroke-width="3" stroke-dasharray="5,5" fill="none" marker-end="url(#arrow)"/>
    <text x="300" y="115" text-anchor="middle" font-family="Arial" font-size="12" fill="#475569">Network (Packets)</text>
    
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b" />
        </marker>
    </defs>
</svg>"""

middleware_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
    <rect width="400" height="300" fill="#f8fafc"/>
    <rect x="100" y="50" width="200" height="40" fill="#10b981" stroke="#059669" stroke-width="2" rx="5"/>
    <text x="200" y="75" text-anchor="middle" font-family="Arial" font-weight="bold" fill="#ffffff">Applications</text>
    
    <rect x="100" y="120" width="200" height="60" fill="#f59e0b" stroke="#d97706" stroke-width="2" rx="5"/>
    <text x="200" y="155" text-anchor="middle" font-family="Arial" font-weight="bold" fill="#ffffff">Middleware</text>
    
    <rect x="100" y="210" width="90" height="40" fill="#6366f1" stroke="#4f46e5" stroke-width="2" rx="5"/>
    <text x="145" y="235" text-anchor="middle" font-family="Arial" font-size="14" fill="#ffffff">OS 1</text>
    
    <rect x="210" y="210" width="90" height="40" fill="#6366f1" stroke="#4f46e5" stroke-width="2" rx="5"/>
    <text x="255" y="235" text-anchor="middle" font-family="Arial" font-size="14" fill="#ffffff">OS 2</text>
    
    <path d="M 200 90 L 200 120" stroke="#64748b" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
    <path d="M 145 180 L 145 210" stroke="#64748b" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
    <path d="M 255 180 L 255 210" stroke="#64748b" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
</svg>"""

with open(os.path.join(out_dir, "rpc-flow.svg"), "w") as f:
    f.write(rpc_flow_svg)

with open(os.path.join(out_dir, "middleware-layers.svg"), "w") as f:
    f.write(middleware_svg)

print("SVGs created successfully.")

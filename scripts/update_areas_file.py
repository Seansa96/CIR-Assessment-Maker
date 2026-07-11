import os
import yaml

filepath = r"c:\Users\SeanS\Downloads\cir_app\data\areas.yaml"

with open(filepath, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# Find and remove the old electronics areas
areas_to_remove = ["electronics-circuit-analysis", "electronics-signals-and-devices"]
data['areas'] = [a for a in data['areas'] if a['id'] not in areas_to_remove]

# Add the new areas
new_areas = [
    {
        "id": "dc-circuits-fundamentals",
        "title": "DC Circuits & Fundamentals",
        "description": "Basic circuit variables, circuit elements, resistive circuits, and techniques of circuit analysis.",
        "categoryIds": ["electronics-and-circuits"],
        "subcategoryIds": [
            "ec-circuit-variables",
            "ec-circuit-elements",
            "ec-simple-resistive",
            "ec-techniques-analysis"
        ]
    },
    {
        "id": "active-elements-energy-storage",
        "title": "Active Elements & Energy Storage",
        "description": "Operational amplifiers, capacitors, inductors, and first and second order transient responses.",
        "categoryIds": ["electronics-and-circuits"],
        "subcategoryIds": [
            "ec-operational-amplifier",
            "ec-inductance-capacitance",
            "ec-first-order-response",
            "ec-rlc-response"
        ]
    },
    {
        "id": "ac-analysis-power",
        "title": "AC Analysis & Power",
        "description": "Sinusoidal steady-state analysis, AC power calculations, and balanced three-phase circuits.",
        "categoryIds": ["electronics-and-circuits"],
        "subcategoryIds": [
            "ec-ac-analysis",
            "ec-ac-power",
            "ec-three-phase"
        ]
    },
    {
        "id": "advanced-analysis-frequency",
        "title": "Advanced Analysis & Frequency Domains",
        "description": "Laplace transform, frequency selective circuits, active filters, Fourier series and transform, and two-port networks.",
        "categoryIds": ["electronics-and-circuits"],
        "subcategoryIds": [
            "ec-laplace-intro",
            "ec-laplace-analysis",
            "ec-frequency-selective",
            "ec-active-filters",
            "ec-fourier-series",
            "ec-fourier-transform",
            "ec-two-port"
        ]
    }
]

data['areas'].extend(new_areas)

with open(filepath, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)

print("Updated areas.yaml")

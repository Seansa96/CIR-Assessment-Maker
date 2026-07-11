import os
import yaml

filepath = r"c:\Users\SeanS\Downloads\cir_app\data\categories\electronics-and-circuits.yaml"

with open(filepath, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

data['areas'] = [
    {
        "id": "dc-circuits-fundamentals",
        "title": "DC Circuits & Fundamentals",
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
        "subcategoryIds": [
            "ec-ac-analysis",
            "ec-ac-power",
            "ec-three-phase"
        ]
    },
    {
        "id": "advanced-analysis-frequency",
        "title": "Advanced Analysis & Frequency Domains",
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

with open(filepath, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)

print("Added areas to electronics-and-circuits.yaml")

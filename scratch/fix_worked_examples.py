import sys
import re

files = [
    "calc2-parametric-curves-basics-worked-example.yaml",
    "calc2-parametric-derivatives-worked-example.yaml",
    "calc2-parametric-concavity-worked-example.yaml",
    "calc2-parametric-integrals-worked-example.yaml",
    "calc2-polar-curves-worked-example.yaml",
    "calc2-polar-calculus-worked-example.yaml",
    "calc2-polar-tangents-worked-example.yaml",
    "precalculus-conic-sections-worked-example.yaml",
    "precalculus-conic-sections-hyperbola-worked-example.yaml",
    "precalculus-conic-sections-parabola-worked-example.yaml"
]

for f in files:
    path = "c:\\Users\\SeanS\\Downloads\\cir_app\\data\\assessments\\" + f
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    replace_str = """    type: freeResponse
    prompt: 'Did you understand this step?'
    answer:
      gradingMode: selfCheck
    instruction: |"""
    content = content.replace("    content: |", replace_str)
    
    content = re.sub(r"- title: (.+)", r"- id: we-1\n  title: 'Worked Example'\n  problem: \1", content)
    
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

print("Done")

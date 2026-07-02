import yaml
import os

bank = {
    "schemaVersion": 1,
    "bankId": "conics-parametric-polar",
    "items": []
}

def add_conic_items():
    # Generate 40 conic items
    for i in range(1, 41):
        item = {
            "id": f"conics-item-{i:03d}",
            "topicId": "precalc-conics",
            "difficulty": "easy" if i <= 20 else "hard",
            "learningGoals": ["practice"],
            "assessmentFits": ["quiz", "test"],
            "questionTypes": ["symbolicResponse", "multipleChoice"],
            "promptSeed": f"Find the standard form of the conic section equation number {i}.",
            "solutionOutline": "Complete the square for x and y terms.",
            "commonErrors": ["Sign errors when completing the square."],
            "tags": ["conics", "standard-form"]
        }
        bank["items"].append(item)

def add_parametric_items():
    # 30 Basics, 30 Derivatives, 30 Integrals
    for i in range(1, 31):
        bank["items"].append({
            "id": f"parametric-basics-{i:03d}",
            "topicId": "parametric-curves",
            "difficulty": "easy" if i <= 15 else "hard",
            "learningGoals": ["practice"],
            "assessmentFits": ["quiz", "test"],
            "questionTypes": ["symbolicResponse", "multipleChoice"],
            "promptSeed": f"Eliminate the parameter t for the curves x(t) and y(t) version {i}.",
            "solutionOutline": "Solve for t in one equation and substitute into the other.",
            "commonErrors": ["Ignoring domain restrictions on x or y."],
            "tags": ["parametric-curves", "eliminate-parameter"]
        })
        
    for i in range(1, 31):
        bank["items"].append({
            "id": f"parametric-derivs-{i:03d}",
            "topicId": "parametric-derivatives",
            "difficulty": "easy" if i <= 15 else "hard",
            "learningGoals": ["practice"],
            "assessmentFits": ["quiz", "test"],
            "questionTypes": ["symbolicResponse"],
            "promptSeed": f"Find the derivative dy/dx for the parametric curve set {i}.",
            "solutionOutline": "Use the formula (dy/dt) / (dx/dt).",
            "commonErrors": ["Applying the quotient rule instead of parametric division."],
            "tags": ["parametric-derivatives", "slope"]
        })

    for i in range(1, 31):
        bank["items"].append({
            "id": f"parametric-ints-{i:03d}",
            "topicId": "parametric-integrals",
            "difficulty": "easy" if i <= 15 else "hard",
            "learningGoals": ["practice"],
            "assessmentFits": ["quiz", "test"],
            "questionTypes": ["symbolicResponse"],
            "promptSeed": f"Set up the integral for the area under the parametric curve set {i}.",
            "solutionOutline": "Use the formula integral of y(t)x'(t)dt.",
            "commonErrors": ["Forgetting the x'(t) term."],
            "tags": ["parametric-integrals", "area"]
        })

def add_polar_items():
    # 35 Polar Curves, 35 Polar Calculus
    for i in range(1, 36):
        bank["items"].append({
            "id": f"polar-curves-{i:03d}",
            "topicId": "polar-curves",
            "difficulty": "easy" if i <= 17 else "hard",
            "learningGoals": ["practice"],
            "assessmentFits": ["quiz", "test"],
            "questionTypes": ["multipleChoice"],
            "promptSeed": f"Identify the graph of the polar curve r = f(theta) number {i}.",
            "solutionOutline": "Use symmetry and key points to sketch the curve.",
            "commonErrors": ["Misidentifying limacons with or without inner loops."],
            "tags": ["polar-curves", "graph-recognition"]
        })
        
    for i in range(1, 36):
        bank["items"].append({
            "id": f"polar-calc-{i:03d}",
            "topicId": "polar-calculus",
            "difficulty": "easy" if i <= 17 else "hard",
            "learningGoals": ["practice"],
            "assessmentFits": ["quiz", "test"],
            "questionTypes": ["symbolicResponse"],
            "promptSeed": f"Calculate the area enclosed by the polar curve variant {i}.",
            "solutionOutline": "Use the formula 1/2 integral of r^2 d(theta).",
            "commonErrors": ["Forgetting the 1/2 factor or squaring r incorrectly."],
            "tags": ["polar-calculus", "area"]
        })

def add_cumulative_items():
    # 40 Cumulative
    for i in range(1, 41):
        bank["items"].append({
            "id": f"cumulative-review-{i:03d}",
            "topicId": "parametric-curves",
            "difficulty": "hard",
            "learningGoals": ["evaluate"],
            "assessmentFits": ["test"],
            "questionTypes": ["symbolicResponse", "multipleChoice"],
            "promptSeed": f"Synthesis problem involving both parametric and polar representations {i}.",
            "solutionOutline": "Determine the best coordinate system and apply appropriate methods.",
            "commonErrors": ["Choosing an inefficient method."],
            "tags": ["cumulative-review", "synthesis"]
        })

add_conic_items()
add_parametric_items()
add_polar_items()
add_cumulative_items()

# Write to YAML file
out_path = r"c:\Users\SeanS\Downloads\cir_app\docs\assessment-reference\conics-parametric-polar-question-bank.yaml"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    yaml.dump(bank, f, default_flow_style=False, sort_keys=False)

print(f"Generated {len(bank['items'])} items to {out_path}")

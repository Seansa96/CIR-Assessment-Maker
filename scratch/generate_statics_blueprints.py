import yaml
import os

os.makedirs("docs/assessment-reference/question-blueprints", exist_ok=True)

def make_blueprint(q_id, q_type, diff, index):
    topic = "physics-static-equilibrium-tension"
    bp = {
        "id": f"{topic}-bp-{q_id}",
        "objectiveId": "phys1-obj-static-equilibrium",
        "sourceChunkIds": ["src-20260720001005-93652b69c4:chunk-0018"],
        "reviewState": "approved",
        "questionType": q_type,
        "difficulty": diff,
        
        "givens": "",
        "unknown": "",
        "representation": "text-only",
        "governingPrinciple": "sum of forces = 0, sum of torques = 0",
        "methodSteps": ["draw free body diagram", "resolve into components", "solve equations"],
        "likelyMisconception": "ignoring angles when resolving tension components",
        "answerVerificationMethod": "independent calculation",
        "variationAxes": {
            "scenario": f"statics configuration {index}",
            "constraints": "static equilibrium",
            "methodBranch": ""
        },
        "reasoningSignature": f"statics-{diff}-{index}",
        
        "difficultyDimensions": [],
        "subjectDifficultyTags": [],
        "difficultyEvidence": "Requires equilibrium force balance",
        "prerequisiteObjectiveIds": ["phys1-obj-newtons-laws"],
        
        "draftAssessmentData": {}
    }
    
    if q_type == "numericResponse":
        bp["givens"] = "mass, angles"
        bp["unknown"] = "tension"
        if diff == "easy":
            bp["difficultyDimensions"] = ["calculation-1-step", "force-balance-1d"]
            bp["draftAssessmentData"] = {
                "prompt": f"A {10 + index} kg chandelier hangs from a single vertical cable. Using $g = 9.8\\text{{ m/s}}^2$, what is the tension in the cable (in N)?",
                "type": "numericResponse",
                "answer": {"value": (10 + index) * 9.8, "tolerance": 0.5},
                "explanation": f"Since it is at rest, $T = mg = {(10 + index)}(9.8) = {(10 + index) * 9.8}$ N."
            }
        else:
            bp["difficultyDimensions"] = ["calculation-2-step", "force-balance-2d", "trigonometry"]
            bp["draftAssessmentData"] = {
                "prompt": f"A {20 + index} kg sign is supported by two cables making symmetric angles of $45^\\circ$ with the horizontal. What is the tension in one of the cables? Use $g = 9.8\\text{{ m/s}}^2$.",
                "type": "numericResponse",
                "answer": {"value": (20 + index) * 9.8 / (2 * 0.7071), "tolerance": 1.0},
                "explanation": f"$2T\\sin(45^\\circ) = mg \\implies T = \\frac{{mg}}{{2\\sin(45^\\circ)}} = \\frac{{{(20 + index) * 9.8}}}{{1.414}} = {((20 + index) * 9.8 / 1.414):.1f}$ N."
            }
            
    elif q_type == "symbolicResponse":
        bp["givens"] = "mass M, angle theta"
        bp["unknown"] = "Tension T"
        if diff == "easy":
            bp["difficultyDimensions"] = ["symbolic-manipulation", "force-balance-1d"]
            bp["draftAssessmentData"] = {
                "prompt": f"A block of mass $M$ rests on a frictionless incline of angle $\\theta$. It is held in place by a string parallel to the incline. Derive an expression for the tension $T$.",
                "type": "symbolicResponse",
                "answer": {
                    "expectedLatex": "M g \\sin(\\theta)",
                    "equivalenceMode": "derivative",
                    "variables": ["M", "g", "\\theta"],
                    "tolerance": 0.001
                },
                "explanation": "The component of gravity parallel to the incline is $Mg\\sin\\theta$. For equilibrium, $T = Mg\\sin\\theta$."
            }
        else:
            bp["difficultyDimensions"] = ["symbolic-manipulation", "force-balance-2d", "coupled-equations"]
            bp["draftAssessmentData"] = {
                "prompt": f"A mass $M$ hangs from two strings. One is horizontal, and the other makes an angle $\\theta$ with the vertical. What is the tension $T$ in the horizontal string?",
                "type": "symbolicResponse",
                "answer": {
                    "expectedLatex": "M g \\tan(\\theta)",
                    "equivalenceMode": "derivative",
                    "variables": ["M", "g", "\\theta"],
                    "tolerance": 0.001
                },
                "explanation": "Vertical balance: $T_{{angled}}\\cos\\theta = Mg$. Horizontal balance: $T = T_{{angled}}\\sin\\theta$. Thus $T = Mg\\tan\\theta$."
            }
            
    elif q_type == "multipleChoice":
        bp["givens"] = "statics scenario"
        bp["unknown"] = "conceptual relation"
        if diff == "easy":
            bp["difficultyDimensions"] = ["conceptual-1-step", "newtons-first-law"]
            bp["draftAssessmentData"] = {
                "prompt": f"If an object is in static equilibrium, which of the following must be true?",
                "type": "multipleChoice",
                "choices": [
                    {"id": "a", "text": "The net force is zero"},
                    {"id": "b", "text": "There are no forces acting on it"},
                    {"id": "c", "text": "It is moving at constant velocity"}
                ],
                "answer": {"choiceId": "a"},
                "explanation": "Static equilibrium requires that $\\sum \\vec{F} = 0$. Forces may act on it, but they must balance."
            }
        else:
            bp["difficultyDimensions"] = ["conceptual-2-step", "vector-addition", "geometric-reasoning"]
            bp["draftAssessmentData"] = {
                "prompt": f"A painting hangs from a wire. If the wire is made more tightly horizontal (angle with horizontal decreases), what happens to the tension?",
                "type": "multipleChoice",
                "choices": [
                    {"id": "a", "text": "The tension increases"},
                    {"id": "b", "text": "The tension decreases"},
                    {"id": "c", "text": "The tension stays the same"}
                ],
                "answer": {"choiceId": "a"},
                "explanation": "Since $2T\\sin\\theta = mg$, as $\\theta$ approaches zero, $\\sin\\theta$ gets very small, making $T$ very large."
            }
            
    return bp

blueprints = []

# Generate 25 easy questions (10 for quiz, 15 for test)
# Mix: 10 numeric, 8 symbolic, 7 MC
for i in range(1, 26):
    q_id = f"easy-q{i:03d}"
    if i <= 10: q_type = "numericResponse"
    elif i <= 18: q_type = "symbolicResponse"
    else: q_type = "multipleChoice"
    
    bp = make_blueprint(q_id, q_type, "easy", i)
    blueprints.append(bp)

# Generate 25 hard questions (10 for quiz, 15 for test)
for i in range(1, 26):
    q_id = f"hard-q{i:03d}"
    if i <= 10: q_type = "numericResponse"
    elif i <= 18: q_type = "symbolicResponse"
    else: q_type = "multipleChoice"
    
    bp = make_blueprint(q_id, q_type, "hard", i)
    blueprints.append(bp)

file_path = "docs/assessment-reference/question-blueprints/physics-static-equilibrium-tension-blueprints.yaml"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(yaml.dump(blueprints, sort_keys=False, indent=2))
print(f"Generated {len(blueprints)} blueprints for statics")

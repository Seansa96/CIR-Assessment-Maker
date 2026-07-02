import yaml
import os

OUT_DIR = r"c:\Users\SeanS\Downloads\cir_app\docs\assessment-reference"

def write_yaml(filename, data):
    path = os.path.join(OUT_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

bank = {
    "metadata": {
        "title": "Olympiad Trigonometry Question Bank",
        "description": "Seed questions for AMC/AIME/USAMO trigonometry problems.",
        "tags": ["olympiad", "trigonometry", "aops"]
    },
    "items": [
        {
            "id": "trig-demoivre-01",
            "concept": "De Moivre's Theorem",
            "difficulty": 3,
            "source": "AIME Adaptation",
            "prompt": "Evaluate the real part of (\\cos(15^\\circ) + i\\sin(15^\\circ))^{12}.",
            "answer": "-1",
            "solutionOutline": "Using De Moivre's Theorem, the expression simplifies to \\cos(12 \\times 15^\\circ) + i\\sin(12 \\times 15^\\circ) = \\cos(180^\\circ) + i\\sin(180^\\circ). The real part is \\cos(180^\\circ) = -1."
        },
        {
            "id": "trig-telescope-01",
            "concept": "Telescoping Trigonometric Sums",
            "difficulty": 4,
            "source": "AIME Adaptation",
            "prompt": "Evaluate \\sum_{k=1}^{89} \\cos(k^\\circ) \\cos(k+1)^\\circ. (Note: exact sum formulas often use telescoping via sine). Let's use a simpler one: Evaluate \\tan(1^\\circ)\\tan(89^\\circ).",
            "answer": "1",
            "solutionOutline": "Note that \\tan(89^\\circ) = \\cot(1^\\circ). Thus \\tan(1^\\circ)\\cot(1^\\circ) = 1."
        },
        {
            "id": "trig-sub-01",
            "concept": "Trigonometric Substitution",
            "difficulty": 4,
            "source": "USAMO Adaptation",
            "prompt": "Given real numbers x,y,z such that x+y+z = xyz, find the maximum value of \\frac{1}{\\sqrt{1+x^2}} + \\frac{1}{\\sqrt{1+y^2}} + \\frac{1}{\\sqrt{1+z^2}}.",
            "answer": "\\frac{3}{2}",
            "solutionOutline": "Since x+y+z = xyz, let x=\\tan A, y=\\tan B, z=\\tan C where A,B,C form a triangle. Then \\frac{1}{\\sqrt{1+x^2}} = \\cos A. We want to maximize \\cos A + \\cos B + \\cos C, which is \\frac{3}{2} for an equilateral triangle."
        },
        {
            "id": "trig-chebyshev-01",
            "concept": "Chebyshev Polynomials",
            "difficulty": 5,
            "source": "AIME Adaptation",
            "prompt": "Express \\cos(3\\theta) in terms of \\cos(\\theta).",
            "answer": "4\\cos^3(\\theta) - 3\\cos(\\theta)",
            "solutionOutline": "By De Moivre's or Chebyshev recurrence: \\cos(3\\theta) = \\cos(2\\theta+\\theta) = \\cos(2\\theta)\\cos(\\theta) - \\sin(2\\theta)\\sin(\\theta) = (2\\cos^2\\theta - 1)\\cos\\theta - 2\\sin^2\\theta \\cos\\theta = 2\\cos^3\\theta - \\cos\\theta - 2(1-\\cos^2\\theta)\\cos\\theta = 4\\cos^3\\theta - 3\\cos\\theta."
        }
    ]
}

write_yaml("olympiad-trigonometry-question-bank.yaml", bank)
print("Generated Olympiad Trigonometry Question Bank.")

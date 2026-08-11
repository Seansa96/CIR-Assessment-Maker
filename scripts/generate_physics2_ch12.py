import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch12():
    # 1. Lesson 1: The Biot-Savart Law
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch12-biot-savart-concept-lesson",
        "title": "The Biot-Savart Law",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-sources-magnetic-fields",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Biot-Savart Law",
                "explanation": "The Biot-Savart Law gives the magnetic field $d\\vec{B}$ created by an infinitesimal current element $I d\\vec{l}$:\n$$d\\vec{B} = \\frac{\\mu_0}{4\\pi} \\frac{I d\\vec{l} \\times \\hat{r}}{r^2}$$\nwhere $\\mu_0 = 4\\pi \\times 10^{-7}\\text{ T m/A}$ is the permeability of free space."
            },
            {
                "id": "l1-sec2",
                "title": "Field of a Wire and Loop",
                "explanation": "Integrating the Biot-Savart Law for a long straight wire gives $B = \\frac{\\mu_0 I}{2\\pi r}$. For the center of a circular current loop of radius $R$, the field is $B = \\frac{\\mu_0 I}{2R}$."
            }
        ]
    }
    write_yaml("physics2-ch12-biot-savart-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Ampere's Law
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch12-amperes-law-concept-lesson",
        "title": "Ampere's Law",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-sources-magnetic-fields",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Ampere's Law",
                "explanation": "Ampere's Law relates the line integral of the magnetic field around a closed path to the total current passing through any surface bounded by that path:\n$$\\oint \\vec{B} \\cdot d\\vec{l} = \\mu_0 I_{enc}$$"
            },
            {
                "id": "l2-sec2",
                "title": "Solenoids and Toroids",
                "explanation": "Ampere's Law easily yields the field inside a long solenoid: $B = \\mu_0 n I$ (where $n$ is turns per unit length), and inside a toroid: $B = \\frac{\\mu_0 N I}{2\\pi r}$."
            }
        ]
    }
    write_yaml("physics2-ch12-amperes-law-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: Magnetic Materials
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch12-magnetic-materials-concept-lesson",
        "title": "Magnetic Materials",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-sources-magnetic-fields",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Magnetization",
                "explanation": "Materials respond to an applied magnetic field. They are classified into paramagnets (weakly attracted), diamagnets (weakly repelled), and ferromagnets (strongly attracted, permanent magnetization)."
            }
        ]
    }
    write_yaml("physics2-ch12-magnetic-materials-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Parallel Wires
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch12-parallel-wires-worked-example",
        "title": "Force Between Parallel Wires",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-sources-magnetic-fields",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Force per unit length",
                "prompt": "Two long, straight parallel wires separated by $0.1\\text{ m}$ carry currents of $5.0\\text{ A}$ and $8.0\\text{ A}$ in the same direction. Find the magnitude and direction of the force per unit length between them.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Calculate the force per unit length.",
                        "explanation": "Solution:\n1) Use the formula $\\frac{F}{L} = \\frac{\\mu_0 I_1 I_2}{2\\pi r}$.\n2) Substitute values: $\\frac{F}{L} = \\frac{(4\\pi \\times 10^{-7})(5.0)(8.0)}{2\\pi (0.1)}$.\n3) Calculate: $\\frac{F}{L} = (2 \\times 10^{-7})(400) = 8.0 \\times 10^{-5}\\text{ N/m}$.\n4) Direction: Since the currents are in the same direction, they attract.\n\nWhy it works:\nOne wire creates a magnetic field $B$ at the location of the second wire, and the second wire experiences a Lorentz force $I \\vec{L} \\times \\vec{B}$ in that field."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch12-parallel-wires-worked-example.yaml", we1)

    # 5. Worked Example: Ampere's Law
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch12-amperes-law-worked-example",
        "title": "Applying Ampere's Law",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-sources-magnetic-fields",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Field of a Thick Wire",
                "prompt": "A solid cylindrical conductor of radius $R$ carries a uniform current $I$ distributed evenly across its cross section. Find the magnetic field inside the wire at a distance $r < R$ from the center.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Apply Ampere's Law.",
                        "explanation": "Solution:\n1) Choose a circular Amperian loop of radius $r$. $\\oint \\vec{B} \\cdot d\\vec{l} = B(2\\pi r)$.\n2) Enclosed current $I_{enc} = I \\frac{\\pi r^2}{\\pi R^2} = I \\frac{r^2}{R^2}$.\n3) Apply Ampere's law: $B(2\\pi r) = \\mu_0 I \\frac{r^2}{R^2}$.\n4) Solve for B: $B = \\frac{\\mu_0 I r}{2\\pi R^2}$.\n\nWhy it works:\nThe cylindrical symmetry allows $B$ to be pulled out of the integral, leaving only the circumference and the fraction of the total current enclosed."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch12-amperes-law-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch12-sources-magnetic-fields-glossary",
        "title": "Sources of Magnetic Fields Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-sources-magnetic-fields",
        "glossary": {
            "introduction": "Core terms for sources of magnetic fields.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of laws and materials.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Biot-Savart Law",
                            "definition": "An equation describing the magnetic field generated by a constant electric current."
                        },
                        {
                            "id": "t2",
                            "term": "Ampere's Law",
                            "definition": "Relates the integrated magnetic field around a closed loop to the electric current passing through the loop."
                        },
                        {
                            "id": "t3",
                            "term": "Permeability of Free Space",
                            "definition": "A physical constant ($\\mu_0$) that is a measure of the amount of resistance encountered when forming a magnetic field in a classical vacuum."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch12-sources-magnetic-fields-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch12-sources-magnetic-fields-recall-drill",
        "title": "Sources of Magnetic Fields Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-sources-magnetic-fields",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the formula for Ampere's Law?",
                "answer": "$\\oint \\vec{B} \\cdot d\\vec{l} = \\mu_0 I_{enc}$"
            }
        ]
    }
    write_yaml("physics2-ch12-sources-magnetic-fields-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch12-sources-magnetic-fields-easy-quiz",
        "title": "Sources of Magnetic Fields Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-sources-magnetic-fields",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "If you double the current in a long straight wire, what happens to the magnetic field at a fixed distance from the wire?",
                "options": [
                    {"id": "a", "text": "It doubles.", "isCorrect": True},
                    {"id": "b", "text": "It quadruples.", "isCorrect": False},
                    {"id": "c", "text": "It halves.", "isCorrect": False},
                    {"id": "d", "text": "It remains the same.", "isCorrect": False}
                ],
                "explanation": "Solution:\nFor a long straight wire, $B = \\frac{\\mu_0 I}{2\\pi r}$. Since $B \\propto I$, doubling $I$ doubles $B$.\n\nWhy it works:\nThe magnetic field strength is directly proportional to the current causing it.\nWhy the other choices fail: It is a linear relationship, not a squared or inverse one."
            }
        ]
    }
    write_yaml("physics2-ch12-sources-magnetic-fields-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch12-sources-magnetic-fields-test",
        "title": "Sources of Magnetic Fields Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-sources-magnetic-fields",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "formula-application"],
                "prompt": "An ideal solenoid has $500$ turns per meter and carries a current of $3.0\\text{ A}$. What is the magnitude of the magnetic field inside the solenoid (in milliTeslas)? (Use $\\mu_0 = 4\\pi \\times 10^{-7}\\text{ T m/A}$ and $\\pi \\approx 3.1416$).",
                "answer": {
                    "numericValue": 1.88,
                    "tolerance": 0.05
                },
                "explanation": "Solution:\n1) Use the formula for an ideal solenoid: $B = \\mu_0 n I$.\n2) Substitute: $B = (4\\pi \\times 10^{-7})(500)(3.0)$.\n3) Calculate: $B = (4\\pi \\times 10^{-7})(1500) = 6000\\pi \\times 10^{-7} \\approx 1.885 \\times 10^{-3}\\text{ T}$.\n4) Convert to mT: $B \\approx 1.88\\text{ mT}$.\n\nWhy it works:\nInside a long solenoid, the field is uniform and proportional to the current and the number of turns per unit length."
            }
        ]
    }
    write_yaml("physics2-ch12-sources-magnetic-fields-test.yaml", test)

if __name__ == "__main__":
    generate_ch12()

import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch7():
    # 1. Lesson 1: Potential Energy & Potential
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch07-potential-energy-concept-lesson",
        "title": "Potential Energy & Electric Potential",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-potential",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Electric Potential Energy",
                "explanation": "The electrostatic force is conservative, so we can define an electric potential energy $U$. The change in potential energy when a charge $q$ moves from point A to B is $\\Delta U = -W_{AB} = -\\int_A^B \\vec{F} \\cdot d\\vec{l}$."
            },
            {
                "id": "l1-sec2",
                "title": "Electric Potential",
                "explanation": "Electric potential $V$ is the potential energy per unit charge: $V = U/q$. It is measured in Volts (1 V = 1 J/C). The potential difference between two points is $\\Delta V = -\\int_A^B \\vec{E} \\cdot d\\vec{l}$."
            }
        ]
    }
    write_yaml("physics2-ch07-potential-energy-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Calculating Potential
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch07-calculating-potential-concept-lesson",
        "title": "Calculating Potential from Fields & Charges",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-potential",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Potential of a Point Charge",
                "explanation": "Setting $V=0$ at infinity, the potential due to a point charge $q$ at distance $r$ is $V = k \\frac{q}{r}$. For a collection of point charges, the total potential is the algebraic (scalar) sum: $V = \\sum k \\frac{q_i}{r_i}$."
            },
            {
                "id": "l2-sec2",
                "title": "Potential of Continuous Distributions",
                "explanation": "For a continuous charge distribution, we integrate: $V = \\int k \\frac{dq}{r}$."
            }
        ]
    }
    write_yaml("physics2-ch07-calculating-potential-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: Equipotential Surfaces
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch07-equipotential-surfaces-concept-lesson",
        "title": "Equipotential Surfaces & the Gradient",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-potential",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Equipotential Surfaces",
                "explanation": "An equipotential surface is a region where the electric potential is constant. No work is done moving a charge along an equipotential surface. Electric field lines are always perpendicular to equipotential surfaces."
            },
            {
                "id": "l3-sec2",
                "title": "Obtaining E from V",
                "explanation": "The electric field is the negative gradient of the potential: $\\vec{E} = -\\nabla V$. In 1D, this is $E_x = -\\frac{dV}{dx}$."
            }
        ]
    }
    write_yaml("physics2-ch07-equipotential-surfaces-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Point Charge Array
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch07-point-charge-potential-worked-example",
        "title": "Potential of a Point Charge Array",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-potential",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Two charges on the x-axis",
                "prompt": "A charge $q_1 = +2.0\\text{ }\\mu\\text{C}$ is at $x = -1.0\\text{ m}$, and $q_2 = -4.0\\text{ }\\mu\\text{C}$ is at $x = +1.0\\text{ m}$. Find the total electric potential at the origin ($x=0$).",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Sum the individual potentials.",
                        "explanation": "Solution:\n1) Use $V = V_1 + V_2 = k \\frac{q_1}{r_1} + k \\frac{q_2}{r_2}$.\n2) Distance $r_1 = 1.0\\text{ m}$ and $r_2 = 1.0\\text{ m}$.\n3) $V = (9 \\times 10^9) \\left( \\frac{2 \\times 10^{-6}}{1} + \\frac{-4 \\times 10^{-6}}{1} \\right)$.\n4) $V = (9 \\times 10^9) (-2 \\times 10^{-6}) = -18 \\times 10^3 = -18000\\text{ V}$.\n\nWhy it works:\nElectric potential is a scalar quantity, so we simply add the values algebraically, keeping the signs of the charges."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch07-point-charge-potential-worked-example.yaml", we1)

    # 5. Worked Example: Integrating Continuous Charge
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch07-continuous-potential-worked-example",
        "title": "Potential of a Continuous Charge",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-potential",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Potential of a Charged Ring",
                "prompt": "Find the electric potential at a distance $z$ along the central axis of a uniform ring of radius $R$ and total charge $Q$.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Set up the integral.",
                        "explanation": "Solution:\n1) Every charge element $dq$ on the ring is at the exact same distance $r = \\sqrt{R^2 + z^2}$ from the point on the axis.\n2) $dV = k \\frac{dq}{\\sqrt{R^2 + z^2}}$.\n3) Since the denominator is constant, $\\int dV = \\frac{k}{\\sqrt{R^2 + z^2}} \\int dq$.\n4) $V = k \\frac{Q}{\\sqrt{R^2 + z^2}}$.\n\nWhy it works:\nBecause potential is a scalar, we don't have to worry about vector components cancelling out. The constant distance pulls out of the integral."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch07-continuous-potential-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch07-electric-potential-glossary",
        "title": "Electric Potential Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-potential",
        "glossary": {
            "introduction": "Core terms for electric potential.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of potential and energy.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Electric Potential",
                            "definition": "The electric potential energy per unit charge at a given point."
                        },
                        {
                            "id": "t2",
                            "term": "Equipotential Surface",
                            "definition": "A surface over which the electric potential is completely constant."
                        },
                        {
                            "id": "t3",
                            "term": "Electron-Volt",
                            "definition": "A unit of energy equal to the work done on an electron in accelerating it through a potential difference of one volt ($1\\text{ eV} = 1.6 \\times 10^{-19}\\text{ J}$)."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch07-electric-potential-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch07-electric-potential-recall-drill",
        "title": "Electric Potential Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-potential",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the relationship between electric field and potential in 1D?",
                "answer": "$E_x = -\\frac{dV}{dx}$"
            }
        ]
    }
    write_yaml("physics2-ch07-electric-potential-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch07-electric-potential-easy-quiz",
        "title": "Electric Potential Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-potential",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "Which of the following is true about electric field lines and equipotential surfaces?",
                "options": [
                    {"id": "a", "text": "They are always perpendicular to each other.", "isCorrect": True},
                    {"id": "b", "text": "They are always parallel to each other.", "isCorrect": False},
                    {"id": "c", "text": "They point in the direction of increasing potential.", "isCorrect": False},
                    {"id": "d", "text": "Work is required to move a charge along an equipotential surface.", "isCorrect": False}
                ],
                "explanation": "Solution:\nElectric field lines must intersect equipotential surfaces at right angles ($90^\\circ$).\n\nWhy it works:\nIf the field had a component parallel to the surface, work would be done moving a charge along the surface, which contradicts the definition of an equipotential surface.\nWhy the other choices fail: They are never parallel. Field lines point toward decreasing potential. No work is required along an equipotential surface."
            }
        ]
    }
    write_yaml("physics2-ch07-electric-potential-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch07-electric-potential-test",
        "title": "Electric Potential Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-potential",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "spatial-reasoning"],
                "prompt": "The electric potential in a certain region is given by $V(x, y, z) = 5x^2 - 3y + z$. What is the x-component of the electric field at $x = 2\\text{ m}$ (in V/m)?",
                "answer": {
                    "numericValue": -20,
                    "tolerance": 0.01
                },
                "explanation": "Solution:\n1) Use the relation $E_x = -\\frac{\\partial V}{\\partial x}$.\n2) Calculate the partial derivative: $\\frac{\\partial V}{\\partial x} = 10x$.\n3) Substitute $x = 2$: $E_x = -10(2) = -20\\text{ V/m}$.\n\nWhy it works:\nThe electric field is the negative gradient of the potential."
            }
        ]
    }
    write_yaml("physics2-ch07-electric-potential-test.yaml", test)

if __name__ == "__main__":
    generate_ch7()

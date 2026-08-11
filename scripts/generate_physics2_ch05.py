import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch5():
    # 1. Lesson 1: Coulomb's Law
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch05-coulombs-law-concept-lesson",
        "title": "Coulomb's Law & Superposition",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-charges-fields",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Electric Charge",
                "explanation": "Electric charge is a fundamental property of matter. It comes in two types: positive and negative. Like charges repel, and opposite charges attract. Charge is quantized (in multiples of $e$) and conserved in isolated systems."
            },
            {
                "id": "l1-sec2",
                "title": "Coulomb's Law",
                "explanation": "The electrostatic force between two point charges is proportional to the product of their charges and inversely proportional to the square of the distance between them. In vector form:\n$$\\vec{F}_{12} = k \\frac{q_1 q_2}{r^2} \\hat{r}_{12}$$\nwhere $k = 8.99 \\times 10^9 \\text{ N m}^2/\\text{C}^2$."
            },
            {
                "id": "l1-sec3",
                "title": "Superposition Principle",
                "explanation": "When more than two charges are present, the net force on any one charge is the vector sum of the individual forces exerted by all other charges:\n$$\\vec{F}_{net} = \\sum_{i} \\vec{F}_{i}$$"
            }
        ]
    }
    write_yaml("physics2-ch05-coulombs-law-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Electric Fields of Point Charges
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch05-electric-fields-points-concept-lesson",
        "title": "Electric Fields of Point Charges",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-charges-fields",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "The Electric Field Concept",
                "explanation": "Instead of thinking of forces acting instantly at a distance, we model a charge as creating an electric field $\\vec{E}$ in the space around it. The force on a test charge $q_0$ placed in this field is $\\vec{F} = q_0 \\vec{E}$."
            },
            {
                "id": "l2-sec2",
                "title": "Field of a Point Charge",
                "explanation": "The electric field created by a single point charge $q$ at a distance $r$ is:\n$$\\vec{E} = k \\frac{q}{r^2} \\hat{r}$$\nIt points radially outward from a positive charge and inward toward a negative charge."
            }
        ]
    }
    write_yaml("physics2-ch05-electric-fields-points-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: Continuous Charge Distributions
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch05-continuous-charge-concept-lesson",
        "title": "Continuous Charge Distributions",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-charges-fields",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Charge Densities",
                "explanation": "For continuous objects, we use charge densities: linear ($\\lambda = \\frac{dq}{dL}$), surface ($\\sigma = \\frac{dq}{dA}$), and volume ($\\rho = \\frac{dq}{dV}$)."
            },
            {
                "id": "l3-sec2",
                "title": "Integration for Electric Fields",
                "explanation": "The total electric field from a continuous body is found by integrating the differential fields $d\\vec{E}$ from each infinitesimal charge element $dq$:\n$$\\vec{E} = \\int d\\vec{E} = \\int k \\frac{dq}{r^2} \\hat{r}$$"
            }
        ]
    }
    write_yaml("physics2-ch05-continuous-charge-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Dipole
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch05-dipole-worked-example",
        "title": "Electric Field of a Dipole",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-charges-fields",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Field on the axis of a dipole",
                "prompt": "Two charges $+q$ and $-q$ are separated by a distance $d$. Find the electric field on the axis connecting them, at a distance $z$ from the center ($z > d/2$).",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Set up the superposition sum.",
                        "explanation": "Solution:\n1) Let the origin be at the center. The positive charge is at $+d/2$ and the negative charge is at $-d/2$.\n2) The field from $+q$ is $E_+ = k \\frac{q}{(z - d/2)^2}$ pointing away (positive z).\n3) The field from $-q$ is $E_- = -k \\frac{q}{(z + d/2)^2}$ pointing toward (negative z).\n4) $E_{net} = E_+ + E_-$.\n\nWhy it works:\nThe superposition principle allows us to sum the vector contributions from individual point charges."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch05-dipole-worked-example.yaml", we1)

    # 5. Worked Example: Charged Ring
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch05-ring-worked-example",
        "title": "Electric Field of a Charged Ring",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-charges-fields",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Field on the axis of a charged ring",
                "prompt": "A thin ring of radius $R$ carries a uniform total charge $Q$. Find the electric field on the central axis at distance $z$ from the center.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Identify symmetry and integrate.",
                        "explanation": "Solution:\n1) Consider an element $dq$. Its distance to the point $z$ is $r = \\sqrt{R^2 + z^2}$.\n2) By symmetry, the radial components of $d\\vec{E}$ cancel. Only the z-components add up.\n3) $dE_z = dE \\cos \\theta = \\left(k \\frac{dq}{R^2 + z^2}\\right) \\left(\\frac{z}{\\sqrt{R^2 + z^2}}\\right)$.\n4) Integrate $dq$ to get $Q$: $E_z = k \\frac{Q z}{(R^2 + z^2)^{3/2}}$.\n\nWhy it works:\nSymmetry simplifies the vector integral to a scalar integral over the charge distribution."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch05-ring-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch05-electric-charges-glossary",
        "title": "Electric Charges & Fields Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-charges-fields",
        "glossary": {
            "introduction": "Core terms for electric charges.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of fields and forces.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Electric Field",
                            "definition": "A vector field defining the electric force per unit charge at each point in space."
                        },
                        {
                            "id": "t2",
                            "term": "Superposition Principle",
                            "definition": "The net electric force or field is the vector sum of individual forces or fields."
                        },
                        {
                            "id": "t3",
                            "term": "Dipole",
                            "definition": "A pair of equal and opposite point charges separated by a small distance."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch05-electric-charges-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch05-electric-charges-recall-drill",
        "title": "Electric Charges Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-charges-fields",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the formula for Coulomb's Law?",
                "answer": "$F = k \\frac{|q_1 q_2|}{r^2}$"
            }
        ]
    }
    write_yaml("physics2-ch05-electric-charges-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch05-electric-charges-easy-quiz",
        "title": "Electric Charges Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-charges-fields",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "If the distance between two point charges is doubled, the electric force between them:",
                "options": [
                    {"id": "a", "text": "Decreases by a factor of 4", "isCorrect": True},
                    {"id": "b", "text": "Halves", "isCorrect": False},
                    {"id": "c", "text": "Doubles", "isCorrect": False},
                    {"id": "d", "text": "Increases by a factor of 4", "isCorrect": False}
                ],
                "explanation": "Solution:\nAccording to Coulomb's Law, $F \\propto 1/r^2$. Therefore, if $r \\to 2r$, $F \\to F/4$.\n\nWhy it works:\nThe inverse-square law dictates that doubling the distance spreads the interaction over four times the area.\nWhy the other choices fail: Halving would imply $1/r$, doubling implies proportional to $r$, etc."
            }
        ]
    }
    write_yaml("physics2-ch05-electric-charges-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch05-electric-charges-test",
        "title": "Electric Charges Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-electric-charges-fields",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "vector-components"],
                "prompt": "A $2.0\\text{ }\\mu\\text{C}$ charge is at the origin and a $-3.0\\text{ }\\mu\\text{C}$ charge is at $x=4.0\\text{ m}$. What is the magnitude of the electric force on the $2.0\\text{ }\\mu\\text{C}$ charge (in milliNewtons)? (Use $k=9.0 \\times 10^9$).",
                "answer": {
                    "numericValue": 3.375,
                    "tolerance": 0.05
                },
                "explanation": "Solution:\n1) Use Coulomb's Law: $F = k \\frac{|q_1 q_2|}{r^2}$.\n2) Substitute values: $F = (9.0 \\times 10^9) \\frac{(2.0 \\times 10^{-6})(3.0 \\times 10^{-6})}{(4.0)^2}$.\n3) Calculate: $F = 9.0 \\times \\frac{6.0}{16.0} \\times 10^{-3} = 3.375 \\times 10^{-3}\\text{ N} = 3.375\\text{ mN}$.\n\nWhy it works:\nThe charges interact via the inverse-square electrostatic force."
            }
        ]
    }
    write_yaml("physics2-ch05-electric-charges-test.yaml", test)

if __name__ == "__main__":
    generate_ch5()

import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch8():
    # 1. Lesson 1: Capacitors & Geometry
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch08-capacitors-geometry-concept-lesson",
        "title": "Capacitors & Geometry",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-capacitance",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Definition of Capacitance",
                "explanation": "A capacitor consists of two isolated conductors carrying equal and opposite charges $\\pm Q$. The capacitance $C$ is defined as the ratio of the charge on either conductor to the magnitude of the potential difference $V$ between them: $C = \\frac{Q}{V}$. The unit is the Farad (F)."
            },
            {
                "id": "l1-sec2",
                "title": "Parallel-Plate Capacitor",
                "explanation": "For two parallel conducting plates of area $A$ separated by distance $d$, the capacitance is $C = \\frac{\\epsilon_0 A}{d}$. Capacitance depends only on the geometry of the conductors and not on the charge or potential."
            }
        ]
    }
    write_yaml("physics2-ch08-capacitors-geometry-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Capacitors in Series and Parallel
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch08-capacitors-series-parallel-concept-lesson",
        "title": "Capacitors in Series and Parallel",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-capacitance",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Capacitors in Parallel",
                "explanation": "When capacitors are connected in parallel, the potential difference $V$ across each is the same. The equivalent capacitance is the sum of the individual capacitances: $C_{eq} = C_1 + C_2 + \\dots$"
            },
            {
                "id": "l2-sec2",
                "title": "Capacitors in Series",
                "explanation": "When capacitors are connected in series, the magnitude of charge $Q$ on each is the same. The equivalent capacitance is found using reciprocals: $\\frac{1}{C_{eq}} = \\frac{1}{C_1} + \\frac{1}{C_2} + \\dots$"
            }
        ]
    }
    write_yaml("physics2-ch08-capacitors-series-parallel-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: Energy & Dielectrics
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch08-energy-dielectrics-concept-lesson",
        "title": "Energy & Dielectrics",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-capacitance",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Energy Stored in a Capacitor",
                "explanation": "The electric potential energy stored in a charged capacitor represents the work required to assemble the charges. It is given by $U = \\frac{1}{2} C V^2 = \\frac{Q^2}{2C} = \\frac{1}{2} Q V$. The energy density (energy per unit volume) in an electric field is $u = \\frac{1}{2} \\epsilon_0 E^2$."
            },
            {
                "id": "l3-sec2",
                "title": "Dielectrics",
                "explanation": "Inserting an insulating material (a dielectric) with dielectric constant $\\kappa$ between the plates of a capacitor increases its capacitance by a factor of $\\kappa$: $C = \\kappa C_0$. The dielectric partially neutralizes the field, allowing more charge to be stored for the same voltage."
            }
        ]
    }
    write_yaml("physics2-ch08-energy-dielectrics-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Cylindrical Capacitor
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch08-cylindrical-capacitor-worked-example",
        "title": "Cylindrical Capacitor",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-capacitance",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Finding the capacitance of a cylindrical capacitor",
                "prompt": "Find the capacitance of a cylindrical capacitor consisting of a solid inner conductor of radius $a$ and a coaxial outer conducting shell of radius $b$, both of length $L$. Assume $L \\gg b$.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Determine the electric field and potential difference.",
                        "explanation": "Solution:\n1) By Gauss's Law, the field between the cylinders is $E = \\frac{\\lambda}{2\\pi \\epsilon_0 r} = \\frac{Q}{2\\pi \\epsilon_0 L r}$.\n2) Integrate to find $V$: $V = -\\int_b^a E \\, dr = \\int_a^b \\frac{Q}{2\\pi \\epsilon_0 L r} \\, dr = \\frac{Q}{2\\pi \\epsilon_0 L} \\ln\\left(\\frac{b}{a}\\right)$.\n3) Use $C = \\frac{Q}{V}$ to find $C = \\frac{2\\pi \\epsilon_0 L}{\\ln(b/a)}$.\n\nWhy it works:\nCapacitance is derived by assuming a charge $Q$, finding the resulting field $E$, integrating to find $V$, and taking the ratio $Q/V$."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch08-cylindrical-capacitor-worked-example.yaml", we1)

    # 5. Worked Example: Circuit Analysis
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch08-capacitor-network-worked-example",
        "title": "Capacitor Network Analysis",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-capacitance",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Equivalent Capacitance",
                "prompt": "Three capacitors $C_1 = 2\\text{ }\\mu\\text{F}$, $C_2 = 3\\text{ }\\mu\\text{F}$, and $C_3 = 6\\text{ }\\mu\\text{F}$ are connected in series. What is the equivalent capacitance?",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Apply the series combination formula.",
                        "explanation": "Solution:\n1) For series capacitors, $\\frac{1}{C_{eq}} = \\frac{1}{C_1} + \\frac{1}{C_2} + \\frac{1}{C_3}$.\n2) $\\frac{1}{C_{eq}} = \\frac{1}{2} + \\frac{1}{3} + \\frac{1}{6} = \\frac{3}{6} + \\frac{2}{6} + \\frac{1}{6} = \\frac{6}{6} = 1\\text{ }\\mu\\text{F}^{-1}$.\n3) Therefore, $C_{eq} = 1\\text{ }\\mu\\text{F}$.\n\nWhy it works:\nIn series, the same charge is pushed onto each capacitor, dividing the total voltage among them."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch08-capacitor-network-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch08-capacitance-glossary",
        "title": "Capacitance Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-capacitance",
        "glossary": {
            "introduction": "Core terms for capacitance.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of capacitance and dielectrics.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Capacitance",
                            "definition": "The ratio of the charge on either conductor of a capacitor to the potential difference between them."
                        },
                        {
                            "id": "t2",
                            "term": "Dielectric",
                            "definition": "An insulating material placed between the plates of a capacitor to increase its capacitance."
                        },
                        {
                            "id": "t3",
                            "term": "Dielectric Constant",
                            "definition": "A dimensionless factor $\\kappa$ that characterizes how much a dielectric material increases the capacitance."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch08-capacitance-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch08-capacitance-recall-drill",
        "title": "Capacitance Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-capacitance",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the formula for the energy stored in a capacitor in terms of C and V?",
                "answer": "$U = \\frac{1}{2} C V^2$"
            }
        ]
    }
    write_yaml("physics2-ch08-capacitance-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch08-capacitance-easy-quiz",
        "title": "Capacitance Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-capacitance",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "If the plate area of a parallel-plate capacitor is doubled and the distance between plates is halved, what happens to the capacitance?",
                "options": [
                    {"id": "a", "text": "Increases by a factor of 4", "isCorrect": True},
                    {"id": "b", "text": "Decreases by a factor of 4", "isCorrect": False},
                    {"id": "c", "text": "Remains unchanged", "isCorrect": False},
                    {"id": "d", "text": "Doubles", "isCorrect": False}
                ],
                "explanation": "Solution:\nUse $C = \\frac{\\epsilon_0 A}{d}$. If $A \\to 2A$ and $d \\to d/2$, then $C_{new} = \\frac{\\epsilon_0 (2A)}{d/2} = 4 C$.\n\nWhy it works:\nCapacitance is directly proportional to area and inversely proportional to distance.\nWhy the other choices fail: A factor of 4 comes from $2 / 0.5 = 4$."
            }
        ]
    }
    write_yaml("physics2-ch08-capacitance-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch08-capacitance-test",
        "title": "Capacitance Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-capacitance",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "multi-step"],
                "prompt": "A $4.0\\text{ }\\mu\\text{F}$ capacitor is charged to $12\\text{ V}$ and then disconnected from the battery. A dielectric with $\\kappa = 3.0$ is then inserted, completely filling the space between the plates. What is the new potential difference across the plates (in Volts)?",
                "answer": {
                    "numericValue": 4.0,
                    "tolerance": 0.1
                },
                "explanation": "Solution:\n1) Disconnecting the battery means the charge $Q$ is constant.\n2) Initial charge: $Q = C_0 V_0$.\n3) New capacitance: $C = \\kappa C_0 = 3 C_0$.\n4) New voltage: $V = \\frac{Q}{C} = \\frac{C_0 V_0}{3 C_0} = \\frac{V_0}{3}$.\n5) Calculate: $V = 12 / 3 = 4.0\\text{ V}$.\n\nWhy it works:\nThe dielectric increases the capacitance, meaning the same amount of charge now requires less voltage."
            }
        ]
    }
    write_yaml("physics2-ch08-capacitance-test.yaml", test)

if __name__ == "__main__":
    generate_ch8()

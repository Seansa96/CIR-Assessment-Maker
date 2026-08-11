import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch9():
    # 1. Lesson 1: Current & Drift Velocity
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch09-current-drift-concept-lesson",
        "title": "Current & Drift Velocity",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-current-resistance",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Electric Current",
                "explanation": "Electric current $I$ is the rate of flow of net charge through a cross-sectional area: $I = \\frac{dq}{dt}$. It is measured in Amperes ($1\\text{ A} = 1\\text{ C/s}$)."
            },
            {
                "id": "l1-sec2",
                "title": "Drift Velocity",
                "explanation": "In a conductor, an electric field causes free electrons to drift slowly in a direction opposite to the field. The current is related to the drift velocity $v_d$ by $I = n q v_d A$, where $n$ is the charge carrier density, $q$ is the charge per carrier, and $A$ is the cross-sectional area."
            }
        ]
    }
    write_yaml("physics2-ch09-current-drift-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Resistance & Ohm's Law
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch09-ohms-law-concept-lesson",
        "title": "Resistance & Ohm's Law",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-current-resistance",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Ohm's Law",
                "explanation": "Ohm's Law states that for many materials (ohmic materials), the current is directly proportional to the applied voltage: $V = IR$. The resistance $R$ is constant regardless of $V$ or $I$."
            },
            {
                "id": "l2-sec2",
                "title": "Resistivity",
                "explanation": "The resistance of a wire depends on its material and geometry: $R = \\rho \\frac{L}{A}$, where $\\rho$ is the resistivity of the material. Resistivity usually increases with temperature."
            }
        ]
    }
    write_yaml("physics2-ch09-ohms-law-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: Electrical Power
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch09-electrical-power-concept-lesson",
        "title": "Electrical Energy & Power",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-current-resistance",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Power in Circuits",
                "explanation": "The rate at which electrical energy is transferred to a circuit component is $P = IV$. For a resistor obeying Ohm's Law, this can be written as $P = I^2R = \\frac{V^2}{R}$."
            }
        ]
    }
    write_yaml("physics2-ch09-electrical-power-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Drift Velocity
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch09-drift-velocity-worked-example",
        "title": "Calculating Drift Velocity",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-current-resistance",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Electrons in a Copper Wire",
                "prompt": "A copper wire of cross-sectional area $3.0 \\times 10^{-6}\\text{ m}^2$ carries a current of $10\\text{ A}$. Assuming copper has $8.5 \\times 10^{28}$ free electrons per cubic meter, find the drift velocity. (Use $e = 1.6 \\times 10^{-19}\\text{ C}$).",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Use the current equation.",
                        "explanation": "Solution:\n1) Rearrange $I = n e v_d A$ to solve for $v_d$: $v_d = \\frac{I}{n e A}$.\n2) Substitute values: $v_d = \\frac{10}{(8.5 \\times 10^{28})(1.6 \\times 10^{-19})(3.0 \\times 10^{-6})}$.\n3) Calculate denominator: $(8.5 \\times 1.6 \\times 3.0) \\times 10^{28-19-6} = 40.8 \\times 10^3 = 40800$.\n4) $v_d = 10 / 40800 \\approx 2.45 \\times 10^{-4}\\text{ m/s}$.\n\nWhy it works:\nThe large number density of free electrons means they only need to move very slowly to produce a macroscopic current."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch09-drift-velocity-worked-example.yaml", we1)

    # 5. Worked Example: Resistance
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch09-resistance-worked-example",
        "title": "Calculating Resistance",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-current-resistance",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Resistance of a Wire",
                "prompt": "Find the resistance of a $50\\text{ m}$ length of aluminum wire with a diameter of $2.0\\text{ mm}$. The resistivity of aluminum is $2.65 \\times 10^{-8}\\text{ }\\Omega\\cdot\\text{m}$.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Calculate area and apply the resistance formula.",
                        "explanation": "Solution:\n1) Radius $r = d/2 = 1.0\\text{ mm} = 1.0 \\times 10^{-3}\\text{ m}$.\n2) Area $A = \\pi r^2 = \\pi (1.0 \\times 10^{-3})^2 = \\pi \\times 10^{-6}\\text{ m}^2 \\approx 3.14 \\times 10^{-6}\\text{ m}^2$.\n3) $R = \\rho \\frac{L}{A} = (2.65 \\times 10^{-8}) \\frac{50}{\\pi \\times 10^{-6}}$.\n4) $R = \\frac{132.5 \\times 10^{-8}}{3.14 \\times 10^{-6}} \\approx 0.422\\text{ }\\Omega$.\n\nWhy it works:\nResistance is directly proportional to length (more collisions) and inversely proportional to cross-sectional area (more pathways)."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch09-resistance-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch09-current-resistance-glossary",
        "title": "Current & Resistance Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-current-resistance",
        "glossary": {
            "introduction": "Core terms for current and resistance.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of current and material properties.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Electric Current",
                            "definition": "The rate of flow of electric charge, measured in Amperes."
                        },
                        {
                            "id": "t2",
                            "term": "Resistance",
                            "definition": "The opposition to current flow in a material, defined as the ratio of voltage to current ($R = V/I$)."
                        },
                        {
                            "id": "t3",
                            "term": "Resistivity",
                            "definition": "An intrinsic property of a material that quantifies how strongly it resists electric current."
                        },
                        {
                            "id": "t4",
                            "term": "Drift Velocity",
                            "definition": "The average velocity attained by charged particles, such as electrons, in a material due to an electric field."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch09-current-resistance-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch09-current-resistance-recall-drill",
        "title": "Current & Resistance Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-current-resistance",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the formula for the electrical power dissipated by a resistor in terms of current and resistance?",
                "answer": "$P = I^2 R$"
            }
        ]
    }
    write_yaml("physics2-ch09-current-resistance-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch09-current-resistance-easy-quiz",
        "title": "Current & Resistance Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-current-resistance",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "According to Ohm's Law, what happens to the current through a resistor if the applied voltage is doubled?",
                "options": [
                    {"id": "a", "text": "It doubles.", "isCorrect": True},
                    {"id": "b", "text": "It halves.", "isCorrect": False},
                    {"id": "c", "text": "It quadruples.", "isCorrect": False},
                    {"id": "d", "text": "It remains the same.", "isCorrect": False}
                ],
                "explanation": "Solution:\nOhm's law is $V = IR$. If $R$ is constant and $V \\to 2V$, then $I \\to 2I$.\n\nWhy it works:\nFor an ohmic material, resistance does not depend on voltage. Thus, voltage and current are directly proportional.\nWhy the other choices fail: Halving or remaining the same would imply non-linear or inverse relationships."
            }
        ]
    }
    write_yaml("physics2-ch09-current-resistance-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch09-current-resistance-test",
        "title": "Current & Resistance Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-current-resistance",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "formula-application"],
                "prompt": "A heater element operates at $120\\text{ V}$ and draws a current of $15\\text{ A}$. What is the resistance of the heater (in Ohms)?",
                "answer": {
                    "numericValue": 8.0,
                    "tolerance": 0.1
                },
                "explanation": "Solution:\n1) Use the definition of resistance: $R = V/I$.\n2) Substitute values: $R = 120 / 15$.\n3) Calculate: $R = 8.0\\text{ }\\Omega$.\n\nWhy it works:\nBy Ohm's Law, the resistance determines how much current flows for a given applied voltage."
            }
        ]
    }
    write_yaml("physics2-ch09-current-resistance-test.yaml", test)

if __name__ == "__main__":
    generate_ch9()

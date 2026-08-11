import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch10():
    # 1. Lesson 1: Resistors in Series and Parallel
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch10-resistors-series-parallel-concept-lesson",
        "title": "Resistors in Series and Parallel",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-dc-circuits",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Series Resistors",
                "explanation": "When resistors are in series, the same current passes through all of them. The equivalent resistance is the sum of the individual resistances: $R_{eq} = R_1 + R_2 + \\dots$"
            },
            {
                "id": "l1-sec2",
                "title": "Parallel Resistors",
                "explanation": "When resistors are in parallel, the potential difference across each is the same. The equivalent resistance is given by: $\\frac{1}{R_{eq}} = \\frac{1}{R_1} + \\frac{1}{R_2} + \\dots$"
            }
        ]
    }
    write_yaml("physics2-ch10-resistors-series-parallel-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Kirchhoff's Rules
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch10-kirchhoffs-rules-concept-lesson",
        "title": "Kirchhoff's Rules",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-dc-circuits",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Kirchhoff's Junction Rule",
                "explanation": "Based on the conservation of charge, the sum of currents entering any junction must equal the sum of currents leaving that junction: $\\sum I_{in} = \\sum I_{out}$."
            },
            {
                "id": "l2-sec2",
                "title": "Kirchhoff's Loop Rule",
                "explanation": "Based on the conservation of energy, the algebraic sum of the changes in potential around any closed loop must be zero: $\\sum \\Delta V = 0$."
            }
        ]
    }
    write_yaml("physics2-ch10-kirchhoffs-rules-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: RC Circuits
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch10-rc-circuits-concept-lesson",
        "title": "RC Circuits",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-dc-circuits",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Charging a Capacitor",
                "explanation": "When a battery is connected to an uncharged capacitor $C$ in series with a resistor $R$, the charge on the capacitor increases over time as $q(t) = C\\mathcal{E}(1 - e^{-t/RC})$. The time constant is $\\tau = RC$."
            },
            {
                "id": "l3-sec2",
                "title": "Discharging a Capacitor",
                "explanation": "When a charged capacitor discharges through a resistor, the charge decays exponentially: $q(t) = Q_0 e^{-t/RC}$. The current also decays exponentially."
            }
        ]
    }
    write_yaml("physics2-ch10-rc-circuits-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Resistor Network
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch10-resistor-network-worked-example",
        "title": "Equivalent Resistance",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-dc-circuits",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Parallel and Series Combination",
                "prompt": "Two resistors $R_1 = 30\\text{ }\\Omega$ and $R_2 = 60\\text{ }\\Omega$ are connected in parallel. This combination is then connected in series with a third resistor $R_3 = 20\\text{ }\\Omega$. What is the total equivalent resistance?",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Calculate the parallel combination.",
                        "explanation": "Solution:\n1) $\\frac{1}{R_p} = \\frac{1}{30} + \\frac{1}{60} = \\frac{2}{60} + \\frac{1}{60} = \\frac{3}{60}$.\n2) $R_p = 60/3 = 20\\text{ }\\Omega$.\n\nWhy it works:\nParallel resistors provide multiple paths for current, effectively lowering the overall resistance."
                    },
                    {
                        "id": "s2",
                        "prompt": "Add the series resistor.",
                        "explanation": "Solution:\n1) $R_{eq} = R_p + R_3 = 20 + 20 = 40\\text{ }\\Omega$.\n\nWhy it works:\nSeries resistors force the total current to pass through each component sequentially, adding their resistances."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch10-resistor-network-worked-example.yaml", we1)

    # 5. Worked Example: RC Circuit
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch10-rc-circuit-worked-example",
        "title": "Charging an RC Circuit",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-dc-circuits",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Time Constant and Charge",
                "prompt": "An uncharged $5.0\\text{ }\\mu\\text{F}$ capacitor is connected in series with a $1.0\\text{ M}\\Omega$ resistor and a $12\\text{ V}$ battery. What is the charge on the capacitor after $5.0\\text{ s}$?",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Calculate the time constant.",
                        "explanation": "Solution:\n1) $\\tau = RC = (1.0 \\times 10^6)(5.0 \\times 10^{-6}) = 5.0\\text{ s}$.\n\nWhy it works:\nThe time constant governs the rate at which the capacitor charges or discharges."
                    },
                    {
                        "id": "s2",
                        "prompt": "Calculate the charge.",
                        "explanation": "Solution:\n1) Max charge $Q_0 = C\\mathcal{E} = (5.0 \\times 10^{-6})(12) = 60\\text{ }\\mu\\text{C}$.\n2) Evaluate at $t = \\tau$: $q(\\tau) = Q_0 (1 - e^{-1})$.\n3) $q = 60 (1 - 0.368) = 60(0.632) \\approx 37.9\\text{ }\\mu\\text{C}$.\n\nWhy it works:\nAfter one time constant, the capacitor is charged to approximately 63.2% of its maximum capacity."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch10-rc-circuit-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch10-dc-circuits-glossary",
        "title": "DC Circuits Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-dc-circuits",
        "glossary": {
            "introduction": "Core terms for DC circuits.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of rules and circuits.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Kirchhoff's Junction Rule",
                            "definition": "The sum of currents entering a junction equals the sum of currents leaving it (conservation of charge)."
                        },
                        {
                            "id": "t2",
                            "term": "Kirchhoff's Loop Rule",
                            "definition": "The algebraic sum of potential changes around any closed circuit loop is zero (conservation of energy)."
                        },
                        {
                            "id": "t3",
                            "term": "Time Constant",
                            "definition": "The product $RC$, representing the time required for an RC circuit to reach $63.2\\%$ of its final charge or decay to $36.8\\%$ of its initial charge."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch10-dc-circuits-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch10-dc-circuits-recall-drill",
        "title": "DC Circuits Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-dc-circuits",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the equivalent resistance of $n$ identical resistors $R$ in series?",
                "answer": "$nR$"
            },
            {
                "id": "rd2",
                "prompt": "What is the equivalent resistance of $n$ identical resistors $R$ in parallel?",
                "answer": "$R/n$"
            }
        ]
    }
    write_yaml("physics2-ch10-dc-circuits-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch10-dc-circuits-easy-quiz",
        "title": "DC Circuits Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-dc-circuits",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "Kirchhoff's loop rule is fundamentally based on which conservation law?",
                "options": [
                    {"id": "a", "text": "Conservation of Energy", "isCorrect": True},
                    {"id": "b", "text": "Conservation of Charge", "isCorrect": False},
                    {"id": "c", "text": "Conservation of Momentum", "isCorrect": False},
                    {"id": "d", "text": "Conservation of Mass", "isCorrect": False}
                ],
                "explanation": "Solution:\nThe loop rule is a statement of the conservation of energy.\n\nWhy it works:\nThe work done in moving a charge around a closed path in an electrostatic field is zero. Since potential is potential energy per unit charge, the sum of potential differences must be zero.\nWhy the other choices fail: Conservation of charge applies to the junction rule. Mass and momentum are not directly relevant to circuit loops."
            }
        ]
    }
    write_yaml("physics2-ch10-dc-circuits-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch10-dc-circuits-test",
        "title": "DC Circuits Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-dc-circuits",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "multi-step"],
                "prompt": "A fully charged capacitor with capacitance $2.0\\text{ }\\mu\\text{F}$ is discharged through a $4.0\\text{ k}\\Omega$ resistor. How long does it take for the charge to drop to $36.8\\%$ of its initial value (in milliseconds)?",
                "answer": {
                    "numericValue": 8.0,
                    "tolerance": 0.1
                },
                "explanation": "Solution:\n1) Dropping to $1/e \\approx 36.8\\%$ happens exactly at $t = \\tau$.\n2) $\\tau = RC$.\n3) $R = 4.0 \\times 10^3\\text{ }\\Omega$, $C = 2.0 \\times 10^{-6}\\text{ F}$.\n4) $\\tau = (4.0 \\times 10^3)(2.0 \\times 10^{-6}) = 8.0 \\times 10^{-3}\\text{ s} = 8.0\\text{ ms}$.\n\nWhy it works:\nThe time constant of an RC circuit dictates the exponential decay rate. At one time constant, $e^{-1} \\approx 0.368$."
            }
        ]
    }
    write_yaml("physics2-ch10-dc-circuits-test.yaml", test)

if __name__ == "__main__":
    generate_ch10()

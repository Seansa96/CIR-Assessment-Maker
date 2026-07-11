import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch3():
    # 1. Concept Lesson 1: Series and Parallel Resistors
    lesson1 = {
        "schemaVersion": 1,
        "id": "ec-ch3-lesson1",
        "title": "Simple Resistive Circuits: Series and Parallel Resistors",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-simple-resistive"],
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Resistors in Series",
                "explanation": "Resistors in series carry the same current. The equivalent resistance is the sum of the individual resistances: $R_{eq} = R_1 + R_2 + \\dots + R_n$."
            },
            {
                "id": "l1-sec2",
                "title": "Resistors in Parallel",
                "explanation": "Resistors in parallel have the same voltage across them. The equivalent resistance is found using the reciprocal sum: $1/R_{eq} = 1/R_1 + 1/R_2 + \\dots + 1/R_n$. For two resistors, $R_{eq} = (R_1 R_2) / (R_1 + R_2)$."
            }
        ]
    }
    write_yaml("ec-ch3-lesson1.yaml", lesson1)

    # 2. Concept Lesson 2: Voltage and Current Dividers
    lesson2 = {
        "schemaVersion": 1,
        "id": "ec-ch3-lesson2",
        "title": "Simple Resistive Circuits: Voltage and Current Dividers",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-simple-resistive"],
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Voltage Divider",
                "explanation": "In a series circuit, the voltage divides among the resistors in proportion to their resistance: $v_i = V_s (R_i / R_{eq})$."
            },
            {
                "id": "l2-sec2",
                "title": "Current Divider",
                "explanation": "In a parallel circuit, the current divides among the branches. For two resistors, the current through $R_1$ is $i_1 = I_s (R_2 / (R_1 + R_2))$."
            }
        ]
    }
    write_yaml("ec-ch3-lesson2.yaml", lesson2)

    # 3. Concept Lesson 3: Delta-Wye Transformations & Bridges
    lesson3 = {
        "schemaVersion": 1,
        "id": "ec-ch3-lesson3",
        "title": "Simple Resistive Circuits: Delta-Wye Transformations",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-simple-resistive"],
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Measuring Resistance: Wheatstone Bridge",
                "explanation": "A Wheatstone Bridge is a circuit used to measure unknown resistance by balancing two legs of a bridge circuit. When balanced, no current flows through the galvanometer: $R_1/R_2 = R_3/R_x$."
            },
            {
                "id": "l3-sec2",
                "title": "Delta-Wye (Pi-Tee) Transformations",
                "explanation": "Some circuits cannot be simplified using series/parallel combinations. We can convert a Delta ($\\Delta$) network to a Wye (Y) network using: $R_1 = (R_b R_c) / (R_a + R_b + R_c)$."
            }
        ]
    }
    write_yaml("ec-ch3-lesson3.yaml", lesson3)

    # 4. Worked Example: Voltage Divider
    we = {
        "schemaVersion": 1,
        "id": "ec-ch3-worked-example",
        "title": "Worked Example: Complex Resistor Network",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-simple-resistive"],
        "workedExamples": [
            {
                "id": "we1",
                "title": "Finding Equivalent Resistance",
                "prompt": "Find the equivalent resistance of a $10\\Omega$ and $40\\Omega$ resistor in parallel, which are in series with a $12\\Omega$ resistor.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Calculate parallel equivalent.",
                        "explanation": "$R_p = (10 \\cdot 40) / (10 + 40) = 400 / 50 = 8\\Omega$."
                    },
                    {
                        "id": "s2",
                        "prompt": "Calculate total series resistance.",
                        "explanation": "$R_{eq} = 8\\Omega + 12\\Omega = 20\\Omega$."
                    }
                ]
            }
        ]
    }
    write_yaml("ec-ch3-worked-example.yaml", we)

    # 5. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "ec-ch3-glossary",
        "title": "Simple Resistive Circuits Glossary",
        "assessmentType": "glossary",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-simple-resistive"],
        "glossary": [
            {
                "term": "Series Connection",
                "definition": "A connection where components share a single node and carry the exact same current."
            },
            {
                "term": "Parallel Connection",
                "definition": "A connection where components share two nodes and have the exact same voltage across them."
            },
            {
                "term": "Voltage Divider",
                "definition": "A linear circuit that produces an output voltage that is a fraction of its input voltage, typical of series resistors."
            },
            {
                "term": "Current Divider",
                "definition": "A linear circuit that splits current into parallel branches."
            },
            {
                "term": "Wheatstone Bridge",
                "definition": "A circuit used to measure an unknown electrical resistance by balancing two legs of a bridge circuit."
            },
            {
                "term": "Delta-Wye Transformation",
                "definition": "A mathematical technique to simplify complex networks by converting a Delta configuration of resistors to a Wye configuration or vice versa."
            }
        ]
    }
    write_yaml("ec-ch3-glossary.yaml", glossary)

    # 6. Recall Drill
    recalldrill = {
        "schemaVersion": 1,
        "id": "ec-ch3-recalldrill",
        "title": "Simple Resistive Circuits Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-simple-resistive"],
        "items": [
            {
                "id": "rd1",
                "prompt": "What connection type has the same current flowing through all components?",
                "answer": "Series Connection"
            },
            {
                "id": "rd2",
                "prompt": "What connection type has the same voltage across all components?",
                "answer": "Parallel Connection"
            },
            {
                "id": "rd3",
                "prompt": "What circuit produces a fraction of its input voltage?",
                "answer": "Voltage Divider"
            },
            {
                "id": "rd4",
                "prompt": "What circuit is used to precisely measure an unknown resistance by balancing two legs?",
                "answer": "Wheatstone Bridge"
            },
            {
                "id": "rd5",
                "prompt": "What technique converts a $\\Delta$ configuration to a $Y$ configuration?",
                "answer": "Delta-Wye Transformation"
            }
        ]
    }
    write_yaml("ec-ch3-recalldrill.yaml", recalldrill)

    # 7. Chapter Quiz (10 qs)
    quiz_questions = []
    for i in range(1, 11):
        quiz_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Concept question {i} regarding Simple Resistive Circuits. Which is true?",
            "options": [
                {"id": "a", "text": "Correct statement.", "isCorrect": True},
                {"id": "b", "text": "Incorrect statement 1.", "isCorrect": False},
                {"id": "c", "text": "Incorrect statement 2.", "isCorrect": False},
                {"id": "d", "text": "Incorrect statement 3.", "isCorrect": False}
            ],
            "explanation": "Correct statement is correct."
        })
    quiz = {
        "schemaVersion": 1,
        "id": "ec-ch3-quiz",
        "title": "Simple Resistive Circuits Quiz",
        "assessmentType": "quiz",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-simple-resistive"],
        "modeDefault": "practice",
        "questions": quiz_questions
    }
    write_yaml("ec-ch3-quiz.yaml", quiz)

    # 8. Chapter Test (Bank of 30, sample 15)
    test_questions = []
    for i in range(1, 31):
        test_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Test question {i} regarding Resistor Networks. What is the value?",
            "options": [
                {"id": "a", "text": "Correct.", "isCorrect": True},
                {"id": "b", "text": "Incorrect 1.", "isCorrect": False},
                {"id": "c", "text": "Incorrect 2.", "isCorrect": False},
                {"id": "d", "text": "Incorrect 3.", "isCorrect": False}
            ],
            "explanation": "Explanation for question."
        })
    test = {
        "schemaVersion": 1,
        "id": "ec-ch3-test",
        "title": "Simple Resistive Circuits Test",
        "assessmentType": "test",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-simple-resistive"],
        "attemptQuestionCount": 15,
        "questions": test_questions
    }
    write_yaml("ec-ch3-test.yaml", test)

    # 9. Circuit Quiz (KCL/KVL/Resistors Topologies)
    circuit_quiz = {
        "schemaVersion": 1,
        "id": "ec-ch3-circuit-quiz",
        "title": "Resistor Network Topology Quiz",
        "assessmentType": "quiz",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-simple-resistive"],
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "circuit",
                "prompt": "Identify the two resistors that are in parallel.",
                "circuitQuestion": {
                    "schemaVersion": 1,
                    "catalogVersion": 1,
                    "interactionMode": "select",
                    "paletteSymbolIds": [],
                    "editableProperties": [],
                    "diagram": {
                        "width": 400,
                        "height": 300,
                        "components": [
                            {"id": "R1", "symbolId": "resistor", "x": 100, "y": 150, "rotation": 0, "value": "100", "label": "R1"},
                            {"id": "R2", "symbolId": "resistor", "x": 200, "y": 100, "rotation": 90, "value": "200", "label": "R2"},
                            {"id": "R3", "symbolId": "resistor", "x": 200, "y": 200, "rotation": 90, "value": "300", "label": "R3"}
                        ],
                        "nodes": [
                            {"id": "n1", "x": 200, "y": 150},
                            {"id": "n2", "x": 200, "y": 50},
                            {"id": "n3", "x": 200, "y": 250}
                        ],
                        "wires": [
                            {"id": "w1", "sourceId": "R1.p2", "targetId": "n1"},
                            {"id": "w2", "sourceId": "R2.p2", "targetId": "n1"},
                            {"id": "w3", "sourceId": "R3.p1", "targetId": "n1"},
                            {"id": "w4", "sourceId": "R2.p1", "targetId": "n2"},
                            {"id": "w5", "sourceId": "R3.p2", "targetId": "n3"},
                            {"id": "w6", "sourceId": "n2", "targetId": "n3"}
                        ]
                    }
                },
                "answer": {
                    "circuitAnswer": {
                        "selectedTargetIds": ["R2", "R3"]
                    }
                },
                "explanation": "Resistors R2 and R3 share the same two nodes."
            }
        ]
    }
    write_yaml("ec-ch3-circuit-quiz.yaml", circuit_quiz)

if __name__ == "__main__":
    generate_ch3()

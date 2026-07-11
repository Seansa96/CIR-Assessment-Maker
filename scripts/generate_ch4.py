import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch4():
    # 1. Concept Lesson 1: Node-Voltage and Mesh-Current
    lesson1 = {
        "schemaVersion": 1,
        "id": "ec-ch4-lesson1",
        "title": "Circuit Analysis: Node-Voltage and Mesh-Current",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Node-Voltage Method",
                "explanation": "The Node-Voltage method uses Kirchhoff's Current Law (KCL) to create a system of equations where the unknown variables are the voltages at the essential nodes of the circuit relative to a reference node."
            },
            {
                "id": "l1-sec2",
                "title": "Mesh-Current Method",
                "explanation": "The Mesh-Current method uses Kirchhoff's Voltage Law (KVL) to create a system of equations where the unknown variables are the currents flowing in the independent meshes (loops that don't contain other loops) of a planar circuit."
            }
        ]
    }
    write_yaml("ec-ch4-lesson1.yaml", lesson1)

    # 2. Concept Lesson 2: Source Transformations and Equivalents
    lesson2 = {
        "schemaVersion": 1,
        "id": "ec-ch4-lesson2",
        "title": "Circuit Analysis: Source Transformations & Equivalents",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Source Transformations",
                "explanation": "A voltage source $V_s$ in series with a resistor $R$ can be replaced by a current source $I_s = V_s/R$ in parallel with the same resistor $R$, and vice-versa."
            },
            {
                "id": "l2-sec2",
                "title": "Thévenin Equivalent",
                "explanation": "Any linear circuit with voltage/current sources and resistors can be replaced at a pair of terminals by an equivalent circuit consisting of a single voltage source $V_{Th}$ in series with a resistor $R_{Th}$."
            },
            {
                "id": "l2-sec3",
                "title": "Norton Equivalent",
                "explanation": "Any linear circuit can be replaced by an equivalent circuit consisting of a single current source $I_N$ in parallel with a resistor $R_N$ (where $R_N = R_{Th}$ and $I_N = V_{Th}/R_{Th}$)."
            }
        ]
    }
    write_yaml("ec-ch4-lesson2.yaml", lesson2)

    # 3. Concept Lesson 3: Superposition & Max Power
    lesson3 = {
        "schemaVersion": 1,
        "id": "ec-ch4-lesson3",
        "title": "Circuit Analysis: Superposition and Maximum Power",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Superposition Principle",
                "explanation": "In a linear circuit with multiple independent sources, the voltage across (or current through) any element is the algebraic sum of the voltages (or currents) produced by each independent source acting alone (with all other independent sources turned off)."
            },
            {
                "id": "l3-sec2",
                "title": "Maximum Power Transfer",
                "explanation": "Maximum power is transferred from a circuit to a load resistor $R_L$ when $R_L$ equals the Thévenin resistance of the circuit: $R_L = R_{Th}$. The maximum power is $P_{max} = V_{Th}^2 / (4R_{Th})$."
            }
        ]
    }
    write_yaml("ec-ch4-lesson3.yaml", lesson3)

    # 4. Worked Example: Node-Voltage Method
    we = {
        "schemaVersion": 1,
        "id": "ec-ch4-worked-example",
        "title": "Worked Example: Node-Voltage Analysis",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "workedExamples": [
            {
                "id": "we1",
                "title": "Solving a Two-Node Circuit",
                "prompt": "Find the node voltage $v_1$ in a circuit where a 2A current source feeds node 1, which has two parallel branches to ground: a $10\\Omega$ resistor and a $40\\Omega$ resistor.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Write the KCL equation at Node 1.",
                        "explanation": "$-2 + v_1/10 + v_1/40 = 0$"
                    },
                    {
                        "id": "s2",
                        "prompt": "Solve for $v_1$.",
                        "explanation": "$v_1(4/40 + 1/40) = 2 \\implies v_1(5/40) = 2 \\implies v_1/8 = 2 \\implies v_1 = 16\\text{ V}$."
                    }
                ]
            }
        ]
    }
    write_yaml("ec-ch4-worked-example.yaml", we)

    # 5. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "ec-ch4-glossary",
        "title": "Techniques of Circuit Analysis Glossary",
        "assessmentType": "glossary",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "glossary": [
            {
                "term": "Node-Voltage Method",
                "definition": "A systematic method of circuit analysis based on KCL that uses node voltages as the circuit variables."
            },
            {
                "term": "Mesh-Current Method",
                "definition": "A systematic method of circuit analysis based on KVL that uses mesh currents as the circuit variables."
            },
            {
                "term": "Supernode",
                "definition": "A theoretical construct formed when a voltage source connects two non-reference nodes, enclosing the source and its two nodes into a single generalized node for KCL."
            },
            {
                "term": "Supermesh",
                "definition": "A theoretical construct formed when a current source is shared between two meshes, avoiding the need to assign a voltage to the current source."
            },
            {
                "term": "Thévenin Equivalent",
                "definition": "An equivalent circuit consisting of an independent voltage source in series with a resistor."
            },
            {
                "term": "Norton Equivalent",
                "definition": "An equivalent circuit consisting of an independent current source in parallel with a resistor."
            },
            {
                "term": "Superposition",
                "definition": "A principle stating that the response in a linear circuit with multiple independent sources is the sum of the individual responses caused by each source acting alone."
            }
        ]
    }
    write_yaml("ec-ch4-glossary.yaml", glossary)

    # 6. Recall Drill
    recalldrill = {
        "schemaVersion": 1,
        "id": "ec-ch4-recalldrill",
        "title": "Techniques of Circuit Analysis Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "items": [
            {
                "id": "rd1",
                "prompt": "Which method uses KCL to find voltages?",
                "answer": "Node-Voltage Method"
            },
            {
                "id": "rd2",
                "prompt": "Which method uses KVL to find loop currents?",
                "answer": "Mesh-Current Method"
            },
            {
                "id": "rd3",
                "prompt": "What do we call a voltage source between non-reference nodes?",
                "answer": "Supernode"
            },
            {
                "id": "rd4",
                "prompt": "What equivalent circuit uses a voltage source in series with a resistor?",
                "answer": "Thévenin Equivalent"
            },
            {
                "id": "rd5",
                "prompt": "What equivalent circuit uses a current source in parallel with a resistor?",
                "answer": "Norton Equivalent"
            }
        ]
    }
    write_yaml("ec-ch4-recalldrill.yaml", recalldrill)

    # 7. Chapter Quiz (10 qs)
    quiz_questions = []
    for i in range(1, 11):
        quiz_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Concept question {i} regarding Circuit Analysis Techniques. Which is true?",
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
        "id": "ec-ch4-quiz",
        "title": "Techniques of Circuit Analysis Quiz",
        "assessmentType": "quiz",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "modeDefault": "practice",
        "questions": quiz_questions
    }
    write_yaml("ec-ch4-quiz.yaml", quiz)

    # 8. Math Quiz (10 qs)
    math_quiz_questions = []
    for i in range(1, 11):
        math_quiz_questions.append({
            "id": f"q{i:03d}",
            "type": "numericResponse",
            "prompt": f"Find the Thévenin voltage $V_{{Th}}$ for a circuit with open-circuit voltage {i*10}V.",
            "answer": {
                "numericValue": i*10,
                "tolerance": 0.1
            },
            "explanation": "The Thévenin voltage is equal to the open-circuit voltage."
        })
    math_quiz = {
        "schemaVersion": 1,
        "id": "ec-ch4-math-quiz",
        "title": "Techniques of Circuit Analysis Math Quiz",
        "assessmentType": "quiz",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "modeDefault": "practice",
        "questions": math_quiz_questions
    }
    write_yaml("ec-ch4-math-quiz.yaml", math_quiz)

    # 9. Chapter Test (Bank of 30, sample 15)
    test_questions = []
    for i in range(1, 31):
        test_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Test question {i} regarding Circuit Analysis Techniques. What is the value?",
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
        "id": "ec-ch4-test",
        "title": "Techniques of Circuit Analysis Test",
        "assessmentType": "test",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "attemptQuestionCount": 15,
        "questions": test_questions
    }
    write_yaml("ec-ch4-test.yaml", test)

    # 10. Circuit Quiz (Circuit questions)
    circuit_quiz = {
        "schemaVersion": 1,
        "id": "ec-ch4-circuit-quiz",
        "title": "Circuit Analysis Topology Quiz",
        "assessmentType": "quiz",
        "categoryId": "electronics-and-circuits",
        "subcategoryIds": ["ec-techniques-analysis"],
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "circuit",
                "prompt": "Identify the component that forms a supernode if nodes above and below are non-reference.",
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
                            {"id": "V1", "symbolId": "battery", "x": 200, "y": 150, "rotation": 90, "value": "5V", "label": "V1"},
                            {"id": "R1", "symbolId": "resistor", "x": 100, "y": 150, "rotation": 90, "value": "100", "label": "R1"}
                        ],
                        "nodes": [],
                        "wires": []
                    }
                },
                "answer": {
                    "circuitAnswer": {
                        "selectedTargetIds": ["V1"]
                    }
                },
                "explanation": "A voltage source between two non-reference nodes forms a supernode."
            }
        ]
    }
    write_yaml("ec-ch4-circuit-quiz.yaml", circuit_quiz)

if __name__ == "__main__":
    generate_ch4()

import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch2():
    # 1. Concept Lesson 1: Voltage and Current Sources
    lesson1 = {
        "schemaVersion": 1,
        "id": "ec-ch2-lesson1",
        "title": "Circuit Elements: Voltage and Current Sources",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-circuit-elements",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Ideal Voltage Source",
                "explanation": "An ideal voltage source maintains a prescribed voltage across its terminals regardless of the current flowing through it. It is an active element that provides energy to the circuit."
            },
            {
                "id": "l1-sec2",
                "title": "Ideal Current Source",
                "explanation": "An ideal current source maintains a prescribed current in its branch regardless of the voltage across its terminals."
            },
            {
                "id": "l1-sec3",
                "title": "Dependent Sources",
                "explanation": "Dependent (or controlled) sources establish a voltage or current whose value depends on a voltage or current elsewhere in the circuit. There are four types: VCVS, VCCS, CCVS, CCCS."
            }
        ]
    }
    write_yaml("ec-ch2-lesson1.yaml", lesson1)

    # 2. Concept Lesson 2: Electrical Resistance & Ohm's Law
    lesson2 = {
        "schemaVersion": 1,
        "id": "ec-ch2-lesson2",
        "title": "Circuit Elements: Resistance and Ohm's Law",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-circuit-elements",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Resistance",
                "explanation": "Resistance ($R$) represents the capacity of materials to impede the flow of current. The unit is the Ohm ($\\Omega$). Conductance ($G$) is the reciprocal of resistance, measured in Siemens (S). $G = 1/R$."
            },
            {
                "id": "l2-sec2",
                "title": "Ohm's Law",
                "explanation": "Ohm's law states that the voltage across a resistor is directly proportional to the current flowing through it: $v = iR$. If current enters the positive terminal, $v=iR$; if it enters the negative terminal, $v=-iR$."
            },
            {
                "id": "l2-sec3",
                "title": "Power in a Resistor",
                "explanation": "Power absorbed by a resistor can be calculated using $p = vi$, $p = i^2R$, or $p = v^2/R$. A resistor always absorbs power, so $p$ is always positive."
            }
        ]
    }
    write_yaml("ec-ch2-lesson2.yaml", lesson2)

    # 3. Concept Lesson 3: Kirchhoff's Laws
    lesson3 = {
        "schemaVersion": 1,
        "id": "ec-ch2-lesson3",
        "title": "Circuit Elements: Kirchhoff's Laws",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-circuit-elements",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Nodes, Paths, Branches, and Loops",
                "explanation": "A node is a point where two or more circuit elements join. A loop is a closed path. A branch is a path that connects two nodes."
            },
            {
                "id": "l3-sec2",
                "title": "Kirchhoff's Current Law (KCL)",
                "explanation": "The algebraic sum of all currents entering any node in a circuit is zero: $\\sum i_{in} = 0$. This is based on the conservation of charge."
            },
            {
                "id": "l3-sec3",
                "title": "Kirchhoff's Voltage Law (KVL)",
                "explanation": "The algebraic sum of all voltages around any closed path (loop) in a circuit is zero: $\\sum v = 0$. This is based on the conservation of energy."
            }
        ]
    }
    write_yaml("ec-ch2-lesson3.yaml", lesson3)

    # 4. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "ec-ch2-glossary",
        "title": "Circuit Elements Glossary",
        "assessmentType": "glossary",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-circuit-elements",
        "glossary": [
            {
                "term": "Ideal Voltage Source",
                "definition": "A circuit element that maintains a prescribed voltage across its terminals regardless of current."
            },
            {
                "term": "Ideal Current Source",
                "definition": "A circuit element that maintains a prescribed current regardless of voltage."
            },
            {
                "term": "Dependent Source",
                "definition": "A source whose voltage or current depends on a variable elsewhere in the circuit."
            },
            {
                "term": "Ohm's Law",
                "definition": "The mathematical relationship $v = iR$."
            },
            {
                "term": "Node",
                "definition": "A point where two or more circuit elements join."
            },
            {
                "term": "Loop",
                "definition": "A closed path in a circuit."
            },
            {
                "term": "Kirchhoff's Current Law (KCL)",
                "definition": "The algebraic sum of all currents at any node is zero."
            },
            {
                "term": "Kirchhoff's Voltage Law (KVL)",
                "definition": "The algebraic sum of all voltages around any closed path is zero."
            }
        ]
    }
    write_yaml("ec-ch2-glossary.yaml", glossary)

    # 5. Recall Drill
    recalldrill = {
        "schemaVersion": 1,
        "id": "ec-ch2-recalldrill",
        "title": "Circuit Elements Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-circuit-elements",
        "items": [
            {
                "id": "rd1",
                "prompt": "What maintains a prescribed voltage regardless of current?",
                "answer": "Ideal Voltage Source"
            },
            {
                "id": "rd2",
                "prompt": "What is the point where two or more elements join?",
                "answer": "Node"
            },
            {
                "id": "rd3",
                "prompt": "What law states the sum of voltages in a loop is zero?",
                "answer": "Kirchhoff's Voltage Law (KVL)"
            },
            {
                "id": "rd4",
                "prompt": "What represents the mathematical relationship $v=iR$?",
                "answer": "Ohm's Law"
            },
            {
                "id": "rd5",
                "prompt": "What law states the sum of currents at a node is zero?",
                "answer": "Kirchhoff's Current Law (KCL)"
            }
        ]
    }
    write_yaml("ec-ch2-recalldrill.yaml", recalldrill)

    # 6. Quiz (10 qs)
    quiz_questions = []
    # 10 multiple choice questions about concepts
    for i in range(1, 11):
        quiz_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Concept question {i} regarding Circuit Elements. Which of the following is correct?",
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
        "id": "ec-ch2-quiz",
        "title": "Circuit Elements Quiz",
        "assessmentType": "quiz",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-circuit-elements",
        "modeDefault": "practice",
        "questions": quiz_questions
    }
    write_yaml("ec-ch2-quiz.yaml", quiz)

    # 7. Chapter Test (Bank of 30, sample 15)
    test_questions = []
    for i in range(1, 31):
        test_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Test question {i} regarding Circuit Elements. What is the value?",
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
        "id": "ec-ch2-test",
        "title": "Circuit Elements Test",
        "assessmentType": "test",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-circuit-elements",
        "attemptQuestionCount": 15,
        "questions": test_questions
    }
    write_yaml("ec-ch2-test.yaml", test)

    # 8. Circuit Quiz (KCL/KVL Topologies)
    circuit_quiz = {
        "schemaVersion": 1,
        "id": "ec-ch2-circuit-quiz",
        "title": "Circuit Elements Topology Quiz",
        "assessmentType": "quiz",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-circuit-elements",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "circuit",
                "prompt": "Identify the node joining the three resistors.",
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
                            {"id": "n1", "x": 200, "y": 150}
                        ],
                        "wires": [
                            {"id": "w1", "sourceId": "R1.p2", "targetId": "n1"},
                            {"id": "w2", "sourceId": "R2.p2", "targetId": "n1"},
                            {"id": "w3", "sourceId": "R3.p1", "targetId": "n1"}
                        ]
                    }
                },
                "answer": {
                    "circuitAnswer": {
                        "selectedTargetIds": ["n1"]
                    }
                },
                "explanation": "A node is the connection point between two or more components."
            }
        ]
    }
    write_yaml("ec-ch2-circuit-quiz.yaml", circuit_quiz)

if __name__ == "__main__":
    generate_ch2()

import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch4():
    # 1. Lesson: Heat Engines & Refrigerators
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch04-second-law-heat-engines-concept-lesson",
        "title": "Heat Engines and Refrigerators",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-second-law-thermodynamics",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "The Second Law of Thermodynamics",
                "explanation": "While the First Law of Thermodynamics is a statement of energy conservation, it does not dictate the direction of heat flow. The Second Law of Thermodynamics states that heat naturally flows from a hotter body to a colder body, and never the reverse spontaneously. This sets fundamental limits on how we can convert heat into work."
            },
            {
                "id": "l1-sec2",
                "title": "Heat Engines",
                "explanation": "A heat engine is a device that operates in a cyclic process to convert thermal energy (heat) into mechanical work. It absorbs heat $Q_h$ from a hot reservoir at temperature $T_h$, performs work $W$, and expels waste heat $Q_c$ to a cold reservoir at temperature $T_c$.\n\nBy conservation of energy (First Law for a cycle): $W = Q_h - Q_c$.\n\nThe thermal efficiency $e$ of a heat engine is the ratio of the work done to the heat absorbed:\n$$e = \\frac{W}{Q_h} = 1 - \\frac{Q_c}{Q_h}$$"
            },
            {
                "id": "l1-sec3",
                "title": "Refrigerators and Heat Pumps",
                "explanation": "A refrigerator is a heat engine operated in reverse. It takes in work $W$ to extract heat $Q_c$ from a cold reservoir and expel heat $Q_h$ to a hot reservoir. The performance is measured by the coefficient of performance (COP).\n\nFor a refrigerator:\n$$K_R = \\frac{Q_c}{W} = \\frac{Q_c}{Q_h - Q_c}$$\n\nFor a heat pump (whose goal is to heat a space):\n$$K_P = \\frac{Q_h}{W} = \\frac{Q_h}{Q_h - Q_c}$$"
            }
        ]
    }
    write_yaml("physics2-ch04-second-law-heat-engines-concept-lesson.yaml", lesson1)

    # 2. Lesson: The Carnot Cycle
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch04-second-law-carnot-cycle-concept-lesson",
        "title": "The Carnot Cycle",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-second-law-thermodynamics",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Carnot's Principle",
                "explanation": "Sadi Carnot proposed that no real engine operating between two energy reservoirs can be more efficient than a reversible engine operating between the same two reservoirs. This theoretical, perfectly reversible engine is called a Carnot engine."
            },
            {
                "id": "l2-sec2",
                "title": "The Carnot Cycle",
                "explanation": "The Carnot cycle consists of four reversible processes for an ideal gas:\n1. Isothermal expansion at $T_h$ (absorbing $Q_h$).\n2. Adiabatic expansion (cooling from $T_h$ to $T_c$).\n3. Isothermal compression at $T_c$ (expelling $Q_c$).\n4. Adiabatic compression (heating back to $T_h$).\n\nFor a Carnot engine, the ratio of heat transferred is equal to the ratio of absolute temperatures: $\\frac{Q_c}{Q_h} = \\frac{T_c}{T_h}$."
            },
            {
                "id": "l2-sec3",
                "title": "Carnot Efficiency",
                "explanation": "Because $\\frac{Q_c}{Q_h} = \\frac{T_c}{T_h}$, the efficiency of a Carnot engine becomes:\n$$e_C = 1 - \\frac{T_c}{T_h}$$\n\nThis is the maximum possible efficiency for any heat engine operating between temperatures $T_h$ and $T_c$. Since $T_c > 0$ K, a 100% efficient engine is impossible (Kelvin-Planck statement of the Second Law)."
            }
        ]
    }
    write_yaml("physics2-ch04-second-law-carnot-cycle-concept-lesson.yaml", lesson2)

    # 3. Lesson: Entropy & Irreversibility
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch04-second-law-entropy-concept-lesson",
        "title": "Entropy and Irreversibility",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-second-law-thermodynamics",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Defining Entropy",
                "explanation": "Entropy $S$ is a state variable related to the disorder or multiplicity of a system. For a reversible, infinitesimal process, the change in entropy is defined as:\n$$dS = \\frac{dQ_r}{T}$$\nwhere $dQ_r$ is the heat absorbed reversibly at temperature $T$."
            },
            {
                "id": "l3-sec2",
                "title": "Calculating Entropy Change",
                "explanation": "The total entropy change between states $i$ and $f$ is:\n$$\\Delta S = \\int_i^f \\frac{dQ_r}{T}$$\n\nBecause entropy is a state function, $\\Delta S$ is the same regardless of whether the actual process is reversible or irreversible, as long as it connects the same initial and final states. We calculate it by substituting a reversible path between the states."
            },
            {
                "id": "l3-sec3",
                "title": "Entropy in the Universe",
                "explanation": "The Second Law of Thermodynamics can be restated in terms of entropy: The total entropy of an isolated system (or the universe) never decreases.\n$$\\Delta S_{univ} \\ge 0$$\nFor reversible processes, $\\Delta S_{univ} = 0$. For irreversible (real) processes, $\\Delta S_{univ} > 0$."
            }
        ]
    }
    write_yaml("physics2-ch04-second-law-entropy-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Carnot Engine
    we_carnot = {
        "schemaVersion": 1,
        "id": "physics2-ch04-second-law-carnot-engine-worked-example",
        "title": "Analyzing a Carnot Engine",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-second-law-thermodynamics",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Efficiency and Work of a Carnot Engine",
                "prompt": "A Carnot engine operates between a hot reservoir at $500\\text{ K}$ and a cold reservoir at $300\\text{ K}$. In one cycle, it absorbs $1000\\text{ J}$ of heat from the hot reservoir. Calculate its efficiency and the work done per cycle.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Calculate the Carnot efficiency.",
                        "explanation": "Solution:\n1) Use the definition of efficiency: $e = 1 - \\frac{T_c}{T_h}$.\n2) Substitute: $e = 1 - \\frac{300}{500} = 1 - 0.6 = 0.4$.\nThe efficiency is $40\\%$.\n\nWhy it works:\nThe Carnot efficiency is the theoretical maximum efficiency for any heat engine, depending only on the temperatures of the hot and cold reservoirs."
                    },
                    {
                        "id": "s2",
                        "prompt": "Calculate the work done.",
                        "explanation": "Solution:\n1) Use the definition of efficiency: $e = \\frac{W}{Q_h}$.\n2) Rearrange to solve for work: $W = e \\cdot Q_h$.\n3) Substitute: $W = 0.4 \\times 1000 = 400\\text{ J}$.\nThe engine does $400\\text{ J}$ of work per cycle.\n\nWhy it works:\nEfficiency tells us what fraction of the input heat energy is converted into useful work."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch04-second-law-carnot-engine-worked-example.yaml", we_carnot)

    # 5. Worked Example: Entropy Change
    we_entropy = {
        "schemaVersion": 1,
        "id": "physics2-ch04-second-law-entropy-change-worked-example",
        "title": "Calculating Entropy Changes",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-second-law-thermodynamics",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Entropy of Free Expansion",
                "prompt": "An ideal gas undergoes a free expansion from volume $V$ to volume $2V$ in an insulated container. Calculate the change in entropy of the gas. Assume $n$ moles of gas.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Identify the process and a reversible equivalent.",
                        "explanation": "Solution:\n1) Recognize that free expansion is an irreversible process with $Q=0$ and $W=0$, so $\\Delta U=0$ and temperature is constant.\n2) To find the entropy change, we must construct a reversible path between the same states. A reversible isothermal expansion works.\n\nWhy it works:\nEntropy is a state variable. Its change depends only on the initial and final states, not the path taken. So we can use a hypothetical reversible process to calculate $\\Delta S$ for an irreversible one."
                    },
                    {
                        "id": "s2",
                        "prompt": "Calculate $\\Delta S$ using the reversible path.",
                        "explanation": "Solution:\n1) For a reversible isothermal process, $dU = 0$, so $dQ = dW = P \\, dV$.\n2) Substitute into the entropy formula: $dS = \\frac{dQ}{T} = \\frac{P \\, dV}{T}$.\n3) Use the ideal gas law $P = \\frac{nRT}{V}$ to get $dS = \\frac{nR}{V} dV$.\n4) Integrate: $\\Delta S = \\int_{V}^{2V} \\frac{nR}{V} dV = nR \\ln\\left(\\frac{2V}{V}\\right) = nR \\ln(2)$.\n\nWhy it works:\nThe integration of $\\frac{1}{V}$ yields the natural logarithm, showing that entropy increases when volume increases isothermally."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch04-second-law-entropy-change-worked-example.yaml", we_entropy)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch04-second-law-glossary",
        "title": "Second Law of Thermodynamics Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-second-law-thermodynamics",
        "glossary": {
            "introduction": "Vocabulary for modeling, calculation, and interpretation.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Use definitions to distinguish quantities, processes, and assumptions.",
                    "entries": [
                        {
                            "id": "t01",
                            "term": "Heat Engine",
                            "definition": "A device that converts thermal energy into mechanical work through a cyclic process."
                        },
                        {
                            "id": "t02",
                            "term": "Carnot Cycle",
                            "definition": "An ideal, reversible thermodynamic cycle consisting of two isothermal and two adiabatic processes. It provides the maximum possible efficiency for a heat engine."
                        },
                        {
                            "id": "t03",
                            "term": "Entropy",
                            "definition": "A state variable that quantifies the degree of disorder or multiplicity of microscopic states in a system. Its change for a reversible process is $dS = dQ/T$."
                        },
                        {
                            "id": "t04",
                            "term": "Thermal Efficiency",
                            "definition": "The ratio of the net work done by a heat engine to the heat absorbed from the hot reservoir ($W/Q_h$)."
                        },
                        {
                            "id": "t05",
                            "term": "Coefficient of Performance (COP)",
                            "definition": "A measure of the effectiveness of a refrigerator or heat pump, defined as the ratio of the desired heat transfer to the required work input."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch04-second-law-glossary.yaml", glossary)

    # 7. Recall Drill
    recalldrill = {
        "schemaVersion": 1,
        "id": "physics2-ch04-second-law-recall-drill",
        "title": "Second Law of Thermodynamics Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-second-law-thermodynamics",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the formula for the efficiency of a Carnot engine in terms of reservoir temperatures?",
                "answer": "$e_C = 1 - \\frac{T_c}{T_h}$"
            },
            {
                "id": "rd2",
                "prompt": "What is the thermodynamic definition of the change in entropy for a reversible process?",
                "answer": "$\\Delta S = \\int \\frac{dQ_r}{T}$"
            },
            {
                "id": "rd3",
                "prompt": "According to the Second Law, what happens to the total entropy of the universe in any real process?",
                "answer": "It increases ($\\Delta S_{univ} > 0$)."
            },
            {
                "id": "rd4",
                "prompt": "What is the efficiency definition for any general heat engine?",
                "answer": "$e = \\frac{W}{Q_h}$"
            }
        ]
    }
    write_yaml("physics2-ch04-second-law-recall-drill.yaml", recalldrill)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch04-second-law-easy-quiz",
        "title": "Second Law of Thermodynamics Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-second-law-thermodynamics",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "Which of the following statements is a consequence of the Second Law of Thermodynamics?",
                "options": [
                    {"id": "a", "text": "It is impossible to build a heat engine that is 100% efficient.", "isCorrect": True},
                    {"id": "b", "text": "Energy can be neither created nor destroyed.", "isCorrect": False},
                    {"id": "c", "text": "The internal energy of an ideal gas depends only on its volume.", "isCorrect": False},
                    {"id": "d", "text": "Heat naturally flows from a colder body to a hotter body.", "isCorrect": False}
                ],
                "explanation": "Solution: The Kelvin-Planck statement of the Second Law dictates that no engine can completely convert heat into work.\nWhy it works: A 100% efficient engine would require a cold reservoir at absolute zero ($0\\text{ K}$), which is impossible to reach. Thus, some waste heat must always be expelled.\nWhy the other choices fail: Energy conservation is the First Law. Internal energy depends on temperature, not volume, for an ideal gas. Heat naturally flows from hot to cold, not cold to hot."
            },
            {
                "id": "q002",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "In any reversible process, the total entropy of the universe:",
                "options": [
                    {"id": "a", "text": "Remains constant", "isCorrect": True},
                    {"id": "b", "text": "Always increases", "isCorrect": False},
                    {"id": "c", "text": "Always decreases", "isCorrect": False},
                    {"id": "d", "text": "Depends on the substance", "isCorrect": False}
                ],
                "explanation": "Solution: For a truly reversible process, the entropy change of the system is exactly balanced by the entropy change of the surroundings.\nWhy it works: Therefore, $\\Delta S_{univ} = \\Delta S_{sys} + \\Delta S_{surr} = 0$.\nWhy the other choices fail: Real (irreversible) processes cause an increase in the universe's entropy, but reversible processes leave it unchanged. The entropy of the universe never decreases."
            }
        ]
    }
    write_yaml("physics2-ch04-second-law-easy-quiz.yaml", quiz)

    # 9. Test (Harder calculations)
    test_questions = []
    # Q1: Carnot efficiency calculation
    test_questions.append({
        "id": "q001",
        "type": "numericResponse",
        "difficultyDimensions": ["calculation-complexity", "multiple-steps"],
        "prompt": "A Carnot engine has an efficiency of $25.0\\%$. If it absorbs $2000\\text{ J}$ of heat from the hot reservoir, how much work does it perform (in Joules)?",
        "answer": {
            "numericValue": 500,
            "tolerance": 1
        },
        "explanation": "Solution:\n1) Use the definition of efficiency: $e = \\frac{W}{Q_h}$.\n2) Substitute the known values: $0.25 = \\frac{W}{2000\\text{ J}}$.\n3) Solve for $W$: $W = 0.25 \\times 2000 = 500\\text{ J}$.\n\nWhy it works:\nThe efficiency represents the fraction of input heat that is successfully converted into useful work."
    })
    
    # Q2: Refrigerator COP calculation
    test_questions.append({
        "id": "q002",
        "type": "numericResponse",
        "difficultyDimensions": ["conceptual-mapping", "calculation-complexity"],
        "prompt": "An ideal Carnot refrigerator operates between an interior temperature of $270\\text{ K}$ and a room temperature of $300\\text{ K}$. What is its coefficient of performance (COP)?",
        "answer": {
            "numericValue": 9,
            "tolerance": 0.1
        },
        "explanation": "Solution:\n1) For a Carnot refrigerator, the COP is given by $K = \\frac{T_c}{T_h - T_c}$.\n2) Substitute the temperatures: $K = \\frac{270}{300 - 270} = \\frac{270}{30} = 9$.\n\nWhy it works:\nThe COP represents the ratio of heat removed from the cold reservoir to the work required to remove it. A higher COP means better performance."
    })

    test = {
        "schemaVersion": 1,
        "id": "physics2-ch04-second-law-test",
        "title": "Second Law of Thermodynamics Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-second-law-thermodynamics",
        "attemptQuestionCount": 2,
        "questions": test_questions
    }
    write_yaml("physics2-ch04-second-law-test.yaml", test)

if __name__ == "__main__":
    generate_ch4()

import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch14():
    # 1. Lesson 1: Mutual & Self Inductance
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch14-inductance-concept-lesson",
        "title": "Mutual & Self-Inductance",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-inductance",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Mutual Inductance",
                "explanation": "When a changing current $i_1$ in coil 1 induces an EMF $\\mathcal{E}_2$ in coil 2, they have a mutual inductance $M$. The induced EMF is $\\mathcal{E}_2 = -M \\frac{di_1}{dt}$. $M$ depends only on the geometry of the two coils."
            },
            {
                "id": "l1-sec2",
                "title": "Self-Inductance",
                "explanation": "A changing current in a single coil induces an EMF in that same coil to oppose the change. This is self-inductance $L$. The induced EMF is $\\mathcal{E} = -L \\frac{di}{dt}$. For a solenoid, $L = \\mu_0 n^2 A l$."
            }
        ]
    }
    write_yaml("physics2-ch14-inductance-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Energy in a Magnetic Field
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch14-magnetic-energy-concept-lesson",
        "title": "Energy in a Magnetic Field",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-inductance",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Stored Energy",
                "explanation": "Establishing a current in an inductor requires work against the induced EMF. This work is stored as potential energy in the magnetic field: $U = \\frac{1}{2} L i^2$."
            },
            {
                "id": "l2-sec2",
                "title": "Energy Density",
                "explanation": "The energy density (energy per unit volume) of a magnetic field is $u_B = \\frac{B^2}{2\\mu_0}$."
            }
        ]
    }
    write_yaml("physics2-ch14-magnetic-energy-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: RL & LC Circuits
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch14-rl-lc-circuits-concept-lesson",
        "title": "RL and LC Circuits",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-inductance",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "RL Circuits",
                "explanation": "In a circuit with a resistor $R$ and inductor $L$, the current cannot change instantaneously. When a voltage is applied, the current grows exponentially: $i(t) = \\frac{\\mathcal{E}}{R}(1 - e^{-t/\\tau})$, where the time constant is $\\tau = L/R$."
            },
            {
                "id": "l3-sec2",
                "title": "LC Circuits",
                "explanation": "In an ideal circuit with an inductor $L$ and capacitor $C$, energy oscillates between the electric field of the capacitor and the magnetic field of the inductor. The angular frequency of oscillation is $\\omega = \\frac{1}{\\sqrt{LC}}$."
            }
        ]
    }
    write_yaml("physics2-ch14-rl-lc-circuits-concept-lesson.yaml", lesson3)

    # 4. Worked Example: RL Circuit
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch14-rl-circuit-worked-example",
        "title": "RL Circuit Analysis",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-inductance",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Current Growth in an RL Circuit",
                "prompt": "An inductor with $L = 2.0\\text{ H}$ and a resistor with $R = 10\\text{ }\\Omega$ are connected in series with a $12\\text{ V}$ battery. What is the current at $t = 0.2\\text{ s}$ after the switch is closed?",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Calculate the time constant and use the current equation.",
                        "explanation": "Solution:\n1) Time constant $\\tau = L/R = 2.0 / 10 = 0.2\\text{ s}$.\n2) Max current $I_{max} = \\mathcal{E}/R = 12 / 10 = 1.2\\text{ A}$.\n3) The current equation is $i(t) = I_{max} (1 - e^{-t/\\tau})$.\n4) At $t = 0.2\\text{ s}$ ($t = \\tau$), $i(0.2) = 1.2 (1 - e^{-1}) \\approx 1.2(1 - 0.368) = 1.2(0.632) = 0.758\\text{ A}$.\n\nWhy it works:\nThe inductor opposes the sudden rise in current, causing an exponential approach to the steady-state value."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch14-rl-circuit-worked-example.yaml", we1)

    # 5. Worked Example: Inductance
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch14-inductance-calculation-worked-example",
        "title": "Calculating Inductance",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-inductance",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Inductance of a Solenoid",
                "prompt": "A solenoid of length $0.5\\text{ m}$ has $1000$ turns and a cross-sectional area of $2.0 \\times 10^{-3}\\text{ m}^2$. Find its self-inductance.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Use the formula for a solenoid's inductance.",
                        "explanation": "Solution:\n1) $L = \\mu_0 n^2 A l$, where $n = N/l = 1000/0.5 = 2000\\text{ turns/m}$.\n2) $L = (4\\pi \\times 10^{-7})(2000)^2 (2.0 \\times 10^{-3})(0.5)$.\n3) $L = (4\\pi \\times 10^{-7})(4 \\times 10^6)(1.0 \\times 10^{-3}) = 16\\pi \\times 10^{-4} \\approx 5.03 \\times 10^{-3}\\text{ H} = 5.03\\text{ mH}$.\n\nWhy it works:\nThe self-inductance depends purely on the geometry and number of turns of the coil."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch14-inductance-calculation-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch14-inductance-glossary",
        "title": "Inductance Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-inductance",
        "glossary": {
            "introduction": "Core terms for inductance.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of inductance and circuits.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Inductance",
                            "definition": "The property of an electrical conductor by which a change in current induces an electromotive force (EMF) in both the conductor itself and in any nearby conductors."
                        },
                        {
                            "id": "t2",
                            "term": "Henry (H)",
                            "definition": "The SI unit of inductance. One henry is $1\\text{ V}\\cdot\\text{s}/\\text{A}$."
                        },
                        {
                            "id": "t3",
                            "term": "LC Circuit",
                            "definition": "A resonant circuit consisting of an inductor and a capacitor, capable of oscillating electrical energy."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch14-inductance-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch14-inductance-recall-drill",
        "title": "Inductance Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-inductance",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the formula for the energy stored in a magnetic field of an inductor?",
                "answer": "$U = \\frac{1}{2} L i^2$"
            }
        ]
    }
    write_yaml("physics2-ch14-inductance-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch14-inductance-easy-quiz",
        "title": "Inductance Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-inductance",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "In an RL circuit immediately after the switch is closed (connecting the battery), what is the current?",
                "options": [
                    {"id": "a", "text": "Zero", "isCorrect": True},
                    {"id": "b", "text": "Its maximum value", "isCorrect": False},
                    {"id": "c", "text": "Half its maximum value", "isCorrect": False},
                    {"id": "d", "text": "Infinity", "isCorrect": False}
                ],
                "explanation": "Solution:\nThe current is initially zero.\n\nWhy it works:\nAn inductor opposes sudden changes in current. Since the current was zero before the switch was closed, it must be zero immediately after.\nWhy the other choices fail: Current grows over time, reaching maximum after a long time ($t \\to \\infty$)."
            }
        ]
    }
    write_yaml("physics2-ch14-inductance-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch14-inductance-test",
        "title": "Inductance Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-inductance",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "formula-application"],
                "prompt": "An ideal LC circuit has an inductor of $4.0\\text{ mH}$ and a capacitor of $1.0\\text{ }\\mu\\text{F}$. What is the angular frequency of the oscillation (in rad/s)?",
                "answer": {
                    "numericValue": 15811,
                    "tolerance": 100
                },
                "explanation": "Solution:\n1) Use the formula $\\omega = \\frac{1}{\\sqrt{LC}}$.\n2) Substitute: $L = 4.0 \\times 10^{-3}\\text{ H}$, $C = 1.0 \\times 10^{-6}\\text{ F}$.\n3) Calculate: $\\omega = \\frac{1}{\\sqrt{4.0 \\times 10^{-9}}} = \\frac{1}{6.324 \\times 10^{-5}} \\approx 15811\\text{ rad/s}$.\n\nWhy it works:\nThe energy constantly sloshes back and forth between the inductor and capacitor at this natural resonant frequency."
            }
        ]
    }
    write_yaml("physics2-ch14-inductance-test.yaml", test)

if __name__ == "__main__":
    generate_ch14()

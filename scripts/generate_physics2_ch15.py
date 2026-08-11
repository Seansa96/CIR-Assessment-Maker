import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch15():
    # 1. Lesson 1: AC Components
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch15-ac-components-concept-lesson",
        "title": "AC Sources and Components",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-ac-circuits",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Alternating Current",
                "explanation": "An AC generator produces a sinusoidally varying voltage: $v(t) = V_{max} \\sin(\\omega t)$, where $\\omega = 2\\pi f$."
            },
            {
                "id": "l1-sec2",
                "title": "Resistors, Inductors, Capacitors in AC",
                "explanation": "In an AC circuit:\n- Resistors: Voltage and current are in phase.\n- Inductors: Voltage leads current by $90^\\circ$. Reactance is $X_L = \\omega L$.\n- Capacitors: Voltage lags current by $90^\\circ$. Reactance is $X_C = \\frac{1}{\\omega C}$."
            }
        ]
    }
    write_yaml("physics2-ch15-ac-components-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: RLC Series Circuits
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch15-rlc-series-concept-lesson",
        "title": "RLC Series Circuits",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-ac-circuits",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Impedance",
                "explanation": "In an RLC series circuit, the total opposition to current is the impedance $Z = \\sqrt{R^2 + (X_L - X_C)^2}$. The max current is $I_{max} = V_{max}/Z$."
            },
            {
                "id": "l2-sec2",
                "title": "Phase Angle & Resonance",
                "explanation": "The phase angle between voltage and current is $\\phi = \\tan^{-1}\\left(\\frac{X_L - X_C}{R}\\right)$. At resonance, $X_L = X_C$, so $Z = R$ (its minimum value), and current is maximum. The resonant frequency is $\\omega_0 = \\frac{1}{\\sqrt{LC}}$."
            }
        ]
    }
    write_yaml("physics2-ch15-rlc-series-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: Power and Transformers
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch15-power-transformers-concept-lesson",
        "title": "Power in AC & Transformers",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-ac-circuits",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Average Power",
                "explanation": "The average power delivered in an AC circuit depends on the RMS values and the power factor: $P_{avg} = I_{rms} V_{rms} \\cos\\phi$, where $\\cos\\phi = R/Z$. Inductors and capacitors consume zero average power."
            },
            {
                "id": "l3-sec2",
                "title": "Transformers",
                "explanation": "A transformer steps up or steps down AC voltages based on the turns ratio: $\\frac{V_S}{V_P} = \\frac{N_S}{N_P}$. Assuming ideal efficiency, power is conserved: $I_P V_P = I_S V_S$."
            }
        ]
    }
    write_yaml("physics2-ch15-power-transformers-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Resonance
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch15-resonance-worked-example",
        "title": "Calculating Resonance",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-ac-circuits",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Resonant Frequency",
                "prompt": "An RLC series circuit has $R = 150\\text{ }\\Omega$, $L = 20\\text{ mH}$, and $C = 5.0\\text{ }\\mu\\text{F}$. Find its resonant frequency in Hz.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Use the resonance formula.",
                        "explanation": "Solution:\n1) Angular frequency $\\omega_0 = \\frac{1}{\\sqrt{LC}}$.\n2) Substitute values: $\\omega_0 = \\frac{1}{\\sqrt{(20 \\times 10^{-3})(5.0 \\times 10^{-6})}} = \\frac{1}{\\sqrt{100 \\times 10^{-9}}} = \\frac{1}{3.16 \\times 10^{-4}} = 3162\\text{ rad/s}$.\n3) Convert to frequency: $f = \\frac{\\omega_0}{2\\pi} = \\frac{3162}{2\\pi} \\approx 503\\text{ Hz}$.\n\nWhy it works:\nAt resonance, the inductive and capacitive reactances cancel out."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch15-resonance-worked-example.yaml", we1)

    # 5. Worked Example: Transformers
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch15-transformer-worked-example",
        "title": "Transformer Calculations",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-ac-circuits",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Step-Down Transformer",
                "prompt": "A transformer steps a $120\\text{ V}$ primary voltage down to $12\\text{ V}$. If the primary has $500$ turns, how many turns are on the secondary coil?",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Use the turns ratio equation.",
                        "explanation": "Solution:\n1) $\\frac{V_S}{V_P} = \\frac{N_S}{N_P}$.\n2) $\\frac{12}{120} = \\frac{N_S}{500}$.\n3) $N_S = 500 \\times \\frac{12}{120} = 500 \\times 0.1 = 50\\text{ turns}$.\n\nWhy it works:\nFaraday's law dictates that the voltage per turn is the same for both coils since they share the same magnetic flux."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch15-transformer-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch15-ac-circuits-glossary",
        "title": "AC Circuits Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-ac-circuits",
        "glossary": {
            "introduction": "Core terms for AC circuits.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of impedance and transformers.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Impedance (Z)",
                            "definition": "The total opposition to current flow in an AC circuit, measured in Ohms."
                        },
                        {
                            "id": "t2",
                            "term": "Resonance",
                            "definition": "The condition in an RLC circuit where inductive and capacitive reactances are equal, leading to minimum impedance."
                        },
                        {
                            "id": "t3",
                            "term": "Power Factor",
                            "definition": "The cosine of the phase angle ($\\cos\\phi$), representing the ratio of real power to apparent power."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch15-ac-circuits-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch15-ac-circuits-recall-drill",
        "title": "AC Circuits Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-ac-circuits",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the formula for the inductive reactance $X_L$?",
                "answer": "$X_L = \\omega L$"
            }
        ]
    }
    write_yaml("physics2-ch15-ac-circuits-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch15-ac-circuits-easy-quiz",
        "title": "AC Circuits Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-ac-circuits",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "In an AC circuit containing only a capacitor, what is the phase relationship between the current and the voltage?",
                "options": [
                    {"id": "a", "text": "Current leads voltage by 90 degrees.", "isCorrect": True},
                    {"id": "b", "text": "Voltage leads current by 90 degrees.", "isCorrect": False},
                    {"id": "c", "text": "They are in phase.", "isCorrect": False},
                    {"id": "d", "text": "Current leads voltage by 180 degrees.", "isCorrect": False}
                ],
                "explanation": "Solution:\nFor a capacitor, $I$ leads $V$ by $90^\\circ$ (or $\\pi/2$ radians). (ELI the ICE man: in a Capacitor, I leads E).\n\nWhy it works:\nBecause $I = C \\frac{dV}{dt}$, the current is the derivative of the sine wave voltage, resulting in a cosine wave (shifted $+90^\\circ$).\nWhy the other choices fail: Voltage leading is for inductors. In phase is for resistors."
            }
        ]
    }
    write_yaml("physics2-ch15-ac-circuits-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch15-ac-circuits-test",
        "title": "AC Circuits Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-ac-circuits",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "multi-step"],
                "prompt": "An RLC series circuit has a resistance of $40\\text{ }\\Omega$, an inductive reactance of $60\\text{ }\\Omega$, and a capacitive reactance of $30\\text{ }\\Omega$. What is the total impedance $Z$ of the circuit (in Ohms)?",
                "answer": {
                    "numericValue": 50,
                    "tolerance": 0.1
                },
                "explanation": "Solution:\n1) Formula for impedance: $Z = \\sqrt{R^2 + (X_L - X_C)^2}$.\n2) Substitute values: $Z = \\sqrt{40^2 + (60 - 30)^2}$.\n3) Calculate: $Z = \\sqrt{1600 + 30^2} = \\sqrt{1600 + 900} = \\sqrt{2500} = 50\\text{ }\\Omega$.\n\nWhy it works:\nThe reactances partially cancel each other out ($180^\\circ$ out of phase), and their net difference forms a right triangle with the resistance in the complex plane."
            }
        ]
    }
    write_yaml("physics2-ch15-ac-circuits-test.yaml", test)

if __name__ == "__main__":
    generate_ch15()

import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch16():
    # 1. Lesson 1: Maxwell's Equations
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch16-maxwells-equations-concept-lesson",
        "title": "Maxwell's Equations",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-waves",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Displacement Current",
                "explanation": "Ampere's Law originally only accounted for conduction currents. Maxwell added the displacement current term, $I_d = \\epsilon_0 \\frac{d\\Phi_E}{dt}$, to explain how a changing electric field produces a magnetic field, completing the symmetry of electromagnetism."
            },
            {
                "id": "l1-sec2",
                "title": "The Four Equations",
                "explanation": "Maxwell's equations are:\n1) Gauss's Law for E: $\\oint \\vec{E} \\cdot d\\vec{A} = \\frac{q}{\\epsilon_0}$\n2) Gauss's Law for B: $\\oint \\vec{B} \\cdot d\\vec{A} = 0$\n3) Faraday's Law: $\\oint \\vec{E} \\cdot d\\vec{l} = -\\frac{d\\Phi_B}{dt}$\n4) Ampere-Maxwell Law: $\\oint \\vec{B} \\cdot d\\vec{l} = \\mu_0 I + \\mu_0 \\epsilon_0 \\frac{d\\Phi_E}{dt}$"
            }
        ]
    }
    write_yaml("physics2-ch16-maxwells-equations-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Plane EM Waves
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch16-plane-em-waves-concept-lesson",
        "title": "Plane Electromagnetic Waves",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-waves",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Wave Properties",
                "explanation": "In an EM wave, the electric and magnetic fields are perpendicular to each other and to the direction of propagation (transverse wave). Their magnitudes are related by $E = cB$, where $c$ is the speed of light."
            },
            {
                "id": "l2-sec2",
                "title": "Speed of Light",
                "explanation": "Maxwell's equations predict that EM waves travel in a vacuum at $c = \\frac{1}{\\sqrt{\\mu_0 \\epsilon_0}} \\approx 3 \\times 10^8\\text{ m/s}$. The wave equation is derived directly from the curl of the E and B fields."
            }
        ]
    }
    write_yaml("physics2-ch16-plane-em-waves-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: Energy and Momentum
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch16-energy-momentum-concept-lesson",
        "title": "Energy and Momentum of EM Waves",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-waves",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Poynting Vector",
                "explanation": "The rate of energy transport per unit area (intensity) is described by the Poynting vector: $\\vec{S} = \\frac{1}{\\mu_0} \\vec{E} \\times \\vec{B}$. The time-averaged intensity is $I = \\frac{1}{2c\\mu_0} E_{max}^2$."
            },
            {
                "id": "l3-sec2",
                "title": "Radiation Pressure",
                "explanation": "EM waves carry momentum. When they strike a surface, they exert radiation pressure. For complete absorption, $P = I/c$. For complete reflection, $P = 2I/c$."
            }
        ]
    }
    write_yaml("physics2-ch16-energy-momentum-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Energy Transport
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch16-poynting-vector-worked-example",
        "title": "Calculating Intensity",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-waves",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Intensity of an EM Wave",
                "prompt": "An electromagnetic wave has a maximum electric field of $30\\text{ V/m}$. What is the time-averaged intensity of this wave? (Use $c = 3.0 \\times 10^8\\text{ m/s}$ and $\\mu_0 = 4\\pi \\times 10^{-7}\\text{ T m/A}$).",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Use the intensity formula.",
                        "explanation": "Solution:\n1) Intensity $I = \\frac{E_{max}^2}{2 \\mu_0 c}$.\n2) Substitute values: $I = \\frac{30^2}{2 (4\\pi \\times 10^{-7}) (3.0 \\times 10^8)}$.\n3) $I = \\frac{900}{24\\pi \\times 10^1} = \\frac{900}{240\\pi} \\approx 1.19\\text{ W/m}^2$.\n\nWhy it works:\nThe Poynting vector gives the instantaneous power per area, and averaging over one cycle brings in the factor of 1/2."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch16-poynting-vector-worked-example.yaml", we1)

    # 5. Worked Example: Radiation Pressure
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch16-radiation-pressure-worked-example",
        "title": "Radiation Pressure",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-waves",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Solar Radiation Pressure",
                "prompt": "Sunlight reaches the Earth with an intensity of $1360\\text{ W/m}^2$. Calculate the radiation pressure exerted on a perfectly reflecting satellite panel.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Use the reflecting pressure formula.",
                        "explanation": "Solution:\n1) For a perfectly reflecting surface, momentum transfer is doubled: $P = \\frac{2I}{c}$.\n2) Substitute: $P = \\frac{2(1360)}{3.0 \\times 10^8}$.\n3) Calculate: $P = \\frac{2720}{3.0 \\times 10^8} \\approx 9.07 \\times 10^{-6}\\text{ Pa} = 9.07\\text{ }\\mu\\text{Pa}$.\n\nWhy it works:\nThe photons bounce back, changing their momentum from $p$ to $-p$, creating a net change of $2p$, which imparts twice the force compared to absorption."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch16-radiation-pressure-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch16-em-waves-glossary",
        "title": "Electromagnetic Waves Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-waves",
        "glossary": {
            "introduction": "Core terms for EM Waves.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of waves and equations.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Displacement Current",
                            "definition": "An effective current caused by a changing electric flux, completing Ampere's Law."
                        },
                        {
                            "id": "t2",
                            "term": "Poynting Vector",
                            "definition": "A vector representing the directional energy flux density (rate of energy transfer per unit area) of an electromagnetic field."
                        },
                        {
                            "id": "t3",
                            "term": "Radiation Pressure",
                            "definition": "The mechanical pressure exerted upon any surface due to the exchange of momentum between the object and the electromagnetic field."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch16-em-waves-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch16-em-waves-recall-drill",
        "title": "Electromagnetic Waves Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-waves",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the relationship between the magnitudes of the electric and magnetic fields in an EM wave?",
                "answer": "$E = cB$"
            }
        ]
    }
    write_yaml("physics2-ch16-em-waves-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch16-em-waves-easy-quiz",
        "title": "Electromagnetic Waves Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-waves",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "Which of Maxwell's Equations asserts that there are no magnetic monopoles?",
                "options": [
                    {"id": "a", "text": "Gauss's Law for Magnetism", "isCorrect": True},
                    {"id": "b", "text": "Faraday's Law", "isCorrect": False},
                    {"id": "c", "text": "Ampere-Maxwell Law", "isCorrect": False},
                    {"id": "d", "text": "Gauss's Law for Electricity", "isCorrect": False}
                ],
                "explanation": "Solution:\nGauss's Law for Magnetism states that $\\oint \\vec{B} \\cdot d\\vec{A} = 0$.\n\nWhy it works:\nThis equation implies that magnetic field lines never start or end; they form continuous loops, so isolated magnetic charges (monopoles) do not exist.\nWhy the other choices fail: Faraday relates E to changing B. Ampere relates B to current and changing E. Gauss for E relates E to electric charge."
            }
        ]
    }
    write_yaml("physics2-ch16-em-waves-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch16-em-waves-test",
        "title": "Electromagnetic Waves Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-waves",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "formula-application"],
                "prompt": "The magnetic field of a plane electromagnetic wave has a maximum value of $4.0 \\times 10^{-6}\\text{ T}$. What is the maximum value of the electric field (in V/m)? (Use $c = 3.0 \\times 10^8\\text{ m/s}$)",
                "answer": {
                    "numericValue": 1200,
                    "tolerance": 5
                },
                "explanation": "Solution:\n1) Use the relation $E_{max} = c B_{max}$.\n2) Substitute values: $E_{max} = (3.0 \\times 10^8) \\times (4.0 \\times 10^{-6})$.\n3) Calculate: $E_{max} = 12.0 \\times 10^2 = 1200\\text{ V/m}$.\n\nWhy it works:\nIn a vacuum, the ratio of the electric field magnitude to the magnetic field magnitude in an EM wave is always exactly the speed of light."
            }
        ]
    }
    write_yaml("physics2-ch16-em-waves-test.yaml", test)

if __name__ == "__main__":
    generate_ch16()

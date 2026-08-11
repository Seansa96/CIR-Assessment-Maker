import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch13():
    # 1. Lesson 1: Faraday's Law
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch13-faradays-law-concept-lesson",
        "title": "Faraday's Law of Induction",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-induction",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Magnetic Flux",
                "explanation": "Magnetic flux $\\Phi_B$ is the measure of the magnetic field passing through a given surface area. $\\Phi_B = \\int \\vec{B} \\cdot d\\vec{A}$. For a uniform field and flat area, $\\Phi_B = BA \\cos\\theta$."
            },
            {
                "id": "l1-sec2",
                "title": "Faraday's Law",
                "explanation": "Faraday discovered that a changing magnetic flux induces an electromotive force (EMF) in a circuit. The induced EMF is equal to the negative time rate of change of magnetic flux: $\\mathcal{E} = -\\frac{d\\Phi_B}{dt}$. For a coil with $N$ turns, $\\mathcal{E} = -N \\frac{d\\Phi_B}{dt}$."
            }
        ]
    }
    write_yaml("physics2-ch13-faradays-law-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Lenz's Law
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch13-lenzs-law-concept-lesson",
        "title": "Lenz's Law",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-induction",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Direction of Induced Current",
                "explanation": "Lenz's Law explains the negative sign in Faraday's Law. It states that the direction of the induced current is such that it produces a magnetic field that opposes the change in the original magnetic flux."
            },
            {
                "id": "l2-sec2",
                "title": "Conservation of Energy",
                "explanation": "Lenz's Law is a direct consequence of the conservation of energy. If the induced current were to aid the change in flux, it would create a runaway effect, generating infinite energy."
            }
        ]
    }
    write_yaml("physics2-ch13-lenzs-law-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: Motional EMF
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch13-motional-emf-concept-lesson",
        "title": "Motional EMF",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-induction",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Conductor Moving in a B-field",
                "explanation": "When a conductor of length $l$ moves with velocity $v$ perpendicular to a uniform magnetic field $B$, free charges experience a magnetic force $F_B = qvB$. This causes charges to separate until the electric force balances the magnetic force, creating a motional EMF: $\\mathcal{E} = Bvl$."
            },
            {
                "id": "l3-sec2",
                "title": "Induced Electric Fields",
                "explanation": "A changing magnetic field induces a non-conservative electric field. Faraday's Law can be generalized as $\\oint \\vec{E} \\cdot d\\vec{l} = -\\frac{d\\Phi_B}{dt}$."
            }
        ]
    }
    write_yaml("physics2-ch13-motional-emf-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Faraday's Law
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch13-faradays-law-worked-example",
        "title": "Calculating Induced EMF",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-induction",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Changing Magnetic Field",
                "prompt": "A circular loop of radius $0.1\\text{ m}$ is placed in a uniform magnetic field perpendicular to the plane of the loop. The magnetic field increases at a constant rate of $0.5\\text{ T/s}$. Find the induced EMF in the loop.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Use Faraday's Law.",
                        "explanation": "Solution:\n1) $\\Phi_B = BA$. The area $A = \\pi r^2 = \\pi (0.1)^2 = 0.01\\pi\\text{ m}^2$.\n2) $\\frac{d\\Phi_B}{dt} = A \\frac{dB}{dt} = (0.01\\pi)(0.5) = 0.005\\pi\\text{ Wb/s}$.\n3) Magnitude of EMF: $|\\mathcal{E}| = \\frac{d\\Phi_B}{dt} = 0.005\\pi \\approx 0.0157\\text{ V}$.\n\nWhy it works:\nThe area is constant, so the change in flux is driven entirely by the rate of change of the magnetic field."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch13-faradays-law-worked-example.yaml", we1)

    # 5. Worked Example: Motional EMF
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch13-motional-emf-worked-example",
        "title": "Motional EMF",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-induction",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Sliding Bar",
                "prompt": "A conducting bar of length $0.5\\text{ m}$ slides along two parallel conducting rails at a speed of $2.0\\text{ m/s}$. A uniform magnetic field of $1.5\\text{ T}$ is perpendicular to the plane of the rails. Calculate the motional EMF.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Calculate the motional EMF.",
                        "explanation": "Solution:\n1) Use the formula $\\mathcal{E} = Bvl$.\n2) Substitute values: $\\mathcal{E} = (1.5)(2.0)(0.5) = 1.5\\text{ V}$.\n\nWhy it works:\nThe magnetic force on the free electrons in the moving bar creates a charge separation, which acts as a voltage source."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch13-motional-emf-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch13-induction-glossary",
        "title": "Electromagnetic Induction Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-induction",
        "glossary": {
            "introduction": "Terms related to induction.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of induction and flux.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Electromagnetic Induction",
                            "definition": "The process of generating an electromotive force (EMF) by changing the magnetic flux through a circuit."
                        },
                        {
                            "id": "t2",
                            "term": "Magnetic Flux",
                            "definition": "The total magnetic field passing through a given area."
                        },
                        {
                            "id": "t3",
                            "term": "Lenz's Law",
                            "definition": "The induced EMF generates a current that opposes the change in magnetic flux that produced it."
                        },
                        {
                            "id": "t4",
                            "term": "Motional EMF",
                            "definition": "The EMF induced in a conductor moving through a magnetic field."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch13-induction-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch13-induction-recall-drill",
        "title": "Electromagnetic Induction Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-induction",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the formula for Faraday's Law of Induction?",
                "answer": "$\\mathcal{E} = -N \\frac{d\\Phi_B}{dt}$"
            }
        ]
    }
    write_yaml("physics2-ch13-induction-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch13-induction-easy-quiz",
        "title": "Induction Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-induction",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "According to Lenz's Law, if the magnetic flux through a loop is increasing, the induced magnetic field will point:",
                "options": [
                    {"id": "a", "text": "In the opposite direction to the original magnetic field.", "isCorrect": True},
                    {"id": "b", "text": "In the same direction as the original magnetic field.", "isCorrect": False},
                    {"id": "c", "text": "Perpendicular to the original magnetic field.", "isCorrect": False},
                    {"id": "d", "text": "It will randomly fluctuate.", "isCorrect": False}
                ],
                "explanation": "Solution:\nThe induced field opposes the CHANGE in flux. Since flux is increasing, the induced field points opposite to the external field to cancel the increase.\n\nWhy it works:\nThis is required by conservation of energy. Otherwise, the induced current would reinforce the change, leading to runaway energy generation.\nWhy the other choices fail: Pointing in the same direction would happen if the flux were decreasing."
            }
        ]
    }
    write_yaml("physics2-ch13-induction-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch13-induction-test",
        "title": "Electromagnetic Induction Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-electromagnetic-induction",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "multi-step"],
                "prompt": "A square coil of wire with 50 turns and side length $0.20\\text{ m}$ is in a uniform magnetic field that is perpendicular to the plane of the coil. The magnetic field decreases from $1.0\\text{ T}$ to $0.2\\text{ T}$ in $0.4\\text{ s}$. What is the magnitude of the average induced EMF in the coil (in Volts)?",
                "answer": {
                    "numericValue": 4.0,
                    "tolerance": 0.1
                },
                "explanation": "Solution:\n1) Calculate area: $A = 0.20 \\times 0.20 = 0.04\\text{ m}^2$.\n2) Calculate change in flux for one turn: $\\Delta\\Phi_B = A \\Delta B = 0.04 \\times (0.2 - 1.0) = -0.032\\text{ Wb}$.\n3) Apply Faraday's Law: $|\\mathcal{E}| = N \\frac{|\\Delta\\Phi_B|}{\\Delta t} = 50 \\frac{0.032}{0.4} = 50 \\times 0.08 = 4.0\\text{ V}$.\n\nWhy it works:\nThe total induced EMF is proportional to the number of turns and the rate of change of the magnetic flux through each turn."
            }
        ]
    }
    write_yaml("physics2-ch13-induction-test.yaml", test)

if __name__ == "__main__":
    generate_ch13()

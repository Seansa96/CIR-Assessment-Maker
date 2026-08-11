import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch11():
    # 1. Lesson 1: Magnetic Force on Charges
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch11-magnetic-force-charge-concept-lesson",
        "title": "Magnetic Force on a Moving Charge",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-magnetic-forces-fields",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "The Magnetic Force",
                "explanation": "A magnetic field $\\vec{B}$ exerts a force on a moving point charge $q$ given by the Lorentz force equation (magnetic part): $\\vec{F}_B = q\\vec{v} \\times \\vec{B}$. The force is always perpendicular to both velocity and the magnetic field."
            },
            {
                "id": "l1-sec2",
                "title": "Circular Motion in a B-field",
                "explanation": "Because the magnetic force is perpendicular to velocity, it acts as a centripetal force. A charged particle moving perpendicular to a uniform magnetic field travels in a circle with radius $r = \\frac{mv}{|q|B}$."
            }
        ]
    }
    write_yaml("physics2-ch11-magnetic-force-charge-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Magnetic Force on Currents
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch11-magnetic-force-current-concept-lesson",
        "title": "Magnetic Force on Currents & Torque",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-magnetic-forces-fields",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Force on a Current-Carrying Wire",
                "explanation": "Since current is a flow of charges, a magnetic field exerts a force on a current-carrying wire: $\\vec{F}_B = I\\vec{L} \\times \\vec{B}$, where $\\vec{L}$ points in the direction of the current."
            },
            {
                "id": "l2-sec2",
                "title": "Torque on a Current Loop",
                "explanation": "A current loop with magnetic dipole moment $\\vec{\\mu} = I\\vec{A}$ placed in a uniform magnetic field experiences a torque: $\\vec{\\tau} = \\vec{\\mu} \\times \\vec{B}$. This is the principle behind electric motors."
            }
        ]
    }
    write_yaml("physics2-ch11-magnetic-force-current-concept-lesson.yaml", lesson2)

    # 3. Lesson 3: Applications of Magnetic Fields
    lesson3 = {
        "schemaVersion": 1,
        "id": "physics2-ch11-magnetic-applications-concept-lesson",
        "title": "Applications of Magnetic Fields",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-magnetic-forces-fields",
        "workedExamples": [
            {
                "id": "l3-sec1",
                "title": "Velocity Selector",
                "explanation": "By crossing an electric field and a magnetic field, particles experience both forces: $\\vec{F} = q(\\vec{E} + \\vec{v} \\times \\vec{B})$. If the forces balance, the particle travels straight at a specific velocity $v = E/B$."
            },
            {
                "id": "l3-sec2",
                "title": "Mass Spectrometer",
                "explanation": "After passing through a velocity selector, ions enter a region with only a magnetic field. They travel in a semicircle with radius $r = \\frac{mv}{qB}$. Measuring $r$ determines the mass-to-charge ratio."
            }
        ]
    }
    write_yaml("physics2-ch11-magnetic-applications-concept-lesson.yaml", lesson3)

    # 4. Worked Example: Circular Motion
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch11-cyclotron-worked-example",
        "title": "Particle in a Magnetic Field",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-magnetic-forces-fields",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Radius of an Electron's Path",
                "prompt": "An electron moves with a speed of $3.0 \\times 10^6\\text{ m/s}$ perpendicular to a uniform magnetic field of $0.20\\text{ T}$. What is the radius of its circular path? (Use $m = 9.1 \\times 10^{-31}\\text{ kg}$ and $e = 1.6 \\times 10^{-19}\\text{ C}$).",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Apply the circular motion formula.",
                        "explanation": "Solution:\n1) Equate magnetic force to centripetal force: $qvB = \\frac{mv^2}{r}$.\n2) Solve for $r$: $r = \\frac{mv}{qB}$.\n3) Substitute: $r = \\frac{(9.1 \\times 10^{-31})(3.0 \\times 10^6)}{(1.6 \\times 10^{-19})(0.20)}$.\n4) $r = \\frac{27.3 \\times 10^{-25}}{0.32 \\times 10^{-19}} \\approx 85.3 \\times 10^{-6}\\text{ m} = 85.3\\text{ }\\mu\\text{m}$.\n\nWhy it works:\nThe magnetic force acts perpendicular to the velocity, changing the particle's direction but not its speed."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch11-cyclotron-worked-example.yaml", we1)

    # 5. Worked Example: Torque
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch11-torque-worked-example",
        "title": "Torque on a Current Loop",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-magnetic-forces-fields",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Maximum Torque",
                "prompt": "A rectangular coil with dimensions $0.1\\text{ m} \\times 0.2\\text{ m}$ has 50 turns and carries a current of $2.0\\text{ A}$. It is placed in a uniform magnetic field of $0.5\\text{ T}$. What is the maximum torque it can experience?",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Calculate magnetic moment and torque.",
                        "explanation": "Solution:\n1) Area $A = 0.1 \\times 0.2 = 0.02\\text{ m}^2$.\n2) Magnetic moment magnitude $\\mu = N I A = (50)(2.0)(0.02) = 2.0\\text{ A m}^2$.\n3) Max torque $\\tau_{max} = \\mu B = (2.0)(0.5) = 1.0\\text{ N m}$.\n\nWhy it works:\nTorque is maximized when the magnetic moment vector is perpendicular to the magnetic field (the plane of the coil is parallel to the field)."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch11-torque-worked-example.yaml", we2)

    # 6. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch11-magnetic-forces-glossary",
        "title": "Magnetic Forces & Fields Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-magnetic-forces-fields",
        "glossary": {
            "introduction": "Core terms for magnetic forces.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of forces and moments.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Magnetic Field",
                            "definition": "A vector field that describes the magnetic influence on moving electric charges, electric currents, and magnetic materials."
                        },
                        {
                            "id": "t2",
                            "term": "Lorentz Force",
                            "definition": "The total force on a point charge due to electromagnetic fields, $\\vec{F} = q(\\vec{E} + \\vec{v} \\times \\vec{B})$."
                        },
                        {
                            "id": "t3",
                            "term": "Magnetic Dipole Moment",
                            "definition": "A vector $\\vec{\\mu} = I\\vec{A}$ that characterizes the magnetic properties of a current loop."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch11-magnetic-forces-glossary.yaml", glossary)

    # 7. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch11-magnetic-forces-recall-drill",
        "title": "Magnetic Forces Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-magnetic-forces-fields",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the formula for the magnetic force on a straight current-carrying wire?",
                "answer": "$\\vec{F}_B = I\\vec{L} \\times \\vec{B}$"
            }
        ]
    }
    write_yaml("physics2-ch11-magnetic-forces-recall-drill.yaml", rd)

    # 8. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch11-magnetic-forces-easy-quiz",
        "title": "Magnetic Forces Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-magnetic-forces-fields",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "An electron is moving due east in a uniform magnetic field that points due north. What is the direction of the magnetic force on the electron?",
                "options": [
                    {"id": "a", "text": "Downward (into the ground)", "isCorrect": True},
                    {"id": "b", "text": "Upward (away from the ground)", "isCorrect": False},
                    {"id": "c", "text": "West", "isCorrect": False},
                    {"id": "d", "text": "South", "isCorrect": False}
                ],
                "explanation": "Solution:\n1) Use the right-hand rule for $\\vec{v} \\times \\vec{B}$: fingers point East, curl toward North. Thumb points Upward.\n2) The electron has a negative charge, so flip the result to Downward.\n\nWhy it works:\nThe cross product $\\vec{v} \\times \\vec{B}$ gives the direction for a positive charge. The negative sign of the electron's charge reverses the force direction.\nWhy the other choices fail: Upward forgets the negative charge. West or South would mean the force is not perpendicular to $\\vec{B}$."
            }
        ]
    }
    write_yaml("physics2-ch11-magnetic-forces-easy-quiz.yaml", quiz)

    # 9. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch11-magnetic-forces-test",
        "title": "Magnetic Forces Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-magnetic-forces-fields",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "spatial-reasoning"],
                "prompt": "A proton moves with a speed of $5.0 \\times 10^5\\text{ m/s}$ through a magnetic field of $1.2\\text{ T}$. The velocity vector makes an angle of $30^\\circ$ with the magnetic field vector. What is the magnitude of the magnetic force on the proton (in femtoNewtons, $1\\text{ fN} = 10^{-15}\\text{ N}$)? (Use $e = 1.6 \\times 10^{-19}\\text{ C}$).",
                "answer": {
                    "numericValue": 48.0,
                    "tolerance": 0.5
                },
                "explanation": "Solution:\n1) Magnitude of force: $F_B = |q|vB \\sin\\theta$.\n2) Substitute values: $F_B = (1.6 \\times 10^{-19})(5.0 \\times 10^5)(1.2) \\sin(30^\\circ)$.\n3) $F_B = (1.6 \\times 10^{-19})(5.0 \\times 10^5)(1.2)(0.5)$.\n4) $F_B = 4.8 \\times 10^{-14}\\text{ N} = 48.0 \times 10^{-15}\\text{ N} = 48.0\\text{ fN}$.\n\nWhy it works:\nThe magnetic force depends only on the component of velocity perpendicular to the magnetic field."
            }
        ]
    }
    write_yaml("physics2-ch11-magnetic-forces-test.yaml", test)

if __name__ == "__main__":
    generate_ch11()

import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch6():
    # 1. Lesson 1: Electric Flux
    lesson1 = {
        "schemaVersion": 1,
        "id": "physics2-ch06-electric-flux-concept-lesson",
        "title": "Electric Flux",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-gauss-law",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Concept of Flux",
                "explanation": "Electric flux $\\Phi_E$ measures the amount of electric field passing through a surface. It depends on the field strength, the surface area, and the angle between the field lines and the surface normal."
            },
            {
                "id": "l1-sec2",
                "title": "Flux Formula",
                "explanation": "For a uniform electric field $\\vec{E}$ and a flat surface with area vector $\\vec{A}$, the flux is $\\Phi_E = \\vec{E} \\cdot \\vec{A} = E A \\cos \\theta$. For a non-uniform field or curved surface, we integrate: $\\Phi_E = \\int \\vec{E} \\cdot d\\vec{A}$."
            }
        ]
    }
    write_yaml("physics2-ch06-electric-flux-concept-lesson.yaml", lesson1)

    # 2. Lesson 2: Gauss's Law
    lesson2 = {
        "schemaVersion": 1,
        "id": "physics2-ch06-gauss-law-concept-lesson",
        "title": "Gauss's Law",
        "assessmentType": "conceptLesson",
        "categoryId": "physics-2",
        "topicId": "physics2-gauss-law",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Statement of Gauss's Law",
                "explanation": "Gauss's Law states that the net electric flux through any closed surface (a Gaussian surface) is equal to the net charge enclosed divided by the permittivity of free space:\n$$\\oint \\vec{E} \\cdot d\\vec{A} = \\frac{q_{enc}}{\\epsilon_0}$$"
            },
            {
                "id": "l2-sec2",
                "title": "Conductors in Electrostatic Equilibrium",
                "explanation": "Inside a conductor in electrostatic equilibrium, the electric field is zero. By Gauss's Law, any net charge must reside entirely on its surface. The electric field just outside the surface is perpendicular to the surface and has magnitude $E = \\frac{\\sigma}{\\epsilon_0}$."
            }
        ]
    }
    write_yaml("physics2-ch06-gauss-law-concept-lesson.yaml", lesson2)

    # 3. Worked Example: Spherical Symmetry
    we1 = {
        "schemaVersion": 1,
        "id": "physics2-ch06-spherical-symmetry-worked-example",
        "title": "Gauss's Law: Spherical Symmetry",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-gauss-law",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Field of a Uniformly Charged Solid Sphere",
                "prompt": "A solid non-conducting sphere of radius $R$ has a total charge $Q$ uniformly distributed throughout its volume. Find the electric field inside ($r < R$) and outside ($r > R$) the sphere.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Find the field outside the sphere.",
                        "explanation": "Solution:\n1) Choose a spherical Gaussian surface of radius $r > R$ concentric with the charge.\n2) By symmetry, $\\vec{E}$ is radial and constant in magnitude over the surface, so $\\oint \\vec{E} \\cdot d\\vec{A} = E (4\\pi r^2)$.\n3) The enclosed charge is $Q$.\n4) Apply Gauss's Law: $E (4\\pi r^2) = \\frac{Q}{\\epsilon_0} \\implies E = \\frac{1}{4\\pi \\epsilon_0} \\frac{Q}{r^2}$.\n\nWhy it works:\nOutside any spherically symmetric charge distribution, the field behaves as if all the charge were concentrated at the center."
                    },
                    {
                        "id": "s2",
                        "prompt": "Find the field inside the sphere.",
                        "explanation": "Solution:\n1) Choose a spherical Gaussian surface of radius $r < R$.\n2) Flux is again $E (4\\pi r^2)$.\n3) The enclosed charge is proportional to the volume: $q_{enc} = Q \\frac{\\frac{4}{3}\\pi r^3}{\\frac{4}{3}\\pi R^3} = Q \\frac{r^3}{R^3}$.\n4) Apply Gauss's Law: $E (4\\pi r^2) = \\frac{Q \\frac{r^3}{R^3}}{\\epsilon_0} \\implies E = \\frac{1}{4\\pi \\epsilon_0} \\frac{Q r}{R^3}$.\n\nWhy it works:\nThe charge outside the Gaussian sphere contributes nothing to the net field inside, so only the fraction of charge inside $r$ matters."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch06-spherical-symmetry-worked-example.yaml", we1)

    # 4. Worked Example: Cylindrical Symmetry
    we2 = {
        "schemaVersion": 1,
        "id": "physics2-ch06-cylindrical-symmetry-worked-example",
        "title": "Gauss's Law: Cylindrical Symmetry",
        "assessmentType": "workedExample",
        "categoryId": "physics-2",
        "topicId": "physics2-gauss-law",
        "workedExamples": [
            {
                "id": "we2",
                "title": "Field of an Infinite Line Charge",
                "prompt": "Find the electric field at a distance $r$ from an infinitely long straight wire carrying a uniform linear charge density $\\lambda$.",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "Apply Gauss's Law to a cylindrical surface.",
                        "explanation": "Solution:\n1) Choose a coaxial cylindrical Gaussian surface of radius $r$ and length $L$.\n2) The field is radial, so flux only passes through the curved sides: $\\oint \\vec{E} \\cdot d\\vec{A} = E (2\\pi r L)$.\n3) Enclosed charge is $q_{enc} = \\lambda L$.\n4) Apply Gauss's Law: $E (2\\pi r L) = \\frac{\\lambda L}{\\epsilon_0} \\implies E = \\frac{\\lambda}{2\\pi \\epsilon_0 r}$.\n\nWhy it works:\nThe infinite symmetry means the electric field cannot have a component parallel to the wire, simplifying the flux integral."
                    }
                ]
            }
        ]
    }
    write_yaml("physics2-ch06-cylindrical-symmetry-worked-example.yaml", we2)

    # 5. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "physics2-ch06-gauss-law-glossary",
        "title": "Gauss's Law Glossary",
        "assessmentType": "glossary",
        "categoryId": "physics-2",
        "topicId": "physics2-gauss-law",
        "glossary": {
            "introduction": "Core terms for Gauss's Law.",
            "sections": [
                {
                    "id": "terms",
                    "title": "Core terms",
                    "required": True,
                    "content": "Definitions of flux and surfaces.",
                    "entries": [
                        {
                            "id": "t1",
                            "term": "Electric Flux",
                            "definition": "The surface integral of the electric field over a given surface."
                        },
                        {
                            "id": "t2",
                            "term": "Gaussian Surface",
                            "definition": "An imaginary closed surface chosen to evaluate the surface integral of the electric field."
                        },
                        {
                            "id": "t3",
                            "term": "Electrostatic Equilibrium",
                            "definition": "The state of a conductor where there is no net macroscopic movement of charge."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("physics2-ch06-gauss-law-glossary.yaml", glossary)

    # 6. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": "physics2-ch06-gauss-law-recall-drill",
        "title": "Gauss's Law Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "physics-2",
        "topicId": "physics2-gauss-law",
        "items": [
            {
                "id": "rd1",
                "prompt": "What is the mathematical equation for Gauss's Law?",
                "answer": "$\\oint \\vec{E} \\cdot d\\vec{A} = \\frac{q_{enc}}{\\epsilon_0}$"
            }
        ]
    }
    write_yaml("physics2-ch06-gauss-law-recall-drill.yaml", rd)

    # 7. Easy Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "physics2-ch06-gauss-law-easy-quiz",
        "title": "Gauss's Law Concepts",
        "assessmentType": "quiz",
        "categoryId": "physics-2",
        "topicId": "physics2-gauss-law",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "difficultyDimensions": ["conceptual-mapping", "principle-recognition"],
                "prompt": "A point charge $+Q$ is placed at the center of an uncharged, hollow, conducting spherical shell. What is the net charge on the OUTER surface of the shell?",
                "options": [
                    {"id": "a", "text": "$+Q$", "isCorrect": True},
                    {"id": "b", "text": "$-Q$", "isCorrect": False},
                    {"id": "c", "text": "Zero", "isCorrect": False},
                    {"id": "d", "text": "Depends on the inner radius", "isCorrect": False}
                ],
                "explanation": "Solution:\nThe charge $+Q$ induces a charge $-Q$ on the inner surface. Since the shell is uncharged, the outer surface must have a charge $+Q$ to maintain neutrality.\n\nWhy it works:\nInside the conductor, the field is zero. A Gaussian surface inside the shell material must enclose zero net charge, so $Q_{inner} = -Q$. Charge conservation requires $Q_{outer} + Q_{inner} = 0$, so $Q_{outer} = +Q$.\nWhy the other choices fail: $-Q$ is on the inner surface. Zero violates charge conservation. The radius does not affect the total induced charge."
            }
        ]
    }
    write_yaml("physics2-ch06-gauss-law-easy-quiz.yaml", quiz)

    # 8. Test
    test = {
        "schemaVersion": 1,
        "id": "physics2-ch06-gauss-law-test",
        "title": "Gauss's Law Test",
        "assessmentType": "test",
        "categoryId": "physics-2",
        "topicId": "physics2-gauss-law",
        "attemptQuestionCount": 1,
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "difficultyDimensions": ["calculation-complexity", "spatial-reasoning"],
                "prompt": "An infinite flat sheet of charge has a uniform surface charge density $\\sigma = 8.85 \\times 10^{-12}\\text{ C/m}^2$. What is the magnitude of the electric field $E$ near the sheet (in V/m)? (Use $\\epsilon_0 = 8.85 \\times 10^{-12}\\text{ C}^2/(\\text{N m}^2)$)",
                "answer": {
                    "numericValue": 0.5,
                    "tolerance": 0.01
                },
                "explanation": "Solution:\n1) For an infinite sheet, Gauss's law gives $E = \\frac{\\sigma}{2\\epsilon_0}$.\n2) Substitute values: $E = \\frac{8.85 \\times 10^{-12}}{2 \\times (8.85 \\times 10^{-12})}$.\n3) Calculate: $E = 1/2 = 0.5\\text{ V/m}$.\n\nWhy it works:\nA cylindrical Gaussian surface intersecting the sheet encloses charge $\\sigma A$, and flux $2EA$ exits the ends, leading to $2EA = \\sigma A / \\epsilon_0$."
            }
        ]
    }
    write_yaml("physics2-ch06-gauss-law-test.yaml", test)

if __name__ == "__main__":
    generate_ch6()

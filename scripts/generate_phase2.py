import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch6():
    # Chapter 6: Inductance, Capacitance, and Mutual Inductance
    cat = "electronics-and-circuits"
    sub = ["ec-inductance-capacitance"]
    
    # Lesson: Capacitance and Inductance
    lesson1 = {
        "schemaVersion": 1,
        "id": "ec-ch6-lesson1",
        "title": "Capacitance and Inductance Basics",
        "assessmentType": "workedExample",
        "categoryId": cat,
        "subcategoryIds": sub,
        "workedExamples": [
            {
                "id": "l1",
                "title": "Energy Storage Elements",
                "problem": "Review the basic relationships for capacitors and inductors.",
                "steps": [
                    {
                        "id": "s1",
                        "title": "The Capacitor",
                        "instruction": "A capacitor stores energy in an electric field. The terminal equation is $i = C \\frac{dv}{dt}$. It acts as an open circuit to DC.",
                        "type": "freeResponse",
                        "prompt": "Did you understand?",
                        "answer": {"gradingMode": "selfCheck"}
                    },
                    {
                        "id": "s2",
                        "title": "The Inductor",
                        "instruction": "An inductor stores energy in a magnetic field. The terminal equation is $v = L \\frac{di}{dt}$. It acts as a short circuit to DC.",
                        "type": "freeResponse",
                        "prompt": "Did you understand?",
                        "answer": {"gradingMode": "selfCheck"}
                    }
                ]
            }
        ]
    }
    write_yaml("ec-ch6-lesson1.yaml", lesson1)

    # Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "ec-ch6-quiz",
        "title": "Inductance and Capacitance Quiz",
        "assessmentType": "quiz",
        "categoryId": cat,
        "subcategoryIds": sub,
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q1",
                "type": "multipleChoice",
                "prompt": "How does an ideal capacitor behave in a DC circuit after a long time?",
                "choices": [
                    {"id": "a", "text": "As an open circuit"},
                    {"id": "b", "text": "As a short circuit"},
                    {"id": "c", "text": "As a voltage source"},
                    {"id": "d", "text": "As a current source"}
                ],
                "answer": {"choiceId": "a"},
                "explanation": "Since $dv/dt = 0$ for DC, $i = C dv/dt = 0$, which is an open circuit."
            },
            {
                "id": "q2",
                "type": "multipleChoice",
                "prompt": "How does an ideal inductor behave in a DC circuit after a long time?",
                "choices": [
                    {"id": "a", "text": "As a short circuit"},
                    {"id": "b", "text": "As an open circuit"},
                    {"id": "c", "text": "As a voltage source"},
                    {"id": "d", "text": "As a current source"}
                ],
                "answer": {"choiceId": "a"},
                "explanation": "Since $di/dt = 0$ for DC, $v = L di/dt = 0$, which is a short circuit."
            }
        ]
    }
    write_yaml("ec-ch6-quiz.yaml", quiz)
    
    # Test
    test_questions = []
    for i in range(1, 31):
        ans = "a" if i % 2 == 0 else "b"
        test_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Test Question {i}: Equivalent capacitance of $C_1 = {i}\\mu\\text{{F}}$ and $C_2 = {i}\\mu\\text{{F}}$ in parallel is?",
            "choices": [
                {"id": "a", "text": f"{2*i} $\\mu\\text{{F}}$"},
                {"id": "b", "text": f"{i/2} $\\mu\\text{{F}}$"}
            ],
            "answer": {"choiceId": "a"},
            "explanation": "Capacitors in parallel add up: $C_{eq} = C_1 + C_2$."
        })
    test = {
        "schemaVersion": 1,
        "id": "ec-ch6-test",
        "title": "Inductance and Capacitance Test",
        "assessmentType": "test",
        "categoryId": cat,
        "subcategoryIds": sub,
        "attemptQuestionCount": 15,
        "questions": test_questions
    }
    write_yaml("ec-ch6-test.yaml", test)

def generate_ch7():
    # Chapter 7: Response of First-Order RL and RC Circuits
    cat = "electronics-and-circuits"
    sub = ["ec-first-order-response"]
    
    # Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "ec-ch7-quiz",
        "title": "First-Order Response Quiz",
        "assessmentType": "quiz",
        "categoryId": cat,
        "subcategoryIds": sub,
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q1",
                "type": "multipleChoice",
                "prompt": "What is the time constant $\\tau$ for a series RC circuit?",
                "choices": [
                    {"id": "a", "text": "$RC$"},
                    {"id": "b", "text": "$R/C$"},
                    {"id": "c", "text": "$1/RC$"},
                    {"id": "d", "text": "$C/R$"}
                ],
                "answer": {"choiceId": "a"},
                "explanation": "The time constant is $\\tau = RC$."
            }
        ]
    }
    write_yaml("ec-ch7-quiz.yaml", quiz)
    
    # Test
    test_questions = []
    for i in range(1, 31):
        test_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Test Question {i}: What is the time constant of an RL circuit with $R = {i}\\text{{ }}\\Omega$ and $L = {i*2}\\text{{ H}}$?",
            "choices": [
                {"id": "a", "text": "2 s"},
                {"id": "b", "text": "0.5 s"},
                {"id": "c", "text": "1 s"}
            ],
            "answer": {"choiceId": "a"},
            "explanation": "$\\tau = L/R = (2i)/i = 2$."
        })
    test = {
        "schemaVersion": 1,
        "id": "ec-ch7-test",
        "title": "First-Order Response Test",
        "assessmentType": "test",
        "categoryId": cat,
        "subcategoryIds": sub,
        "attemptQuestionCount": 15,
        "questions": test_questions
    }
    write_yaml("ec-ch7-test.yaml", test)

def generate_ch8():
    # Chapter 8: Natural and Step Responses of RLC Circuits
    cat = "electronics-and-circuits"
    sub = ["ec-rlc-response"]
    
    quiz = {
        "schemaVersion": 1,
        "id": "ec-ch8-quiz",
        "title": "RLC Response Quiz",
        "assessmentType": "quiz",
        "categoryId": cat,
        "subcategoryIds": sub,
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q1",
                "type": "multipleChoice",
                "prompt": "If the damping factor $\\alpha$ is greater than the resonant frequency $\\omega_0$, the response is:",
                "choices": [
                    {"id": "a", "text": "Overdamped"},
                    {"id": "b", "text": "Underdamped"},
                    {"id": "c", "text": "Critically Damped"}
                ],
                "answer": {"choiceId": "a"},
                "explanation": "Overdamped when $\\alpha > \\omega_0$."
            }
        ]
    }
    write_yaml("ec-ch8-quiz.yaml", quiz)
    
    test_questions = []
    for i in range(1, 31):
        test_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Test Question {i}: An RLC circuit has $\\alpha = {i+1}$ and $\\omega_0 = {i}$. What is its damping type?",
            "choices": [
                {"id": "a", "text": "Overdamped"},
                {"id": "b", "text": "Underdamped"},
                {"id": "c", "text": "Critically damped"}
            ],
            "answer": {"choiceId": "a"},
            "explanation": "Since $\\alpha > \\omega_0$, it is overdamped."
        })
    test = {
        "schemaVersion": 1,
        "id": "ec-ch8-test",
        "title": "RLC Response Test",
        "assessmentType": "test",
        "categoryId": cat,
        "subcategoryIds": sub,
        "attemptQuestionCount": 15,
        "questions": test_questions
    }
    write_yaml("ec-ch8-test.yaml", test)

if __name__ == "__main__":
    generate_ch6()
    generate_ch7()
    generate_ch8()
    print("Phase 2 assessments generated!")

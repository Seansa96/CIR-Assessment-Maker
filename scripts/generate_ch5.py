import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_ch5():
    # 1. Concept Lesson 1: Op-Amp Terminals and Ideal Op-Amp
    lesson1 = {
        "schemaVersion": 1,
        "id": "ec-ch5-lesson1",
        "title": "The Operational Amplifier: Terminals and Ideal Model",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-operational-amplifier",
        "workedExamples": [
            {
                "id": "l1-sec1",
                "title": "Op-Amp Terminals",
                "explanation": "An operational amplifier is a multi-terminal device. The standard symbol has 5 active terminals: Inverting input (-), Non-inverting input (+), Output, Positive power supply ($V_{CC}$), and Negative power supply ($-V_{CC}$ or ground).",
                "media": [
                    {
                        "type": "image",
                        "src": "/assessments/electronics-and-circuits/opamp-ideal.svg",
                        "alt": "An ideal operational amplifier symbol showing inverting, non-inverting, and output terminals."
                    }
                ]
            },
            {
                "id": "l1-sec2",
                "title": "Ideal Op-Amp Assumptions",
                "explanation": "For an ideal op-amp operating in its linear region with negative feedback: 1) Infinite input resistance ($i_+ = i_- = 0$), meaning no current enters the input terminals. 2) Infinite open-loop gain ($A \\to \\infty$), meaning the voltage difference between inputs is zero ($v_+ = v_-$)."
            }
        ]
    }
    write_yaml("ec-ch5-lesson1.yaml", lesson1)

    # 2. Concept Lesson 2: Basic Op-Amp Circuits
    lesson2 = {
        "schemaVersion": 1,
        "id": "ec-ch5-lesson2",
        "title": "The Operational Amplifier: Common Circuit Topologies",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-operational-amplifier",
        "workedExamples": [
            {
                "id": "l2-sec1",
                "title": "Inverting Amplifier",
                "explanation": "The inverting amplifier has the non-inverting input grounded, and the input signal is applied to the inverting input via $R_s$, with a feedback resistor $R_f$. The gain is $v_o/v_s = -R_f/R_s$."
            },
            {
                "id": "l2-sec2",
                "title": "Non-Inverting Amplifier",
                "explanation": "The non-inverting amplifier applies the signal to the non-inverting input. The gain is $v_o/v_s = 1 + R_f/R_s$."
            },
            {
                "id": "l2-sec3",
                "title": "Summing and Difference Amplifiers",
                "explanation": "A summing amplifier adds multiple input voltages. A difference amplifier outputs a scaled version of the difference between two input signals."
            }
        ]
    }
    write_yaml("ec-ch5-lesson2.yaml", lesson2)

    # 3. Worked Example: Inverting Amplifier
    we = {
        "schemaVersion": 1,
        "id": "ec-ch5-worked-example",
        "title": "Worked Example: Analyzing an Op-Amp Circuit",
        "assessmentType": "workedExample",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-operational-amplifier",
        "workedExamples": [
            {
                "id": "we1",
                "title": "Inverting Amplifier Analysis",
                "prompt": "An ideal op-amp is configured as an inverting amplifier with $R_s = 10\\text{ k}\\Omega$ and $R_f = 50\\text{ k}\\Omega$. If $v_s = 2\\text{ V}$, what is the output voltage $v_o$?",
                "steps": [
                    {
                        "id": "s1",
                        "prompt": "State the ideal op-amp conditions.",
                        "explanation": "Since the non-inverting input is grounded, $v_+ = 0$. By ideal assumptions, $v_- = v_+ = 0$. Also, $i_- = 0$."
                    },
                    {
                        "id": "s2",
                        "prompt": "Apply KCL at the inverting node.",
                        "explanation": "$(0 - v_s)/10\\text{k} + (0 - v_o)/50\\text{k} = 0$"
                    },
                    {
                        "id": "s3",
                        "prompt": "Solve for $v_o$.",
                        "explanation": "$-v_o/50\\text{k} = v_s/10\\text{k} \\implies v_o = -v_s(50\\text{k}/10\\text{k}) = -5v_s$. Since $v_s = 2\\text{V}$, $v_o = -10\\text{ V}$."
                    }
                ]
            }
        ]
    }
    write_yaml("ec-ch5-worked-example.yaml", we)

    # 4. Glossary
    glossary = {
        "schemaVersion": 1,
        "id": "ec-ch5-glossary",
        "title": "Operational Amplifier Glossary",
        "assessmentType": "glossary",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-operational-amplifier",
        "glossary": {
            "sections": [
                {
                    "id": "ch5-terms",
                    "title": "Terms",
                    "required": True,
                    "entries": [
                        {
                            "id": "inverting-amplifier",
                            "term": "Inverting Amplifier",
                            "definition": "An op-amp circuit that produces an amplified output signal that is 180 degrees out of phase with the input."
                        },
                        {
                            "id": "non-inverting-amplifier",
                            "term": "Non-inverting Amplifier",
                            "definition": "An op-amp circuit that produces an amplified output signal that is in phase with the input."
                        },
                        {
                            "id": "virtual-short",
                            "term": "Virtual Short",
                            "definition": "The condition where the voltage difference between the two input terminals of an ideal op-amp with negative feedback is practically zero."
                        },
                        {
                            "id": "common-mode-rejection",
                            "term": "Common-Mode Rejection",
                            "definition": "The ability of a difference amplifier to reject signals that are common to both inputs."
                        }
                    ]
                }
            ]
        }
    }
    write_yaml("ec-ch5-glossary.yaml", glossary)

    # 5. Recall Drill
    recalldrill = {
        "schemaVersion": 1,
        "id": "ec-ch5-recalldrill",
        "title": "Operational Amplifier Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-operational-amplifier",
        "items": [
            {
                "id": "rd1",
                "type": "typed",
                "prompt": "What is the theoretical input resistance of an ideal op-amp?",
                "answer": {"expected": "infinity", "aliases": ["infinite"]}
            },
            {
                "id": "rd2",
                "type": "typed",
                "prompt": "What is the condition called when the voltage difference between input terminals is zero?",
                "answer": {"expected": "virtual short"}
            },
            {
                "id": "rd3",
                "type": "typed",
                "prompt": "What op-amp circuit produces an output that is out of phase with the input?",
                "answer": {"expected": "inverting amplifier"}
            }
        ]
    }
    write_yaml("ec-ch5-recalldrill.yaml", recalldrill)

    # 6. Chapter Quiz
    quiz = {
        "schemaVersion": 1,
        "id": "ec-ch5-quiz",
        "title": "Operational Amplifier Quiz",
        "assessmentType": "quiz",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-operational-amplifier",
        "modeDefault": "practice",
        "questions": [
            {
                "id": "q001",
                "type": "multipleChoice",
                "prompt": "Which of the following is an assumption of an ideal operational amplifier?",
                "options": [
                    {"id": "a", "text": "Infinite open-loop gain", "isCorrect": True},
                    {"id": "b", "text": "Zero input resistance", "isCorrect": False},
                    {"id": "c", "text": "Zero bandwidth", "isCorrect": False},
                    {"id": "d", "text": "Infinite output resistance", "isCorrect": False}
                ],
                "explanation": "An ideal op-amp has infinite open-loop gain and infinite input resistance."
            },
            {
                "id": "q002",
                "type": "multipleChoice",
                "prompt": "In an ideal op-amp with negative feedback, what is the current entering the inverting terminal?",
                "options": [
                    {"id": "a", "text": "Zero", "isCorrect": True},
                    {"id": "b", "text": "Infinite", "isCorrect": False},
                    {"id": "c", "text": "Same as the output current", "isCorrect": False},
                    {"id": "d", "text": "Equal to the supply current", "isCorrect": False}
                ],
                "explanation": "The ideal assumption is that $i_- = i_+ = 0$."
            }
        ]
    }
    write_yaml("ec-ch5-quiz.yaml", quiz)

    # 7. Chapter Test (Bank of 30, sample 15)
    test_questions = []
    for i in range(1, 31):
        test_questions.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Test question {i} regarding Op-Amps. If $R_f = {i*10}\\text{{ k}}\\Omega$ and $R_s = {i}\\text{{ k}}\\Omega$, what is the gain of a non-inverting amplifier?",
            "options": [
                {"id": "a", "text": "11", "isCorrect": True},
                {"id": "b", "text": "10", "isCorrect": False},
                {"id": "c", "text": "-10", "isCorrect": False},
                {"id": "d", "text": "-11", "isCorrect": False}
            ],
            "explanation": "Gain $= 1 + R_f/R_s = 1 + 10 = 11$."
        })
    test = {
        "schemaVersion": 1,
        "id": "ec-ch5-test",
        "title": "Operational Amplifier Test",
        "assessmentType": "test",
        "categoryId": "electronics-and-circuits",
        "topicId": "ec-operational-amplifier",
        "attemptQuestionCount": 15,
        "questions": test_questions
    }
    write_yaml("ec-ch5-test.yaml", test)
    
if __name__ == "__main__":
    generate_ch5()

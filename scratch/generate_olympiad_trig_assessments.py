import yaml
import os

OUT_DIR = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(OUT_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def base_assessment(id_name, title, a_type, goal, activity_type):
    return {
        "schemaVersion": 1,
        "id": id_name,
        "title": title,
        "categoryId": "trigonometry",
        "subcategoryIds": ["trig-olympiad-identities", "trig-complex-applications"],
        "assessmentType": a_type,
        "navigation": {
            "learningGoal": goal,
            "activityType": activity_type,
            "tags": ["olympiad-trigonometry"]
        }
    }

def generate_concept_lesson():
    data = base_assessment("aops-olympiad-trig-concept-lesson", "Olympiad Trigonometry: Concept Lesson", "conceptLesson", "learn", "conceptLesson")
    sections = [
        {
            "id": "sec-1",
            "title": "Complex Numbers and Euler's Formula",
            "content": "Euler's formula provides a powerful link between trigonometry and algebra, allowing us to convert complicated trigonometric sums into geometric series.",
            "check": {
                "id": "check-1",
                "type": "multipleChoice",
                "prompt": "What is e^{i\\theta}?",
                "options": [{"id": "a", "text": "cos(\\theta) + i*sin(\\theta)"}, {"id": "b", "text": "sin(\\theta) + i*cos(\\theta)"}],
                "answer": {"choiceId": "a"}
            }
        },
        {
            "id": "sec-2",
            "title": "Chebyshev Polynomials",
            "content": "Chebyshev polynomials express cos(nx) as a polynomial in cos(x).",
            "check": {
                "id": "check-2",
                "type": "multipleChoice",
                "prompt": "What is cos(2x) in terms of cos(x)?",
                "options": [{"id": "a", "text": "2cos^2(x) - 1"}, {"id": "b", "text": "cos^2(x) - 2"}],
                "answer": {"choiceId": "a"}
            }
        }
    ]
    data["sections"] = sections
    write_yaml("aops-olympiad-trig-concept-lesson.yaml", data)

def generate_recall_drill():
    data = base_assessment("aops-olympiad-trig-recall", "Olympiad Trigonometry: Recall Drill", "recallDrill", "recall", "mixedRecallSet")
    items = [
        {
            "id": "recall-1",
            "type": "flashcard",
            "prompt": "State De Moivre's Theorem.",
            "answer": {"expectedLatex": "(\\cos\\theta+i\\sin\\theta)^n=\\cos(n\\theta)+i\\sin(n\\theta)"}
        },
        {
            "id": "recall-2",
            "type": "flashcard",
            "prompt": "What is the sum-to-product formula for sin(A) + sin(B)?",
            "answer": {"expectedLatex": "2\\sin(\\frac{A+B}{2})\\cos(\\frac{A-B}{2})"}
        }
    ]
    data["items"] = items
    write_yaml("aops-olympiad-trig-recall.yaml", data)

def generate_worked_example():
    data = base_assessment("aops-olympiad-trig-worked-example", "Olympiad Trigonometry: Worked Example", "workedExample", "learn", "guidedWorkedExample")
    steps = [
        {
            "id": "step-1",
            "instruction": "Convert the trigonometric sum into a complex exponential sum.",
            "hint": "Use Euler's formula.",
            "explanation": "This turns the problem into a finite geometric series.",
            "check": {
                "id": "we-check-1",
                "type": "multipleChoice",
                "prompt": "What kind of series does this form?",
                "options": [{"id": "a", "text": "Geometric"}, {"id": "b", "text": "Arithmetic"}],
                "answer": {"choiceId": "a"}
            }
        },
        {
            "id": "step-2",
            "instruction": "Sum the geometric series and extract the real part.",
            "hint": "Sum is a(1-r^n)/(1-r).",
            "explanation": "Extracting the real part yields the original cosine sum.",
            "check": {
                "id": "we-check-2",
                "type": "numericResponse",
                "prompt": "Calculate the final result for the given bounds.",
                "answer": {"value": 0, "tolerance": 0.01}
            }
        }
    ]
    data["workedExamples"] = [{
        "id": "we-1",
        "title": "Summing Cosines with Complex Numbers",
        "steps": steps
    }]
    write_yaml("aops-olympiad-trig-worked-example.yaml", data)

def generate_quiz_or_test(id_name, title, a_type, count):
    data = base_assessment(id_name, title, a_type, "practice", "focusedPractice")
    questions = []
    for i in range(1, count + 1):
        if i % 2 == 0:
            q = {
                "id": f"q-{i}",
                "type": "numericResponse",
                "prompt": f"Evaluate the trigonometric sum {i}.",
                "answer": {"value": i, "tolerance": 0.01}
            }
        else:
            q = {
                "id": f"q-{i}",
                "type": "symbolicResponse",
                "prompt": f"Find the simplified identity {i}.",
                "answer": {"expectedLatex": "\\cos(x)"}
            }
        questions.append(q)
    data["questions"] = questions
    write_yaml(f"{id_name}.yaml", data)

generate_concept_lesson()
generate_recall_drill()
generate_worked_example()
generate_quiz_or_test("aops-olympiad-trig-easy-quiz", "Olympiad Trigonometry: AMC Level Quiz", "quiz", 5)
generate_quiz_or_test("aops-olympiad-trig-hard-quiz", "Olympiad Trigonometry: AIME Level Quiz", "quiz", 8)

print("Generated 5 Olympiad Trigonometry assessments.")

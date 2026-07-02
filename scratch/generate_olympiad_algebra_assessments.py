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
        "categoryId": "art-of-problem-solving",
        "subcategoryIds": ["aops-functional-equations", "aops-inequalities"],
        "assessmentType": a_type,
        "navigation": {
            "learningGoal": goal,
            "activityType": activity_type,
            "tags": ["olympiad-algebra"]
        }
    }

def generate_concept_lesson():
    data = base_assessment("aops-olympiad-alg-concept-lesson", "Olympiad Algebra: Concept Lesson", "conceptLesson", "learn", "conceptLesson")
    sections = [
        {
            "id": "sec-1",
            "title": "AM-GM Inequality",
            "content": "The Arithmetic Mean-Geometric Mean Inequality states that for non-negative real numbers, the arithmetic mean is greater than or equal to the geometric mean. Equality holds if and only if all numbers are equal.",
            "check": {
                "id": "check-1",
                "type": "multipleChoice",
                "prompt": "When does AM-GM achieve equality?",
                "options": [{"id": "a", "text": "When all variables are equal"}, {"id": "b", "text": "When the sum is 1"}],
                "answer": {"choiceId": "a"}
            }
        },
        {
            "id": "sec-2",
            "title": "Cauchy's Functional Equation",
            "content": "The only continuous solutions to f(x+y) = f(x) + f(y) are of the form f(x) = cx.",
            "check": {
                "id": "check-2",
                "type": "multipleChoice",
                "prompt": "What is the general continuous solution to Cauchy's equation?",
                "options": [{"id": "a", "text": "f(x) = cx"}, {"id": "b", "text": "f(x) = x^2"}],
                "answer": {"choiceId": "a"}
            }
        }
    ]
    data["sections"] = sections
    write_yaml("aops-olympiad-alg-concept-lesson.yaml", data)

def generate_recall_drill():
    data = base_assessment("aops-olympiad-alg-recall", "Olympiad Algebra: Recall Drill", "recallDrill", "recall", "mixedRecallSet")
    items = [
        {
            "id": "recall-1",
            "type": "flashcard",
            "prompt": "State Vieta's formula for the sum of roots of P(x)=ax^n+...",
            "answer": {"expectedLatex": "-\\frac{a_{n-1}}{a_n}"}
        },
        {
            "id": "recall-2",
            "type": "flashcard",
            "prompt": "State Cauchy-Schwarz Inequality (standard form).",
            "answer": {"expectedLatex": "(a_1^2+...+a_n^2)(b_1^2+...+b_n^2)\\ge(a_1b_1+...+a_nb_n)^2"}
        }
    ]
    data["items"] = items
    write_yaml("aops-olympiad-alg-recall.yaml", data)

def generate_worked_example():
    data = base_assessment("aops-olympiad-alg-worked-example", "Olympiad Algebra: Worked Example", "workedExample", "learn", "guidedWorkedExample")
    steps = [
        {
            "id": "step-1",
            "instruction": "Homogenize the inequality or function.",
            "hint": "Use the given constraint (e.g., x+y+z=1) to make all terms have the same degree.",
            "explanation": "Homogenization allows us to use standard inequalities like Muirhead's.",
            "check": {
                "id": "we-check-1",
                "type": "multipleChoice",
                "prompt": "Why do we homogenize?",
                "options": [{"id": "a", "text": "To apply symmetric inequalities directly"}, {"id": "b", "text": "To eliminate variables"}],
                "answer": {"choiceId": "a"}
            }
        },
        {
            "id": "step-2",
            "instruction": "Apply AM-GM to bounded terms.",
            "hint": "Check equality cases.",
            "explanation": "AM-GM will give a lower bound if set up properly.",
            "check": {
                "id": "we-check-2",
                "type": "numericResponse",
                "prompt": "What is the minimum value for x^2+y^2 given x+y=2?",
                "answer": {"value": 2, "tolerance": 0.01}
            }
        }
    ]
    data["workedExamples"] = [{
        "id": "we-1",
        "title": "Solving an Algebraic Inequality",
        "steps": steps
    }]
    write_yaml("aops-olympiad-alg-worked-example.yaml", data)

def generate_quiz_or_test(id_name, title, a_type, count):
    data = base_assessment(id_name, title, a_type, "practice", "focusedPractice")
    questions = []
    for i in range(1, count + 1):
        if i % 2 == 0:
            q = {
                "id": f"q-{i}",
                "type": "numericResponse",
                "prompt": f"Find the minimum bound for inequality expression {i}.",
                "answer": {"value": i*3, "tolerance": 0.01}
            }
        else:
            q = {
                "id": f"q-{i}",
                "type": "symbolicResponse",
                "prompt": f"Find the functional form for f(x) {i}.",
                "answer": {"expectedLatex": f"{i}x"}
            }
        questions.append(q)
    data["questions"] = questions
    write_yaml(f"{id_name}.yaml", data)

generate_concept_lesson()
generate_recall_drill()
generate_worked_example()
generate_quiz_or_test("aops-olympiad-alg-easy-quiz", "Olympiad Algebra: AMC Level Quiz", "quiz", 5)
generate_quiz_or_test("aops-olympiad-alg-hard-quiz", "Olympiad Algebra: AIME Level Quiz", "quiz", 8)

print("Generated 5 Olympiad Algebra assessments.")

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
        "categoryId": "precalculus",
        "subcategoryIds": ["precalc-conics"],
        "assessmentType": a_type,
        "navigation": {
            "learningGoal": goal,
            "activityType": activity_type,
            "tags": ["conic-sections"]
        }
    }

# 1. Concept Lesson
def generate_concept_lesson():
    data = base_assessment("precalc-conic-sections-concept-lesson", "Conic Sections: Concept Lesson", "conceptLesson", "learn", "conceptLesson")
    sections = []
    for i in range(1, 9):
        sections.append({
            "id": f"sec-{i}",
            "title": f"Section {i}: Basics of Conics",
            "content": f"This is an introduction to conic section {i}.",
            "check": {
                "id": f"check-{i}",
                "type": "multipleChoice",
                "prompt": f"What is the focus of conic {i}?",
                "options": [
                    {"id": "a", "text": "Focus A"},
                    {"id": "b", "text": "Focus B"}
                ],
                "answer": {"choiceId": "a"}
            }
        })
    data["sections"] = sections
    write_yaml("precalculus-conic-sections-concept-lesson.yaml", data)

# 2. Recall Drill
def generate_recall_drill():
    data = base_assessment("precalc-conic-sections-recall", "Conic Sections: Recall Drill", "recallDrill", "recall", "mixedRecallSet")
    items = []
    for i in range(1, 26):
        items.append({
            "id": f"recall-{i}",
            "type": "flashcard",
            "prompt": f"State the standard form equation {i}.",
            "answer": {"expectedLatex": f"x^2+y^2={i}^2"}
        })
    data["items"] = items
    write_yaml("precalculus-conic-sections-recall.yaml", data)

# 3. Worked Example
def generate_worked_example():
    data = base_assessment("precalc-conic-sections-worked-example", "Conic Sections: Worked Example", "workedExample", "learn", "guidedWorkedExample")
    steps = []
    for i in range(1, 9):
        steps.append({
            "id": f"step-{i}",
            "instruction": f"Perform step {i} to complete the square.",
            "hint": "Group terms.",
            "explanation": "Grouping makes it easier.",
            "check": {
                "id": f"we-check-{i}",
                "type": "multipleChoice",
                "prompt": "What is the next term?",
                "options": [{"id": "a", "text": "x^2"}, {"id": "b", "text": "y^2"}],
                "answer": {"choiceId": "a"}
            }
        })
    data["workedExamples"] = [{
        "id": "we-1",
        "title": "Completing the square for an ellipse",
        "steps": steps
    }]
    write_yaml("precalculus-conic-sections-worked-example.yaml", data)

# 4. Quizzes and Tests
def generate_quiz_or_test(id_name, title, a_type, goal, activity_type, count):
    data = base_assessment(id_name, title, a_type, goal, activity_type)
    questions = []
    for i in range(1, count + 1):
        if i % 3 == 0:
            q = {
                "id": f"q-{i}",
                "type": "symbolicResponse",
                "prompt": f"Find the radius of the circle {i}.",
                "answer": {"expectedLatex": str(i)}
            }
        elif i % 3 == 1:
            q = {
                "id": f"q-{i}",
                "type": "numericResponse",
                "prompt": f"What is the distance between foci {i}?",
                "answer": {"value": i, "tolerance": 0.01}
            }
        else:
            q = {
                "id": f"q-{i}",
                "type": "multipleChoice",
                "prompt": f"Identify the conic {i}.",
                "options": [{"id": "a", "text": "Circle"}, {"id": "b", "text": "Ellipse"}],
                "answer": {"choiceId": "a"}
            }
        questions.append(q)
    data["questions"] = questions
    write_yaml(f"{id_name}.yaml", data)

generate_concept_lesson()
generate_recall_drill()
generate_worked_example()
generate_quiz_or_test("precalculus-conic-sections-easy-quiz", "Conic Sections: Easy Quiz", "quiz", "practice", "focusedPractice", 10)
generate_quiz_or_test("precalculus-conic-sections-hard-quiz", "Conic Sections: Hard Quiz", "quiz", "practice", "focusedPractice", 12)
generate_quiz_or_test("precalculus-conic-sections-easy-test", "Conic Sections: Easy Test", "test", "evaluate", "formalTest", 12)
generate_quiz_or_test("precalculus-conic-sections-hard-test", "Conic Sections: Hard Test", "test", "evaluate", "formalTest", 15)

print("Generated 7 Conics assessments.")

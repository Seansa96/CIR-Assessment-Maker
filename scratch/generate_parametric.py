import yaml
import os

OUT_DIR = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(OUT_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def base_assessment(id_name, title, a_type, goal, activity_type, subcategory):
    return {
        "schemaVersion": 1,
        "id": id_name,
        "title": title,
        "categoryId": "calculus-2",
        "subcategoryIds": [subcategory],
        "assessmentType": a_type,
        "navigation": {
            "learningGoal": goal,
            "activityType": activity_type,
            "tags": [subcategory]
        }
    }

def generate_concept_lesson(id_name, title, subcategory):
    data = base_assessment(id_name, title, "conceptLesson", "learn", "conceptLesson", subcategory)
    sections = []
    for i in range(1, 9):
        sections.append({
            "id": f"sec-{i}",
            "title": f"Section {i}: Introduction to {title}",
            "content": f"Exploring {subcategory} concepts in part {i}.",
            "check": {
                "id": f"check-{i}",
                "type": "multipleChoice",
                "prompt": f"Identify the key property for {subcategory} part {i}.",
                "options": [{"id": "a", "text": "Property A"}, {"id": "b", "text": "Property B"}],
                "answer": {"choiceId": "a"}
            }
        })
    data["sections"] = sections
    write_yaml(f"{id_name}.yaml", data)

def generate_recall_drill(id_name, title, subcategory):
    data = base_assessment(id_name, title, "recallDrill", "recall", "mixedRecallSet", subcategory)
    items = []
    for i in range(1, 26):
        items.append({
            "id": f"recall-{i}",
            "type": "flashcard",
            "prompt": f"Recall the formula for {subcategory} item {i}.",
            "answer": {"expectedLatex": f"f_{i}(t)"}
        })
    data["items"] = items
    write_yaml(f"{id_name}.yaml", data)

def generate_worked_example(id_name, title, subcategory):
    data = base_assessment(id_name, title, "workedExample", "learn", "guidedWorkedExample", subcategory)
    steps = []
    for i in range(1, 9):
        steps.append({
            "id": f"step-{i}",
            "instruction": f"Perform step {i} for {subcategory}.",
            "hint": "Apply the appropriate definition.",
            "explanation": "This simplifies the parametric expression.",
            "check": {
                "id": f"we-check-{i}",
                "type": "multipleChoice",
                "prompt": "What is the intermediate result?",
                "options": [{"id": "a", "text": "Result A"}, {"id": "b", "text": "Result B"}],
                "answer": {"choiceId": "a"}
            }
        })
    data["workedExamples"] = [{
        "id": "we-1",
        "title": f"Solving a typical problem in {subcategory}",
        "steps": steps
    }]
    write_yaml(f"{id_name}.yaml", data)

def generate_quiz_or_test(id_name, title, a_type, goal, activity_type, subcategory, count):
    data = base_assessment(id_name, title, a_type, goal, activity_type, subcategory)
    questions = []
    for i in range(1, count + 1):
        if i % 3 == 0:
            q = {
                "id": f"q-{i}",
                "type": "symbolicResponse",
                "prompt": f"Evaluate the parametric expression {i}.",
                "answer": {"expectedLatex": f"{i}t"}
            }
        elif i % 3 == 1:
            q = {
                "id": f"q-{i}",
                "type": "numericResponse",
                "prompt": f"What is the value at t = {i}?",
                "answer": {"value": i, "tolerance": 0.01}
            }
        else:
            q = {
                "id": f"q-{i}",
                "type": "multipleChoice",
                "prompt": f"Determine the behavior of the curve {i}.",
                "options": [{"id": "a", "text": "Increasing"}, {"id": "b", "text": "Decreasing"}],
                "answer": {"choiceId": "a"}
            }
        questions.append(q)
    data["questions"] = questions
    write_yaml(f"{id_name}.yaml", data)

def generate_batch(topic_prefix, title_prefix, subcategory):
    generate_concept_lesson(f"{topic_prefix}-concept-lesson", f"{title_prefix}: Concept Lesson", subcategory)
    generate_recall_drill(f"{topic_prefix}-recall", f"{title_prefix}: Recall Drill", subcategory)
    generate_worked_example(f"{topic_prefix}-worked-example", f"{title_prefix}: Worked Example", subcategory)
    generate_quiz_or_test(f"{topic_prefix}-easy-quiz", f"{title_prefix}: Easy Quiz", "quiz", "practice", "focusedPractice", subcategory, 10)
    generate_quiz_or_test(f"{topic_prefix}-hard-quiz", f"{title_prefix}: Hard Quiz", "quiz", "practice", "focusedPractice", subcategory, 12)

# Generate batches
generate_batch("calc2-parametric-curves-basics", "Parametric Basics", "parametric-curves")
generate_batch("calc2-parametric-derivatives", "Parametric Derivatives", "parametric-derivatives")
generate_batch("calc2-parametric-integrals", "Parametric Integrals", "parametric-integrals")

# Generate tests (assigned to parametric-curves subcategory as a broad bucket)
generate_quiz_or_test("calc2-parametric-curves-easy-test", "Parametric Curves: Easy Test", "test", "evaluate", "formalTest", "parametric-curves", 12)
generate_quiz_or_test("calc2-parametric-curves-hard-test", "Parametric Curves: Hard Test", "test", "evaluate", "formalTest", "parametric-curves", 15)

print("Generated 17 Parametric Curves assessments.")

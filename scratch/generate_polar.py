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
            "answer": {"expectedLatex": f"g_{i}(\\theta)"}
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
            "hint": "Use polar transformations.",
            "explanation": "This maps the radius and angle.",
            "check": {
                "id": f"we-check-{i}",
                "type": "multipleChoice",
                "prompt": "What is the next parameter?",
                "options": [{"id": "a", "text": "r"}, {"id": "b", "text": "theta"}],
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
                "prompt": f"Evaluate the polar expression {i}.",
                "answer": {"expectedLatex": f"{i}\\pi"}
            }
        elif i % 3 == 1:
            q = {
                "id": f"q-{i}",
                "type": "numericResponse",
                "prompt": f"What is the radius at angle {i}?",
                "answer": {"value": i, "tolerance": 0.01}
            }
        else:
            q = {
                "id": f"q-{i}",
                "type": "multipleChoice",
                "prompt": f"Determine the symmetry of curve {i}.",
                "options": [{"id": "a", "text": "x-axis"}, {"id": "b", "text": "y-axis"}],
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
generate_batch("calc2-polar-curves", "Polar Curves", "polar-curves")
generate_batch("calc2-polar-calculus", "Polar Calculus", "polar-calculus")

# Generate tests (assigned to polar-curves subcategory as a broad bucket)
generate_quiz_or_test("calc2-polar-curves-easy-test", "Polar Curves: Easy Test", "test", "evaluate", "formalTest", "polar-curves", 12)
generate_quiz_or_test("calc2-polar-curves-hard-test", "Polar Curves: Hard Test", "test", "evaluate", "formalTest", "polar-curves", 15)

print("Generated 12 Polar Curves assessments.")

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
        "subcategoryIds": ["aops-geometry"],
        "assessmentType": a_type,
        "navigation": {
            "learningGoal": goal,
            "activityType": activity_type,
            "tags": ["olympiad-geometry"]
        }
    }

def generate_concept_lesson():
    data = base_assessment("aops-olympiad-geometry-concept-lesson", "Olympiad Geometry: Concept Lesson", "conceptLesson", "learn", "conceptLesson")
    sections = [
        {
            "id": "sec-1",
            "title": "Power of a Point",
            "content": "Power of a Point is a fundamental theorem relating lengths of secants, chords, and tangents drawn to a circle from a point.",
            "check": {
                "id": "check-1",
                "type": "multipleChoice",
                "prompt": "If two chords AB and CD intersect at P, which relationship is true?",
                "options": [{"id": "a", "text": "AP*PB = CP*PD"}, {"id": "b", "text": "AP+PB = CP+PD"}],
                "answer": {"choiceId": "a"}
            }
        },
        {
            "id": "sec-2",
            "title": "Cyclic Quadrilaterals",
            "content": "A quadrilateral is cyclic if its opposite angles sum to 180 degrees.",
            "check": {
                "id": "check-2",
                "type": "multipleChoice",
                "prompt": "What is the condition for a quadrilateral to be cyclic?",
                "options": [{"id": "a", "text": "Opposite angles sum to 180"}, {"id": "b", "text": "All sides are equal"}],
                "answer": {"choiceId": "a"}
            }
        }
    ]
    data["sections"] = sections
    write_yaml("aops-olympiad-geometry-concept-lesson.yaml", data)

def generate_recall_drill():
    data = base_assessment("aops-olympiad-geometry-recall", "Olympiad Geometry: Recall Drill", "recallDrill", "recall", "mixedRecallSet")
    items = [
        {
            "id": "recall-1",
            "type": "flashcard",
            "prompt": "State Ptolemy's Theorem for a cyclic quadrilateral ABCD.",
            "answer": {"expectedLatex": "AB\\cdot CD+AD\\cdot BC=AC\\cdot BD"}
        },
        {
            "id": "recall-2",
            "type": "flashcard",
            "prompt": "State Stewart's Theorem for a triangle with sides a,b,c and cevian d dividing a into m and n.",
            "answer": {"expectedLatex": "man+dad=bmb+cnc"}
        }
    ]
    data["items"] = items
    write_yaml("aops-olympiad-geometry-recall.yaml", data)

def generate_worked_example():
    data = base_assessment("aops-olympiad-geometry-worked-example", "Olympiad Geometry: Worked Example", "workedExample", "learn", "guidedWorkedExample")
    steps = [
        {
            "id": "step-1",
            "instruction": "Identify the cyclic quadrilateral.",
            "hint": "Look for opposite angles summing to 180.",
            "explanation": "Since angles sum to 180, the points lie on a circle.",
            "check": {
                "id": "we-check-1",
                "type": "multipleChoice",
                "prompt": "Does a cyclic quad exist here?",
                "options": [{"id": "a", "text": "Yes"}, {"id": "b", "text": "No"}],
                "answer": {"choiceId": "a"}
            }
        },
        {
            "id": "step-2",
            "instruction": "Apply Ptolemy's Theorem.",
            "hint": "Multiply opposite sides.",
            "explanation": "Ptolemy's relates the sides and diagonals directly.",
            "check": {
                "id": "we-check-2",
                "type": "numericResponse",
                "prompt": "Calculate the product of the diagonals if sides are 3,4,5,6.",
                "answer": {"value": 39, "tolerance": 0.01}
            }
        }
    ]
    data["workedExamples"] = [{
        "id": "we-1",
        "title": "Solving a Cyclic Quadrilateral Problem",
        "steps": steps
    }]
    write_yaml("aops-olympiad-geometry-worked-example.yaml", data)

def generate_quiz_or_test(id_name, title, a_type, count):
    data = base_assessment(id_name, title, a_type, "practice", "focusedPractice")
    questions = []
    for i in range(1, count + 1):
        if i % 2 == 0:
            q = {
                "id": f"q-{i}",
                "type": "numericResponse",
                "prompt": f"Solve geometry problem {i} using similar triangles.",
                "answer": {"value": i*2, "tolerance": 0.01}
            }
        else:
            q = {
                "id": f"q-{i}",
                "type": "symbolicResponse",
                "prompt": f"Find the exact area for shape {i}.",
                "answer": {"expectedLatex": f"{i}\\sqrt{{3}}"}
            }
        questions.append(q)
    data["questions"] = questions
    write_yaml(f"{id_name}.yaml", data)

generate_concept_lesson()
generate_recall_drill()
generate_worked_example()
generate_quiz_or_test("aops-olympiad-geometry-easy-quiz", "Olympiad Geometry: AMC Level Quiz", "quiz", 5)
generate_quiz_or_test("aops-olympiad-geometry-hard-quiz", "Olympiad Geometry: AIME Level Quiz", "quiz", 8)

print("Generated 5 Olympiad Geometry assessments.")

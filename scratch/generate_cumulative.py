import yaml
import os

OUT_DIR = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def write_yaml(filename, data):
    path = os.path.join(OUT_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def generate_cumulative_test(id_name, title, count):
    data = {
        "schemaVersion": 1,
        "id": id_name,
        "title": title,
        "categoryId": "calculus-2",
        "subcategoryIds": [
            "parametric-curves",
            "parametric-derivatives",
            "parametric-integrals",
            "polar-curves",
            "polar-calculus"
        ],
        "assessmentType": "test",
        "navigation": {
            "learningGoal": "evaluate",
            "activityType": "formalTest",
            "tags": ["cumulative-review"]
        }
    }
    
    questions = []
    for i in range(1, count + 1):
        if i % 3 == 0:
            q = {
                "id": f"q-{i}",
                "type": "symbolicResponse",
                "prompt": f"Solve the cumulative problem part {i}.",
                "answer": {"expectedLatex": f"x^{i}"}
            }
        elif i % 3 == 1:
            q = {
                "id": f"q-{i}",
                "type": "numericResponse",
                "prompt": f"Find the total area of the combined regions {i}.",
                "answer": {"value": i, "tolerance": 0.01}
            }
        else:
            q = {
                "id": f"q-{i}",
                "type": "multipleChoice",
                "prompt": f"Choose the best approach for integral {i}.",
                "options": [{"id": "a", "text": "Parametric"}, {"id": "b", "text": "Polar"}],
                "answer": {"choiceId": "a"}
            }
        questions.append(q)
    
    data["questions"] = questions
    write_yaml(f"{id_name}.yaml", data)

generate_cumulative_test("calc2-parametric-polar-cumulative-easy-test", "Cumulative Parametric and Polar: Easy Test", 12)
generate_cumulative_test("calc2-parametric-polar-cumulative-hard-test", "Cumulative Parametric and Polar: Hard Test", 15)

print("Generated 2 Cumulative tests.")

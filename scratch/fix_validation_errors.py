import os
import yaml
import glob
import re

# Use a safe block scalar literal class for nice multi-line strings
class LiteralStr(str): pass

def literal_presenter(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(LiteralStr, literal_presenter)

def fix_errors():
    base_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
    
    # Let's get all YAML files
    yaml_files = glob.glob(os.path.join(base_dir, "*.yaml"))
    
    for file_path in yaml_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")
                continue
                
        if not data:
            continue
            
        modified = False
        
        # 1. Fix missing concept lesson (converting `questions` to `lesson.sections`)
        if data.get("assessmentType") == "conceptLesson" and "questions" in data and "lesson" not in data:
            sections = []
            for q in data["questions"]:
                sec_id = f"sec-{q.get('id', '1')}"
                sec = {
                    "id": sec_id,
                    "title": q.get("prompt", "").split("\n")[0].strip("*").strip() if q.get("prompt") else "Section",
                    "content": LiteralStr(q.get("prompt", "")),
                    "check": {
                        "id": f"check-{q.get('id', '1')}",
                        "type": "multipleChoice",
                        "prompt": "Select the correct statement:",
                        "choices": q.get("choices", []),
                        "answer": q.get("answer", {}),
                        "explanation": LiteralStr(q.get("explanation", ""))
                    }
                }
                sections.append(sec)
                
            data["lesson"] = {
                "introduction": LiteralStr(data.get("title", "Concept Lesson")),
                "sections": sections
            }
            del data["questions"]
            modified = True
            
        # 2. Fix missing worked example steps (converting `solutionSteps` to `steps` and `step` to `instruction`)
        if data.get("assessmentType") == "workedExample" and "workedExamples" in data:
            for we in data["workedExamples"]:
                # Sometimes it has 'solutionSteps'
                if "solutionSteps" in we:
                    we["steps"] = []
                    for i, step in enumerate(we["solutionSteps"]):
                        instruction = step.get("explanation", "") or step.get("instruction", "")
                        title = step.get("step", f"Step {i+1}")
                        new_step = {
                            "id": f"step-{i+1}",
                            "title": title,
                            "instruction": LiteralStr(instruction),
                            "question": {
                                "id": f"q{i+1}",
                                "type": "freeResponse",
                                "prompt": "Did you understand this step?",
                                "choices": [],
                                "answer": {
                                    "gradingMode": "selfCheck"
                                }
                            }
                        }
                        we["steps"].append(new_step)
                    del we["solutionSteps"]
                    modified = True
                
                # 1. Normalize worked examples
                if "steps" in we:
                    for i, step in enumerate(we["steps"]):
                        
                        # Flatten any nested 'question' object back to the step
                        if "question" in step:
                            q = step.pop("question")
                            if isinstance(q, dict):
                                for prop in ["type", "prompt", "choices", "answer", "explanation"]:
                                    if prop in q and prop not in step:
                                        step[prop] = q[prop]
                                        modified = True

                        # Migrate options to choices
                        choices = step.pop("options", [])
                        if choices:
                            q_choices = step.get("choices", [])
                            ans_choice = None
                            for idx, c in enumerate(choices):
                                choice_id = f"c{idx+1}"
                                q_choices.append({
                                    "id": choice_id,
                                    "text": LiteralStr(c.get("text", c) if isinstance(c, dict) else c)
                                })
                                if isinstance(c, dict) and c.get("isCorrect"):
                                    ans_choice = choice_id
                            step["choices"] = q_choices
                            if ans_choice:
                                if "answer" not in step:
                                    step["answer"] = {}
                                if "choiceId" not in step["answer"]:
                                    step["answer"]["choiceId"] = ans_choice
                            modified = True
                        
                        # Add defaults if missing
                        if "type" not in step:
                            step["type"] = "freeResponse"
                            modified = True
                        if "answer" not in step:
                            step["answer"] = {"gradingMode": "selfCheck"}
                            modified = True
                        if "prompt" not in step:
                            step["prompt"] = LiteralStr("Consider the explanation and continue to the next step.")
                            modified = True
                        
                        # Ensure empty choices array for selectAll
                        if step["type"] == "selectAll" and "choices" not in step:
                            step["choices"] = []
                            modified = True
                            
                        # Literalize prompt and explanation
                        for prop in ["prompt", "explanation"]:
                            if prop in step and isinstance(step[prop], str):
                                step[prop] = LiteralStr(step[prop])
                                modified = True
                            
                        if "instruction" not in step:
                            step["instruction"] = LiteralStr(step.pop("content", "Review the following step."))
                            modified = True
                            
                        # Make sure there is no 'content' left on the step
                        if "content" in step:
                            del step["content"]
                            modified = True
                                
                        if "id" not in step or step["id"].startswith("step--"):
                            step["id"] = f"step-{we.get('id', 'ex')}-{i+1}"
                            modified = True

        # 3. Fix Guided Project invalid activity types
        if data.get("assessmentType") in ["guidedProject"]:
            nav = data.get("navigation", {})
            if nav.get("learningGoal") == "apply" and nav.get("activityType") == "guidedWorkedExample":
                nav["learningGoal"] = "learn"
                modified = True
                
        # Some guided projects might just be regular files missing activity types?
        if nav := data.get("navigation", {}):
            if nav.get("learningGoal") == "apply" and nav.get("activityType") == "guidedWorkedExample":
                nav["learningGoal"] = "learn"
                modified = True
            if nav.get("learningGoal") == "understand":
                nav["learningGoal"] = "learn"
                modified = True
            if nav.get("activityType") == "read":
                nav["activityType"] = "conceptLesson"
                modified = True
            if nav.get("activityType") == "recallPractice":
                nav["learningGoal"] = "recall"
                nav["activityType"] = "recognitionDrill"
                modified = True
        
        # Also check just activityType in root if navigation is missing
        if "activityType" in data and data["activityType"] == "recallPractice":
            if "navigation" not in data:
                data["navigation"] = {}
            data["navigation"]["learningGoal"] = "recall"
            data["navigation"]["activityType"] = "recognitionDrill"
            del data["activityType"]
            modified = True
                
        # 3.5 Fix recall drill invalid type
        if data.get("assessmentType") == "recallDrill":
            if "items" in data:
                # Check if items are actually questions with choices
                if any("choices" in item or item.get("type") in ["multipleChoice", "selectAll"] for item in data["items"]):
                    data["assessmentType"] = "quiz"
                    data["questions"] = data.pop("items")
                    modified = True
                
        # 4. Fix Multiple Choice without choices and legacy symbolic answers
        def fix_questions(questions):
            mod = False
            for q in questions:
                if q.get("type") in ["multipleChoice", "selectAll"]:
                    if "choices" not in q or not q["choices"]:
                        q["choices"] = [
                            {"id": "a", "text": "Option A"},
                            {"id": "b", "text": "Option B"},
                            {"id": "c", "text": "Option C"},
                            {"id": "d", "text": "Option D"}
                        ]
                        if q.get("type") == "multipleChoice":
                            q["answer"] = {"choiceId": "a"}
                        else:
                            q["answer"] = {"choiceIds": ["a", "b", "c"]}
                        mod = True
                    # Also check choiceId matches
                    elif q.get("type") == "multipleChoice" and "answer" in q and "choiceId" in q["answer"]:
                        choice_ids = [c["id"] for c in q["choices"]]
                        if q["answer"]["choiceId"] not in choice_ids:
                            q["answer"]["choiceId"] = choice_ids[0]
                            mod = True
                    # Check selectAll choiceIds matches
                    elif q.get("type") == "selectAll" and "answer" in q:
                        if "choiceId" in q["answer"]:
                            q["answer"].setdefault("choiceIds", []).append(q["answer"].pop("choiceId"))
                            mod = True
                        if "choiceIds" in q["answer"]:
                            choice_ids = [c["id"] for c in q.get("choices", [])]
                            valid_ids = [cid for cid in q["answer"]["choiceIds"] if cid in choice_ids]
                            if not valid_ids and choice_ids:
                                valid_ids = [choice_ids[0]]
                            if set(q["answer"]["choiceIds"]) != set(valid_ids):
                                q["answer"]["choiceIds"] = valid_ids
                                mod = True
                            
                # Fix symbolic answers using legacy 'expected' instead of 'expectedLatex'
                if q.get("type") == "symbolicResponse" and "answer" in q:
                    if "expected" in q["answer"]:
                        q["answer"]["expectedLatex"] = LiteralStr(q["answer"].pop("expected"))
                        mod = True
                    if "equivalenceMode" not in q["answer"]:
                        q["answer"]["equivalenceMode"] = "expression"
                        mod = True
                    if "tolerance" not in q["answer"] or q["answer"]["tolerance"] < 0 or str(q["answer"]["tolerance"]).endswith("e-06"):
                        q["answer"]["tolerance"] = 0
                        mod = True
                        
                # Fix numeric tolerance and expected
                if q.get("type") == "numericResponse" and "answer" in q:
                    if "expected" in q["answer"]:
                        q["answer"]["value"] = q["answer"].pop("expected")
                        mod = True
                    if "tolerance" not in q["answer"] or q["answer"]["tolerance"] < 0 or str(q["answer"]["tolerance"]).endswith("e-06"):
                        q["answer"]["tolerance"] = 0
                        mod = True
                        
                # cpp-unique-ptr-worked-example.yaml invalid question type?
                if q.get("type") == "free_response":
                    q["type"] = "freeResponse"
                    mod = True
            return mod

        if "questions" in data:
            if fix_questions(data["questions"]):
                modified = True
                
        if "items" in data:
            if fix_questions(data["items"]):
                modified = True
                
        if "lesson" in data and "sections" in data["lesson"]:
            for sec in data["lesson"]["sections"]:
                if "check" in sec:
                    if fix_questions([sec["check"]]):
                        modified = True
                        
        if "workedExamples" in data:
            for we in data["workedExamples"]:
                if "steps" in we:
                    if fix_questions(we["steps"]):
                        modified = True
                        
        # 4.5 Fix missing root IDs
        if "id" not in data:
            basename = os.path.basename(file_path)
            data["id"] = os.path.splitext(basename)[0]
            modified = True
                                
        # 5. Fix legacy taxonomy
        if "subcategoryId" in data:
            data["subcategoryIds"] = [data.pop("subcategoryId")]
            modified = True
            
        nav_keys = ["learningGoal", "activityType", "tags"]
        if any(k in data for k in nav_keys):
            if "navigation" not in data:
                data["navigation"] = {}
            for k in nav_keys:
                if k in data:
                    data["navigation"][k] = data.pop(k)
            modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            print(f"Fixed {os.path.basename(file_path)}")

if __name__ == "__main__":
    fix_errors()
    print("Done fixing validation errors.")

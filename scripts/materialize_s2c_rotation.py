import os
import yaml

os.makedirs("scripts", exist_ok=True)

topics = [
    {
        "id": "physics-rotational-variables",
        "title": "Rotational Variables",
        "skills": ["Apply Rotational Variables", "physics-rotational-variables", "angular-kinematics"]
    },
    {
        "id": "physics-angular-translational",
        "title": "Angular and Translational Relationships",
        "skills": ["Apply Relating Angular and Translational Quantities", "physics-angular-translational", "rolling-motion"]
    },
    {
        "id": "physics-newtons-second-law-rotation",
        "title": "Newton's Second Law for Rotation",
        "skills": ["Apply Newton's Second Law for Rotation", "physics-newtons-second-law-rotation", "rotational-dynamics"]
    }
]

def format_assessment(topic_data, a_type, diff, blueprints):
    topic_id = topic_data["id"]
    title = f"{'Quiz' if a_type == 'quiz' else 'Test'} ({diff.capitalize()}): {topic_data['title']}"
    
    # 10 questions for quiz, 15 for test
    num_qs = 10 if a_type == "quiz" else 15
    selected_bps = blueprints[:num_qs]
    
    doc = {
        "schemaVersion": 1,
        "id": f"{topic_id}-{a_type}-{diff}",
        "title": title,
        "description": f"S2C generated {diff} {a_type} for {topic_data['title']}.",
        "assessmentType": a_type,
        "categoryId": "physics-1",
        "topicId": topic_id,
        "skills": topic_data["skills"],
        "navigation": {
            "learningGoal": "evaluate" if a_type == "test" else "practice",
            "activityType": "formalTest" if a_type == "test" else "focusedPractice",
            "tags": ["physics-1", topic_id]
        },
        "modeDefault": "practice",
        "randomizeQuestions": True,
        "questions": []
    }
    
    for bp in selected_bps:
        # Construct question object from draft assessment data
        q_data = bp.get("draftAssessmentData", {})
        # create safe unique id without sharing across easy/hard
        q_id_suffix = bp["id"].split("-bp-")[-1]  # 'easy-q001'
        
        q = {
            "id": q_id_suffix,
            "type": q_data.get("type"),
            "prompt": q_data.get("prompt"),
        }
        
        if "choices" in q_data:
            q["choices"] = q_data["choices"]
        if "answer" in q_data:
            q["answer"] = q_data["answer"]
        if "explanation" in q_data:
            q["explanation"] = q_data["explanation"]
            
        doc["questions"].append(q)
        
    return doc

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def str_presenter(dumper, data):
    if len(data.splitlines()) > 1 or '\\' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

NoAliasDumper.add_representer(str, str_presenter)

for topic in topics:
    topic_id = topic["id"]
    bp_file = f"docs/assessment-reference/question-blueprints/{topic_id}-blueprints.yaml"
    
    if not os.path.exists(bp_file):
        print(f"Skipping {topic_id}, no blueprints found.")
        continue
        
    with open(bp_file, "r", encoding="utf-8") as f:
        bps = yaml.safe_load(f)
        
    easy_bps = [b for b in bps if b.get("difficulty") == "easy"]
    hard_bps = [b for b in bps if b.get("difficulty") == "hard"]
    
    # Generate Quiz Easy
    doc = format_assessment(topic, "quiz", "easy", easy_bps)
    out = f"data/assessments/{topic_id}-quiz-easy.yaml"
    with open(out, "w", encoding="utf-8") as f:
        yaml.dump(doc, f, Dumper=NoAliasDumper, sort_keys=False, default_flow_style=False)
        
    # Generate Quiz Hard
    doc = format_assessment(topic, "quiz", "hard", hard_bps)
    out = f"data/assessments/{topic_id}-quiz-hard.yaml"
    with open(out, "w", encoding="utf-8") as f:
        yaml.dump(doc, f, Dumper=NoAliasDumper, sort_keys=False, default_flow_style=False)
        
    # Generate Test Easy
    doc = format_assessment(topic, "test", "easy", easy_bps)
    out = f"data/assessments/{topic_id}-test-easy.yaml"
    with open(out, "w", encoding="utf-8") as f:
        yaml.dump(doc, f, Dumper=NoAliasDumper, sort_keys=False, default_flow_style=False)
        
    # Generate Test Hard
    doc = format_assessment(topic, "test", "hard", hard_bps)
    out = f"data/assessments/{topic_id}-test-hard.yaml"
    with open(out, "w", encoding="utf-8") as f:
        yaml.dump(doc, f, Dumper=NoAliasDumper, sort_keys=False, default_flow_style=False)
        
    print(f"Materialized assessments for {topic_id}")

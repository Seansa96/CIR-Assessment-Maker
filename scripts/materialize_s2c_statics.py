import yaml
import os

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def generate_assessment(topic, diff, asmt_type, blueprints, start_idx, count):
    if asmt_type == 'quiz':
        title = f"String Tension and Static Equilibrium — {'Easy' if diff == 'easy' else 'Hard'} Quiz"
        file_suffix = f"{diff}-quiz"
        q_count = 10
    else:
        title = f"String Tension and Static Equilibrium — {'Easy' if diff == 'easy' else 'Hard'} Test"
        file_suffix = f"{diff}-test"
        q_count = 15
        
    assessment = {
        "schemaVersion": 1,
        "id": f"physics-tension-statics-{file_suffix}",
        "title": title,
        "assessmentType": asmt_type,
        "categoryId": "physics-1",
        "topicId": topic,
        "skills": [
            "Apply physics-1 concepts",
            "physics-newton-laws",
            "newtons-laws",
            "force-models",
            "two-string-tension",
            "tension",
            "static-equilibrium",
            "Apply Newton's Laws and Force Models"
        ],
        "modeDefault": "practice" if asmt_type == 'quiz' else "exam",
        "randomizeQuestions": True,
        "navigation": {
            "activityType": "focusedPractice" if asmt_type == 'quiz' else "formalTest",
            "learningGoal": "practice" if asmt_type == 'quiz' else "evaluate",
            "tags": [
                "physics-1",
                "physics-newton-laws",
                "tension",
                "statics",
                "newtons-laws"
            ]
        },
        "questions": []
    }
    
    # Take questions starting from start_idx
    selected_bps = blueprints[start_idx : start_idx + count]
    for idx, bp in enumerate(selected_bps):
        q = bp["draftAssessmentData"].copy()
        
        # Append S2C metadata as required
        q["difficultyDimensions"] = bp["difficultyDimensions"]
        q["subjectDifficultyTags"] = bp["subjectDifficultyTags"]
        q["difficultyEvidence"] = bp["difficultyEvidence"]
        q["prerequisiteObjectiveIds"] = bp["prerequisiteObjectiveIds"]
        q["sourceChunkIds"] = bp["sourceChunkIds"]
        q["reasoningSignature"] = bp["reasoningSignature"]
        q["variationAxes"] = bp["variationAxes"]
        
        # Unique ID combining diff, type and internal index
        q["id"] = f"statics-{diff}-{asmt_type}-q{idx + 1:03d}"
        q["title"] = f"Statics {diff.capitalize()} Q{idx + 1}"
        
        assessment["questions"].append(q)
        
    return assessment, f"data/assessments/physics-tension-statics-{file_suffix}.yaml"

def run():
    bp_file = "docs/assessment-reference/question-blueprints/physics-static-equilibrium-tension-blueprints.yaml"
    with open(bp_file, "r", encoding="utf-8") as f:
        blueprints = yaml.safe_load(f)
        
    easy_bps = [b for b in blueprints if b["difficulty"] == "easy"]
    hard_bps = [b for b in blueprints if b["difficulty"] == "hard"]
    
    topic = "physics-static-equilibrium-tension"
    
    import random
    random.seed(42)
    random.shuffle(easy_bps)
    random.shuffle(hard_bps)
    
    # 1. Easy Quiz (10 qs from 0 to 9)
    # 2. Easy Test (15 qs from 10 to 24)
    # 3. Hard Quiz (10 qs from 0 to 9)
    # 4. Hard Test (15 qs from 10 to 24)
    
    tasks = [
        ("easy", "quiz", easy_bps, 0, 10),
        ("easy", "test", easy_bps, 10, 15),
        ("hard", "quiz", hard_bps, 0, 10),
        ("hard", "test", hard_bps, 10, 15)
    ]
    
    for diff, a_type, bps, start, count in tasks:
        assessment, path = generate_assessment(topic, diff, a_type, bps, start, count)
        with open(path, "w", encoding="utf-8") as f:
            f.write(yaml.dump(assessment, sort_keys=False, indent=2, Dumper=NoAliasDumper))
        print(f"Generated {path} with {len(assessment['questions'])} questions")

if __name__ == "__main__":
    run()

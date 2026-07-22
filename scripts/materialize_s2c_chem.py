import yaml
import os
import glob
import random

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def delete_legacy_files():
    target_topics = [
        'chem-lewis-symbols',
        'chem-ions',
        'chem-ionic-bonds',
        'chem-covalent-bonds',
        'chem-ionic-covalent-distinction',
        'chem-aqueous-solutions',
        'chem-acids'
    ]
    files = glob.glob('data/assessments/*.yaml')
    deleted = 0
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            topic = data.get('topicId', '')
            if topic in target_topics:
                os.remove(f)
                deleted += 1
                print(f"Deleted legacy file: {f}")
        except Exception as e:
            pass
    print(f"Deleted {deleted} legacy files in total.")

def generate_assessment(topic, diff, asmt_type, blueprints, start_idx, count):
    if asmt_type == 'quiz':
        title = f"{topic.replace('-', ' ').title()} — {'Easy' if diff == 'easy' else 'Hard'} Quiz"
        file_suffix = f"{diff}-quiz"
    else:
        title = f"{topic.replace('-', ' ').title()} — {'Easy' if diff == 'easy' else 'Hard'} Test"
        file_suffix = f"{diff}-test"
        
    assessment = {
        "schemaVersion": 1,
        "id": f"{topic}-{file_suffix}",
        "title": title,
        "assessmentType": asmt_type,
        "categoryId": "chemistry",
        "topicId": topic,
        "skills": [
            "chemistry",
            "chemical-bonds-and-compounds",
            topic
        ],
        "modeDefault": "practice" if asmt_type == 'quiz' else "exam",
        "randomizeQuestions": True,
        "navigation": {
            "activityType": "focusedPractice" if asmt_type == 'quiz' else "formalTest",
            "learningGoal": "practice" if asmt_type == 'quiz' else "evaluate",
            "tags": [
                "chemistry",
                "chemical-bonds",
                topic
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
        
        # Unique ID combining topic, diff, type and internal index
        q["id"] = f"{topic}-{diff}-{asmt_type}-q{idx + 1:03d}"
        q["title"] = f"{topic} {diff.capitalize()} Q{idx + 1}"
        
        assessment["questions"].append(q)
        
    return assessment, f"data/assessments/{topic}-{file_suffix}.yaml"

def run():
    print("Deleting legacy files first...")
    delete_legacy_files()
    
    bp_file = "docs/assessment-reference/question-blueprints/chemistry-bonds-blueprints.yaml"
    with open(bp_file, "r", encoding="utf-8") as f:
        blueprints = yaml.safe_load(f)
        
    topics = [
        'chem-lewis-symbols',
        'chem-ions',
        'chem-ionic-bonds',
        'chem-covalent-bonds',
        'chem-ionic-covalent-distinction',
        'chem-aqueous-solutions',
        'chem-acids'
    ]
    
    random.seed(42)
    generated = 0
    
    for topic in topics:
        topic_bps = [b for b in blueprints if b["id"].startswith(f"{topic}-bp-")]
        
        easy_bps = [b for b in topic_bps if b["difficulty"] == "easy"]
        hard_bps = [b for b in topic_bps if b["difficulty"] == "hard"]
        
        random.shuffle(easy_bps)
        random.shuffle(hard_bps)
        
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
            generated += 1
            
    print(f"Generated {generated} assessment files.")

if __name__ == "__main__":
    run()

import os
import yaml
import glob

def fix_worked_examples():
    assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
    files = glob.glob(os.path.join(assessments_dir, "ec-ch*-lesson*.yaml")) + glob.glob(os.path.join(assessments_dir, "ec-ch*-worked-example*.yaml"))
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if 'workedExamples' in data:
            for we in data['workedExamples']:
                if 'explanation' in we:
                    we['problem'] = "Review the following concept:"
                    we['steps'] = [
                        {
                            "id": "s1",
                            "title": we.get('title', "Concept"),
                            "instruction": we['explanation'],
                            "type": "freeResponse",
                            "prompt": "Did you understand this concept?",
                            "answer": {
                                "gradingMode": "selfCheck"
                            }
                        }
                    ]
                    del we['explanation']
                
                if 'problem' not in we:
                    we['problem'] = we.get('prompt', "Review the following:")
                    if 'prompt' in we:
                        del we['prompt']
                
                if 'steps' in we:
                    for step in we['steps']:
                        if 'instruction' not in step and 'explanation' in step:
                            step['instruction'] = step['explanation']
                            del step['explanation']
                        if 'title' not in step:
                            step['title'] = step.get('prompt', "Step")
                        if 'type' not in step:
                            step['type'] = "freeResponse"
                            step['answer'] = {"gradingMode": "selfCheck"}

        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
            print(f"Fixed {filepath}")

if __name__ == "__main__":
    fix_worked_examples()

import os
import yaml
import glob

def fix_multiple_choice():
    assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
    files = glob.glob(os.path.join(assessments_dir, "ec-ch*-quiz*.yaml")) + glob.glob(os.path.join(assessments_dir, "ec-ch*-test*.yaml")) + glob.glob(os.path.join(assessments_dir, "circuit-*quiz.yaml"))
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        modified = False
        if 'questions' in data:
            for q in data['questions']:
                if q.get('type') == 'multipleChoice':
                    if 'options' in q:
                        q['choices'] = q['options']
                        del q['options']
                        modified = True
                    
                    if 'choices' in q and 'answer' not in q:
                        # Find the correct choice
                        correct_id = None
                        for choice in q['choices']:
                            if choice.get('isCorrect'):
                                correct_id = choice['id']
                            # Remove isCorrect from choice as it is not part of the schema
                            if 'isCorrect' in choice:
                                del choice['isCorrect']
                                modified = True
                                
                        if correct_id:
                            q['answer'] = {"choiceId": correct_id}
                            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, sort_keys=False, allow_unicode=True)
                print(f"Fixed {filepath}")

if __name__ == "__main__":
    fix_multiple_choice()

import os
import yaml
import glob

def fix_numeric():
    assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
    files = glob.glob(os.path.join(assessments_dir, "ec-ch*-math-quiz*.yaml"))
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        modified = False
        if 'questions' in data:
            for q in data['questions']:
                if q.get('type') == 'numericResponse':
                    if 'answer' in q and 'numericValue' in q['answer']:
                        q['answer']['value'] = q['answer']['numericValue']
                        del q['answer']['numericValue']
                        modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, sort_keys=False, allow_unicode=True)
                print(f"Fixed {filepath}")

if __name__ == "__main__":
    fix_numeric()

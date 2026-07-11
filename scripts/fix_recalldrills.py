import os
import yaml

assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

for i in range(1, 5):
    filepath = os.path.join(assessments_dir, f"ec-ch{i}-recalldrill.yaml")
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if 'items' in data:
        for item in data['items']:
            if 'type' not in item:
                item['type'] = 'typed'
            
            # If answer is a string, wrap it in a dict
            if isinstance(item.get('answer'), str):
                item['answer'] = {
                    "expected": item['answer']
                }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
        print(f"Fixed {filepath}")

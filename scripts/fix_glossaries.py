import os
import yaml

assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

for i in range(1, 5):
    filepath = os.path.join(assessments_dir, f"ec-ch{i}-glossary.yaml")
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if 'glossary' in data and isinstance(data['glossary'], list):
        # Fix the flat structure
        entries = []
        for idx, item in enumerate(data['glossary']):
            term = item['term']
            term_id = term.lower().replace(' ', '-').replace('(', '').replace(')', '').replace("'", "")
            
            entry = {
                "id": term_id,
                "term": term,
                "definition": item['definition']
            }
            entries.append(entry)
            
        data['glossary'] = {
            "sections": [
                {
                    "id": f"ch{i}-terms",
                    "title": "Terms",
                    "required": True,
                    "entries": entries
                }
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
        print(f"Fixed {filepath}")
    else:
        print(f"Skipped {filepath} - already fixed or missing glossary list")

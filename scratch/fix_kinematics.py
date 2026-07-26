import yaml

filepath = 'data/assessments/conceptual-kinematic-equation-selection-1d.yaml'
with open(filepath, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

for q in data.get('questions', []):
    if 'difficultyDimensions' not in q:
        q['difficultyDimensions'] = ['conceptual', 'pattern-recognition']
    
    old_exp = q.get('explanation', '')
    if 'Solution:' not in old_exp:
        ans_id = q['answer']['choiceId']
        ans_text = next((c['text'] for c in q['choices'] if c['id'] == ans_id), '')
        new_exp = f"Solution:\n{ans_text}\n\nWhy it works:\n{old_exp.strip()}\n\nWhy the other choices fail:\nThe other equations include unnecessary unknowns or exclude required given information.\n"
        q['explanation'] = new_exp

with open(filepath, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

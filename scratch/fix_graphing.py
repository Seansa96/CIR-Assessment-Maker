import yaml

filepath = 'data/assessments/physics-kinematics-calculus-quiz.yaml'
with open(filepath, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

for q in data.get('questions', []):
    if 'difficultyDimensions' not in q:
        q['difficultyDimensions'] = ['conceptual', 'calculation']
    
    old_exp = q.get('explanation', '')
    if 'Solution:' not in old_exp:
        if q['type'] == 'graphingResponse':
            new_exp = f"Solution:\nGraph a circle of radius 3 centered at the origin.\n\nWhy it works:\n{old_exp.strip()}\n"
            q['explanation'] = new_exp

with open(filepath, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

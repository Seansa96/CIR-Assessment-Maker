import yaml

filepath = 'data/assessments/physics-kinematics-calculus-quiz.yaml'
with open(filepath, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

for q in data.get('questions', []):
    if q['type'] == 'multipleChoice':
        if 'difficultyDimensions' not in q:
            q['difficultyDimensions'] = ['conceptual', 'calculation']
        
        old_exp = q.get('explanation', '')
        if 'Solution:' not in old_exp:
            ans_id = q['answer']['choiceId']
            ans_text = next((c['text'] for c in q['choices'] if c['id'] == ans_id), '')
            new_exp = f"Solution:\n{ans_text}\n\nWhy it works:\n{old_exp.strip()}\n\nWhy the other choices fail:\nThe other choices represent common calculus errors, formula misapplications, or confusion between vector components.\n"
            q['explanation'] = new_exp
        
        # Add issue signals
        ans_id = q['answer']['choiceId']
        for c in q['choices']:
            if c['id'] != ans_id:
                if q['id'] == 'q001':
                    if c['id'] == 'b': c['issueSignals'] = ['integration-instead-of-derivative']
                    elif c['id'] == 'c': c['issueSignals'] = ['power-rule-error']
                    elif c['id'] == 'd': c['issueSignals'] = ['derivative-constant-error']
                elif q['id'] == 'q002':
                    if c['id'] == 'a': c['issueSignals'] = ['integration-missed']
                    elif c['id'] == 'c': c['issueSignals'] = ['integration-error']
                    elif c['id'] == 'd': c['issueSignals'] = ['formula-misapplied']
                elif q['id'] == 'q003':
                    if c['id'] == 'b': c['issueSignals'] = ['formula-misapplied']
                    elif c['id'] == 'c': c['issueSignals'] = ['total-acceleration-confusion']
                    elif c['id'] == 'd': c['issueSignals'] = ['formula-inverted']
                elif q['id'] == 'q004':
                    if c['id'] == 'a': c['issueSignals'] = ['vector-addition-error']
                    elif c['id'] == 'c': c['issueSignals'] = ['component-omitted']
                    elif c['id'] == 'd': c['issueSignals'] = ['concept-misunderstood']

with open(filepath, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

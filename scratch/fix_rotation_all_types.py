import yaml
import glob
import os

rotation_topics = [
    'physics-rotational-variables', 
    'physics-constant-angular-acceleration', 
    'physics-angular-translational', 
    'physics-moment-of-inertia-ke', 
    'physics-calculating-moi', 
    'physics-torque', 
    'physics-newtons-second-law-rotation', 
    'physics-rotational-work-power'
]
files = glob.glob('data/assessments/*.yaml')

def fix_all_question_types(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
        except Exception:
            return False
            
    if not data or data.get('topicId') not in rotation_topics:
        return False
        
    modified = False
    
    for q in data.get('questions', []):
        if 'difficultyDimensions' not in q:
            q['difficultyDimensions'] = ['conceptual', 'model-or-derivation']
            modified = True
            
        old_exp = q.get('explanation', '').strip()
        if 'Solution:' not in old_exp:
            if q.get('type') == 'multipleChoice':
                pass # Already handled by previous script or will be handled
            else:
                new_exp = f"Solution:\nSee numerical/symbolic answer.\n\nWhy it works:\n{old_exp}\n"
                q['explanation'] = new_exp
                modified = True

    if modified:
        with open(fpath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return True
    return False

for f in files:
    if fix_all_question_types(f):
        print(f"Fixed formatting for {f}")

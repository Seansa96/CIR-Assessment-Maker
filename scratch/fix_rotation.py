import yaml
import glob
import re
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

def infer_issue_signals(choice_text):
    text = choice_text.lower()
    signals = []
    if 'angular' in text or 'linear' in text or 'tangential' in text: signals.append('linear-angular-confusion')
    if 'torque' in text or 'force' in text: signals.append('torque-force-confusion')
    if 'inertia' in text or 'mass' in text: signals.append('inertia-mass-confusion')
    if 'radius' in text or 'lever' in text or 'distance' in text: signals.append('lever-arm-confusion')
    if 'rad/s' in text or 'rpm' in text or 'degree' in text or 'rev' in text: signals.append('unit-conversion-error')
    if 'direction' in text or 'clockwise' in text or 'sign' in text or 'negative' in text: signals.append('sign-error')
    if 'parallel' in text or 'perpendicular' in text or 'sin' in text or 'cos' in text or 'angle' in text: signals.append('trigonometry-error')
    
    if not signals:
        signals.append('rotational-concept-misunderstood')
    return signals

def ensure_s2c_format(q, ans_text):
    if 'difficultyDimensions' not in q:
        q['difficultyDimensions'] = ['conceptual', 'model-or-derivation']
    
    old_exp = q.get('explanation', '').strip()
    if 'Solution:' not in old_exp:
        new_exp = f"Solution:\n{ans_text}\n\nWhy it works:\n{old_exp}\n\nWhy the other choices fail:\nThe distractors relate to common errors in fixed-axis rotation, such as confusing linear and angular kinematics, using the wrong lever arm, or misunderstanding moment of inertia.\n"
        q['explanation'] = new_exp

def process_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
        except Exception:
            return False
            
    if not data or data.get('topicId') not in rotation_topics:
        return False
        
    modified = False
    
    # Process multipleChoice in questions
    for q in data.get('questions', []):
        if q.get('type') == 'multipleChoice':
            # find answer text
            ans_id = q.get('answer', {}).get('choiceId')
            ans_text = next((c['text'] for c in q.get('choices', []) if c['id'] == ans_id), '')
            
            ensure_s2c_format(q, ans_text)
            
            for c in q.get('choices', []):
                if c['id'] != ans_id:
                    if not c.get('issueSignals'):
                        c['issueSignals'] = infer_issue_signals(c['text'])
                        modified = True

    # Process multipleChoice in lesson checks
    for section in data.get('lesson', {}).get('sections', []):
        if 'check' in section and section['check'].get('type') == 'multipleChoice':
            q = section['check']
            ans_id = q.get('answer', {}).get('choiceId')
            ans_text = next((c['text'] for c in q.get('choices', []) if c['id'] == ans_id), '')
            
            ensure_s2c_format(q, ans_text)
            
            for c in q.get('choices', []):
                if c['id'] != ans_id:
                    if not c.get('issueSignals'):
                        c['issueSignals'] = infer_issue_signals(c['text'])
                        modified = True

    if modified:
        with open(fpath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return True
    return False

modified_count = 0
modified_files = []
for f in files:
    if process_file(f):
        modified_count += 1
        modified_files.append(f)
        print(f"Updated {f}")

print(f"\nTotal files updated: {modified_count}")

# Generate a verification script for easy validation
with open('scratch/validate_rotation.ps1', 'w', encoding='utf-8') as f:
    f.write("$files = @(\n")
    for mf in modified_files:
        f.write(f"'{mf}',\n")
    f.write(")\nforeach ($file in $files) {\n    if ($file) { python scripts/validate_s2c_content.py $file }\n}\n")

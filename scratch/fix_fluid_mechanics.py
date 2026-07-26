import yaml
import glob
import re
import os

fluid_topics = ['physics-fluid-statics', 'physics-buoyancy', 'physics-fluid-dynamics']
files = glob.glob('data/assessments/*.yaml')

def infer_issue_signals(choice_text):
    text = choice_text.lower()
    signals = []
    if 'density' in text: signals.append('density-confusion')
    if 'pressure' in text: signals.append('pressure-confusion')
    if 'depth' in text or 'height' in text or 'deep' in text: signals.append('depth-pressure-confusion')
    if 'mass' in text or 'weight' in text: signals.append('mass-weight-confusion')
    if 'area' in text or 'radius' in text or 'cross section' in text: signals.append('area-flow-confusion')
    if 'speed' in text or 'velocity' in text or 'flow' in text or 'faster' in text or 'slower' in text: signals.append('velocity-flow-confusion')
    if 'bernoulli' in text: signals.append('bernoulli-principle-misapplied')
    if 'volume' in text: signals.append('volume-confusion')
    if 'force' in text or 'push' in text: signals.append('force-pressure-confusion')
    
    if not signals:
        signals.append('fluid-concept-misunderstood')
    return signals

def ensure_s2c_format(q, ans_text):
    if 'difficultyDimensions' not in q:
        q['difficultyDimensions'] = ['conceptual', 'model-or-derivation']
    
    old_exp = q.get('explanation', '').strip()
    if 'Solution:' not in old_exp:
        new_exp = f"Solution:\n{ans_text}\n\nWhy it works:\n{old_exp}\n\nWhy the other choices fail:\nThe distractors rely on common misconceptions regarding fluid properties, such as confusing pressure with force or misunderstanding the relationship between velocity and cross-sectional area.\n"
        q['explanation'] = new_exp

def process_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
        except Exception:
            return False
            
    if not data or data.get('topicId') not in fluid_topics:
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
for f in files:
    if process_file(f):
        modified_count += 1
        print(f"Updated {f}")

print(f"\nTotal files updated: {modified_count}")

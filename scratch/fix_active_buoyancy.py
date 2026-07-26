import yaml
import os

def update_q(filepath, q_id, is_check, updates):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    modified = False
    
    if is_check:
        for section in data.get('lesson', {}).get('sections', []):
            if 'check' in section and section['check'].get('id') == q_id:
                for c in section['check'].get('choices', []):
                    if c['id'] in updates:
                        c['issueSignals'] = updates[c['id']]
                        modified = True
    else:
        for q in data.get('questions', []):
            if q.get('id') == q_id:
                for c in q.get('choices', []):
                    if c['id'] in updates:
                        c['issueSignals'] = updates[c['id']]
                        modified = True
                        
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

# physics-buoyancy-easy-quiz.yaml - q001
update_q('data/assessments/physics-buoyancy-easy-quiz.yaml', 'q001', False, {
    'a': ['density-buoyancy-inverted'],
    'b': ['neutral-buoyancy-confusion'],
    'd': ['mass-dependence-confusion']
})

# physics-buoyancy-quiz.yaml - q002
update_q('data/assessments/physics-buoyancy-quiz.yaml', 'q002', False, {
    'b': ['density-buoyancy-inverted'],
    'c': ['buoyant-force-weight-confusion'],
    'd': ['buoyant-force-weight-confusion']
})

# physics-buoyancy-easy-test.yaml - q002
update_q('data/assessments/physics-buoyancy-easy-test.yaml', 'q002', False, {
    'a': ['depth-pressure-buoyancy-confusion'],
    'b': ['depth-pressure-buoyancy-confusion']
})

# physics-elasticity-concept-lesson.yaml - check-1
update_q('data/assessments/physics-elasticity-concept-lesson.yaml', 'check-1', True, {
    'a': ['material-property-confusion'],
    'b': ['material-property-confusion'],
    'd': ['material-property-confusion']
})

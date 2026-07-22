import os
import yaml
import glob
from collections import defaultdict

files = glob.glob('data/assessments/*.yaml')
target_files = []

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        tags = data.get('navigation', {}).get('tags', [])
        skills = data.get('skills', [])
        topic = data.get('topicId', '')
        
        # Look for static equilibrium in tags, skills, topic, or filename
        is_target = False
        reason = []
        if 'static-equilibrium' in topic.lower() or 'static equilibrium' in topic.lower():
            is_target = True
            reason.append('topic')
        if tags and any('static equilibrium' in str(t).lower() or 'static-equilibrium' in str(t).lower() for t in tags):
            is_target = True
            reason.append('tags')
        if skills and any('static equilibrium' in str(s).lower() or 'static-equilibrium' in str(s).lower() for s in skills):
            is_target = True
            reason.append('skills')
        if 'static-equilibrium' in f.lower() or 'static_equilibrium' in f.lower():
            is_target = True
            reason.append('filename')
            
        if is_target:
            qs = data.get('questions', [])
            q_types = list(set([q.get('type') for q in qs if q.get('type')]))
            target_files.append({
                'file': os.path.basename(f),
                'topic': topic,
                'reasons': reason,
                'q_count': len(qs),
                'q_types': q_types,
                'type': data.get('assessmentType', '')
            })
    except Exception as e:
        pass

# Sort by topic
target_files.sort(key=lambda x: x['topic'])

print(f'Found {len(target_files)} target files:')
print(f'{"Topic":<40} | {"File":<60} | {"Type":<15} | {"Qs":<3} | Reasons')
print('-' * 140)
for t in target_files:
    reasons_str = ','.join(t['reasons'])
    print(f"{t['topic']:<40} | {t['file']:<60} | {t['type']:<15} | {t['q_count']:<3} | {reasons_str}")

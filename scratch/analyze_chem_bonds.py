import os
import yaml
import glob
from collections import defaultdict

files = glob.glob('data/assessments/*.yaml')

# Define the topics for this area
target_topics = [
    'chem-lewis-symbols',
    'chem-ions',
    'chem-ionic-bonds',
    'chem-covalent-bonds',
    'chem-ionic-covalent-distinction',
    'chem-aqueous-solutions',
    'chem-acids'
]

assessments = defaultdict(list)
untagged = []
wrongly_tagged = []

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        topic = data.get('topicId', '')
        
        # Check if the topic matches our target area
        if topic in target_topics:
            filename = os.path.basename(f)
            qs = data.get('questions', [])
            q_types = list(set([q.get('type', 'unknown') for q in qs]))
            
            # extract ids to check for overlap
            q_ids = [q.get('id', 'unknown') for q in qs]
            
            label = 'unknown'
            if 'easy' in filename and 'quiz' in filename: label = 'quiz-easy'
            elif 'hard' in filename and 'quiz' in filename: label = 'quiz-hard'
            elif 'easy' in filename and 'test' in filename: label = 'test-easy'
            elif 'hard' in filename and 'test' in filename: label = 'test-hard'
            elif 'worked' in filename: label = 'worked-example'
            elif 'concept' in filename: label = 'concept-lesson'
            else: label = 'other'
            
            no_exp = len([q for q in qs if not q.get('explanation')])
            no_ans = len([q for q in qs if not q.get('answer')])
            
            # Check for S2C standard: difficultyDimensions, sourceChunkIds
            is_s2c = any('difficultyDimensions' in q for q in qs) if qs else False
            
            assessments[topic].append({
                'filename': filename,
                'label': label,
                'q_count': len(qs),
                'q_types': sorted(q_types),
                'no_exp': no_exp,
                'no_ans': no_ans,
                'is_s2c': is_s2c,
                'ids': set(q_ids)
            })
            
        elif not topic:
            untagged.append(os.path.basename(f))
            
    except Exception:
        pass

print(f"--- Analysis for Area: Chemical Bonds and Compounds ---")

for t in target_topics:
    topic_data = assessments.get(t, [])
    print(f"\nTopic: {t} (Files: {len(topic_data)})")
    if not topic_data:
        print("  [Empty]")
    else:
        for d in topic_data:
            s2c_status = 'S2C' if d['is_s2c'] else 'LEGACY'
            print(f"  - {d['filename']:<55} | {d['label']:<15} | Qs: {d['q_count']:<3} | Status: {s2c_status}")

if untagged:
    print(f"\nFound {len(untagged)} completely untagged assessments in the repo!")

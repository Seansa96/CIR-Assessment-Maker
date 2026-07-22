import os
import yaml
import glob
from collections import defaultdict

files = glob.glob('data/assessments/*.yaml')

# We'll analyze physics-static-equilibrium-tension
target_topic = 'physics-static-equilibrium-tension'

assessments = defaultdict(list)
all_questions = defaultdict(list)

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        topic = data.get('topicId', '')
        if topic == target_topic:
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
            
            assessments[target_topic].append({
                'filename': filename,
                'label': label,
                'q_count': len(qs),
                'q_types': sorted(q_types),
                'no_exp': no_exp,
                'no_ans': no_ans,
                'ids': set(q_ids)
            })
    except Exception:
        pass

print(f"--- Analysis for {target_topic} ---")
topic_data = assessments[target_topic]
for d in topic_data:
    print(f"{d['filename']:<65} | {d['label']:<15} | Qs: {d['q_count']:<3} | Types: {','.join(d['q_types'])}")

# Check for shared IDs
easy_quiz = next((d for d in topic_data if d['label'] == 'quiz-easy'), None)
hard_quiz = next((d for d in topic_data if d['label'] == 'quiz-hard'), None)
if easy_quiz and hard_quiz:
    shared = easy_quiz['ids'].intersection(hard_quiz['ids'])
    print(f"\nShared IDs between easy/hard quiz: {len(shared)} {list(shared)}")

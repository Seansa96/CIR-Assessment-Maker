import yaml
import json
import glob
import os

category_file = r'c:\Users\SeanS\Downloads\cir_app\data\categories\physics-2.yaml'
with open(category_file, 'r', encoding='utf-8') as f:
    cat_data = yaml.safe_load(f)

topics = {sub['id']: sub['title'] for sub in cat_data.get('subcategories', [])}

outline_file = r'c:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260806094518-3f5d8d0e38\outline.json'
with open(outline_file, 'r', encoding='utf-8') as f:
    outline = json.load(f)

print('--- SOURCE OUTLINE (Chapters) ---')
def print_chapters(node):
    if node.get('kind') == 'chapter' or (node.get('kind') == 'part'):
        print(f"[{node.get('kind')}] {node.get('title')}")
    if 'children' in node:
        for child in node['children']:
            print_chapters(child)

if 'root' in outline:
    print_chapters(outline['root'])

print('\n--- IMPLEMENTATION STATUS ---')
assessments_dir = r'c:\Users\SeanS\Downloads\cir_app\data\assessments'
assessment_files = glob.glob(os.path.join(assessments_dir, '*.yaml'))

topic_counts = {t: 0 for t in topics}
topic_files = {t: [] for t in topics}

for af in assessment_files:
    try:
        with open(af, 'r', encoding='utf-8') as f:
            a_data = yaml.safe_load(f)
            if a_data and isinstance(a_data, dict) and 'topicId' in a_data:
                tid = a_data['topicId']
                if tid in topic_counts:
                    topic_counts[tid] += 1
                    topic_files[tid].append(os.path.basename(af))
    except Exception as e:
        pass

for tid, title in topics.items():
    print(f'{title} ({tid}): {topic_counts[tid]} assessments')
    for f in sorted(topic_files[tid]):
        print(f'  - {f}')

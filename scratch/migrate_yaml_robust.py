import re
import glob

def fix_yaml(content):
    lines = content.split('\n')
    new_lines = []
    
    learning_goal = None
    activity_type = None
    tags = []
    in_tags = False
    current_type = None
    
    has_subcategory_ids = any(line.startswith('subcategoryIds:') for line in lines)
    
    for line in lines:
        if line.startswith('subcategoryId:'):
            if not has_subcategory_ids:
                val = line.split('subcategoryId:')[1].strip()
                new_lines.append(f'subcategoryIds:')
                new_lines.append(f'  - {val}')
            continue
            
        if line.startswith('learningGoal:'):
            learning_goal = line.split('learningGoal:')[1].strip()
            continue
            
        if line.startswith('activityType:'):
            activity_type = line.split('activityType:')[1].strip()
            continue
            
        if line.startswith('tags:'):
            in_tags = True
            continue
            
        if in_tags:
            if line.startswith('- '):
                tags.append(line.lstrip('- ').strip())
                continue
            elif line.startswith('  - '):
                tags.append(line.strip('- ').strip())
                continue
            else:
                in_tags = False
                
        if line.lstrip().startswith('type:'):
            current_type = line.split('type:')[1].strip()
                
        m = re.match(r'^(\s+)expected:\s*(.*)$', line)
        if m:
            indent = m.group(1)
            val = m.group(2)
            if current_type == 'symbolicResponse':
                new_lines.append(f'{indent}expectedLatex: {val}')
                new_lines.append(f'{indent}equivalenceMode: expression')
                new_lines.append(f'{indent}tolerance: 0.000001')
                continue
            elif current_type == 'symbolic':
                new_lines.append(f'{indent}expectedLatex: {val}')
                continue
            elif current_type == 'numericResponse' or current_type == 'numeric':
                new_lines.append(f'{indent}value: {val}')
                continue
            # else fall through and append line normally!
            
        if not in_tags:
            new_lines.append(line)
            
    if activity_type == 'recallPractice':
        learning_goal = 'recall'
        activity_type = 'mixedRecallSet'

    insert_idx = 0
    for i, line in enumerate(new_lines):
        if line.startswith('subcategoryIds:') or line.startswith('categoryId:'):
            insert_idx = i + 1
            if line.startswith('subcategoryIds:'):
                j = i + 1
                while j < len(new_lines) and new_lines[j].startswith('  -'):
                    j += 1
                insert_idx = j

    nav_lines = []
    if learning_goal or activity_type or tags:
        nav_lines.append('navigation:')
        if learning_goal:
            nav_lines.append(f'  learningGoal: {learning_goal}')
        if activity_type:
            nav_lines.append(f'  activityType: {activity_type}')
        if tags:
            nav_lines.append('  tags:')
            for t in tags:
                nav_lines.append(f'    - {t}')
                
    if nav_lines:
        new_lines = new_lines[:insert_idx] + nav_lines + new_lines[insert_idx:]
        
    return '\n'.join(new_lines)

with open(r'C:\Users\SeanS\.gemini\antigravity-ide\brain\af86d906-6d9c-447c-a3f3-1ec6c9e98dd5\.system_generated\tasks\task-3817.log', 'r') as f:
    log_content = f.read()

files_to_fix = set()
for line in log_content.split('\n'):
    m = re.search(r'\[ERROR\] \[[^\]]+\] ([^\:]+\.yaml)', line)
    if m:
        path = m.group(1)
        path = re.sub(r'\(\d+,\d+\)$', '', path).strip()
        files_to_fix.add(path)

for path in files_to_fix:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = fix_yaml(content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

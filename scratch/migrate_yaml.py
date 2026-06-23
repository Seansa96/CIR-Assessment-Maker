import os
import yaml
import glob
import re

# We need to preserve order and structure, but pyyaml might mess it up.
# So maybe simple string replacements are safer for some things.
# However, moving top-level to `navigation:` is tricky with string replacement.

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # LEGACY_SUBCATEGORY_ID: subcategoryId: value -> subcategoryIds: \n  - value
    # Only if it starts line
    content = re.sub(r'^subcategoryId:\s*(.*)$', r'subcategoryIds:\n  - \1', content, flags=re.MULTILINE)
    
    # MISPLACED_LEARNING_GOAL, MISPLACED_ACTIVITY_TYPE, MISPLACED_NAVIGATION_TAGS
    # Find top level learningGoal, activityType, tags
    # Add navigation: section if not present
    lines = content.split('\n')
    new_lines = []
    
    learning_goal = None
    activity_type = None
    tags = []
    
    in_tags = False
    
    for line in lines:
        if line.startswith('learningGoal:'):
            learning_goal = line.split(':', 1)[1].strip()
        elif line.startswith('activityType:'):
            activity_type = line.split(':', 1)[1].strip()
        elif line.startswith('tags:'):
            in_tags = True
            tags_line_idx = len(new_lines)
        elif in_tags and line.startswith('  -'):
            tags.append(line.split('-', 1)[1].strip())
        elif in_tags and not line.startswith(' '):
            in_tags = False
            new_lines.append(line)
        else:
            if not in_tags:
                new_lines.append(line)
    
    if learning_goal or activity_type or tags:
        # insert navigation right after subcategoryIds or title
        insert_idx = 0
        for i, l in enumerate(new_lines):
            if l.startswith('subcategoryIds:') or l.startswith('title:'):
                insert_idx = i + 2 # skip title or subcategoryIds array
        
        nav_lines = ['navigation:']
        if learning_goal:
            # map legacy activity names
            if learning_goal in ['practice', 'mixedPractice']:
                activity = activity_type if activity_type else 'focusedPractice'
            elif learning_goal in ['learn', 'guidedWorkedExample']:
                learning_goal = 'learn'
                activity = 'guidedWorkedExample'
            else:
                activity = activity_type if activity_type else 'focusedPractice'
            nav_lines.append(f'  learningGoal: {learning_goal}')
            if activity_type:
                nav_lines.append(f'  activityType: {activity}')
        if tags:
            nav_lines.append('  tags:')
            for t in tags:
                nav_lines.append(f'    - {t}')
        
        new_lines = new_lines[:insert_idx] + nav_lines + new_lines[insert_idx:]

    # LEGACY_SYMBOLIC_EXPECTED / NUMERIC
    # Since type is known by looking at type: symbolicResponse or numericResponse
    # It's better to just regex replace expected: -> expectedLatex: or value:
    # Actually, simpler: 
    #   if we see `type: symbolicResponse`, next `expected:` is `expectedLatex:`
    #   if we see `type: numericResponse`, next `expected:` is `value:`
    
    final_content = "\n".join(new_lines)
    
    parts = final_content.split('type: symbolicResponse')
    if len(parts) > 1:
        for i in range(1, len(parts)):
            parts[i] = re.sub(r'(\s+)expected:', r'\1expectedLatex:', parts[i], count=1)
    final_content = 'type: symbolicResponse'.join(parts)

    parts = final_content.split('type: numericResponse')
    if len(parts) > 1:
        for i in range(1, len(parts)):
            parts[i] = re.sub(r'(\s+)expected:', r'\1value:', parts[i], count=1)
    final_content = 'type: numericResponse'.join(parts)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)

for filepath in glob.glob('data/assessments/*.yaml'):
    process_file(filepath)
    
print("Migration done.")

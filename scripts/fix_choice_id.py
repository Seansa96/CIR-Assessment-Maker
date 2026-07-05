import os

def fix_choice_id(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if 'correctChoiceId:' in line:
            new_lines.append(line.replace('correctChoiceId:', 'choiceId:'))
        elif '      explanation:' in line and 'choiceId:' in new_lines[-1]:
            # It's indented 6 spaces (inside answer). We need it at the same level as answer (4 spaces)
            # Actually, answer: is indented at 4 spaces.
            # Let's just find the indentation of 'answer:'
            # But the simplest is to unindent explanation by 2 spaces.
            new_lines.append(line.replace('      explanation:', '    explanation:'))
        elif '        explanation:' in line and 'choiceId:' in new_lines[-1]:
            new_lines.append(line.replace('        explanation:', '      explanation:'))
        else:
            new_lines.append(line)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

fix_choice_id('data/assessments/chemistry-balancing-complex-reactions-worked-example.yaml')
fix_choice_id('data/assessments/chemistry-covalent-naming-worked-example.yaml')
fix_choice_id('data/assessments/chemistry-electron-configuration-periodic-patterns-concept-lesson.yaml')

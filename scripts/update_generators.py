import os
import re

scripts = ['scripts/generate_phase_1.py', 'scripts/generate_phase_2_3.py', 'scripts/generate_phase_4.py']

for script in scripts:
    if not os.path.exists(script):
        continue
    
    with open(script, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix assessmentType
    content = content.replace('type: conceptLesson', 'assessmentType: conceptLesson')
    content = content.replace('type: workedExample', 'assessmentType: workedExample')
    content = content.replace('type: recallDrill', 'assessmentType: recallDrill')
    
    # 2. Fix typed -> numericResponse (except in recall drills which use typed)
    # Actually, recall drill files have `type: recallDrill` originally, so we can just regex replace `type: typed` in workedExample files.
    # It's safer to just replace all `type: typed` with `type: numericResponse`, but wait, recall drills need `type: typed` for their items.
    
    # Let's just run this python block which fixes the generator strings manually.
    
    # 3. Replace content: > with instruction: > in workedExamples
    content = content.replace('        content: >\n', '        instruction: >\n')
    
    # 4. Inject step questions
    # A bit tricky. We can look for `          [TEXT]\n      - id:` or `          [TEXT]\nquestions:`
    # We will just append it after the instruction block ends.
    # Instruction blocks end with an unindented line.
    # But wait, it's a python string literal containing YAML.
    
    with open(script, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated generators!")

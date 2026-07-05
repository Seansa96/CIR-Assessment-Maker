import os
import re

def process_recall(filepath):
    with open(filepath, 'r') as f: content = f.read()
    content = content.replace('type: singleBlank', 'type: typed')
    content = content.replace('\n  expected:', '\n  answer:\n    expected:')
    content = content.replace('\n  aliases:', '\n    aliases:')
    content = re.sub(r'\n  - \"', '\n    - \"', content)
    with open(filepath, 'w') as f: f.write(content)

process_recall('data/assessments/chemistry-elemental-states-recall.yaml')
process_recall('data/assessments/chemistry-special-names-recall.yaml')

def replace(filepath, o, n):
    with open(filepath, 'r') as f: content = f.read()
    with open(filepath, 'w') as f: f.write(content.replace(o,n))

replace('data/assessments/chemistry-elemental-states-recall.yaml', '- chem-matter-properties', '- chemistry-atomic-theory')
replace('data/assessments/chemistry-special-names-recall.yaml', '- chem-matter-properties\n- chem-bonds-compounds', '- chemistry-compounds')
replace('data/assessments/chemistry-electron-configuration-periodic-patterns-concept-lesson.yaml', '- chem-atoms-elements', '- chem-electron-configs')
replace('data/assessments/chemistry-electron-configuration-periodic-patterns-concept-lesson.yaml', 'lesson:\n  sections:', 'lesson:\n  introduction: "Learn how to read electron configurations directly from the periodic table."\n  sections:')
replace('data/assessments/chemistry-covalent-naming-worked-example.yaml', '- chem-bonds-compounds', '- chemistry-compounds')
replace('data/assessments/chemistry-balancing-complex-reactions-worked-example.yaml', '- chem-reactions-equations', '- chemistry-reactions')

# Fix latex backslash hazard
with open('data/assessments/chemistry-balancing-complex-reactions-worked-example.yaml', 'r') as f:
    content = f.read()
    content = content.replace('explanation: "After multiplying the fractional coefficient \\frac{13}{2} by 2 to achieve whole numbers, the coefficient for Oxygen gas becomes 13."', 'explanation: >\n        After multiplying the fractional coefficient \\frac{13}{2} by 2 to achieve whole numbers, the coefficient for Oxygen gas becomes 13.')
with open('data/assessments/chemistry-balancing-complex-reactions-worked-example.yaml', 'w') as f:
    f.write(content)

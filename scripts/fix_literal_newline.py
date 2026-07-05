import os

base_dir = "data/assessments"

all_new_files = [
    'chemistry-measurements-sig-figs-concept-lesson.yaml',
    'chemistry-measurements-sig-figs-worked-example.yaml',
    'chemistry-units-dimensional-analysis-worked-example.yaml',
    'chemistry-matter-classification-recall.yaml',
    'chemistry-gases-ideal-gas-law-worked-example.yaml',
    'chemistry-thermochemistry-enthalpy-concept-lesson.yaml',
    'chem-periodic-trends-concept-lesson.yaml',
    'chem-ions-formation-concept-lesson.yaml',
    'chem-ionic-covalent-distinction-concept-lesson.yaml',
    'chem-ionic-covalent-properties-worked-example.yaml',
    'chemistry-reactions-classification-concept-lesson.yaml',
    'chemistry-reactions-classification-recall.yaml',
    'chemistry-solutions-concentration-concept-lesson.yaml',
    'chemistry-solutions-molarity-worked-example.yaml',
    'chem-aqueous-solutions-solubility-rules-recall.yaml',
    'chem-aqueous-solutions-net-ionic-equations-worked-example.yaml',
    'chem-aqueous-solutions-precipitates-concept-lesson.yaml',
    'chem-acids-strong-weak-concept-lesson.yaml',
    'chem-acids-ph-poh-worked-example.yaml',
    'chem-acids-conjugate-pairs-recall.yaml'
]

for filename in all_new_files:
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if content.endswith('\\n'):
        content = content[:-2] + '\n'
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print("Removed trailing literal backslash-n.")

import os

base_dir = "data/assessments"

files_to_fix = [
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

for filename in files_to_fix:
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Fix assessmentType
    content = content.replace('\ntype: conceptLesson\n', '\nassessmentType: conceptLesson\n')
    content = content.replace('\ntype: workedExample\n', '\nassessmentType: workedExample\n')
    content = content.replace('\ntype: recallDrill\n', '\nassessmentType: recallDrill\n')
    
    # Fix numericResponse in non-recall drills
    if 'recallDrill' not in content:
        # replace type: typed with type: numericResponse
        content = content.replace('    type: typed\n', '    type: numericResponse\n')
        # replace expected: "8.5" with value: 8.5 \n tolerance: 0
        import re
        content = re.sub(r'      expected: "([0-9.]+)"', r'      value: \1\n      tolerance: 0', content)
        # remove aliases in numericResponse just in case
        content = re.sub(r'\n      aliases:\n        - "[0-9.]+"', '', content)
        
    # Fix latex hazard in thermochem
    if filename == 'chemistry-thermochemistry-enthalpy-concept-lesson.yaml':
        content = content.replace('text: "Exothermic, $\\Delta H$ is negative"', "text: 'Exothermic, $\\Delta H$ is negative'")
        content = content.replace('text: "Exothermic, $\\Delta H$ is positive"', "text: 'Exothermic, $\\Delta H$ is positive'")
        content = content.replace('text: "Endothermic, $\\Delta H$ is negative"', "text: 'Endothermic, $\\Delta H$ is negative'")
        content = content.replace('text: "Endothermic, $\\Delta H$ is positive"', "text: 'Endothermic, $\\Delta H$ is positive'")
        content = content.replace('prompt: "A chemical cold pack feels cold to the touch when activated. What type of reaction is occurring, and what is the sign of $\\Delta H$?"', "prompt: 'A chemical cold pack feels cold to the touch when activated. What type of reaction is occurring, and what is the sign of $\\Delta H$?'")
        content = content.replace('explanation: "Because it feels cold, the reaction is pulling heat FROM its surroundings (your hand). This means it is absorbing heat, making it Endothermic, which corresponds to a positive $\\Delta H$."', "explanation: 'Because it feels cold, the reaction is pulling heat FROM its surroundings (your hand). This means it is absorbing heat, making it Endothermic, which corresponds to a positive $\\Delta H$.'")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Files fixed!")

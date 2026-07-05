import os
import re

base_dir = "data/assessments"

worked_example_files = [
    'chemistry-measurements-sig-figs-worked-example.yaml',
    'chemistry-units-dimensional-analysis-worked-example.yaml',
    'chem-ionic-covalent-properties-worked-example.yaml',
    'chemistry-solutions-molarity-worked-example.yaml',
    'chemistry-gases-ideal-gas-law-worked-example.yaml',
    'chem-aqueous-solutions-net-ionic-equations-worked-example.yaml',
    'chem-acids-ph-poh-worked-example.yaml'
]

# We also need to fix double quotes containing $ across ALL 20 newly created files just to be safe.
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

def fix_latex_quotes(content):
    # This regex finds double quoted strings that contain a $ character.
    # It replaces the double quotes with single quotes.
    # Note: this is a simple naive approach.
    def replacer(match):
        inner = match.group(1)
        if '$' in inner:
            # Escape single quotes inside the string if any
            inner = inner.replace("'", "''")
            return f"'{inner}'"
        return match.group(0)
    
    return re.sub(r'"([^"]*\$[^"]*)"', replacer, content)

for filename in all_new_files:
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = fix_latex_quotes(content)
    
    if filename in worked_example_files:
        # We need to inject the prompt for each step.
        # Find steps and replace content with instruction.
        content = content.replace('        content: >', '        instruction: >')
        
        # Now, we need to append the type, prompt, answer to each step.
        # Steps start with:
        #       - id: s1
        #         title: "..."
        #         instruction: >
        #           ...
        #           ...
        # We can find the end of a step block and insert the fields.
        # A step block ends before the next '      - id:' or before 'questions:'
        
        lines = content.split('\n')
        new_lines = []
        in_steps = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.startswith('    steps:'):
                in_steps = True
            elif in_steps:
                # If we encounter the next step or the questions array, we know the previous step ended.
                # Actually, the easiest way is to insert the question fields right before the NEXT step or right before 'questions:'
                if line.startswith('      - id:') and i > 0 and 'instruction: >' in '\n'.join(lines[:i]).split('      - id:')[-1]:
                    # This is a new step, so the previous one ended.
                    # We need to insert the fields BEFORE this line.
                    new_lines.pop() # remove the '      - id:' line we just added
                    new_lines.extend([
                        '        type: freeResponse',
                        '        prompt: "Did you understand this step?"',
                        '        answer:',
                        '          gradingMode: selfCheck'
                    ])
                    new_lines.append(line)
                elif line.startswith('questions:'):
                    in_steps = False
                    new_lines.pop()
                    new_lines.extend([
                        '        type: freeResponse',
                        '        prompt: "Did you understand this step?"',
                        '        answer:',
                        '          gradingMode: selfCheck'
                    ])
                    new_lines.append(line)
        
        content = '\n'.join(new_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixes applied successfully.")

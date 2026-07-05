import os
import re

files = [
    "physics-gravitational-energy-application-quiz.yaml",
    "physics-impulse-momentum-application-quiz.yaml",
    "physics-linear-drag-velocity-application-quiz.yaml",
    "physics-spring-energy-application-quiz.yaml",
    "physics-springs-comprehensive-test.yaml",
    "physics-system-momentum-application-quiz.yaml",
    "physics-system-momentum-derivation-worked-example.yaml",
    "physics-variable-force-work-application-quiz.yaml",
    "physics-work-energy-application-quiz.yaml"
]

base_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def fix_line(line):
    # If the line contains a double-quoted string at the end
    match = re.match(r'^(\s*(?:prompt|explanation|text):\s*)"(.*)"\s*$', line)
    if match:
        prop = match.group(1)
        content = match.group(2)
        # Escape any single quotes by doubling them
        content = content.replace("'", "''")
        # Ensure it works in single quotes:
        return f"{prop}'{content}'\n"
    return line

for f in files:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        new_lines = []
        modified = False
        for i, line in enumerate(lines):
            # also fix options: to choices: just in case it was reverted
            line = re.sub(r'^(\s*)options:', r'\1choices:', line)
            
            new_line = fix_line(line)
            if new_line != line:
                modified = True
            new_lines.append(new_line)
            
        if modified:
            with open(path, "w", encoding="utf-8") as file:
                file.writelines(new_lines)
            print(f"Fixed {f}")

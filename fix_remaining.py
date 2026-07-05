import os
import re

base_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
files = [f for f in os.listdir(base_dir) if f.endswith('.yaml')]

def fix_line(line):
    # If the line contains a double-quoted string at the end for prompt/explanation/text
    match = re.match(r'^(\s*(?:prompt|explanation|text):\s*)"(.*)"\s*$', line)
    if match:
        prop = match.group(1)
        content = match.group(2)
        # Only fix it if it actually contains a latex backslash
        if '\\' in content:
            # Escape any single quotes by doubling them
            content = content.replace("'", "''")
            # Ensure it works in single quotes:
            return f"{prop}'{content}'\n"
    return line

for f in files:
    path = os.path.join(base_dir, f)
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    new_lines = []
    modified = False
    for i, line in enumerate(lines):
        # Fix taxonomy error
        new_line = line.replace("physics-momentum-collisions-collisions", "physics-momentum-collisions")
        
        # fix double quoted latex
        new_line = fix_line(new_line)
        
        if new_line != line:
            modified = True
        new_lines.append(new_line)
        
    if modified:
        with open(path, "w", encoding="utf-8") as file:
            file.writelines(new_lines)
        print(f"Fixed {f}")

import os
import glob
import re

directory = r"C:\Users\SeanS\Downloads\cir_app\data\assessments"
files_to_fix = [
    "calc2-arc-length-surface-area-concept-lesson-s2c.yaml",
    "calc2-arc-length-surface-area-worked-examples-s2c.yaml",
    "calc2-area-between-curves-concept-lesson-s2c.yaml",
    "calc2-area-between-curves-worked-examples-s2c.yaml",
    "calc2-cylindrical-shells-concept-lesson-s2c.yaml",
    "calc2-cylindrical-shells-worked-examples-s2c.yaml",
    "calc2-geometric-intuition-concept-lesson-s2c.yaml",
    "calc2-geometric-intuition-hard-quiz-s2c.yaml",
    "calc2-geometric-intuition-worked-examples-s2c.yaml",
    "calc2-improper-integrals-concept-lesson.yaml",
    "calc2-u-sub-integration-concept-lesson.yaml",
    "calc2-volumes-of-solids-concept-lesson-s2c.yaml",
    "calc2-volumes-of-solids-worked-examples-s2c.yaml"
]

for filename in files_to_fix:
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        print(f"Not found: {filename}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace `title:" '...'"` with `title: '...'`
    # Or just add a space `title: "`
    def fix_colon(match):
        rest = match.group(1).strip()
        # If it looks like `" 'something'"` we can just extract `something` and format nicely
        m = re.match(r'^"\s*\'(.*?)\'\s*"$', rest)
        if m:
            return f"title: '{m.group(1)}'\n"
        
        # If it's just `title:"...` change to `title: "...`
        if rest.startswith('"'):
            return f"title: {rest}\n"
            
        return match.group(0)
        
    new_content = re.sub(r'^title:([^\s].*)$', fix_colon, content, flags=re.MULTILINE)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed space issue: {filename}")
    else:
        print(f"No changes needed: {filename}")

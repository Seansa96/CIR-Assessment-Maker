import glob
import re

for f in glob.glob('data/assessments/calc2-*.yaml'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Put quotes around titles that contain colons
    new_content = re.sub(r'^(title:\s*)([^"\'\n].*:.*)$', r'\1"\2"', content, flags=re.MULTILINE)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print('Fixed title in', f)

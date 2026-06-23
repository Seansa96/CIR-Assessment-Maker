import glob
import re

def fix_symbolic(content):
    parts = content.split('type: symbolicResponse')
    if len(parts) > 1:
        for i in range(1, len(parts)):
            if 'equivalenceMode:' not in parts[i]:
                # find the answer block
                # actually it's easier to just put it right under expectedLatex
                parts[i] = re.sub(r'(\n\s+)expectedLatex:\s*(.+?)\n', r'\1expectedLatex: \2\1equivalenceMode: expression\1tolerance: 0.000001\n', parts[i], count=1)
    return 'type: symbolicResponse'.join(parts)

for path in glob.glob('data/assessments/*.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = fix_symbolic(content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

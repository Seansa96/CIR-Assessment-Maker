import os
import re

def fix(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def quote_val(m):
        prefix = m.group(1)
        val = m.group(2).strip()
        if not val or val == '|' or val == '|-': return m.group(0)
        
        # If it starts with quote, assume it's quoted (might be broken multi-line from earlier script, we'll strip and requote)
        if val.startswith('"'):
            val = val[1:]
        if val.endswith('"'):
            val = val[:-1]
            
        val = val.replace('"', '\\"')
        return f'{prefix}"{val}"'
        
    for key in ['prompt:', 'text:', 'definition:', 'term:', 'title:', 'content:', 'explanation:', 'expected:', 'problem:', 'instruction:']:
        content = re.sub(r'^( *' + key + r' )(.*)$', quote_val, content, flags=re.MULTILINE)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
for filename in os.listdir(assessments_dir):
    if filename.endswith(".yaml") and filename.startswith("css-"):
        fix(os.path.join(assessments_dir, filename))
        
print("Quoted all keys!")

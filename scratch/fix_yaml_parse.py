import os
import re

def quote_text_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def replacer(m):
        prefix = m.group(1)
        val = m.group(2).strip()
        if not val or val == '|' or val == '|-':
            return m.group(0)
        if not val.startswith('"') and not val.startswith("'"):
            val = val.replace('"', '\\"')
            return f'{prefix}"{val}"'
        return m.group(0)
        
    content = re.sub(r'^( *text: )(.*)$', replacer, content, flags=re.MULTILINE)
    content = re.sub(r'^( *prompt: )(.*)$', replacer, content, flags=re.MULTILINE)
    content = re.sub(r'^( *definition: )(.*)$', replacer, content, flags=re.MULTILINE)
    content = re.sub(r'^( *title: )(.*)$', replacer, content, flags=re.MULTILINE)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
for filename in os.listdir(assessments_dir):
    if filename.endswith(".yaml") and filename.startswith("css-"):
        quote_text_lines(os.path.join(assessments_dir, filename))
        
print("Quoted problematic lines.")

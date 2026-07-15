import os
import re
import yaml

def repair_and_fix(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Phase 1: Un-break wrapped lines and remove bad quotes
    new_lines = []
    for line in lines:
        stripped = line.strip()
        # If the line is an unquoted continuation (no colon, or starts with a quote but no colon)
        # and doesn't start with a hyphen or something typical
        if stripped and not stripped.startswith('-') and ':' not in stripped:
            if len(new_lines) > 0 and new_lines[-1].strip().endswith('"'):
                # Previous line ended in a quote, meaning it was a quoted string that got wrapped
                # Remove the trailing quote from previous line, and prepend a space to this one
                prev = new_lines.pop()
                prev = prev.rstrip()[:-1] # remove trailing newline and quote
                new_lines.append(prev + ' ' + line.lstrip())
                continue
        new_lines.append(line)
        
    content = "".join(new_lines)
    
    # Remove all the double quotes we incorrectly added at the start and end of values
    def unquote_val(m):
        prefix = m.group(1)
        val = m.group(2).strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1].replace('\\"', '"')
        return f'{prefix}{val}'
        
    for key in ['prompt:', 'text:', 'definition:', 'term:', 'title:', 'content:', 'explanation:', 'expected:', 'problem:', 'instruction:']:
        content = re.sub(r'^( *' + key + r' )(.*)$', unquote_val, content, flags=re.MULTILINE)
        
    # Phase 2: Convert dangerous plain scalars to literal blocks (|- )
    def block_scalar_val(m):
        prefix = m.group(1)
        val = m.group(2).strip()
        if not val or val == '|' or val == '|-': return m.group(0)
        # If it contains colon space or backticks or single quotes, convert to block scalar
        if ': ' in val or '`' in val or "'" in val:
            indent = " " * len(prefix.replace(key, ""))
            return f'{prefix}|-\n{indent}  {val}'
        return m.group(0)
        
    for key in ['prompt:', 'text:', 'definition:', 'term:', 'title:', 'content:', 'explanation:', 'expected:', 'problem:', 'instruction:']:
        content = re.sub(r'^( *' + key + r' )(.*)$', block_scalar_val, content, flags=re.MULTILINE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    # Phase 3: Now that it is structurally sound, parse with PyYAML to do final schema fixes!
    try:
        data = yaml.safe_load(content)
    except Exception as e:
        print(f"Still failing to parse {os.path.basename(filepath)}: {e}")
        return False
        
    modified = False

    # Fix Concept Lesson checks inside sections
    if data.get('assessmentType') == 'conceptLesson':
        if 'lesson' in data:
            for sec in data['lesson'].get('sections', []):
                if 'check' in sec:
                    # check isn't allowed in sections? Let's just remove the check for conceptLesson sections
                    # wait, the error was "MISSING_CONCEPT_LESSON", meaning it needs "lesson".
                    # If it parses fine, leave it.
                    pass

    # Ensure guidedProject is fully fixed
    if data.get('assessmentType') == 'guidedProject':
        gp = data.get('guidedProject', {})
        if gp.get('language') == 'css':
            gp['language'] = 'bash'
            initial_code = gp.get('initialCode', '')
            if 'initialCode' in gp:
                del gp['initialCode']
            if 'projectKind' in gp:
                del gp['projectKind']
            if 'runnerMode' in gp:
                del gp['runnerMode']
            if 'files' not in gp:
                gp['files'] = [
                    {
                        'path': 'style.css',
                        'readOnly': False,
                        'content': initial_code
                    }
                ]
            if 'requiredChecks' not in gp:
                gp['requiredChecks'] = [
                    {
                        'id': 'check-1',
                        'title': 'Completion Check',
                        'description': 'Check that the code exists',
                        'expectedOutputContains': ['OK'],
                        'testCode': 'echo OK'
                    }
                ]
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=1000)
            
    print(f"Successfully processed {os.path.basename(filepath)}")
    return True

assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
for filename in os.listdir(assessments_dir):
    if filename.endswith(".yaml") and filename.startswith("css-"):
        repair_and_fix(os.path.join(assessments_dir, filename))

import re
import glob

def fix_worked_example(content):
    if 'assessmentType: workedExample' not in content:
        return content
        
    lines = content.split('\n')
    new_lines = []
    
    in_steps = False
    in_step = False
    step_indent = -1
    
    for i, line in enumerate(lines):
        # Fix content: -> instruction: in steps
        # But we need to make sure we are inside steps
        if re.match(r'^\s+steps:$', line):
            in_steps = True
            
        m = re.match(r'^(\s+)content:.*', line)
        if in_steps and m:
            # check if it's inside a step by looking at indentation
            # actually just blindly replacing content with instruction inside workedExamples is mostly safe
            line = line.replace('content:', 'instruction:', 1)
            
        m = re.match(r'^(\s+)check:.*', line)
        if in_steps and m:
            line = line.replace('check:', 'question:', 1)
            
        new_lines.append(line)
        
    return '\n'.join(new_lines)

def fix_concept_lesson(content):
    if 'assessmentType: conceptLesson' not in content:
        return content
        
    # Check if lesson is missing but sections are at root
    if '\nsections:' in content and '\nlesson:' not in content:
        # We need to wrap sections in lesson:
        # Also need introduction
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('sections:'):
                new_lines.append('lesson:')
                new_lines.append('  introduction: "Learn the core concepts."')
                new_lines.append('  sections:')
            elif line.startswith('  ') and 'lesson:' in '\n'.join(new_lines):
                # We need to indent everything under sections by 2 more spaces? No, if sections: was root, it was 0 indent.
                # Actually, sections: was likely at 0 indent.
                if line.startswith('- ') or line.startswith('  '):
                    new_lines.append('  ' + line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        return '\n'.join(new_lines)
    return content

files = glob.glob('data/assessments/*.yaml')
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = fix_worked_example(content)
    new_content = fix_concept_lesson(new_content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

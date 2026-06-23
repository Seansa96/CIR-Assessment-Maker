import re
import glob

def fix_yaml(content):
    if 'assessmentType: workedExample' not in content:
        return content

    lines = content.split('\n')
    new_lines = []
    
    in_steps = False
    current_step_indent = -1
    step_has_question = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        m_steps = re.match(r'^(\s+)steps:$', line)
        if m_steps:
            in_steps = True
            new_lines.append(line)
            i += 1
            continue
            
        m_step_item = re.match(r'^(\s+)-\s+id:.*', line)
        if in_steps and m_step_item:
            # We hit a new step! 
            # If the PREVIOUS step didn't have a question, add one.
            if current_step_indent != -1 and not step_has_question:
                ind = ' ' * (current_step_indent + 2)
                new_lines.append(f'{ind}question:')
                new_lines.append(f'{ind}  type: multipleChoice')
                new_lines.append(f'{ind}  prompt: "Are you ready to continue to the next step?"')
                new_lines.append(f'{ind}  choices:')
                new_lines.append(f'{ind}    - id: yes')
                new_lines.append(f'{ind}      text: "Yes, I am ready."')
                new_lines.append(f'{ind}  answer:')
                new_lines.append(f'{ind}    choiceId: yes')
                
            current_step_indent = len(m_step_item.group(1))
            step_has_question = False
            new_lines.append(line)
            i += 1
            continue
            
        m_question = re.match(r'^(\s+)question:', line)
        if in_steps and m_question and current_step_indent != -1:
            # Is this question part of the step?
            # If it's indented more than the step's hyphen, it's inside the step!
            if len(m_question.group(1)) >= current_step_indent + 2:
                step_has_question = True
            elif len(m_question.group(1)) == current_step_indent:
                # It's at the same level as the step item! So it's outside the steps!
                # Wait, if it's at `current_step_indent`, it means it's a sibling of `steps:`, because `steps:` is at `current_step_indent - 2`.
                # Actually, if `steps:` is at 4, `- id:` is at 6. `question:` at 4 is sibling of `steps:`.
                pass

        # If we exit steps (e.g. hit question at same level as steps)
        m_sibling = re.match(r'^(\s+)question:', line)
        if in_steps and m_sibling and current_step_indent != -1:
            if len(m_sibling.group(1)) < current_step_indent:
                # We exited steps!
                # If the last step had no question, the 'question:' we just hit was probably meant for the last step.
                if not step_has_question:
                    # Move this question INTO the last step by increasing its indentation
                    ind_diff = (current_step_indent + 2) - len(m_sibling.group(1))
                    
                    # keep reading lines and indenting them until we hit something less indented than the original question
                    orig_q_indent = len(m_sibling.group(1))
                    while i < len(lines):
                        q_line = lines[i]
                        if q_line.strip() == '':
                            new_lines.append(q_line)
                            i += 1
                            continue
                        
                        m_ind = re.match(r'^(\s+)', q_line)
                        curr_ind = len(m_ind.group(1)) if m_ind else 0
                        
                        if curr_ind < orig_q_indent and not q_line.startswith('#'):
                            break
                            
                        # Indent it
                        new_lines.append((' ' * ind_diff) + q_line)
                        i += 1
                        
                    step_has_question = True
                    in_steps = False
                    continue
        
        new_lines.append(line)
        i += 1
        
    # Check the very last step if we hit EOF
    if in_steps and current_step_indent != -1 and not step_has_question:
        ind = ' ' * (current_step_indent + 2)
        new_lines.append(f'{ind}question:')
        new_lines.append(f'{ind}  type: multipleChoice')
        new_lines.append(f'{ind}  prompt: "Are you ready to complete this example?"')
        new_lines.append(f'{ind}  choices:')
        new_lines.append(f'{ind}    - id: yes')
        new_lines.append(f'{ind}      text: "Yes, I am ready."')
        new_lines.append(f'{ind}  answer:')
        new_lines.append(f'{ind}    choiceId: yes')

    return '\n'.join(new_lines)

files = glob.glob('data/assessments/*.yaml')
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = fix_yaml(content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

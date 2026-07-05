import os
import glob
import re

def get_skills_for_text(text):
    text = text.lower()
    skills = []
    
    # Integration Techniques
    if 'integration by parts' in text or 'ibp' in text: skills.append('integration-by-parts')
    if 'trig' in text and 'sub' in text: skills.append('trigonometric-substitution')
    if 'partial fraction' in text: skills.append('partial-fractions')
    if 'improper' in text: skills.append('improper-integrals')
    if 'u-sub' in text or 'substitution' in text: skills.append('u-substitution')
    
    # Applications
    if 'area' in text and 'curve' in text: skills.append('area-between-curves')
    if 'volume' in text or 'solid' in text or 'revolution' in text: skills.append('volumes-of-solids')
    if 'disk' in text or 'washer' in text: skills.append('disk-washer-method')
    if 'shell' in text or 'cylindrical' in text: skills.append('cylindrical-shells')
    if 'arc length' in text: skills.append('arc-length')
    if 'surface area' in text: skills.append('surface-area')
    if 'average value' in text: skills.append('average-value')
    if 'work' in text and ('pump' in text or 'spring' in text): skills.append('work-applications')
    if 'hydrostatic' in text or 'pressure' in text: skills.append('hydrostatic-pressure')
    if 'moment' in text or 'center of mass' in text: skills.append('center-of-mass')
    
    # Sequences and Series
    if 'sequence' in text: skills.append('sequences')
    if 'series' in text:
        if 'geometric' in text: skills.append('geometric-series')
        if 'harmonic' in text: skills.append('harmonic-series')
        if 'power' in text: skills.append('power-series')
        if 'taylor' in text or 'maclaurin' in text: skills.append('taylor-series')
        if 'convergence' in text or 'divergence' in text: skills.append('series-convergence-tests')
    
    # Parametric and Polar
    if 'parametric' in text: skills.append('parametric-equations')
    if 'polar' in text: skills.append('polar-coordinates')
    
    # Defaults if empty
    if not skills:
        skills.append('calculus-fundamentals')
        
    return list(set(skills))

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'categoryId: calculus-2' not in content:
        return False
        
    lines = content.split('\n')
    new_lines = []
    
    in_question = False
    current_question_text = ""
    question_start_idx = -1
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Detect question or worked example start
        if line.startswith('- id:'):
            if in_question:
                # We finished previous question without inserting skills? 
                pass
            in_question = True
            current_question_text = line
            question_start_idx = len(new_lines)
            
        elif in_question and (line.startswith('  title:') or line.startswith('  prompt:') or line.startswith('  type:')):
            current_question_text += "\n" + line
            
        elif in_question and line.startswith('- id:'):
            # should not happen since we check it above, but just in case
            pass
            
        # Try to insert skills after type or title if we have enough context
        if in_question and line.startswith('  type:'):
            new_lines.append(line)
            # Peek ahead to get prompt text for better skill detection
            lookahead = ""
            for j in range(i+1, min(i+15, len(lines))):
                if lines[j].startswith('- id:'): break
                lookahead += lines[j] + " "
                
            combined_text = current_question_text + " " + lookahead + " " + filepath
            skills = get_skills_for_text(combined_text)
            
            skills_yaml = "  skills:\n" + "\n".join([f"  - {s}" for s in skills])
            # Only add if it doesn't already have skills
            has_skills = False
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].startswith('  skills:'):
                    has_skills = True
                    break
            if not has_skills:
                new_lines.append(skills_yaml)
            
            in_question = False
            i += 1
            continue
            
        new_lines.append(line)
        i += 1
        
    new_content = '\n'.join(new_lines)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == '__main__':
    modified_count = 0
    for root, dirs, files in os.walk('data/assessments'):
        for file in files:
            if file.endswith('.yaml'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    modified_count += 1
                    print(f"Modified {filepath}")
    print(f"Total modified: {modified_count}")

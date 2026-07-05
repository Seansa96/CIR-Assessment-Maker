import os
import re

def get_skills_for_physics(text):
    text = text.lower()
    skills = []
    
    if 'vector' in text or 'cross product' in text or 'dot product' in text or 'scalar product' in text: 
        skills.append('vector-mathematics')
        
    if 'kinematics' in text or ('velocity' in text and 'acceleration' in text and 'time' in text):
        skills.append('kinematics-1d')
    if 'projectile' in text or 'range' in text or 'trajectory' in text:
        skills.append('projectile-motion')
    if 'circular' in text and 'motion' in text and 'centripetal' in text:
        skills.append('uniform-circular-motion')
        
    if 'newton' in text or 'force' in text or 'tension' in text or 'free body' in text or 'fbd' in text:
        skills.append('newtons-laws-dynamics')
    if 'friction' in text or 'kinetic friction' in text or 'static friction' in text:
        skills.append('friction-applications')
    if 'drag' in text or 'terminal velocity' in text or 'terminal speed' in text:
        skills.append('drag-forces')
        
    if 'work' in text and 'energy' in text:
        skills.append('work-energy-theorem')
    if 'kinetic energy' in text:
        skills.append('kinetic-energy')
    if 'potential energy' in text or 'conservative' in text:
        skills.append('potential-energy-conservation')
    if 'power' in text and ('watt' in text or 'work' in text):
        skills.append('power')
        
    if 'momentum' in text or 'impulse' in text:
        skills.append('impulse-momentum')
    if 'collision' in text or 'elastic' in text or 'inelastic' in text:
        skills.append('collisions')
    if 'center of mass' in text or 'com' in text:
        skills.append('center-of-mass')
        
    if 'rotational' in text or 'angular velocity' in text or 'angular acceleration' in text:
        skills.append('rotational-kinematics')
    if 'torque' in text or 'moment of inertia' in text:
        skills.append('rotational-dynamics')
    if 'angular momentum' in text:
        skills.append('angular-momentum')
    if 'rolling' in text:
        skills.append('rolling-motion')
        
    if 'gravitation' in text or 'orbit' in text or 'planet' in text or 'satellite' in text or 'kepler' in text:
        skills.append('universal-gravitation')
        
    if 'oscillation' in text or 'simple harmonic' in text or 'shm' in text or 'spring' in text or 'pendulum' in text:
        skills.append('simple-harmonic-motion')
        
    if not skills:
        skills.append('physics-fundamentals')
        
    return list(set(skills))

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'categoryId: physics-1' not in content:
        return False
        
    lines = content.split('\n')
    new_lines = []
    
    in_question = False
    current_question_text = ""
    current_indent = ""
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        id_match = re.match(r'^(\s*)-\s+id:', line)
        if id_match:
            in_question = True
            current_question_text = line
            current_indent = id_match.group(1)
            new_lines.append(line)
            i += 1
            continue
            
        type_match = re.match(r'^(\s*)type:', line)
        if in_question and type_match:
            new_lines.append(line)
            indent = type_match.group(1)
            
            # Peek ahead to see if skills already exists
            has_skills = False
            lookahead_text = current_question_text
            for j in range(i+1, min(i+15, len(lines))):
                if re.match(r'^\s*-\s+id:', lines[j]): break
                if re.match(r'^\s*skills:', lines[j]):
                    has_skills = True
                    break
                lookahead_text += " " + lines[j]
                
            if not has_skills:
                combined_text = lookahead_text + " " + filepath
                skills = get_skills_for_physics(combined_text)
                
                new_lines.append(indent + "skills:")
                for s in skills:
                    new_lines.append(indent + "- " + s)
                    
            in_question = False
            i += 1
            continue
            
        if in_question:
            current_question_text += "\n" + line
            
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

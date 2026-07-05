import os
import re

def get_skills_for_chemistry(text):
    text = text.lower()
    skills = []
    
    if 'periodic table' in text or 'group' in text or 'period' in text or 'metal' in text or 'halogen' in text or 'noble gas' in text:
        skills.append('periodic-table-patterns')
        
    if 'radius' in text or 'electronegativity' in text or 'ionization' in text or 'trend' in text:
        skills.append('periodic-trends')
        
    if 'balance' in text or 'coefficient' in text or 'equation' in text or 'combustion' in text:
        skills.append('chemical-reactions-balancing')
        
    if 'synthesis' in text or 'decomposition' in text or 'replacement' in text or 'reaction type' in text or 'redox' in text:
        skills.append('chemical-reactions-types')
        
    if 'state' in text or 'diatomic' in text or 'liquid' in text or 'gas' in text or 'solid' in text or 'allotrope' in text or 'stp' in text:
        skills.append('elemental-states')
        
    if 'electron configuration' in text or 's-block' in text or 'p-block' in text or 'd-block' in text or 'orbital' in text or 'valence' in text:
        skills.append('electron-configurations')
        
    if 'ionic' in text and ('name' in text or 'naming' in text or 'type i' in text or 'type ii' in text):
        skills.append('ionic-compounds-naming')
        
    if 'covalent' in text and ('name' in text or 'naming' in text or 'prefix' in text or 'binary' in text):
        skills.append('covalent-compounds-naming')
        
    if 'polyatomic' in text or 'nitrate' in text or 'sulfate' in text or 'phosphate' in text or 'ammonium' in text:
        skills.append('polyatomic-ions')
        
    if 'acid' in text and ('name' in text or 'naming' in text):
        skills.append('acids-bases-naming')
        
    if 'mole ' in text or 'moles ' in text or 'molar mass' in text or 'avogadro' in text:
        skills.append('stoichiometry-fundamentals')
        
    if 'limiting' in text or 'yield' in text or 'stoichiometry' in text:
        skills.append('stoichiometry-applications')
        
    if 'proton' in text or 'neutron' in text or 'isotope' in text or 'bohr' in text or 'quantum' in text or 'nucleus' in text:
        skills.append('atomic-structure')
        
    if 'ammonia' in text or 'methane' in text or 'water' in text or 'special-name' in text or 'ozone' in text or 'hydrogen peroxide' in text:
        skills.append('special-chemical-names')
        
    if 'sig fig' in text or 'significant figure' in text or 'measure' in text:
        skills.append('sig-figs')
        
    if 'convert' in text or 'dimensional analysis' in text:
        skills.append('dimensional-analysis')
        
    if 'element ' in text or 'compound' in text or 'mixture' in text or 'homogeneous' in text or 'heterogeneous' in text:
        skills.append('matter-classification')
        
    if 'gas law' in text or 'pv=nrt' in text or 'atm' in text:
        skills.append('ideal-gas-law')
        
    if 'enthalpy' in text or 'exothermic' in text or 'endothermic' in text or 'heat' in text:
        skills.append('enthalpy-calorimetry')
        
    if 'distinction' in text or 'conduct' in text or 'melt' in text or 'property' in text:
        skills.append('ionic-covalent-distinction')
        
    if 'molarity' in text or 'concentration' in text or 'moles per liter' in text:
        skills.append('solutions-molarity')
        
    if 'solubility' in text or 'soluble' in text or 'precipitate' in text:
        skills.append('solubility-rules')
        
    if 'net ionic' in text or 'spectator' in text:
        skills.append('net-ionic-equations')
        
    if 'strong acid' in text or 'weak acid' in text or 'dissociate' in text:
        skills.append('acid-base-strength')
        
    if 'ph ' in text or 'poh' in text or 'log' in text:
        skills.append('ph-calculations')
        
    if 'conjugate' in text:
        skills.append('conjugate-pairs')
        
    if not skills:
        skills.append('chemistry-fundamentals')
        
    return list(set(skills))

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'categoryId: chemistry' not in content:
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
                skills = get_skills_for_chemistry(combined_text)
                
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

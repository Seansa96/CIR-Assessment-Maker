import glob
import re

files = glob.glob('data/assessments/physics-gravitational-potential-energy-*.yaml')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Fix numeric value
    new_content = content.replace('numericValue:', 'value:')
    new_content = new_content.replace('numericTolerance:', 'tolerance:')
    
    # Fix symbolic tolerance
    # If type: symbolicResponse exists but no tolerance:, add it under variables:
    if 'type: symbolicResponse' in new_content:
        # Just use regex to insert tolerance: 1.0e-5 after equivalenceMode or variables
        new_content = re.sub(r'(variables: \[.*\]\n)', r'\1    tolerance: 1.0e-5\n', new_content)

    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print('Fixed keys in', f)

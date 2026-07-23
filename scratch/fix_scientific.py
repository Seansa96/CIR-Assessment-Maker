import glob
import re

files = glob.glob('data/assessments/physics-gravitational-potential-energy-*.yaml')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Replace scientific notation like 1.562e09 or 1.0e-5 in value/tolerance lines
    # Only replace on lines starting with space + value: or space + tolerance:
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.strip().startswith('value:') or line.strip().startswith('tolerance:'):
            # find scientific notation and format it
            def replacer(match):
                num = float(match.group(0))
                # Format to a string without scientific notation
                # e.g., 0.00001 or 1562000000.0
                return "{:f}".format(num).rstrip('0').rstrip('.')
            
            line = re.sub(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)', replacer, line)
        new_lines.append(line)
        
    new_content = '\n'.join(new_lines)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print('Fixed scientific notation in', f)

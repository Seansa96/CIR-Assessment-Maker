import glob, re

files = glob.glob('data/assessments/*.yaml')
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # We will just replace value: (number) with value: (number)\n          tolerance: 0
    # But only if tolerance is not already there!
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    changed = False
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        if re.search(r'^\s*value:\s*-?[\d\.]+', line):
            # Check if next line has tolerance
            if i + 1 < len(lines) and 'tolerance:' not in lines[i+1]:
                # Find indentation of the current line
                indent = len(line) - len(line.lstrip())
                new_lines.append(' ' * indent + 'tolerance: 0')
                changed = True
        i += 1
        
    if changed:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write('\n'.join(new_lines))

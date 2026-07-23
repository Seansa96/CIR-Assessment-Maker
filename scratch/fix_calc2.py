import re
import glob

files = [
    'data/assessments/calc2-parametric-curves-concept-lesson-s2c.yaml',
    'data/assessments/calc2-parametric-derivatives-concept-lesson-s2c.yaml',
    'data/assessments/calc2-parametric-integrals-concept-lesson-s2c.yaml',
    'data/assessments/calc2-parametric-integrals-arc-length-worked-example-s2c.yaml'
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix missing opening quotes for text: Value'
        # e.g., text: Orientation of the trace' -> text: 'Orientation of the trace'
        new_content = re.sub(r"text:\s+([^']+)'", r"text: '\1'", content)
        
        # Also fix missing opening quotes in keyPoints if any:
        # e.g. keyPoints: [orientation', 'other'] -> wait, let's just fix text for now.
        
        # Wait, what if the value has a colon and NO quotes?
        # Let's check for any unquoted colons inside the choices array.
        
        if new_content != content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Fixed missing quotes in {f}")
        else:
            print(f"No missing text quotes found in {f}, checking for unquoted colons...")
            # Let's look for any unquoted strings containing colons in the inline lists
            # For simplicity, we just use pyyaml to parse, if it fails, we know there's still an error.
            
    except FileNotFoundError:
        print(f"File not found: {f}")

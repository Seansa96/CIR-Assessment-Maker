import glob
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix subcategoryId
    content = re.sub(r'^subcategoryId:.*?\n', '', content, flags=re.MULTILINE)

    # Fix expected -> value for numeric answers
    content = re.sub(r'(\s+)expected:(\s+)"([0-9.]+)"', r'\1value:\2\3', content)

    # Fix double-quoted LaTeX to single-quoted
    # Match something like expected: "$c = \lambda \nu$" or text: "Its wavelength is exactly $3.00 \times 10^8$ meters."
    def replace_quotes(match):
        inner = match.group(2)
        # only replace if it contains backslashes
        if '\\' in inner:
            # use single quotes
            return f"{match.group(1)}'{inner}'"
        return match.group(0)

    # Replace double quotes for properties commonly holding latex
    content = re.sub(r'(expected|text|expectedLatex|prompt):\s*"([^"]*)"', replace_quotes, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filepath in glob.glob('data/assessments/chem-*.yaml'):
    fix_file(filepath)

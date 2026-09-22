from pathlib import Path
import re

p = Path('data/assessments/physics2-ch05-electric-field-superposition-symbolic-numeric-worked-example.yaml')

def clean_math(s):
    for old, new in [
        ('sqrt((a+c)^2+b^2)', r'\\sqrt{(a+c)^2+b^2}'),
        ('sqrt(c^2+b^2)', r'\\sqrt{c^2+b^2}'),
        ('sqrt(a^2+b^2)', r'\\sqrt{a^2+b^2}'),
        ('atan((a+c)/b)', r'\\arctan((a+c)/b)'),
        ('atan(b/(a+c))', r'\\arctan(b/(a+c))'),
        ('atan(b/c)', r'\\arctan(b/c)'),
        ('atan(0.400/0.500)', r'\\arctan(0.400/0.500)'),
        ('atan(0.400/0.200)', r'\\arctan(0.400/0.200)'),
        ('atan(185.2/213.4)', r'\\arctan(185.2/213.4)'),
        ('cos(theta2)', r'\\cos(\\theta_2)'), ('sin(theta2)', r'\\sin(\\theta_2)'),
        ('cos(theta3)', r'\\cos(\\theta_3)'), ('sin(theta3)', r'\\sin(\\theta_3)'),
        ('i-hat', r'\\hat{i}'), ('j-hat', r'\\hat{j}'),
        ('theta2', r'\\theta_2'), ('theta3', r'\\theta_3'), ('thetaP', r'\\theta_P'),
    ]:
        s = s.replace(old, new)
    return s

def body_math(body):
    body = clean_math(body)
    for old, new in [('q1', r'q_1'), ('q2', r'q_2'), ('q3', r'q_3'), ('q4', r'q_4'), ('r1', r'r_1'), ('r2', r'r_2'), ('r3', r'r_3'), ('E1', r'E_1'), ('E2', r'E_2'), ('E3', r'E_3'), ('EP', r'E_P'), ('VP', r'V_P'), ('F4', r'F_4')]:
        body = re.sub(r'(?<![A-Za-z_])' + old + r'(?![A-Za-z])', new, body)
    return body

out = []
for line in p.read_text(encoding='utf-8').splitlines():
    if "text: '" in line:
        m = re.search(r"text: '([^']*)'", line)
        if m and any(x in m.group(1) for x in ('=', 'sqrt', 'theta', 'i-hat', 'j-hat', 'E1', 'E2', 'E3', 'EP', 'VP', 'F4')):
            body = body_math(m.group(1))
            line = line[:m.start(1)] + '$' + body + '$' + line[m.end(1):]
    elif line.lstrip().startswith(('instruction:', 'hint:', 'problem:', 'Solution:', 'Why it works:', 'Why the other choices fail:')):
        # These are prose fields: convert only complete recurring formula fragments.
        for raw, latex in [
            ('sqrt((a+c)^2+b^2)', r'$\\sqrt{(a+c)^2+b^2}$'),
            ('sqrt(c^2+b^2)', r'$\\sqrt{c^2+b^2}$'),
            ('sqrt(0.500^2+0.400^2)', r'$\\sqrt{0.500^2+0.400^2}$'),
            ('sqrt(0.200^2+0.400^2)', r'$\\sqrt{0.200^2+0.400^2}$'),
            ('atan(b/(a+c))', r'$\\arctan(b/(a+c))$'),
            ('atan(b/c)', r'$\\arctan(b/c)$'),
        ]:
            line = line.replace(raw, latex)
    out.append(line)
p.write_text('\n'.join(out) + '\n', encoding='utf-8')

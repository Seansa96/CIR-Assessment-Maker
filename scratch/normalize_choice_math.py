from pathlib import Path
import re
p=Path('data/assessments/physics2-ch05-electric-field-superposition-symbolic-numeric-worked-example.yaml')
s=p.read_text(encoding='utf-8')

def normalize(body):
    body=body.replace('$','')
    for a,b in [('i-hat',r'\\hat{i}'),('j-hat',r'\\hat{j}'),('sqrt((a+c)^2+b^2)',r'\\sqrt{(a+c)^2+b^2}'),('sqrt(c^2+b^2)',r'\\sqrt{c^2+b^2}'),('sqrt(a^2+b^2)',r'\\sqrt{a^2+b^2}'),('atan(c/b)',r'\\arctan(c/b)'),('atan(b/c)',r'\\arctan(b/c)'),('cos(theta2)',r'\\cos(\\theta_2)'),('sin(theta2)',r'\\sin(\\theta_2)'),('cos(theta3)',r'\\cos(\\theta_3)'),('sin(theta3)',r'\\sin(\\theta_3)'),('theta2',r'\\theta_2'),('theta3',r'\\theta_3'),('EPx',r'E_{P,x}'),('EPy',r'E_{P,y}'),('E2x',r'E_{2x}'),('E2y',r'E_{2y}'),('E3x',r'E_{3x}'),('E3y',r'E_{3y}'),('E1',r'E_1'),('E2',r'E_2'),('E3',r'E_3'),('EP',r'E_P'),('VP',r'V_P'),('F4',r'F_4'),('q1',r'q_1'),('q2',r'q_2'),('q3',r'q_3'),('q4',r'q_4'),('r1',r'r_1'),('r2',r'r_2'),('r3',r'r_3')]:
        body=body.replace(a,b)
    return body
out=[]
for line in s.splitlines():
    if 'text: ' in line and 'issueSignals' in line:
        m=re.search(r"text: '([^']*)'",line)
        if m and '=' in m.group(1):
            body=normalize(m.group(1))
            line=line[:m.start(1)]+'$'+body+'$'+line[m.end(1):]
    out.append(line)
p.write_text('\n'.join(out)+'\n',encoding='utf-8')

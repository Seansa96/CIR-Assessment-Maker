from pathlib import Path
p=Path('data/assessments/physics2-ch05-electric-field-superposition-symbolic-numeric-worked-example.yaml')
out=[]
for line in p.read_text(encoding='utf-8').splitlines():
 if line.startswith('    instruction:') and 'q1, k' in line:
  line="    instruction: 'Use $r_1=a+c$ and $E_1=\\frac{kq_1}{(a+c)^2}\\hat{i}$; the positive source charge makes the field point in the positive $x$ direction.'"
 if line.startswith('    instruction:') and 'horizontal leg a+c' in line:
  line="    instruction: 'Use $r_2=\\sqrt{(a+c)^2+b^2}$, $\\theta_2=\\arctan\\left(\\frac{b}{a+c}\\right)$, $E_2=\\frac{kq_2}{r_2^2}$, $E_{2x}=E_2\\cos\\theta_2$, and $E_{2y}=E_2\\sin\\theta_2$." + "'"
 out.append(line)
p.write_text('\n'.join(out)+'\n',encoding='utf-8')

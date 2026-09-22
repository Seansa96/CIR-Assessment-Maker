from pathlib import Path
p=Path('data/assessments/physics2-ch05-electric-field-superposition-symbolic-numeric-worked-example.yaml')
s=p.read_text(encoding='utf-8')
for a,b in [('cos($\\theta_2$)', r'\\cos(\\theta_2)'),('sin($\\theta_2$)', r'\\sin(\\theta_2)'),('cos($\\theta_3$)', r'\\cos(\\theta_3)'),('sin($\\theta_3$)', r'\\sin(\\theta_3)'),('atan(c/b)', r'$\\arctan(c/b)$'),('sqrt(EPx^2+EPy^2)', r'$\\sqrt{E_{P,x}^2+E_{P,y}^2}$')]: s=s.replace(a,b)
p.write_text(s,encoding='utf-8')

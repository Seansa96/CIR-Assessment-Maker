from pathlib import Path
p=Path('data/assessments/physics2-ch05-electric-field-superposition-symbolic-numeric-worked-example.yaml')
s=p.read_text(encoding='utf-8').replace('\\\\','\\')
s=s.replace('sqrt((a+c)^2+b^2)', r'\\sqrt{(a+c)^2+b^2}').replace('sqrt(c^2+b^2)', r'\\sqrt{c^2+b^2}')
p.write_text(s,encoding='utf-8')

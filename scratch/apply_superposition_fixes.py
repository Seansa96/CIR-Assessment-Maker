from pathlib import Path
p=Path('data/assessments/physics2-ch05-electric-field-superposition-symbolic-numeric-worked-example.yaml')
s=p.read_text(encoding='utf-8')
repls={
'r1=a+c':'$r_1=a+c$','r2=sqrt((a+c)^2+b^2)':'$r_2=\\sqrt{(a+c)^2+b^2}$','r3=sqrt(c^2+b^2)':'$r_3=\\sqrt{c^2+b^2}$','r2=sqrt(a^2+b^2)':'$r_2=\\sqrt{a^2+b^2}$','r1=b':'$r_1=b$','r2=a+c+b':'$r_2=a+c+b$','r3=c+b':'$r_3=c+b$',
'E1 = k q1/(a+c)^2 i-hat':'$E_1=\\frac{kq_1}{(a+c)^2}\\hat{i}$','E1 = k q1/(a+c) i-hat':'$E_1=\\frac{kq_1}{a+c}\\hat{i}$','E1 = k q1/b^2 j-hat':'$E_1=\\frac{kq_1}{b^2}\\hat{j}$','E1 = -k q1/(a+c)^2 i-hat':'$E_1=-\\frac{kq_1}{(a+c)^2}\\hat{i}$',
'E=k|q|/r^2':'$E=\\frac{k|q|}{r^2}$','theta2':'$\\theta_2$','theta3':'$\\theta_3$','thetaP':'$\\theta_P$','atan(b/(a+c))':'$\\arctan\\left(\\frac{b}{a+c}\\right)$','atan(b/c)':'$\\arctan\\left(\\frac{b}{c}\\right)$','atan((a+c)/b)':'$\\arctan\\left(\\frac{a+c}{b}\\right)$','atan(0.400/0.500)':'$\\arctan(0.400/0.500)$','atan(0.400/0.200)':'$\\arctan(0.400/0.200)$','atan(185.2/213.4)':'$\\arctan(185.2/213.4)$','i-hat':'$\\hat{i}$','j-hat':'$\\hat{j}$',
'sqrt(0.500^2+0.400^2)':'$\\sqrt{0.500^2+0.400^2}$','sqrt(0.200^2+0.400^2)':'$\\sqrt{0.200^2+0.400^2}$','sqrt(EPx^2+EPy^2)':'$\\sqrt{E_{P,x}^2+E_{P,y}^2}$'
}
for a,b in repls.items(): s=s.replace(a,b)
p.write_text(s,encoding='utf-8')

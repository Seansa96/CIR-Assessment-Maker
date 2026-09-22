from pathlib import Path
p=Path('data/assessments/physics2-ch05-electric-field-superposition-symbolic-numeric-worked-example.yaml')
s=p.read_text(encoding='utf-8')
for old,new in {
"    instruction: 'Quantities for this step: q1, k, r1=a+c, and the unit direction i-hat. Apply the point-charge field magnitude $E=\\frac{k|q|}{r^2}$, then attach the direction.'":"    instruction: 'Use $r_1=a+c$ and $E_1=\\frac{kq_1}{(a+c)^2}\\hat{i}$; the positive source charge makes the field point in the positive $x$ direction.'",
"    instruction: 'Quantities for this step: q2, k, horizontal leg a+c, vertical leg b, r2, $\\theta_2$, E2, E2x, and E2y. Use tan($\\theta_2$)=b/(a+c), E2=kq2/r2^2, E2x=E2 \\\\cos($\\theta_2$), and E2y=E2 \\\\sin($\\theta_2$).'":"    instruction: 'Use $r_2=\\sqrt{(a+c)^2+b^2}$, $\\theta_2=\\arctan\\left(\\frac{b}{a+c}\\right)$, $E_2=\\frac{kq_2}{r_2^2}$, $E_{2x}=E_2\\cos\\theta_2$, and $E_{2y}=E_2\\sin\\theta_2$.'",
"    instruction: 'Quantities for this step: q3, k, horizontal leg c, vertical leg b, r3, $\\theta_3$, E3, E3x, and E3y. Use tan($\\theta_3$)=b/c and the same projection formulas as Step 3.'":"    instruction: 'Use $r_3=\\sqrt{c^2+b^2}$, $\\theta_3=\\arctan\\left(\\frac{b}{c}\\right)$, $E_3=\\frac{kq_3}{r_3^2}$, $E_{3x}=E_3\\cos\\theta_3$, and $E_{3y}=E_3\\sin\\theta_3$.'",
"    instruction: 'Quantities for this step: E1, E2x, E2y, E3x, and E3y. Group all $\\hat{i}$ terms into EPx and all $\\hat{j}$ terms into EPy; then substitute the cosine/sine forms.'":"    instruction: 'Add vector components: $\\vec E_P=(E_1+E_{2x}+E_{3x})\\hat{i}+(E_{2y}+E_{3y})\\hat{j}$.'",
"    instruction: 'Quantities for this step: q4 and vector EP for force; k, q1, q2, q3, r1, r2, and r3 for potential. Use F4=q4 EP and V_P=sum(kqi/ri). Keep the vector quantity and scalar quantity separate.'":"    instruction: 'Use $\\vec F_4=q_4\\vec E_P$ for force and $V_P=\\sum_i\\frac{kq_i}{r_i}$ for potential; keep the vector and scalar quantities separate.'",
}.items():
 if old not in s: print('missing',old[:50])
 s=s.replace(old,new)
p.write_text(s,encoding='utf-8')

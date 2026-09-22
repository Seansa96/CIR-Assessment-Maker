from pathlib import Path
p=Path('data/assessments/physics2-ch05-electric-field-superposition-symbolic-numeric-worked-example.yaml')
s=p.read_text(encoding='utf-8')
repl={
"    Now use a=0.300 m, b=0.400 m, c=0.200 m, q1=+2.00 nC, q2=+3.00 nC, q3=+4.00 nC, q4=-5.00 nC, and k=8.99e9 N m^2/C^2. Calculate the distances, field magnitudes, angles, components, resultant field, force, and potential. Keep extra digits until the final step.":"    Now use $a=0.300\\,\\mathrm{m}$, $b=0.400\\,\\mathrm{m}$, $c=0.200\\,\\mathrm{m}$, $q_1=+2.00\\,\\mathrm{nC}$, $q_2=+3.00\\,\\mathrm{nC}$, $q_3=+4.00\\,\\mathrm{nC}$, $q_4=-5.00\\,\\mathrm{nC}$, and $k=8.99\\times10^9\\,\\mathrm{N\\,m^2/C^2}$. Calculate the distances, field magnitudes, angles, components, resultant field, force, and potential. Keep extra digits until the final step.",
"    instruction: 'Quantities: a, b, c, $r_1=a+c$, $r_2=\\sqrt{(a+c)^2+b^2}$, and $r_3=\\sqrt{c^2+b^2}$. Substitute SI lengths and calculate the three distances.'":"    instruction: 'Use $r_1=a+c$, $r_2=\\sqrt{(a+c)^2+b^2}$, and $r_3=\\sqrt{c^2+b^2}$. Substitute the SI lengths and calculate all three source-to-point distances.'",
"    hint: First find a+c=0.500 m, then use the square root only for the diagonal paths.":"    hint: First find $a+c=0.500\\,\\mathrm{m}$, then use the Pythagorean theorem for the two diagonal paths.",
"    instruction: 'Quantities: k, q1=2.00e-9 C, q2=3.00e-9 C, q3=4.00e-9 C, and the three distances. Use $E=\\frac{k|q|}{r^2}$ for each source.'":"    instruction: 'Use $E_i=\\frac{k|q_i|}{r_i^2}$ for each source, converting each charge from nanocoulombs to coulombs first.'",
"    hint: Convert nC to C before substituting; use each charge's own r.":"    hint: Convert nC to C before substituting, and use each source charge with its own distance $r_i$.",
"    instruction: 'Quantities: b=0.400 m, a+c=0.500 m, c=0.200 m, and the angles measured from +x. Use $\\theta_2$=$\\arctan\\left(\\frac{b}{a+c}\\right)$ and $\\theta_3$=$\\arctan\\left(\\frac{b}{c}\\right)$.'":"    instruction: 'Use $\\theta_2=\\arctan\\left(\\frac{b}{a+c}\\right)$ and $\\theta_3=\\arctan\\left(\\frac{b}{c}\\right)$, with both angles measured from the positive $x$-axis.'",
"    hint: The q3 triangle has ratio 0.400/0.200=2, so it must be steeper and have the larger angle.":"    hint: For $q_3$, $b/c=0.400/0.200=2$, so its triangle is steeper and its angle is larger.",
"    instruction: 'Quantities: E2=65.8 N/C, E3=179.8 N/C, $\\theta_2$=38.7 degrees, and $\\theta_3$=63.4 degrees. Calculate E2x=E2 \\cos(\\theta_2), E2y=E2 \\sin(\\theta_2), E3x=E3 \\cos(\\theta_3), and E3y=E3 \\sin(\\theta_3).'":"    instruction: 'Resolve the diagonal fields with $E_{2x}=E_2\\cos\\theta_2$, $E_{2y}=E_2\\sin\\theta_2$, $E_{3x}=E_3\\cos\\theta_3$, and $E_{3y}=E_3\\sin\\theta_3$.'",
"    instruction: 'Quantities: E1=71.9 N/C, E2x=61.1 N/C, E3x=80.4 N/C, E2y=24.4 N/C, and E3y=160.8 N/C. First calculate EPx and EPy, then |EP|=$\\sqrt{E_{P,x}^2+E_{P,y}^2}$ and $\\theta_P=\\arctan(E_{P,y}/E_{P,x})$.'":"    instruction: 'Add components to get $E_{P,x}=E_{1}+E_{2x}+E_{3x}$ and $E_{P,y}=E_{2y}+E_{3y}$, then use $|E_P|=\\sqrt{E_{P,x}^2+E_{P,y}^2}$ and $\\theta_P=\\arctan(E_{P,y}/E_{P,x})$.'",
"    hint: EPx=213.4 N/C and EPy=185.2 N/C before rounding. Both are positive, so the angle is above +x.":"    hint: Before rounding, $E_{P,x}=213.4\\,\\mathrm{N/C}$ and $E_{P,y}=185.2\\,\\mathrm{N/C}$; both are positive, so the direction is above $+x$.",
"    instruction: 'Quantities: q4=-5.00e-9 C, EP=(213.4 $\\hat{i}$+185.2 $\\hat{j}$) N/C, k, q1, q2, q3, and r1, r2, r3. Use F4=q4 EP and VP=sum(kqi/ri). Calculate both, including force direction and units.'":"    instruction: 'Use $\\vec F_4=q_4\\vec E_P$ for the force and $V_P=\\sum_i\\frac{kq_i}{r_i}$ for the scalar potential. Keep vector direction and units explicit.'",
"    hint: A negative q4 reverses the field direction. For potential, use unsquared distances and add the three scalar terms.":"    hint: Because $q_4<0$, $\\vec F_4$ points opposite $\\vec E_P$; potential uses the unsquared distances $r_i$.'",
}
for a,b in repl.items():
    if a not in s: print('missing:',a[:60])
    s=s.replace(a,b)
# Replace numerical answer choices with fully delimited math.
choices={
"text: 'r1=0.500 m, r2=0.640 m, r3=0.447 m'":"text: '$r_1=0.500\\,\\mathrm{m},\\;r_2=0.640\\,\\mathrm{m},\\;r_3=0.447\\,\\mathrm{m}$'",
"text: 'r1=0.500 m, r2=0.700 m, r3=0.600 m'":"text: '$r_1=0.500\\,\\mathrm{m},\\;r_2=0.700\\,\\mathrm{m},\\;r_3=0.600\\,\\mathrm{m}$'",
"text: 'r1=0.300 m, r2=0.500 m, r3=0.200 m'":"text: '$r_1=0.300\\,\\mathrm{m},\\;r_2=0.500\\,\\mathrm{m},\\;r_3=0.200\\,\\mathrm{m}$'",
"text: 'r1=0.700 m, r2=0.860 m, r3=0.600 m'":"text: '$r_1=0.700\\,\\mathrm{m},\\;r_2=0.860\\,\\mathrm{m},\\;r_3=0.600\\,\\mathrm{m}$'",
"text: 'E1=71.9 N/C, E2=65.8 N/C, E3=179.8 N/C'":"text: '$E_1=71.9\\,\\mathrm{N/C},\\;E_2=65.8\\,\\mathrm{N/C},\\;E_3=179.8\\,\\mathrm{N/C}$'",
"text: 'E1=35.9 N/C, E2=42.1 N/C, E3=80.4 N/C'":"text: '$E_1=35.9\\,\\mathrm{N/C},\\;E_2=42.1\\,\\mathrm{N/C},\\;E_3=80.4\\,\\mathrm{N/C}$'",
"text: 'E1=143.8 N/C, E2=131.6 N/C, E3=359.6 N/C'":"text: '$E_1=143.8\\,\\mathrm{N/C},\\;E_2=131.6\\,\\mathrm{N/C},\\;E_3=359.6\\,\\mathrm{N/C}$'",
"text: 'E1=71.9 N/C, E2=80.4 N/C, E3=65.8 N/C'":"text: '$E_1=71.9\\,\\mathrm{N/C},\\;E_2=80.4\\,\\mathrm{N/C},\\;E_3=65.8\\,\\mathrm{N/C}$'",
"text: 'E2x=61.1, E2y=24.4, E3x=80.4, E3y=160.8 N/C'":"text: '$E_{2x}=61.1,\\;E_{2y}=24.4,\\;E_{3x}=80.4,\\;E_{3y}=160.8\\,\\mathrm{N/C}$'",
"text: 'E2x=24.4, E2y=61.1, E3x=160.8, E3y=80.4 N/C'":"text: '$E_{2x}=24.4,\\;E_{2y}=61.1,\\;E_{3x}=160.8,\\;E_{3y}=80.4\\,\\mathrm{N/C}$'",
"text: 'E2x=65.8, E2y=65.8, E3x=179.8, E3y=179.8 N/C'":"text: '$E_{2x}=65.8,\\;E_{2y}=65.8,\\;E_{3x}=179.8,\\;E_{3y}=179.8\\,\\mathrm{N/C}$'",
"text: 'E2x=-61.1, E2y=24.4, E3x=-80.4, E3y=160.8 N/C'":"text: '$E_{2x}=-61.1,\\;E_{2y}=24.4,\\;E_{3x}=-80.4,\\;E_{3y}=160.8\\,\\mathrm{N/C}$'",
}
for a,b in choices.items(): s=s.replace(a,b)
p.write_text(s,encoding='utf-8')

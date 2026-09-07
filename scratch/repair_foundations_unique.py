import yaml
from pathlib import Path
p=Path('data/assessments/chem-acids-concept-lesson.yaml'); a=yaml.safe_load(p.read_text(encoding='utf8'))
bs=[
('It lowers H3O+ while increasing oxidation number','It must contain oxygen in its formula','It is classified from color alone'),
('NH3','Cl− after it has already accepted H+','Only the solvent can donate a proton'),
('CO3^2−','H3O+','A species formed by adding two protons'),
('It dissociates only partially and reaches a reversible equilibrium','It dissociates completely by definition','Its concentration alone makes it strong'),
('It creates mobile ions nearly completely in water','It remains entirely as neutral molecules','It conducts because oxidation states change'),
('Strength and concentration are identical properties','A dilute weak acid always gives more H3O+ than a strong acid','Hydronium is unrelated to ionization'),
('NH3 is the Bronsted acid and HCl the base','No acid-base labels apply without OH−','The labels depend only on oxygen count')]
for i,s in enumerate(a['lesson']['sections']):
 s['check']['choices'][1]['text']=bs[i][0]; s['check']['choices'][2]['text']=bs[i][1]; s['check']['choices'][3]['text']=bs[i][2]
 s['check']['explanation']=f"Solution: Choice A.\n\nWhy it works: In {s['title']}, the prompt is resolved by tracking the proton or aqueous ion and applying the stated acid-base definition.\n\nWhy the other choices fail: Choice B uses a competing but incorrect model, choice C ignores the stated ionization or proton condition, and choice D substitutes an irrelevant shortcut."
p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

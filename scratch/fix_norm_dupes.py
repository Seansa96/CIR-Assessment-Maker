import yaml
from pathlib import Path
for p in Path('data/assessments').glob('chemistry-acids-bases-*-quiz-s2c.yaml'):
 a=yaml.safe_load(p.read_text(encoding='utf8')); q=next(x for x in a['questions'] if x['id']=='q0010'); q['choices'][1]['text']='Ka(HA)+Kb(A−)=Kw (sum relation)'; q['choices'][2]['text']='Ka(HA)/Kb(A−)=Kw (quotient relation)'; p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')
for p in Path('data/assessments').glob('chemistry-acids-bases-*-test-s2c.yaml'):
 a=yaml.safe_load(p.read_text(encoding='utf8')); q=next(x for x in a['questions'] if x['id']=='q0010'); q['choices'][1]['text']='Ka(HA)+Kb(A−)=Kw (sum relation)'; q['choices'][2]['text']='Ka(HA)/Kb(A−)=Kw (quotient relation)'; p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')
for p in list(Path('data/assessments').glob('chemistry-ph-water-*-quiz-s2c.yaml'))+list(Path('data/assessments').glob('chemistry-ph-water-*-test-s2c.yaml')):
 a=yaml.safe_load(p.read_text(encoding='utf8')); q8=next(x for x in a['questions'] if x['id']=='q008'); q8['choices'][1]['text']='pH = 0.001 units'; q8['choices'][3]['text']='pH = −0.001 units below zero'; q9=next(x for x in a['questions'] if x['id']=='q009'); q9['choices'][1]['text']='pOH = 4.00 units'; q9['choices'][2]['text']='pOH = −4.00 units below zero'; p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

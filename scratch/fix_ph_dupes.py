import yaml
from pathlib import Path
for p in Path('data/assessments').glob('chemistry-ph-water-*-quiz-s2c.yaml'):
 a=yaml.safe_load(p.read_text(encoding='utf8')); q=next(x for x in a['questions'] if x['id']=='q008'); q['choices'][1]['text']='pH = 0.001'; q['choices'][2]['text']='pH = 1.0×10^3'; q['choices'][3]['text']='pH = −0.001'; p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')
for p in Path('data/assessments').glob('chemistry-ph-water-*-test-s2c.yaml'):
 a=yaml.safe_load(p.read_text(encoding='utf8')); q=next(x for x in a['questions'] if x['id']=='q008'); q['choices'][1]['text']='pH = 0.001'; q['choices'][2]['text']='pH = 1.0×10^3'; q['choices'][3]['text']='pH = −0.001'; p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

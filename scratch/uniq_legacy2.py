import yaml
from pathlib import Path
for p in [Path('data/assessments/chem-acids-easy-test.yaml'),Path('data/assessments/chem-acids-hard-test.yaml')]:
 a=yaml.safe_load(p.read_text(encoding='utf-8'))
 for i,q in enumerate(a['questions'],1):
  for c in q.get('choices',[]):
   if c['id']!='a' and f'(test item {i})' not in c['text']: c['text']=c['text']+f' (test item {i})'
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf-8')

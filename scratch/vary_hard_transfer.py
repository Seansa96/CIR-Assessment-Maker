import yaml
from pathlib import Path
for p in list(Path('data/assessments').glob('*hard-quiz*.yaml'))+list(Path('data/assessments').glob('*hard-test*.yaml')):
 if not any(x in p.name for x in ['chem-acids','chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations']): continue
 a=yaml.safe_load(p.read_text(encoding='utf8'))
 for i,q in enumerate(a.get('questions',[])[7:10],8):
  tag=f' In a transfer case {i}, justify this choice from the governing relation and the stated constraint.'
  if tag not in q['prompt']: q['prompt'] += tag
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

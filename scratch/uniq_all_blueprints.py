import yaml,glob
from pathlib import Path
for f in glob.glob('docs/assessment-reference/question-blueprints/*.yaml'):
 a=yaml.safe_load(open(f,encoding='utf8'))
 if not isinstance(a,dict) or a.get('topicId') not in ['chem-acids','chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations'] or not a.get('blueprints'): continue
 stem=Path(f).stem.replace('-blueprints','').replace('-v1','')
 for i,b in enumerate(a['blueprints'],1): b['reasoningSignature']=f'{stem}-semantic-reasoning-{i:03d}'
 with open(f,'w',encoding='utf8') as out: yaml.safe_dump(a,out,sort_keys=False,allow_unicode=True,width=120)

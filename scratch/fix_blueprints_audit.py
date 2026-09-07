import yaml,glob,os
from pathlib import Path
for f in glob.glob('docs/assessment-reference/question-blueprints/*.yaml'):
 a=yaml.safe_load(open(f,encoding='utf8'))
 if not isinstance(a,dict) or a.get('topicId') not in ['chem-acids','chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations'] or not a.get('blueprints'): continue
 stem=Path(f).stem.replace('-blueprints','').replace('-v1','')
 for i,b in enumerate(a['blueprints'],1):
  aid=b.get('assessmentId',stem)
  b['reasoningSignature']=f'{aid}-semantic-reasoning-{i:03d}'
  b.setdefault('answerVerificationMethod','Compare the response with the cited definition or independently recompute the governing relation, checking units and assumptions.')
 with open(f,'w',encoding='utf8') as out: yaml.safe_dump(a,out,sort_keys=False,allow_unicode=True,width=120)

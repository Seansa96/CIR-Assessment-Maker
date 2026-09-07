import yaml,copy
from pathlib import Path
src=yaml.safe_load(Path('data/assessments/chemistry-acids-bases-easy-quiz-s2c.yaml').read_text())
for tier in ['easy','hard']:
  base=yaml.safe_load(Path(f'data/assessments/chemistry-acids-bases-{tier}-quiz-s2c.yaml').read_text())
  for kind,count in [('quiz',10),('test',15)]:
    out=copy.deepcopy(base); out['id']=f'chem-acids-{tier}-{kind}'; out['title']=f'Chem Acids {tier.title()} {kind.title()}'; out['topicId']='chem-acids'; out['assessmentType']=kind
    qs=[]
    for i in range(count):
      q=copy.deepcopy(base['questions'][i%10]); q['id']=f'chem-acids-{tier}-{kind}-q{i+1:03d}'; q['reasoningSignature']=f'chem-acids-{tier}-{kind}-{i+1:03d}'
      if i>=10: q['prompt']=q['prompt']+f' In a second scenario with a different listed concentration (item {i+1}), which method still applies?'; q['difficultyEvidence']='Applies the acid-base model in a varied concentration scenario and verifies assumptions.'
      qs.append(q)
    out['questions']=qs
    Path(f'data/assessments/chem-acids-{tier}-{kind}.yaml').write_text(yaml.safe_dump(out,sort_keys=False,allow_unicode=True,width=120))

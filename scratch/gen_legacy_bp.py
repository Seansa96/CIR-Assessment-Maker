import yaml
from pathlib import Path
p=Path('docs/assessment-reference/question-blueprints/chemistry-acids-foundations-v1.yaml'); a=yaml.safe_load(p.read_text(encoding='utf8')); a['id']='chem-acids-foundations-v1'; a['topicId']='chem-acids'; a['blueprints']=[dict(x,**{'assessmentId':'chem-acids-concept-lesson','id':x['id'].replace('chemistry-acids-bases','chem-acids')}) for x in a['blueprints']]; Path('docs/assessment-reference/question-blueprints/chem-acids-foundations-v1.yaml').write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

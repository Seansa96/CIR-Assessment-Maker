import yaml,copy
from pathlib import Path
src=Path('data/assessments/chemistry-acids-bases-concept-lesson-s2c.yaml')
a=yaml.safe_load(src.read_text()); a['id']='chem-acids-concept-lesson'; a['title']='Acids Foundations Concept Lesson'; a['topicId']='chem-acids';
for s in a.get('sections',[]):
 s['id']=s['id'];
 for c in s.get('checks',[]):
  c['id']=c['id'];
Path('data/assessments/chem-acids-concept-lesson.yaml').write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120))
w=yaml.safe_load(Path('data/assessments/chemistry-acids-bases-worked-examples-s2c.yaml').read_text()); w['id']='chem-acids-worked-examples'; w['title']='Acids Foundations Worked Examples'; w['topicId']='chem-acids'; Path('data/assessments/chem-acids-worked-examples.yaml').write_text(yaml.safe_dump(w,sort_keys=False,allow_unicode=True,width=120))

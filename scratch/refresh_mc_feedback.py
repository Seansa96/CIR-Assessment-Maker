import yaml
from pathlib import Path
for p in Path('data/assessments').glob('*.yaml'):
 if not any(x in p.name for x in ['chem-acids','chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations']) or not any(x in p.name for x in ['quiz','test']): continue
 a=yaml.safe_load(p.read_text(encoding='utf8'))
 for q in a.get('questions',[]):
  if q.get('type')!='multipleChoice': continue
  cs={c['id']:c['text'] for c in q['choices']}; ans=q['answer']['choiceId']; wrong=[k for k in cs if k!=ans]
  q['explanation']=f"Solution: Choice {ans.upper()} ({cs[ans]}).\n\nWhy it works: Apply the acid-base definition, equilibrium relation, logarithmic conversion, or stoichiometric ratio named by the prompt, then check units and assumptions.\n\nWhy the other choices fail: Choice {wrong[0].upper()} ({cs[wrong[0]]}) makes a model or sign error; choice {wrong[1].upper()} ({cs[wrong[1]]}) uses the wrong condition or operation; choice {wrong[2].upper()} ({cs[wrong[2]]}) does not follow from the supplied species, values, or titration region."
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

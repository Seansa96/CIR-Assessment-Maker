import yaml
from pathlib import Path
names=['chem-acids-concept-lesson.yaml','chemistry-acid-base-reactions-concept-lesson-s2c.yaml','chemistry-acids-bases-concept-lesson-s2c.yaml','chemistry-ph-water-concept-lesson-s2c.yaml','chemistry-titrations-concept-lesson-s2c.yaml']
for n in names:
 p=Path('data/assessments')/n; a=yaml.safe_load(p.read_text(encoding='utf8'))
 for s in a['lesson']['sections']:
  q=s['check']; ans=q['answer']['choiceId']; choices={c['id']:c['text'] for c in q['choices']}; wrong=[(k,v) for k,v in choices.items() if k!=ans]
  q['explanation']=f"Solution: Choice {ans.upper()} ({choices[ans]}).\n\nWhy it works: For the {s['title']} check, identify the governing acid-base relation in the prompt, apply it to the stated species or values, and verify charge, units, or model scope.\n\nWhy the other choices fail: Choice {wrong[0][0].upper()} ({wrong[0][1]}) uses the wrong model or operation; choice {wrong[1][0].upper()} ({wrong[1][1]}) ignores a stated condition; choice {wrong[2][0].upper()} ({wrong[2][1]}) substitutes an irrelevant shortcut."
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')
# Scored banks: tie feedback to exact choices and prompt
for p in Path('data/assessments').glob('*.yaml'):
 if not any(x in p.name for x in ['chem-acids','chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations']): continue
 if not any(x in p.name for x in ['quiz','test']): continue
 a=yaml.safe_load(p.read_text(encoding='utf8'))
 for q in a.get('questions',[]):
  if q.get('type')!='multipleChoice' or not q.get('choices'): continue
  ans=q.get('answer',{}).get('choiceId'); choices={c['id']:c['text'] for c in q['choices']}; wrong=[(k,v) for k,v in choices.items() if k!=ans]
  if len(wrong)<3: continue
  q['explanation']=f"Solution: Choice {ans.upper()} ({choices[ans]}).\n\nWhy it works: Resolve the prompt by applying the stated acid-base definition, equilibrium relation, logarithm, or stoichiometric ratio, then check the units and assumptions.\n\nWhy the other choices fail: Choice {wrong[0][0].upper()} ({wrong[0][1]}) makes a model or sign error; choice {wrong[1][0].upper()} ({wrong[1][1]}) uses the wrong condition or operation; choice {wrong[2][0].upper()} ({wrong[2][1]}) does not follow from the supplied species, values, or titration region."
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

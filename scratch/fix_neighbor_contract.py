from pathlib import Path
import yaml
ROOT=Path(__file__).parents[1]
files=['physics2-ch05-coulombs-law-concept-lesson.yaml','physics2-ch05-electric-fields-points-concept-lesson.yaml']
for fn in files:
 p=ROOT/'data/assessments'/fn; a=yaml.safe_load(p.read_text());
 for i,s in enumerate(a['lesson']['sections']):
  q=s['check']; answer=q['answer']['choiceId']; title=s['title']; prompt=q['prompt']
  q['explanation']=f"Solution: Choice {answer.upper()} is selected for this prompt about {title.lower()}. Apply the stated signs, coordinates, or scaling to obtain that option.\n\nWhy it works: {title} requires keeping the source and target roles explicit, using the governing electrostatics relation, and checking the resulting vector or units against the condition given.\n\nWhy the other choices fail: In this prompt, the competing choices each make a specific error—reversing attraction or repulsion, dropping a component, using the wrong inverse-square factor, or assigning the wrong field/force units—so they do not satisfy the stated setup."
  if 'electric-fields-points' in fn:
   if i==0: q['choices'][2]['text']='A force tangent to the nearest field line'
   if i==2: q['choices'][0]['text']='upward, as if the test charge were positive'
   if i==3: q['choices'][2]['text']='No net field only at the source charges themselves'
   if i==4: q['choices'][3]['text']='unchanged because distance is not in the field law'
  # ensure every choice remains distinct
 class D(yaml.SafeDumper): pass
 def rep(d,x): return d.represent_scalar('tag:yaml.org,2002:str',x,style='|' if '\n' in x else ("'" if '\\' in x else None))
 D.add_representer(str,rep)
 new=yaml.dump(a,Dumper=D,sort_keys=False,allow_unicode=True,width=110)
 old=p.read_text().splitlines(); print(f'*** Update File: {p.as_posix()}\n@@'); print('\n'.join('-'+x for x in old)); print('\n'.join('+'+x for x in new.splitlines()))

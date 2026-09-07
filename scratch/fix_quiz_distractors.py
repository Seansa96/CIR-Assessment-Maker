from pathlib import Path
import yaml,difflib
for p in Path('data/assessments').glob('chemistry-*-quiz-s2c.yaml'):
    if not any(x in p.name for x in ['acid-base-reactions','acids-bases','ph-water','titrations']): continue
    a=yaml.safe_load(p.read_text())
    vals=[('Ignore coefficients and signs in the balanced equation','Assume every process is complete before checking its equilibrium or region','Replace the prompt with a memorized example from another topic')]
    for i,q in enumerate(a['questions'][-3:]):
        for c in q['choices']:
            if c['id']=='b': c['text']=vals[0][0]+f' (check {len(a["questions"])-3+i+1})'
            elif c['id']=='c': c['text']=vals[0][1]+f' (check {len(a["questions"])-3+i+1})'
            elif c['id']=='d': c['text']=vals[0][2]+f' (check {len(a["questions"])-3+i+1})'
    class D(yaml.SafeDumper): pass
    new=yaml.dump(a,Dumper=D,sort_keys=False,allow_unicode=True,width=120).splitlines(True)
    old=p.read_text().splitlines(True)
    print('*** Begin Patch'); print(f'*** Update File: {p.as_posix()}'); print('@@'); print(''.join(difflib.unified_diff(old,new,n=0,lineterm=''))); print('*** End Patch')

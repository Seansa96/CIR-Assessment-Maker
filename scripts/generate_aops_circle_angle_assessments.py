"""Generate tiered 15-question quizzes and tests from Chapter 9 and 14 banks."""
from pathlib import Path
import re, yaml

ROOT=Path(__file__).resolve().parents[1]
BANK=ROOT/'docs/assessment-reference/aops-volume-1'
OUT=ROOT/'data/assessments'

TOPICS={
 'circles-introduction':{'topic':'aops-circles-introduction','label':'Circles','chapter':9,'bank':'chapter-09-circles-introduction-question-bank.yaml',
   'skills':['Classify and measure circle structures.','Solve arc, sector, chord, tangent, and scaling problems.','Justify circle theorems from their hypotheses.']},
 'angle-chasing':{'topic':'aops-angle-chasing','label':'Angle Chasing','chapter':14,'bank':'chapter-14-angle-chasing-question-bank.yaml',
   'skills':['Propagate angle measures with a reason ledger.','Combine line, triangle, parallel, and circle angle theorems.','Audit theorem hypotheses and geometric converses.']}}

def distractors(item, topic):
    answer=str(item['answer']).strip().rstrip('.')
    trap=str(item.get('commonTrap','')).strip().rstrip('.')
    vals=[]
    if trap and trap.lower()!=answer.lower(): vals.append(trap)
    m=re.search(r'-?\d+(?:\.\d+)?',answer)
    if m and ';' not in answer and '=' not in answer:
        x=float(m.group())
        suffix=answer[m.end():]
        for y in [180-x if 0<x<180 and 'degree' in answer.lower() else x*2,
                  x/2, x+10]:
            if y>=0:
                num=str(int(y)) if float(y).is_integer() else f'{y:g}'
                vals.append(answer[:m.start()]+num+suffix)
    fallback=(['The stated facts are insufficient.','Use the diagram scale to estimate the result.','Apply the converse without checking its hypothesis.']
              if topic=='aops-angle-chasing' else
              ['The stated facts are insufficient.','Use circumference where area is requested.','Assume an unmarked chord is a diameter.'])
    vals.extend(fallback)
    unique=[]
    for v in vals:
        if v and v.casefold()!=answer.casefold() and v.casefold() not in [u.casefold() for u in unique]: unique.append(v)
    return unique[:3]

def make_question(item, pos, topic, prefix):
    correct=str(item['answer']).strip().rstrip('.')
    choices=[correct]+distractors(item,topic)
    while len(choices)<4: choices.append(f'No valid conclusion {len(choices)}')
    shift=pos%4
    choices=choices[shift:]+choices[:shift]
    ids=list('abcd')
    correct_id=ids[choices.index(correct)]
    explanation=str(item['solutionOutline']).strip()
    if not explanation.endswith('.'): explanation+='.'
    trap=str(item.get('commonTrap','')).strip()
    if trap: explanation+=f' A common error is {trap[0].lower()+trap[1:] if len(trap)>1 else trap}'
    return {'id':f'{prefix}-{item["id"].split("-")[-1]}','type':'multipleChoice','prompt':str(item['prompt']).strip(),
            'choices':[{'id':i,'text':t} for i,t in zip(ids,choices)],'answer':{'choiceId':correct_id},'explanation':explanation}

def assessment(info,kind,level,selected):
    base=info['topic']
    if level=='easy': aid=f'{base}-{kind}'
    else: aid=f'{base}-{level}-{kind}'
    label={'easy':'Easy','hard':'Hard','olympiad':'Olympiad'}[level]
    is_test=kind=='test'
    return {'schemaVersion':1,'id':aid,'title':f'{info["label"]}: {label} {kind.title()}',
      'assessmentType':kind,'categoryId':'art-of-problem-solving','topicId':info['topic'],
      'modeDefault':'scored' if is_test else 'practice','randomizeQuestions':True,
      'navigation':{'learningGoal':'evaluate' if is_test else 'practice','activityType':'formalTest' if is_test else ('mixedPractice' if level in ('hard','olympiad') else 'focusedPractice'),
                    'tags':['art-of-problem-solving',info['topic'],'aops-volume-1',f'chapter-{info["chapter"]}',level,kind,'geometry']},
      'skills':info['skills'],'questions':[make_question(x,i,info['topic'],f'{level}-{kind}') for i,x in enumerate(selected,1)]}

def diversified(pool):
    """Interleave archetypes so one assessment never becomes a numeric variant drill."""
    groups={}
    for item in pool:
        key=item.get('archetype') or item.get('concept') or 'mixed'
        groups.setdefault(key,[]).append(item)
    ordered=[]
    while any(groups.values()):
        for key in sorted(groups):
            if groups[key]: ordered.append(groups[key].pop(0))
    return ordered

for key,info in TOPICS.items():
    bank=yaml.safe_load((BANK/info['bank']).read_text(encoding='utf-8'))['items']
    by={'easy':[x for x in bank if x['difficulty']=='foundational'],
        'hard':[x for x in bank if x['difficulty']=='intermediate'],
        'olympiad':[x for x in bank if x['difficulty']=='advanced']}
    for level,pool in by.items():
        pool=diversified(pool)
        assert len(pool)>=30,(key,level,len(pool))
        for kind,offset in [('quiz',0),('test',15)]:
            data=assessment(info,kind,level,pool[offset:offset+15])
            (OUT/f'{data["id"]}.yaml').write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=1000),encoding='utf-8')
            print(data['id'],len(data['questions']))

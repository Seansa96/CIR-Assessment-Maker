import yaml,glob,os,re,collections
fs=[f for f in glob.glob('data/assessments/*.yaml') if any(x in os.path.basename(f) for x in ['chem-acids','chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations'])]
for f in fs:
 a=yaml.safe_load(open(f,encoding='utf8')); qs=a.get('questions',[])
 if qs:
  prompts=[re.sub(r'\W+',' ',q.get('prompt','').lower()).strip() for q in qs]; choices=[re.sub(r'\W+',' ',c.get('text','').lower()).strip() for q in qs for c in q.get('choices',[])[1:]]
  dp=[x for x,n in collections.Counter(prompts).items() if n>1]; dc=[x for x,n in collections.Counter(choices).items() if n>1]
  print(os.path.basename(f), 'q',len(qs),'prompt_dupes',len(dp),'distractor_dupes',len(dc))
 elif a.get('lesson',{}).get('sections'):
  ss=a['lesson']['sections']; ex=[s['check'].get('explanation','') for s in ss]; print(os.path.basename(f),'sections',len(ss),'checks',len(ex),'explanation_dupes',len(ex)-len(set(ex)))
 elif a.get('items'): print(os.path.basename(f),'items',len(a['items']))
 elif a.get('glossary'): print(os.path.basename(f),'glossary entries',sum(len(s.get('entries',[])) for s in a['glossary'].get('sections',[])))
 elif a.get('workedExamples'): print(os.path.basename(f),'worked examples',len(a['workedExamples']))

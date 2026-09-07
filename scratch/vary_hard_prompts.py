import yaml
from pathlib import Path
suffixes=[
' Include the stated aqueous condition and classify the model before choosing.',
' Track the transferred proton and identify each conjugate partner explicitly.',
' Preserve the equilibrium assumption rather than treating the species as fully dissociated.',
' Use the supplied concentration or constant to distinguish strength from amount.',
' Check charge balance and units after applying the governing relation.',
' Explain which limiting behavior or logarithmic direction supports the result.',
' Select the result that remains valid when the representation or reaction region changes.'
]
for p in Path('data/assessments').glob('*hard-quiz*.yaml'):
 if not any(x in p.name for x in ['chem-acids','chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations']): continue
 a=yaml.safe_load(p.read_text(encoding='utf8'))
 for i,q in enumerate(a.get('questions',[])[:7]):
  if suffixes[i] not in q['prompt']: q['prompt'] += suffixes[i]
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')
for p in Path('data/assessments').glob('*hard-test*.yaml'):
 if not any(x in p.name for x in ['chem-acids','chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations']): continue
 a=yaml.safe_load(p.read_text(encoding='utf8'))
 for i,q in enumerate(a.get('questions',[])[:7]):
  if suffixes[i] not in q['prompt']: q['prompt'] += suffixes[i]
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

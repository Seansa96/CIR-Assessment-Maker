import yaml
from pathlib import Path
mp={'chem-acids':'packet-chemistry-acids-foundations-v1','chemistry-acid-base-reactions':'packet-chemistry-acid-base-reactions-v1','chemistry-acids-bases':'packet-chemistry-acids-bases-equilibrium-v1','chemistry-ph-water':'packet-chemistry-ph-water-calculus-v1','chemistry-titrations':'packet-chemistry-titrations-analysis-v1'}
for p in Path('data/assessments').glob('*.yaml'):
 if not any(x in p.name for x in ['chem-acids','chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations']): continue
 a=yaml.safe_load(p.read_text(encoding='utf8')); t=a.get('topicId');
 if t not in mp or 'authoring' not in a: continue
 a['authoring']['sourcePacketId']=mp[t]
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

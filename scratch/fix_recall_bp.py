import yaml
from pathlib import Path
mp={'chemistry-acid-base-reactions-recall-v1.yaml':'chunk-0419','chemistry-acids-bases-recall-v1.yaml':'chunk-1836','chemistry-ph-water-recall-v1.yaml':'chunk-1842','chemistry-titrations-recall-v1.yaml':'chunk-0455'}
for fn,ch in mp.items():
 p=Path('docs/assessment-reference/question-blueprints')/fn; a=yaml.safe_load(p.read_text(encoding='utf8'))
 for b in a.get('blueprints',[]): b['sourceChunks']=['src-20260720035703-91ea51b0d8:'+ch]
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

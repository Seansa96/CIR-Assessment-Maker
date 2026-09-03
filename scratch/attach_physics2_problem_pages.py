import json, re, subprocess
from pathlib import Path

root=Path(r"C:\Users\SeanS\OneDrive\Documents\Obsidian\Lexicon of the Arcane\18 - Physics\OpenStax University Physics Volume 2\Practice Problems")
src=Path(r"C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260806094518-3f5d8d0e38")
starts=[100,207,272,340,429,506,598,668,759,855,926,998,1071,1130,1183,1260]
chunks=json.loads((src/"chunks.json").read_text(encoding="utf8"))
cue=re.compile(r"\b(figure|figures|diagram|drawing|shown (?:below|here)|accompanying|graph|chart|table below|image)\b",re.I)
locations={}
for ch,start in enumerate(starts,1):
  end=starts[ch] if ch<len(starts) else 1298
  for c in chunks:
    if not start<=c["ordinal"]<end: continue
    page=re.search(r"# PAGE (\d+)",c["text"])
    if not page: continue
    for m in re.finditer(r"(?m)^\s*(\d{1,3})\s+\.\s+",c["text"]):
      b=c["text"][m.start():m.start()+1600]
      if cue.search(b): locations[(ch,m.group(1))]=int(page.group(1))
assets=root/"assets"; assets.mkdir(exist_ok=True); attached=[]
for note in root.glob("Chapter * Practice Problems.md"):
  ch=int(re.search(r"Chapter (\d+)",note.name).group(1)); text=note.read_text(encoding="utf8")
  def add(m):
    n=m.group(1); page=locations.get((ch,n))
    if not page or f"![[assets/physics2-ch{ch}-problem-{n}-page-{page}.png]]" in text: return m.group(0)
    name=f"physics2-ch{ch}-problem-{n}-page-{page}.png"; target=assets/name
    if not target.exists():
      subprocess.run(["pdftoppm","-f",str(page),"-l",str(page),"-singlefile","-png","-r","144",str(src/"original.pdf"),str(target.with_suffix(""))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    attached.append((ch,n)); return m.group(0)+f"\n\n![[assets/{name}]]"
  text=re.sub(r"(?m)^# Problem (\d{1,3})$",add,text)
  note.write_text(text,encoding="utf8")

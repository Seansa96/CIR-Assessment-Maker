from __future__ import annotations
import json, re
from pathlib import Path

source = Path(r"C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260806094518-3f5d8d0e38")
dest = Path(r"C:\Users\SeanS\OneDrive\Documents\Obsidian\Lexicon of the Arcane\18 - Physics\OpenStax University Physics Volume 2\Practice Problems")
# First source chunk containing each chapter's chapter-review problem material.
starts = [100, 207, 272, 340, 429, 506, 598, 668, 759, 855, 926, 998, 1071, 1130, 1183, 1260]

def clean(s: str) -> str:
    s = re.sub(r"(?m)^# PAGE \d+\s*$", "", s)
    s = re.sub(r"(?m)^\s*\d+\s*•\s*Chapter Review.*$", "", s)
    s = re.sub(r"(?m)^Access for free at openstax\.org\s*$", "", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()

def blocks(text: str) -> dict[int, str]:
    pat = re.compile(r"(?m)^\s*(\d{1,3})\s+\.\s+")
    ms = list(pat.finditer(text))
    out = {}
    for i,m in enumerate(ms):
        n = int(m.group(1)); end = ms[i+1].start() if i+1<len(ms) else len(text)
        b = clean(text[m.start():end])
        if n not in out or len(b)>len(out[n]): out[n]=b
    return out

chunks=json.loads((source/"chunks.json").read_text(encoding="utf-8"))
answer_text="\n".join(c["text"] for c in chunks if c["ordinal"]>=1298)
markers=list(re.finditer(r"(?m)^Chapter (\d{1,2})\s*$", answer_text))
answer_sections={}
for i,m in enumerate(markers):
    n=int(m.group(1)); end=markers[i+1].start() if i+1<len(markers) else len(answer_text)
    if n not in answer_sections: answer_sections[n]=answer_text[m.end():end]

dest.mkdir(parents=True, exist_ok=True)
verify=["# OpenStax University Physics, Volume 2 - Practice Problems","","Only exercises with a source-provided Answer Key entry are included.",""]
for ch,start in enumerate(starts,1):
    end=starts[ch] if ch<len(starts) else 1298
    raw="\n".join(c["text"] for c in chunks if start<=c["ordinal"]<end)
    pos=raw.lower().find("\nproblems")
    if pos>=0: raw=raw[pos:]
    qs=blocks(raw)
    answer_raw = answer_sections.get(ch, "")
    # The Answer Key begins with conceptual-question answers. Keep only the
    # separately labelled Problems portion so identically numbered conceptual
    # items cannot be paired with a problem prompt.
    answer_pos = answer_raw.lower().find("\nproblems")
    if answer_pos >= 0:
        answer_raw = answer_raw[answer_pos:]
    ans=blocks(answer_raw)
    nums=sorted(set(qs)&set(ans))
    title=f"Chapter {ch} Practice Problems"
    p=["# "+title,"","## Extracted problems",""]
    s=["# "+title+" Solutions","","Source-provided Answer Key entries.",""]
    for n in nums:
        p += [f"# Problem {n}","",qs[n],""]
        s += [f"# Problem {n}","",ans[n],""]
    (dest/(title+".md")).write_text("\n".join(p).rstrip()+"\n",encoding="utf-8")
    (dest/(title+" Solutions.md")).write_text("\n".join(s).rstrip()+"\n",encoding="utf-8")
    verify.append(f"- Chapter {ch}: {len(nums)} matched headings - "+", ".join(map(str,nums)))
(dest/"Extraction Verification.md").write_text("\n".join(verify)+"\n",encoding="utf-8")

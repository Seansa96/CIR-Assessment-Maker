from pathlib import Path
import json,re

source=Path(r"C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260910183147-0bc11b67fa\chunks.json")
root=Path(r"C:\Users\SeanS\OneDrive\Documents\Obsidian\Lexicon of the Arcane\18 - Physics\Physics Young and Freedman\Practice Problems")
chunks=json.load(open(source,encoding='utf-8'))
targets=[(5,65),(7,45),(7,71),(10,7),(17,67),(18,67)]

def tidy(text):
    return re.sub(r"\s+"," ",text).strip()

for chapter,number in targets:
    label=f"{chapter}.{number}"
    next_label=rf"(?<!\d){chapter}\.{number+1}\b"
    candidates=[]
    for chunk in chunks:
        text=chunk.get("text","")
        for match in re.finditer(rf"(?<!\d){re.escape(label)}\b",text):
            following=re.search(next_label,text[match.end():])
            segment=text[match.end():match.end()+(following.start() if following else min(len(text)-match.end(),1200))]
            # Exercise chunks normally contain a number, difficulty dot, or a
            # question mark immediately after the label; contents entries do not.
            if len(tidy(segment))>30:
                candidates.append(segment)
    if not candidates:
        continue
    prompt=tidy(max(candidates,key=len))
    note=root/f"Chapter {chapter} Practice Problems.md"
    text=note.read_text(encoding='utf-8')
    # These labels are not reliably present in the question extraction. Remove
    # any speculative fallback block rather than admitting answer-key text into
    # a question-only collection.
    text=re.sub(rf"(?ms)\n# Problem {re.escape(label)}\n.*?(?=\n# Problem |\Z)","\n",text)
    note.write_text(text,encoding='utf-8')

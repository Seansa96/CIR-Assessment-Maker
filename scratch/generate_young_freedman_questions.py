"""Create question-only Young & Freedman practice notes from answer-key coverage."""
from pathlib import Path
import re
import fitz
import sys
import json

SOURCE = Path(r"C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260910183147-0bc11b67fa\original.pdf")
ROOT = Path(r"C:\Users\SeanS\OneDrive\Documents\Obsidian\Lexicon of the Arcane\18 - Physics\Physics Young and Freedman")
OUT = ROOT / "Practice Problems"
ASSETS = OUT / "assets"
pdf = fitz.open(SOURCE)
OUT.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(exist_ok=True)

# The appendix itself defines the inclusion set: odd-numbered problems with
# an answer entry. It is intentionally used only for selection here; no answer
# text is written into the question notes.
answers = set()
for index in range(1556, 1571):
    for chapter, number in re.findall(r"(?m)^\s*(\d{1,2})\.(\d+)\s*$", pdf[index].get_text()):
        if 1 <= int(chapter) <= 44 and int(number) % 2:
            answers.add((int(chapter), int(number)))

pages = [(page, page.get_text()) for page in pdf[:1556]]
chunks=json.load(open(SOURCE.with_name("chunks.json"),encoding="utf-8"))
question_index={}
loose_index={}
fallback_index={}
current_page=None
label_pattern=re.compile(r"(?m)^\s*(\d{1,2})\.(\d+)\s*(?:\n\s*)?\.+\s+")
loose_pattern=re.compile(r"(?m)^\s*(\d{1,2})\.(\d+)\s*(?:\n\s*)?\.?\s+")
for chunk in chunks:
    page_marker=re.search(r"(?m)^# PAGE (\d+)",chunk.get("text", ""))
    if page_marker:
        current_page=int(page_marker.group(1))
    if chunk.get("pageNumber"):
        current_page=chunk["pageNumber"]
    text=chunk.get("text", "")
    for match in re.finditer(r"(?<!\d)(\d{1,2})\.(\d+)\b", text):
        key=(int(match.group(1)),int(match.group(2)))
        if key in answers:
            fallback_index.setdefault(key,[]).append((current_page or 0,match.start(),match.end(),text))
    if current_page and current_page >= 1557:
        continue
    for match in label_pattern.finditer(text):
        key=(int(match.group(1)),int(match.group(2)))
        if key in answers:
            question_index.setdefault(key,[]).append((current_page or 0,match.start(),match.end(),text))
    for match in loose_pattern.finditer(text):
        key=(int(match.group(1)),int(match.group(2)))
        if key in answers:
            loose_index.setdefault(key,[]).append((current_page or 0,match.start(),match.end(),text))

def tidy(value: str) -> str:
    value = re.sub(r"(?m)^\s*\d+\s+(?:CHAPTER|Questions|Exercises|Problems).*\n?", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value.replace("- ", "").replace("  ", " ")

def find_question(chapter: int, number: int):
    candidates=question_index.get((chapter,number),[])
    if not candidates:
        candidates=loose_index.get((chapter,number),[])
    if not candidates:
        candidates=fallback_index.get((chapter,number),[])
    if not candidates:
        return None
    # The chunked source preserves the end-of-chapter question layout and its
    # difficulty dots, avoiding false matches from chapter contents/headings.
    page_number, start, match_end, text=candidates[0]
    next_label=re.compile(rf"(?m)^\s*{chapter}\.\d+\s*(?:\n\s*)?\.?\s+")
    following=next_label.search(text,match_end)
    return page_number - 1, tidy(text[match_end:following.start() if following else len(text)])

def crop_figure(chapter: int, number: int, page_index: int):
    page, _ = pages[page_index]
    label=f"{chapter}.{number}"
    rects=[r for r in page.search_for(label) if r.x0 < 125 or 285 < r.x0 < 360]
    if not rects:
        return None
    start=max(rects,key=lambda r:r.y0)
    left=start.x0 < page.rect.width/2
    x0,x1=(52,306) if left else (306,560)
    end_y=page.rect.height-50
    for following in range(number+1,number+14):
        for rect in page.search_for(f"{chapter}.{following}"):
            at_margin=rect.x0 < 125 or 285 < rect.x0 < 360
            if at_margin and (rect.x0 < page.rect.width/2)==left and rect.y0 > start.y0+8:
                end_y=min(end_y,rect.y0-7)
    clip=fitz.Rect(x0,max(16,start.y0-10),x1,max(start.y0+48,end_y))
    name=f"young-freedman-ch{chapter}-problem-{number}.png"
    page.get_pixmap(matrix=fitz.Matrix(2.35,2.35),clip=clip,alpha=False).save(ASSETS/name)
    return name

chapter_counts={}
unlocated=[]
figures=0
start_chapter=int(sys.argv[1]) if len(sys.argv)>1 else 1
end_chapter=int(sys.argv[2]) if len(sys.argv)>2 else 44
for chapter in range(start_chapter,end_chapter+1):
    selected=sorted(number for ch,number in answers if ch==chapter)
    content=[
        f"# Young & Freedman University Physics - Chapter {chapter} Practice Problems",
        "",
        "> [!note] Answer-key-backed selection",
        "> Includes only odd-numbered problems that have a corresponding entry in the textbook's answer appendix. Worked solutions will be added separately.",
        "",
    ]
    found=0
    for number in selected:
        located=find_question(chapter,number)
        if not located:
            unlocated.append(f"{chapter}.{number}")
            continue
        page_index, prompt=located
        if len(prompt)<20:
            unlocated.append(f"{chapter}.{number}")
            continue
        content.extend([f"# Problem {chapter}.{number}", "", f"{chapter}.{number} {prompt}"])
        if page_index >= 0 and re.search(r"\b(?:fig(?:ure)?\.?|shown|diagram|illustration)\b", prompt, re.I):
            image=crop_figure(chapter,number,page_index)
            if image:
                content.extend(["", "> [!figure] Original figure and notation", f"> ![[assets/{image}]]"])
                figures += 1
        content.append("")
        found += 1
    (OUT/f"Chapter {chapter} Practice Problems.md").write_text("\n".join(content).rstrip()+"\n",encoding="utf-8")
    chapter_counts[chapter]=found

if start_chapter == 1 and end_chapter == 44:
    coverage=["# Young & Freedman University Physics - Answer-Key Coverage", "", "This collection contains only prompts with a corresponding odd-numbered answer entry in the textbook appendix.", ""]
    for chapter in range(1,45):
        coverage.append(f"- Chapter {chapter}: {chapter_counts[chapter]} prompts")
    (OUT/"Answer-Key Coverage.md").write_text("\n".join(coverage)+"\n",encoding="utf-8")
print(f"Questions written: {sum(chapter_counts.values())}")
print(f"Figure crops written: {figures}")
print(f"Unlocated entries: {len(unlocated)}")
print(" ".join(unlocated))

"""Batch-polish Physics 2 prompt notes and localize their legacy PDF captures."""
from pathlib import Path
import re
import fitz

ROOT = Path(r"C:\Users\SeanS\OneDrive\Documents\Obsidian\Lexicon of the Arcane\18 - Physics\OpenStax University Physics Volume 2\Practice Problems")
PDF_PATH = Path(r"C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260806094518-3f5d8d0e38\original.pdf")
ASSETS = ROOT / "assets"
MANUAL_SOURCE_PAGES = {
    ("7", "67"): 330,
    ("10", "45"): 468,
    ("14", "61"): 630,
}

def normalize(value: str) -> str:
    value = value.lower().replace("-\n", "")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()

pdf = fitz.open(PDF_PATH)
pages = [(page, page.get_text(), normalize(page.get_text())) for page in pdf]

def locate(chapter: str, number: str, prompt: str):
    manual_page = MANUAL_SOURCE_PAGES.get((chapter, number))
    if manual_page:
        page, _, _ = pages[manual_page - 1]
        rectangles = [r for r in page.search_for(number) if r.x0 < 125 or 285 < r.x0 < 360]
        if rectangles:
            return manual_page - 1, max(rectangles, key=lambda r: r.y0)
    words = normalize(re.sub(rf"^\s*{re.escape(number)}\s*\.?\s*", "", prompt)).split()
    for length in (12, 8, 5):
        phrase = " ".join(words[:length])
        candidates=[]
        for index, (page, _, normalized_text) in enumerate(pages):
            if phrase not in normalized_text:
                continue
            rectangles=[]
            for rect in page.search_for(number):
                if rect.x0 < 125 or 285 < rect.x0 < 360:
                    rectangles.append(rect)
            if len(rectangles) == 1:
                candidates.append((index, rectangles[0]))
        if len(candidates) == 1:
            return candidates[0]
    return None

def crop_exercise(chapter: str, number: str, prompt: str):
    located = locate(chapter, number, prompt)
    if not located:
        return None
    index, start = located
    page, _, _ = pages[index]
    left = start.x0 < page.rect.width / 2
    col_left, col_right=(52,306) if left else (306,560)
    end_y=page.rect.height-54
    for following in range(int(number)+1, int(number)+13):
        for rect in page.search_for(str(following)):
            at_margin=rect.x0 < 125 or 285 < rect.x0 < 360
            same_column=(rect.x0 < page.rect.width/2)==left
            if at_margin and same_column and rect.y0 > start.y0+8:
                end_y=min(end_y,rect.y0-7)
    clip=fitz.Rect(col_left,max(16,start.y0-10),col_right,max(start.y0+48,end_y))
    output=ASSETS/f"physics2-ch{chapter}-problem-{number}-source.png"
    page.get_pixmap(matrix=fitz.Matrix(2.35,2.35),clip=clip,alpha=False).save(output)
    return output.name

asset_pattern=re.compile(r"assets/physics2-ch(\d+)-problem-(\d+)-(?:page-\d+|source)\.png")
heading_pattern=re.compile(r"(?m)^# Problem (\d+)\s*$")

processed=linked=0
unlocated=[]
for note in sorted(ROOT.glob("Chapter * Practice Problems.md")):
    if note.name.startswith("Chapter 5 "):
        continue
    chapter_match=re.match(r"Chapter (\d+) Practice Problems\.md",note.name)
    if not chapter_match:
        continue
    chapter=chapter_match.group(1)
    text=note.read_text(encoding="utf-8")
    text=text.replace(" # Problem ","\n\n# Problem ")
    text=re.sub(r"(?<!\n)# Problem ","\n\n# Problem ",text)
    text=re.sub(r"(?m)^(# Problem \d+)\s+(?=\d+\s*\.)",r"\1\n\n",text)
    headings=set(heading_pattern.findall(text))
    legacy=set((ch,num) for ch,num in asset_pattern.findall(text) if ch==chapter)
    for asset in ASSETS.glob(f"physics2-ch{chapter}-problem-*-page-*.png"):
        found=re.fullmatch(rf"physics2-ch{chapter}-problem-(\d+)-page-\d+\.png",asset.name)
        if found and found.group(1) in headings:
            legacy.add((chapter,found.group(1)))

    text=re.sub(r"(?m)^> \[!figure\] Original figure and notation\s*$\n?","",text)
    text=re.sub(r"(?m)^> \!\[\[assets/physics2-ch\d+-problem-\d+-(?:page-\d+|source)\.png\]\]\s*$\n?","",text)
    text=re.sub(r"\n*\!\[\[assets/physics2-ch\d+-problem-\d+-(?:page-\d+|source)\.png(?:\|\d+)?\]\]","",text)
    text=text.replace("## Extracted problems","> [!note] Source-faithful practice set\n> Cropped source figures preserve diagrams and mathematical notation that the PDF text layer does not represent reliably.")

    matches=list(heading_pattern.finditer(text))
    rebuilt=[]; cursor=0
    for pos, match in enumerate(matches):
        rebuilt.append(text[cursor:match.start()])
        end=matches[pos+1].start() if pos+1<len(matches) else len(text)
        body=text[match.end():end]
        body=re.sub(r"(?m)^\s*\d{1,3}\s+\d+\s+• Chapter Review\s*$","",body)
        body=re.sub(r"(?m)^Access for free at openstax\.org\s*$","",body)
        body=re.sub(r"\s+"," ",body).strip()
        body=body.replace("lower- right","lower-right").replace("s ame","same")
        number=match.group(1)
        crop=None
        if (chapter,number) in legacy:
            crop=crop_exercise(chapter,number,body)
            if not crop:
                unlocated.append(f"{note.name}: {number}")
        visual=f"\n\n> [!figure] Original figure and notation\n> ![[assets/{crop}]]" if crop else ""
        if crop:
            linked+=1
        rebuilt.append(f"{match.group(0)}\n\n{body}{visual}\n\n")
        cursor=end
    rebuilt.append(text[cursor:])
    result=re.sub(r"\n{3,}","\n\n","".join(rebuilt)).rstrip()+"\n"
    note.write_text(result,encoding="utf-8")
    processed+=1

print(f"Processed notes: {processed}")
print(f"Localized crop embeds: {linked}")
print(f"Unlocated source exercises: {len(unlocated)}")
for item in unlocated:
    print(item)

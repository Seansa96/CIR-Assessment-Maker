"""Batch-polish Chemistry practice prompts and replace broad page images.

The source PDF has a searchable exercise-number layer.  This script uses it
instead of the legacy image filenames, which were not reliable page locators.
"""
from pathlib import Path
import re
import fitz

ROOT = Path(r"C:\Users\SeanS\OneDrive\Documents\Obsidian\Lexicon of the Arcane\17 - Chemistry\Chemistry - The Central Science (14th Edition)\Practice Problems")
PDF_PATH = Path(r"C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260720035703-91ea51b0d8\original.pdf")
ASSETS = ROOT / "assets"
MANUAL_SOURCE_PAGES = {
    ("3", "5"): 151,
    ("9", "3"): 424,
    ("10", "3"): 465,
    ("11", "59"): 507,
    ("19", "1"): 878,
}

pdf = fitz.open(PDF_PATH)
def normalize(value: str) -> str:
    value = value.lower().replace("-\n", "")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()

pages = []
for page in pdf:
    page_text = page.get_text()
    labels = []
    for word in page.get_text("words"):
        token = word[4].rstrip(".,")
        match = re.fullmatch(r"(\d{1,2})\.(\d+)", token)
        # Exercises are printed at a column margin; section labels are not.
        if match and (word[0] < 112 or 285 < word[0] < 350):
            labels.append((match.group(1), match.group(2), fitz.Rect(word[:4])))
    pages.append((page, labels, page_text, normalize(page_text)))

def locate(chapter: str, exercise: str, prompt: str):
    manual_page = MANUAL_SOURCE_PAGES.get((chapter, exercise))
    if manual_page:
        _, labels, _, _ = pages[manual_page - 1]
        matching = [rect for found_chapter, found_exercise, rect in labels if (found_chapter, found_exercise) == (chapter, exercise)]
        if matching:
            return manual_page - 1, matching[0]
    prompt_words = normalize(re.sub(rf"^\s*{re.escape(chapter)}\.{re.escape(exercise)}\s*", "", prompt)).split()
    # The long phrase distinguishes the exercise from a table of contents or
    # a section reference.  Shorter fallbacks accommodate badly OCR'd prompts
    # and continuation pages that do not repeat the "Exercises" running head.
    for length in (12, 8, 5):
        phrase = " ".join(prompt_words[:length])
        matches = []
        for index, (_, labels, _, normalized_text) in enumerate(pages):
            if phrase not in normalized_text:
                continue
            for found_chapter, found_exercise, rect in labels:
                if (found_chapter, found_exercise) == (chapter, exercise):
                    matches.append((index, rect))
        if len(matches) == 1:
            return matches[0]
    return None

def crop_exercise(chapter: str, exercise: str, prompt: str):
    located = locate(chapter, exercise, prompt)
    if not located:
        return None
    index, start = located
    page, labels, _, _ = pages[index]
    left_column = start.x0 < page.rect.width / 2
    col_left, col_right = (52, 306) if left_column else (306, 560)
    end_y = page.rect.height - 52
    for found_chapter, found_exercise, rect in labels:
        if found_chapter != chapter:
            continue
        if (rect.x0 < page.rect.width / 2) == left_column and rect.y0 > start.y0 + 8:
            end_y = min(end_y, rect.y0 - 7)
    clip = fitz.Rect(col_left, max(16, start.y0 - 10), col_right, max(start.y0 + 48, end_y))
    output = ASSETS / f"chemistry-problem-{chapter}-{exercise}-source.png"
    page.get_pixmap(matrix=fitz.Matrix(2.35, 2.35), clip=clip, alpha=False).save(output)
    return output.name

asset_pattern = re.compile(r"assets/chemistry-problem-(\d+)-(\d+)-(?:page-\d+|source)\.png")
problem_heading = re.compile(r"(?m)^# Problem (\d+)\.(\d+)\s*$")

processed_notes = 0
linked_crops = 0
unlocated = []

for note in sorted(ROOT.glob("*.md")):
    if " Solutions" in note.name or note.name in {"Diagram Attachment Verification.md", "Extraction Verification.md"}:
        continue
    text = note.read_text(encoding="utf-8")
    # A few legacy extracts glued a subsequent heading to the previous prompt.
    text = text.replace(" # Problem ", "\n\n# Problem ")
    text = re.sub(r"(?<!\n)# Problem ", "\n\n# Problem ", text)
    text = re.sub(r"(?m)^(# Problem \d+\.\d+)\s+(?=\d+\.\d+\s)", r"\1\n\n", text)
    heading_ids = set(problem_heading.findall(text))
    legacy_assets = set(asset_pattern.findall(text))
    # Retain the original attachment set even if a previous repair pass
    # temporarily removed an embed after failing to locate its source page.
    for asset in ASSETS.glob("chemistry-problem-*-*-page-*.png"):
        found = re.fullmatch(r"chemistry-problem-(\d+)-(\d+)-page-\d+\.png", asset.name)
        if found and found.groups() in heading_ids:
            legacy_assets.add(found.groups())
    # Figure callouts from a prior pass are regenerated below.
    text = re.sub(r"(?m)^> \[!figure\] Original figure and notation\s*$\n?", "", text)
    text = re.sub(r"(?m)^> \!\[\[assets/chemistry-problem-\d+-\d+-(?:page-\d+|source)\.png\]\]\s*$\n?", "", text)
    crop_by_problem = {}
    # Remove legacy broad captures; each crop is placed under its own prompt.
    text = re.sub(r"\n*\!\[\[assets/chemistry-problem-\d+-\d+-(?:page-\d+|source)\.png(?:\|\d+)?\]\]", "", text)
    text = re.sub(r"(?m)^\s*(Exercises|Additional Exercises)\s+\d*\s*$", "", text)
    text = text.replace("## Extracted problems", "> [!note] Source-faithful practice set\n> Cropped source figures preserve diagrams and mathematical notation that the PDF text layer does not represent reliably.")

    # Clean only inside individual exercise blocks, leaving the note hierarchy intact.
    matches = list(problem_heading.finditer(text))
    rebuilt = []
    cursor = 0
    for pos, match in enumerate(matches):
        rebuilt.append(text[cursor:match.start()])
        end = matches[pos + 1].start() if pos + 1 < len(matches) else len(text)
        heading = match.group(0)
        body = text[match.end():end]
        body = re.sub(r"(?m)^\s*\d{1,3}\s+(CHAPTER|Exercises).*\n?", "", body)
        body = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", body)
        body = re.sub(r"\s+", " ", body).strip()
        body = body.replace("mi - croscope", "microscope").replace("bra ss", "brass")
        body = body.replace("den- sity", "density").replace("calcu - late", "calculate")
        identity = (match.group(1), match.group(2))
        crop = crop_by_problem.get(identity)
        if identity in legacy_assets and not crop:
            crop = crop_exercise(*identity, body)
            if crop:
                crop_by_problem[identity] = crop
            else:
                unlocated.append(f"{note.name}: {identity[0]}.{identity[1]}")
        visual = f"\n\n> [!figure] Original figure and notation\n> ![[assets/{crop}]]" if crop else ""
        if crop:
            linked_crops += 1
        rebuilt.append(f"{heading}\n\n{body}{visual}\n\n")
        cursor = end
    rebuilt.append(text[cursor:])
    result = "".join(rebuilt)
    result = re.sub(r"\n{3,}", "\n\n", result).rstrip() + "\n"
    note.write_text(result, encoding="utf-8")
    processed_notes += 1

print(f"Processed notes: {processed_notes}")
print(f"Localized crop embeds: {linked_crops}")
print(f"Unlocated source exercises: {len(unlocated)}")
for item in unlocated:
    print(item)

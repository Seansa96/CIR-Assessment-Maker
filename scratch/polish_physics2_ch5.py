import re
from pathlib import Path
import fitz

root=Path(r"C:\Users\SeanS\OneDrive\Documents\Obsidian\Lexicon of the Arcane\18 - Physics\OpenStax University Physics Volume 2\Practice Problems")
note=root/"Chapter 5 Practice Problems.md"
assets=root/"assets"
pdf=fitz.open(r"C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260806094518-3f5d8d0e38\original.pdf")

for image in assets.glob("physics2-ch5-problem-*-page-*.png"):
    m=re.search(r"problem-(\d+)-page-(\d+)",image.name)
    number, page_no=map(int,m.groups())
    page=pdf[page_no-1]
    words=page.get_text("words")
    hits=[w for w in words if re.fullmatch(fr"{number}\s*\.",w[4])]
    if not hits: continue
    x0,y0,x1,y1,_=hits[0]
    mid=page.rect.width/2
    left=x0<mid
    col_words=[w for w in words if (w[0]<mid)==left]
    starts=[w for w in col_words if re.fullmatch(r"\d+\s*\.",w[4]) and w[1]>y0+8]
    y_end=min((w[1] for w in starts), default=page.rect.height-24)-5
    clip=fitz.Rect(18 if left else mid+4,max(18,y0-8),mid-4 if left else page.rect.width-18,max(y0+45,y_end))
    pix=page.get_pixmap(matrix=fitz.Matrix(2.25,2.25),clip=clip,alpha=False)
    pix.save(str(image))

visual_problems={55,59,63,83,87,95,97,103,105,107,109,111,115,117,125}

def problem_rect(number):
    """Locate an exercise number in the review pages, avoiding incidental numbers."""
    candidates=[]
    for index in range(210,232):
        page=pdf[index]
        for rect in page.search_for(str(number)):
            if rect.x0 < 120 or 290 < rect.x0 < 360:
                candidates.append((index,rect))
    # A real problem number begins at the margin; use the last hit when an
    # earlier page happens to contain the same number in the prose.
    return candidates[-1] if candidates else None

for number in visual_problems:
    located=problem_rect(number)
    if not located:
        continue
    index, start=located
    page=pdf[index]
    left=start.x0 < page.rect.width/2
    col_left, col_right=(54,306) if left else (306,558)
    next_y=page.rect.height-58
    for following in range(number+1, number+12):
        for rect in page.search_for(str(following)):
            same_column=(rect.x0 < page.rect.width/2)==left
            at_margin=(rect.x0 < 120 or 290 < rect.x0 < 360)
            if same_column and at_margin and rect.y0 > start.y0+10:
                next_y=min(next_y,rect.y0-7)
    clip=fitz.Rect(col_left,max(18,start.y0-10),col_right,max(start.y0+44,next_y))
    image=assets/f"physics2-ch5-problem-{number}-source.png"
    pix=page.get_pixmap(matrix=fitz.Matrix(2.4,2.4),clip=clip,alpha=False)
    pix.save(str(image))

# A few exercises split the prompt and its visual across columns/pages.  Keep
# those visual continuations as their own tight crop instead of reverting to a
# whole-page screenshot.
detail_clips={
    55:(221,fitz.Rect(54,18,306,394)),
    95:(224,fitz.Rect(54,18,306,370)),
    107:(226,fitz.Rect(54,18,306,222)),
    117:(227,fitz.Rect(306,48,558,204)),
}
for number,(index,clip) in detail_clips.items():
    image=assets/f"physics2-ch5-problem-{number}-detail.png"
    pdf[index].get_pixmap(matrix=fitz.Matrix(2.4,2.4),clip=clip,alpha=False).save(str(image))

text=note.read_text(encoding="utf-8")
# Start from the structured text, removing the old broad page captures.
text=re.sub(r"\n*\!\[\[assets/physics2-ch5-problem-[^\n]+\]\]", "", text)
text=re.sub(r"(?m)^> \!\[\[assets/physics2-ch5-problem-[^\n]+\]\]\s*$\n?", "", text)
text=re.sub(r"(?m)^> \[!figure\] Original figure and notation.*\n?", "", text)
# Remove running heads/footers and restore normal paragraph wrapping.
text=re.sub(r"(?m)^\d{3}\s+5\s+• Chapter Review\s*$", "", text)
text=re.sub(r"(?m)^Access for free at openstax\.org\s*$", "", text)
text=re.sub(r"\n\s*\n\s*(shown below|shown here|there is|and along|hydrogen atom)", r" \1", text)
text=re.sub(r"(?<!\n)\n(?!\n)", " ", text)
text=re.sub(r"\n{3,}", "\n\n", text)
text=text.replace("s ame", "same").replace("lower- right", "lower-right")
text=text.replace("resul ting", "resulting").replace("charge\n\nconfigurations", "charge configurations")
text=text.replace("Q/2", "$Q/2$")
for title in ["5.3 Coulomb's Law","5.5 Calculating Electric Fields of Charge Distributions","5.6 Electric Field Lines","Additional Problems"]:
    text=text.replace("\n"+title+"\n",f"\n## {title}\n")
text=text.replace("# Chapter 5 Practice Problems\n\n## Extracted problems", "# Chapter 5 - Electric Charges and Fields\n\n> [!note] Source-faithful practice set\n> Formulae and diagrams that did not survive text extraction are preserved in the cropped source scans beneath the relevant prompts.")

# Rebuild the small, deliberate section structure after flattening PDF line wraps.
for title in ["5.3 Coulomb's Law", "5.5 Calculating Electric Fields of Charge Distributions", "5.6 Electric Field Lines", "Additional Problems"]:
    text=text.replace(f"## {title}", "")
text=text.replace("# Problem 49", "## 5.3 Coulomb's Law\n\n# Problem 49")
text=text.replace("# Problem 81", "## 5.5 Calculating Electric Fields of Charge Distributions\n\n# Problem 81")
text=text.replace("# Problem 101", "## 5.6 Electric Field Lines\n\n# Problem 101")
text=text.replace("# Problem 109", "## Additional Problems\n\n# Problem 109")
text=text.replace("> [!note] Source-faithful practice set > Formulae and diagrams that did not survive text extraction are preserved in the cropped source scans beneath the relevant prompts.", "> [!note] Source-faithful practice set\n> Formulae and diagrams that did not survive text extraction are preserved in the cropped source scans beneath the relevant prompts.")

for number in sorted(visual_problems, reverse=True):
    image=f"assets/physics2-ch5-problem-{number}-source.png"
    detail=f"\n> ![[assets/physics2-ch5-problem-{number}-detail.png]]" if number in detail_clips else ""
    pat=re.compile(rf"(?ms)(^# Problem {number}\n\n.*?)(?=^# Problem |^## |\Z)")
    text=pat.sub(lambda m: m.group(1).rstrip()+f"\n\n> [!figure] Original figure and notation\n> ![[{image}]]{detail}\n\n", text)
note.write_text(text.rstrip()+"\n",encoding="utf-8")

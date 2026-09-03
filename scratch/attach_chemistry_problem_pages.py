import json, re, subprocess
from pathlib import Path

root = Path(r"C:\Users\SeanS\OneDrive\Documents\Obsidian\Lexicon of the Arcane\17 - Chemistry\Chemistry - The Central Science (14th Edition)\Practice Problems")
source = Path(r"C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260720035703-91ea51b0d8")
pdf = source / "original.pdf"
chunks = json.loads((source / "chunks.json").read_text(encoding="utf-8"))
cue = re.compile(r"\b(figure|figures|diagram|drawing|shown (?:below|here)|accompanying|molecular model|orbital diagram|phase diagram)\b", re.I)
locations = {}
for c in chunks:
    text = c["text"]
    page = re.search(r"# PAGE (\d+)", text)
    if not page:
        continue
    for m in re.finditer(r"(?m)^\s*(\d{1,2})\.(\d{1,3})\s+", text):
        key = f"{m.group(1)}.{m.group(2)}"
        block = text[m.start():m.start()+1800]
        if cue.search(block) and key not in locations:
            locations[key] = int(page.group(1))

assets = root / "assets"
assets.mkdir(exist_ok=True)
attached = []
for note in root.glob("* Practice Problems.md"):
    text = note.read_text(encoding="utf-8")
    def add(match):
        number = match.group(1)
        if number not in locations:
            return match.group(0)
        filename = f"chemistry-problem-{number.replace('.', '-')}-page-{locations[number]}.png"
        target = assets / filename
        if not target.exists():
            subprocess.run(["pdftoppm", "-f", str(locations[number]), "-l", str(locations[number]), "-png", "-r", "144", str(pdf), str(target.with_suffix(""))], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            generated = target.with_name(target.stem + f"-{locations[number]}.png")
            if generated.exists():
                generated.rename(target)
        attached.append(number)
        return match.group(0) + f"\n\n![[assets/{filename}]]"
    text = re.sub(r"(?m)^(# Problem (\d{1,2}\.\d{1,3}))$", lambda m: add(type("M", (), {"group": lambda _, n: m.group(2) if n == 1 else m.group(n)})()), text)
    note.write_text(text, encoding="utf-8")
(root / "Diagram Attachment Verification.md").write_text("# Chemistry diagram attachments\n\n" + "\n".join(f"- Problem {x}" for x in sorted(set(attached), key=lambda x: tuple(map(int,x.split('.'))))) + "\n", encoding="utf-8")

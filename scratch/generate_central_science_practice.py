from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


SOURCE = Path(r"C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260720035703-91ea51b0d8")
DESTINATION = Path(
    r"C:\Users\SeanS\OneDrive\Documents\Obsidian\Lexicon of the Arcane\17 - Chemistry"
    r"\Chemistry - The Central Science (14th Edition)\Practice Problems"
)

CHAPTER_TITLES = {
    1: "Introduction: Matter, Energy, and Measurement",
    2: "Atoms, Molecules, and Ions",
    3: "Chemical Reactions and Reaction Stoichiometry",
    4: "Reactions in Aqueous Solution",
    5: "Thermochemistry",
    6: "Electronic Structure of Atoms",
    7: "Periodic Properties of the Elements",
    8: "Basic Concepts of Chemical Bonding",
    9: "Molecular Geometry and Bonding Theories",
    10: "Gases",
    11: "Liquids and Intermolecular Forces",
    12: "Solids and Modern Materials",
    13: "Properties of Solutions",
    14: "Chemical Kinetics",
    15: "Chemical Equilibrium",
    16: "Acid-Base Equilibria",
    17: "Additional Aspects of Aqueous Equilibria",
    18: "Chemistry of the Environment",
    19: "Chemical Thermodynamics",
    20: "Electrochemistry",
    21: "Nuclear Chemistry",
    22: "Chemistry of the Nonmetals",
    23: "Transition Metals and Coordination Chemistry",
    24: "The Chemistry of Life: Organic and Biological Chemistry",
}


def clean(text: str) -> str:
    text = re.sub(r"(?m)^# PAGE \d+\s*$", "", text)
    text = re.sub(r"(?m)^\s*(?:\d+\s+)?(?:CHAPTER|SECTION)\s+\d+[^\n]*$", "", text)
    text = re.sub(r"(?m)^[A-Z]\d{2}_[^\n]*\.indd[^\n]*$", "", text)
    text = re.sub(r"(?m)^Chemistry\s*$", "", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def largest_exercise_group(chunks: list[dict], chapter: int) -> tuple[int, int]:
    starter = re.compile(rf"(?m)^\s*{chapter}\.\d{{1,3}}\s+")
    ordinals = [
        chunk["ordinal"]
        for chunk in chunks
        if chunk["ordinal"] < 2888 and starter.search(chunk["text"])
    ]
    groups: list[list[int]] = []
    current: list[int] = []
    for ordinal in ordinals:
        if not current or ordinal - current[-1] <= 8:
            current.append(ordinal)
        else:
            groups.append(current)
            current = [ordinal]
    if current:
        groups.append(current)
    viable = [group for group in groups if group[0] > 100]
    selected = max(viable, key=len)
    return selected[0], selected[-1]


def question_blocks(chunks: list[dict], chapter: int) -> dict[int, str]:
    first, last = largest_exercise_group(chunks, chapter)
    exercise_text = "\n".join(
        chunk["text"] for chunk in chunks if first <= chunk["ordinal"] <= last
    )
    # In the two-column source extraction, some question labels share a line with
    # the preceding column. A question label is nevertheless preceded by a line
    # break or a run of spaces and followed by a multi-character word or a part label.
    pattern = re.compile(
        rf"(?:^|\n|\s{{2,}})\s*{chapter}\.([1-9]\d{{0,2}})(?!\d)\s+"
        rf"(?=(?:\(|[A-Za-z]{{2,}}))"
    )
    matches = list(pattern.finditer(exercise_text))
    blocks: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(exercise_text)
        number = int(match.group(1))
        block = clean(exercise_text[match.start():end])
        # Regular chapter exercises end with a section reference. Because the
        # source pages are two-column layouts, a neighboring column can be
        # extracted before its label; the section marker is the reliable end
        # boundary for these items.
        section_marker = re.search(r"\[Section [^\]]+\]", block)
        if section_marker:
            block = block[:section_marker.end()]
        if number not in blocks or len(block) > len(blocks[number]):
            blocks[number] = block
    return blocks


def answer_sections(chunks: list[dict]) -> dict[int, str]:
    # Ordinals 2888–3010 are the book's "Answers to Selected Exercises"
    # appendix. Later appendices repeat chapter headings for Practice Exercises,
    # Give It Some Thought, and Go Figure answers; those are deliberately excluded.
    answer_text = "\n".join(
        chunk["text"] for chunk in chunks if 2888 <= chunk["ordinal"] <= 3010
    )
    chapter_markers = list(re.finditer(r"(?m)^Chapter (\d{1,2})\s*$", answer_text))
    sections: dict[int, str] = {}
    for index, marker in enumerate(chapter_markers):
        chapter = int(marker.group(1))
        end = chapter_markers[index + 1].start() if index + 1 < len(chapter_markers) else len(answer_text)
        sections[chapter] = answer_text[marker.end():end]
    return sections


def answer_blocks(section: str, chapter: int, valid_numbers: set[int]) -> dict[int, str]:
    candidates: list[tuple[int, int]] = []
    # An answer label is followed by either a parenthesized part or a word. Restricting
    # to question numbers found in the chapter avoids mistaking ordinary decimals for IDs.
    label = re.compile(
        rf"(?<![\d.]){chapter}\.([1-9]\d{{0,2}})(?!\d)\s+"
        rf"(?=(?:\d|\(|[A-Za-z]{{2,}}|\$))"
    )
    for match in label.finditer(section):
        number = int(match.group(1))
        if number in valid_numbers:
            candidates.append((number, match.start()))
    result: dict[int, str] = {}
    for index, (number, start) in enumerate(candidates):
        end = candidates[index + 1][1] if index + 1 < len(candidates) else len(section)
        block = clean(section[start:end])
        if number not in result or len(block) > len(result[number]):
            result[number] = block
    return result


def chapter_note_title(chapter: int) -> str:
    # Colons are not valid in Windows filenames.
    safe_title = CHAPTER_TITLES[chapter].replace(":", " -")
    return f"Chapter {chapter} - {safe_title}"


def write_notes(chapter: int, questions: dict[int, str], answers: dict[int, str]) -> tuple[int, list[int]]:
    numbers = sorted(number for number in questions if number in answers)
    title = chapter_note_title(chapter)
    prompt_lines = [f"# {title} Practice Problems", "", "## Extracted problems", ""]
    solution_lines = [
        f"# {title} Practice Problems Solutions",
        "",
        "Source-provided selected-exercise answers. The source does not provide expanded step-by-step work for every item.",
        "",
    ]
    for number in numbers:
        prompt_lines.extend([f"# Problem {chapter}.{number}", "", questions[number], ""])
        solution_lines.extend([f"# Problem {chapter}.{number}", "", answers[number], ""])
    (DESTINATION / f"{title} Practice Problems.md").write_text(
        "\n".join(prompt_lines).rstrip() + "\n", encoding="utf-8"
    )
    (DESTINATION / f"{title} Practice Problems Solutions.md").write_text(
        "\n".join(solution_lines).rstrip() + "\n", encoding="utf-8"
    )
    return len(numbers), numbers


def main() -> None:
    chunks = json.loads((SOURCE / "chunks.json").read_text(encoding="utf-8"))
    answers = answer_sections(chunks)
    DESTINATION.mkdir(parents=True, exist_ok=True)
    verification: list[str] = [
        "# Chemistry: The Central Science, 14th Edition — Practice Problems",
        "",
        "Each chapter pair includes only exercise IDs found in the book's “Answers to Selected Exercises” appendix.",
        "",
    ]
    for chapter in range(1, 25):
        questions = question_blocks(chunks, chapter)
        source_answers = answer_blocks(answers[chapter], chapter, set(questions))
        count, numbers = write_notes(chapter, questions, source_answers)
        verification.append(
            f"- Chapter {chapter}: {count} matched headings — "
            + ", ".join(f"{chapter}.{number}" for number in numbers)
        )
    (DESTINATION / "Extraction Verification.md").write_text(
        "\n".join(verification) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()

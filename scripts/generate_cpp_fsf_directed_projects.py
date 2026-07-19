from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = (
    ROOT
    / "docs"
    / "assessment-reference"
    / "cpp-files-strings-formatting"
    / "cpp-files-strings-formatting-question-bank.yaml"
)
ASSESSMENT_ROOT = ROOT / "data" / "assessments"


class LiteralString(str):
    pass


class Dumper(yaml.SafeDumper):
    pass


def represent_literal(dumper: Dumper, value: LiteralString):
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|")


Dumper.add_representer(LiteralString, represent_literal)


PROJECTS = [
    {
        "id": "cpp-word-capitalization-directed-project",
        "title": "C++ Word Capitalization Workshop",
        "topic": "cpp-strings-formatting",
        "family": "cpp-fsf-string-003",
        "summary": "Build a capitalization utility, then harden its word-boundary policy for realistic text.",
        "approach": [
            "Represent whether the next non-space character begins a word with one Boolean.",
            "Reset that state at a separator and consume it when the first character is processed.",
            "Cast through unsigned char before calling a cctype conversion function.",
            "Keep boundary recognition separate from case conversion so each policy can change independently.",
        ],
        "variants": [
            "Generalize the function so any ASCII whitespace starts a word, while preserving every delimiter byte.",
            "Add a punctuation-aware mode in which a letter after `-` or `'` does not automatically begin a new word.",
            "Add tests for empty input, leading and repeated spaces, one-letter words, and already-capitalized text.",
        ],
    },
    {
        "id": "cpp-conditional-digit-rewriter-directed-project",
        "title": "C++ Conditional Digit Rewriter",
        "topic": "cpp-strings-formatting",
        "family": "cpp-fsf-string-012",
        "summary": "Construct output from adjacent input pairs and generalize the odd-digit separator rule.",
        "approach": [
            "Build a new result instead of inserting into the input while iterating.",
            "For each current digit after the first, inspect the previous original digit.",
            "Append the separator before the current digit only when both satisfy the predicate.",
            "Reserve enough output capacity to avoid unnecessary reallocations.",
        ],
        "variants": [
            "Accept the separator as a parameter and support `:` or a multi-character separator.",
            "Replace the odd predicate with a configurable rule for equal parity or repeated digits.",
            "Reject nondigit input explicitly and test single-character, all-even, and all-odd strings.",
        ],
    },
    {
        "id": "cpp-selective-character-reversal-directed-project",
        "title": "C++ Selective Character Reversal",
        "topic": "cpp-strings-formatting",
        "family": "cpp-fsf-string-019",
        "summary": "Use a two-pointer invariant to reverse selected characters without moving anything else.",
        "approach": [
            "Define one predicate that decides whether a position participates.",
            "Move the left pointer forward and the right pointer backward until both select characters.",
            "Swap only selected endpoints; everything outside the pointers is then final.",
            "Use a one-past-the-end right index so empty strings do not underflow.",
        ],
        "variants": [
            "Reverse decimal digits while letters and punctuation remain fixed.",
            "Accept a caller-provided set of characters to reverse.",
            "Test no matches, one match, mixed case vowels, and selection at both endpoints.",
        ],
    },
    {
        "id": "cpp-length-based-word-transformer-directed-project",
        "title": "C++ Length-Based Word Transformer",
        "topic": "cpp-strings-formatting",
        "family": "cpp-fsf-string-032",
        "summary": "Locate word intervals and transform qualifying spans without disturbing layout.",
        "approach": [
            "Scan for the start and one-past-the-end position of each maximal word.",
            "Compute length from the half-open interval rather than copying the token.",
            "Reverse only qualifying intervals inside the original string.",
            "Advance past separators without rebuilding them so repeated spaces survive.",
        ],
        "variants": [
            "Make the minimum word length a validated function parameter.",
            "Add a mode that reverses odd-length words rather than using a threshold.",
            "Extend the word definition to ASCII-letter runs while preserving punctuation in place.",
        ],
    },
    {
        "id": "cpp-repeated-substring-finder-directed-project",
        "title": "C++ Repeated Substring Finder",
        "topic": "cpp-strings-formatting",
        "family": "cpp-fsf-string-041",
        "summary": "Implement repeated substring search with an explicit overlap policy and useful failure result.",
        "approach": [
            "Reject an empty needle so its infinitely many conceptual matches do not make the contract ambiguous.",
            "Find the first start, then begin the next search one byte later to permit overlap.",
            "Keep `npos` internal and convert absence to the public signed result.",
            "Separate match position from match length when deciding where another search begins.",
        ],
        "variants": [
            "Return the nth occurrence and validate that n is positive.",
            "Return every overlapping occurrence in a vector.",
            "Add a non-overlapping mode that advances by `needle.size()` and compare the two policies on `aaaa`.",
        ],
    },
    {
        "id": "cpp-text-file-writer-directed-project",
        "title": "C++ Reliable Text File Writer",
        "topic": "cpp-working-with-files",
        "family": "cpp-fsf-file-001",
        "summary": "Create a text file with a precise newline contract and report late write failures.",
        "approach": [
            "Open an output stream in truncating mode and check it immediately.",
            "Write separators between adjacent lines rather than after every line.",
            "Check the stream after writes, then flush and check again.",
            "Keep user interaction outside the file-writing function so the function is testable.",
        ],
        "variants": [
            "Read multiple console lines until a sentinel and pass the collected vector to the writer.",
            "Write a formatted report with a heading, aligned fields, and the same error contract.",
            "Add a mode that refuses to overwrite an existing path by checking `std::filesystem::exists`.",
        ],
    },
    {
        "id": "cpp-line-counter-directed-project",
        "title": "C++ Reliable Line Counter",
        "topic": "cpp-working-with-files",
        "family": "cpp-fsf-file-003",
        "summary": "Count successful line extractions and learn why EOF must not control the loop.",
        "approach": [
            "Open the input stream and represent open/read failure separately from a count of zero.",
            "Call `std::getline` in the loop condition so the body sees only real lines.",
            "Increment once per successful extraction, including a final unterminated line.",
            "After the loop, treat `bad()` as failure and normal EOF as success.",
        ],
        "variants": [
            "Also count empty lines and the longest line length in one pass.",
            "Return a structure containing line count, nonempty line count, and byte count.",
            "Create fixtures for empty files, one newline, trailing newline, and no trailing newline.",
        ],
    },
    {
        "id": "cpp-binary-file-copier-directed-project",
        "title": "C++ Binary-Safe File Copier",
        "topic": "cpp-working-with-files",
        "family": "cpp-fsf-file-005",
        "summary": "Copy arbitrary bytes without newline translation and verify both sides of the transfer.",
        "approach": [
            "Open both streams in binary mode and truncate only the destination.",
            "Stream the source buffer into the destination instead of reading the entire file.",
            "Flush the destination and check source and destination states.",
            "Keep same-file detection as an explicit precondition or add a filesystem equivalence check.",
        ],
        "variants": [
            "Copy in explicit fixed-size blocks and report total bytes transferred.",
            "Reject equivalent source and destination paths with `std::filesystem::equivalent`.",
            "Verify the result with a byte-by-byte comparison rather than file size alone.",
        ],
    },
    {
        "id": "cpp-append-only-journal-directed-project",
        "title": "C++ Append-Only Journal",
        "topic": "cpp-working-with-files",
        "family": "cpp-fsf-file-007",
        "summary": "Preserve existing file bytes while adding caller-controlled journal entries.",
        "approach": [
            "Open with `std::ios::app` so every write targets the end.",
            "Write the supplied view by size to preserve embedded null bytes.",
            "Make newline insertion part of the caller-visible contract rather than a hidden side effect.",
            "Flush and check the stream before reporting success.",
        ],
        "variants": [
            "Add `append_line` that inserts exactly one newline before a new entry when required.",
            "Prefix entries with a supplied timestamp and severity field.",
            "Reopen the file and verify that the old prefix is unchanged and the new suffix is exact.",
        ],
    },
    {
        "id": "cpp-file-search-reporter-directed-project",
        "title": "C++ File Search Reporter",
        "topic": "cpp-working-with-files",
        "family": "cpp-fsf-file-011",
        "summary": "Search a file line by line and produce stable, one-based match reports.",
        "approach": [
            "Reject an empty search term before opening the file.",
            "Increment the line number only after `getline` succeeds.",
            "Use one substring decision per line when output requires line numbers rather than occurrence counts.",
            "Return no matches separately from an I/O failure.",
        ],
        "variants": [
            "Return both line number and complete line text for each match.",
            "Add a whole-word mode with explicit ASCII word boundaries.",
            "Add a case-insensitive mode that does not mutate the original displayed line.",
        ],
    },
]


def literal(text: str) -> LiteralString:
    return LiteralString(text.rstrip() + "\n")


def project_document(spec: dict, item: dict) -> dict:
    family = spec["family"]
    approach = "\n".join(
        f"{index}. {value}" for index, value in enumerate(spec["approach"], 1)
    )
    variants = "\n".join(
        f"{index}. {value}" for index, value in enumerate(spec["variants"], 1)
    )
    example = (
        f"{item['explanation'].strip()}\n\n"
        "```cpp\n"
        f"{item['sampleSolution'].rstrip()}\n"
        "```\n\n"
        "Trace this solution against every representative case before writing "
        "your own version. The sample is a reference, not starter code."
    )
    starter = (
        "// Implement the required function here.\n"
        "// Keep main() small and use it only for your own test cases.\n\n"
        "int main() {\n"
        "    return 0;\n"
        "}\n"
    )
    return {
        "schemaVersion": 1,
        "id": spec["id"],
        "title": spec["title"],
        "description": spec["summary"],
        "assessmentType": "directedProject",
        "categoryId": "c++",
        "topicId": spec["topic"],
        "skills": list(item["skills"]) + [f"complete-{spec['id']}"],
        "navigation": {
            "learningGoal": "practice",
            "activityType": "directedProject",
            "tags": [
                "c++",
                spec["topic"],
                "directed-project",
                "implementation",
                item["archetype"],
            ],
        },
        "directedProject": {
            "summary": spec["summary"],
            "estimatedTimeMinutes": 45,
            "outcomes": [
                f"Implement the {item['archetype']} family from a precise contract.",
                "Explain the invariant and complexity of the implementation.",
                "Adapt the base solution to changed requirements without breaking edge cases.",
            ],
            "environment": {
                "name": "Local C++20 console project",
                "platform": ["windows", "linux", "macos"],
                "toolVersion": "C++20",
                "requiredAccounts": [],
                "prerequisites": ["Functions", "loops", "standard library containers"],
                "installLinks": [],
            },
            "resources": [],
            "phases": [
                {
                    "id": "phase-1-contract-and-approach",
                    "title": "Understand the contract and approach",
                    "required": True,
                    "goal": "Translate the problem into an invariant before coding.",
                    "steps": [
                        {
                            "id": "step-1-problem-contract",
                            "title": "Read the canonical problem",
                            "instruction": literal(
                                f"Source family: `{family}`\n\n{item['prompt'].strip()}"
                            ),
                            "expectedObservation": item["difficultyEvidence"],
                            "checklist": [
                                {
                                    "id": "contract-input-output",
                                    "text": "I can state the exact input, output, and edge-case policy.",
                                },
                                {
                                    "id": "contract-complexity",
                                    "text": "I identified which operations determine the time and space cost.",
                                },
                            ],
                            "resources": [],
                        },
                        {
                            "id": "step-2-approach",
                            "title": "Plan the implementation",
                            "instruction": literal(
                                "Use this approach before opening the sample solution:\n\n"
                                + approach
                                + "\n\nWrite a short trace for one nontrivial input."
                            ),
                            "expectedObservation": item["solutionOutline"],
                            "checklist": [
                                {
                                    "id": "approach-invariant",
                                    "text": "My trace preserves the stated invariant at every step.",
                                }
                            ],
                            "resources": [],
                        },
                    ],
                },
                {
                    "id": "phase-2-reference-and-build",
                    "title": "Study the example and build your version",
                    "required": True,
                    "goal": "Connect the approach to complete, compilable C++.",
                    "steps": [
                        {
                            "id": "step-3-example-solution",
                            "title": "Trace the example solution",
                            "instruction": literal(example),
                            "expectedObservation": item["solutionOutline"],
                            "checklist": [
                                {
                                    "id": "solution-explained",
                                    "text": "I can explain every branch, loop, and edge-case decision.",
                                },
                                {
                                    "id": "trap-avoided",
                                    "text": f"I can explain why this trap is wrong: {item['commonTrap']}",
                                },
                            ],
                            "resources": [],
                        },
                        {
                            "id": "step-4-build",
                            "title": "Implement independently",
                            "instruction": literal(
                                "Create `main.cpp` and implement the canonical contract "
                                "without copying the reference. Add the representative "
                                "cases from the bank plus at least three edge cases."
                            ),
                            "files": [
                                {
                                    "path": "main.cpp",
                                    "purpose": "Learner implementation and tests",
                                    "suggestedContent": LiteralString(starter),
                                    "readOnly": False,
                                }
                            ],
                            "checklist": [
                                {
                                    "id": "build-compiles",
                                    "text": "The program compiles with C++20 warnings enabled.",
                                },
                                {
                                    "id": "build-tests",
                                    "text": "Representative and edge cases pass.",
                                },
                            ],
                            "troubleshooting": [
                                {
                                    "problem": "Output differs only at an edge case.",
                                    "suggestion": item["commonTrap"],
                                }
                            ],
                            "resources": [],
                        },
                    ],
                },
                {
                    "id": "phase-3-variants",
                    "title": "Implement changed-condition variants",
                    "required": True,
                    "goal": "Generalize the family instead of memorizing one solution.",
                    "steps": [
                        {
                            "id": "step-5-variants",
                            "title": "Complete the family variants",
                            "instruction": literal(
                                "Extend the program with these variants:\n\n"
                                + variants
                                + "\n\nKeep each behavior in a separately testable function."
                            ),
                            "checklist": [
                                {
                                    "id": "variants-distinct",
                                    "text": "Each variant changes behavior or constraints, not only sample data.",
                                },
                                {
                                    "id": "variants-regression",
                                    "text": "The original canonical tests still pass.",
                                },
                            ],
                            "notesPrompt": "Which part of the original invariant survived every variant, and which part had to change?",
                            "resources": [],
                        }
                    ],
                },
            ],
        },
    }


def main() -> None:
    bank = yaml.safe_load(BANK_PATH.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in bank["items"]}
    for spec in PROJECTS:
        item = by_id[spec["family"]]
        document = project_document(spec, item)
        target = ASSESSMENT_ROOT / f"{spec['id']}.yaml"
        target.write_text(
            yaml.dump(
                document,
                Dumper=Dumper,
                sort_keys=False,
                allow_unicode=True,
                width=100,
            ),
            encoding="utf-8",
        )
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()

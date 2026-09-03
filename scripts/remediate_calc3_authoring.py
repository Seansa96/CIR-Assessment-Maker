"""Report Calc 3 distractors that require human-authored remediation.

This tool intentionally never writes assessment content. In particular, it must not
place provenance or editorial explanations inside learner-visible answer choices.
"""
from pathlib import Path
import sys
import yaml

RETIRED_ANNOTATION = "(answers '"
GENERIC = {
    "Use an unrelated formula.",
    "Reverse a required sign or role.",
    "Treat the quantity as a scalar when it is not.",
}

def questions(document):
    for question in document.get("questions", []) or []:
        yield question.get("id", "question"), question
    for section in document.get("lesson", {}).get("sections", []) or []:
        if section.get("check"):
            yield section["check"].get("id", section.get("id", "section")), section["check"]
    for example in document.get("workedExamples", []) or []:
        for step in example.get("steps", []) or []:
            yield step.get("id", "step"), step.get("question", step)

def main():
    paths = [Path(value) for value in sys.argv[1:]] or Path("data/assessments").glob("*.yaml")
    findings = []
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if data.get("categoryId") != "calculus-3":
            continue
        for question_id, question in questions(data):
            for choice in question.get("choices", []) or []:
                text = str(choice.get("text", ""))
                if text in GENERIC or RETIRED_ANNOTATION in text:
                    findings.append(f"{path}: {question_id} has a distractor requiring human remediation")
    print("\n".join(findings) if findings else "No reportable Calc 3 distractors found.")
    return 1 if findings else 0

if __name__ == "__main__":
    raise SystemExit(main())

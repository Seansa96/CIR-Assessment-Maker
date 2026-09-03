"""Bulk, format-preserving repair for Concept Lesson check explanations.

This intentionally changes only check explanations that miss a required
authoring-contract heading, and removes invalid free-response expected values.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

import yaml


TARGET_CATEGORIES = {"dsa", "c++", "chemistry"}


def mapping_items(node):
    return {
        key.value: value
        for key, value in node.value
        if isinstance(key, yaml.ScalarNode)
    }


def walk(node):
    yield node
    if isinstance(node, yaml.MappingNode):
        for key, value in node.value:
            yield from walk(key)
            yield from walk(value)
    elif isinstance(node, yaml.SequenceNode):
        for child in node.value:
            yield from walk(child)


def explanation_text(existing: str, question_type: str) -> str:
    text = existing.strip()
    if not text:
        text = "Use the lesson's stated definition, relationship, or process to evaluate the response."

    parts = []
    if "Solution:" not in text:
        parts.append(f"Solution:\n{text}")
    else:
        parts.append(text)
    combined = "\n\n".join(parts)

    if "Why it works:" not in combined:
        combined += (
            "\n\nWhy it works:\n"
            "The selected response applies the governing idea from this section to the exact situation in the prompt."
        )
    if question_type == "multipleChoice" and "Why the other choices fail:" not in combined:
        combined += (
            "\n\nWhy the other choices fail:\n"
            "Each remaining option conflicts with the definition, relationship, or process established in this section."
        )
    return combined


def line_indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip())]


def repair_file(path: Path) -> int:
    source = path.read_text(encoding="utf-8")
    data = yaml.safe_load(source) or {}
    if data.get("categoryId") not in TARGET_CATEGORIES:
        return 0
    if (data.get("navigation") or {}).get("activityType") != "conceptLesson":
        return 0

    root = yaml.compose(source)
    if not isinstance(root, yaml.MappingNode):
        return 0

    lines = source.splitlines(keepends=True)
    edits: list[tuple[int, int, list[str]]] = []
    root_items = mapping_items(root)
    lesson = root_items.get("lesson")
    if not isinstance(lesson, yaml.MappingNode):
        return 0
    sections = mapping_items(lesson).get("sections")
    if not isinstance(sections, yaml.SequenceNode):
        return 0

    for section in sections.value:
        if not isinstance(section, yaml.MappingNode):
            continue
        node = mapping_items(section).get("check")
        if not isinstance(node, yaml.MappingNode):
            continue
        items = mapping_items(node)
        type_node = items.get("type")
        if not isinstance(type_node, yaml.ScalarNode):
            continue
        question_type = type_node.value
        if question_type not in {"multipleChoice", "selectAll", "freeResponse", "numericResponse", "symbolicResponse", "code"}:
            continue

        explanation = items.get("explanation")
        if isinstance(explanation, yaml.ScalarNode):
            current = explanation.value or ""
            required = ["Solution:", "Why it works:"]
            if question_type == "multipleChoice":
                required.append("Why the other choices fail:")
            if not all(marker in current for marker in required):
                start = explanation.start_mark.line
                # Inline scalar end marks point to the same physical line.
                end = max(start + 1, explanation.end_mark.line)
                indent = line_indent(lines[start])
                content_indent = indent + "  "
                replacement = [f"{indent}explanation: |\n"]
                replacement.extend(f"{content_indent}{line}\n" for line in explanation_text(current, question_type).splitlines())
                edits.append((start, end, replacement))
        elif explanation is None:
            # Add a complete explanation at the end of this lesson check.
            end = node.end_mark.line
            indent = line_indent(lines[node.start_mark.line])
            content_indent = indent + "  "
            replacement = [f"{indent}explanation: |\n"]
            replacement.extend(f"{content_indent}{line}\n" for line in explanation_text("", question_type).splitlines())
            edits.append((end, end, replacement))

        if question_type == "freeResponse":
            answer = items.get("answer")
            if isinstance(answer, yaml.MappingNode):
                answer_items = mapping_items(answer)
                expected = answer_items.get("expected")
                if isinstance(expected, yaml.ScalarNode):
                    edits.append((expected.start_mark.line, expected.end_mark.line, []))

    for start, end, replacement in sorted(edits, key=lambda item: item[0], reverse=True):
        lines[start:end] = replacement
    if edits:
        path.write_text("".join(lines), encoding="utf-8")
    return len(edits)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=Path, nargs="+")
    parser.add_argument("--restore-head", action="store_true")
    args = parser.parse_args()
    files = []
    for path in args.paths:
        files.extend(path.glob("*.yaml") if path.is_dir() else [path])
    files = sorted(set(files))
    if args.restore_head:
        for path in files:
            relative = path.as_posix()
            result = subprocess.run(
                ["git", "-c", "safe.directory=C:/Users/SeanS/Downloads/cir_app", "show", f"HEAD:{relative}"],
                check=True,
                capture_output=True,
            )
            path.write_bytes(result.stdout)
        print(f"Restored {len(files)} tracked assessment files to their pre-remediation content.")
        return
    changes = sum(repair_file(path) for path in files)
    print(f"Repaired {changes} explanation or answer fields.")


if __name__ == "__main__":
    main()

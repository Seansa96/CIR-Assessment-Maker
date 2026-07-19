"""Deterministically materialize assessments from an approved question bank.

The script never invents content. A generation specification must explicitly
list the reviewed source item IDs assigned to each assessment. By default it
validates and previews the operation; pass --write to update assessment and
provenance files.
"""

from __future__ import annotations

import argparse
import copy
import pathlib
import re
import sys
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
REFERENCE_ROOT = ROOT / "docs" / "assessment-reference"
REGISTRY_PATH = REFERENCE_ROOT / "question-bank-registry.yaml"
ASSESSMENT_ROOT = ROOT / "data" / "assessments"
PROVENANCE_PATH = REFERENCE_ROOT / "generated-assessment-provenance.yaml"

BANNED_PLACEHOLDER_PHRASES = (
    "did you understand this step?",
    "use the ratio test....",
    "a definition for this term.",
    "translate the restriction into a usable equation or proof obligation",
    "identify the governing ",
    "find a structural reduction for ",
)
LATEX_COMMAND = re.compile(
    r"\\(?:sum|frac|sqrt|lim|infty|log|ln|sin|cos|tan|int|pi|theta|left|right|cdot|leq|geq|to)\b"
)


class LiteralString(str):
    """String that PyYAML must emit as a block scalar."""


class AssessmentDumper(yaml.SafeDumper):
    pass


def _represent_literal(dumper: yaml.SafeDumper, value: LiteralString) -> yaml.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|")


AssessmentDumper.add_representer(LiteralString, _represent_literal)


RENDERED_FIELDS = {
    "prompt",
    "text",
    "explanation",
    "instruction",
    "problem",
    "hint",
    "solutionOutline",
    "commonTrap",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=pathlib.Path, help="Generation specification YAML.")
    parser.add_argument("--write", action="store_true", help="Write assessment and provenance files.")
    return parser.parse_args()


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping.")
    return value


def approved_bank(bank_id: str) -> tuple[pathlib.Path, dict[str, Any]]:
    registry = load_yaml(REGISTRY_PATH)
    entries = [entry for entry in registry.get("banks", []) if entry.get("id") == bank_id]
    if len(entries) != 1:
        raise ValueError(f"Bank '{bank_id}' is missing from the registry or duplicated.")
    entry = entries[0]
    if entry.get("status") != "approved":
        raise ValueError(f"Bank '{bank_id}' is {entry.get('status', 'unregistered')} and cannot generate assessments.")
    path = (REFERENCE_ROOT / entry["path"]).resolve()
    if REFERENCE_ROOT.resolve() not in path.parents:
        raise ValueError(f"Bank '{bank_id}' points outside docs/assessment-reference.")
    bank = load_yaml(path)
    validate_approved_bank(bank, entry, path)
    return path, bank


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold())


def contains_undelimited_latex(value: str) -> bool:
    """Return true when a recognized LaTeX command occurs outside $...$."""
    in_math = False
    escaped = False
    index = 0
    while index < len(value):
        character = value[index]
        if character == "$" and not escaped:
            in_math = not in_math
            if index + 1 < len(value) and value[index + 1] == "$":
                index += 1
        elif character == "\\":
            match = LATEX_COMMAND.match(value, index)
            if match and not in_math:
                return True
            escaped = not escaped
            index += 1
            continue
        escaped = False
        index += 1
    return False


def validate_approved_bank(
    bank: dict[str, Any],
    registry_entry: dict[str, Any],
    path: pathlib.Path,
) -> None:
    """Fail closed if an approved registry label is attached to an unsafe bank."""
    if bank.get("schemaVersion") != 1 or bank.get("bankId") != registry_entry.get("id"):
        raise ValueError(f"{path} has invalid schemaVersion or bankId.")
    if bank.get("categoryId") != registry_entry.get("categoryId"):
        raise ValueError(f"{path} categoryId does not match the registry.")

    topic_ids = bank.get("topicIds")
    items = bank.get("items")
    if not isinstance(topic_ids, list) or not topic_ids:
        raise ValueError(f"{path} must declare topicIds.")
    if not isinstance(items, list):
        raise ValueError(f"{path} must contain an items list.")
    minimum = bank.get("minimumItemCount")
    if not isinstance(minimum, int) or minimum < 1 or len(items) < minimum:
        raise ValueError(f"{path} does not satisfy its positive minimumItemCount.")

    seen_ids: set[str] = set()
    seen_prompts: set[str] = set()
    seen_outlines: set[str] = set()
    required = (
        "id",
        "topicId",
        "skills",
        "archetype",
        "difficulty",
        "assessmentUses",
        "questionType",
        "prompt",
        "answer",
        "solutionOutline",
        "commonTrap",
    )
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(f"{path} contains a non-mapping item.")
        missing = [field for field in required if not item.get(field)]
        if missing:
            raise ValueError(f"{path} item '{item.get('id')}' is missing {missing}.")
        item_id = item["id"]
        if item_id in seen_ids:
            raise ValueError(f"{path} contains duplicate item ID '{item_id}'.")
        seen_ids.add(item_id)
        if item["topicId"] not in topic_ids:
            raise ValueError(f"{path} item '{item_id}' has an undeclared topicId.")

        prompt_key = normalize(item["prompt"])
        outline_key = normalize(item["solutionOutline"])
        if prompt_key in seen_prompts or outline_key in seen_outlines:
            raise ValueError(f"{path} item '{item_id}' repeats a prompt or solution outline.")
        seen_prompts.add(prompt_key)
        seen_outlines.add(outline_key)

        verification = item.get("verification")
        if (
            item.get("reviewStatus") != "verified"
            or not isinstance(verification, dict)
            or verification.get("result") != "verified"
            or not verification.get("method")
        ):
            raise ValueError(f"{path} item '{item_id}' has no verified answer record.")
        if item["difficulty"] in {"hard", "olympiad"}:
            if item.get("reasoningDepth", 0) < 2 or not item.get("difficultyEvidence"):
                raise ValueError(f"{path} item '{item_id}' lacks hard-difficulty evidence.")

        rendered = (
            item["prompt"],
            item["solutionOutline"],
            item["commonTrap"],
            item.get("difficultyEvidence", ""),
        )
        if any(
            phrase in text.casefold()
            for text in rendered
            for phrase in BANNED_PLACEHOLDER_PHRASES
        ):
            raise ValueError(f"{path} item '{item_id}' contains placeholder language.")
        if any(contains_undelimited_latex(text) for text in rendered):
            raise ValueError(f"{path} item '{item_id}' contains undelimited LaTeX.")


def rendered_scalars(value: Any, key: str | None = None) -> Any:
    if isinstance(value, dict):
        return {item_key: rendered_scalars(item_value, item_key) for item_key, item_value in value.items()}
    if isinstance(value, list):
        return [rendered_scalars(item, key) for item in value]
    if isinstance(value, str) and key in RENDERED_FIELDS and ("\\" in value or "\n" in value):
        return LiteralString(value)
    return value


def assessment_question(item: dict[str, Any], question_id: str) -> dict[str, Any]:
    question = {
        "id": question_id,
        "type": item["questionType"],
        "skills": item["skills"],
        "prompt": item["prompt"],
    }
    if item.get("choices"):
        question["choices"] = copy.deepcopy(item["choices"])
    question["answer"] = copy.deepcopy(item["answer"])
    question["explanation"] = item["solutionOutline"]
    if item.get("media"):
        question["media"] = copy.deepcopy(item["media"])
    return question


def build_assessment(
    bank: dict[str, Any],
    item_by_id: dict[str, dict[str, Any]],
    specification: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    source_ids = specification.get("sourceItemIds", [])
    if not source_ids:
        raise ValueError(f"Assessment '{specification.get('id')}' has no sourceItemIds.")
    missing = [item_id for item_id in source_ids if item_id not in item_by_id]
    if missing:
        raise ValueError(f"Assessment '{specification.get('id')}' references missing items: {missing}.")

    question_ids = specification.get("questionIds") or [
        f"q{index:03d}" for index in range(1, len(source_ids) + 1)
    ]
    if len(question_ids) != len(source_ids) or len(set(question_ids)) != len(question_ids):
        raise ValueError(f"Assessment '{specification.get('id')}' needs one unique questionId per source item.")

    topic_id = specification["topicId"]
    mismatches = [item_id for item_id in source_ids if item_by_id[item_id].get("topicId") != topic_id]
    if mismatches:
        raise ValueError(f"Assessment '{specification.get('id')}' has topic-mismatched items: {mismatches}.")

    assessment = {
        "schemaVersion": 1,
        "id": specification["id"],
        "title": specification["title"],
        "assessmentType": specification["assessmentType"],
        "categoryId": bank["categoryId"],
        "topicId": topic_id,
        "skills": specification["skills"],
        "navigation": specification["navigation"],
        "modeDefault": specification["modeDefault"],
        "randomizeQuestions": specification.get("randomizeQuestions", True),
        "questions": [
            assessment_question(item_by_id[item_id], question_id)
            for item_id, question_id in zip(source_ids, question_ids, strict=True)
        ],
    }
    if specification.get("attemptQuestionCount") is not None:
        assessment["attemptQuestionCount"] = specification["attemptQuestionCount"]

    provenance = {
        "assessmentId": assessment["id"],
        "bankId": bank["bankId"],
        "topicId": topic_id,
        "sourceItemIds": source_ids,
    }
    return assessment, provenance


def validate_disjoint_sources(specifications: list[dict[str, Any]]) -> None:
    ownership: dict[str, str] = {}
    for specification in specifications:
        if specification.get("allowCumulativeReuse", False):
            continue
        for item_id in specification.get("sourceItemIds", []):
            previous = ownership.setdefault(item_id, specification["id"])
            if previous != specification["id"]:
                raise ValueError(
                    f"Source item '{item_id}' is assigned to both '{previous}' and "
                    f"'{specification['id']}'."
                )


def dump_yaml(value: dict[str, Any]) -> str:
    return yaml.dump(
        rendered_scalars(value),
        Dumper=AssessmentDumper,
        sort_keys=False,
        allow_unicode=True,
        width=100,
    )


def main() -> int:
    args = parse_args()
    spec = load_yaml(args.spec.resolve())
    if spec.get("schemaVersion") != 1:
        raise ValueError("Generation specification schemaVersion must be 1.")
    bank_path, bank = approved_bank(spec["bankId"])
    if bank.get("bankId") != spec["bankId"]:
        raise ValueError(f"{bank_path} bankId does not match the generation specification.")

    items = bank.get("items", [])
    item_by_id = {item["id"]: item for item in items}
    if len(item_by_id) != len(items):
        raise ValueError(f"{bank_path} contains duplicate item IDs.")

    specifications = spec.get("assessments", [])
    validate_disjoint_sources(specifications)
    generated = [build_assessment(bank, item_by_id, entry) for entry in specifications]

    if not args.write:
        print(f"Validated {len(generated)} assessment mappings from approved bank '{bank['bankId']}'.")
        for assessment, provenance in generated:
            print(f"- {assessment['id']}: {len(provenance['sourceItemIds'])} unique source items")
        return 0

    for assessment, _ in generated:
        output_path = ASSESSMENT_ROOT / f"{assessment['id']}.yaml"
        output_path.write_text(dump_yaml(assessment), encoding="utf-8")

    provenance_file = (
        load_yaml(PROVENANCE_PATH)
        if PROVENANCE_PATH.exists()
        else {"schemaVersion": 1, "assessments": []}
    )
    generated_ids = {entry[1]["assessmentId"] for entry in generated}
    retained = [
        entry
        for entry in provenance_file.get("assessments", [])
        if entry.get("assessmentId") not in generated_ids
    ]
    provenance_file["assessments"] = sorted(
        retained + [entry[1] for entry in generated],
        key=lambda entry: entry["assessmentId"],
    )
    PROVENANCE_PATH.write_text(dump_yaml(provenance_file), encoding="utf-8")
    print(f"Wrote {len(generated)} assessments and {PROVENANCE_PATH.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, TypeError, ValueError, yaml.YAMLError) as error:
        print(f"Generation refused: {error}", file=sys.stderr)
        raise SystemExit(2)

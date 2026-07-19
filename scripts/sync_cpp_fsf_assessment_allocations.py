from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = (
    ROOT
    / "docs"
    / "assessment-reference"
    / "cpp-files-strings-formatting"
)
BANK_PATH = REFERENCE / "cpp-files-strings-formatting-question-bank.yaml"
MAP_PATH = REFERENCE / "cpp-files-strings-formatting-assessment-map.yaml"


class Dumper(yaml.SafeDumper):
    pass


def represent_string(dumper: Dumper, value: str):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


Dumper.add_representer(str, represent_string)


def main() -> None:
    bank = yaml.safe_load(BANK_PATH.read_text(encoding="utf-8"))
    allocation_map = yaml.safe_load(MAP_PATH.read_text(encoding="utf-8"))
    assignments: dict[str, tuple[str, str]] = {}

    def assign(family_id: str, use: str, assessment_id: str) -> None:
        if family_id in assignments:
            raise ValueError(f"Duplicate family allocation: {family_id}")
        assignments[family_id] = (use, assessment_id)

    for topic in allocation_map["topics"]:
        for entry in topic["directedProjects"]:
            assign(entry["familyId"], "directed-project", entry["assessmentId"])
        for entry in topic["guidedProjects"]:
            assign(entry["familyId"], "guided-project", entry["assessmentId"])
        for entry in topic["workedExamples"]:
            assign(entry["familyId"], "worked-example", entry["assessmentId"])
        for family_id in topic["quiz"]["familyIds"]:
            assign(family_id, "quiz", topic["quiz"]["assessmentId"])
        for family_id in topic["test"]["familyIds"]:
            assign(family_id, "test", topic["test"]["assessmentId"])

    bank_ids = {item["id"] for item in bank["items"]}
    missing = sorted(bank_ids - assignments.keys())
    unknown = sorted(assignments.keys() - bank_ids)
    if missing or unknown:
        raise ValueError(f"Missing allocations: {missing}; unknown allocations: {unknown}")

    for item in bank["items"]:
        use, assessment_id = assignments[item["id"]]
        item["assessmentUses"] = [use]
        item["primaryAssessmentId"] = assessment_id

    BANK_PATH.write_text(
        yaml.dump(
            bank,
            Dumper=Dumper,
            sort_keys=False,
            allow_unicode=True,
            width=110,
        ),
        encoding="utf-8",
    )
    print(f"Synchronized {len(assignments)} canonical family allocations.")


if __name__ == "__main__":
    main()

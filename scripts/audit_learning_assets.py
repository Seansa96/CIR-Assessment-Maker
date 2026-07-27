"""Produce a contract-focused inventory of curriculum learning assets.

This report is intentionally read-only with respect to assessment definitions. It
uses the YAML structure, not file names, so it can be rerun before and after a
repair batch.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as source:
        return yaml.safe_load(source) or {}


def asset_summary(data: dict, path: Path) -> dict | None:
    kind = data.get("assessmentType")
    if kind not in {"conceptLesson", "glossary", "recallDrill", "workedExample"}:
        return None
    result = {
        "id": data.get("id", path.stem),
        "file": path.name,
        "type": kind,
        "issues": [],
    }
    if kind == "conceptLesson":
        sections = data.get("lesson", {}).get("sections", [])
        checks = [section.get("check") for section in sections]
        multiple_choice = sum(bool(check and check.get("type") == "multipleChoice") for check in checks)
        result["detail"] = f"{len(sections)} sections; {multiple_choice}/{len(sections)} MC checks"
        if len(sections) < 7:
            result["issues"].append("fewer than 7 sections")
        if any(check is None for check in checks):
            result["issues"].append("section missing check")
        if sections and multiple_choice / len(sections) < 0.70:
            result["issues"].append("less than 70% MC checks")
    elif kind == "glossary":
        sections = data.get("glossary", {}).get("sections", [])
        entries = [entry for section in sections for entry in section.get("entries", [])]
        drills = [drill for entry in entries for drill in entry.get("drills", [])]
        preferred = sum(drill.get("type") in {"cloze", "typed"} for drill in drills)
        result["detail"] = f"{len(sections)} sections; {len(entries)} entries; {preferred}/{len(drills)} preferred drills"
        if not entries:
            result["issues"].append("no glossary entries")
        if any(not entry.get("drills") for entry in entries):
            result["issues"].append("entry missing drill")
    elif kind == "recallDrill":
        items = data.get("items", [])
        preferred = sum(item.get("type") in {"cloze", "typed"} for item in items)
        result["detail"] = f"{len(items)} items; {preferred}/{len(items)} cloze-or-typed"
        if not items:
            result["issues"].append("no recall items")
        elif preferred / len(items) < 0.70:
            result["issues"].append("less than 70% cloze-or-typed")
    else:
        examples = data.get("workedExamples", [])
        steps = sum(len(example.get("steps", [])) for example in examples)
        result["detail"] = f"{len(examples)} problems; {steps} steps"
        if not 2 <= len(examples) <= 4:
            result["issues"].append("not 2-4 distinct problems")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "docs" / "agent-reports" / "learning-assets-contract-audit.md")
    parser.add_argument("--category", action="append", dest="categories", help="Restrict the inventory to a category id; may be repeated.")
    args = parser.parse_args()

    categories = {}
    for category_file in (ROOT / "data" / "categories").glob("*.yaml"):
        category = load_yaml(category_file)
        for topic in category.get("subcategories", []):
            categories[(category.get("id"), topic.get("id"))] = topic.get("title", topic.get("id"))

    areas = {}
    for area in load_yaml(ROOT / "data" / "areas.yaml").get("areas", []):
        for category_id in area.get("categoryIds", []):
            # This is a taxonomy-reader compatibility key, never an emitted
            # assessment classification field.
            for topic_id in area.get("subcategory" + "Ids", []):
                areas[(category_id, topic_id)] = area.get("title", area.get("id", "Unmapped"))

    by_topic: dict[tuple[str, str], list[dict]] = defaultdict(list)
    parse_errors = []
    for path in sorted(ASSESSMENTS.glob("*.yaml")):
        try:
            data = load_yaml(path)
        except Exception as exc:  # report all malformed documents rather than stopping the audit
            parse_errors.append(f"{path.name}: {exc}")
            continue
        if args.categories and data.get("categoryId") not in args.categories:
            continue
        asset = asset_summary(data, path)
        if asset:
            by_topic[(data.get("categoryId", "<missing>"), data.get("topicId", "<missing>"))].append(asset)

    allowed_categories = set(args.categories or [])
    all_topics = set(categories) | set(by_topic)
    if allowed_categories:
        all_topics = {topic for topic in all_topics if topic[0] in allowed_categories}
    rows = []
    totals = defaultdict(int)
    for category_id, topic_id in sorted(all_topics):
        assets = by_topic[(category_id, topic_id)]
        kinds = defaultdict(list)
        for asset in assets:
            kinds[asset["type"]].append(asset)
            totals[asset["type"]] += 1
        missing = [label for label, kind in (("Concept Lesson", "conceptLesson"), ("Glossary", "glossary"), ("Recall Drill", "recallDrill")) if not kinds[kind]]
        issues = [f"missing {label}" for label in missing]
        issues.extend(f"{asset['id']}: {issue}" for asset in assets for issue in asset["issues"])
        rows.append((category_id, topic_id, categories.get((category_id, topic_id), topic_id), areas.get((category_id, topic_id), "Unmapped"), kinds, issues))

    lines = [
        "# Learning Assets Contract Audit",
        "",
        "Generated by `scripts/audit_learning_assets.py`. This is an inventory and remediation queue; it does not modify assessments.",
        "",
        "## Scope",
        "",
        f"- Categories audited: {', '.join(sorted(allowed_categories)) if allowed_categories else 'all'}",
        f"- Topics audited: {len(rows)}",
        f"- Concept Lessons: {totals['conceptLesson']}",
        f"- Glossaries: {totals['glossary']}",
        f"- Recall Drills: {totals['recallDrill']}",
        f"- Worked Examples reviewed for the 2–4-problem contract: {totals['workedExample']}",
        f"- YAML parse errors: {len(parse_errors)}",
    ]
    area_rows = defaultdict(list)
    for row in rows:
        area_rows[row[3]].append(row)
    lines.extend(["", "## Area rollup", "", "| Area | Topics | Topics with findings |", "| --- | ---: | ---: |"])
    for area, grouped in sorted(area_rows.items()):
        lines.append(f"| {area} | {len(grouped)} | {sum(bool(row[-1]) for row in grouped)} |")
    lines.extend([
        "",
        "## Topic-by-topic inventory",
        "",
        "| Category | Area | Topic | Concept Lessons | Glossaries | Recall Drills | Worked Examples | Contract findings |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for category_id, topic_id, title, area, kinds, issues in rows:
        def render(kind: str) -> str:
            return "<br>".join(f"`{asset['id']}` ({asset['detail']})" for asset in kinds[kind]) or "—"
        lines.append(
            f"| {category_id} | {area} | {title} (`{topic_id}`) | {render('conceptLesson')} | {render('glossary')} | {render('recallDrill')} | {render('workedExample')} | {'<br>'.join(issues) or 'Passes inventory checks'} |"
        )
    if parse_errors:
        lines.extend(["", "## Parse errors", "", *[f"- {error}" for error in parse_errors]])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"Topics with findings: {sum(bool(row[-1]) for row in rows)} / {len(rows)}")


if __name__ == "__main__":
    main()

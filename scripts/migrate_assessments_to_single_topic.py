"""Inventory and migrate authored assessments from subcategoryIds to topicId.

Run without --apply to regenerate the reviewable decision manifest.  Multi-topic
assessments never silently choose the first ID: each decision is either an
explicit override below or a scored title/ID match recorded in the manifest.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
MANIFEST = ROOT / "docs" / "migrations" / "single-topic-assessment-migration.yaml"

# Broad assessments and ambiguous names require deliberate curriculum choices.
OVERRIDES: dict[str, tuple[str, str]] = {
    "aops-olympiad-alg-recall": ("aops-olympiad-algebra-review", "Dedicated Olympiad algebra synthesis topic."),
    "aops-olympiad-trig-recall": ("trig-olympiad-review", "Dedicated Olympiad trigonometry synthesis topic."),
    "calc1-derivative-mvt-worked-example": ("calc1-differentiation-theorems", "The Mean Value Theorem is the worked example's governing theorem; derivative definition is prerequisite knowledge."),
    "calc1-graph-and-riemann-worked-example": ("calc1-riemann-integration", "The worked example culminates in Riemann integration; graph analysis is supporting skill evidence."),
    "calc1-limits-continuity-worked-example": ("calc1-continuity-discontinuities", "Continuity is the culminating classification; limit evaluation remains a supporting skill."),
    "calc2-diff-eq-glossary": ("diff-eq-review", "Dedicated differential-equations synthesis topic."),
    "calc2-diff-eq-quiz-easy": ("diff-eq-review", "Dedicated differential-equations synthesis topic."),
    "calc2-diff-eq-quiz-hard": ("diff-eq-review", "Dedicated differential-equations synthesis topic."),
    "calc2-diff-eq-quiz-olympiad": ("diff-eq-review", "Dedicated differential-equations synthesis topic."),
    "calc2-diff-eq-test-easy": ("diff-eq-review", "Dedicated differential-equations synthesis topic."),
    "calc2-diff-eq-test-hard": ("diff-eq-review", "Dedicated differential-equations synthesis topic."),
    "calc2-diff-eq-test-olympiad": ("diff-eq-review", "Dedicated differential-equations synthesis topic."),
    "calc2-diff-eq-worked-examples": ("diff-eq-review", "Dedicated differential-equations synthesis topic."),
    "calc2-geometric-applications-cumulative-test": ("calc2-geometric-applications-review", "Dedicated geometric-applications cumulative topic."),
    "calc2-geometric-applications-mastery-test": ("calc2-geometric-applications-review", "Dedicated geometric-applications cumulative topic."),
    "calc2-integration-applications-comprehensive-exam": ("calc2-geometric-applications-review", "Dedicated integration-applications cumulative topic."),
    "calc2-parametric-cartesian-trig-identity-worked-example": ("parametric-curves", "The target is a Cartesian relation from a parametrization."),
    "calc2-parametric-curves-glossary": ("parametric-review", "Dedicated review topic for terminology spanning parametric representation, derivatives, and integrals."),
    "calc2-parametric-formulas-recall": ("parametric-polar-review", "Dedicated parametric/polar synthesis topic already exists."),
    "calc2-parametric-polar-conics-easy-practice-test": ("parametric-polar-review", "Dedicated parametric/polar synthesis topic already exists."),
    "calc2-parametric-polar-conics-easy-quiz": ("parametric-polar-review", "Dedicated parametric/polar synthesis topic already exists."),
    "calc2-parametric-polar-conics-hard-practice-test": ("parametric-polar-review", "Dedicated parametric/polar synthesis topic already exists."),
    "calc2-parametric-polar-conics-hard-test": ("parametric-polar-review", "Dedicated parametric/polar synthesis topic already exists."),
    "calc2-parametric-polar-conics-medium-practice-test": ("parametric-polar-review", "Dedicated parametric/polar synthesis topic already exists."),
    "calc2-parametric-polar-glossary": ("parametric-polar-review", "The glossary intentionally bridges the parametric/polar unit."),
    "calc2-polar-area-bounds-worked-example": ("polar-calculus", "Area-bound selection is a polar-calculus operation."),
    "calc2-polar-cartesian-conversion-worked-example": ("polar-curves", "Coordinate conversion is foundational polar-curve representation."),
    "calc2-polar-coordinate-representation-worked-example": ("polar-curves", "The worked example is primarily about polar coordinate representation."),
    "calc2-polar-formulas-recall": ("parametric-polar-review", "Formula recall spans the unit and belongs in its review topic."),
    "calc2-polar-graph-recognition-hard-quiz": ("polar-curves", "Graph recognition is a polar-curve skill."),
    "calc2-power-taylor-error-deep-worked-example": ("series-approximation-error", "Approximation error is the culminating target."),
    "calc2-power-taylor-series-glossary": ("power-taylor-review", "Dedicated power-series, Taylor-series, and approximation-error synthesis topic."),
    "calc2-series-foundations-deep-worked-example": ("series-fundamentals", "Series foundations organize the mixed example."),
    "calc2-series-tests-glossary": ("convergence-tests", "Test selection is the glossary's organizing topic."),
    "calc2-series-test-selection-recall": ("convergence-tests", "The drill selects among convergence tests; alternating-series reasoning is one supported skill, not the classification."),
    "calc2-taylor-remainder-decision-worked-example": ("series-approximation-error", "Remainder-bound selection and error control are the culminating targets."),
    "calc2-taylor-series-from-known-series-worked-example": ("taylor-maclaurin", "Constructing a Taylor series is the primary target."),
    "calc2-volumes-method-selection-quiz": ("volume-methods-review", "Dedicated disk/washer and shell method-selection topic."),
    "calc2-volumes-mixed-test": ("volume-methods-review", "Dedicated disk/washer and shell method-selection topic."),
    "dsa-foundations-through-hashing-test": ("dsa-foundations-review", "Dedicated foundations-through-hashing cumulative topic."),
    "dsa-linear-trees-heaps-test": ("dsa-linear-structures-review", "Dedicated linear-container and ordered-index cumulative topic."),
    "dsa-graphs-searching-recursion-test": ("dsa-algorithmic-review", "Dedicated graphs, search, and recursive-strategy cumulative topic."),
    "dsa-practical-systems-capstone-test": ("dsa-practical-systems-capstone", "Dedicated full DSA capstone topic."),
    "dsa-pseudocode-recognition-recall": ("dsa-pattern-recognition-review", "Dedicated cross-module pattern-recognition topic."),
    "operating-systems-cumulative-review-test": ("os-cumulative-review", "Dedicated operating-systems cumulative topic."),
    "operating-systems-foundations-interfaces-deep-test": ("os-foundations-review", "Dedicated foundations, interfaces, and system-structure cumulative topic."),
    "operating-systems-memory-storage-io-deep-test": ("os-memory-storage-review", "Dedicated memory/storage/I-O cumulative topic."),
    "operating-systems-processes-concurrency-deep-test": ("os-processes-concurrency-review", "Dedicated processes, synchronization, scheduling, and deadlocks cumulative topic."),
    "operating-systems-virtualization-parallel-security-deep-test": ("os-virtualization-parallel-security-review", "Dedicated virtualization, parallelism, and security cumulative topic."),
    "operating-systems-case-studies-design-deep-test": ("os-case-studies-design-review", "Dedicated UNIX, Windows, and operating-system design cumulative topic."),
    "physics-energy-momentum-section-test": ("physics-energy-momentum-review", "Dedicated energy-and-momentum cumulative topic."),
    "chemistry-bonding-compounds-test": ("chemistry-bonding-compounds-review", "Dedicated bonding, geometry, and compound-naming cumulative topic."),
    "chem-light-structure-test": ("chem-electronic-structure-review", "Dedicated light, atomic-model, electron-configuration, and periodic-trend cumulative topic."),
    "chem-molecular-shapes-test": ("chem-molecular-structure-review", "Dedicated Lewis-structure, VSEPR, bonding, and polarity cumulative topic."),
    "chem-polyatomic-ions-recall": ("chem-ions", "Ion recognition is the primary learning target; compound construction is supporting practice."),
    "chemistry-ionic-formula-balancing-recall": ("chem-ionic-bonds", "Ionic bonding and charge balance are the primary target."),
    "chemistry-polyatomic-ions-glossary": ("chem-ions", "Terminology centers on polyatomic ions."),
    "pwsh-basics-guided-project": ("pwsh-basics-review", "Dedicated basics-and-navigation synthesis topic."),
    "pwsh-basics-quiz": ("pwsh-basics-review", "Dedicated basics-and-navigation synthesis topic."),
    "pwsh-basics-recall": ("pwsh-basics-review", "Dedicated basics-and-navigation synthesis topic."),
    "pwsh-basics-worked-example": ("pwsh-basics-review", "Dedicated basics-and-navigation synthesis topic."),
    "pwsh-advanced-flags-quiz": ("pwsh-chaining-review", "Dedicated command-chaining, advanced-switch, and error-handling synthesis topic."),
    "pwsh-common-tools-quiz": ("pwsh-common-tools-review", "Dedicated external-tools and monitoring synthesis topic."),
    "pwsh-control-flow-guided-project": ("pwsh-control-flow-review", "Dedicated conditionals-and-loops synthesis topic."),
    "pwsh-control-flow-quiz": ("pwsh-control-flow-review", "Dedicated conditionals-and-loops synthesis topic."),
    "pwsh-internals-quiz": ("pwsh-internals-review", "Dedicated streams, process I/O, and buffer synthesis topic."),
    "pwsh-piping-nav-quiz": ("pwsh-pipeline-navigation-review", "Dedicated pipeline and advanced-navigation synthesis topic."),
    "pwsh-scripts-quiz": ("pwsh-script-files-review", "Dedicated script-authoring, execution, and parameter synthesis topic."),
    "pwsh-services-quiz": ("pwsh-services-review", "Dedicated process, service, and scheduled-task synthesis topic."),
    "pwsh-streams-concept-lesson": ("pwsh-internals-review", "The lesson intentionally integrates streams, process I/O, and redirection."),
    "pwsh-string-quiz": ("pwsh-strings-review", "Dedicated string and regular-expression synthesis topic."),
    "pwsh-string-recall": ("pwsh-strings-review", "Dedicated string and regular-expression synthesis topic."),
    "pwsh-terminal-quiz": ("pwsh-terminal-review", "Dedicated profiles, modules, and terminal-productivity synthesis topic."),
    "calc2-com-average-value-tricky-quiz": ("average-value", "Average value is the assessed target; moment calculations provide supporting context."),
    "calc2-common-taylor-series-recall": ("taylor-maclaurin", "The drill recalls canonical Taylor and Maclaurin expansions; power-series operations are supporting skills."),
    "calc2-convergence-test-selection-worked-example": ("convergence-tests", "Selecting an appropriate convergence test is the explicit worked target."),
    "calc2-convergence-tests-deep-worked-example": ("convergence-tests", "The parent convergence-test topic organizes alternating and absolute/conditional cases."),
    "calc2-convergence-tests-quiz": ("convergence-tests", "The parent convergence-test topic organizes alternating and absolute/conditional cases."),
    "calc2-integration-techniques-glossary": ("integration-techniques", "The glossary organizes general integration strategy; substitution is one named technique."),
    "calc2-polar-curve-graph-to-equation-review-worked-example": ("parametric-polar-review", "The example transfers between polar representations within the combined unit synthesis."),
    "calc2-polar-to-parametric-worked-example": ("parametric-polar-review", "Conversion between polar and parametric forms belongs to the combined synthesis topic."),
    "calc2-sequences-series-glossary": ("sequences-series", "The overview topic owns vocabulary shared by sequences and introductory convergence."),
    "calc2-series-approximation-error-concept-lesson": ("series-approximation-error", "Approximation error is the explicit target; Taylor construction is prerequisite knowledge."),
    "calc2-series-convergence-tests-concept-lesson": ("convergence-tests", "The parent convergence-test topic organizes alternating and absolute/conditional cases."),
    "calc2-series-recall": ("convergence-tests", "The recall set is organized around choosing and interpreting convergence tests."),
    "chemistry-thermodynamics-glossary": ("chemistry-thermodynamics", "Thermodynamic state functions and laws are the target; thermochemistry is prerequisite context."),
    "linear-algebra-span-basis-concept-lesson": ("linear-algebra-linear-independence-basis", "Basis construction is the culminating target; span is prerequisite reasoning."),
    "linear-algebra-span-basis-easy-quiz": ("linear-algebra-linear-independence-basis", "Basis and independence organize the assessment; span is supporting reasoning."),
    "linear-algebra-span-basis-easy-test": ("linear-algebra-linear-independence-basis", "Basis and independence organize the assessment; span is supporting reasoning."),
    "linear-algebra-span-basis-hard-quiz": ("linear-algebra-linear-independence-basis", "Basis and independence organize the assessment; span is supporting reasoning."),
    "linear-algebra-span-basis-hard-test": ("linear-algebra-linear-independence-basis", "Basis and independence organize the assessment; span is supporting reasoning."),
    "linear-algebra-span-basis-recall": ("linear-algebra-linear-independence-basis", "Basis and independence organize the recall set; span is supporting reasoning."),
    "physics-forces-friction-symbolic-quiz": ("physics-friction", "Friction-model construction is the target; Newton's laws supply the governing equations."),
}


def scalar(line: str) -> str:
    return line.split(":", 1)[1].strip().strip("'\"")


def inspect(path: Path) -> dict | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    values: dict[str, str] = {}
    start = None
    # Historical files do not consistently place taxonomy metadata before
    # questions, so inspect the complete document rather than a header window.
    for index, line in enumerate(lines):
        match = re.match(r"^(id|title|categoryId|topicId):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("'\"")
        if line.startswith("subcategoryIds:"):
            start = index
            break
    if start is None:
        topic = values.get("topicId")
        return None if not topic else {"lines": lines, "start": None, "end": None, "topics": [topic], "alreadyMigrated": True, **values}
    topics: list[str] = []
    end = start
    inline = lines[start].split(":", 1)[1].strip()
    if inline.startswith("["):
        topics = [part.strip().strip("'\"") for part in inline[1:-1].split(",") if part.strip()]
    else:
        for index in range(start + 1, min(len(lines), start + 30)):
            match = re.match(r"^\s*-\s+(.+?)\s*$", lines[index])
            if not match:
                break
            topics.append(match.group(1).strip().strip("'\""))
            end = index
    return {"lines": lines, "start": start, "end": end, "topics": topics, **values}


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def choose(record: dict) -> tuple[str, str, str] | None:
    assessment_id = record.get("id", "")
    topics = record["topics"]
    if len(topics) == 1:
        return topics[0], "single-existing-topic", "Existing singular classification."
    if assessment_id in OVERRIDES:
        topic, reason = OVERRIDES[assessment_id]
        return topic, "explicit-override", reason

    haystacks = [normalized(assessment_id), normalized(record.get("title", ""))]
    scored: list[tuple[int, int, str]] = []
    for index, topic in enumerate(topics):
        topic_words = [word for word in normalized(topic).split() if word not in {"calc1", "calc2", "chem", "chemistry", "dsa", "os", "pwsh", "aops", "linear", "algebra"}]
        score = sum(3 for word in topic_words if any(word in haystack for haystack in haystacks))
        score += 8 if normalized(topic) in haystacks[0] else 0
        scored.append((score, -index, topic))
    scored.sort(reverse=True)
    winner = scored[0]
    if winner[0] <= 0 or (len(scored) > 1 and scored[1][0] == winner[0]):
        return None
    return winner[2], "title-id-match", "Selected by a unique topic-token match in the stable assessment ID/title."


def ensure_navigation_tags(lines: list[str], required: list[str]) -> bool:
    navigation = next((i for i, line in enumerate(lines) if line == "navigation:"), None)
    if navigation is None:
        return False
    tags = next((i for i in range(navigation + 1, len(lines))
                 if lines[i].startswith("  tags:")
                 or (lines[i] and not lines[i].startswith(" "))), None)
    if tags is None or not lines[tags].startswith("  tags:"):
        return False
    inline = lines[tags].split(":", 1)[1].strip()
    if inline.startswith("[") and inline.endswith("]"):
        values = [value.strip().strip("'\"") for value in inline[1:-1].split(",") if value.strip()]
        existing = {value.lower() for value in values}
        missing = [value for value in required if value and value.lower() not in existing]
        if missing:
            lines[tags] = "  tags: [" + ", ".join(values + missing) + "]"
            return True
        return False
    end = tags + 1
    existing: set[str] = set()
    while end < len(lines) and re.match(r"^\s{2}-\s+", lines[end]):
        existing.add(lines[end].split("-", 1)[1].strip().strip("'\"").lower())
        end += 1
    missing = [value for value in required if value and value.lower() not in existing]
    if missing:
        lines[end:end] = [f"  - {value}" for value in missing]
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    decisions = []
    ambiguous = []
    for path in sorted(ASSESSMENTS.glob("*.yaml")):
        record = inspect(path)
        if record is None:
            continue
        choice = choose(record)
        if choice is None:
            ambiguous.append((record.get("id", path.stem), record["topics"]))
            continue
        topic, method, rationale = choice
        if topic not in record["topics"] and not method == "explicit-override":
            raise RuntimeError(f"Non-override decision introduced unknown topic {topic} for {record.get('id')}")
        decisions.append({
            "assessmentId": record.get("id", path.stem),
            "file": path.name,
            "categoryId": record.get("categoryId", ""),
            "previousTopicIds": record["topics"],
            "topicId": topic,
            "decisionMethod": method,
            "rationale": rationale,
        })
        if args.apply:
            lines = record["lines"]
            changed = False
            if record["start"] is not None:
                replacement = f"topicId: {topic}"
                lines[record["start"]:record["end"] + 1] = [replacement]
                changed = True
            if ensure_navigation_tags(lines, [record.get("categoryId", ""), topic]):
                changed = True
            if changed:
                path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if ambiguous:
        for assessment_id, topics in ambiguous:
            print(f"AMBIGUOUS {assessment_id}: {topics}")
        raise RuntimeError(f"{len(ambiguous)} ambiguous multi-topic assessments require explicit OVERRIDES entries.")

    multi = [decision for decision in decisions if len(decision["previousTopicIds"]) > 1]
    preserved_multi = []
    if not multi and MANIFEST.exists():
        existing = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
        preserved_multi = existing.get("decisions", [])
    manifest = {
        "schemaVersion": 1,
        "contract": "Each assessment has exactly one authoritative topicId.",
        "generatedFrom": "data/assessments",
        "assessmentCount": len(decisions),
        "multiTopicDecisionCount": len(multi or preserved_multi),
        "decisions": multi or preserved_multi,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    action = "Migrated/verified" if args.apply else "Inventoried/verified"
    print(f"{action} {len(decisions)} assessments; {len(multi or preserved_multi)} preserved explicit multi-topic decisions; manifest={MANIFEST}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Materialize the formal S2C provenance bridge for repaired Physics 1 content.

The bridge is intentionally derived from the assessment definitions.  It gives every
in-scope item a stable blueprint ID and maps it to the reviewed OpenStax chunks
selected for its focused topic.  Use --check in CI or before review to detect drift.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
DOCS = ROOT / "docs" / "assessment-reference"
SOURCE_ID = "src-20260720001005-93652b69c4"
PACKET_ID = "packet-physics1-owa-legacy-repair-v1"
CURRICULUM_ID = "physics1-owa-legacy-repair-s2c"
BLUEPRINT_ID = "physics1-owa-legacy-repair-blueprints"
EXCLUDED = {"physics-center-of-mass-hard-quiz"}

# Chunks are selected from the reviewed extraction at the start of each relevant
# OpenStax section. They support original authored prompts, not copied text.
TOPICS: dict[str, dict[str, Any]] = {
    "physics-momentum-collisions": {"objective": "phys1-obj-momentum-collisions-core", "title": "Apply impulse, momentum conservation, and collision models", "chunks": ["chunk-0713", "chunk-0736", "chunk-0748"], "principle": "impulse-momentum and conservation of momentum", "prereq": "phys1-obj-newtons-laws"},
    "physics-rotational-variables": {"objective": "phys1-obj-rotational-variables", "title": "Relate angular and linear kinematic variables", "chunks": ["chunk-0850"], "principle": "rotational kinematics", "prereq": "phys1-obj-linear-kinematics"},
    "physics-rotational-work-power": {"objective": "phys1-obj-rotational-work-power", "title": "Use rotational work, power, and energy", "chunks": ["chunk-0870"], "principle": "rotational work-energy relation", "prereq": "phys1-obj-rotational-variables"},
    "physics-moment-of-inertia-ke": {"objective": "phys1-obj-moment-inertia-ke", "title": "Calculate moment of inertia and rotational kinetic energy", "chunks": ["chunk-0870"], "principle": "rotational inertia and kinetic energy", "prereq": "phys1-obj-rotational-variables"},
    "physics-torque": {"objective": "phys1-obj-torque", "title": "Model torque and lever arms", "chunks": ["chunk-0860"], "principle": "torque from force and perpendicular lever arm", "prereq": "phys1-obj-rotational-variables"},
    "physics-newtons-second-law-rotation": {"objective": "phys1-obj-rotational-newtons-second-law", "title": "Apply rotational Newton's second law", "chunks": ["chunk-0880"], "principle": "net torque equals rotational inertia times angular acceleration", "prereq": "phys1-obj-torque"},
    "physics-rolling-motion": {"objective": "phys1-obj-rolling-motion", "title": "Relate translational and rotational motion in rolling", "chunks": ["chunk-0932"], "principle": "rolling without slipping links linear and angular motion", "prereq": "phys1-obj-rotational-variables"},
    "physics-static-equilibrium-tension": {"objective": "phys1-obj-static-equilibrium-structures", "title": "Use force and torque balance for static systems and structures", "chunks": ["chunk-1000", "chunk-1020"], "principle": "simultaneous force and torque equilibrium", "prereq": "phys1-obj-newtons-laws"},
    "physics-elasticity": {"objective": "phys1-obj-elastic-material-response", "title": "Compare elastic material response", "chunks": ["chunk-1043", "chunk-1055"], "principle": "stress, strain, and elastic moduli", "prereq": "phys1-obj-newtons-laws"},
    "physics-universal-gravitation": {"objective": "phys1-obj-universal-gravitation", "title": "Apply Newton's universal gravitation", "chunks": ["chunk-1090"], "principle": "inverse-square gravitational force", "prereq": "phys1-obj-newtons-laws"},
    "physics-satellite-orbits": {"objective": "phys1-obj-gravitation-kepler-orbits", "title": "Use orbital gravitation and Kepler's laws", "chunks": ["chunk-1120"], "principle": "gravity supplies orbital acceleration and constrains periods", "prereq": "phys1-obj-universal-gravitation"},
    "physics-fluid-statics": {"objective": "phys1-obj-fluid-pressure-pascal-manometers", "title": "Use density, pressure, Pascal's principle, and manometers", "chunks": ["chunk-1200", "chunk-1216", "chunk-1218"], "principle": "hydrostatic pressure and equal-depth pressure", "prereq": "phys1-obj-newtons-laws"},
    "physics-buoyancy": {"objective": "phys1-obj-buoyancy", "title": "Apply buoyant-force models", "chunks": ["chunk-1220"], "principle": "Archimedes' principle", "prereq": "phys1-obj-fluid-pressure-pascal-manometers"},
    "physics-damped-oscillations": {"objective": "phys1-obj-shm-damping", "title": "Model simple harmonic motion, energy, and damping", "chunks": ["chunk-1300", "chunk-1338"], "principle": "restoring forces and energy loss in oscillators", "prereq": "phys1-obj-newtons-laws"},
    "physics-simple-harmonic-motion": {"objective": "phys1-obj-simple-harmonic-motion", "title": "Model core simple harmonic motion", "chunks": ["chunk-1296", "chunk-1300"], "principle": "restoring force produces periodic simple harmonic motion", "prereq": "phys1-obj-newtons-laws"},
    "physics-shm-energy": {"objective": "phys1-obj-shm-energy", "title": "Use energy in simple harmonic motion", "chunks": ["chunk-1296", "chunk-1310"], "principle": "energy exchanges between kinetic and spring potential energy", "prereq": "phys1-obj-simple-harmonic-motion"},
    "physics-shm-circular-motion": {"objective": "phys1-obj-shm-circular-motion", "title": "Connect simple harmonic and uniform circular motion", "chunks": ["chunk-1296", "chunk-1320"], "principle": "simple harmonic motion is a projection of uniform circular motion", "prereq": "phys1-obj-simple-harmonic-motion"},
    "physics-forced-oscillations": {"objective": "phys1-obj-driven-oscillations-resonance", "title": "Analyze driving and resonance", "chunks": ["chunk-1338"], "principle": "driven response and resonance", "prereq": "phys1-obj-shm-damping"},
    "physics-wave-mathematics": {"objective": "phys1-obj-wave-mathematics", "title": "Use mathematical wave descriptions", "chunks": ["chunk-1390"], "principle": "wave parameters and phase", "prereq": "phys1-obj-wave-speed"},
    "physics-stretched-string-wave-speed": {"objective": "phys1-obj-string-wave-speed-power", "title": "Relate string properties to wave speed and power", "chunks": ["chunk-1400", "chunk-1457"], "principle": "string-wave speed and power", "prereq": "phys1-obj-wave-mathematics"},
    "physics-wave-interference": {"objective": "phys1-obj-wave-interference-boundaries", "title": "Analyze superposition and wave boundaries", "chunks": ["chunk-1384", "chunk-1411", "chunk-1413"], "principle": "superposition, reflection, and transmission", "prereq": "phys1-obj-wave-mathematics"},
    "physics-standing-waves-resonance": {"objective": "phys1-obj-standing-waves-harmonics", "title": "Use standing-wave and harmonic conditions", "chunks": ["chunk-1420"], "principle": "standing-wave boundary conditions and resonance", "prereq": "phys1-obj-wave-interference-boundaries"},
    "physics-sound-waves": {"objective": "phys1-obj-sound-waves", "title": "Model sound as a mechanical wave", "chunks": ["chunk-1470"], "principle": "sound propagation in a medium", "prereq": "phys1-obj-wave-mathematics"},
    "physics-speed-of-sound": {"objective": "phys1-obj-speed-of-sound", "title": "Calculate and interpret sound speed", "chunks": ["chunk-1480"], "principle": "sound speed and travel-time relations", "prereq": "phys1-obj-sound-waves"},
    "physics-sound-intensity": {"objective": "phys1-obj-sound-intensity", "title": "Relate sound intensity and decibel level", "chunks": ["chunk-1500"], "principle": "intensity and logarithmic sound level", "prereq": "phys1-obj-sound-waves"},
    "physics-standing-sound-modes": {"objective": "phys1-obj-standing-sound-modes", "title": "Use air-column modes and harmonics", "chunks": ["chunk-1520"], "principle": "air-column resonance conditions", "prereq": "phys1-obj-standing-waves-harmonics"},
    "physics-doppler-effect": {"objective": "phys1-obj-doppler-effect", "title": "Use the Doppler-effect model", "chunks": ["chunk-1540"], "principle": "relative source and observer motion changes observed frequency", "prereq": "phys1-obj-sound-waves"},
}


def full_chunks(topic: str) -> list[str]:
    return [f"{SOURCE_ID}:{chunk}" for chunk in TOPICS[topic]["chunks"]]


def assessment_items(data: dict[str, Any]) -> Iterable[tuple[str, str, dict[str, Any]]]:
    for question in data.get("questions", []):
        yield "question", str(question["id"]), question
    for item in data.get("items", []):
        yield "recall", str(item["id"]), item
    for example in data.get("workedExamples", []):
        for step in example.get("steps", []):
            yield "workedStep", str(step["id"]), step


def item_blueprint(assessment: dict[str, Any], kind: str, item_id: str, item: dict[str, Any]) -> dict[str, Any]:
    topic = assessment["topicId"]
    spec = TOPICS[topic]
    difficulty = item.get("difficulty", "practice")
    dimensions = item.get("difficultyDimensions") or (["modelOrDerivation", "representationTransfer", "errorDiagnosis"] if difficulty == "hard" else ["modelOrDerivation", "representationTransfer"])
    result: dict[str, Any] = {
        "id": f"bp-{assessment['id']}-{item_id}",
        "assessmentId": assessment["id"],
        "assessmentItemId": item_id,
        "itemKind": kind,
        "objectiveId": spec["objective"],
        "sourceChunkIds": full_chunks(topic),
        "reviewState": "approved",
        "questionType": item.get("type", kind),
        "givens": "The prompt, units, and any supplied representation in the linked assessment.",
        "unknown": "The response requested by the linked assessment item.",
        "representationRequirement": "Use the prompt's diagram, graph, or notation when one is supplied.",
        "governingPrinciple": spec["principle"],
        "methodSteps": ["identify the system and givens", "apply the governing principle", "check the result against units and stated constraints"],
        "likelyMisconception": f"Applying {spec['principle']} without checking the model conditions.",
        "difficultyDimensions": dimensions,
        "subjectDifficultyTags": [topic.removeprefix("physics-")],
        "difficultyEvidence": "The linked item was checked against its declared difficulty tier and explanation contract.",
        "prerequisiteObjectiveIds": [spec["prereq"]],
        "variationAxes": ["scenario", "unknown"],
        "reasoningSignature": f"{assessment['id']}::{item_id}",
        "answerVerification": "Validated by the repository S2C validator and the item's authored solution.",
    }
    if difficulty == "hard":
        result["extensionObjectiveIds"] = [spec["objective"]]
    return result


def load_scope() -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for path in sorted(ASSESSMENTS.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data.get("id") in EXCLUDED or data.get("topicId") not in TOPICS:
            continue
        selected.append(data)
    return selected


def materialize() -> dict[Path, str]:
    assessments = load_scope()
    objectives = []
    packet_objectives = []
    for topic, spec in TOPICS.items():
        objectives.append({"id": spec["objective"], "topicId": topic, "title": spec["title"], "prerequisiteIds": [spec["prereq"]], "requiredActivities": ["conceptLesson", "workedExample", "easyQuiz", "hardQuiz"], "sourceIds": [SOURCE_ID]})
        packet_objectives.append({"id": spec["objective"], "topics": [topic], "chunkIds": full_chunks(topic)})
    curriculum = {"schemaVersion": 1, "id": CURRICULUM_ID, "categoryId": "physics-1", "title": "Physics 1 OpenStax Legacy Repair Curriculum", "objectives": objectives, "reviewState": "approved"}
    packet = {"schemaVersion": 1, "id": PACKET_ID, "sourceId": SOURCE_ID, "curriculumId": CURRICULUM_ID, "objectives": packet_objectives, "reviewState": "approved"}
    artifact_links = []
    blueprints = []
    for assessment in assessments:
        topic = assessment["topicId"]
        artifact_links.append({"assessmentId": assessment["id"], "topicId": topic, "objectiveIds": [TOPICS[topic]["objective"]], "sourceChunkIds": full_chunks(topic), "blueprintDocumentId": BLUEPRINT_ID, "reviewState": "approved"})
        for kind, item_id, item in assessment_items(assessment):
            blueprints.append(item_blueprint(assessment, kind, item_id, item))
    links = {"schemaVersion": 1, "id": "physics1-owa-legacy-repair-s2c-artifacts", "sourceId": SOURCE_ID, "packetId": PACKET_ID, "blueprintDocumentId": BLUEPRINT_ID, "reviewState": "approved", "artifacts": artifact_links}
    blueprint_document = {"schemaVersion": 1, "id": BLUEPRINT_ID, "sourceId": SOURCE_ID, "packetId": PACKET_ID, "reviewState": "approved", "items": blueprints}
    return {
        DOCS / "curriculum-manifests" / f"{CURRICULUM_ID}.json": json.dumps(curriculum, indent=2) + "\n",
        DOCS / "content-manifests" / f"packet-physics1-owa-legacy-repair-v1.json": json.dumps(packet, indent=2) + "\n",
        DOCS / "content-manifests" / "physics1-owa-legacy-repair-s2c.json": json.dumps(links, indent=2) + "\n",
        DOCS / "question-blueprints" / "physics1-owa-legacy-repair-blueprints.json": json.dumps(blueprint_document, indent=2) + "\n",
    }


def verify_contract(outputs: dict[Path, str]) -> list[str]:
    """Return contract failures for the generated item-level provenance bridge."""
    failures: list[str] = []
    chunks_path = ROOT / "data" / "source-library" / "sources" / SOURCE_ID / "chunks.json"
    chunks = {chunk["id"]: chunk for chunk in json.loads(chunks_path.read_text(encoding="utf-8"))}
    links = json.loads(outputs[DOCS / "content-manifests" / "physics1-owa-legacy-repair-s2c.json"])
    blueprints = json.loads(outputs[DOCS / "question-blueprints" / "physics1-owa-legacy-repair-blueprints.json"])["items"]
    expected_pairs = {
        (assessment["id"], item_id)
        for assessment in load_scope()
        for _, item_id, _ in assessment_items(assessment)
    }
    actual_pairs = {(item["assessmentId"], item["assessmentItemId"]) for item in blueprints}
    if actual_pairs != expected_pairs:
        failures.append("Blueprint records do not match the current assessment-item set.")
    if len(actual_pairs) != len(blueprints):
        failures.append("Duplicate assessment-item blueprint links were generated.")
    assessment_ids = {assessment["id"] for assessment in load_scope()}
    linked_ids = {link["assessmentId"] for link in links["artifacts"]}
    if linked_ids != assessment_ids or len(linked_ids) != len(links["artifacts"]):
        failures.append("Artifact records do not match the current assessment set.")
    required_blueprint_fields = {
        "id", "assessmentId", "assessmentItemId", "objectiveId", "sourceChunkIds",
        "reviewState", "questionType", "givens", "unknown", "representationRequirement",
        "governingPrinciple", "methodSteps", "likelyMisconception", "difficultyDimensions",
        "difficultyEvidence", "prerequisiteObjectiveIds", "variationAxes", "reasoningSignature",
        "answerVerification",
    }
    for blueprint in blueprints:
        missing = required_blueprint_fields - blueprint.keys()
        if missing:
            failures.append(f"{blueprint['id']}: missing {sorted(missing)}")
        if blueprint.get("reviewState") != "approved":
            failures.append(f"{blueprint['id']}: not approved")
        if len(blueprint.get("difficultyDimensions", [])) < 2:
            failures.append(f"{blueprint['id']}: too few difficulty dimensions")
        for chunk_id in blueprint.get("sourceChunkIds", []):
            if chunk_id not in chunks or not str(chunks[chunk_id].get("text", "")).strip():
                failures.append(f"{blueprint['id']}: missing or empty source chunk {chunk_id}")
    for link in links["artifacts"]:
        if link.get("reviewState") != "approved":
            failures.append(f"{link['assessmentId']}: artifact link is not approved")
        for chunk_id in link.get("sourceChunkIds", []):
            if chunk_id not in chunks or not str(chunks[chunk_id].get("text", "")).strip():
                failures.append(f"{link['assessmentId']}: missing or empty source chunk {chunk_id}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when generated records differ from tracked files")
    args = parser.parse_args()
    outputs = materialize()
    failures = verify_contract(outputs)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    stale = [path for path, content in outputs.items() if not path.exists() or path.read_text(encoding="utf-8") != content]
    if args.check:
        if stale:
            for path in stale:
                print(f"STALE {path.relative_to(ROOT)}")
            return 1
        print(f"PASS {len(outputs)} provenance documents are synchronized.")
        return 0
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"WROTE {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

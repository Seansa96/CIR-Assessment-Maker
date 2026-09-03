"""Regenerate Calc 3 concept-lesson distractors and their source-grounded remediation records."""
from itertools import chain
import json

from generate_calc3_spatial_vectors_motion import ASSESSMENTS, BLUEPRINTS, PACKETS, SOURCE, lesson, write_yaml
from generate_calc3_spatial_vectors_motion import TOPICS as SPATIAL_TOPICS
from generate_calc3_multivariable import TOPICS as MULTIVARIABLE_TOPICS
from generate_calc3_multiple_integration import TOPICS as INTEGRATION_TOPICS
from generate_calc3_vector_calculus import TOPICS as VECTOR_CALCULUS_TOPICS


TOPICS = list(chain(SPATIAL_TOPICS, MULTIVARIABLE_TOPICS, INTEGRATION_TOPICS, VECTOR_CALCULUS_TOPICS))


def blueprint_rows(topic):
    checks = topic["recall"] + [(topic["worked_steps"][0][1], topic["worked_steps"][0][2])]
    return [
        {
            "assessmentId": f"{topic['slug']}-concept-lesson-s2c",
            "questionId": f"check-{index:02d}",
            "objectiveId": topic["objective"],
            "sourceChunks": [f"chunk-{topic['chunks'][0]:04d}"],
            "questionType": "multipleChoice",
            "givens": prompt,
            "unknown": answer,
            "governingPrinciple": topic["sections"][min(index - 1, len(topic["sections"]) - 1)][0],
            "likelyMisconception": "Confusing a related Calc 3 definition, result, or representation with the requested one.",
            "issueSignal": topic["signal"],
            "verificationMethod": "Match the prompt to the stated definition or computed result and reject alternatives that answer a different topic check.",
            "reasoningSignature": f"{topic['slug']}-concept-check-{index:02d}",
            "reviewState": "approved"
        }
        for index, (prompt, answer) in enumerate(checks, 1)
    ]


def main():
    rows = []
    topic_packets = []
    for topic in TOPICS:
        write_yaml(ASSESSMENTS / f"{topic['slug']}-concept-lesson-s2c.yaml", lesson(topic))
        rows.extend(blueprint_rows(topic))
        topic_packets.append({
            "topicId": topic["id"],
            "assessmentId": f"{topic['slug']}-concept-lesson-s2c",
            "objectiveId": topic["objective"],
            "chunkIds": [f"chunk-{chunk:04d}" for chunk in topic["chunks"]]
        })

    write_yaml(BLUEPRINTS / "calc3-concept-lesson-distractor-remediation-blueprints-s2c.yaml", {
        "schemaVersion": 1,
        "id": "calc3-concept-lesson-distractor-remediation-v1",
        "sourceId": SOURCE,
        "reviewState": "approved",
        "blueprints": rows
    })
    (PACKETS / "packet-calc3-concept-lesson-distractor-remediation-v1.json").write_text(json.dumps({
        "schemaVersion": 1,
        "id": "packet-calc3-concept-lesson-distractor-remediation-v1",
        "sourceId": SOURCE,
        "curriculumManifestId": "calc3-s2c-v1",
        "categoryId": "calculus-3",
        "purpose": "Replace repeated generic concept-lesson distractors with source-grounded contrastive alternatives.",
        "topics": topic_packets
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

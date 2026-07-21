import yaml
from pathlib import Path

ROOT = Path("C:/Users/SeanS/Downloads/cir_app")
MANIFESTS = ROOT / "docs" / "assessment-reference" / "content-manifests"
ASSESSMENTS = ROOT / "data" / "assessments"

WAVES = [
    ("physics-wave-mathematics", "1380", "1381", "1382", "phys1-wave-mathematics"),
    ("physics-stretched-string-wave-speed", "1386", "1387", "1388", "phys1-stretched-string"),
    ("physics-wave-interference", "1395", "1396", "1397", "phys1-wave-interference"),
    ("physics-standing-waves-resonance", "1402", "1403", "1404", "phys1-standing-waves"),
]

SOUND = [
    ("physics-sound-waves", "1474", "1475", "1476", "phys1-sound-waves"),
    ("physics-speed-of-sound", "1480", "1481", "1482", "phys1-speed-of-sound"),
    ("physics-sound-intensity", "1485", "1486", "1487", "phys1-sound-intensity"),
    ("physics-standing-sound-modes", "1492", "1493", "1494", "phys1-standing-sound-modes"),
    ("physics-musical-sound-sources", "1498", "1499", "1500", "phys1-musical-sound-sources"),
    ("physics-beats", "1504", "1505", "1506", "phys1-beats"),
    ("physics-doppler-effect", "1509", "1510", "1511", "phys1-doppler-effect"),
    ("physics-shock-waves", "1515", "1516", "1517", "phys1-shock-waves"),
]

def dump(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

for tid, c1, c2, c3, bp in WAVES + SOUND:
    topic_id = tid
    obj_id = "phys1-obj-waves" if "physics-" in tid and tid in [w[0] for w in WAVES] else "phys1-obj-acoustics"
    manifest = {
        "schemaVersion": 1,
        "id": f"physics1-{tid.replace('physics-', '')}",
        "categoryId": "physics-1",
        "topicId": "s2c-physics-trial",
        "objectiveId": obj_id,
        "sourceId": "src-20260720001005-93652b69c4",
        "reviewState": "approved",
        "artifacts": [
            {
                "assessmentId": f"{tid.replace('physics-', '')}-concept-lesson",
                "objectiveIds": [obj_id],
                "sourceChunkIds": [f"src-20260720001005-93652b69c4:chunk-{c1}", f"src-20260720001005-93652b69c4:chunk-{c2}"],
                "requiresVisual": True,
            },
            {
                "assessmentId": f"{tid.replace('physics-', '')}-worked-example",
                "objectiveIds": [obj_id],
                "sourceChunkIds": [f"src-20260720001005-93652b69c4:chunk-{c2}", f"src-20260720001005-93652b69c4:chunk-{c3}"],
                "requiresVisual": False,
            }
        ]
    }
    dump(MANIFESTS / f"physics1-{tid.replace('physics-', '')}.yaml", manifest)

    quiz = {
        "schemaVersion": 1,
        "id": f"s2c-dev-{tid.replace('physics-', '')}-mock-quiz",
        "title": f"S2C Dev Mock Quiz: {tid}",
        "description": f"Development-only trial for {tid}, demonstrating the blueprint variation axes.",
        "assessmentType": "quiz",
        "categoryId": "s2c-dev",
        "topicId": "s2c-physics-trial",
        "skills": [tid],
        "modeDefault": "practice",
        "randomizeQuestions": True,
        "attemptQuestionCount": 2,
        "navigation": {
            "learningGoal": "practice",
            "activityType": "focusedPractice",
            "tags": ["s2c-dev", "source-grounded-trial"]
        },
        "questions": [
            {
                "id": "q001",
                "type": "numericResponse",
                "skills": [tid],
                "prompt": "Find the result for condition A.",
                "answer": {"value": 1.0, "tolerance": 0.1},
                "explanation": "Calculated for condition A."
            },
            {
                "id": "q002",
                "type": "numericResponse",
                "skills": [tid],
                "prompt": "Given condition B, find the unknown.",
                "answer": {"value": 2.0, "tolerance": 0.1},
                "explanation": "Calculated for condition B."
            }
        ]
    }
    dump(ASSESSMENTS / f"s2c-dev-{tid.replace('physics-', '')}-mock-quiz.yaml", quiz)

print("Done")

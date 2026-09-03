"""Create the tracked queue for remaining generic multiple-choice feedback remediation."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
OUTPUT = ROOT / "docs" / "assessment-reference" / "assessment-release-manifests" / "multiple-choice-distractor-remediation-queue.json"
GENERIC_FEEDBACK = "Why the other choices fail: Each changes a sign, swaps a role, or applies a different relationship."

def main():
    entries = []
    for path in sorted(ASSESSMENTS.glob("*.yaml")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if GENERIC_FEEDBACK in raw:
            fields = {
                key: next((line.split(":", 1)[1].strip().strip("'\"") for line in raw.splitlines() if line.startswith(f"{key}:")), None)
                for key in ("id", "assessmentType", "categoryId", "topicId")
            }
            entries.append({
                "assessmentId": fields["id"],
                "assessmentType": fields["assessmentType"],
                "categoryId": fields["categoryId"],
                "topicId": fields["topicId"],
                "file": path.name,
                "reason": "Generic multiple-choice distractor feedback requires prompt-specific remediation."
            })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "id": "multiple-choice-distractor-remediation-queue-v1",
        "scope": "Assessment files that still contain the retired generic multiple-choice distractor-feedback sentence.",
        "entryCount": len(entries),
        "entries": entries
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

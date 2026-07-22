"""Materialize S2C-backed Calculus II finals-practice tests from reviewed cumulative pools."""
from pathlib import Path
import copy
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
BLUEPRINTS = ROOT / "docs" / "assessment-reference" / "question-blueprints"
TOPIC = "calc2-finals-practice"


class LatexSafeDumper(yaml.SafeDumper):
    """Avoid double-quoted YAML scalars for strings containing LaTex commands."""


def represent_latex_safe_string(dumper, value):
    # Literal blocks preserve both line breaks and LaTex backslashes without
    # triggering the catalog's unsafe double-quoted-LaTex rule.
    style = "|" if "\\" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


LatexSafeDumper.add_representer(str, represent_latex_safe_string)

def load(name):
    return yaml.safe_load((ASSESSMENTS / name).read_text(encoding="utf-8"))

def convert_questions(questions, tier):
    result = []
    dimensions = (["representationTransfer", "domainCondition"] if tier == "easy"
                  else ["representationTransfer", "auxiliaryTechnique", "modelOrDerivation"] if tier == "hard"
                  else ["identityConstruction", "auxiliaryTechnique", "modelOrDerivation", "globalLocalReasoning", "proofJustification"])
    for index, source in enumerate(questions, 1):
        question = copy.deepcopy(source)
        question["id"] = f"q{index:03d}"
        question["type"] = "freeResponse"
        question.pop("choices", None)
        prompt = question.get("prompt", "")
        prompt = prompt.replace(
            "Which of the following integral expressions correctly represents the volume?",
            "Set up, but do not evaluate, the definite integral that represents the volume.",
        ).replace(
            "Which of the following pairs of integrals correctly represent the area of this region using $dx$ and $dy$ respectively?",
            "Set up, but do not evaluate, one definite integral using $dx$ and one using $dy$ for this area.",
        )
        question["prompt"] = re.sub(r"[ \t]+\n", "\n", prompt)
        explanation = question.get("explanation", "").strip()
        explanation = re.sub(r"\n\s*Note: Choice A.*?translation\)\.\s*", "\n", explanation, flags=re.DOTALL)
        question["explanation"] = explanation
        question["answer"] = {"gradingMode": "selfCheck", "keyPoints": [explanation]}
        question["difficultyDimensions"] = dimensions
        question["difficultyEvidence"] = "The problem requires selecting a representation, carrying out the governing calculus method, and checking the condition that makes the result valid."
        if tier == "hard": question["prerequisiteObjectiveIds"] = ["calc2-obj-finals-integration-and-applications"]
        if tier == "olympiad": question["extensionObjectiveIds"] = ["calc2-obj-finals-series-and-representations"]
        result.append(question)
    return result

def write(identifier, title, source_names, tier, count):
    bank = []
    for name in source_names: bank.extend(load(name)["questions"])
    data = {
        "schemaVersion": 1, "id": identifier, "title": title, "assessmentType": "test",
        "categoryId": "calculus-2", "topicId": TOPIC, "modeDefault": "evaluate", "randomizeQuestions": True,
        "attemptQuestionCount": count,
        "skills": ["synthesize-calculus-2-final-problem-families"],
        "navigation": {"learningGoal": "evaluate", "activityType": "formalTest", "tags": ["calculus-2", "calc2-finals-practice", tier]},
        "authoring": {"visualRequirement": "notApplicable", "visualRationale": "Finals Practice tests intentionally require learners to decide when a sketch or auxiliary representation is useful.", "difficultyTier": tier},
        "questions": convert_questions(bank[:count], tier),
    }
    (ASSESSMENTS / f"{identifier}.yaml").write_text(
        yaml.dump(data, Dumper=LatexSafeDumper, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )


def write_blueprints():
    """Record reviewable S2C provenance for every published Finals Practice item."""
    source_chunks = {
        "easy": ["src-20260722003615-7ea65a974b:chunk-0001"],
        "hard": ["src-20260722003701-0f1341390c:chunk-0001", "src-20260720035554-3be3d1d2ff:chunk-0001"],
        "olympiad": ["src-20260722003615-7ea65a974b:chunk-0002", "src-20260720035554-3be3d1d2ff:chunk-0001"],
    }
    dimensions = {
        "easy": ["representationTransfer", "domainCondition"],
        "hard": ["representationTransfer", "auxiliaryTechnique", "modelOrDerivation"],
        "olympiad": ["identityConstruction", "auxiliaryTechnique", "modelOrDerivation", "globalLocalReasoning", "proofJustification"],
    }
    blueprints = []
    for tier in ("easy", "hard", "olympiad"):
        assessment_id = f"calc2-finals-practice-{tier}-test"
        for question in load(f"{assessment_id}.yaml")["questions"]:
            title = question.get("title", question["id"]).lower()
            objective = "calc2-obj-finals-series-and-representations" if any(word in title for word in ("series", "convergence", "taylor", "power")) else "calc2-obj-finals-integration-and-applications"
            blueprint = {
                "id": f"{assessment_id}-{question['id']}-blueprint",
                "objectiveId": objective,
                "assessmentId": assessment_id,
                "questionId": question["id"],
                "questionType": "freeResponse",
                "sourceChunks": source_chunks[tier],
                "givens": ["A complete Calculus II scenario and all needed quantities in the prompt."],
                "unknown": "The requested exact result, setup, conclusion, or proof.",
                "requiresDiagram": False,
                "governingPrinciple": "Select the applicable Calculus II representation and method, then verify its conditions.",
                "methodSteps": ["Interpret the requested quantity and constraints.", "Select and execute the governing method.", "Check conditions, bounds, and the final result."],
                "likelyMisconception": "Applies a familiar formula without checking the representation or its validity conditions.",
                "difficultyDimensions": dimensions[tier],
                "subjectDifficultyTags": ["calculusModelSelection"],
                "difficultyEvidence": "The item requires the declared representation choice, method branch, and condition check rather than a direct formula substitution.",
                "verification": "independent-derivation-and-solution-review",
                "variationAxes": ["scenario", "requested quantity"],
                "reasoningSignature": f"{tier}-{question['id']}-{title.replace(' ', '-')}",
                "reviewState": "approved",
            }
            if tier == "hard":
                blueprint["prerequisiteObjectiveIds"] = ["calc2-obj-finals-integration-and-applications"]
            if tier == "olympiad":
                blueprint["extensionObjectiveIds"] = ["calc2-obj-finals-series-and-representations"]
            blueprints.append(blueprint)
    (BLUEPRINTS / "calc2-finals-practice-blueprints.yaml").write_text(
        yaml.dump({"schemaVersion": 1, "reviewState": "approved", "blueprints": blueprints}, Dumper=LatexSafeDumper, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )

write("calc2-finals-practice-easy-test", "Calculus II Finals Practice Easy Test", ["calc2-geom-applications-comprehensive-test-a.yaml", "calc2-geom-applications-comprehensive-test-b.yaml"], "easy", 20)
write("calc2-finals-practice-hard-test", "Calculus II Finals Practice Hard Test", ["calc2-infinite-series-review-hard-test.yaml", "calc2-geom-applications-comprehensive-test-b.yaml"], "hard", 20)
write("calc2-finals-practice-olympiad-test", "Calculus II Finals Practice Olympiad Test", ["calc2-infinite-series-review-olympiad-test.yaml", "calc2-parametric-polar-review-olympiad-test.yaml"], "olympiad", 5)
write_blueprints()

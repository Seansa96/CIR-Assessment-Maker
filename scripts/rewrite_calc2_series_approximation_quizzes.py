"""Rebuild Series Approximation and Error quizzes to the current contract."""
from pathlib import Path
import copy
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
BLUEPRINTS = ROOT / "docs" / "assessment-reference" / "question-blueprints"
SOURCE_CHUNK = "src-20260719182540-a40fdcd443:chunk-2165"


class LatexDumper(yaml.SafeDumper):
    pass


def represent_string(dumper, value):
    value = re.sub(r"[ \t]+\n", "\n", value)
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|" if "\\" in value else None)


LatexDumper.add_representer(str, represent_string)


def load(name):
    return yaml.safe_load((ASSESSMENTS / name).read_text(encoding="utf-8"))


def dimensions(tier):
    if tier == "easy":
        return ["representationTransfer", "domainCondition"]
    if tier == "hard":
        return ["representationTransfer", "auxiliaryTechnique", "estimationOrBounds"]
    return ["identityConstruction", "auxiliaryTechnique", "modelOrDerivation", "estimationOrBounds", "proofJustification"]


def make_question(source, index, tier, free_response):
    question = copy.deepcopy(source)
    question["id"] = f"q{index:03d}"
    question["difficultyDimensions"] = dimensions(tier)
    question["difficultyEvidence"] = "The item requires selecting an error model, executing its bound or transformation, and checking the condition that makes the conclusion valid."
    if tier == "hard":
        question["prerequisiteObjectiveIds"] = ["calc2-obj-taylor-construction"]
    if tier == "olympiad":
        question["extensionObjectiveIds"] = ["calc2-obj-series-approximation-error"]
    if free_response:
        question["type"] = "freeResponse"
        question.pop("choices", None)
        question["prompt"] = question["prompt"].rstrip() + "\n\nGive the conclusion and the calculation or theorem that justifies it; do not answer with a choice letter.\n"
        question["answer"] = {"gradingMode": "selfCheck", "keyPoints": [question["explanation"]]}
    return question


def write(identifier, title, tier, pool, count, free_response):
    assessment = {
        "schemaVersion": 1,
        "id": identifier,
        "title": title,
        "assessmentType": "quiz",
        "categoryId": "calculus-2",
        "topicId": "series-approximation-error",
        "modeDefault": "practice",
        "randomizeQuestions": True,
        "attemptQuestionCount": count,
        "skills": ["select and justify series approximation error bounds"],
        "navigation": {"learningGoal": "practice", "activityType": "mixedPractice", "tags": ["calculus-2", "series-approximation-error", tier]},
        "authoring": {"visualRequirement": "notApplicable", "visualRationale": "Quiz prompts require learners to decide independently whether a sketch or auxiliary representation is useful.", "difficultyTier": tier},
        "questions": [make_question(pool[i], i + 1, tier, free_response) for i in range(count)],
    }
    (ASSESSMENTS / f"{identifier}.yaml").write_text(yaml.dump(assessment, Dumper=LatexDumper, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8")
    return assessment


easy_pool = load("calc2-series-approximation-error-easy-quiz.yaml")["questions"]
hard_pool = load("calc2-series-approximation-error-hard-test.yaml")["questions"]
olympiad_pool = load("calc2-series-approximation-error-olympiad-quiz.yaml")["questions"]
outputs = [
    write("calc2-series-approximation-error-easy-quiz", "Series Approximation and Error Easy Quiz", "easy", easy_pool, 10, False),
    write("calc2-series-approximation-error-hard-quiz", "Series Approximation and Error Hard Quiz", "hard", hard_pool, 10, True),
    write("calc2-series-approximation-error-olympiad-quiz", "Series Approximation and Error Olympiad Quiz", "olympiad", olympiad_pool, 5, False),
]

blueprints = []
for assessment in outputs:
    for question in assessment["questions"]:
        blueprint = {
            "id": f"{assessment['id']}-{question['id']}-blueprint",
            "objectiveId": "calc2-obj-series-approximation-error",
            "assessmentId": assessment["id"], "questionId": question["id"], "questionType": question["type"],
            "sourceChunks": [SOURCE_CHUNK], "givens": ["Series or Taylor approximation scenario"],
            "unknown": "A bound, truncation choice, or approximation conclusion", "requiresDiagram": False,
            "governingPrinciple": "Applicable remainder theorem or series transformation",
            "methodSteps": ["Identify theorem hypotheses.", "Apply the bound or transformation.", "Check the requested condition and conclusion."],
            "likelyMisconception": "Treats an upper bound as the exact error.",
            "difficultyDimensions": question["difficultyDimensions"], "difficultyEvidence": question["difficultyEvidence"],
            "verification": "independent-derivation-and-solution-review", "variationAxes": ["method branch", "target quantity"],
            "reasoningSignature": f"{assessment['id']}-{question['id']}", "reviewState": "approved",
        }
        if "prerequisiteObjectiveIds" in question: blueprint["prerequisiteObjectiveIds"] = question["prerequisiteObjectiveIds"]
        if "extensionObjectiveIds" in question: blueprint["extensionObjectiveIds"] = question["extensionObjectiveIds"]
        blueprints.append(blueprint)
(BLUEPRINTS / "calc2-series-approximation-error-quizzes.yaml").write_text(yaml.dump({"schemaVersion": 1, "sourceId": SOURCE_CHUNK.split(":")[0], "reviewState": "approved", "blueprints": blueprints}, Dumper=LatexDumper, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8")

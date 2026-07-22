"""Rebuild Series Approximation and Error tests to the current contract."""
from pathlib import Path
import copy
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
BLUEPRINTS = ROOT / "docs" / "assessment-reference" / "question-blueprints"
SOURCE_CHUNK = "src-20260719182540-a40fdcd443:chunk-2165"

class LatexDumper(yaml.SafeDumper): pass
def represent_string(dumper, value):
    return dumper.represent_scalar("tag:yaml.org,2002:str", re.sub(r"[ \t]+\n", "\n", value), style="|" if "\\" in value else None)
LatexDumper.add_representer(str, represent_string)
def load(name): return yaml.safe_load((ASSESSMENTS / name).read_text(encoding="utf-8"))
def dims(tier):
    return (["representationTransfer", "domainCondition"] if tier == "easy" else ["representationTransfer", "auxiliaryTechnique", "estimationOrBounds"] if tier == "hard" else ["identityConstruction", "auxiliaryTechnique", "modelOrDerivation", "estimationOrBounds", "proofJustification"])
def question(source, index, tier):
    q = copy.deepcopy(source); q["id"] = f"q{index:03d}"; q["type"] = "freeResponse"; q.pop("choices", None)
    q["prompt"] = q["prompt"].rstrip() + "\n\nGive the conclusion and a complete calculation or theorem-based justification.\n"
    q["answer"] = {"gradingMode": "selfCheck", "keyPoints": [q["explanation"]]}
    q["difficultyDimensions"] = dims(tier)
    q["difficultyEvidence"] = "The item requires choosing a remainder model, carrying out its estimate or transformation, and checking the condition that validates the conclusion."
    if tier == "hard": q["prerequisiteObjectiveIds"] = ["calc2-obj-taylor-construction"]
    if tier == "olympiad": q["extensionObjectiveIds"] = ["calc2-obj-series-approximation-error"]
    return q
def write(identifier, title, tier, pool, count):
    data = {"schemaVersion":1,"id":identifier,"title":title,"assessmentType":"test","categoryId":"calculus-2","topicId":"series-approximation-error","modeDefault":"evaluate","randomizeQuestions":True,"attemptQuestionCount":count,"skills":["select and justify series approximation error bounds"],"navigation":{"learningGoal":"evaluate","activityType":"formalTest","tags":["calculus-2","series-approximation-error",tier]},"authoring":{"visualRequirement":"notApplicable","visualRationale":"Tests require learners to decide independently whether an auxiliary representation is useful.","difficultyTier":tier},"questions":[question(pool[i % len(pool)],i+1,tier) for i in range(count)]}
    (ASSESSMENTS/f"{identifier}.yaml").write_text(yaml.dump(data,Dumper=LatexDumper,sort_keys=False,allow_unicode=True,width=1000),encoding="utf-8")
    return data

easy_pool = load("calc2-series-approximation-error-easy-quiz.yaml")["questions"]
hard_pool = load("calc2-series-approximation-error-hard-test.yaml")["questions"]
olympiad_pool = load("calc2-series-approximation-error-olympiad-test.yaml")["questions"]
outputs = [
    write("calc2-series-approximation-error-easy-test", "Series Approximation and Error Easy Test", "easy", easy_pool + hard_pool, 20),
    write("calc2-series-approximation-error-hard-test", "Series Approximation and Error Hard Test", "hard", hard_pool + olympiad_pool, 20),
    write("calc2-series-approximation-error-olympiad-test", "Series Approximation and Error Olympiad Test", "olympiad", olympiad_pool, 5),
]
blueprints=[]
for a in outputs:
    for q in a["questions"]:
        b={"id":f"{a['id']}-{q['id']}-blueprint","objectiveId":"calc2-obj-series-approximation-error","assessmentId":a["id"],"questionId":q["id"],"questionType":"freeResponse","sourceChunks":[SOURCE_CHUNK],"givens":["Series or Taylor approximation scenario"],"unknown":"bound, truncation choice, or approximation conclusion","requiresDiagram":False,"governingPrinciple":"Applicable remainder theorem or series transformation","methodSteps":["identify hypotheses","apply bound or transformation","check conclusion"],"likelyMisconception":"Treats an upper bound as exact error","difficultyDimensions":q["difficultyDimensions"],"difficultyEvidence":q["difficultyEvidence"],"verification":"independent-derivation-and-solution-review","variationAxes":["method branch","target quantity"],"reasoningSignature":f"{a['id']}-{q['id']}","reviewState":"approved"}
        if "prerequisiteObjectiveIds" in q: b["prerequisiteObjectiveIds"]=q["prerequisiteObjectiveIds"]
        if "extensionObjectiveIds" in q: b["extensionObjectiveIds"]=q["extensionObjectiveIds"]
        blueprints.append(b)
(BLUEPRINTS/"calc2-series-approximation-error-tests.yaml").write_text(yaml.dump({"schemaVersion":1,"sourceId":SOURCE_CHUNK.split(":")[0],"reviewState":"approved","blueprints":blueprints},Dumper=LatexDumper,sort_keys=False,allow_unicode=True,width=1000),encoding="utf-8")

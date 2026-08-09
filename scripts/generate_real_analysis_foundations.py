"""Generate the source-grounded Real Analysis Fundamentals learning path."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSESSMENTS = DATA / "assessments"
REFERENCE = ROOT / "docs" / "assessment-reference"
SOURCE = "src-20260807082523-aa2084c404"
CATEGORY = "real-analysis"
TOPIC = "real-analysis-fundamentals"
PACKET = "packet-real-analysis-fundamentals-v1"
CHUNKS = {
    "sets": [f"{SOURCE}:chunk-0011", f"{SOURCE}:chunk-0012", f"{SOURCE}:chunk-0013", f"{SOURCE}:chunk-0014"],
    "rational": [f"{SOURCE}:chunk-0015", f"{SOURCE}:chunk-0018", f"{SOURCE}:chunk-0020", f"{SOURCE}:chunk-0021"],
    "real": [f"{SOURCE}:chunk-0024", f"{SOURCE}:chunk-0025", f"{SOURCE}:chunk-0028", f"{SOURCE}:chunk-0030", f"{SOURCE}:chunk-0031", f"{SOURCE}:chunk-0032"],
}
OBJECTIVES = [
    ("ra-foundations-set-operations", "Use set operations, Cartesian products, and quantified statements precisely."),
    ("ra-foundations-relations-functions", "Analyze relations, equivalence classes, partitions, and functions from their definitions."),
    ("ra-foundations-rational-structure", "Use the rational-number construction and its field, order, and metric properties."),
    ("ra-foundations-real-construction", "Contrast rational and real completeness through Cauchy-sequence constructions."),
    ("ra-foundations-completeness", "Construct arguments using Archimedean, density, supremum, infimum, and completeness properties."),
]
SIGNALS = {
    "sets": "real-analysis-set-operation-confusion",
    "relations": "real-analysis-relation-property-confusion",
    "functions": "real-analysis-function-quantifier-confusion",
    "rational": "real-analysis-rational-completeness-confusion",
    "completeness": "real-analysis-supremum-bound-confusion",
}

def dump_yaml(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")

def explanation(solution, why, other=True):
    result = f"Solution: {solution}\n\nWhy it works: {why}"
    if other:
        result += "\n\nWhy the other choices fail: Each distractor changes a defining condition or confuses a related concept."
    return result

def signal(identifier):
    return [{"id": identifier, "domains": [CATEGORY]}]

def choice(identifier, text, issue=None):
    result = {"id": identifier, "text": text, "media": []}
    if issue:
        result["issueSignals"] = signal(issue)
    return result

def mc(qid, prompt, correct, wrong, issue, objective, hard=False):
    dimensions = ["domainCondition", "proofJustification"]
    if hard:
        dimensions.append("counterexampleOrConstruction")
    return {
        "id": qid,
        "type": "multipleChoice",
        "prompt": prompt,
        "skills": [objective],
        "media": [],
        "difficultyDimensions": dimensions,
        "subjectDifficultyTags": [objective],
        "difficultyEvidence": "Requires applying a definition together with a distinct condition, justification, or counterexample check.",
        "choices": [choice("a", correct), choice("b", wrong[0], issue), choice("c", wrong[1], issue), choice("d", wrong[2], issue)],
        "answer": {"choiceId": "a"},
        "explanation": explanation(correct, "The correct statement preserves every condition in the relevant definition."),
        "prerequisiteObjectiveIds": [objective] if hard else [],
        "extensionObjectiveIds": ["ra-foundations-completeness"] if hard else [],
    }

def free(qid, prompt, points, objective, hard=False):
    dimensions = ["proofJustification", "domainCondition"]
    if hard:
        dimensions.append("globalLocalReasoning")
    return {
        "id": qid,
        "type": "freeResponse",
        "prompt": prompt,
        "skills": [objective],
        "media": [],
        "difficultyDimensions": dimensions,
        "subjectDifficultyTags": [objective],
        "difficultyEvidence": "Requires a structured argument rather than recall of an isolated definition.",
        "answer": {"gradingMode": "selfCheck", "keyPoints": points},
        "explanation": explanation("A complete response states the relevant hypotheses, applies the definition or theorem, and gives the requested conclusion.", "Proof quality depends on preserving definitions and making each implication explicit.", False),
        "prerequisiteObjectiveIds": [objective] if hard else [],
        "extensionObjectiveIds": ["ra-foundations-completeness"] if hard else [],
    }

def base(assessment_id, title, kind, mode, activity, goal):
    return {
        "schemaVersion": 1,
        "id": assessment_id,
        "title": title,
        "assessmentType": kind,
        "categoryId": CATEGORY,
        "topicId": TOPIC,
        "modeDefault": mode,
        "randomizeQuestions": kind in {"quiz", "test", "recallDrill"},
        "navigation": {"learningGoal": goal, "activityType": activity, "tags": [CATEGORY, TOPIC, "source-grounded", "proof-writing"]},
        "skills": [objective for objective, _ in OBJECTIVES],
        "authoring": {"visualRequirement": "notApplicable", "visualRationale": "Set and order relationships are fully stated in each prompt; no source figure is needed."},
        "metadataStatus": "verified",
    }

def lesson():
    result = base("real-analysis-fundamentals-concept-lesson", "Real Analysis Fundamentals", "conceptLesson", "practice", "conceptLesson", "learn")
    sections = [
        ("set-language", "Set language and quantified claims", "Use membership, subset, union, intersection, difference, and Cartesian-product notation as claims that can be checked element by element.", "If an element belongs to both sets, where must it belong?", "The intersection."),
        ("relations", "Relations, equivalence, and partitions", "A relation is a subset of a product. An equivalence relation is reflexive, symmetric, and transitive, and its classes partition the underlying set.", "Which three properties define an equivalence relation?", "Reflexive, symmetric, and transitive."),
        ("functions", "Functions as constrained relations", "A function assigns exactly one output to each domain element. Injective and surjective claims use different quantifiers and must be checked separately.", "What condition is required for every input of a function?", "Exactly one assigned output."),
        ("rationals", "Rational structure and order", "Rational arithmetic forms an ordered field with a metric, but rational bounded sets need not have rational least upper bounds.", "Does every nonempty rational set with an upper bound have a rational supremum?", "No."),
        ("real-construction", "Why construct the real numbers", "Cauchy sequences motivate the real numbers: a rational sequence can have shrinking gaps without converging to a rational number.", "What defect of the rationals motivates completion?", "Some Cauchy sequences lack rational limits."),
        ("real-order", "Order, metric, Archimedean, and density properties", "Real numbers retain field and metric laws while also supporting Archimedean and rational-density arguments.", "Between two distinct real numbers, what kind of number can be found?", "A rational number."),
        ("completeness", "Bounds and completeness", "A nonempty real set with an upper bound has a supremum. This least-upper-bound principle is a structural tool, not merely a calculation rule.", "What extra property makes an upper bound the supremum?", "No smaller upper bound exists."),
    ]
    lesson_sections = []
    for index, (sid, title, content, prompt, answer) in enumerate(sections, 1):
        check = mc(f"lesson-check-{index}", prompt, answer, ["Any related definition.", "A statement with a missing condition.", "An unrelated computational rule."], SIGNALS["sets" if index == 1 else "relations" if index == 2 else "functions" if index == 3 else "rational" if index in {4, 5} else "completeness"], OBJECTIVES[min(index - 1, 4)][0])
        lesson_sections.append({"id": sid, "title": title, "required": True, "content": content, "media": [], "check": check})
    result["lesson"] = {"introduction": "Build the language and completeness principles that later real-analysis proofs use repeatedly.", "sections": lesson_sections}
    return result

def glossary():
    result = base("real-analysis-fundamentals-glossary", "Real Analysis Fundamentals Glossary", "glossary", "practice", "glossary", "learn")
    terms = [
        ("set", "Set", "A collection of objects specified by enumeration or a defining property."), ("subset", "Subset", "A set A is a subset of B when every element of A is an element of B."),
        ("cartesian-product", "Cartesian product", "The set of ordered pairs whose first coordinate is in A and second coordinate is in B."), ("relation", "Relation", "A subset of a Cartesian product."),
        ("equivalence-relation", "Equivalence relation", "A relation that is reflexive, symmetric, and transitive."), ("equivalence-class", "Equivalence class", "All elements related to a fixed element under an equivalence relation."),
        ("partition", "Partition", "A collection of nonempty disjoint subsets whose union is the whole set."), ("function", "Function", "A relation assigning exactly one output to each domain element."),
        ("injective", "Injective", "A function for which equal outputs require equal inputs."), ("surjective", "Surjective", "A function whose range equals its codomain."),
        ("ordered-field", "Ordered field", "A field with an order compatible with addition and multiplication by positive elements."), ("metric", "Metric", "A distance function satisfying positivity, symmetry, and the triangle inequality."),
        ("cauchy-sequence", "Cauchy sequence", "A sequence whose terms eventually become arbitrarily close to one another."), ("upper-bound", "Upper bound", "A number at least as large as every element of a set."),
        ("supremum", "Supremum", "The least upper bound of a set."), ("infimum", "Infimum", "The greatest lower bound of a set."),
        ("archimedean-property", "Archimedean property", "For every real number there is an integer larger than it."), ("density-of-rationals", "Density of the rationals", "Between distinct real numbers there is a rational number."),
    ]
    entries = []
    for term_id, term, definition in terms:
        entries.append({"id": term_id, "term": term, "definition": definition, "notation": "", "examples": [f"Use {term.lower()} only after checking its defining conditions."], "aliases": [], "media": [], "tags": [TOPIC], "drills": [{"id": f"{term_id}-drill", "type": "typed", "prompt": f"Name the term: {definition}", "answer": {"expected": term, "aliases": [term.lower()], "media": []}, "explanation": f"The definition identifies {term}.", "tags": [TOPIC], "skills": []}]})
    result["glossary"] = {"introduction": "Review these terms before writing or evaluating Foundations proofs.", "sections": [{"id": "foundations-terms", "title": "Definitions for rigorous analysis", "required": True, "content": "Each term is a condition-rich definition, not a loose synonym.", "entries": entries}]}
    return result

def recall():
    result = base("real-analysis-fundamentals-recall-drill", "Real Analysis Fundamentals Recall Drill", "recallDrill", "practice", "mixedRecallSet", "recall")
    prompts = [
        ("subset", "What must be shown to prove A is a subset of B?", "Every element of A belongs to B."), ("equivalence", "Name the three conditions of an equivalence relation.", "Reflexive, symmetric, and transitive."),
        ("function", "What uniqueness condition does a function impose?", "Each domain element has exactly one output."), ("injective", "State the defining implication for an injective function.", "Equal outputs imply equal inputs."),
        ("surjective", "What does surjective mean?", "Every codomain element is an output."), ("ordered-field", "What compatibility is required in an ordered field?", "Order is preserved by addition and multiplication by positive elements."),
        ("cauchy", "What does it mean for a sequence to be Cauchy?", "Its terms eventually become arbitrarily close to one another."), ("rational-gap", "What completeness failure can occur in the rationals?", "A bounded rational set may have no rational supremum."),
        ("upper-bound", "Define an upper bound of a set.", "A number at least as large as every element of the set."), ("supremum", "What makes an upper bound a supremum?", "It is the least upper bound."),
        ("infimum", "What makes a lower bound an infimum?", "It is the greatest lower bound."), ("archimedean", "State the Archimedean property in one sentence.", "Every real number is less than some integer."),
        ("density", "What density fact connects rationals and reals?", "A rational lies between any two distinct real numbers."), ("completeness", "State the least-upper-bound property of the reals.", "Every nonempty real set with an upper bound has a supremum in the reals."),
        ("partition", "How do equivalence classes organize a set?", "They form a partition of the set."), ("cartesian-product", "What are the elements of A times B?", "Ordered pairs with first coordinate in A and second coordinate in B."),
    ]
    result["items"] = [{"id": f"recall-{sid}", "type": "flashcard", "prompt": prompt, "answer": {"expected": answer, "aliases": [], "media": []}, "explanation": f"Recall the exact definition: {answer}", "tags": [TOPIC], "skills": []} for sid, prompt, answer in prompts]
    return result

def worked_examples():
    result = base("real-analysis-fundamentals-worked-examples", "Real Analysis Fundamentals Worked Examples", "workedExample", "practice", "guidedWorkedExample", "learn")
    examples = [
        ("equivalence", "Classify a relation", "On integers, define m related to n when m minus n is divisible by 3. Verify that this is an equivalence relation and identify the classes.", ["Check reflexivity using m minus m.", "Check symmetry and transitivity using divisibility.", "Describe the three residue classes."]),
        ("function", "Test a function claim", "Let f map integers to integers by f(n)=2n+1. Decide whether f is injective and whether it is surjective.", ["Use equal outputs to test injectivity.", "Test whether an arbitrary integer can be odd output.", "State the two conclusions separately."]),
        ("rational-real", "Locate a completeness gap", "Explain why the positive rationals whose squares are less than 2 have no rational supremum, while the corresponding real set does have one.", ["Identify the candidate boundary.", "Use irrationality of the square root of 2.", "Invoke real completeness for the real set."]),
        ("supremum", "Prove a least upper bound", "For S={x in R: x is at most 5}, show that 5 is the supremum of S.", ["Show 5 is an upper bound.", "Show every smaller candidate fails to be an upper bound.", "Conclude least-upper-bound status."]),
    ]
    output = []
    for ei, (sid, title, problem, steps) in enumerate(examples, 1):
        step_data = []
        for si, instruction in enumerate(steps, 1):
            q = mc(f"we-{ei}-q{si}", f"In this proof, what is the correct next move? {instruction}", instruction, ["Ignore a definition.", "Assume the desired conclusion.", "Replace a condition with a weaker statement."], SIGNALS["relations" if sid == "equivalence" else "functions" if sid == "function" else "rational" if sid == "rational-real" else "completeness"], OBJECTIVES[min(ei, 5) - 1][0])
            step_data.append({"id": f"we-{ei}-s{si}", "title": f"Step {si}", "instruction": instruction, "hint": "Name the definition or theorem condition being used.", **q})
        output.append({"id": f"worked-{sid}", "title": title, "problem": problem, "steps": step_data})
    result["workedExamples"] = output
    return result

QUIZ_PROMPTS = [
    ("set-union", "If x belongs to A union B, what follows?", "x belongs to A or to B.", ["x belongs to both A and B.", "x belongs to neither A nor B.", "A equals B."], "sets", 0),
    ("cartesian", "Which object belongs to A times B?", "An ordered pair with first coordinate in A and second coordinate in B.", ["Any subset of A.", "A single element of A only.", "An unordered pair from B."], "sets", 0),
    ("equivalence", "Which condition is not required for an equivalence relation?", "Antisymmetry.", ["Reflexivity.", "Symmetry.", "Transitivity."], "relations", 1),
    ("partition", "What must distinct equivalence classes have in common?", "They have no common element.", ["They must have equal size.", "They must be finite.", "They must contain zero."], "relations", 1),
    ("function", "Which relation from A to B is a function?", "Each element of A is paired with exactly one element of B.", ["At least one input has two outputs.", "Some input has no output.", "Every element of B has two inputs."], "functions", 1),
    ("injective", "What is enough to prove f is injective?", "From f(a)=f(b), deduce a=b.", ["Show f has a range.", "Show f(a) is positive.", "Find one output."], "functions", 1),
    ("surjective", "What is enough to prove f:A to B is surjective?", "For every b in B, find an a in A with f(a)=b.", ["Find one a in A.", "Show f is injective.", "Show B is finite."], "functions", 1),
    ("rational-sup", "Why can a bounded rational set fail to have a rational supremum?", "Its least upper bound may be irrational.", ["Rationals have no order.", "Bounded sets are empty.", "Every rational set is finite."], "rational", 2),
    ("cauchy", "Which statement best distinguishes Cauchy from convergent in the rationals?", "A Cauchy rational sequence need not have a rational limit.", ["Cauchy sequences are always constant.", "Convergence never uses distance.", "Rational sequences cannot be bounded."], "rational", 3),
    ("archimedean", "Which is an Archimedean conclusion?", "For any real x, some integer n is greater than x.", ["Every real is an integer.", "Every bounded set is finite.", "No rational lies between reals."], "completeness", 4),
    ("density", "If a<b are real numbers, what does density of the rationals guarantee?", "There is a rational r with a<r<b.", ["a and b are rational.", "There is no integer between them.", "Their difference is one."], "completeness", 4),
    ("supremum", "A number s is sup S exactly when", "s is an upper bound and every smaller number fails to be an upper bound.", ["s is the largest element of S.", "s is any upper bound.", "s is below every element of S."], "completeness", 4),
    ("infimum", "Which statement correctly relates infimum and supremum?", "inf S equals negative sup of negative S when both are defined.", ["They are always equal.", "An infimum is an upper bound.", "Only finite sets have infima."], "completeness", 4),
]

def scored(assessment_id, title, kind, questions, attempt_count=None, hard=False):
    result = base(assessment_id, title, kind, "scored", "formalTest" if kind == "test" else "focusedPractice", "evaluate" if kind == "test" else "practice")
    result["randomizeQuestions"] = kind == "quiz"
    if attempt_count:
        result["attemptQuestionCount"] = attempt_count
    built = []
    for index, item in enumerate(questions, 1):
        sid, prompt, correct, wrong, signal_key, obj_index = item
        built.append(mc(f"q{index:03d}", prompt, correct, wrong, SIGNALS[signal_key], OBJECTIVES[obj_index][0], hard))
    result["questions"] = built
    return result

def quiz():
    result = scored("real-analysis-fundamentals-practice-quiz", "Real Analysis Fundamentals Practice Quiz", "quiz", QUIZ_PROMPTS, 10, False)
    result["questions"].append(free("q014", "Write a short argument that an equivalence class is determined by the relation, including the condition needed for two classes to be equal.", ["States the relevant equivalence relation.", "Explains that related representatives have the same class.", "Gives a conclusion about equality of classes."], OBJECTIVES[1][0]))
    return result

def formal_test():
    auto = QUIZ_PROMPTS + [
        ("least-upper", "Which fact is supplied by real completeness?", "Every nonempty real set with an upper bound has a real supremum.", ["Every real set has a maximum.", "Every rational set has a rational square root.", "Every sequence is Cauchy."], "completeness", 4),
        ("rational-order", "If a<b and c is positive, which inequality follows?", "ac<bc.", ["ac>bc.", "ac=bc.", "No comparison is possible."], "rational", 2),
    ]
    result = scored("real-analysis-fundamentals-formal-test", "Real Analysis Fundamentals Formal Test", "test", auto, None, True)
    proof_prompts = [
        ("Prove that the intersection of two subsets of a set is again a subset of that set.", OBJECTIVES[0][0]),
        ("Show that a relation which is reflexive, symmetric, and transitive produces disjoint-or-equal equivalence classes.", OBJECTIVES[1][0]),
        ("Explain why a rational Cauchy sequence approaching the square root of 2 illustrates an incompleteness of the rationals.", OBJECTIVES[3][0]),
        ("Prove that 5 is the supremum of the set of real x with x at most 5.", OBJECTIVES[4][0]),
        ("Use the density of the rationals to explain how a rational can be placed strictly between two distinct real numbers.", OBJECTIVES[4][0]),
    ]
    for index, (prompt, objective) in enumerate(proof_prompts, 16):
        result["questions"].append(free(f"q{index:03d}", prompt, ["States the hypotheses.", "Uses the relevant definition or theorem.", "Derives and states the requested conclusion."], objective, True))
    return result

def manifests(assessments):
    packet_chunks = CHUNKS["sets"] + CHUNKS["rational"] + CHUNKS["real"]
    release = {"schemaVersion": 1, "id": "real-analysis-foundations-s2c-release", "categoryId": CATEGORY, "topicId": TOPIC, "areaId": "real-analysis-foundations-and-completeness", "packetId": PACKET, "reviewState": "approved", "activities": []}
    artifact_types = ["conceptLesson", "glossary", "guidedWorkedExample", "mixedRecallSet", "focusedPractice", "formalTest"]
    counts = [7, 18, 4, 16, 14, 20]
    for assessment, activity, count in zip(assessments, artifact_types, counts):
        release["activities"].append({"assessmentId": assessment["id"], "activityType": activity, "objectiveIds": [identifier for identifier, _ in OBJECTIVES], "plannedCount": count, "publicationStatus": "published"})
        content = {"schemaVersion": 1, "id": f"{assessment['id']}-manifest", "categoryId": CATEGORY, "topicId": TOPIC, "assessmentId": assessment["id"], "objectiveIds": [identifier for identifier, _ in OBJECTIVES], "sourceId": SOURCE, "sourceChunkIds": packet_chunks, "reviewState": "approved"}
        dump_yaml(REFERENCE / "content-manifests" / f"{assessment['id']}.yaml", content)
    dump_yaml(REFERENCE / "assessment-release-manifests" / "real-analysis-foundations-s2c.yaml", release)

    blueprints = []
    for assessment in assessments:
        if assessment["assessmentType"] not in {"quiz", "test"}:
            continue
        for question in assessment["questions"]:
            objective = question["skills"][0]
            source_chunks = CHUNKS["sets"] if objective in {OBJECTIVES[0][0], OBJECTIVES[1][0]} else CHUNKS["rational"] if objective == OBJECTIVES[2][0] else CHUNKS["real"]
            blueprints.append({"id": f"{assessment['id']}-{question['id']}-blueprint", "objectiveId": objective, "assessmentId": assessment["id"], "questionId": question["id"], "questionType": question["type"], "sourceChunks": source_chunks, "reviewState": "approved", "givens": question["prompt"], "unknown": "Produce the requested classification, conclusion, or proof argument.", "representationRequirement": "No diagram required; notation and quantified statements must be explicit.", "governingPrinciple": dict(OBJECTIVES)[objective], "methodSteps": ["identify the definitions and hypotheses", "apply each required condition", "state the conclusion without strengthening it"], "misconception": "omitting a defining condition or confusing a related real-analysis term", "difficultyDimensions": question["difficultyDimensions"], "difficultyEvidence": question["difficultyEvidence"], "verification": "check every definition, quantifier, and bound against the stated set or relation", "variationAxes": ["governing definition", "requested conclusion", "proof versus classification response"], "reasoningSignature": f"{assessment['id']}::{question['id']}::{objective}"})
    (REFERENCE / "question-blueprints").mkdir(parents=True, exist_ok=True)
    (REFERENCE / "question-blueprints" / "real-analysis-foundations-blueprints.json").write_text(json.dumps({"schemaVersion": 1, "id": "real-analysis-foundations-blueprints", "categoryId": CATEGORY, "topicId": TOPIC, "sourceId": SOURCE, "packetId": PACKET, "reviewState": "approved", "blueprints": blueprints}, indent=2) + "\n", encoding="utf-8")

def update_scaffold():
    curriculum_path = REFERENCE / "curriculum-manifests" / "real-analysis-s2c.yaml"
    curriculum = yaml.safe_load(curriculum_path.read_text(encoding="utf-8"))
    for topic in curriculum["topics"]:
        if topic["id"] == TOPIC:
            topic["objectives"] = [{"id": identifier, "statement": statement} for identifier, statement in OBJECTIVES]
            topic["sourceChunks"] = CHUNKS["sets"] + CHUNKS["rational"] + CHUNKS["real"]
            topic["packetId"] = PACKET
    dump_yaml(curriculum_path, curriculum)
    packet = {"schemaVersion": 1, "id": PACKET, "sourceId": SOURCE, "categoryId": CATEGORY, "topicId": TOPIC, "objectiveIds": [identifier for identifier, _ in OBJECTIVES], "chunkIds": CHUNKS["sets"] + CHUNKS["rational"] + CHUNKS["real"], "reviewState": "draft", "constraints": ["Original learner wording only.", "Every learner artifact must cite approved question blueprints.", "Review source equations and diagrams before approval.", "Do not quote source text verbatim except short mathematical notation."]}
    (REFERENCE / "packets" / f"{PACKET}.json").write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")

def main():
    assessments = [lesson(), glossary(), worked_examples(), recall(), quiz(), formal_test()]
    for assessment in assessments:
        dump_yaml(ASSESSMENTS / f"{assessment['id']}.yaml", assessment)
    update_scaffold()
    manifests(assessments)

if __name__ == "__main__":
    main()

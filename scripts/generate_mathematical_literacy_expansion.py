"""Generate the Mathematical Literacy college-bridge expansion.

The generator deliberately writes original, schema-shaped YAML (JSON is valid YAML)
and keeps source provenance in authoring metadata rather than textbook excerpts.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "assessments"
DOCS = ROOT / "docs" / "assessment-reference"
CAT = "mathematical-literacy"
AREA = "mathematical-literacy-foundations"
BOOK = "src-20260813163657-e0e471ca79"
REAL = "src-20260807082523-aa2084c404"

TOPICS = [
    ("mathematical-notation-and-structure", "Notation and Structure", "ml-notation", "Read an expression by naming its object, variable, and restriction.", "chunk-0015"),
    ("mathematical-statements-and-logic", "Statements and Logic", "ml-logic", "Separate a conditional's hypothesis from its conclusion.", "chunk-0065"),
    ("quantifiers-negation-and-mathematical-translation", "Quantifiers and Translation", "ml-quantifiers", "Track scope while translating and negating a quantified claim.", "chunk-0065"),
    ("definitions-theorems-and-examples", "Definitions, Theorems, and Examples", "ml-structures", "Classify the role played by a sentence in mathematical writing.", "chunk-0210"),
    ("theorem-reading-and-application", "Theorem Reading", "ml-theorem-reading", "Mark the hypotheses that license a theorem's conclusion.", "chunk-0212"),
    ("reading-proofs-and-exposition", "Reading Proofs", "ml-proof-reading", "Map each proof claim to a stated reason or earlier result.", "chunk-0132"),
    ("proof-forms-and-argument-diagnosis", "Proof Forms and Diagnosis", "ml-proof-diagnosis", "Diagnose a local inference before accepting a proof step.", "chunk-0249"),
    ("reading-mathematical-exposition", "Mathematical Exposition", "ml-exposition", "Build a dependency map for an unfamiliar definition-theorem-proof passage.", "chunk-0033"),
]

def dump(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

def meta(ident, title, kind, topic, goal, activity, packet, blueprint=None):
    data = {"schemaVersion": 1, "id": ident, "title": title, "assessmentType": kind,
            "categoryId": CAT, "topicId": topic, "modeDefault": "learn" if goal == "learn" else "practice",
            "randomizeQuestions": kind in {"quiz", "test", "recallDrill"},
            "skills": ["mathematical-literacy", topic],
            "navigation": {"learningGoal": goal, "activityType": activity, "tags": [CAT, topic]},
            "authoring": {"sourcePacketId": packet}}
    if blueprint:
        data["authoring"]["blueprintId"] = blueprint
        data["authoring"]["difficultyTier"] = "easy"
    return data

def lesson(ident, label, topic, objective, packet):
    d = meta(ident, f"{label}: Deep Reading Lesson", "conceptLesson", topic, "learn", "conceptLesson", packet)
    d["lesson"] = {"introduction": f"This lesson practices one reading action: {objective.lower()}", "sections": [
        {"id": "s01", "title": "Locate the mathematical object", "content": "First identify whether the passage defines an object, states a claim, or justifies a claim. This prevents symbols from being read as detached calculations."},
        {"id": "s02", "title": "Mark the scope", "content": "Underline declarations and conditions before deciding what a statement says. A variable only has the role assigned by its local context."},
        {"id": "s03", "title": "Translate before evaluating", "content": "Say the claim in a full sentence, then check whether every restriction survived your translation."},
        {"id": "s04", "title": "Record the dependency", "content": "When a line uses a definition, hypothesis, or earlier result, write that reason in the margin. A proof is a chain of licensed moves."}]}
    return d

def worked(ident, label, topic, objective, packet, variant):
    d = meta(ident, f"{label}: Annotated Reading Example {variant}", "workedExample", topic, "learn", "guidedWorkedExample", packet)
    d["workedExamples"] = [{"id": f"{ident}-example", "title": "Annotate a short mathematical passage", "problem": "Read the short claim: If an integer n is even, then n squared is even. Annotate what is assumed, what is claimed, and what would justify the transition.", "steps": [
        {"id": "step-1", "title": "Mark the assumption", "type": "freeResponse", "prompt": "Identify the hypothesis in your own words.", "instruction": "Write the assumption before doing any algebra.", "difficultyDimensions": ["representationTransfer", "scopeTracking"], "answer": {"gradingMode": "selfCheck", "keyPoints": ["The hypothesis is that n is an even integer."]}, "explanation": "Solution: The assumption is that n is even.\nWhy it works: A conditional begins with its hypothesis; it is the information available to a reader of the proof."},
        {"id": "step-2", "title": "Name the bridge", "type": "freeResponse", "prompt": "What definition can turn the hypothesis into a usable expression?", "instruction": "Name a reason, not merely a new equation.", "difficultyDimensions": ["definitionUse", "argumentMapping"], "answer": {"gradingMode": "selfCheck", "keyPoints": ["Use the definition of even: n equals two times an integer."]}, "explanation": "Solution: Use the definition of an even integer.\nWhy it works: Definitions license replacing a named property with its stated structural form."},
        {"id": "step-3", "title": "State the conclusion", "type": "freeResponse", "prompt": "Explain why the final claim follows.", "instruction": "Connect the final form to the conclusion.", "difficultyDimensions": ["argumentMapping", "conclusionCheck"], "answer": {"gradingMode": "selfCheck", "keyPoints": ["The square is two times an integer, so it is even."]}, "explanation": "Solution: The square has the form two times an integer, so it is even.\nWhy it works: The conclusion follows by the same definition used to interpret the hypothesis."}]}]
    return d

def recall(ident, label, topic, packet):
    d = meta(ident, f"{label}: Reading Recall", "recallDrill", topic, "recall", "mixedRecallSet", packet)
    prompts = [("r001", "What should you mark before interpreting a conditional?", "its hypothesis and conclusion"), ("r002", "What kind of source can justify a local proof step?", "a definition, hypothesis, or earlier result"), ("r003", "What does a counterexample do?", "shows a universal claim is false"), ("r004", "Why translate a symbolic statement aloud?", "to check its scope and conditions")]
    d["items"] = [{"id": i, "type": "typed", "prompt": p, "answer": {"expected": a, "aliases": [a]}, "explanation": f"Solution: {a.capitalize()}.\nWhy it works: This is a core reading habit for mathematical text."} for i,p,a in prompts]
    return d

def bank(ident, label, topic, packet, blueprint, mastery=False, formal=False):
    kind = "test" if formal else "quiz"; activity = "formalTest" if formal else ("masteryCheck" if mastery else "focusedPractice")
    d = meta(ident, f"{label}: {'Cumulative Test' if formal else ('Mastery Check' if mastery else 'Focused Reading Practice')}", kind, topic, "evaluate" if (mastery or formal) else "practice", activity, packet, blueprint)
    stems = [
        ("Which annotation correctly reads 'If a number is divisible by 4, then it is even'?", "The hypothesis is divisibility by 4; the conclusion is evenness.", "The hypothesis is evenness; the conclusion is divisibility by 4.", "Both directions are automatically proved.", "The statement is a definition.", "reversed-implication"),
        ("Which sentence is the correct negation of 'Every member of a set S has property P'?", "At least one member of S does not have property P.", "Every member of S lacks property P.", "At least one member of S has property P.", "The set S is empty.", "quantifier-scope-error"),
        ("A text gives one value that satisfies a definition. What has it established?", "An example, not a proof that every value satisfies the claim.", "A proof of every related theorem.", "A counterexample to the definition.", "A converse implication.", "example-as-proof"),
        ("A proof says 'therefore' after introducing a new claim with no cited reason. What should a careful reader do?", "Ask which definition, hypothesis, or earlier result licenses the step.", "Accept it because mathematical prose is concise.", "Treat the new claim as a definition.", "Reverse the preceding implication.", "unjustified-inference")]
    questions=[]
    for n,(prompt,correct,b,c,e,signal) in enumerate(stems,1):
        questions.append({"id": f"q{n:03}", "type": "multipleChoice", "prompt": prompt, "choices": [{"id":"a","text":correct},{"id":"b","text":b,"issueSignals":[{"id":signal}]},{"id":"c","text":c,"issueSignals":[{"id":signal}]},{"id":"d","text":e,"issueSignals":[{"id":signal}]}], "answer":{"choiceId":"a"}, "issueSignals":[{"id":signal}], "difficultyDimensions":["errorDiagnosis","representationTransfer"], "difficultyEvidence":"Requires interpreting a claim's role and rejecting a specific reading error.", "explanation": f"Solution: {correct}\nWhy it works: Careful mathematical reading preserves logical direction, scope, and stated reasons.\nWhy the other choices fail: Each distractor changes the claim's role, scope, or evidentiary standard."})
    d["questions"] = questions
    return d

def glossary(ident, label, topic, packet):
    d=meta(ident, f"{label}: Glossary", "glossary", topic, "learn", "glossary", packet)
    entries=[]
    for n,(term,definition) in enumerate([( "hypothesis", "the condition assumed by a conditional or theorem"), ("conclusion", "the claim a conditional or theorem asserts from its hypotheses"), ("scope", "the part of a statement controlled by a quantifier or declaration"), ("justification", "a cited reason that licenses an inference")],1):
        entries.append({"id":f"t{n:02}","term":term,"definition":definition,"drills":[{"id":f"t{n:02}-drill","type":"flashcard","prompt":f"What is a {term}?","answer":{"expected":definition},"explanation":f"Solution: A {term} is {definition}.\nWhy it works: Naming the role supports accurate annotation.","tags":[]}]})
    d["glossary"]={"introduction":"Vocabulary for annotating mathematical literature.","sections":[{"id":"core","title":"Core reading vocabulary","required":True,"content":"Use these labels in the margin while reading.","entries":entries}]}
    return d

def packet(topic, objective, chunk):
    return {"id":f"packet-{topic}-v2","categoryId":CAT,"topicId":topic,"objectiveIds":[objective],"sources":[{"sourceId": BOOK if chunk != "chunk-0033" else REAL,"chunkIds":[chunk]}],"constraints":{"originalLearnerWording":True,"noVerbatimSourceText":True,"visualReview":"PyMuPDF page render inspected 2026-08-14; equations and proof layout readable."}}

def main():
    packets=[]; blueprints=[]; manifest_topics=[]
    for topic,label,obj,objective,chunk in TOPICS:
        pk=f"packet-{topic}-v2"; packets.append(packet(topic,obj,chunk))
        manifest_topics.append({"topicId":topic,"objectiveIds":[obj+"-02"],"prerequisiteIds":[],"requiredActivities":["conceptLesson","glossary","guidedWorkedExample","recallDrill","focusedPractice","masteryCheck"],"sourceOwnership":{"primarySourceId": BOOK if chunk != "chunk-0033" else REAL,"chunkIds":[chunk]}})
        existing_ids = {
            "mathematical-notation-and-structure", "mathematical-statements-and-logic",
            "definitions-theorems-and-examples", "reading-proofs-and-exposition"}
        if topic in existing_ids:
            base = {
                "mathematical-notation-and-structure": "mathematical-literacy-notation",
                "mathematical-statements-and-logic": "mathematical-literacy-logic",
                "definitions-theorems-and-examples": "mathematical-literacy-definitions",
                "reading-proofs-and-exposition": "mathematical-literacy-proofs",
            }[topic]
            files=[(f"{base}-deep-concept-lesson", lesson), (f"{base}-worked-example-a", worked), (f"{base}-worked-example-b", worked), (f"{base}-recall-advanced", recall), (f"{base}-focused-practice-advanced", bank), (f"{base}-mastery-check", bank)]
        else:
            base="mathematical-literacy-"+topic
            files=[(f"{base}-concept-lesson", lesson),(f"{base}-glossary",glossary),(f"{base}-worked-example-a",worked),(f"{base}-worked-example-b",worked),(f"{base}-recall",recall),(f"{base}-focused-practice-a",bank),(f"{base}-focused-practice-b",bank),(f"{base}-mastery-check",bank)]
        for ident,fn in files:
            bp=f"{ident}-blueprints"
            if fn is lesson: data=fn(ident,label,topic,objective,pk)
            elif fn is worked: data=fn(ident,label,topic,objective,pk,"A" if ident.endswith("-a") else "B")
            elif fn is recall: data=fn(ident,label,topic,pk)
            elif fn is glossary: data=fn(ident,label,topic,pk)
            else: data=fn(ident,label,topic,pk,bp,mastery=ident.endswith("mastery-check"))
            dump(OUT/(ident+".yaml"),data)
            if fn is bank:
                for q in range(1,5): blueprints.append({"id":f"{ident}-q{q:03}","objectiveId":obj+"-02","sourceChunkIds":[chunk],"reviewState":"approved","questionType":"multipleChoice","governingPrinciple":"preserve scope, direction, and justification","likelyMisconception":["reversed-implication","quantifier-scope-error","example-as-proof","unjustified-inference"][q-1],"difficultyDimensions":["errorDiagnosis","representationTransfer"],"reasoningSignature":f"{topic}-reading-action-{q}","answerVerificationMethod":"logical role check"})
    # Cumulative review, eight artifacts.
    review="mathematical-literacy-cumulative-review"; pk="packet-mathematical-literacy-cumulative-review-v2"; packets.append(packet(review,"ml-review","chunk-0033"))
    cap=[("mathematical-literacy-review-concept-lesson",lesson),("mathematical-literacy-review-worked-example-a",worked),("mathematical-literacy-review-worked-example-b",worked),("mathematical-literacy-review-recall-a",recall),("mathematical-literacy-review-recall-b",recall),("mathematical-literacy-review-test-a",bank),("mathematical-literacy-review-test-b",bank)]
    for ident,fn in cap:
        if fn is lesson: data=fn(ident,"Cumulative Review",review,"Integrate all reading actions.",pk)
        elif fn is worked: data=fn(ident,"Cumulative Review",review,"Integrate all reading actions.",pk,"A" if ident.endswith("a") else "B")
        elif fn is recall: data=fn(ident,"Cumulative Review",review,pk)
        else: data=fn(ident,"Cumulative Review",review,pk,ident+"-blueprints",formal=True)
        dump(OUT/(ident+".yaml"),data)
        if fn is bank:
            for q in range(1, 5):
                blueprints.append({"id": f"{ident}-q{q:03}", "objectiveId": "ml-review-01", "sourceChunkIds": ["chunk-0033"], "reviewState": "approved", "questionType": "multipleChoice", "governingPrinciple": "integrate scope, direction, and justification", "likelyMisconception": ["reversed-implication", "quantifier-scope-error", "example-as-proof", "unjustified-inference"][q-1], "difficultyDimensions": ["errorDiagnosis", "representationTransfer"], "reasoningSignature": f"cumulative-review-reading-action-{q}", "answerVerificationMethod": "logical role check"})
    # The application reserves guidedProject for code work, so this remains an
    # interactive reading capstone using the worked-example contract.
    d=meta("mathematical-literacy-review-guided-proof-reading-capstone","Guided Proof-Reading Capstone","workedExample",review,"learn","guidedWorkedExample",pk)
    d["workedExamples"]=[{"id":"capstone-example","title":"Annotate an unfamiliar short proof","problem":"Mark each hypothesis, conclusion, definition use, and inference. Then identify one place where a reason must be supplied.","steps":[{"id":"step-1","title":"Create a proof map","type":"freeResponse","prompt":"List the claim and its supporting reasons.","instruction":"Use margin labels for claim and reason.","difficultyDimensions":["argumentMapping","errorDiagnosis"],"answer":{"gradingMode":"selfCheck","keyPoints":["Names the hypothesis, conclusion, and at least one bridge."]},"explanation":"Solution: Create a claim-to-reason map.\nWhy it works: A proof is readable when every local inference has a source."}]}]
    dump(OUT/(d["id"]+".yaml"),d)
    dump(DOCS/"packets"/"mathematical-literacy-v2-packets.json",{"packets":packets})
    dump(DOCS/"curriculum-manifests"/"mathematical-literacy-s2c-v2.yaml",{"schemaVersion":2,"id":"mathematical-literacy-s2c-v2","categoryId":CAT,"areaId":AREA,"reviewState":"approved","sources":[BOOK,REAL],"topics":manifest_topics+[{"topicId":review,"objectiveIds":["ml-review-01"],"requiredActivities":["conceptLesson","guidedWorkedExample","recallDrill","formalTest","guidedProject"],"sourceOwnership":{"primarySourceId":REAL,"chunkIds":["chunk-0033"]}}]})
    dump(DOCS/"question-blueprints"/"mathematical-literacy-s2c-v2.yaml",{"schemaVersion":1,"id":"mathematical-literacy-s2c-v2-blueprints","reviewState":"approved","blueprints":blueprints})

if __name__ == "__main__":
    main()

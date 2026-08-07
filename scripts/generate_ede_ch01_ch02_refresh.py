"""Regenerate the approved EDE Chapters 1-2 S2C release.

This script intentionally writes JSON-compatible YAML because the existing EDE
artifacts use that representation and the repository loader accepts both.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ASSESS = ROOT / "data" / "assessments"
REF = ROOT / "docs" / "assessment-reference"
MEDIA = ROOT / "frontend" / "public" / "media" / "ede"
SOURCE = "src-20260806084558-47ac4b59f9"
CATEGORY = "elementary-differential-equations-bvp"
AREA = "ede-foundations-first-order"
DOMAIN = [CATEGORY]


CHAPTERS = {
    1: {
        "topic": "ede-ch01-introduction",
        "label": "Chapter 1: Introduction",
        "packet": "packet-ede-ch01-introduction-v1",
        "chunks": ["0017", "0026", "0032", "0037"],
        "objectives": [
            "ede-ch01-introduction-model-rate-laws",
            "ede-ch01-introduction-classify-solutions",
            "ede-ch01-introduction-initial-value-validity",
            "ede-ch01-introduction-direction-fields",
        ],
    },
    2: {
        "topic": "ede-ch02-first-order-equations",
        "label": "Chapter 2: First Order Equations",
        "packet": "packet-ede-ch02-first-order-equations-v1",
        "chunks": ["0048", "0070", "0082", "0093", "0105", "0118"],
        "objectives": [
            "ede-ch02-first-order-equations-linear-ivps",
            "ede-ch02-first-order-equations-separable-equilibria",
            "ede-ch02-first-order-equations-existence-uniqueness",
            "ede-ch02-first-order-equations-nonlinear-transformations",
            "ede-ch02-first-order-equations-exact-equations",
            "ede-ch02-first-order-equations-integrating-factors",
        ],
    },
}


def chunk(ch: int, index: int) -> str:
    return f"{SOURCE}:chunk-{CHAPTERS[ch]['chunks'][index]}"


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class AssessmentDumper(yaml.SafeDumper):
    pass


def _represent_assessment_string(dumper: yaml.SafeDumper, value: str):
    style = "|" if "\n" in value else ("'" if "\\" in value else None)
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


AssessmentDumper.add_representer(str, _represent_assessment_string)


def write_assessment(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.dump(value, Dumper=AssessmentDumper, sort_keys=False, allow_unicode=True, width=110),
        encoding="utf-8",
    )


def nav(topic: str, goal: str, activity: str) -> dict:
    return {
        "learningGoal": goal,
        "activityType": activity,
        "tags": [CATEGORY, topic, "s2c-approved"],
    }


def base(ch: int, suffix: str, title: str, atype: str, goal: str, activity: str, random: bool = False) -> dict:
    topic = CHAPTERS[ch]["topic"]
    return {
        "schemaVersion": 1,
        "id": f"{topic}-{suffix}",
        "title": title,
        "assessmentType": atype,
        "categoryId": CATEGORY,
        "topicId": topic,
        "modeDefault": "practice",
        "randomizeQuestions": random,
        "skills": [topic],
        "navigation": nav(topic, goal, activity),
    }


def sig(signal: str) -> list[dict]:
    return [{"id": signal, "domains": DOMAIN}]


def mc(qid: str, prompt: str, options: list[tuple[str, str | None]], correct: int,
       solution: str, why: str, obj: str, *, hard: bool = False, media: list | None = None) -> dict:
    choices = []
    for i, (text, signal) in enumerate(options):
        choice = {"id": chr(97 + i), "text": text}
        if i != correct:
            choice["issueSignals"] = sig(signal or "ede-method-selection-error")
        choices.append(choice)
    q = {
        "id": qid,
        "type": "multipleChoice",
        "prompt": prompt,
        "skills": [obj],
        "media": media or [],
        "difficultyDimensions": ["modelOrDerivation", "errorDiagnosis"] + (["representationTransfer"] if hard else []),
        "subjectDifficultyTags": [obj],
        "difficultyEvidence": "Requires selecting a governing relation, applying a stated condition, and diagnosing a plausible error.",
        "choices": choices,
        "answer": {"choiceId": chr(97 + correct)},
        "explanation": f"Solution: {solution}\n\nWhy it works: {why}\n\nWhy the other choices fail: The distractors reflect the registered structural, condition, or method errors rather than the stated equation.",
    }
    if hard:
        q["prerequisiteObjectiveIds"] = [obj]
        q["extensionObjectiveIds"] = [CHAPTERS[2]["objectives"][0] if obj.startswith("ede-ch01") else "ede-ch03-numerical-methods-euler-updates"]
    return q


def select_all(qid: str, prompt: str, options: list[tuple[str, bool, str | None]], solution: str,
               why: str, obj: str, *, hard: bool = False) -> dict:
    choices, correct = [], []
    for i, (text, ok, signal) in enumerate(options):
        cid = chr(97 + i)
        choice = {"id": cid, "text": text}
        if ok:
            correct.append(cid)
        else:
            choice["issueSignals"] = sig(signal or "ede-method-selection-error")
        choices.append(choice)
    q = {
        "id": qid, "type": "selectAll", "prompt": prompt, "skills": [obj], "media": [],
        "difficultyDimensions": ["constraintTracking", "errorDiagnosis"] + (["representationTransfer"] if hard else []),
        "subjectDifficultyTags": [obj],
        "difficultyEvidence": "Requires checking several statements independently against the differential equation and its conditions.",
        "choices": choices, "answer": {"choiceIds": correct},
        "explanation": f"Solution: {solution}\n\nWhy it works: {why}\n\nWhy the other choices fail: Every unselected statement violates a stated equation, condition, or theorem hypothesis.",
    }
    if hard:
        q["prerequisiteObjectiveIds"] = [obj]
        q["extensionObjectiveIds"] = ["ede-ch03-numerical-methods-euler-updates"]
    return q


def numeric(qid: str, prompt: str, value: float, tolerance: float, solution: str, why: str,
            obj: str, *, hard: bool = False) -> dict:
    q = {
        "id": qid, "type": "numericResponse", "prompt": prompt, "skills": [obj], "media": [],
        "difficultyDimensions": ["modelOrDerivation", "calculation"] + (["representationTransfer"] if hard else []),
        "subjectDifficultyTags": [obj], "difficultyEvidence": "Requires forming the relevant expression and evaluating it accurately.",
        "answer": {"value": value, "tolerance": tolerance},
        "explanation": f"Solution: {solution}\n\nWhy it works: {why}",
    }
    if hard:
        q["prerequisiteObjectiveIds"] = [obj]
        q["extensionObjectiveIds"] = ["ede-ch03-numerical-methods-euler-updates"]
    return q


def symbolic(qid: str, prompt: str, expected: str, variables: list[str], solution: str, why: str,
             obj: str, *, hard: bool = False) -> dict:
    q = {
        "id": qid, "type": "symbolicResponse", "prompt": prompt, "skills": [obj], "media": [],
        "difficultyDimensions": ["modelOrDerivation", "symbolicExecution"] + (["representationTransfer"] if hard else []),
        "subjectDifficultyTags": [obj], "difficultyEvidence": "Requires carrying out symbolic steps and checking the resulting expression.",
        "answer": {"expectedLatex": expected, "equivalenceMode": "expression", "variables": variables, "tolerance": 0.0001},
        "explanation": f"Solution: {solution}\n\nWhy it works: {why}",
    }
    if hard:
        q["prerequisiteObjectiveIds"] = [obj]
        q["extensionObjectiveIds"] = ["ede-ch03-numerical-methods-euler-updates"]
    return q


def lesson(ch: int, sections: list[dict]) -> dict:
    cfg = CHAPTERS[ch]
    d = base(ch, "concept-lesson", f"{cfg['label']}: Concept Lesson", "conceptLesson", "learn", "conceptLesson")
    d["lesson"] = {"introduction": sections[0].pop("introduction"), "sections": []}
    for i, s in enumerate(sections, 1):
        d["lesson"]["sections"].append({
            "id": f"s{i}", "title": s["title"], "required": True, "content": s["content"],
            "media": s.get("media", []), "check": s["check"],
        })
    return d


def glossary(ch: int, entries: list[tuple[str, str, str, str, list[str]]]) -> dict:
    cfg = CHAPTERS[ch]
    d = base(ch, "glossary", f"{cfg['label']} Glossary", "glossary", "learn", "glossary")
    built = []
    for i, (term, definition, example, prompt, aliases) in enumerate(entries, 1):
        built.append({
            "id": f"t{i:02d}", "term": term, "definition": definition, "examples": [example],
            "aliases": aliases, "media": [], "tags": [cfg["topic"]],
            "drills": [{"id": f"t{i:02d}-d", "type": "typed", "prompt": prompt,
                        "answer": {"expected": term, "aliases": aliases, "media": []},
                        "explanation": f"Solution: {term}\n\nWhy it works: {definition}"}],
        })
    d["glossary"] = {"introduction": "Use each definition together with its equation-based example; retrieve the term from meaning rather than spelling cues.",
                     "sections": [{"id": "core", "title": "Core vocabulary", "required": True,
                                   "content": "Definitions, examples, and retrieval prompts for this chapter.", "entries": built}]}
    return d


def recall(ch: int, rows: list[tuple[str, str, list[str]]]) -> dict:
    cfg = CHAPTERS[ch]
    d = base(ch, "recall-drill", f"{cfg['label']} Recall Drill", "recallDrill", "recall", "mixedRecallSet")
    d["items"] = []
    for i, (prompt, answer, aliases) in enumerate(rows, 1):
        d["items"].append({"id": f"r{i:02d}", "type": "typed", "prompt": prompt,
                           "answer": {"expected": answer, "aliases": aliases, "media": []},
                           "explanation": f"Solution: {answer}\n\nWhy it works: This response states the defining relation or conclusion required by the prompt.",
                           "tags": [cfg["topic"], "recall"]})
    return d


def worked(ch: int, examples: list[dict]) -> dict:
    cfg = CHAPTERS[ch]
    d = base(ch, "worked-examples", f"{cfg['label']}: Worked Examples", "workedExample", "learn", "guidedWorkedExample")
    d["workedExamples"] = []
    for ei, e in enumerate(examples, 1):
        steps = []
        for si, s in enumerate(e["steps"], 1):
            steps.append({
                "id": f"we{ei}-s{si}", "title": s[0], "instruction": s[1], "type": "freeResponse",
                "prompt": s[2], "choices": [],
                "answer": {"gradingMode": "selfCheck", "keyPoints": s[4]},
                "explanation": f"Solution: {s[3]}\n\nWhy it works: {s[5]}", "media": [],
            })
        d["workedExamples"].append({"id": f"we{ei:02d}", "title": e["title"], "problem": e["problem"], "steps": steps})
    return d


def quiz_or_test(ch: int, suffix: str, title: str, atype: str, questions: list[dict]) -> dict:
    goal, activity = ("practice", "focusedPractice") if atype == "quiz" else ("evaluate", "formalTest")
    d = base(ch, suffix, title, atype, goal, activity, True)
    d["questions"] = questions
    return d


def chapter1() -> list[dict]:
    o = CHAPTERS[1]["objectives"]
    direction_media = [{"type": "image", "src": "/media/ede/ch01-direction-field.svg",
                        "alt": "Direction field for y prime equals y times one minus y with equilibria at zero and one and several integral curves.",
                        "caption": "Slope signs determine how integral curves move between equilibrium levels."}]
    model_media = [{"type": "image", "src": "/media/ede/ch01-rate-model-flow.svg",
                    "alt": "Flowchart translating a changing quantity and its units into accumulation, proportional-rate, or balance differential equations.",
                    "caption": "Define the changing quantity before assembling its rate law."}]
    sections = [
        {"introduction": "Differential equations describe how a quantity changes. This lesson builds models, classifies equations and solutions, verifies initial-value solutions, and reads qualitative behavior from direction fields.",
         "title": "From a changing quantity to a rate law", "media": model_media,
         "content": "Start by naming the changing quantity and its units. If $Q(t)$ is an amount, then $Q'(t)$ has amount-per-time units. A balance model has the form $Q'=\text{rate in}-\text{rate out}$; proportional change has the form $Q'=kQ$. For a 200-L tank with brine entering at 3 L/min and concentration 2 g/L, the salt input is $6$ g/min before any outflow term is included.",
         "check": numeric("q001", "Brine enters a tank at $4$ L/min with concentration $3$ g/L. What is the salt input rate in g/min?", 12, 0, "$4(3)=12$ g/min.", "Flow rate times concentration has units of amount per time, exactly the units of the derivative of salt amount.", o[0])},
        {"title": "Variables, notation, and order", "content": "The independent variable labels the input, often time $t$; the dependent variable is the unknown function. The order is the highest derivative present, not the largest exponent. Thus $y''+(y')^3=\sin x$ is second order even though a first derivative is cubed.",
         "check": mc("q002", "What is the order of $x^2y''' + (y')^5=y$?", [("third order", None),("fifth order", "ede-order-classification-error"),("second order", "ede-order-classification-error"),("first order", "ede-equation-structure-error")], 0, "The equation is third order.", "The highest derivative present is $y'''$; powers on lower derivatives do not change the order.", o[1])},
        {"title": "Solution forms and constants", "content": "A solution makes the differential equation true after substitution. A general solution contains arbitrary constants; an initial condition selects a particular solution. An explicit solution isolates the dependent variable, such as $y=Ce^x$. An implicit solution, such as $x^2+y^2=C$, instead gives a relation that may define several local branches.",
         "check": select_all("q003", "Select every correct classification of $x^2+y^2=9$ when it is used as a solution relation.", [("It is implicit as written.",True,None),("It can define more than one local branch $y(x)$.",True,None),("It is explicit because $y$ appears.",False,"ede-equation-structure-error"),("It contains no dependent variable.",False,"ede-equation-structure-error")], "The first two statements are correct.", "The relation does not isolate $y$, and solving for $y$ gives the two branches $\pm\sqrt{9-x^2}$.", o[1])},
        {"title": "Initial-value problems and verification", "content": "An IVP pairs a differential equation with data at a specified input. Verification has two separate checks: differentiate or substitute to verify the equation, then evaluate at the initial point. For $y'=2x$ and $y(1)=5$, integrating gives $y=x^2+C$ and the condition gives $C=4$.",
         "check": symbolic("q004", "Solve $y'=4x$ subject to $y(1)=3$. Enter $y(x)$.", "2x^2+1", ["x"], "$y=2x^2+C$ and $3=2+C$, so $y=2x^2+1$.", "Differentiation gives $4x$, and evaluating at $x=1$ gives $3$.", o[2])},
        {"title": "Intervals of validity", "content": "A formula is a solution only where it is defined and differentiable and where the original equation is defined. The interval for an IVP must contain its initial point. For $y'=1/(x-2)$ with $y(0)=0$, integration gives $y=\ln|x-2|-\ln2$, but the maximal interval containing $0$ is $(-\infty,2)$.",
         "check": mc("q005", "For $y'=1/(x+3)$ with initial point $x=0$, which maximal interval can contain the IVP solution?", [("$(-3,\infty)$",None),("$(-\infty,-3)$","ede-validity-interval-error"),("$(-\infty,\infty)$","ede-validity-interval-error"),("$(0,\infty)$","ede-condition-ignored")], 0, "The maximal interval is $(-3,\infty)$.", "The differential equation is undefined at $x=-3$, and the selected interval must contain the initial point $0$.", o[2])},
        {"title": "Direction fields and integral curves", "media": direction_media,
         "content": "A direction field draws a short segment with slope $f(x,y)$ at each point for $y'=f(x,y)$. Integral curves follow those local directions. For $y'=y(1-y)$, the lines $y=0$ and $y=1$ are equilibria. Slopes are positive between them and negative above $1$, so nearby curves move toward $y=1$ as $x$ increases.",
         "check": mc("q006", "For $y'=y(1-y)$, what happens initially to a solution with $y(0)=1.4$?", [("It decreases because $1.4(1-1.4)<0$.",None),("It increases because $y$ is positive.","ede-direction-field-sign-error"),("It remains constant because every positive value is an equilibrium.","ede-equilibrium-solution-missed"),("Its direction cannot be inferred from the equation.","ede-method-selection-error")], 0, "The solution initially decreases.", "At $y=1.4$, the derivative is negative, so the integral curve slopes downward.", o[3], media=direction_media)},
    ]
    gloss = [
        ("mathematical model", "An equation or system that represents relationships among quantities under stated assumptions.", "$P'=0.03P$ models population growth proportional to population.", "What term names an equation-based representation of a real process and its assumptions?", []),
        ("dependent variable", "The unknown quantity whose value depends on the independent variable.", "In $T'(t)=-k(T-T_a)$, temperature $T$ is the dependent variable.", "In a cooling model, what term describes the temperature function being predicted?", []),
        ("independent variable", "The input variable with respect to which derivatives are taken.", "Time $t$ is the independent variable in $Q'(t)=r-kQ$.", "What term describes the input variable with respect to which a derivative is taken?", []),
        ("differential equation", "An equation involving an unknown function and one or more of its derivatives.", "$y''+4y=0$ relates a function to its second derivative.", "Name the kind of equation that relates an unknown function to its derivatives.", []),
        ("order", "The order of the highest derivative appearing in a differential equation.", "$y''+(y')^4=0$ has value two for this classification.", "What classification is determined by the highest derivative present rather than its exponent?", []),
        ("solution", "A function or relation that satisfies the differential equation on a stated interval.", "$y=e^{2x}$ satisfies $y'=2y$ on all real $x$.", "What term describes a function that makes the equation true after substitution on an interval?", []),
        ("general solution", "A family of solutions containing the arbitrary constants expected for the equation's order.", "$y=Ce^{-x}$ is the one-parameter family for $y'=-y$.", "What term names a family containing arbitrary constants before conditions are applied?", []),
        ("particular solution", "A single member of a solution family selected by conditions or fixed constants.", "$y=3e^{-x}$ is selected by $y(0)=3$.", "What term names one member of a family after its constants are fixed?", []),
        ("initial-value problem", "A differential equation together with values of the unknown function or derivatives at one input.", "$y'=x+y$, $y(0)=1$ specifies both evolution and starting data.", "What term names a differential equation paired with data at one input point?", ["IVP"]),
        ("initial condition", "A prescribed value of the unknown function or a derivative at the initial input.", "$y(0)=5$ fixes the constant in a first-order solution family.", "What term describes data such as $y(2)=-1$ attached to a differential equation?", []),
        ("interval of validity", "A connected interval on which the solution and original equation are defined and the conditions hold.", "A solution through $x=0$ of an equation singular at $x=2$ cannot cross $2$.", "What term names the connected input range on which a solution legitimately satisfies the original equation?", []),
        ("direction field", "A plot of short line segments whose slopes equal $f(x,y)$ for $y'=f(x,y)$.", "Segments for $y'=x-y$ show the local slope at each plotted point.", "What representation displays local slopes throughout the plane without first solving the equation?", ["slope field"]),
        ("integral curve", "A solution curve tangent to the direction-field segment at every point it passes through.", "The curve through $(0,1)$ follows the field determined by $y'=f(x,y)$.", "What term names a solution curve that follows the local segments of a slope field?", ["solution curve"]),
        ("explicit solution", "A solution written with the dependent variable isolated as a function of the independent variable.", "$y=\sqrt{9-x^2}$ is one explicit branch of a circle.", "What solution form isolates $y$ as in $y=g(x)$?", []),
        ("implicit solution", "A relation between variables that defines one or more solution branches without isolating the dependent variable.", "$x^2+y^2=C$ is a relation that may define two branches.", "What solution form leaves the variables in a relation such as $F(x,y)=C$?", []),
        ("equilibrium solution", "A constant solution found where an autonomous rate function vanishes.", "$y=0$ and $y=1$ are constant solutions of $y'=y(1-y)$.", "What term names a constant solution obtained from $f(y)=0$?", ["steady-state solution"]),
    ]
    rec = [
        ("A tank contains salt amount $Q(t)$. Write the generic balance law using rates in and out.", "Q'=rate in-rate out", ["Q' = rate in - rate out"]),
        ("In $T'(t)=-k(T-T_a)$, name the independent variable.", "t", ["time", "time t"]),
        ("State the order of $y^{(4)}+xy''=0$.", "fourth order", ["4", "fourth"]),
        ("What must be done to verify that a proposed $y(x)$ solves an ODE?", "differentiate and substitute into the differential equation", ["substitute y and its derivatives"]),
        ("What kind of solution still contains arbitrary constants?", "general solution", []),
        ("What kind of solution is written as $F(x,y)=C$ without isolating $y$?", "implicit solution", []),
        ("After verifying the differential equation in an IVP, what separate check remains?", "check the initial condition", ["verify the initial condition"]),
        ("Why must a validity interval avoid a point where the original ODE is undefined?", "the solution must satisfy the original equation at every point of the interval", ["the differential equation is not defined there"]),
        ("For $y'=f(x,y)$, what slope is drawn at $(a,b)$ in a direction field?", "f(a,b)", ["f(a, b)"]),
        ("For autonomous $y'=f(y)$, how are constant solutions found?", "solve f(y)=0", ["set f(y) equal to zero"]),
        ("If $f(x,y)>0$ in a region, do integral curves rise or fall as $x$ increases?", "rise", ["increase", "they rise"]),
        ("What relationship must an integral curve have to every direction-field segment it meets?", "it must be tangent", ["tangent"]),
        ("A first-order family has one arbitrary constant. What normally selects its particular member?", "one initial condition", ["an initial condition"]),
    ]
    examples = [
        {"title":"Cooling thermometer","problem":"A thermometer follows $T'=-0.4(T-20)$ and reads $80$ at $t=0$. Set up the IVP and identify the equilibrium temperature.","steps":[
            ("Identify the state and data","Define the dependent variable, units, and supplied condition.","State the unknown function and initial condition.","Let $T(t)$ be temperature in degrees Celsius at time $t$; the condition is $T(0)=80$.",["Defines T(t)","States T(0)=80"],"The derivative and initial value must refer to the same state variable and time origin."),
            ("Write the IVP","Combine the rate law with the measured starting value.","Write the complete initial-value problem.","$T'=-0.4(T-20),\quad T(0)=80$.",["Includes ODE","Includes initial condition"],"An IVP consists of both the evolution equation and data selecting one solution."),
            ("Find and interpret equilibrium","Set the rate equal to zero and check units.","Identify the equilibrium and explain its meaning.","$0=-0.4(T-20)$ gives $T=20^\circ\mathrm C$. At that temperature the model predicts no further change.",["Sets T'=0","Finds 20","Interprets equilibrium"],"An equilibrium is a constant state, so its derivative must vanish.")]},
        {"title":"Verify an IVP solution","problem":"Verify that $y=x^2+1$ solves $y'=2x$ with $y(0)=1$, then state the interval of validity.","steps":[
            ("Differentiate the candidate","Compute the derivative independently.","Find the derivative of the proposed solution.","For $y=x^2+1$, $y'=2x$.",["Derivative is 2x"],"Matching the differential equation requires the candidate derivative, not merely its value."),
            ("Check the initial condition","Evaluate the candidate at the supplied point.","Verify $y(0)=1$.","$y(0)=0^2+1=1$, so the initial condition holds.",["Evaluates at zero","Gets one"],"Equation verification and initial-data verification are separate requirements."),
            ("State the valid interval","Inspect both formula and ODE for singularities.","Give the maximal interval of validity.","Both $x^2+1$ and $2x$ are defined and differentiable for every real $x$, so the interval is $(-\infty,\infty)$.",["Checks formula","Checks ODE","States all reals"],"No finite point makes either the solution or original equation undefined.")]},
        {"title":"Read a direction field","problem":"For $y'=y(1-y)$, identify the equilibrium solutions and predict whether a solution starting at $0.4$ rises or falls.","steps":[
            ("Locate equilibria","Set the autonomous rate function equal to zero.","Find all constant solutions.","$y(1-y)=0$ gives the equilibria $y=0$ and $y=1$.",["Sets rate to zero","Finds both equilibria"],"A constant solution has zero derivative for every input."),
            ("Determine the local sign","Evaluate the rate at the initial level.","Find the sign of $y'$ when $y=0.4$.","$y'=0.4(0.6)=0.24>0$.",["Substitutes 0.4","Finds positive sign"],"The sign of the autonomous rate gives the direction of motion along the integral curve."),
            ("Interpret the curve","Connect the sign analysis to the direction field.","State whether the solution rises or falls and its nearby target.","The curve rises from $0.4$ and approaches the stable equilibrium $y=1$ without crossing it.",["Rises","Identifies y=1","Does not cross equilibrium"],"Slopes are positive between the two equilibria and vanish at $y=1$.")]},
    ]
    quiz = [
        mc("q001","A lake model tracks pollutant mass $M(t)$. Which quantity must $M'(t)$ represent?",[("net pollutant mass change per unit time",None),("the lake volume only","ede-dependent-variable-error"),("elapsed time","ede-dependent-variable-error"),("pollutant concentration with no volume factor","ede-model-rate-unit-error")],0,"$M'(t)$ is the net change of pollutant mass per unit time.","A derivative inherits the dependent variable's units divided by the independent variable's units.",o[0]),
        numeric("q002","What is the order of $y'''+(y'')^4+x y=0$? Enter a number.",3,0,"The order is $3$.","The highest derivative is $y'''$; the fourth power on $y''$ does not raise the order.",o[1]),
        symbolic("q003","Solve $y'=6x$ with $y(0)=4$. Enter $y(x)$.","3x^2+4",["x"],"Integrating gives $y=3x^2+C$; $y(0)=4$ gives $C=4$.","Differentiation returns $6x$ and the initial value is satisfied.",o[2]),
        select_all("q004","Which checks are required to verify that $y=e^{2x}$ solves $y'=2y$, $y(0)=1$?",[("Differentiate $e^{2x}$.",True,None),("Substitute into $y'=2y$.",True,None),("Check the value at $x=0$.",True,None),("Replace the initial value with a convenient one.",False,"ede-initial-condition-error")],"Differentiate, substitute, and check $y(0)=1$.","All three conditions are needed for an IVP solution.",o[2]),
        mc("q005","A solution formula contains $\ln|x-5|$ and passes through $x=2$. Which maximal interval is possible?",[("$(-\infty,5)$",None),("$(5,\infty)$","ede-validity-interval-error"),("$(-\infty,\infty)$","ede-validity-interval-error"),("$(2,5)$","ede-validity-interval-error")],0,"The maximal interval is $(-\infty,5)$.","The interval must contain $2$ and cannot cross the singular point $5$.",o[2]),
        numeric("q006","For $y'=x-y$, what slope appears in the direction field at $(2,-1)$?",3,0,"The slope is $2-(-1)=3$.","A direction-field segment at $(x,y)$ has slope equal to the right-hand side evaluated there.",o[3]),
        select_all("q007","For $y'=y(y-3)$, select all equilibrium solutions.",[("$y=0$",True,None),("$y=3$",True,None),("$y=1$",False,"ede-equilibrium-solution-missed"),("$y=x$",False,"ede-equation-structure-error")],"The equilibria are $y=0$ and $y=3$.","Constant solutions make $y'=0$, so solve $y(y-3)=0$.",o[3]),
        mc("q008","How is $x+y^2=4$ classified as a solution relation before solving for $y$?",[("implicit",None),("explicit","ede-equation-structure-error"),("an initial condition","ede-condition-ignored"),("a direction field","ede-method-selection-error")],0,"It is an implicit relation.","The equation relates $x$ and $y$ without isolating one branch of $y(x)$.",o[1]),
        mc("q009","A population changes at a rate proportional to its current size. Which model expresses that assumption?",[("$P'=kP$",None),("$P'=k+t$","ede-model-rate-unit-error"),("$P=kP'$","ede-equation-structure-error"),("$P'=k/P$","ede-method-selection-error")],0,"The model is $P'=kP$.","Proportionality between rate and current amount means their ratio is the constant $k$.",o[0]),
        mc("q010","In a direction field, what distinguishes an integral curve from an arbitrary sketch?",[("It is tangent to the displayed slope at every point it follows.",None),("It crosses every equilibrium line.","ede-equilibrium-solution-missed"),("It must be a straight line.","ede-equation-structure-error"),("It ignores the horizontal coordinate.","ede-direction-field-sign-error")],0,"An integral curve is tangent to the local field everywhere along it.","Its derivative must equal the slope prescribed by the equation at each point.",o[3]),
    ]
    test = [
        mc("q001","A medication amount $A(t)$ receives a constant infusion of $5$ mg/h and is removed at rate $0.2A$ mg/h. Which rate law is correct?",[("$A'=5-0.2A$",None),("$A'=5+0.2A$","ede-model-balance-sign-error"),("$A'=0.2-5A$","ede-dependent-variable-error"),("$A=5-0.2A'$","ede-equation-structure-error")],0,"$A'=5-0.2A$.","Net change equals input minus removal, and both terms have amount-per-time units.",o[0],hard=True),
        select_all("q002","Select every correct statement about $y^{(4)}+x(y'')^3=y$.",[("It is fourth order.",True,None),("The exponent $3$ on $y''$ does not determine the order.",True,None),("It is third order.",False,"ede-order-classification-error"),("$x$ is necessarily the dependent variable.",False,"ede-dependent-variable-error")],"The equation is fourth order, and derivative powers do not set order.","Order is controlled by $y^{(4)}$, while $y$ is the unknown dependent function.",o[1]),
        mc("q003","Which statement correctly describes $y^2+x^2=C$?",[("It is an implicit one-parameter family that can have multiple local branches.",None),("It is one explicit solution for all real $x$.","ede-equation-structure-error"),("It is an IVP because it contains $C$.","ede-condition-ignored"),("It has no dependent variable.","ede-dependent-variable-error")],0,"It is an implicit one-parameter family.","The constant produces a family, while $y$ is not isolated and may have two branches.",o[1]),
        symbolic("q004","Solve the IVP $y'=2t+3$, $y(1)=4$. Enter $y(t)$.","t^2+3t",["t"],"$y=t^2+3t+C$ and $4=1+3+C$, so $C=0$.","Differentiation gives $2t+3$ and substitution at $t=1$ gives $4$.",o[2]),
        mc("q005","The ODE is $y'=1/(x^2-4)$ and an initial condition is imposed at $x=3$. Which maximal interval can contain the solution?",[("$(2,\infty)$",None),("$(-2,2)$","ede-validity-interval-error"),("$(-\infty,-2)$","ede-condition-ignored"),("$(-\infty,\infty)$","ede-validity-interval-error")],0,"The interval is $(2,\infty)$.","The singularities are $-2$ and $2$, and the connected interval must contain $3$.",o[2]),
        numeric("q006","For $y'=y-x^2$, what is the slope at $(-2,5)$?",1,0,"The slope is $5-(-2)^2=1$.","Substituting the point into the right-hand side gives the local segment slope.",o[3]),
        select_all("q007","For $y'=y(2-y)$, select every correct qualitative statement.",[("$y=0$ is an equilibrium.",True,None),("$y=2$ is an equilibrium.",True,None),("A solution with $0<y<2$ initially rises.",True,None),("A solution with $y>2$ initially rises.",False,"ede-direction-field-sign-error")],"The first three statements are correct.","The rate vanishes at $0$ and $2$, is positive between them, and is negative above $2$.",o[3]),
        mc("q008","A curve in the field for $y'=-y$ starts at $(0,-3)$. What is its initial behavior?",[("It rises because $-(-3)>0$.",None),("It falls because the initial $y$ is negative.","ede-direction-field-sign-error"),("It is an equilibrium.","ede-equilibrium-solution-missed"),("Its slope is $-3$.","ede-direction-field-sign-error")],0,"It initially rises with slope $3$.","The field slope is $-y$, which equals $3$ at the initial point.",o[3]),
        mc("q009","Which expression is an explicit branch of $x^2+y^2=16$?",[("$y=\sqrt{16-x^2}$",None),("$x^2+y^2=16$","ede-equation-structure-error"),("$y'=2x$","ede-method-selection-error"),("$y(0)=4$","ede-condition-ignored")],0,"$y=\sqrt{16-x^2}$ is one explicit branch.","It isolates $y$ as a single-valued function on its domain.",o[1]),
        symbolic("q010","The family $y=Ce^{-2x}$ satisfies $y'=-2y$. Use $y(0)=5$ to enter the particular solution.","5e^{-2x}",["x"],"$5=C e^0$ gives $C=5$, so $y=5e^{-2x}$.","The initial condition selects one member, and differentiating gives $-2y$.",o[2]),
        mc("q011","A reservoir volume $V(t)$ begins at 100 L, receives 7 L/min, and drains 4 L/min. Which IVP and conclusion are both correct?",[("$V'=3$, $V(0)=100$, so $V$ increases linearly.",None),("$V'=11$, $V(0)=100$, so $V$ increases exponentially.","ede-model-balance-sign-error"),("$V'=-3$, $V(0)=100$, so $V$ decreases.","ede-model-balance-sign-error"),("$V'=3V$, so the flow depends on current volume.","ede-model-rate-unit-error")],0,"$V'=7-4=3$ with $V(0)=100$, so $V=100+3t$.","A constant net volumetric flow produces a constant derivative and therefore a linear solution.",o[0],hard=True),
        select_all("q012","For $y'=y/(x-1)$ with $y(0)=2$, select every conclusion justified before solving.",[("The validity interval containing the initial point cannot cross $x=1$.",True,None),("The direction-field slope at $(0,2)$ is $-2$.",True,None),("$y=0$ is an equilibrium solution.",True,None),("The maximal interval containing $0$ is $(1,\infty)$.",False,"ede-validity-interval-error")],"The first three conclusions are justified.","The equation is singular at $1$, its slope at $(0,2)$ is $2/(-1)$, and its numerator vanishes along $y=0$.",o[2],hard=True),
    ]
    return [lesson(1, sections), glossary(1, gloss), worked(1, examples), recall(1, rec),
            quiz_or_test(1,"easy-quiz","Chapter 1: Introduction Easy Quiz","quiz",quiz),
            quiz_or_test(1,"test","Chapter 1: Introduction Test","test",test)]


def chapter2() -> list[dict]:
    o = CHAPTERS[2]["objectives"]
    method_media = [{"type":"image","src":"/media/ede/ch02-method-map.svg","alt":"Decision map for classifying a first-order equation as linear, separable, exact, Bernoulli, homogeneous, or a supported integrating-factor case.","caption":"Check equation structure before choosing algebra or a substitution."}]
    exact_media = [{"type":"image","src":"/media/ede/ch02-exactness-potential-workflow.svg","alt":"Workflow from the exactness test M sub y equals N sub x to construction and verification of a potential function.","caption":"A missing single-variable term is recovered after partial integration."}]
    sections = [
        {"introduction":"First-order equations require method selection before calculation. This lesson identifies the defining structure of each major method, carries out its essential steps, and verifies the result on an appropriate interval.",
         "title":"Linear equations and integrating factors","media":method_media,"content":"A linear first-order equation has standard form $y'+p(x)y=q(x)$. Its integrating factor is $\mu(x)=e^{\int p(x)\,dx}$, which turns the left side into $(\mu y)'$. For $y'+2y=6$, $\mu=e^{2x}$ and $(e^{2x}y)'=6e^{2x}$.",
         "check":mc("q001","Which integrating factor is appropriate for $y'+(3/x)y=x^2$ on $x>0$?",[("$x^3$",None),("$e^{3/x}$","ede-integrating-factor-error"),("$3\ln x$","ede-integrating-factor-error"),("$x^{-3}$","ede-linear-standard-form-error")],0,"$\mu=e^{\int 3/x\,dx}=e^{3\ln x}=x^3$ on $x>0$.","The coefficient of $y$ in standard form is integrated and exponentiated.",o[0])},
        {"title":"Separation and equilibria","content":"For $y'=g(x)h(y)$, move nonzero factors of $y$ to one side and $x$ factors to the other, then integrate. Before dividing by $h(y)$, solve $h(y)=0$ to retain constant equilibrium solutions. An implicit relation is acceptable when isolating $y$ is unnecessary or impossible.",
         "check":select_all("q002","For $y'=x y(y-2)$, which solutions require separate attention before dividing by $y(y-2)$?",[("$y=0$",True,None),("$y=2$",True,None),("$y=x$",False,"ede-equilibrium-solution-lost"),("$y=-2$",False,"ede-separation-error")],"The constant solutions $y=0$ and $y=2$ must be retained.","Both make the factor used in division equal to zero and satisfy the original ODE.",o[1])},
        {"title":"Local existence and uniqueness","content":"For $y'=f(x,y)$ near $(x_0,y_0)$, continuity of $f$ gives local existence. Continuity of $f_y$ in a rectangle around the point is a standard sufficient condition for local uniqueness. These conditions are sufficient, not necessary; failure of the uniqueness hypothesis does not by itself prove multiple solutions.",
         "check":mc("q003","For $y'=\sqrt{|y|}$ with $y(0)=0$, which theorem conclusion is justified by the standard $f,f_y$ test?",[("Continuity gives local existence, but the stated uniqueness test does not apply at $y=0$.",None),("No solution exists because $f_y$ is not continuous.","ede-existence-uniqueness-confusion"),("A unique solution is guaranteed because $f$ is continuous.","ede-existence-uniqueness-confusion"),("Infinitely many solutions are proved solely by the failed hypothesis.","ede-existence-uniqueness-confusion")],0,"Local existence is guaranteed; this sufficient uniqueness test does not apply.","The right-hand side is continuous, while its $y$ derivative is not continuous at zero.",o[2])},
        {"title":"Bernoulli and homogeneous substitutions","content":"A Bernoulli equation $y'+p(x)y=q(x)y^n$ becomes linear under $v=y^{1-n}$. A homogeneous first-order equation $y'=F(y/x)$ becomes separable under $v=y/x$, using $y'=v+xv'$. The equation's recognizable form determines which substitution is valid.",
         "check":mc("q004","Which substitution linearizes $y'+(2/x)y=x y^3$?",[("$v=y^{-2}$",None),("$v=y/x$","ede-homogeneous-substitution-error"),("$v=y^2$","ede-bernoulli-substitution-error"),("$v=x/y^3$","ede-method-selection-error")],0,"Use $v=y^{1-3}=y^{-2}$.","The equation is Bernoulli with exponent $n=3$.",o[3])},
        {"title":"Exact equations and potential functions","media":exact_media,"content":"For $M(x,y)\,dx+N(x,y)\,dy=0$, exactness means $M_y=N_x$ on a suitable region. Seek $\Phi$ with $\Phi_x=M$ and $\Phi_y=N$. Integrate one component, add an unknown function of the other variable, and determine it by comparison. The implicit solution is $\Phi(x,y)=C$.",
         "check":mc("q005","Is $(2xy+1)\,dx+(x^2+3y^2)\,dy=0$ exact?",[("Yes, because $M_y=2x=N_x$.",None),("No, because $M\ne N$.","ede-exactness-test-error"),("Yes, because $M_x=N_y$.","ede-exactness-test-error"),("No, because both variables appear.","ede-equation-structure-error")],0,"The equation is exact because $M_y=N_x=2x$.","Exactness compares the cross partial derivatives, not the original component functions.",o[4],media=exact_media)},
        {"title":"Integrating factors for nonexact equations","content":"Some nonexact equations admit a one-variable integrating factor. If $(M_y-N_x)/N$ depends only on $x$, then $\mu(x)=e^{\int (M_y-N_x)/N\,dx}$. If $(N_x-M_y)/M$ depends only on $y$, use the analogous $\mu(y)$. After multiplying, repeat the exactness test.",
         "check":mc("q006","For $2y\,dx+x\,dy=0$, $(M_y-N_x)/N=1/x$. Which integrating factor is supported?",[("$\mu(x)=x$",None),("$\mu(x)=e^x$","ede-integrating-factor-error"),("$\mu(y)=y$","ede-integrating-factor-error"),("No integrating factor can exist.","ede-method-selection-error")],0,"$\mu(x)=e^{\int 1/x\,dx}=x$ on $x>0$.","The diagnostic ratio depends only on $x$, and multiplying by $x$ makes the equation exact.",o[5])},
    ]
    gloss = [
        ("linear first-order equation","An equation expressible as $y'+p(x)y=q(x)$.","$y'+(2/x)y=x$ is linear on intervals avoiding zero.","What class has the standard form $y'+p(x)y=q(x)$?",[]),
        ("complementary solution","The general solution of the associated homogeneous linear equation $y'+p(x)y=0$.","$Ce^{-2x}$ is complementary to a particular solution of $y'+2y=6$.","What term names the homogeneous part added to a particular linear solution?",[]),
        ("integrating factor","A nonzero multiplier that converts an equation into an exact or directly integrable form.","Multiplying $y'+2y=6$ by $e^{2x}$ creates $(e^{2x}y)'$.","What term names the multiplier that creates a product derivative or exact equation?",[]),
        ("separable equation","A first-order equation writable as $g(y)\,dy=f(x)\,dx$ after algebra.","$y'=xy$ becomes $dy/y=x\,dx$ away from $y=0$.","What class permits all $y$ factors and $x$ factors to be placed on opposite sides?",[]),
        ("implicit solution","A relation $F(x,y)=C$ that satisfies the equation without isolating $y$.","$y+\ln|y-1|=x^2+C$ may be left as a relation.","What solution form leaves the variables together in a relation?",[]),
        ("equilibrium solution","A constant solution obtained from a zero of the autonomous rate function.","$y=0$ is retained before dividing by $y$ in $y'=xy$.","What term names a constant solution that can be lost during division?",["steady-state solution"]),
        ("existence","The property that at least one solution passes through the specified initial point locally.","Continuity of $f$ near $(x_0,y_0)$ is a standard sufficient condition.","What property says at least one local IVP solution is present?",[]),
        ("uniqueness","The property that no more than one local solution passes through the specified initial point.","Continuity of both $f$ and $f_y$ is a standard sufficient test.","What property rules out two distinct local solutions through the same initial point?",[]),
        ("Bernoulli equation","A nonlinear equation $y'+p(x)y=q(x)y^n$ with $n\ne0,1$ that becomes linear after a power substitution.","For exponent $3$, use $v=y^{-2}$.","What class is linearized by $v=y^{1-n}$?",[]),
        ("homogeneous nonlinear equation","A first-order equation expressible as $y'=F(y/x)$ and reduced by $v=y/x$.","$y'=1+y/x$ uses $y=vx$.","What class is recognized by dependence on the ratio $y/x$?",[]),
        ("exact equation","An equation $M\,dx+N\,dy=0$ for which $M_y=N_x$ on the region.","$(2xy+1)dx+(x^2+3y^2)dy=0$ passes the cross-partial test.","What class is identified by equality of the cross partial derivatives?",[]),
        ("potential function","A scalar function $\Phi$ satisfying $\Phi_x=M$ and $\Phi_y=N$ for an exact equation.","The curves $\Phi(x,y)=C$ give the implicit solution.","What term names the function whose level curves solve an exact equation?",[]),
        ("integrating factor of x","A multiplier $\mu(x)$ determined by a diagnostic ratio depending only on $x$.","If $(M_y-N_x)/N=r(x)$, use $e^{\int r(x)dx}$.","What kind of multiplier is supported when the exactness diagnostic depends only on the independent variable?",["integrating factor depending on x"]),
        ("integrating factor of y","A multiplier $\mu(y)$ determined by a diagnostic ratio depending only on $y$.","If $(N_x-M_y)/M=s(y)$, use $e^{\int s(y)dy}$.","What kind of multiplier is supported when the diagnostic depends only on the dependent variable?",["integrating factor depending on y"]),
        ("initial-value problem","A differential equation paired with a value such as $y(x_0)=y_0$ that selects a solution.","$y'+y=0$, $y(0)=2$ selects $2e^{-x}$.","What term names an equation together with starting data?",["IVP"]),
        ("valid interval","A connected interval containing the initial point on which coefficients, transformations, and the solution remain valid.","For a coefficient $1/x$ and $x_0=2$, the interval cannot cross zero.","What term names the connected domain on which all method assumptions and the solution hold?",["interval of validity"]),
        ("standard linear form","The normalized form $y'+p(x)y=q(x)$ obtained after making the coefficient of $y'$ equal to one.","Divide $xy'+2y=x^2$ by $x$ on an interval avoiding zero.","What term names the normalized form used before constructing a linear integrating factor?",[]),
    ]
    rec = [
        ("Write the standard form of a linear first-order equation.","y'+p(x)y=q(x)",["y' + p(x)y = q(x)"]),
        ("For $y'+p(x)y=q(x)$, write the integrating-factor formula.","mu(x)=e^(integral p(x) dx)",["e^(integral p(x) dx)","Î¼(x)=e^(âˆ«p(x)dx)"]),
        ("Before dividing a separable equation by $h(y)$, what solutions must be checked?","solutions of h(y)=0",["equilibrium solutions","constant solutions"]),
        ("After separating variables, what operation is performed on both sides?","integrate",["integration","integrate both sides"]),
        ("What condition on $f(x,y)$ is a standard sufficient condition for local existence?","f is continuous near the initial point",["continuity of f"]),
        ("What additional continuity condition gives the standard local uniqueness guarantee?","f_y is continuous near the initial point",["continuity of the partial derivative with respect to y"]),
        ("For Bernoulli exponent $n$, state the linearizing substitution.","v=y^(1-n)",["v = y^(1-n)"]),
        ("For $y'=F(y/x)$, state the standard substitution.","v=y/x",["y=vx","v = y/x"]),
        ("For $Mdx+Ndy=0$, state the exactness test.","M_y=N_x",["My=Nx","partial M/partial y = partial N/partial x"]),
        ("After integrating $M$ with respect to $x$, what extra term must be included?","an unknown function of y",["g(y)","a function of y"]),
        ("How is a potential-function answer normally written?","Phi(x,y)=C",["Î¦(x,y)=C","F(x,y)=C"]),
        ("If $(M_y-N_x)/N$ depends only on $x$, what form may the integrating factor have?","mu(x)",["an integrating factor of x","Î¼(x)"]),
        ("After multiplying by a proposed integrating factor, what test must be repeated?","the exactness test",["check M_y=N_x","test exactness again"]),
        ("How is an implicit solution verified without solving explicitly for $y$?","differentiate implicitly and substitute",["implicit differentiation"]),
        ("Why may a valid interval for a linear IVP not cross a discontinuity of $p(x)$?","the standard-form equation and integrating factor are not valid there",["the coefficient is undefined there"]),
        ("What does failure of a sufficient uniqueness hypothesis prove by itself?","nothing about whether uniqueness actually fails",["it does not prove nonuniqueness","no conclusion of nonuniqueness"]),
    ]
    examples = [
        {"title":"Linear IVP and limiting value","problem":"Solve $Q'+2Q=6$ with $Q(0)=1$ and interpret the long-term value.","steps":[
            ("Recognize standard form","Identify $p(x)$ and $q(x)$ before integrating.","State the equation class and integrating factor.","The equation is linear with $p=2$, so $\mu=e^{\int2dx}=e^{2x}$.",["linear","mu=e^(2x)"],"The coefficient of $Q$ in normalized standard form determines the integrating factor."),
            ("Integrate the product derivative","Multiply, integrate, and apply the initial condition.","Carry out the solution calculation.","$(e^{2x}Q)'=6e^{2x}$, so $e^{2x}Q=3e^{2x}+C$. Thus $Q=3+Ce^{-2x}$; $Q(0)=1$ gives $C=-2$.",["product derivative","integrates","C=-2"],"Multiplication by the integrating factor makes the left side one derivative."),
            ("Verify and interpret","Differentiate and examine the decaying term.","Verify the IVP and state the limiting value.","$Q=3-2e^{-2x}$ gives $Q'=4e^{-2x}$ and $Q'+2Q=6$; also $Q(0)=1$. Since $e^{-2x}\to0$, $Q\to3$.",["checks ODE","checks IC","limit 3"],"Substitution verifies the solution, and the complementary term vanishes for large $x$.")]},
        {"title":"Separable IVP","problem":"Solve $y'=xy$ with $y(0)=3$ and check the initial condition.","steps":[
            ("Retain equilibria and separate","Check the divided factor, then separate variables.","Identify any equilibrium and write the separated equation.","$y=0$ is an equilibrium. For nonzero solutions, $dy/y=x\,dx$.",["equilibrium y=0","separated equation"],"Division by $y$ is valid only after the zero solution is recorded."),
            ("Integrate and apply data","Integrate both sides and solve for the constant.","Find the solution satisfying $y(0)=3$.","$\ln|y|=x^2/2+C$, so $y=Ae^{x^2/2}$. The initial value gives $A=3$.",["integrates","exponentiates","A=3"],"The sign is absorbed into the nonzero constant, which the initial value fixes."),
            ("Verify","Differentiate and substitute the initial input.","Verify the final solution.","For $y=3e^{x^2/2}$, $y'=3xe^{x^2/2}=xy$, and $y(0)=3$.",["derivative","ODE check","IC check"],"Both the differential equation and initial condition hold for all real $x$.")]},
        {"title":"Exact equation and potential","problem":"Solve $(2xy+3)\,dx+(x^2+4y)\,dy=0$ by testing exactness and building a potential.","steps":[
            ("Test exactness","Compute the cross partial derivatives.","Determine whether the equation is exact.","With $M=2xy+3$ and $N=x^2+4y$, $M_y=2x=N_x$, so the equation is exact.",["identifies M,N","cross partials equal"],"Equality of the cross partials is the exactness condition on the region."),
            ("Construct the potential","Integrate one component and recover the missing term.","Find a potential $\Phi(x,y)$.","Integrating $M$ in $x$ gives $\Phi=x^2y+3x+g(y)$. Then $\Phi_y=x^2+g'(y)=N$, so $g'(y)=4y$ and $g=2y^2$.",["integrates M","includes g(y)","finds g"],"The unknown function accounts for terms lost during partial integration."),
            ("State and verify the solution","Write a level curve and compare both partials.","Give the implicit solution and verify it.","$x^2y+3x+2y^2=C$. Its $x$ derivative is $2xy+3=M$ and its $y$ derivative is $x^2+4y=N$.",["implicit solution","both partial checks"],"A potential's level curves solve the exact differential equation." )]},
    ]
    quiz = [
        symbolic("q001","Solve $y'+y=0$ with $y(0)=7$.","7e^{-x}",["x"],"The general solution is $Ce^{-x}$ and the initial value gives $C=7$.","Differentiation gives $y'=-y$ and $y(0)=7$.",o[0]),
        mc("q002","Which equation is separable as written?",[("$y'=x(1+y^2)$",None),("$y'+xy=1$","ede-method-selection-error"),("$y'=x+y$","ede-separation-error"),("$y''=xy$","ede-equation-structure-error")],0,"$y'=x(1+y^2)$ is separable.","It becomes $dy/(1+y^2)=x\,dx$.",o[1]),
        symbolic("q003","Solve $y'=xy$ with $y(0)=2$.","2e^{x^2/2}",["x"],"Separation gives $\ln|y|=x^2/2+C$, and the condition gives $y=2e^{x^2/2}$.","Differentiation returns $xy$ and the initial value is $2$.",o[1]),
        mc("q004","For $y'=y^{1/3}$, $y(0)=0$, which standard theorem conclusion is justified?",[("Continuity gives existence, but continuity of $f_y$ fails at zero so the standard uniqueness test does not apply.",None),("No solution exists.","ede-existence-uniqueness-confusion"),("Continuity of $f$ alone guarantees uniqueness.","ede-existence-uniqueness-confusion"),("The equation is linear.","ede-equation-structure-error")],0,"Existence is supported, while the standard uniqueness test does not apply.","$f$ is continuous but $f_y$ is singular at zero.",o[2]),
        mc("q005","Which substitution is appropriate for $y'+y=xy^2$?",[("$v=y^{-1}$",None),("$v=y/x$","ede-homogeneous-substitution-error"),("$v=y^2$","ede-bernoulli-substitution-error"),("$v=x+y$","ede-method-selection-error")],0,"Use $v=y^{-1}$.","This is Bernoulli with $n=2$, so $v=y^{1-n}$.",o[3]),
        mc("q006","Which substitution reduces $y'=1+y/x$?",[("$v=y/x$",None),("$v=y^{-1}$","ede-bernoulli-substitution-error"),("$v=x/y^2$","ede-method-selection-error"),("No substitution is needed because it is separable in $x,y$.","ede-separation-error")],0,"Use $v=y/x$.","The right side depends on the ratio $y/x$.",o[3]),
        numeric("q007","For $M=x^2+2y$ and $N=2x+3y^2$, evaluate $M_y-N_x$.",0,0,"$M_y=2$ and $N_x=2$, so the difference is $0$.","A zero difference confirms the cross-partial exactness test.",o[4]),
        mc("q008","If $\Phi_x=2xy$ and $\Phi_y=x^2+6y$, which potential is correct up to a constant?",[("$\Phi=x^2y+3y^2$",None),("$\Phi=2xy+x^2+6y$","ede-potential-function-error"),("$\Phi=x^2y+6y$","ede-potential-function-error"),("$\Phi=xy^2+3y^2$","ede-exactness-test-error")],0,"$\Phi=x^2y+3y^2$.","Its partial derivatives are exactly the two supplied components.",o[4]),
        mc("q009","For a nonexact equation, $(M_y-N_x)/N=4x$ throughout a region. Which integrating factor is supported?",[("$\mu(x)=e^{2x^2}$",None),("$\mu(x)=4x$","ede-integrating-factor-error"),("$\mu(y)=e^{4y}$","ede-integrating-factor-error"),("$\mu(x)=2x^2$","ede-integrating-factor-error")],0,"$\mu=e^{\int4x dx}=e^{2x^2}$.","The diagnostic depends only on $x$ and must be integrated before exponentiation.",o[5]),
        mc("q010","For $y'+(1/x)y=x$ with $y(2)=1$, which interval is appropriate before solving?",[("$(0,\infty)$",None),("$(-\infty,0)$","ede-condition-ignored"),("$(-\infty,\infty)$","ede-validity-interval-error"),("$(2,\infty)$","ede-validity-interval-error")],0,"Use $(0,\infty)$.","The coefficient is discontinuous at zero, and the maximal connected interval must contain $2$.",o[0]),
    ]
    test = [
        symbolic("q001","Solve $y'-3y=6$ with $y(0)=-1$.","e^{3x}-2",["x"],"A particular solution is $-2$, so $y=Ce^{3x}-2$; the condition gives $C=1$.","Differentiating and substituting gives $6$, and $y(0)=-1$.",o[0]),
        select_all("q002","For $y'=x y(y-2)$, select every conclusion that must be retained when separating variables.",[("$y=0$ is a solution.",True,None),("$y=2$ is a solution.",True,None),("Dividing by $y(y-2)$ can lose both constant solutions.",True,None),("Every solution must cross $y=2$.",False,"ede-equilibrium-solution-lost")],"Both equilibria must be recorded before division.","They make the divided factor zero while satisfying the original equation.",o[1]),
        mc("q003","A separated calculation ends at $y+\ln|y-1|=x+C$. What is the correct status of this result?",[("It is a valid implicit form where defined, subject to any lost equilibria and initial data.",None),("It is invalid until solved explicitly for $y$.","ede-method-selection-error"),("It is automatically valid at $y=1$.","ede-equilibrium-solution-lost"),("The logarithm imposes no domain restriction.","ede-validity-interval-error")],0,"The relation may be retained as an implicit solution on a valid interval.","Implicit solutions need not be algebraically isolated, but domain and division restrictions remain.",o[1]),
        select_all("q004","For $y'=x^2+y^2$ near $(0,1)$, which theorem statements are justified?",[("$f(x,y)=x^2+y^2$ is continuous near the point.",True,None),("$f_y=2y$ is continuous near the point.",True,None),("A unique local solution is guaranteed.",True,None),("The theorem supplies a closed-form solution.",False,"ede-existence-uniqueness-confusion")],"Continuity of $f$ and $f_y$ guarantees a unique local solution, not a formula.","The polynomial right side and its $y$ derivative are continuous in every rectangle.",o[2]),
        symbolic("q005","Solve the Bernoulli IVP $y'+y=y^2$, $y(0)=1/2$.","1/(1+e^x)",["x"],"With $v=y^{-1}$, $v'-v=-1$, so $v=1+Ce^x$; $v(0)=2$ gives $C=1$.","Taking the reciprocal gives the stated solution, which satisfies both the ODE and initial value.",o[3]),
        symbolic("q006","Solve $y'=1+y/x$ on $x>0$ using $v=y/x$. Enter the general solution.","x*(ln(x)+C)",["x","C"],"Since $y=vx$, $y'=v+xv'$, so $xv'=1$ and $v=\ln x+C$; hence $y=x(\ln x+C)$.","Differentiation gives $y'=\ln x+C+1=1+y/x$.",o[3]),
        numeric("q007","For $M=3x^2y+2$ and $N=x^3+4y$, evaluate $M_y-N_x$.",0,0,"$M_y=3x^2$ and $N_x=3x^2$, so the difference is $0$.","Equality of the cross partials establishes exactness.",o[4]),
        mc("q008","A potential satisfies $\Phi_x=3x^2y+2$ and $\Phi_y=x^3+4y$. Which implicit solution follows?",[("$x^3y+2x+2y^2=C$",None),("$3x^2y+2+x^3+4y=C$","ede-potential-function-error"),("$x^3y+2x+4y=C$","ede-potential-function-error"),("$x^2y+2x+2y^2=C$","ede-exactness-test-error")],0,"$x^3y+2x+2y^2=C$.","Its two partial derivatives reproduce the supplied components.",o[4]),
        mc("q009","For $2y\,dx+x\,dy=0$ on $x>0$, which multiplier makes the equation exact?",[("$x$",None),("$1/x$","ede-integrating-factor-error"),("$e^x$","ede-integrating-factor-error"),("$y$","ede-integrating-factor-error")],0,"Multiply by $x$.","The ratio $(M_y-N_x)/N=1/x$ yields $\mu=e^{\int dx/x}=x$.",o[5]),
        select_all("q010","To verify $x^2y=C$ as an implicit solution of $2xy\,dx+x^2\,dy=0$, which checks are valid?",[("Differentiate to obtain $2xy+x^2y'=0$.",True,None),("Rewrite as $2xy\,dx+x^2\,dy=0$.",True,None),("Check the relation on an interval where any earlier multiplier assumptions hold.",True,None),("Assume exactness without comparing derivatives.",False,"ede-exactness-test-error")],"Implicit differentiation and interval checks verify the relation.","Differentiating the level curve reproduces the differential form.",o[4]),
        mc("q011","An equation is both linear and separable: $y'=-xy$, $y(0)=4$. Which approach is sound?",[("Either method is valid if $y=0$ is retained during separation and the IVP is checked.",None),("Only separation is allowed because methods cannot overlap.","ede-method-selection-error"),("Divide by $y$ and declare that no equilibrium exists.","ede-equilibrium-solution-lost"),("Use a Bernoulli substitution because the equation contains a product.","ede-bernoulli-substitution-error")],0,"Either linear or separable reasoning gives $y=4e^{-x^2/2}$.","Method classes can overlap; correctness depends on preserving solutions and checking the condition.",o[0],hard=True),
        mc("q012","For $xy'+y=x^2$, $y(2)=3$, which preparation and interval are correct?",[("Divide by $x$ to get $y'+y/x=x$ and work on $(0,\infty)$.",None),("Use all real $x$ because the original coefficients are polynomials.","ede-validity-interval-error"),("Treat $x=0$ as an ordinary point after division.","ede-linear-standard-form-error"),("Separate as $dy/y=x\,dx$.","ede-separation-error")],0,"Normalize on $(0,\infty)$, the maximal coefficient-continuity interval containing $2$.","Dividing by the leading coefficient exposes the singular point that controls the linear theorem and integrating factor.",o[0],hard=True),
    ]
    return [lesson(2, sections), glossary(2, gloss), worked(2, examples), recall(2, rec),
            quiz_or_test(2,"easy-quiz","Chapter 2: First Order Equations Easy Quiz","quiz",quiz),
            quiz_or_test(2,"test","Chapter 2: First Order Equations Test","test",test)]


def assessment_items(d: dict) -> list[tuple[str, str, str]]:
    """Return (item id, type, prompt) in learner order."""
    if d["assessmentType"] in {"quiz", "test"}:
        return [(q["id"], q["type"], q["prompt"]) for q in d["questions"]]
    if d["assessmentType"] == "conceptLesson":
        return [(s["check"]["id"], s["check"]["type"], s["check"]["prompt"]) for s in d["lesson"]["sections"]]
    if d["assessmentType"] == "workedExample":
        return [(s["id"], s["type"], s["prompt"]) for e in d["workedExamples"] for s in e["steps"]]
    if d["assessmentType"] == "recallDrill":
        return [(x["id"], x["type"], x["prompt"]) for x in d["items"]]
    return [(dr["id"], dr["type"], dr["prompt"]) for sec in d["glossary"]["sections"] for e in sec["entries"] for dr in e["drills"]]


def objective_for(ch: int, assessment_id: str, index: int) -> str:
    objectives = CHAPTERS[ch]["objectives"]
    if "worked-examples" in assessment_id:
        mapping = ([0, 2, 3] if ch == 1 else [0, 1, 4])
        return objectives[mapping[index // 3]]
    return objectives[index % len(objectives)]


def contracts(ch: int, assessments: list[dict]) -> None:
    cfg = CHAPTERS[ch]
    blueprint_records = []
    for d in assessments:
        items = assessment_items(d)
        for i, (iid, qtype, prompt) in enumerate(items):
            obj = objective_for(ch, d["id"], i)
            source_index = cfg["objectives"].index(obj)
            source_index = min(source_index, len(cfg["chunks"]) - 1)
            blueprint_records.append({
                "id": f"{d['id']}-{i+1:03d}", "objectiveId": obj, "assessmentId": d["id"],
                "questionId": iid, "questionType": qtype, "sourceChunks": [chunk(ch, source_index)],
                "reviewState": "approved", "givens": prompt,
                "unknown": "The specific classification, equation, value, solution, or justification requested in the prompt.",
                "representationRequirement": "Use the named diagram only when the prompt requires geometric or workflow interpretation.",
                "governingPrinciple": next(x["title"] for x in json.loads((REF / "curriculum-manifests" / "elementary-differential-equations-bvp.yaml").read_text(encoding="utf-8"))["objectives"][ch-1]["objectives"] if x["id"] == obj),
                "methodSteps": ["identify the equation structure or modeled quantity", "apply the governing relation without dropping conditions", "verify the result against the equation, data, and valid interval"],
                "misconception": "The item targets a concrete structure, condition, sign, domain, or method-selection error identified by its distractor signals or expected response.",
                "difficultyEvidence": "The learner must connect the stated representation and conditions to a checkable mathematical conclusion.",
                "verification": "Differentiate, substitute, check initial data and domain, compare cross partials, or recompute the requested value as applicable.",
                "variationAxes": ["equation structure", "requested representation", f"reasoning target {i+1}"],
                "reasoningSignature": f"{d['id']}::{iid}::{obj}::reasoning-{i+1}",
            })
    write_json(REF / "question-blueprints" / f"{cfg['topic']}-blueprints.json",
               {"schemaVersion": 1, "sourceId": SOURCE, "reviewState": "approved", "blueprints": blueprint_records})

    for d in assessments:
        objective_ids = sorted({objective_for(ch, d["id"], i) for i, _ in enumerate(assessment_items(d))}, key=cfg["objectives"].index)
        source_ids = sorted({chunk(ch, min(cfg["objectives"].index(o), len(cfg["chunks"])-1)) for o in objective_ids})
        write_json(REF / "content-manifests" / f"{d['id']}.json", {
            "schemaVersion": 1, "id": f"{d['id']}-manifest", "categoryId": CATEGORY,
            "topicId": cfg["topic"], "assessmentId": d["id"], "objectiveIds": objective_ids,
            "sourceId": SOURCE, "sourceChunkIds": source_ids, "reviewState": "approved",
        })

    activity_meta = [
        ("concept-lesson","conceptLesson","learn","conceptLesson",6),
        ("glossary","glossary","learn","glossary",16 if ch == 1 else 17),
        ("worked-examples","workedExample","learn","guidedWorkedExample",3),
        ("recall-drill","recallDrill","recall","mixedRecallSet",13 if ch == 1 else 16),
        ("easy-quiz","quiz","practice","focusedPractice",10),
        ("test","test","evaluate","formalTest",12),
    ]
    artifacts = []
    for suffix, atype, goal, activity, count in activity_meta:
        aid = f"{cfg['topic']}-{suffix}"
        manifest = json.loads((REF / "content-manifests" / f"{aid}.json").read_text(encoding="utf-8"))
        artifacts.append({"id": aid, "assessmentType": atype, "learningGoal": goal, "activityType": activity,
                          "objectiveIds": manifest["objectiveIds"], "plannedCount": count, "publicationStatus": "published"})
    write_json(REF / "assessment-release-manifests" / f"{cfg['topic']}.json", {
        "schemaVersion": 1, "id": f"{cfg['topic']}-assessment-release", "categoryId": CATEGORY,
        "topicId": cfg["topic"], "areaId": AREA, "packetId": cfg["packet"],
        "publicationStatus": "published", "sourceReviewState": "approved", "artifacts": artifacts,
    })


def svg_assets() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    assets = {
        "ch01-rate-model-flow.svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" role="img" aria-labelledby="t d"><title id="t">Rate-model construction workflow</title><desc id="d">A workflow connects the changing quantity and its units to accumulation, proportional change, and input-output balance models.</desc><rect width="900" height="300" rx="24" fill="#f8fafc"/><g font-family="Arial,sans-serif" text-anchor="middle"><rect x="35" y="95" width="190" height="110" rx="18" fill="#dbeafe" stroke="#1d4ed8" stroke-width="3"/><text x="130" y="133" font-size="20" font-weight="700">Define the state</text><text x="130" y="163" font-size="17">Q(t) and units</text><path d="M225 150h75" stroke="#334155" stroke-width="4" marker-end="url(#a)"/><rect x="300" y="60" width="260" height="180" rx="18" fill="#ecfeff" stroke="#0f766e" stroke-width="3"/><text x="430" y="98" font-size="20" font-weight="700">Identify the rate rule</text><text x="430" y="133" font-size="17">accumulation: Qâ€² = r(t)</text><text x="430" y="165" font-size="17">proportional: Qâ€² = kQ</text><text x="430" y="197" font-size="17">balance: Qâ€² = in âˆ’ out</text><path d="M560 150h75" stroke="#334155" stroke-width="4" marker-end="url(#a)"/><rect x="635" y="95" width="230" height="110" rx="18" fill="#fef3c7" stroke="#b45309" stroke-width="3"/><text x="750" y="133" font-size="20" font-weight="700">Check the model</text><text x="750" y="163" font-size="17">units and signs agree</text></g><defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0L9 3L0 6z" fill="#334155"/></marker></defs></svg>''',
        "ch01-direction-field.svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="430" viewBox="0 0 1050 430" role="img" aria-labelledby="t d"><title id="t">Direction field and integral curves</title><desc id="d">Direction field for y prime equals y times one minus y, with equilibrium lines at zero and one, positive slopes between them, negative slopes above one, and representative integral curves.</desc><rect width="1050" height="430" fill="#f8fafc"/><g transform="translate(90 35)"><path d="M0 320H730M0 0V360" stroke="#334155" stroke-width="3"/><g stroke="#94a3b8" stroke-width="2"><path d="M20 295l24 0m46 0h24m46 0h24m46 0h24m46 0h24m46 0h24m46 0h24m46 0h24m46 0h24"/><path d="M20 210l22 -10m48 10l22 -10m48 10l22 -10m48 10l22 -10m48 10l22 -10m48 10l22 -10m48 10l22 -10m48 10l22 -10"/><path d="M20 125l24 0m46 0h24m46 0h24m46 0h24m46 0h24m46 0h24m46 0h24m46 0h24"/><path d="M20 45l22 12m48 -12l22 12m48 -12l22 12m48 -12l22 12m48 -12l22 12m48 -12l22 12m48 -12l22 12m48 -12l22 12"/></g><path d="M0 295H730" stroke="#0f766e" stroke-width="5"/><path d="M0 125H730" stroke="#0f766e" stroke-width="5"/><path d="M0 260C150 250 230 190 360 155S580 130 730 127" fill="none" stroke="#2563eb" stroke-width="5"/><path d="M0 70C170 92 260 112 390 120S620 125 730 125" fill="none" stroke="#dc2626" stroke-width="5"/><text x="745" y="302" font-family="Arial" font-size="18">y=0 equilibrium</text><text x="745" y="132" font-family="Arial" font-size="18">y=1 equilibrium</text><text x="390" y="188" font-family="Arial" font-size="18" fill="#2563eb">increasing</text><text x="390" y="80" font-family="Arial" font-size="18" fill="#dc2626">decreasing</text><text x="710" y="350" font-family="Arial" font-size="20">x</text><text x="-35" y="20" font-family="Arial" font-size="20">y</text></g></svg>''',
        "ch02-method-map.svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="470" viewBox="0 0 1000 470" role="img" aria-labelledby="t d"><title id="t">First-order differential-equation method map</title><desc id="d">A decision map checks linear, separable, exact, Bernoulli, homogeneous, and supported integrating-factor structures before solving and verifying.</desc><rect width="1000" height="470" rx="24" fill="#f8fafc"/><g font-family="Arial,sans-serif" text-anchor="middle"><rect x="350" y="25" width="300" height="58" rx="15" fill="#dbeafe" stroke="#1d4ed8" stroke-width="3"/><text x="500" y="61" font-size="21" font-weight="700">Normalize the first-order ODE</text><path d="M500 83v38" stroke="#334155" stroke-width="4"/><g font-size="18"><rect x="35" y="122" width="175" height="78" rx="14" fill="#ecfeff" stroke="#0f766e" stroke-width="3"/><text x="122" y="153">linear?</text><text x="122" y="179">yâ€²+py=q</text><rect x="225" y="122" width="175" height="78" rx="14" fill="#ecfeff" stroke="#0f766e" stroke-width="3"/><text x="312" y="153">separable?</text><text x="312" y="179">g(y)dy=f(x)dx</text><rect x="415" y="122" width="175" height="78" rx="14" fill="#ecfeff" stroke="#0f766e" stroke-width="3"/><text x="502" y="153">exact?</text><text x="502" y="179">Máµ§=Nâ‚“</text><rect x="605" y="122" width="175" height="78" rx="14" fill="#ecfeff" stroke="#0f766e" stroke-width="3"/><text x="692" y="153">Bernoulli?</text><text x="692" y="179">v=yÂ¹â»â¿</text><rect x="795" y="122" width="170" height="78" rx="14" fill="#ecfeff" stroke="#0f766e" stroke-width="3"/><text x="880" y="153">homogeneous?</text><text x="880" y="179">v=y/x</text></g><path d="M500 200v55" stroke="#334155" stroke-width="4" marker-end="url(#a)"/><rect x="245" y="255" width="510" height="72" rx="15" fill="#fef3c7" stroke="#b45309" stroke-width="3"/><text x="500" y="285" font-size="20" font-weight="700">If nonexact, test only the supported</text><text x="500" y="312" font-size="18">one-variable integrating-factor ratios</text><path d="M500 327v45" stroke="#334155" stroke-width="4" marker-end="url(#a)"/><rect x="290" y="372" width="420" height="62" rx="15" fill="#dcfce7" stroke="#15803d" stroke-width="3"/><text x="500" y="397" font-size="20" font-weight="700">Solve â†’ apply data â†’ verify</text><text x="500" y="422" font-size="17">including equilibria and valid interval</text></g><defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0L9 3L0 6z" fill="#334155"/></marker></defs></svg>''',
        "ch02-exactness-potential-workflow.svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="300" viewBox="0 0 960 300" role="img" aria-labelledby="t d"><title id="t">Exactness and potential-function workflow</title><desc id="d">Four boxes show comparing M sub y and N sub x, integrating M with respect to x plus g of y, matching the y derivative to N, and verifying both partial derivatives.</desc><rect width="960" height="300" rx="24" fill="#f8fafc"/><g font-family="Arial,sans-serif" text-anchor="middle"><g fill="#e0f2fe" stroke="#0369a1" stroke-width="3"><rect x="25" y="80" width="195" height="130" rx="16"/><rect x="265" y="80" width="195" height="130" rx="16"/><rect x="505" y="80" width="195" height="130" rx="16"/><rect x="745" y="80" width="190" height="130" rx="16"/></g><g font-size="18"><text x="122" y="119" font-weight="700">1. Test</text><text x="122" y="153">Máµ§ = Nâ‚“</text><text x="362" y="119" font-weight="700">2. Integrate M</text><text x="362" y="153">Î¦ = âˆ«M dx + g(y)</text><text x="602" y="119" font-weight="700">3. Match N</text><text x="602" y="153">Î¦áµ§ = N â†’ find gâ€²</text><text x="840" y="119" font-weight="700">4. Verify</text><text x="840" y="153">Î¦â‚“=M and Î¦áµ§=N</text><text x="840" y="182">then Î¦=C</text></g><g stroke="#334155" stroke-width="4"><path d="M220 145h45"/><path d="M460 145h45"/><path d="M700 145h45"/></g></g></svg>''',
    }
    for name, content in assets.items():
        (MEDIA / name).write_text(content + "\n", encoding="utf-8")


def main() -> None:
    all_assessments = {1: chapter1(), 2: chapter2()}
    for ch, docs in all_assessments.items():
        for d in docs:
            write_assessment(ASSESS / f"{d['id']}.yaml", d)
        contracts(ch, docs)
    svg_assets()


if __name__ == "__main__":
    main()


"""Generate the targeted EDE Chapters 3-4 refresh without replacing sound banks."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

import generate_ede_ch01_ch02_refresh as common


ROOT = Path(__file__).resolve().parents[1]
ASSESS = ROOT / "data" / "assessments"
REF = ROOT / "docs" / "assessment-reference"
MEDIA = ROOT / "frontend" / "public" / "media" / "ede"
SOURCE = common.SOURCE
CATEGORY = common.CATEGORY
AREA = "ede-numerical-first-order-applications"


CONFIG = {
    3: {
        "topic": "ede-ch03-numerical-methods",
        "label": "Chapter 3: Numerical Methods",
        "packet": "packet-ede-ch03-numerical-methods-v1",
        "chunks": ["0133", "0143", "0158", "0176", "0180"],
        "objectives": [
            "ede-ch03-numerical-methods-euler-updates",
            "ede-ch03-numerical-methods-error-step-size",
            "ede-ch03-numerical-methods-improved-euler",
            "ede-ch03-numerical-methods-runge-kutta",
            "ede-ch03-numerical-methods-method-comparison",
        ],
        "glossaryCount": 15,
        "recallCount": 12,
    },
    4: {
        "topic": "ede-ch04-first-order-applications",
        "label": "Chapter 4: Applications of First Order Equations",
        "packet": "packet-ede-ch04-first-order-applications-v1",
        "chunks": ["0193", "0210", "0223", "0240", "0262"],
        "objectives": [
            "ede-ch04-first-order-applications-growth-decay",
            "ede-ch04-first-order-applications-cooling-mixing",
            "ede-ch04-first-order-applications-mechanics",
            "ede-ch04-first-order-applications-autonomous-phase",
            "ede-ch04-first-order-applications-curves",
        ],
        "glossaryCount": 18,
        "recallCount": 12,
    },
}

common.CHAPTERS.update(CONFIG)

WHY_BY_OBJECTIVE = {
    "ede-ch03-numerical-methods-euler-updates": "Euler advances from the known current mesh state by multiplying its right-hand-side slope by the step size.",
    "ede-ch03-numerical-methods-error-step-size": "The claim compares an approximation and reference at the same point while distinguishing one-step error from accumulated error.",
    "ede-ch03-numerical-methods-improved-euler": "The corrected update uses a predictor or midpoint stage to represent how the slope changes across the step.",
    "ede-ch03-numerical-methods-runge-kutta": "RK4 evaluates four prescribed stage states and combines their slopes with weights $1,2,2,1$.",
    "ede-ch03-numerical-methods-method-comparison": "A fair method comparison fixes the IVP and endpoint, then considers both reference error and right-hand-side evaluation cost.",
    "ede-ch04-first-order-applications-growth-decay": "A proportional-rate model produces an exponential transient whose sign, initial value, and limiting behavior determine the interpretation.",
    "ede-ch04-first-order-applications-cooling-mixing": "The model follows a signed balance: ambient temperature defines the cooling equilibrium, while flow times concentration defines each solute rate.",
    "ede-ch04-first-order-applications-mechanics": "Newton's law uses a declared positive direction, includes the mass factor, and makes resistance oppose velocity.",
    "ede-ch04-first-order-applications-autonomous-phase": "The sign of the autonomous rate between its zeros determines phase-line direction and stability.",
    "ede-ch04-first-order-applications-curves": "Eliminating the family parameter gives its slope field, and perpendicular trajectories use the negative reciprocal slope.",
}

OTHER_CHOICES_BY_OBJECTIVE = {
    "ede-ch03-numerical-methods-euler-updates": "The distractors use a future or unrelated state, omit the step-size update, or substitute information Euler does not require.",
    "ede-ch03-numerical-methods-error-step-size": "The distractors confuse a slope or initial datum with error, compare unlike endpoints, or reverse the refinement evidence.",
    "ede-ch03-numerical-methods-improved-euler": "The distractors omit the predictor/correction stage or evaluate the correcting slope at the wrong state.",
    "ede-ch03-numerical-methods-runge-kutta": "The distractors misplace a stage, discard a slope, or replace the $1,2,2,1$ weighted combination.",
    "ede-ch03-numerical-methods-method-comparison": "The distractors compare unlike tasks or ignore either endpoint accuracy or the number of slope evaluations.",
    "ede-ch04-first-order-applications-growth-decay": "The distractors reverse the rate sign, confuse equilibrium with initial data, or violate the exponential model's limit.",
    "ede-ch04-first-order-applications-cooling-mixing": "The distractors omit the ambient shift, misuse amount as concentration, freeze a changing volume, or reverse a balance sign.",
    "ede-ch04-first-order-applications-mechanics": "The distractors omit mass, reverse resistance, or impose a condition unrelated to zero acceleration.",
    "ede-ch04-first-order-applications-autonomous-phase": "The distractors classify a zero without checking neighboring signs or reverse the phase-line arrows.",
    "ede-ch04-first-order-applications-curves": "The distractors retain the original slope or use a sign change/reciprocal that is not the negative reciprocal.",
}


def load(assessment_id: str) -> dict:
    return yaml.safe_load((ASSESS / f"{assessment_id}.yaml").read_text(encoding="utf-8"))


def transfer(question: dict, prerequisite: str, extension: str) -> dict:
    dims = question.setdefault("difficultyDimensions", [])
    for dim in ["modelOrDerivation", "constraintTracking", "representationTransfer"]:
        if dim not in dims:
            dims.append(dim)
    question["prerequisiteObjectiveIds"] = [prerequisite]
    question["extensionObjectiveIds"] = [extension]
    return question


def enrich_retained(ch: int, suffix: str, objective_map: list[int], signal_map: list[str]) -> dict:
    cfg = CONFIG[ch]
    d = load(f"{cfg['topic']}-{suffix}")
    if suffix == "glossary":
        for section in d["glossary"]["sections"]:
            for entry in section["entries"]:
                for drill in entry.get("drills", []):
                    drill["explanation"] = (
                        f"Solution: {entry['term']}\n\nWhy it works: {entry['definition']}"
                    )
        d["navigation"]["tags"] = [CATEGORY, cfg["topic"], "s2c-approved"]
        return d
    items = d["items"] if suffix == "recall-drill" else d["questions"]
    for i, item in enumerate(items):
        obj = cfg["objectives"][objective_map[i]]
        item["skills"] = [obj]
        item["subjectDifficultyTags"] = [obj] if suffix != "recall-drill" else item.get("subjectDifficultyTags", [])
        if suffix == "easy-quiz":
            item["difficultyDimensions"] = item.get("difficultyDimensions", ["modelOrDerivation", "errorDiagnosis"])
            if len(item["difficultyDimensions"]) < 2:
                item["difficultyDimensions"].append("errorDiagnosis")
            item["difficultyEvidence"] = "Requires applying the named method or model and checking a distinct state, condition, or interpretation."
        if item.get("type") in {"multipleChoice", "selectAll"}:
            correct = {item["answer"].get("choiceId")} | set(item["answer"].get("choiceIds", []))
            for choice in item.get("choices", []):
                if choice["id"] not in correct:
                    choice["issueSignals"] = common.sig(signal_map[i])
        explanation = item.get("explanation", "")
        solution = explanation.partition("\n\nWhy it works:")[0]
        if not solution.startswith("Solution:"):
            answer = item.get("answer", {}).get("expected", "the stated relationship")
            solution = f"Solution: {answer}"
        item["explanation"] = f"{solution}\n\nWhy it works: {WHY_BY_OBJECTIVE[obj]}"
        if item.get("type") in {"multipleChoice", "selectAll"}:
            item["explanation"] += f"\n\nWhy the other choices fail: {OTHER_CHOICES_BY_OBJECTIVE[obj]}"
    d["navigation"]["tags"] = [CATEGORY, cfg["topic"], "s2c-approved"]
    return d


def chapter3() -> list[dict]:
    o = CONFIG[3]["objectives"]
    euler_media = [{"type": "image", "src": "/media/ede/ch03-euler-steps.svg",
                    "alt": "Euler polygon following current tangent slopes beneath a curved reference solution.",
                    "caption": "Euler advances from the current state along one local tangent."}]
    error_media = [{"type": "image", "src": "/media/ede/ch03-error-method-comparison.svg",
                    "alt": "Reference curve with coarse and fine Euler polygons, a marked local error, endpoint global errors, and a cost-accuracy comparison for Euler, Heun, and RK4.",
                    "caption": "Step size changes both accumulated error and computational cost."}]
    sections = [
        {"introduction": "Numerical methods replace an unavailable or inconvenient exact solution by a sequence of computed states. Every update must use the correct mesh point, step size, and slope data, and every accuracy claim needs a fair reference.",
         "title": "Why approximate?", "content": "For an IVP $y'=f(x,y)$, $y(x_0)=y_0$, a numerical method constructs values $y_n\\approx y(x_n)$ on mesh points $x_n=x_0+nh$. This is useful when no elementary closed form exists, when only sampled output is needed, or when a model is coupled to data. The method still requires $f$ to be evaluable at every stage.",
         "check": common.mc("chk-01", "A solver has reached $(x_n,y_n)=(0.4,1.7)$ for $y'=x-y$. What information is needed before any one-step method can advance?", [("A step size and the method's required evaluations of $f$",None),("Only the original value $y_0$","ede-numerical-current-state-error"),("An assumed exact solution","ede-numerical-reference-error"),("A new differential equation","ede-method-selection-error")],0,"The method needs $h$ and its prescribed slope evaluations.","A one-step rule advances from the current numerical state using the given right-hand side.",o[0])},
        {"title": "Euler updates", "content": "Euler's method uses the current slope only: $y_{n+1}=y_n+h f(x_n,y_n)$. Geometrically it follows the tangent line at $(x_n,y_n)$ for a horizontal distance $h$. For $y'=x-y$ at $(0,2)$ with $h=0.25$, the slope is $-2$ and the next value is $1.5$.", "media": euler_media,
         "check": common.numeric("chk-02", "Use one Euler step for $y'=2x+y$ from $(x_0,y_0)=(1,3)$ with $h=0.2$. Find $y_1$.",4.0,0.0001,"$f(1,3)=5$, so $y_1=3+0.2(5)=4$.","Euler evaluates the slope at the current point, not at the unknown next state.",o[0])},
        {"title": "Local error, global error, and step size", "content": "Local truncation error compares one update started from the exact current value with the exact value one step later. Global error compares the accumulated numerical value $y_n$ with $y(x_n)$ after many steps. Euler has local error of order $h^2$ and, over a fixed interval under standard smoothness assumptions, global error of order $h$. Halving $h$ usually reduces Euler's global error by about a factor of two, not four.", "media": error_media,
         "check": common.mc("chk-03", "Euler errors at a fixed endpoint are $0.048$ for $h=0.2$ and $0.025$ for $h=0.1$. Which conclusion is justified?", [("The behavior is consistent with approximately first-order global convergence.",None),("The local error is exactly $0.025$.","ede-numerical-local-global-error"),("Halving $h$ made the method exact.","ede-numerical-step-size-error"),("The larger-step result must be more accurate.","ede-numerical-step-size-error")],0,"The endpoint error is roughly halved when the step is halved.","That pattern is consistent with Euler's first-order global error, while two data points do not prove exactness.",o[1])},
        {"title": "Improved Euler and midpoint corrections", "content": "Heun's improved Euler method predicts $y^*=y_n+h f(x_n,y_n)$, evaluates the endpoint slope $f(x_n+h,y^*)$, and averages the two slopes. The explicit midpoint method instead predicts a half-step state and uses its slope for the full update. Both are second-order methods, but their stage locations are different.",
         "check": common.numeric("chk-04", "For $y'=x+y$, $(x_0,y_0)=(0,1)$, and $h=0.4$, Heun predicts $y^*=1.4$. What corrected value results?",1.56,0.0001,"The slopes are $1$ and $f(0.4,1.4)=1.8$, so $y_1=1+0.4(1+1.8)/2=1.56$.","Heun averages the starting slope and the predicted endpoint slope.",o[2])},
        {"title": "Classical fourth-order Runge–Kutta", "content": "RK4 samples four slopes: $k_1=f(x_n,y_n)$, two midpoint slopes $k_2$ and $k_3$, and the endpoint slope $k_4$. The update is $y_{n+1}=y_n+\\frac h6(k_1+2k_2+2k_3+k_4)$. The stage states, not merely the stage locations, must be updated before each evaluation.",
         "check": common.mc("chk-05", "In classical RK4, where is $k_3$ evaluated?", [("At the midpoint using the state predicted from $k_2$",None),("At the initial point again","ede-rk4-stage-location-error"),("At the endpoint using $k_1$","ede-rk4-stage-location-error"),("At the midpoint using the unchanged value $y_n$","ede-rk4-stage-location-error")],0,"$k_3=f(x_n+h/2,y_n+hk_2/2)$.","The second midpoint stage uses the state generated by the preceding midpoint slope.",o[3])},
        {"title": "Choosing a method fairly", "content": "Accuracy must be compared at the same endpoint against the same reference solution or sufficiently accurate benchmark. Cost should report right-hand-side evaluations, not just step count: Euler uses one per step, Heun typically two, and RK4 four. Smaller steps improve resolution but increase cost and can magnify roundoff in extreme cases.", "media": error_media,
         "check": common.select_all("chk-06", "Select every fair comparison between Euler and RK4 on the same IVP.", [("Compare endpoint errors against the same reference value.",True,None),("Report total evaluations of $f$.",True,None),("Give RK4 a smaller interval and compare raw errors.",False,"ede-numerical-cost-comparison-error"),("Compare only the number of time steps and ignore stages.",False,"ede-numerical-cost-comparison-error")],"Use a common endpoint/reference and report function-evaluation cost.","Both accuracy and computational work must be measured on comparable tasks.",o[4])},
    ]
    examples = [
        {"title":"Euler: a rising concentration","problem":"For $y'=x+y$, $y(0)=1$, use Euler with $h=0.2$ to estimate $y(0.4)$.","steps":[
            ("First current-state update","Evaluate the slope at the initial mesh point and advance exactly one step.","Compute $f(x_0,y_0)$ and $y_1$.","At $(0,1)$, $f=1$, so $y_1=1+0.2(1)=1.2$.",["slope 1","y1=1.2"],"Euler uses the known current state $(0,1)$ for the first tangent prediction."),
            ("Second current-state update","Use the newly computed state rather than reusing the initial slope.","Compute $f(x_1,y_1)$ and $y_2$.","At $(0.2,1.2)$, $f=1.4$, so $y_2=1.2+0.2(1.4)=1.48$.",["slope 1.4","y2=1.48"],"The recurrence advances both coordinates before the next slope evaluation."),
            ("Report and audit the table","Check that the mesh point and number of steps match the requested endpoint.","State the estimate and verify the update table reaches $x=0.4$.","The two steps reach $x_2=0.4$, so $y(0.4)\\approx1.48$. Each slope was evaluated at its current row.",["x2=0.4","estimate 1.48","current-row slopes"],"A correct numerical value is meaningful only when it corresponds to the requested mesh point.")]},
        {"title":"Improved Euler: average slopes","problem":"For $y'=x+y$, $y(0)=1$, take one improved-Euler step with $h=0.2$.","steps":[
            ("Predict the endpoint state","Use the initial slope for an Euler predictor only.","Compute the predictor $y^*$.","$f(0,1)=1$, so $y^*=1+0.2(1)=1.2$.",["initial slope","predictor 1.2"],"Heun needs a provisional endpoint state before it can evaluate the endpoint slope."),
            ("Average the endpoint slopes","Evaluate the slope at the predicted endpoint and apply the trapezoidal average.","Compute the corrected value $y_1$.","$f(0.2,1.2)=1.4$, so $y_1=1+\\frac{0.2}{2}(1+1.4)=1.24$.",["endpoint slope 1.4","corrected 1.24"],"The average accounts for the slope change across the step."),
            ("Compare the methods","Explain the numerical difference without claiming proof of accuracy.","Compare the Euler and Heun one-step values.","Euler gives $1.20$ while Heun gives $1.24$. Because the slope grows over the step, the endpoint correction raises the estimate.",["Euler 1.20","Heun 1.24","slope-growth explanation"],"A method comparison should connect the changed stage information to the changed estimate.")]},
        {"title":"RK4: a four-slope step","problem":"For $y'=y$, $y(0)=1$, use RK4 with $h=0.1$ for one step.","steps":[
            ("Compute the four stages","Use the correct midpoint and endpoint stage states.","Calculate $k_1,k_2,k_3,k_4$.","$k_1=1$, $k_2=1.05$, $k_3=1.0525$, and $k_4=1.10525$.",["four correct stages","midpoint states"],"Each later slope is evaluated at the state predicted by the preceding stage."),
            ("Apply the RK4 weights","Combine the stages using weights $1,2,2,1$.","Compute $y_1$.","$y_1=1+\\frac{0.1}{6}(1+2(1.05)+2(1.0525)+1.10525)=1.105170833\\ldots$.",["correct weights","value 1.105170833"],"The RK4 weighted average is multiplied by the full step size."),
            ("Compare with a reference","Evaluate the exact solution only as an accuracy reference.","Compare the RK4 value with $e^{0.1}$.","$e^{0.1}\\approx1.105170186$, so the absolute one-step error is about $6.47\\times10^{-7}$.",["reference value","error about 6.47e-7"],"The exact solution verifies the scale of the error without changing the RK4 calculation.")]},
    ]
    glossary = enrich_retained(3,"glossary",[],[])
    recall = enrich_retained(3,"recall-drill",[0,0,1,2,2,1,3,3,3,4,0,4],["ede-method-selection-error"]*12)
    quiz = enrich_retained(3,"easy-quiz",[0,0,0,1,2,1,3,0,4,4],["ede-euler-update-error","ede-numerical-current-state-error","ede-euler-update-error","ede-numerical-local-global-error","ede-improved-euler-stage-error","ede-numerical-step-size-error","ede-rk4-weighting-error","ede-euler-update-error","ede-numerical-reference-error","ede-numerical-cost-comparison-error"])
    test = [
        common.numeric("q001","Use Euler for $y'=x-y$, $y(0)=1$, with $h=0.25$. After two steps, what is $y_2$?",0.625,0.0001,"$y_1=1+0.25(-1)=0.75$; then $f(0.25,0.75)=-0.5$ and $y_2=0.75-0.125=0.625$.","Each update uses the new mesh point and state.",o[0],hard=True),
        common.numeric("q002","From $(x_n,y_n)=(1,2)$, take one Euler step of size $0.1$ for $y'=x^2+y$. Find $y_{n+1}$.",2.3,0.0001,"$f(1,2)=3$, so $y_{n+1}=2+0.1(3)=2.3$.","The nonautonomous slope uses both coordinates of the current state.",o[0]),
        common.select_all("q003","Select every correct distinction between local truncation error and global error.",[("Local error analyzes one step begun from exact data.",True,None),("Global error includes accumulated effects at a mesh point.",True,None),("Local and global error are always numerically equal.",False,"ede-numerical-local-global-error"),("Global error can be assessed without identifying the endpoint.",False,"ede-numerical-local-global-error")],"The first two statements are correct.","The two errors differ in starting state and accumulation across steps.",o[1]),
        common.numeric("q004","Euler endpoint errors are $0.080$ for $h=0.2$ and $0.040$ for $h=0.1$. What is the ratio of the larger error to the smaller?",2,0.0001,"$0.080/0.040=2$.","A factor near two under step halving is consistent with first-order global convergence.",o[1]),
        common.numeric("q005","For $y'=x+y$, $y(0)=0$, take one Heun step with $h=0.5$. Find the corrected value.",0.125,0.0001,"$k_1=0$, the predictor is $0$, and $k_2=f(0.5,0)=0.5$; hence $y_1=0+0.25(0+0.5)=0.125$.","Heun averages the starting and predicted endpoint slopes.",o[2]),
        common.numeric("q006","Use the explicit midpoint method for $y'=x-y$, $y(0)=2$, with $h=0.2$. Find $y_1$.",1.66,0.0001,"The midpoint state is $2+0.1(-2)=1.8$ at $x=0.1$; its slope is $-1.7$, so $y_1=2+0.2(-1.7)=1.66$.","The midpoint slope, not an endpoint predictor slope, controls the full update.",o[2]),
        common.numeric("q007","For one RK4 step on $y'=x+y$ from $(0,1)$ with $h=0.2$, $k_1=1$, $k_2=1.2$, and $k_3=1.22$. Find $k_4$.",1.444,0.0001,"$k_4=f(0.2,1+0.2(1.22))=f(0.2,1.244)=1.444$.","The endpoint stage uses the state generated from $k_3$.",o[3]),
        common.numeric("q008","An RK4 step has $y_n=2$, $h=0.2$, and slopes $k_1=2$, $k_2=2.2$, $k_3=2.22$, $k_4=2.444$. Find $y_{n+1}$.",2.4428,0.0001,"$y_{n+1}=2+\\frac{0.2}{6}(2+4.4+4.44+2.444)=2.4428$.","RK4 uses the weighted slope sum $1,2,2,1$.",o[3]),
        common.mc("q009","At $x=1$, a reference value is $2.71828$. Method A gives $2.70$ using 10 evaluations; Method B gives $2.719$ using 40 evaluations. Which statement is defensible?",[("Method B is more accurate here, while Method A is cheaper by the stated cost measure.",None),("Method B is always preferable for every tolerance.","ede-numerical-cost-comparison-error"),("Method A is more accurate because it uses fewer evaluations.","ede-numerical-reference-error"),("No comparison is possible even though a common reference is supplied.","ede-numerical-reference-error")],0,"Method B has smaller endpoint error, while Method A uses fewer evaluations.","Accuracy and cost are separate quantities and both were measured on the same target.",o[4]),
        common.select_all("q010","Two solvers reach the same endpoint. Select all information needed for a fair cost-accuracy comparison.",[("A common reference or error estimate",True,None),("The total number of right-hand-side evaluations",True,None),("The same requested endpoint and IVP",True,None),("Only the method names",False,"ede-numerical-cost-comparison-error")],"Use the same task, a common accuracy measure, and comparable computational cost.","Raw step counts are insufficient when methods use different numbers of stages.",o[4],hard=True),
        common.mc("q011","A forecast is computed with Euler at $h=0.2$ and $h=0.1$. What is the most defensible use of the two results?",[("Compare their endpoint difference as convergence evidence, without treating it as proof of the exact error.",None),("Declare the fine result exact.","ede-numerical-reference-error"),("Use the coarse result because it has fewer rows.","ede-numerical-step-size-error"),("Subtract the step sizes instead of the approximations.","ede-numerical-local-global-error")],0,"The difference is evidence about step-size sensitivity, not an exact-error certificate.","Without an exact reference or rigorous estimate, refinement supports but does not prove accuracy.",o[4],hard=True),
        common.mc("q012","An RK4 program evaluates four stage slopes per step. What comparison reports computational cost honestly?",[("Compare total evaluations of $f$ together with endpoint error.",None),("Compare only the number of time steps.","ede-numerical-cost-comparison-error"),("Count RK4 as one evaluation per step.","ede-rk4-stage-location-error"),("Ignore accuracy whenever costs differ.","ede-numerical-cost-comparison-error")],0,"Report function evaluations and error on the same task.","Each RK4 step contains four right-hand-side evaluations, so step count alone understates its work.",o[4],hard=True),
    ]
    for q in test:
        if len(q.get("difficultyDimensions", [])) >= 3:
            q["prerequisiteObjectiveIds"] = ["ede-ch02-first-order-equations-linear-ivps"]
            q["extensionObjectiveIds"] = ["ede-ch04-first-order-applications-growth-decay"]
    return [common.lesson(3,sections),glossary,common.worked(3,examples),recall,quiz,
            common.quiz_or_test(3,"test","Chapter 3: Numerical Methods Test","test",test)]


def chapter4() -> list[dict]:
    o = CONFIG[4]["objectives"]
    flow_media = [{"type":"image","src":"/media/ede/ch04-model-flow.svg","alt":"Workflow from physical situation through variables, rate law, initial data, and interpretation.","caption":"Model assumptions and units are checked before and after solving."}]
    phase_media = [{"type":"image","src":"/media/ede/ch04-phase-line-trajectory-map.svg","alt":"Stable and unstable phase-line equilibria paired with solution curves, plus perpendicular tangent directions for orthogonal trajectories.","caption":"Signs control autonomous motion; negative reciprocal slopes control orthogonality."}]
    sections = [
        {"introduction":"Applications begin with a state variable and a rate balance, not a memorized formula. This lesson builds and checks growth, cooling, mixing, resistance, autonomous, and curve-family models.",
         "title":"Growth, decay, input, and limiting values","content":"Pure proportional change satisfies $Q'=kQ$ and gives $Q=Q_0e^{kt}$. A constant input with proportional removal gives $Q'=a-kQ$ and equilibrium $Q_*=a/k$. The solution $Q=Q_*+(Q_0-Q_*)e^{-kt}$ shows directly whether the state rises or falls toward its limiting value.","media":flow_media,
         "check":common.symbolic("chk-01","Solve $Q'=12-0.3Q$ with $Q(0)=10$.","40-30e^{-0.3t}",["t"],"The equilibrium is $40$, so $Q=40+Ce^{-0.3t}$ and $C=-30$.","Differentiation verifies the rate law, the initial value is $10$, and the limiting value is $40$.",o[0])},
        {"title":"Newton cooling","content":"Newton's law uses the temperature difference from the ambient value: $T'=-k(T-T_a)$ for $k>0$. Thus $T=T_a+(T_0-T_a)e^{-kt}$. The sign automatically reverses when the object is colder than its surroundings, and a changed ambient temperature starts a new IVP at the switching time.",
         "check":common.mc("chk-02","A sample is at $10^\\circ$C in a $25^\\circ$C room and follows $T'=-0.2(T-25)$. What is true initially?",[("It warms because $T'(0)=3>0$.",None),("It cools because the leading sign is negative.","ede-cooling-ambient-shift-error"),("It remains constant because the room temperature is fixed.","ede-equilibrium-limiting-error"),("Its rate is $-3^\\circ$C per time unit.","ede-growth-decay-sign-error")],0,"The sample initially warms at $3^\\circ$C per time unit.","The temperature difference is negative, so the negative coefficient produces a positive derivative.",o[1])},
        {"title":"Well-mixed tanks","content":"For salt amount $Q(t)$, use $Q'=\\text{mass rate in}-\\text{mass rate out}$. Each mass rate is volumetric flow times concentration. The tank concentration is $Q/V(t)$ only under the well-mixed assumption, and $V(t)$ must change when inflow and outflow differ.",
         "check":common.mc("chk-03","A tank has volume $V(t)$, salt amount $Q(t)$, and outflow $r$ L/min. Which salt-out term is correct?",[("$rQ/V(t)$",None),("$rV(t)/Q$","ede-mixing-concentration-error"),("$Q/r$","ede-model-rate-unit-error"),("$rQ$","ede-mixing-concentration-error")],0,"The salt-out rate is $r[Q/V(t)]$.","Flow times the well-mixed concentration has mass-per-time units.",o[1])},
        {"title":"Mechanics with linear resistance","content":"Choose a positive direction before writing Newton's law. With downward positive, a falling mass with linear resistance satisfies $mv'=mg-bv$ because resistance opposes positive downward velocity. Terminal velocity occurs when acceleration vanishes, giving $v_T=mg/b$ in this convention.",
         "check":common.numeric("chk-04","A $3$-kg object falls downward with resistance coefficient $b=1.5$ kg/s and $g=9.8$ m/s². What is its terminal speed in m/s?",19.6,0.0001,"$v_T=mg/b=3(9.8)/1.5=19.6$ m/s.","At terminal speed the net force and acceleration are zero.",o[2])},
        {"title":"Autonomous equations and phase lines","content":"An autonomous first-order equation has the form $y'=f(y)$. Equilibria solve $f(y)=0$. A phase line records the sign of $f$ between equilibria: arrows pointing toward an equilibrium from both sides indicate stability; arrows pointing away indicate instability.","media":phase_media,
         "check":common.mc("chk-05","For $y'=y(1-y)$, how is $y=1$ classified?",[("Stable, because nearby arrows point toward $1$.",None),("Unstable, because $f(1)=0$.","ede-autonomous-stability-error"),("Not an equilibrium.","ede-equilibrium-limiting-error"),("Stable only for initial values above $1$.","ede-autonomous-stability-error")],0,"$y=1$ is stable.","The derivative is positive below $1$ and negative above $1$, so both sides move toward it.",o[3])},
        {"title":"Curve families and orthogonal trajectories","content":"Differentiate a one-parameter family and eliminate its parameter to obtain the differential equation of the family. If its slope is $m(x,y)$, an orthogonal trajectory has slope $-1/m(x,y)$ where $m\\ne0$. The perpendicular relation is local and must be integrated to obtain the new family.","media":phase_media,
         "check":common.mc("chk-06","The family $y=cx^2$ has slope $2y/x$. Which ODE describes its orthogonal trajectories?",[("$y'=-x/(2y)$",None),("$y'=2y/x$","ede-orthogonal-slope-error"),("$y'=-2y/x$","ede-orthogonal-slope-error"),("$y'=x/(2y)$","ede-orthogonal-slope-error")],0,"The orthogonal slope is the negative reciprocal, $-x/(2y)$.","Perpendicular nonvertical slopes have product $-1$.",o[4])},
    ]
    examples = [
        {"title":"Cooling a sensor","problem":"A sensor begins at $90^\\circ$C in a $20^\\circ$C room and follows $T'=-0.1(T-20)$. Find $T(t)$.","steps":[
            ("Shift by the ambient temperature","Define the temperature excess and translate the initial data.","Set $u=T-20$ and write its IVP.","$u'=T'=-0.1u$ and $u(0)=90-20=70$.",["u=T-20","u'=-0.1u","u(0)=70"],"The ambient shift converts the model into pure exponential decay."),
            ("Solve the shifted IVP","Apply the initial condition before shifting back.","Find $u(t)$ and then $T(t)$.","$u=70e^{-0.1t}$, so $T(t)=20+70e^{-0.1t}$.",["u solution","T solution"],"The initial excess is the multiplicative constant."),
            ("Verify and interpret","Check the initial value, rate law, and long-term limit.","Verify the solution and interpret its limit.","$T(0)=90$, $T'=-7e^{-0.1t}=-0.1(T-20)$, and $T(t)\\to20^\\circ$C.",["initial check","ODE check","limit 20"],"All mathematical checks agree with cooling toward the ambient temperature.")]},
        {"title":"A salt tank","problem":"A 100-L tank contains 10 kg salt. Pure water enters and leaves at 5 L/min. Set up and solve for salt amount $Q(t)$.","steps":[
            ("Construct the balance","Use the well-mixed concentration and verify units.","Compute the salt-in and salt-out rates.","Salt input is $0$; concentration is $Q/100$ kg/L, so salt output is $5(Q/100)=Q/20$ kg/min and $Q'=-Q/20$.",["input zero","output Q/20","balance equation"],"Volumetric flow times concentration produces the required mass-per-time rate."),
            ("Solve the IVP","Use the initial salt amount to determine the constant.","Solve $Q'=-Q/20$, $Q(0)=10$.","$Q(t)=Ce^{-t/20}$ and $Q(0)=10$ gives $Q(t)=10e^{-t/20}$ kg.",["exponential solution","constant 10","units kg"],"A constant-volume pure-water flush removes a fixed fraction of the current salt per minute."),
            ("Check physical behavior","Verify nonnegativity, the derivative, and the limit.","Audit the solution against the model.","$Q(t)>0$, $Q'=-\\frac12e^{-t/20}=-Q/20$, and $Q(t)\\to0$ as $t\\to\\infty$.",["nonnegative","ODE check","limit zero"],"The solution never predicts negative salt and approaches the physically expected empty-salt state.")]},
        {"title":"Orthogonal curves","problem":"Find the slope field for curves $y=cx^2$ and state the orthogonal-trajectory equation.","steps":[
            ("Eliminate the parameter","Differentiate the family and replace $c$ using the original relation.","Find the family slope in terms of $x$ and $y$.","Differentiating gives $y'=2cx$; since $c=y/x^2$, the slope is $y'=2y/x$ where $x\\ne0$.",["differentiate","eliminate c","slope 2y/x"],"A differential equation for the family cannot retain the arbitrary parameter."),
            ("Take the perpendicular slope","Use the negative reciprocal where the original slope is finite and nonzero.","Find the orthogonal slope.","$m_\\perp=-1/(2y/x)=-x/(2y)$.",["negative reciprocal","slope -x/(2y)"],"Perpendicular tangent slopes multiply to $-1$."),
            ("State and integrate the ODE","Separate the orthogonal equation to identify its family.","Give the orthogonal ODE and its integrated family.","The ODE is $y'=-x/(2y)$. Thus $2y\\,dy=-x\\,dx$, so $x^2+2y^2=C$.",["orthogonal ODE","separation","family x²+2y²=C"],"Integrating turns the local perpendicular slope condition into the full trajectory family.")]},
    ]
    glossary = enrich_retained(4,"glossary",[],[])
    recall = enrich_retained(4,"recall-drill",[0,0,1,1,1,2,2,3,3,3,4,4],["ede-method-selection-error"]*12)
    quiz = enrich_retained(4,"easy-quiz",[0,0,1,1,2,3,0,3,4,1],["ede-growth-decay-sign-error","ede-equilibrium-limiting-error","ede-cooling-ambient-shift-error","ede-mixing-concentration-error","ede-terminal-velocity-error","ede-autonomous-stability-error","ede-equilibrium-limiting-error","ede-autonomous-stability-error","ede-orthogonal-slope-error","ede-model-rate-unit-error"])
    test = [
        common.numeric("q001","A population obeys $P'=kP$ and doubles every $8$ years. Find $k$ in inverse years.",0.0866434,0.0001,"$2=e^{8k}$, so $k=\\ln2/8\\approx0.0866434$ yr$^{-1}$.","The doubling condition determines the proportional-rate constant independently of the initial population.",o[0],hard=True),
        common.numeric("q002","A radioactive tracer has half-life $6$ hours and begins with $80$ mg. How many milligrams remain after $15$ hours?",14.1421,0.001,"$Q=80(1/2)^{15/6}=80(1/2)^{2.5}\\approx14.1421$ mg.","The elapsed time is measured in half-life units.",o[0]),
        common.symbolic("q003","Solve $Q'=18-0.3Q$, $Q(0)=10$.","60-50e^{-0.3t}",["t"],"The equilibrium is $60$ and $Q=60+Ce^{-0.3t}$; $Q(0)=10$ gives $C=-50$.","The transient decays while the solution approaches the input-removal balance.",o[0]),
        common.symbolic("q004","At a reset time $t=0$, a sensor is $50^\\circ$C and is moved into a $10^\\circ$C room. If $T'=-0.2(T-10)$, find $T(t)$.","10+40e^{-0.2t}",["t"],"The initial excess is $40$, giving $T=10+40e^{-0.2t}$.","The new ambient temperature defines the shifted equilibrium for the reset IVP.",o[1]),
        common.mc("q005","A tank starts with 100 L. Brine enters at 5 L/min with concentration 2 g/L, and mixture leaves at 3 L/min. Which salt equation is correct?",[("$Q'=10-3Q/(100+2t)$",None),("$Q'=10-3Q/100$","ede-mixing-volume-error"),("$Q'=2-3Q/(100+2t)$","ede-mixing-concentration-error"),("$Q'=10+3Q/(100+2t)$","ede-mixing-balance-sign-error")],0,"$V(t)=100+2t$ and $Q'=5(2)-3Q/V(t)$.","Unequal flows change the volume, and output is flow times the current well-mixed concentration.",o[1],hard=True),
        common.numeric("q006","A 100-L tank contains 20 g of salt. Pure water enters and mixture leaves at 4 L/min. How many grams remain after 10 min?",13.4064,0.001,"$Q'=-(4/100)Q$, so $Q=20e^{-0.04t}$ and $Q(10)=20e^{-0.4}\\approx13.4064$ g.","The constant-volume outflow removes four percent of the current salt per minute.",o[1]),
        common.mc("q007","Take downward as positive for a falling $2$-kg object with linear resistance $0.5v$ and $g=9.8$. Which equation is correct?",[("$2v'=19.6-0.5v$",None),("$2v'=19.6+0.5v$","ede-resistance-direction-error"),("$v'=2(9.8)-0.5v$","ede-mechanics-mass-error"),("$2v'=-19.6-0.5v$","ede-growth-decay-sign-error")],0,"$2v'=mg-bv=19.6-0.5v$.","Resistance opposes positive downward velocity, while gravity acts in the chosen positive direction.",o[2]),
        common.numeric("q008","For the falling object governed by $2v'=19.6-0.5v$, find the terminal speed in m/s.",39.2,0.0001,"Set $v'=0$: $19.6-0.5v_T=0$, so $v_T=39.2$ m/s.","Terminal velocity is the equilibrium of the velocity equation.",o[2]),
        common.mc("q009","For $y'=y(y-1)(2-y)$, how is the equilibrium $y=1$ classified?",[("Unstable, because nearby arrows point away on both sides.",None),("Stable, because every zero of $f$ is stable.","ede-autonomous-stability-error"),("Semistable, because the factors are linear.","ede-autonomous-stability-error"),("Not an equilibrium.","ede-equilibrium-limiting-error")],0,"$y=1$ is unstable.","The rate is negative just below $1$ and positive just above it, so both sides move away.",o[3]),
        common.symbolic("q010","The family $y=cx^3$ has slope $3y/x$. Orthogonal trajectories satisfy $y'=-x/(3y)$. Enter the left side of their implicit family in the form $F(x,y)=C$.","x^2+3y^2",["x","y"],"$3y\\,dy=-x\\,dx$ gives $3y^2/2=-x^2/2+C$, hence $x^2+3y^2=C$.","The negative reciprocal slope is separated and integrated to obtain the perpendicular family.",o[4],hard=True),
        common.mc("q011","A tank model predicts a negative amount after a long simulation. What should be checked before accepting it?",[("Check the balance signs, volume domain, assumptions, and whether the solution was used beyond its valid interval.",None),("Accept it because differential equations may produce any sign.","ede-model-assumption-error"),("Delete the initial condition.","ede-condition-ignored"),("Reverse every rate term automatically.","ede-mixing-balance-sign-error")],0,"Audit the model, domain, and physical assumptions before accepting a negative amount.","A mass amount should remain nonnegative; a negative prediction signals a setup, domain, or applicability problem.",o[1],hard=True),
        common.mc("q012","A proposed orthogonal trajectory has the same nonzero slope as the given family at an intersection. What conclusion is justified?",[("It is not orthogonal there because the slopes should be negative reciprocals.",None),("It is orthogonal because the slopes agree.","ede-orthogonal-slope-error"),("Every intersection is automatically perpendicular.","ede-orthogonal-slope-error"),("Slope information cannot test orthogonality.","ede-method-selection-error")],0,"The proposed curve is not orthogonal at that intersection.","Equal nonzero slopes indicate tangency, whereas perpendicular slopes have product $-1$.",o[4],hard=True),
    ]
    for q in test:
        if len(q.get("difficultyDimensions", [])) >= 3:
            q["prerequisiteObjectiveIds"] = ["ede-ch02-first-order-equations-linear-ivps"]
            q["extensionObjectiveIds"] = ["ede-ch05-linear-second-order-equations-curriculum"]
    return [common.lesson(4,sections),glossary,common.worked(4,examples),recall,quiz,
            common.quiz_or_test(4,"test","Chapter 4: Applications of First Order Equations Test","test",test)]


def items(d: dict) -> list[tuple[str,str,str]]:
    return common.assessment_items(d)


def contracts(ch: int, docs: list[dict]) -> None:
    cfg=CONFIG[ch]
    curriculum=json.loads((REF/"curriculum-manifests"/"elementary-differential-equations-bvp.yaml").read_text(encoding="utf-8"))
    objective_titles={x["id"]:x["title"] for x in curriculum["objectives"][ch-1]["objectives"]}
    method_contracts = {
        "ede-ch03-numerical-methods-euler-updates": (["read the current mesh state and step size", "evaluate the slope only at the current state", "apply $y_{n+1}=y_n+h f(x_n,y_n)$ and advance the mesh point"], "evaluating Euler's slope at a future state or omitting the factor $h$", "recompute each slope and update from the listed mesh state"),
        "ede-ch03-numerical-methods-error-step-size": (["identify the reference value and the approximation being compared", "compute signed or absolute error at the same point", "relate the error change to the stated step refinement without confusing local and global error"], "confusing a one-step defect with accumulated endpoint error or comparing different endpoints", "subtract the approximation from the supplied exact/reference value and check the refinement ratio"),
        "ede-ch03-numerical-methods-improved-euler": (["compute the first slope at the current point", "form the stated predictor or midpoint state and evaluate the second slope there", "use the required slope average or midpoint slope in the corrected update"], "mixing the Heun predictor-corrector stages with Euler or evaluating the second slope at the wrong state", "recompute both stage locations and substitute them in the complete corrected update"),
        "ede-ch03-numerical-methods-runge-kutta": (["evaluate $k_1$ at the current state", "evaluate $k_2$, $k_3$, and $k_4$ at their prescribed midpoint or endpoint states", "combine stages with weights $1,2,2,1$ and multiply by $h/6$"], "placing an RK4 stage at the wrong provisional state or weighting the stages equally", "recompute all four stages and their weighted combination before checking the endpoint"),
        "ede-ch03-numerical-methods-method-comparison": (["hold the IVP, interval, endpoint, and comparison criterion fixed", "count slope evaluations and compute the requested error evidence", "compare accuracy, cost, and step-size sensitivity using like-for-like data"], "declaring a method superior from step size alone or ignoring evaluation cost", "check that every reported error uses the same endpoint and that cost counts all stage evaluations"),
        "ede-ch04-first-order-applications-growth-decay": (["identify the proportional-rate or approach-to-limit law", "apply the initial value or doubling/half-life condition to determine constants", "check sign, units, initial value, and long-run behavior"], "using the wrong exponent sign or confusing the transient coefficient with the limiting value", "differentiate the proposed exponential model and check its initial value and limit"),
        "ede-ch04-first-order-applications-cooling-mixing": (["translate the physical flow or temperature statement into a signed rate balance", "use ambient excess or flow-times-concentration with the correct volume", "solve or interpret the IVP and check units, nonnegativity, and limiting behavior"], "omitting the ambient shift, using amount as concentration, or reversing an inflow/outflow sign", "substitute the solution into the balance and check volume, units, initial data, and physical limits"),
        "ede-ch04-first-order-applications-mechanics": (["choose and state a positive direction", "write Newton's law with resistance opposing velocity", "solve for or interpret the requested velocity and verify terminal behavior"], "dropping the mass factor or assigning resistance the same direction as motion", "check force units, the sign convention, and the zero-acceleration terminal condition"),
        "ede-ch04-first-order-applications-autonomous-phase": (["solve $f(y)=0$ for equilibria", "determine the sign of $f$ on each interval between equilibria", "direct phase-line arrows and classify stability from both sides"], "classifying stability from $f(y_*)=0$ alone or reversing the phase-line arrows", "sample the rate on every neighboring interval and confirm each arrow from the sign"),
        "ede-ch04-first-order-applications-curves": (["differentiate the given curve family and eliminate its parameter", "take the negative reciprocal of the resulting slope where defined", "separate or integrate the orthogonal equation and verify perpendicular slopes"], "retaining the family parameter or using the same/negative slope instead of the negative reciprocal", "differentiate both families and verify that their slopes multiply to $-1$ at regular intersections")
    }
    records=[]
    for d in docs:
        for i,(iid,qtype,prompt) in enumerate(items(d)):
            if "worked-examples" in d["id"]:
                obj=cfg["objectives"][[0,2,3][i//3] if ch==3 else [1,1,4][i//3]]
            else:
                obj=cfg["objectives"][i%5]
            oi=cfg["objectives"].index(obj)
            method_steps, misconception, verification = method_contracts[obj]
            records.append({"id":f"{d['id']}-{i+1:03d}","objectiveId":obj,"assessmentId":d["id"],"questionId":iid,"questionType":qtype,"sourceChunks":[f"{SOURCE}:chunk-{cfg['chunks'][oi]}"],"reviewState":"approved","givens":prompt,"unknown":f"Determine and justify the specific result requested in item {iid}.","representationRequirement":"Use a diagram only when the prompt depends on numerical geometry, model flow, phase-line direction, or orthogonality.","governingPrinciple":objective_titles[obj],"methodSteps":method_steps,"misconception":misconception,"difficultyEvidence":"The item combines its stated equation or model with a distinct computation, comparison, interpretation, or verification demand.","verification":verification,"variationAxes":["equation or physical scenario",f"response form: {qtype}",f"objective method branch: {obj}"],"reasoningSignature":f"{d['id']}::{iid}::{obj}::reasoning-{i+1}"})
    common.write_json(REF/"question-blueprints"/f"{cfg['topic']}-blueprints.json",{"schemaVersion":1,"sourceId":SOURCE,"reviewState":"approved","blueprints":records})
    for d in docs:
        objective_ids=[]
        source_ids=[]
        for i,_ in enumerate(items(d)):
            if "worked-examples" in d["id"]: obj=cfg["objectives"][[0,2,3][i//3] if ch==3 else [1,1,4][i//3]]
            else: obj=cfg["objectives"][i%5]
            if obj not in objective_ids: objective_ids.append(obj)
        for obj in objective_ids: source_ids.append(f"{SOURCE}:chunk-{cfg['chunks'][cfg['objectives'].index(obj)]}")
        common.write_json(REF/"content-manifests"/f"{d['id']}.json",{"schemaVersion":1,"id":f"{d['id']}-manifest","categoryId":CATEGORY,"topicId":cfg["topic"],"assessmentId":d["id"],"objectiveIds":objective_ids,"sourceId":SOURCE,"sourceChunkIds":source_ids,"reviewState":"approved"})
    meta=[("concept-lesson","conceptLesson","learn","conceptLesson",6),("glossary","glossary","learn","glossary",cfg["glossaryCount"]),("worked-examples","workedExample","learn","guidedWorkedExample",3),("recall-drill","recallDrill","recall","mixedRecallSet",cfg["recallCount"]),("easy-quiz","quiz","practice","focusedPractice",10),("test","test","evaluate","formalTest",12)]
    artifacts=[]
    for suffix,atype,goal,activity,count in meta:
        aid=f"{cfg['topic']}-{suffix}"; manifest=json.loads((REF/"content-manifests"/f"{aid}.json").read_text(encoding="utf-8"))
        artifacts.append({"id":aid,"assessmentType":atype,"learningGoal":goal,"activityType":activity,"objectiveIds":manifest["objectiveIds"],"plannedCount":count,"publicationStatus":"published"})
    common.write_json(REF/"assessment-release-manifests"/f"{cfg['topic']}.json",{"schemaVersion":1,"id":f"{cfg['topic']}-assessment-release","categoryId":CATEGORY,"topicId":cfg["topic"],"areaId":AREA,"packetId":cfg["packet"],"publicationStatus":"published","sourceReviewState":"approved","artifacts":artifacts})


def visuals() -> None:
    assets={
        "ch03-error-method-comparison.svg":'''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="430" viewBox="0 0 1050 430" role="img" aria-labelledby="t d"><title id="t">Numerical error and method comparison</title><desc id="d">A reference curve is compared with coarse and fine Euler polygons. One-step local error and final global errors are labeled. A table compares Euler, Heun, and RK4 evaluations per step and typical global order.</desc><rect width="1050" height="430" rx="22" fill="#f8fafc"/><g transform="translate(55 45)" font-family="Arial,sans-serif"><path d="M0 300H610M0 0V320" stroke="#334155" stroke-width="3"/><path d="M20 280C160 250 250 175 360 120S520 45 590 35" fill="none" stroke="#2563eb" stroke-width="5"/><polyline points="20,280 210,215 400,123 590,75" fill="none" stroke="#dc2626" stroke-width="4" stroke-dasharray="12 8"/><polyline points="20,280 115,255 210,214 305,170 400,121 495,78 590,43" fill="none" stroke="#0f766e" stroke-width="4"/><path d="M210 214v-22" stroke="#b45309" stroke-width="4"/><path d="M590 75v-40M590 43v-8" stroke="#7c3aed" stroke-width="4"/><text x="330" y="90" fill="#2563eb" font-size="18">reference</text><text x="320" y="225" fill="#dc2626" font-size="18">coarse Euler</text><text x="330" y="155" fill="#0f766e" font-size="18">fine Euler</text><text x="120" y="190" fill="#b45309" font-size="17">local one-step error</text><text x="455" y="105" fill="#7c3aed" font-size="17">endpoint global errors</text><g transform="translate(655 50)"><rect width="325" height="245" rx="15" fill="#eef2ff" stroke="#4338ca" stroke-width="3"/><text x="162" y="36" text-anchor="middle" font-size="20" font-weight="700">Cost and typical order</text><text x="25" y="78" font-size="18">Euler</text><text x="145" y="78" font-size="18">1 eval/step</text><text x="265" y="78" font-size="18">order 1</text><text x="25" y="125" font-size="18">Heun</text><text x="145" y="125" font-size="18">2 eval/step</text><text x="265" y="125" font-size="18">order 2</text><text x="25" y="172" font-size="18">RK4</text><text x="145" y="172" font-size="18">4 eval/step</text><text x="265" y="172" font-size="18">order 4</text><text x="162" y="218" text-anchor="middle" font-size="17">compare at the same endpoint</text></g></g></svg>''',
        "ch04-phase-line-trajectory-map.svg":'''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="430" viewBox="0 0 1050 430" role="img" aria-labelledby="t d"><title id="t">Phase-line stability and orthogonal trajectories</title><desc id="d">Two phase lines show arrows toward a stable equilibrium and away from an unstable equilibrium, paired with representative solution curves. A second panel shows intersecting tangent directions with negative reciprocal slopes.</desc><rect width="1050" height="430" rx="22" fill="#f8fafc"/><g font-family="Arial,sans-serif"><text x="250" y="38" text-anchor="middle" font-size="22" font-weight="700">Autonomous stability</text><path d="M100 80V360M280 80V360" stroke="#334155" stroke-width="4"/><circle cx="100" cy="210" r="9" fill="#15803d"/><circle cx="280" cy="210" r="9" fill="#dc2626"/><path d="M100 105v75M100 315v-75" stroke="#15803d" stroke-width="5"/><path d="M280 180v-75M280 240v75" stroke="#dc2626" stroke-width="5"/><text x="70" y="390" font-size="18">stable</text><text x="242" y="390" font-size="18">unstable</text><path d="M355 320C425 305 450 235 500 210S580 200 620 200" fill="none" stroke="#15803d" stroke-width="4"/><path d="M355 90C425 105 455 170 500 195S575 200 620 200" fill="none" stroke="#15803d" stroke-width="4"/><path d="M355 205H620" stroke="#64748b" stroke-width="2" stroke-dasharray="8 6"/><text x="760" y="38" text-anchor="middle" font-size="22" font-weight="700">Orthogonal slopes</text><path d="M665 315C730 270 800 210 930 95" fill="none" stroke="#2563eb" stroke-width="5"/><path d="M675 105C760 165 840 240 930 325" fill="none" stroke="#b45309" stroke-width="5"/><path d="M765 220l105 -92M765 220l95 95" stroke="#334155" stroke-width="4"/><rect x="782" y="210" width="22" height="22" fill="none" stroke="#334155" stroke-width="3"/><text x="700" y="345" font-size="18" fill="#2563eb">slope m</text><text x="835" y="350" font-size="18" fill="#b45309">slope −1/m</text></g></svg>'''}
    MEDIA.mkdir(parents=True,exist_ok=True)
    for name, text in assets.items():
        if name == "ch04-phase-line-trajectory-map.svg":
            markers = '<defs><marker id="stable-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#15803d"/></marker><marker id="unstable-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#dc2626"/></marker></defs>'
            text = text.replace('<rect width="1050" height="430" rx="22" fill="#f8fafc"/>', '<rect width="1050" height="430" rx="22" fill="#f8fafc"/>' + markers)
            text = text.replace('<path d="M100 105v75M100 315v-75" stroke="#15803d" stroke-width="5"/>', '<path d="M100 105v75" stroke="#15803d" stroke-width="5" marker-end="url(#stable-arrow)"/><path d="M100 315v-75" stroke="#15803d" stroke-width="5" marker-end="url(#stable-arrow)"/>')
            text = text.replace('<path d="M280 180v-75M280 240v75" stroke="#dc2626" stroke-width="5"/>', '<path d="M280 180v-75" stroke="#dc2626" stroke-width="5" marker-end="url(#unstable-arrow)"/><path d="M280 240v75" stroke="#dc2626" stroke-width="5" marker-end="url(#unstable-arrow)"/>')
        (MEDIA / name).write_text(text + "\n", encoding="utf-8")


def main() -> None:
    chapters={3:chapter3(),4:chapter4()}
    for ch,docs in chapters.items():
        for d in docs: common.write_assessment(ASSESS/f"{d['id']}.yaml",d)
        contracts(ch,docs)
    visuals()


if __name__ == "__main__": main()

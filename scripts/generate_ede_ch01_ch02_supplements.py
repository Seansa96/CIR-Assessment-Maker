"""Generate the approved Chapters 1-2 supplemental EDE learning release.

The source text is never copied into learner artifacts.  This script records only
source chunk identifiers in the tracked S2C contracts.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSESS = ROOT / "data" / "assessments"
REF = ROOT / "docs" / "assessment-reference"
MEDIA = ROOT / "frontend" / "public" / "media" / "ede"
CAT = "elementary-differential-equations-bvp"
SRC = "src-20260806084558-47ac4b59f9"


class LiteralDumper(yaml.SafeDumper):
    pass


def _str(dumper, value):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


LiteralDumper.add_representer(str, _str)


SIGNALS = {
    "readiness": "ede-readiness-rule-error",
    "units": "ede-unit-consistency-error",
    "model": "ede-model-assumption-error",
    "type": "ede-equation-type-confusion",
    "branch": "ede-implicit-branch-error",
    "domain": "ede-validity-interval-error",
    "field": "ede-direction-field-construction-error",
    "theorem": "ede-local-global-theorem-confusion",
    "linear": "ede-complementary-solution-confusion",
    "lost": "ede-transformed-solution-lost",
    "factor": "ede-integrating-factor-equivalence-error",
    "method": "ede-method-selection-error",
}


def common_check(qid, qtype, prompt, objective, explanation):
    return {
        "id": qid,
        "type": qtype,
        "prompt": prompt,
        "skills": [objective],
        "media": [],
        "difficultyDimensions": ["modelOrDerivation", "errorDiagnosis" if qtype in ("multipleChoice", "selectAll") else "calculation"],
        "subjectDifficultyTags": [objective],
        "difficultyEvidence": "Requires choosing the governing relation and checking the result against the stated conditions.",
        "explanation": explanation,
    }


def mc(qid, prompt, objective, choices, correct, solution, signal="method"):
    q = common_check(qid, "multipleChoice", prompt, objective,
                     f"Solution: {solution}\n\nWhy it works: The stated structure and conditions determine the result.\n\nWhy the other choices fail: The other choices misuse a rule, omit a condition, or reverse the relevant relationship.")
    q["choices"] = []
    for cid, text in choices:
        choice = {"id": cid, "text": text}
        if cid != correct:
            choice["issueSignals"] = [{"id": SIGNALS[signal], "domains": [CAT]}]
        q["choices"].append(choice)
    q["answer"] = {"choiceId": correct}
    return q


def num(qid, prompt, objective, value, solution, tolerance=0.0001):
    q = common_check(qid, "numericResponse", prompt, objective,
                     f"Solution: {solution}\n\nWhy it works: Direct substitution verifies the numerical result and its units or sign.")
    q["answer"] = {"value": value, "tolerance": tolerance}
    return q


def sym(qid, prompt, objective, latex, solution, variables=("x",)):
    q = common_check(qid, "symbolicResponse", prompt, objective,
                     f"Solution: {solution}\n\nWhy it works: Differentiation and the supplied data verify the expression.")
    q["answer"] = {"expectedLatex": latex, "equivalenceMode": "expression", "variables": list(variables), "tolerance": 0.0001}
    return q


def section(sid, title, content, check, media=None):
    return {"id": sid, "title": title, "required": True, "content": content, "media": media or [], "check": check}


def concept(aid, topic, title, intro, sections):
    return {
        "schemaVersion": 1, "id": aid, "title": title, "assessmentType": "conceptLesson",
        "categoryId": CAT, "topicId": topic, "modeDefault": "practice", "randomizeQuestions": False,
        "skills": [topic], "navigation": {"learningGoal": "learn", "activityType": "conceptLesson", "tags": [CAT, topic, "s2c-approved", "supplemental"]},
        "lesson": {"introduction": intro, "sections": sections},
    }


def step(sid, title, instruction, prompt, solution, points):
    return {
        "id": sid, "title": title, "instruction": instruction, "type": "freeResponse", "prompt": prompt,
        "choices": [], "answer": {"gradingMode": "selfCheck", "keyPoints": points},
        "explanation": f"Solution: {solution}\n\nWhy it works: The calculation preserves the original equation, data, and domain conditions.", "media": [],
    }


def example(eid, title, problem, rows):
    return {"id": eid, "title": title, "problem": problem,
            "steps": [step(f"{eid}-s{i}", *row) for i, row in enumerate(rows, 1)]}


def worked(aid, topic, title, examples):
    return {
        "schemaVersion": 1, "id": aid, "title": title, "assessmentType": "workedExample",
        "categoryId": CAT, "topicId": topic, "modeDefault": "practice", "randomizeQuestions": False,
        "skills": [topic], "navigation": {"learningGoal": "learn", "activityType": "guidedWorkedExample", "tags": [CAT, topic, "s2c-approved", "supplemental"]},
        "workedExamples": examples,
    }


def ch1_assessments():
    ready = "ede-ch01-introduction-calculus-readiness"
    model = "ede-ch01-introduction-model-types-assumptions"
    classify = "ede-ch01-introduction-classify-solutions"
    valid = "ede-ch01-introduction-initial-value-validity"
    field = "ede-ch01-introduction-direction-fields"
    rate = "ede-ch01-introduction-model-rate-laws"
    return [
        concept("ede-ch01-ode-readiness-concept-lesson", "ede-ch01-introduction", "ODE Readiness: Calculus, Algebra, and Domains",
                "A differential-equations method is reliable only when its algebra, calculus, units, and domain restrictions are reliable.", [
            section("s1", "Functions and valid domains", "A proposed solution must be defined and differentiable on an open interval. Denominators cannot vanish, logarithm arguments must be positive before absolute-value simplification, and an IVP interval must contain its initial input.", mc("q001", "What is the real domain of $f(x)=\\ln(x-2)/(x+1)$?", ready, [("a", "$(2,\\infty)$"), ("b", "$(-1,\\infty)$"), ("c", "$(-\\infty,-1)\\cup(2,\\infty)$"), ("d", "$[-1,2]$")], "a", "The logarithm requires $x>2$, which already excludes $x=-1$.", "domain")),
            section("s2", "Derivatives as rates with units", "If $V(t)$ is measured in liters and $t$ in minutes, then $V'(t)$ is measured in liters per minute. Units are a fast check on whether a proposed rate law can be correct.", mc("q002", "If $M(t)$ is mass in grams and $t$ is seconds, what are the units of $M'(t)$?", ready, [("a", "grams per second"), ("b", "seconds per gram"), ("c", "grams"), ("d", "grams squared per second")], "a", "$M'$ measures change in mass divided by change in time.", "units")),
            section("s3", "Product and chain rules", "ODE verification often differentiates products and compositions. For $y=x e^{x^2}$, the product rule and chain rule give $y'=e^{x^2}(1+2x^2)$.", mc("q003", "Differentiate $x e^{x^2}$.", ready, [("a", "$e^{x^2}(1+2x^2)$"), ("b", "$2x^2e^{x^2}$"), ("c", "$e^{2x}$"), ("d", "$(1+2x)e^{x^2}$")], "a", "The product derivative is $e^{x^2}+x(2x)e^{x^2}$.", "readiness")),
            section("s4", "Antiderivatives and initial data", "Integrating $y'=g(x)$ gives a family $y=G(x)+C$. The constant remains until initial data select one member of the family.", sym("q004", "Solve $y'=6x-2$ with $y(0)=5$.", ready, "3x^2-2x+5", "$y=3x^2-2x+C$ and $C=5$.")),
            section("s5", "Logarithms and partial fractions", "Separation frequently produces rational functions. Decompose first, integrate each simple term, retain absolute values, and only then use initial data to choose a branch.", mc("q005", "Which decomposition is correct for $1/[y(y-2)]$?", ready, [("a", "$-1/(2y)+1/[2(y-2)]$"), ("b", "$1/y+1/(y-2)$"), ("c", "$1/(2y)+1/[2(y-2)]$"), ("d", "$-1/y+1/(y-2)$")], "a", "Solving $1=A(y-2)+By$ gives $A=-1/2$ and $B=1/2$.", "readiness")),
            section("s6", "Implicit differentiation and verification", "An implicit relation can define local solution branches. Differentiate the entire relation, solve for the required derivative where possible, and check that the selected point lies on the curve.", num("q006", "For $x^2+y^2=25$, find $dy/dx$ at $(3,4)$.", ready, -0.75, "$2x+2yy'=0$, so $y'=-x/y=-3/4$.")),
        ]),
        worked("ede-ch01-ode-readiness-worked-examples", "ede-ch01-introduction", "ODE Readiness: Worked Examples", [
            example("we01", "Verify a product-composition solution", "Verify that $y=xe^{-x}$ solves $y'+y=e^{-x}$ and state its maximal interval.", [
                ("Differentiate accurately", "Apply product and chain rules.", "Compute $y'$.", "$y'=e^{-x}-xe^{-x}=(1-x)e^{-x}$.", ["Uses product rule", "Uses chain rule"]),
                ("Substitute into the ODE", "Combine the derivative and original function.", "Evaluate $y'+y$.", "$(1-x)e^{-x}+xe^{-x}=e^{-x}$, matching the right side.", ["Substitutes", "Simplifies"]),
                ("Check the interval", "Inspect both formula and equation for singularities.", "State the maximal interval.", "$xe^{-x}$ and $e^{-x}$ are defined and smooth for every real $x$, so the interval is $(-\\infty,\\infty)$.", ["Checks formula", "States all reals"]),
            ]),
            example("we02", "Recover a family and impose data", "Solve $y'=3x^2-4$ with $y(1)=2$.", [
                ("Integrate the rate", "Include the arbitrary constant.", "Find the solution family.", "$y=x^3-4x+C$.", ["Antidifferentiates", "Includes constant"]),
                ("Apply the initial value", "Substitute the supplied point.", "Determine $C$.", "$2=1-4+C$, so $C=5$.", ["Uses initial condition", "Finds five"]),
                ("Verify", "Differentiate and evaluate the data.", "Check the final result.", "$y=x^3-4x+5$ has $y'=3x^2-4$ and $y(1)=2$.", ["Checks derivative", "Checks data"]),
            ]),
            example("we03", "Partial fractions and a solution branch", "Solve $y'=y(y-2)$ with $y(0)=1$ using partial fractions.", [
                ("Separate without losing equilibria", "Record zero factors before division.", "Separate variables and list equilibria.", "$y=0$ and $y=2$ are equilibria; otherwise $dy/[y(y-2)]=dx$.", ["Retains equilibria", "Separates"]),
                ("Integrate and choose the sign", "Use partial fractions and the initial point.", "Obtain an implicit relation.", "$\\tfrac12\\ln|(y-2)/y|=x+C$; the initial value gives $C=0$ and the ratio is negative on this branch.", ["Integrates", "Uses branch sign"]),
                ("Solve and verify the interval", "Isolate $y$ and inspect its denominator.", "Give the explicit solution and interval.", "$y=2/(1+e^{2x})$, defined for all real $x$; differentiation verifies $y'=y(y-2)$.", ["Solves explicitly", "Checks interval"]),
            ]),
        ]),
        concept("ede-ch01-modeling-depth-concept-lesson", "ede-ch01-introduction", "Modeling Depth: From Assumptions to Differential Equations",
                "A model links a stated mechanism to a rate law, then checks units, assumptions, and useful limits.", [
            section("s1", "The modeling cycle", "Name the state, state assumptions, translate mechanisms into rates, attach data, analyze the result, and compare predictions with observations. A mismatch calls for revised assumptions, not silent parameter changes.", mc("q001", "A cooling model repeatedly underpredicts measured temperatures. What is the scientifically appropriate next step?", model, [("a", "Reexamine assumptions such as constant ambient temperature"), ("b", "Declare the measurements impossible"), ("c", "Delete the initial condition"), ("d", "Change temperature units without conversion")], "a", "A persistent model-data mismatch is evidence that assumptions or parameters need review.", "model")),
            section("s2", "State variables, parameters, and units", "A state variable changes; a parameter is held fixed within the model. Every term in an equation for $Q'$ must have the same amount-per-time units.", num("q002", "Water enters at $5$ L/min carrying $0.8$ g/L of dye. Find the dye input rate in g/min.", rate, 4.0, "$5(0.8)=4$ g/min.")),
            section("s3", "Proportional and limited growth", "The Malthus law $P'=aP$ assumes a constant per-capita rate. The logistic law $P'=aP(1-P/K)$ introduces a limiting level $K$ and reverses the sign above it.", mc("q003", "For $P'=0.3P(1-P/500)$ and $P=600$, what does the model predict?", rate, [("a", "$P$ decreases"), ("b", "$P$ increases exponentially"), ("c", "$P$ is an equilibrium"), ("d", "The derivative has population units")], "a", "$1-600/500<0$, so the rate is negative.", "model")),
            section("s4", "Balance laws", "For an amount in a compartment, accumulation equals total inflow minus total outflow. Concentration must be expressed as amount divided by the current volume before multiplying by a volumetric flow.", mc("q004", "A well-mixed tank contains $S$ grams in $100$ L and drains at $2$ L/min. What is the salt outflow rate?", rate, [("a", "$S/50$ g/min"), ("b", "$2S$ g/min"), ("c", "$S/100$ g/min"), ("d", "$50/S$ g/min")], "a", "The concentration is $S/100$ g/L, so outflow is $2(S/100)=S/50$ g/min.", "units")),
            section("s5", "Order and required initial data", "A position model involving acceleration is second order. A typical second-order IVP specifies position and velocity at one time, while a first-order scalar IVP specifies one state value.", mc("q005", "Which data normally complete $y''=-g$ as an IVP at $t=0$?", model, [("a", "$y(0)$ and $y'(0)$"), ("b", "$y(0)$ only"), ("c", "$y''(0)$ only"), ("d", "$y(0),y'(0),y''(0)$")], "a", "A second-order equation normally requires two initial conditions through the first derivative.", "type")),
            section("s6", "Scalar equations, systems, ODEs, and PDEs", "An ODE has ordinary derivatives of functions of one independent variable. A system contains multiple coupled unknown functions. A PDE contains partial derivatives of a function of several independent variables.", mc("q006", "How should $P'=P(1-P-Q)$ and $Q'=Q(2-P-Q)$ be classified?", model, [("a", "A coupled system of first-order ODEs"), ("b", "One second-order ODE"), ("c", "A PDE"), ("d", "An algebraic equation")], "a", "Two time-dependent states are governed by two coupled first-order ordinary differential equations.", "type")),
        ]),
        worked("ede-ch01-modeling-depth-worked-examples", "ede-ch01-introduction", "Modeling Depth: Worked Examples", [
            example("we01", "An epidemic mechanism", "A closed susceptible group has size $S$. Infections occur at a rate proportional to infected-susceptible encounters.", [
                ("Define the state", "Identify infected and susceptible counts.", "Name the unknown and remaining susceptible population.", "Let $I(t)$ be infected people; then $S-I(t)$ are still susceptible.", ["Defines state", "Uses closed population"]),
                ("Translate the mechanism", "Use the proportional encounter assumption.", "Write the differential equation.", "$I'=rI(S-I)$, where $r>0$ has units person$^{-1}$time$^{-1}$.", ["Writes product law", "States units"]),
                ("Interpret limiting states", "Set the rate to zero and discuss assumptions.", "Find equilibria and state one limitation.", "$I=0$ and $I=S$ are equilibria; the model omits recovery and population exchange.", ["Finds equilibria", "States limitation"]),
            ]),
            example("we02", "Cooling as an IVP", "A sample at $72^\\circ$C is placed in a constant $18^\\circ$C room and follows Newton cooling with $k>0$.", [
                ("Choose sign and state", "Temperature should move toward ambient.", "Define $T$ and write its rate law.", "$T(t)$ is sample temperature and $T'=-k(T-18)$.", ["Defines state", "Uses negative feedback"]),
                ("Attach data", "Combine rate law and measurement.", "Write the IVP.", "$T'=-k(T-18),\\quad T(0)=72$.", ["States ODE", "States initial value"]),
                ("Interpret before solving", "Use signs and equilibrium.", "Find the equilibrium and initial direction.", "$T=18$ is equilibrium, and $T'(0)=-54k<0$, so the sample initially cools.", ["Finds equilibrium", "Finds sign"]),
            ]),
            example("we03", "Order and model architecture", "Compare free fall $y''=-g$ with a two-species model $P'=F(P,Q)$, $Q'=G(P,Q)$.", [
                ("Classify free fall", "Use the highest derivative.", "Give its order and state dimension after first-order conversion.", "It is one second-order ODE, equivalent to two first-order state equations for position and velocity.", ["Second order", "Two state variables"]),
                ("Classify competition", "Count unknown functions and equation orders.", "Classify the species model.", "It is a coupled system of two first-order ODEs.", ["Two unknowns", "First-order system"]),
                ("Specify initial data", "Match data count to evolving states.", "State typical initial conditions for both models.", "Free fall needs $y(0)=y_0,y'(0)=v_0$; competition needs $P(0)=P_0,Q(0)=Q_0$.", ["Two conditions each", "Matches states"]),
            ]),
        ]),
        concept("ede-ch01-solution-geometry-concept-lesson", "ede-ch01-introduction", "Solution Geometry: Branches, Fields, and Singular Curves",
                "Solutions are curves constrained simultaneously by local slopes, initial data, and the domain of the differential equation.", [
            section("s1", "Solution curves and integral curves", "A solution curve is the graph of one differentiable function on an interval. An integral curve may be assembled from local function branches when the geometric curve is not globally a graph $y(x)$.", mc("q001", "Why is a full circle not the graph of one solution $y(x)$?", classify, [("a", "Most vertical lines meet it twice"), ("b", "Its radius is constant"), ("c", "It contains no differentiable arcs"), ("d", "It has no tangent slopes")], "a", "A function of $x$ can assign only one $y$ to each input, although each semicircle is a local graph.", "branch")),
            section("s2", "Implicit branches", "From $x^2+y^2=a^2$, the branches are $y=\\pm\\sqrt{a^2-x^2}$. Initial data determine the sign, while implicit differentiation gives $y'=-x/y$ wherever $y\\ne0$.", mc("q002", "Which branch of $x^2+y^2=9$ contains $(0,-3)$?", classify, [("a", "$y=-\\sqrt{9-x^2}$"), ("b", "$y=\\sqrt{9-x^2}$"), ("c", "$x=\\sqrt{9-y^2}$"), ("d", "$y=9-x^2$")], "a", "The initial point has negative $y$, selecting the lower semicircle.", "branch")),
            section("s3", "Maximal intervals and singular loci", "A solution branch stops being a valid $y(x)$ solution when its formula or the original ODE ceases to be defined. For $y'=-x/y$, the line $y=0$ is a singular locus.", mc("q003", "What is the maximal open interval for the upper branch $y=\\sqrt{25-x^2}$?", valid, [("a", "$(-5,5)$"), ("b", "$[-5,5]$"), ("c", "$(0,5)$"), ("d", "$(-\\infty,\\infty)$")], "a", "At $x=\\pm5$ the branch reaches $y=0$, where the original right side is undefined.", "domain")),
            section("s4", "Constructing a direction field", "At each selected point $(x,y)$, evaluate $f(x,y)$ and draw a short segment with that slope. The segment records local direction, not a finite numerical step.", num("q004", "For $y'=x-y$, what slope is drawn at $(2,-1)$?", field, 3.0, "$f(2,-1)=2-(-1)=3$.")),
            section("s5", "Tracing plausible integral curves", "A traced curve should remain tangent to nearby field segments. Steepness, sign changes, and zero-slope curves guide the sketch, but a field alone does not supply an exact formula.", mc("q005", "For $y'=x-y$, where are field segments horizontal?", field, [("a", "On $y=x$"), ("b", "On the $x$-axis"), ("c", "On the $y$-axis"), ("d", "Nowhere")], "a", "Horizontal segments satisfy $x-y=0$.", "field")),
            section("s6", "Parametric motion through a singular slope", "For $y'=A(x,y)/B(x,y)$, the parametric system $dx/dt=B$, $dy/dt=A$ can describe a curve even where the quotient slope is vertical because $B=0$.", mc("q006", "Which parametric system corresponds to $y'=x/y$?", field, [("a", "$dx/dt=y,\\ dy/dt=x$"), ("b", "$dx/dt=x,\\ dy/dt=y$"), ("c", "$dx/dt=1/y,\\ dy/dt=1/x$"), ("d", "$dx/dt=-y,\\ dy/dt=x$")], "a", "The quotient $(dy/dt)/(dx/dt)$ is $x/y$ wherever $y\\ne0$.", "field")),
        ]),
        worked("ede-ch01-solution-geometry-worked-examples", "ede-ch01-introduction", "Solution Geometry: Worked Examples", [
            example("we01", "A circle as an implicit integral curve", "Use $x^2+y^2=25$ with $y'=-x/y$ and initial point $(3,4)$.", [
                ("Verify implicitly", "Differentiate the relation.", "Show that its branches satisfy the ODE.", "$2x+2yy'=0$ gives $y'=-x/y$ wherever $y\\ne0$.", ["Implicit differentiation", "Notes restriction"]),
                ("Select the branch", "Use the sign of the initial value.", "Write the explicit branch.", "$y=\\sqrt{25-x^2}$ because the point has positive $y$.", ["Chooses upper branch", "Contains initial point"]),
                ("State the interval", "Locate endpoints where the ODE fails.", "Give the maximal IVP interval.", "$(-5,5)$; at the endpoints $y=0$ and $-x/y$ is undefined.", ["Open interval", "Checks ODE domain"]),
            ]),
            example("we02", "Build a local direction field", "For $y'=x-y$, analyze slopes near the points $(0,1)$, $(1,1)$, and $(2,1)$.", [
                ("Compute sample slopes", "Evaluate $f=x-y$ at each point.", "List the three slopes.", "The slopes are $-1,0,1$, respectively.", ["Evaluates field", "Keeps point order"]),
                ("Locate zero slopes", "Solve the slope-zero condition.", "Find the horizontal-segment curve.", "$x-y=0$, so field segments are horizontal on $y=x$.", ["Solves condition", "Identifies line"]),
                ("Trace qualitatively", "Compare points above and below the zero-slope line.", "Describe the local curve behavior.", "Above $y=x$ slopes are negative; below it slopes are positive, so traced curves turn where they meet the line.", ["Sign regions", "Connects to curves"]),
            ]),
            example("we03", "A vertical tangent in parametric form", "Compare $y'=x/y$ with $dx/dt=y$, $dy/dt=x$.", [
                ("Recover the quotient", "Divide parametric rates where allowed.", "Compute $dy/dx$.", "$dy/dx=(dy/dt)/(dx/dt)=x/y$ when $y\\ne0$.", ["Uses quotient", "States restriction"]),
                ("Find the curve family", "Differentiate a conserved expression.", "Show that $y^2-x^2$ is constant.", "$d(y^2-x^2)/dt=2yx-2xy=0$, so $y^2-x^2=C$.", ["Differentiates invariant", "Finds constant"]),
                ("Interpret $y=0$", "Evaluate the parametric vector there.", "Explain the apparent singularity.", "At $(x,0)$ with $x\\ne0$, $dx/dt=0$ and $dy/dt=x$, so the curve has a vertical tangent although $dy/dx$ is undefined.", ["Evaluates vector", "Identifies vertical tangent"]),
            ]),
        ]),
    ]


def ch2_assessments():
    lin="ede-ch02-first-order-equations-linear-ivps"; sep="ede-ch02-first-order-equations-separable-equilibria"
    eu="ede-ch02-first-order-equations-existence-uniqueness"; trans="ede-ch02-first-order-equations-nonlinear-transformations"
    exact="ede-ch02-first-order-equations-exact-equations"; fac="ede-ch02-first-order-equations-integrating-factors"
    return [
        concept("ede-ch02-linear-separable-depth-concept-lesson", "ede-ch02-first-order-equations", "Linear and Separable Equations: Structural Depth", "Linear and separable equations are families of related structures, not isolated recipes.", [
            section("s1","Normalize before classifying","Divide by the leading coefficient only on an interval where it is nonzero. The normalized coefficients and their continuity determine the interval on which the linear theorem applies.",mc("q001","Normalize $xy'+2y=x^3$ on $x>0$.",lin,[("a","$y'+(2/x)y=x^2$"),("b","$y'+2y=x^2$"),("c","$y'+(2/x)y=x^3$"),("d","$xy'+2y=x^2$")],"a","Dividing every term by $x$ gives $y'+(2/x)y=x^2$.","linear")),
            section("s2","Complementary solutions","The complementary equation $y'+p(x)y=0$ has nonzero solutions $y_1=Ce^{-\\int p dx}$. Differences of two solutions of the same nonhomogeneous equation solve this complementary equation.",mc("q002","A nonzero complementary solution for $y'+(3/x)y=0$ on $x>0$ is:",lin,[("a","$x^{-3}$"),("b","$x^3$"),("c","$e^{-3/x}$"),("d","$3\\ln x$")],"a","$e^{-\\int3/x dx}=e^{-3\\ln x}=x^{-3}$.","linear")),
            section("s3","Variation of parameters","Writing $y=u y_1$ uses a known complementary solution to cancel the homogeneous terms, leaving an equation for the varying coefficient $u$.",mc("q003","If $y_1=e^{-x}$ solves $y'+y=0$, what substitution starts variation of parameters for $y'+y=f(x)$?",lin,[("a","$y=u(x)e^{-x}$"),("b","$y=u(x)+e^{-x}$"),("c","$y=e^{-u(x)}$"),("d","$y=u'(x)e^x$")],"a","Use the product of the unknown varying parameter and the known complementary solution.","linear")),
            section("s4","Integrating factors and complementary solutions","A nonzero complementary solution $y_1$ and an integrating factor satisfy $\\mu=1/y_1$ up to a nonzero constant. Both viewpoints create a product derivative.",mc("q004","If $y_1=x^{-2}$ is a complementary solution on $x>0$, which integrating factor matches it?",lin,[("a","$x^2$"),("b","$x^{-2}$"),("c","$e^{x^{-2}}$"),("d","$2x$")],"a","The reciprocal $1/y_1=x^2$ is an integrating factor.","linear")),
            section("s5","Implicit separable solutions","After $dy/h(y)=g(x)dx$, integration may naturally produce an implicit relation. Isolating $y$ is optional unless an IVP or interpretation requires a branch.",mc("q005","After integration gives $y+\\ln|y-1|=x^2+C$, what is the correct next statement?",sep,[("a","It is an acceptable implicit solution relation where defined"),("b","It is invalid unless $y$ is isolated"),("c","Drop the logarithm absolute value"),("d","Set $C=0$ without data")],"a","Implicit solution relations are valid when differentiation recovers the ODE on an appropriate branch.","branch")),
            section("s6","Equilibria, branches, and blow-up","Dividing by a factor of $y$ can discard equilibrium solutions. An explicit nonconstant branch may also end at a finite point where its denominator vanishes even though the separated integral was algebraically valid.",mc("q006","For $y'=y(y-2)$, which solutions must be recorded before division?",sep,[("a","$y=0$ and $y=2$"),("b","$y=x$ only"),("c","$y=-2$ only"),("d","No constant solutions")],"a","Both zeros of the autonomous rate give equilibrium solutions.","lost")),
        ]),
        worked("ede-ch02-linear-separable-depth-worked-examples","ede-ch02-first-order-equations","Linear and Separable Equations: Worked Examples",[
            example("we01","A singular-coefficient linear IVP","Solve $xy'+y=x^2$, $y(1)=2$, on the interval containing the initial point.",[
                ("Normalize and choose interval","Divide only where $x$ is nonzero.","Write standard form and interval.","On $x>0$, $y'+y/x=x$; this interval contains $x=1$.",["Normalizes","Chooses x positive"]),
                ("Use the product derivative","Find the integrating factor and integrate.","Construct the general solution.","$\\mu=x$ and $(xy)'=x^2$, so $xy=x^3/3+C$ and $y=x^2/3+C/x$.",["Finds factor","Integrates"]),
                ("Apply and verify data","Determine the constant and check the original equation.","Give the IVP solution.","$2=1/3+C$ gives $C=5/3$; substitution verifies $xy'+y=x^2$ on $(0,\\infty)$.",["Finds constant","Checks interval"]),
            ]),
            example("we02","Variation of parameters and its reciprocal factor","Solve $y'-(2/x)y=x^2$, $y(1)=0$, on $x>0$ using $y=u x^2$.",[
                ("Choose a complementary solution","Solve the homogeneous equation.","Find $y_1$ and relate it to an integrating factor.","$y_1=x^2$; its reciprocal $x^{-2}$ is an integrating factor.",["Finds y1","Relates reciprocal"]),
                ("Vary the parameter","Substitute $y=ux^2$ and cancel complementary terms.","Find the equation for $u$.","$y'=u'x^2+2ux$, so substitution gives $u'x^2=x^2$ and $u'=1$.",["Differentiates product","Cancels terms"]),
                ("Apply data and verify","Integrate $u$ and use the IVP.","Give and check the solution.","$u=x+C$ and $0=1+C$, so $y=x^2(x-1)$; direct substitution verifies the IVP.",["Uses data","Verifies"]),
            ]),
            example("we03","A separable branch with finite blow-up","Solve $y'=y(y-2)$, $y(0)=3$, and find the maximal interval.",[
                ("Retain and separate","Record equilibria, then divide.","Write the separated equation.","$y=0,2$ are equilibria; for the IVP branch, $dy/[y(y-2)]=dx$.",["Retains equilibria","Separates"]),
                ("Integrate and apply data","Use partial fractions and the initial value.","Find the explicit branch.","$\\tfrac12\\ln|(y-2)/y|=x+C$ gives $(y-2)/y=e^{2x}/3$, hence $y=2/(1-e^{2x}/3)$.",["Integrates","Solves branch"]),
                ("Find the maximal interval","Locate the denominator zero around $x=0$.","State and verify the interval.","The denominator vanishes at $x=\\tfrac12\\ln3$, so the maximal interval is $(-\\infty,\\tfrac12\\ln3)$.",["Finds blow-up","Chooses containing interval"]),
            ]),
        ]),
        concept("ede-ch02-existence-uniqueness-depth-concept-lesson","ede-ch02-first-order-equations","Existence and Uniqueness: Local Geometry and Branching","The theorem answers separate questions about whether an IVP has a solution and whether nearby solutions are forced to agree.",[
            section("s1","Open rectangles around initial data","The standard theorem examines an open rectangle containing $(x_0,y_0)$ on which the right side and, for uniqueness, its $y$ derivative are continuous.",mc("q001","For $f=(x+y)/(x-y)$ at $(1,0)$, which obstacle must a valid rectangle avoid?",eu,[("a","The line $x=y$"),("b","The line $x=0$"),("c","The line $y=0$"),("d","The circle $x^2+y^2=1$")],"a","The denominator vanishes precisely on $x=y$.","theorem")),
            section("s2","Existence and uniqueness are separate","Continuity of $f$ gives local existence. Continuity of both $f$ and $f_y$ gives the standard sufficient local uniqueness conclusion.",mc("q002","If $f$ is continuous but $f_y$ is not continuous near the initial point, what follows from this test?",eu,[("a","Existence is guaranteed, but this test gives no uniqueness conclusion"),("b","No solution exists"),("c","Multiple solutions are proved"),("d","A global unique solution is guaranteed")],"a","The two parts of the theorem have different hypotheses and conclusions.","theorem")),
            section("s3","Sufficient is not necessary","A failed hypothesis means the theorem is silent; it does not establish the negation of its conclusion. Another argument may still prove uniqueness.",mc("q003","The standard $f_y$ condition fails. Which statement is logically valid?",eu,[("a","The theorem does not decide uniqueness"),("b","The IVP has infinitely many solutions"),("c","The IVP has no solutions"),("d","Every solution blows up")],"a","Failure of a sufficient condition is not proof that uniqueness fails.","theorem")),
            section("s4","Local versus global conclusions","The theorem guarantees a solution on some interval around $x_0$, not necessarily the whole coefficient domain and not necessarily the largest interval of existence.",mc("q004","What does a local uniqueness theorem guarantee?",eu,[("a","Agreement on some open interval containing $x_0$"),("b","A formula on all real numbers"),("c","No later singularity"),("d","A closed interval including every boundary")],"a","The conclusion is explicitly local around the initial input.","theorem")),
            section("s5","Actual nonuniqueness","For $y'=3y^{2/3}$ with $y(0)=0$, both $y=0$ and $y=x^3$ solve the IVP. Direct verification, not merely theorem failure, proves nonuniqueness.",mc("q005","Which pair directly proves nonuniqueness for $y'=3y^{2/3}$, $y(0)=0$?",eu,[("a","$y=0$ and $y=x^3$"),("b","$y=x$ and $y=-x$"),("c","$y=1$ and $y=e^x$"),("d","$y=x^2$ and $y=2x^2$")],"a","Both candidates satisfy the equation and initial value but differ immediately.","theorem")),
            section("s6","Branching and largest uniqueness intervals","A solution may be unique until it reaches a state where the uniqueness hypotheses fail, after which distinct continuations can branch. The largest uniqueness interval can therefore be smaller than the formula's domain.",mc("q006","Why can two continuations branch after meeting $y=0$ in $y'=3y^{2/3}$?",eu,[("a","$f_y=2y^{-1/3}$ is singular there"),("b","The equation becomes second order"),("c","The independent variable disappears"),("d","Every equilibrium must be crossed")],"a","The standard local uniqueness protection fails at $y=0$.","theorem")),
        ]),
        worked("ede-ch02-existence-uniqueness-depth-worked-examples","ede-ch02-first-order-equations","Existence and Uniqueness: Worked Examples",[
            example("we01","Avoid a singular line","Analyze $y'=(x+y)/(x-y)$ with $y(1)=0$.",[
                ("Locate discontinuities","Inspect $f$ and $f_y$.","Find the singular set.","Both are singular on $x=y$ and continuous away from that line.",["Finds denominator zero","Checks fy"]),
                ("Choose a rectangle","Place the initial point inside without crossing the singular set.","Give one valid rectangle.","For example, $1/2<x<3/2$ and $-1/4<y<1/4$ contains $(1,0)$ and has $x-y>0$.",["Contains point","Avoids line"]),
                ("State the conclusion","Separate local from global claims.","Apply the theorem.","A unique solution exists on some open interval containing $x=1$; no global interval is guaranteed.",["Existence","Local uniqueness"]),
            ]),
            example("we02","Existence without a theorem-based uniqueness claim","Analyze $y'=3y^{2/3}$ with $y(0)=0$.",[
                ("Check existence","Test continuity of $f$.","State the existence conclusion.","$f(y)=3y^{2/3}$ is continuous, so at least one local solution exists.",["Checks f","States existence"]),
                ("Check the uniqueness hypothesis","Differentiate with respect to $y$.","Explain why the standard test stops.","$f_y=2y^{-1/3}$ is undefined at $y=0$, so the sufficient uniqueness hypothesis fails.",["Computes fy","Does not overclaim"]),
                ("Verify actual behavior","Check two candidates directly.","Prove whether uniqueness holds.","Both $y=0$ and $y=x^3$ satisfy the IVP, so uniqueness actually fails.",["Verifies both","Concludes nonunique"]),
            ]),
            example("we03","A largest uniqueness interval","Analyze $y'=3y^{2/3}$ with $y(0)=-1$.",[
                ("Find the initial branch","Use the separated family.","Find a solution through the data.","The family $y=(x-C)^3$ gives $C=1$, so $y=(x-1)^3$.",["Finds family","Uses data"]),
                ("Locate loss of protection","Find where the branch reaches the singular state.","Determine the first zero.","$y=0$ at $x=1$, where $f_y$ is singular.",["Finds x=1","Connects theorem"]),
                ("Describe continuations","Compare immediate continuation with delayed departure.","State the largest interval of forced uniqueness.","The IVP is uniquely determined on $(-\\infty,1)$; after reaching zero, it may remain zero for a time before following a shifted cubic.",["Largest interval","Explains branching"]),
            ]),
        ]),
        concept("ede-ch02-nonlinear-transformations-depth-concept-lesson","ede-ch02-first-order-equations","Nonlinear Transformations: Bernoulli, Homogeneous, and Riccati Forms","A useful substitution is justified by equation structure and must be checked for lost solutions and domain restrictions.",[
            section("s1","Variation-of-parameters motif","Writing $y=u y_1$ lets a known related solution absorb part of the equation. In nonlinear problems, the remaining equation for $u$ may become separable.",mc("q001","What is the purpose of writing $y=u y_1$?",trans,[("a","Use known structure to obtain a simpler equation for $u$"),("b","Assume every solution is constant"),("c","Remove all initial conditions"),("d","Change the independent variable into a parameter")],"a","The known factor is chosen so terms cancel or combine into a separable form.","method")),
            section("s2","Bernoulli equations","For $y'+p(x)y=q(x)y^n$ with $n\\ne0,1$, the substitution $v=y^{1-n}$ produces a linear equation in $v$ on branches where the transformation is defined.",mc("q002","Which substitution applies to $y'+p(x)y=q(x)y^4$?",trans,[("a","$v=y^{-3}$"),("b","$v=y/x$"),("c","$v=y^4$"),("d","$v=x/y$")],"a","Bernoulli uses $v=y^{1-n}=y^{-3}$.","lost")),
            section("s3","Homogeneous nonlinear equations","An equation $y'=q(y/x)$ becomes separable with $y=ux$, so $y'=u+xu'$. This meaning of homogeneous differs from homogeneous linear equations.",mc("q003","After $y=ux$, what is $y'$?",trans,[("a","$u+xu'$"),("b","$xu'$"),("c","$u'$"),("d","$u/x$")],"a","Differentiate the product of two functions of $x$.","readiness")),
            section("s4","Constant-ratio solutions","Before dividing by $q(u)-u$, solve $q(u)=u$. Each root gives a constant $u$ and therefore a straight-line solution $y=ux$ that separation may otherwise lose.",mc("q004","For $q(u)=u^2$, which constant-ratio solutions arise?",trans,[("a","$y=0$ and $y=x$"),("b","$y=1$ only"),("c","$y=x^2$ only"),("d","No straight lines")],"a","$u^2=u$ gives $u=0,1$ and hence $y=ux$.","lost")),
            section("s5","Domain and translated-homogeneous forms","Because $y/x$ requires $x\\ne0$, solutions are considered on intervals on one side of zero. Some ratios of affine linear forms become homogeneous after translating $x=X+x_0$, $y=Y+y_0$ to their common intersection.",mc("q005","Why must a $y/x$ substitution track the interval?",trans,[("a","The ratio and transformed equation are undefined at $x=0$"),("b","Every solution is periodic"),("c","The exponent must be an integer"),("d","Partial derivatives are required")],"a","The substitution itself imposes $x\\ne0$.","domain")),
            section("s6","Known-solution Riccati reduction","For $y'=P+Qy+Ry^2$, subtracting a known particular solution $y_1$ by $z=y-y_1$ cancels the constant residual and produces a Bernoulli equation for $z$.",mc("q006","Given a known Riccati solution $y_1$, which substitution begins the reduction?",trans,[("a","$z=y-y_1$"),("b","$z=y/y'$"),("c","$z=x-y$"),("d","$z=e^y$")],"a","Subtracting the known solution removes the terms it already satisfies.","method")),
        ]),
        worked("ede-ch02-nonlinear-transformations-depth-worked-examples","ede-ch02-first-order-equations","Nonlinear Transformations: Worked Examples",[
            example("we01","A Bernoulli IVP","Solve $y'-y=xy^2$, $y(0)=1$.",[
                ("Recognize and substitute","Identify $n=2$ and transform.","Set $v=1/y$ and derive its equation.","Since $v'=-y'/y^2$, division by $y^2$ gives $v'+v=-x$.",["Uses Bernoulli substitution","Gets linear equation"]),
                ("Solve the transformed equation","Use the integrating factor $e^x$.","Find $v$ from the data.","$(e^xv)'=-xe^x$, so $v=1-x+Ce^{-x}$; $v(0)=1$ gives $C=0$.",["Integrates","Uses transformed data"]),
                ("Return and verify","Invert the substitution and inspect the denominator.","Give the solution and interval.","$y=1/(1-x)$ on $(-\\infty,1)$; differentiation gives $y'-y=xy^2$ and $y(0)=1$.",["Back-substitutes","Checks interval"]),
            ]),
            example("we02","A homogeneous nonlinear IVP","Solve $y'=(y/x)^2$, $y(1)=2$, on $x>0$.",[
                ("Transform and retain lines","Set $y=ux$ and check constant $u$.","Find the transformed equation and straight-line solutions.","$u+xu'=u^2$, so $xu'=u(u-1)$; $u=0,1$ give $y=0,x$.",["Product derivative","Retains lines"]),
                ("Separate the nonconstant branch","Integrate with partial fractions and apply data.","Find $u(x)$.","$\\ln|(u-1)/u|=\\ln x+C$; $u(1)=2$ gives $(u-1)/u=x/2$, hence $u=2/(2-x)$.",["Separates","Uses data"]),
                ("Return and restrict","Use $y=ux$ and find singular points.","Give the IVP solution and interval.","$y=2x/(2-x)$ on $(0,2)$; the interval respects $x>0$ and stops at the pole $x=2$.",["Back-substitutes","States interval"]),
            ]),
            example("we03","Riccati reduction as an extension","For $y'=y^2-1$, use the known solution $y_1=1$ and data $y(0)=0$.",[
                ("Subtract the known solution","Let $z=y-1$.","Derive the equation and data for $z$.","$z'=2z+z^2=z(z+2)$ and $z(0)=-1$.",["Substitutes","Transforms data"]),
                ("Solve the separable equation","Separate $z(z+2)$ and apply data.","Find $z$.","Integration gives $z=-2e^{2x}/(1+e^{2x})$ for the selected branch.",["Partial fractions","Uses branch"]),
                ("Return and verify","Add back $y_1$.","Give a simple final form and check it.","$y=1+z=(1-e^{2x})/(1+e^{2x})=-\\tanh x$; then $y'=-\\operatorname{sech}^2x=y^2-1$ and $y(0)=0$.",["Back-substitutes", "Verifies $-\\tanh x$"]),
            ]),
        ]),
        concept("ede-ch02-exactness-integrating-factors-depth-concept-lesson","ede-ch02-first-order-equations","Exactness and Integrating Factors: Structural Depth","Exactness identifies a hidden potential; integrating factors change a nonexact form into one while requiring careful domain bookkeeping.",[
            section("s1","Differential forms and potentials","If $F_x=M$ and $F_y=N$, then $Mdx+Ndy=dF$ and solution curves are level sets $F=C$. Either $y(x)$ or $x(y)$ may locally parameterize such a curve.",mc("q001","If $F=x^2+xy+y^2$, what are $M$ and $N$ in $dF=Mdx+Ndy$?",exact,[("a","$M=2x+y,\\ N=x+2y$"),("b","$M=x+2y,\\ N=2x+y$"),("c","$M=2x,\\ N=2y$"),("d","$M=N=x+y$")],"a","Partial differentiation gives the two coefficients.","method")),
            section("s2","Two reconstruction routes","Integrating $M$ with respect to $x$ leaves an unknown function of $y$; integrating $N$ with respect to $y$ leaves an unknown function of $x$. Either route must reproduce the other component.",mc("q002","After integrating $N=x+2y$ with respect to $y$, what form should $F$ have?",exact,[("a","$F=xy+y^2+h(x)$"),("b","$F=x^2+2xy+h(y)$"),("c","$F=x+2y+h(x)$"),("d","$F=xy+2y+h(y)$")],"a","Terms constant with respect to $y$ are represented by the unknown function $h(x)$.","method")),
            section("s3","Region hypotheses","The cross-partial test $M_y=N_x$ is applied on an open region where the components and required derivatives are continuous. Equality at one isolated point is not exactness on a region.",mc("q003","If $M_y=N_x$ only on the line $x=0$, what may be concluded?",exact,[("a","The form is not exact on any open rectangle solely from that line equality"),("b","It is exact everywhere"),("c","Every line is a solution"),("d","No derivatives exist")],"a","Exactness requires equality throughout the open region.","method")),
            section("s4","Diagnosing reconstruction failure","For a nonexact form, comparison after partial integration leaves a supposed one-variable derivative that still depends on the other variable. That contradiction identifies failure.",mc("q004","You obtain $h'(y)=4xy$. Why does reconstruction fail?",exact,[("a","A function of $y$ alone cannot have an $x$-dependent derivative"),("b","Partial derivatives cannot contain products"),("c","Every exact solution must be explicit"),("d","The constant must be zero")],"a","The missing term was assumed to depend only on $y$.","method")),
            section("s5","One-variable integrating factors","If $(M_y-N_x)/N$ depends only on $x$, exponentiate its $x$ integral for $\\mu(x)$. The analogous ratio $(N_x-M_y)/M$ yields $\\mu(y)$.",mc("q005","If $(M_y-N_x)/N=2/x$ on $x>0$, which factor is supported?",fac,[("a","$x^2$"),("b","$e^{2/x}$"),("c","$2\\ln x$"),("d","$y^2$")],"a","$e^{\\int2/x dx}=e^{2\\ln x}=x^2$.","factor")),
            section("s6","Product factors and exceptional solutions","Some forms admit $\\mu=P(x)Q(y)$. Multiplication is equivalent to the original equation only where $\\mu$ is defined and nonzero; excluded curves must be checked directly in the original equation.",mc("q006","Why must $y=0$ be checked separately after multiplying by $1/(x^2y^2)$?",fac,[("a","The factor is undefined there and may omit an original solution"),("b","Exact equations forbid zero"),("c","The derivative of zero is infinite"),("d","All integrating factors create PDEs")],"a","Division by a vanishing state can remove a valid solution branch.","factor")),
        ]),
        worked("ede-ch02-exactness-integrating-factors-depth-worked-examples","ede-ch02-first-order-equations","Exactness and Integrating Factors: Worked Examples",[
            example("we01","Reconstruct from the $dy$ component","Solve $(2x+y)dx+(x+2y)dy=0$ by integrating $N$ first.",[
                ("Test exactness","Compute cross partials.","Verify the form is exact.","$M_y=1=N_x$ on all of $\\mathbb R^2$.",["Computes cross partials","States region"]),
                ("Integrate $N$ first","Recover the missing function of $x$.","Construct $F$.","$F=xy+y^2+h(x)$; matching $F_x=y+h'(x)=2x+y$ gives $h=x^2$.",["Integrates N","Finds h"]),
                ("State and verify","Use a level set and both partials.","Give the implicit solution.","$x^2+xy+y^2=C$; its partial derivatives reproduce $M$ and $N$.",["Level set","Verifies components"]),
            ]),
            example("we02","A one-variable integrating factor","Solve $2y dx+x dy=0$ on $x>0$.",[
                ("Diagnose nonexactness","Calculate the ratio for an $x$ factor.","Find the supported ratio.","$M_y=2$, $N_x=1$, and $(M_y-N_x)/N=1/x$.",["Cross partials","Ratio depends on x"]),
                ("Multiply and solve","Use $\\mu=x$ and construct the potential.","Make the form exact.","Multiplication gives $2xy dx+x^2dy=d(x^2y)$.",["Finds factor","Recognizes differential"]),
                ("Verify equivalence","State the solution and domain.","Give the implicit family.","$x^2y=C$ on $x>0$; the factor is nonzero there, so the transformed and original forms are equivalent.",["Solution family","Domain check"]),
            ]),
            example("we03","A product factor and a lost curve","Analyze $y^2dx+x^2dy=0$ using $\\mu=1/(x^2y^2)$.",[
                ("Apply the product factor","Restrict to nonzero $x,y$.","Write the exact transformed form.","The result is $dx/x^2+dy/y^2=0$.",["Multiplies components","States restrictions"]),
                ("Integrate the exact form","Find its potential.","Give the implicit nonzero family.","$-1/x-1/y=C$ because the derivatives are $1/x^2$ and $1/y^2$.",["Integrates","Forms level set"]),
                ("Audit excluded curves","Return to the original equation.","Check whether $y=0$ was lost.","For $y(x)\\equiv0$, $y^2+x^2y'=0$, so it is an original solution omitted because the factor is undefined at $y=0$.",["Checks original","Identifies lost solution"]),
            ]),
        ]),
    ]


CHUNKS = {
 "ede-ch01-ode-readiness-concept-lesson": ["0017","0026","0028","0032"],
 "ede-ch01-ode-readiness-worked-examples": ["0026","0028","0032"],
 "ede-ch01-modeling-depth-concept-lesson": ["0017","0018","0019","0020","0021","0022","0023","0024","0025"],
 "ede-ch01-modeling-depth-worked-examples": ["0019","0021","0023","0024","0025"],
 "ede-ch01-solution-geometry-concept-lesson": ["0028","0032","0033","0037","0040"],
 "ede-ch01-solution-geometry-worked-examples": ["0028","0033","0037","0040"],
 "ede-ch02-linear-separable-depth-concept-lesson": ["0048","0052","0056","0058","0061","0063","0065","0070","0072","0076","0078"],
 "ede-ch02-linear-separable-depth-worked-examples": ["0056","0061","0065","0070","0076","0078"],
 "ede-ch02-existence-uniqueness-depth-concept-lesson": ["0082","0083","0085","0087","0089","0090"],
 "ede-ch02-existence-uniqueness-depth-worked-examples": ["0083","0085","0087","0089","0090"],
 "ede-ch02-nonlinear-transformations-depth-concept-lesson": ["0093","0095","0098","0104"],
 "ede-ch02-nonlinear-transformations-depth-worked-examples": ["0093","0095","0098","0104"],
 "ede-ch02-exactness-integrating-factors-depth-concept-lesson": ["0105","0108","0111","0114","0118","0120","0122","0126"],
 "ede-ch02-exactness-integrating-factors-depth-worked-examples": ["0108","0111","0122","0126","0128"],
}


def source_chunks(aid):
    return [f"{SRC}:chunk-{n}" for n in CHUNKS[aid]]


def objective_ids(doc):
    found=[]
    if doc["assessmentType"] == "conceptLesson":
        for s in doc["lesson"]["sections"]:
            for x in s["check"]["skills"]:
                if x not in found: found.append(x)
    else:
        # Focused mappings by module; chapter objectives are stable.
        aid=doc["id"]
        maps={
          "ode-readiness":["ede-ch01-introduction-calculus-readiness"],
          "modeling-depth":["ede-ch01-introduction-model-rate-laws","ede-ch01-introduction-model-types-assumptions"],
          "solution-geometry":["ede-ch01-introduction-classify-solutions","ede-ch01-introduction-initial-value-validity","ede-ch01-introduction-direction-fields"],
          "linear-separable":["ede-ch02-first-order-equations-linear-ivps","ede-ch02-first-order-equations-separable-equilibria"],
          "existence-uniqueness":["ede-ch02-first-order-equations-existence-uniqueness"],
          "nonlinear-transformations":["ede-ch02-first-order-equations-nonlinear-transformations"],
          "exactness-integrating":["ede-ch02-first-order-equations-exact-equations","ede-ch02-first-order-equations-integrating-factors"],
        }
        for key, vals in maps.items():
            if key in aid: found.extend(vals)
    return found


def write_assessments(docs):
    for doc in docs:
        path=ASSESS/f"{doc['id']}.yaml"
        path.write_text(yaml.dump(doc, Dumper=LiteralDumper, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")


def wire_media(docs):
    links={
      ("ede-ch01-ode-readiness-concept-lesson",2):("ch01-calculus-readiness-map.svg","Dependency map connecting domain checks, derivative rules, antiderivatives, initial data, and verification."),
      ("ede-ch01-modeling-depth-concept-lesson",0):("ch01-model-assumption-cycle.svg","Cycle from state and units through assumptions, a rate law, data comparison, and model revision."),
      ("ede-ch01-modeling-depth-concept-lesson",5):("ch01-equation-type-atlas.svg","Comparison of scalar, higher-order, coupled-system, and partial differential equation structures."),
      ("ede-ch01-solution-geometry-concept-lesson",1):("ch01-implicit-branch-domain.svg","Upper and lower implicit branches selected by initial data with singular endpoints marked."),
      ("ede-ch01-solution-geometry-concept-lesson",3):("ch01-direction-field-construction.svg","Workflow from sampled slopes to short field segments and tangent integral curves with undefined loci marked."),
      ("ede-ch02-linear-separable-depth-concept-lesson",2):("ch02-linear-variation-parameters.svg","Relationship among a complementary solution, variation of parameters, and its reciprocal integrating factor."),
      ("ede-ch02-existence-uniqueness-depth-concept-lesson",0):("ch02-existence-uniqueness-rectangles.svg","Open rectangle showing continuity regions, an initial point, and local existence and uniqueness conclusions."),
      ("ede-ch02-nonlinear-transformations-depth-concept-lesson",1):("ch02-nonlinear-transformation-map.svg","Decision map for Bernoulli, homogeneous nonlinear, translated-homogeneous, and Riccati substitutions."),
      ("ede-ch02-exactness-integrating-factors-depth-concept-lesson",4):("ch02-integrating-factor-families.svg","Integrating-factor families with exactness retesting and warnings about zeros and singularities."),
    }
    byid={d["id"]:d for d in docs}
    for (aid,index),(name,alt) in links.items():
        byid[aid]["lesson"]["sections"][index]["media"]=[{"type":"image","src":f"/media/ede/{name}","alt":alt,"caption":"Use the relationships in the diagram to select and verify the next step."}]


def write_manifests(docs):
    out=REF/"content-manifests"
    for doc in docs:
        data={"schemaVersion":1,"id":f"{doc['id']}-manifest","categoryId":CAT,"topicId":doc["topicId"],"assessmentId":doc["id"],"objectiveIds":objective_ids(doc),"sourceId":SRC,"sourceChunkIds":source_chunks(doc["id"]),"reviewState":"approved"}
        (out/f"{doc['id']}.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")


def make_blueprints(docs, chapter):
    path=REF/"question-blueprints"/f"ede-ch0{chapter}-{'introduction' if chapter==1 else 'first-order-equations'}-blueprints.json"
    bank=json.loads(path.read_text(encoding="utf-8"))
    new_ids={d["id"] for d in docs}
    bank["blueprints"]=[b for b in bank["blueprints"] if b.get("assessmentId") not in new_ids]
    for doc in docs:
        chunks=source_chunks(doc["id"]); objs=objective_ids(doc)
        records=[]
        if doc["assessmentType"]=="conceptLesson":
            for i,s in enumerate(doc["lesson"]["sections"],1):
                q=s["check"]; records.append((q["id"],q["type"],q["skills"][0],q["prompt"],s["title"],s["content"],q["explanation"],f"section-{i}"))
        else:
            for ei,e in enumerate(doc["workedExamples"],1):
                obj=objs[min(ei-1,len(objs)-1)]
                for si,s in enumerate(e["steps"],1):
                    records.append((s["id"],s["type"],obj,f"{e['problem']} {s['prompt']}",s["title"],s["instruction"],s["explanation"],f"example-{ei}-step-{si}"))
        for idx,(qid,qtype,obj,givens,title,method,expl,sig) in enumerate(records,1):
            bank["blueprints"].append({
              "id":f"{doc['id']}-{idx:03d}","objectiveId":obj,"assessmentId":doc["id"],"questionId":qid,"questionType":qtype,
              "sourceChunks":chunks,"reviewState":"approved","givens":givens,"unknown":title,
              "representationRequirement":"Use the module visual when it directly supports the geometric, modeling, or method-selection reasoning.",
              "governingPrinciple":method,"methodSteps":[method,f"Compute or justify the requested result: {title}.","Check the result against the original equation, data, and domain."],
              "misconception":f"A learner may choose an incompatible rule or omit the condition emphasized by {title}.",
              "difficultyEvidence":"Requires a governing relation, an executed calculation or classification, and an explicit verification.",
              "verification":expl.split("Why it works:")[0].replace("Solution:","").strip(),
              "variationAxes":["equation or model structure","requested representation",sig],
              "reasoningSignature":f"{doc['id']}::{qid}::{obj}::{sig}"
            })
    path.write_text(json.dumps(bank,indent=2)+"\n",encoding="utf-8")


def refresh_core_blueprints(chapter):
    topic="ede-ch01-introduction" if chapter==1 else "ede-ch02-first-order-equations"
    aid=f"{topic}-concept-lesson"
    assessment=yaml.safe_load((ASSESS/f"{aid}.yaml").read_text(encoding="utf-8"))
    path=REF/"question-blueprints"/f"{topic}-blueprints.json"
    bank=json.loads(path.read_text(encoding="utf-8"))
    sections={s["check"]["id"]:s for s in assessment["lesson"]["sections"]}
    for record in bank["blueprints"]:
        if record.get("assessmentId") != aid or record.get("questionId") not in sections:
            continue
        s=sections[record["questionId"]]; q=s["check"]
        record.update({
          "objectiveId":q["skills"][0],"givens":q["prompt"],"unknown":s["title"],
          "governingPrinciple":s["content"],
          "methodSteps":[f"Identify the structure required by {s['title']}.",f"Execute the calculation or classification requested in: {q['prompt']}","Verify the conclusion against the original equation and stated conditions."],
          "misconception":f"The learner may misapply the defining condition for {s['title']} or ignore its domain.",
          "verification":q["explanation"].split("Why it works:")[0].replace("Solution:","").strip(),
          "variationAxes":["equation structure","requested representation",s["id"]],
          "reasoningSignature":f"{aid}::{q['id']}::{q['skills'][0]}::{s['id']}-revised"
        })
    path.write_text(json.dumps(bank,indent=2)+"\n",encoding="utf-8")


def refresh_packets_and_core_manifests():
    c1={
      "ede-ch01-introduction-calculus-readiness":["0017","0026","0028","0032"],
      "ede-ch01-introduction-model-types-assumptions":["0017","0018","0024","0025","0030","0032"],
      "ede-ch01-introduction-model-rate-laws":["0017","0018","0019","0020","0021","0022","0023","0024"],
      "ede-ch01-introduction-classify-solutions":["0025","0026","0028","0030"],
      "ede-ch01-introduction-initial-value-validity":["0031","0032","0033","0034"],
      "ede-ch01-introduction-direction-fields":["0037","0040"],
    }
    c2={
      "ede-ch02-first-order-equations-linear-ivps":["0048","0052","0056","0058","0061","0063","0065"],
      "ede-ch02-first-order-equations-separable-equilibria":["0070","0072","0074","0076","0078"],
      "ede-ch02-first-order-equations-existence-uniqueness":["0082","0083","0085","0087","0089","0090"],
      "ede-ch02-first-order-equations-nonlinear-transformations":["0093","0095","0098","0104"],
      "ede-ch02-first-order-equations-exact-equations":["0105","0108","0111","0114"],
      "ede-ch02-first-order-equations-integrating-factors":["0118","0120","0122","0124","0126","0128"],
    }
    for topic,mapping in (("ede-ch01-introduction",c1),("ede-ch02-first-order-equations",c2)):
        p=REF/"packets"/f"packet-{topic}-v1.json"; packet=json.loads(p.read_text(encoding="utf-8"))
        existing={o["id"]:o for o in packet["objectives"]}
        ordered=[]
        for oid,nums in mapping.items():
            obj=existing.get(oid,{"id":oid}); obj["chunkIds"]=[f"{SRC}:chunk-{n}" for n in nums]; ordered.append(obj)
        packet["objectives"]=ordered; packet["reviewState"]="approved"
        p.write_text(json.dumps(packet,indent=2)+"\n",encoding="utf-8")
    core={
      "ede-ch01-introduction-concept-lesson":["0017","0025","0026","0028","0032","0033","0037","0040"],
      "ede-ch02-first-order-equations-concept-lesson":["0048","0052","0070","0076","0082","0083","0093","0095","0105","0108","0118","0122"],
    }
    for aid,nums in core.items():
        p=REF/"content-manifests"/f"{aid}.json"; data=json.loads(p.read_text(encoding="utf-8"))
        data["sourceChunkIds"]=[f"{SRC}:chunk-{n}" for n in nums]; data["reviewState"]="approved"
        p.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")


def refresh_curriculum():
    p=REF/"curriculum-manifests"/"elementary-differential-equations-bvp.yaml"
    data=json.loads(p.read_text(encoding="utf-8"))
    chapter=next(x for x in data["objectives"] if x["id"]=="ede-ch01-introduction-curriculum")
    additions=[
      {"id":"ede-ch01-introduction-calculus-readiness","title":"Apply prerequisite differentiation, integration, algebra, and domain skills when verifying or constructing ODE solutions.","prerequisiteIds":[],"requiredActivities":["conceptLesson","guidedWorkedExample"],"sourceIds":[SRC]},
      {"id":"ede-ch01-introduction-model-types-assumptions","title":"Distinguish scalar equations, systems, ODEs, PDEs, and model orders while stating assumptions and required initial data.","prerequisiteIds":["ede-ch01-introduction-calculus-readiness"],"requiredActivities":["conceptLesson","guidedWorkedExample"],"sourceIds":[SRC]},
    ]
    ids={x["id"] for x in chapter["objectives"]}
    chapter["objectives"]=[x for x in additions if x["id"] not in ids]+chapter["objectives"]
    p.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")


def release_manifest(chapter_docs, chapter):
    topic="ede-ch01-introduction" if chapter==1 else "ede-ch02-first-order-equations"
    rid="ede-ch01-foundations-supplemental-assessment-release" if chapter==1 else "ede-ch02-method-depth-supplemental-assessment-release"
    packet=f"packet-{topic}-v1"
    data={"schemaVersion":1,"id":rid,"categoryId":CAT,"topicId":topic,"areaId":"ede-foundations-first-order","packetId":packet,"releaseKind":"supplemental","publicationStatus":"published","sourceReviewState":"approved","artifacts":[]}
    for d in chapter_docs:
        count=6 if d["assessmentType"]=="conceptLesson" else 3
        data["artifacts"].append({"id":d["id"],"assessmentType":d["assessmentType"],"learningGoal":"learn","activityType":"conceptLesson" if d["assessmentType"]=="conceptLesson" else "guidedWorkedExample","objectiveIds":objective_ids(d),"plannedCount":count,"publicationStatus":"published"})
    path=REF/"assessment-release-manifests"/f"{rid.removesuffix('-assessment-release')}.json"
    path.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")


def svg_assets():
    MEDIA.mkdir(parents=True,exist_ok=True)
    assets={
      "ch01-calculus-readiness-map.svg":("ODE readiness","A dependency chain from domain checks through calculus and initial data to verification",'''<g font-family="Arial" font-size="18" text-anchor="middle">''' + ''.join(f'<rect x="{45+i*180}" y="115" width="150" height="64" rx="12" fill="#fff" stroke="#277da1" stroke-width="3"/><text x="{120+i*180}" y="153">{label}</text>' for i,label in enumerate(["Domain","Differentiate","Integrate","Apply data","Verify"])) + '''<g stroke="#555" stroke-width="3" fill="none"><path d="M195 147h25m155 0h25m155 0h25m155 0h25"/><path d="M215 140l10 7-10 7m180-14l10 7-10 7m180-14l10 7-10 7m180-14l10 7-10 7"/></g></g>'''),
      "ch01-model-assumption-cycle.svg":("Modeling cycle","A feedback cycle linking state variables, assumptions, rate laws, predictions, observations, and revision",'''<g font-family="Arial" font-size="17" text-anchor="middle"><circle cx="480" cy="155" r="92" fill="#fff" stroke="#277da1" stroke-width="3"/><text x="480" y="145">Model</text><text x="480" y="169">with units</text><g fill="#e7f4f8" stroke="#277da1" stroke-width="2"><rect x="70" y="55" width="180" height="50" rx="10"/><rect x="710" y="55" width="180" height="50" rx="10"/><rect x="710" y="215" width="180" height="50" rx="10"/><rect x="70" y="215" width="180" height="50" rx="10"/></g><text x="160" y="86">State + assumptions</text><text x="800" y="86">Rate law + data</text><text x="800" y="246">Prediction</text><text x="160" y="246">Observe and revise</text><g fill="none" stroke="#c65d32" stroke-width="4"><path d="M250 80C380 20 580 20 710 80"/><path d="M800 105v110"/><path d="M710 240C580 290 380 290 250 240"/><path d="M160 215V105"/></g></g>'''),
      "ch01-equation-type-atlas.svg":("Equation types","Four panels distinguish scalar, higher-order, coupled-system, and partial differential equation structures",'''<g font-family="Arial" text-anchor="middle"><g fill="#fff" stroke="#277da1" stroke-width="2"><rect x="35" y="75" width="205" height="145" rx="12"/><rect x="263" y="75" width="205" height="145" rx="12"/><rect x="491" y="75" width="205" height="145" rx="12"/><rect x="719" y="75" width="205" height="145" rx="12"/></g><g font-size="18" font-weight="700"><text x="138" y="110">Scalar ODE</text><text x="366" y="110">Higher order</text><text x="594" y="110">Coupled system</text><text x="822" y="110">PDE</text></g><g font-size="20"><text x="138" y="160">y' = f(t,y)</text><text x="366" y="160">y'' = -g</text><text x="594" y="150">P' = F(P,Q)</text><text x="594" y="180">Q' = G(P,Q)</text><text x="822" y="160">du/dt = k d2u/dx2</text></g></g>'''),
      "ch01-implicit-branch-domain.svg":("Implicit branches","A circle split into upper and lower function branches with an initial point and singular endpoints",'''<g transform="translate(480 155)"><path d="M-210 0a210 105 0 0 1 420 0" fill="none" stroke="#277da1" stroke-width="6"/><path d="M-210 0a210 105 0 0 0 420 0" fill="none" stroke="#8e5ea2" stroke-width="6"/><path d="M-260 0h520M0-125v250" stroke="#555" stroke-width="2"/><circle cx="125" cy="-84" r="8" fill="#c65d32"/><circle cx="-210" cy="0" r="7" fill="#d62828"/><circle cx="210" cy="0" r="7" fill="#d62828"/><g font-family="Arial" font-size="17"><text x="137" y="-95">initial point selects + branch</text><text x="-248" y="25">singular</text><text x="175" y="25">singular</text><text x="10" y="-108">y=+sqrt(a^2-x^2)</text><text x="10" y="104">y=-sqrt(a^2-x^2)</text></g></g>'''),
      "ch01-direction-field-construction.svg":("Direction field","Sampled slope segments for y prime equals x minus y, a zero-slope line, and a tangent solution trace",'''<g transform="translate(80 40)"><g stroke="#7a8a99" stroke-width="3">''' + ''.join(f'<path d="M{x-16} {y-s*16}L{x+16} {y+s*16}"/>' for x in range(80,801,120) for y in range(40,221,60) for s in [max(-1,min(1,(x/120-y/60)/3))]) + '''</g><path d="M35 215L805 25" stroke="#c65d32" stroke-width="3" stroke-dasharray="8 7"/><path d="M40 190C190 230 340 190 470 118S690 55 810 75" fill="none" stroke="#176b3a" stroke-width="6"/><g font-family="Arial" font-size="18"><text x="655" y="30">y=x: zero slopes</text><text x="580" y="118">integral curve stays tangent</text></g></g>'''),
      "ch02-linear-variation-parameters.svg":("Linear structure","A complementary solution connects variation of parameters to the reciprocal integrating factor",'''<g font-family="Arial" text-anchor="middle"><g fill="#fff" stroke="#277da1" stroke-width="3"><rect x="55" y="105" width="240" height="80" rx="14"/><rect x="360" y="105" width="240" height="80" rx="14"/><rect x="665" y="105" width="240" height="80" rx="14"/></g><g font-size="20"><text x="175" y="138">y1' + p y1 = 0</text><text x="175" y="166">known y1 != 0</text><text x="480" y="138">y = u y1</text><text x="480" y="166">solve for u</text><text x="785" y="138">mu = 1/y1</text><text x="785" y="166">(mu y)' = mu q</text></g><g stroke="#c65d32" stroke-width="4" fill="none"><path d="M295 145h65m240 0h65"/><path d="M345 136l15 9-15 9m305-18l15 9-15 9"/></g></g>'''),
      "ch02-existence-uniqueness-rectangles.svg":("Local theorem","An open rectangle around initial data avoids a singular line and distinguishes local from global conclusions",'''<g transform="translate(80 45)" font-family="Arial"><rect x="170" y="25" width="470" height="185" fill="#e7f4f8" stroke="#277da1" stroke-width="4" stroke-dasharray="10 7"/><path d="M675 0L790 230" stroke="#d62828" stroke-width="5"/><circle cx="390" cy="120" r="9" fill="#176b3a"/><path d="M315 135C355 95 430 90 505 125" fill="none" stroke="#176b3a" stroke-width="5"/><text x="405" y="145" font-size="18">(x0,y0)</text><text x="260" y="55" font-size="18">open rectangle: f and f_y continuous</text><text x="665" y="220" font-size="18" fill="#d62828">singular set avoided</text><text x="300" y="235" font-size="17">conclusion: unique on some local x-interval</text></g>'''),
      "ch02-nonlinear-transformation-map.svg":("Transformation map","A decision tree maps Bernoulli, homogeneous nonlinear, and known-solution Riccati forms to their substitutions",'''<g font-family="Arial" text-anchor="middle"><rect x="355" y="35" width="250" height="55" rx="12" fill="#fff" stroke="#277da1" stroke-width="3"/><text x="480" y="70" font-size="20">Recognize equation structure</text><g fill="#e7f4f8" stroke="#277da1" stroke-width="2"><rect x="40" y="185" width="250" height="70" rx="12"/><rect x="355" y="185" width="250" height="70" rx="12"/><rect x="670" y="185" width="250" height="70" rx="12"/></g><g font-size="18"><text x="165" y="214">Bernoulli y^n</text><text x="165" y="240">v=y^(1-n)</text><text x="480" y="214">q(y/x)</text><text x="480" y="240">y=u x; keep q(u)=u</text><text x="795" y="214">Riccati + known y1</text><text x="795" y="240">z=y-y1</text></g><g stroke="#c65d32" stroke-width="3"><path d="M480 90L165 185M480 90v95M480 90l315 95"/></g></g>'''),
      "ch02-integrating-factor-families.svg":("Integrating factors","A workflow branches to one-variable and product integrating factors before retesting exactness and auditing excluded curves",'''<g font-family="Arial" text-anchor="middle"><rect x="35" y="45" width="205" height="60" rx="12" fill="#fff" stroke="#277da1" stroke-width="3"/><text x="138" y="80" font-size="18">Mdx+Ndy nonexact</text><g fill="#e7f4f8" stroke="#277da1" stroke-width="2"><rect x="305" y="20" width="170" height="55" rx="10"/><rect x="305" y="90" width="170" height="55" rx="10"/><rect x="305" y="160" width="170" height="55" rx="10"/></g><text x="390" y="54" font-size="18">mu(x)</text><text x="390" y="124" font-size="18">mu(y)</text><text x="390" y="194" font-size="18">P(x)Q(y)</text><rect x="540" y="75" width="170" height="70" rx="12" fill="#fff" stroke="#277da1" stroke-width="3"/><text x="625" y="105" font-size="18">Multiply</text><text x="625" y="130" font-size="18">retest exactness</text><rect x="765" y="75" width="165" height="70" rx="12" fill="#fff1e8" stroke="#c65d32" stroke-width="3"/><text x="848" y="104" font-size="18">Audit mu=0</text><text x="848" y="130" font-size="18">or undefined</text><g stroke="#555" stroke-width="3"><path d="M240 75l65-28M240 75h65M240 75l65 112M475 48l65 55M475 118l65-8M475 188l65-55M710 110h55"/></g></g>'''),
    }
    for name,(title,subtitle,body) in assets.items():
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="300" viewBox="0 0 960 300" role="img" aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{subtitle}</desc><rect width="960" height="300" rx="24" fill="#f4f8fb"/>{body}</svg>'''
        (MEDIA/name).write_text(svg,encoding="utf-8")


def repair_core_lessons():
    fixes={
      # Prime marks inside YAML single-quoted scalars are intentionally doubled.
      # The existing equations already deserialize as first/second derivatives correctly.
      "ede-ch01-introduction-concept-lesson.yaml":[],
      "ede-ch02-first-order-equations-concept-lesson.yaml":[
          ("text: |-\n          No, because $M\n          e N$", "text: '$M\\ne N$'"),
          ("text: '$M\\ne N$'.", "text: '$M\\ne N$'"),
      ],
    }
    for name,pairs in fixes.items():
        p=ASSESS/name; text=p.read_text(encoding="utf-8")
        for old,new in pairs:
            if old in text:
                text=text.replace(old,new)
            elif new not in text:
                print(f"warning: neither repair token nor corrected text found in {name}: {old}")
        p.write_text(text,encoding="utf-8")


def main():
    c1=ch1_assessments(); c2=ch2_assessments(); docs=c1+c2
    repair_core_lessons(); wire_media(docs); write_assessments(docs); write_manifests(docs)
    make_blueprints(c1,1); make_blueprints(c2,2)
    refresh_core_blueprints(1); refresh_core_blueprints(2)
    refresh_packets_and_core_manifests(); refresh_curriculum()
    release_manifest(c1,1); release_manifest(c2,2); svg_assets()
    print(f"generated {len(docs)} assessments and {sum(6 if d['assessmentType']=='conceptLesson' else 9 for d in docs)} learner items")


if __name__ == "__main__":
    main()

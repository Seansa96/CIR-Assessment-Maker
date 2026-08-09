"""Generate the approved EDE Chapters 3-4 supplemental learning release.

All learner wording and vector media are original. Tracked provenance contains
only source-library chunk identifiers.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

import generate_ede_ch01_ch02_supplements as base

ROOT = Path(__file__).resolve().parents[1]
ASSESS = ROOT / "data" / "assessments"
REF = ROOT / "docs" / "assessment-reference"
MEDIA = ROOT / "frontend" / "public" / "media" / "ede"
CAT = "elementary-differential-equations-bvp"
AREA = "ede-numerical-first-order-applications"
SRC = "src-20260806084558-47ac4b59f9"

CH3 = "ede-ch03-numerical-methods"
CH4 = "ede-ch04-first-order-applications"

O = {
    "error": "ede-ch03-numerical-methods-error-step-size",
    "twostage": "ede-ch03-numerical-methods-two-stage-family",
    "rk4": "ede-ch03-numerical-methods-runge-kutta",
    "backward": "ede-ch03-numerical-methods-backward-integration",
    "semilinear": "ede-ch03-numerical-methods-semilinear-methods",
    "compare": "ede-ch03-numerical-methods-method-comparison",
    "growth": "ede-ch04-first-order-applications-growth-decay",
    "inference": "ede-ch04-first-order-applications-parameter-inference",
    "mixing": "ede-ch04-first-order-applications-cooling-mixing",
    "variablemix": "ede-ch04-first-order-applications-variable-volume-mixing",
    "mechanics": "ede-ch04-first-order-applications-mechanics",
    "drag": "ede-ch04-first-order-applications-nonlinear-resistance-escape",
    "autonomous": "ede-ch04-first-order-applications-autonomous-phase",
    "energy": "ede-ch04-first-order-applications-autonomous-second-order-energy",
    "damping": "ede-ch04-first-order-applications-damped-phase-trajectories",
    "curves": "ede-ch04-first-order-applications-curves",
    "curvefields": "ede-ch04-first-order-applications-geometric-curve-fields",
}

SIGNALS = {
    "localglobal": "ede-numerical-local-global-error",
    "order": "ede-numerical-convergence-order-error",
    "stage": "ede-numerical-stage-location-weight-error",
    "naming": "ede-numerical-method-naming-error",
    "cost": "ede-numerical-evaluation-cost-error",
    "semilinear": "ede-numerical-semilinear-transform-error",
    "backward": "ede-numerical-backward-time-sign-error",
    "quadrature": "ede-numerical-quadrature-rule-error",
    "parameter": "ede-model-parameter-inference-error",
    "units": "ede-model-rate-unit-error",
    "volume": "ede-mixing-changing-volume-error",
    "amount": "ede-mixing-amount-concentration-error",
    "drag": "ede-mechanics-resistance-branch-error",
    "terminal": "ede-mechanics-terminal-escape-error",
    "phase": "ede-autonomous-phase-variable-error",
    "direction": "ede-autonomous-trajectory-direction-error",
    "energy": "ede-autonomous-energy-conservation-error",
    "damping": "ede-autonomous-damping-energy-error",
    "branch": "ede-curves-lost-branch-envelope-error",
    "orthogonal": "ede-curves-orthogonal-slope-error",
}
base.SIGNALS.update(SIGNALS)


def media(name: str, alt: str) -> list[dict]:
    return [{"type": "image", "src": f"/media/ede/{name}", "alt": alt,
             "caption": "Use the relationships in the diagram to organize the calculation and verification."}]


def sec(i: int, title: str, content: str, check: dict, visual: tuple[str, str] | None = None) -> dict:
    return base.section(f"s{i}", title, content, check, media(*visual) if visual else None)


def mc(i: int, prompt: str, obj: str, choices: list[str], correct: int, solution: str, signal: str) -> dict:
    ids = ["a", "b", "c", "d"]
    return base.mc(f"q{i:03d}", prompt, obj, list(zip(ids, choices)), ids[correct], solution, signal)


def num(i: int, prompt: str, obj: str, value: float, solution: str, tolerance: float = .0001) -> dict:
    # YamlDotNet binds this field to decimal and does not accept exponent notation.
    return base.num(f"q{i:03d}", prompt, obj, value, solution, max(tolerance, .0001))


def sym(i: int, prompt: str, obj: str, answer: str, solution: str, variables=("x",)) -> dict:
    return base.sym(f"q{i:03d}", prompt, obj, answer, solution, variables)


def ex(eid: str, title: str, problem: str, setup: tuple[str, str, list[str]],
       compute: tuple[str, str, list[str]], verify: tuple[str, str, list[str]]) -> dict:
    rows = [
        ("Model or transform", "Identify the governing relation and preserve its assumptions.", setup[0], setup[1], setup[2]),
        ("Compute", "Carry out the indicated recurrence, integration, or algebra in an auditable order.", compute[0], compute[1], compute[2]),
        ("Verify and interpret", "Check the result against the equation, data, units, direction, or domain.", verify[0], verify[1], verify[2]),
    ]
    return base.example(eid, title, problem, rows)


def ch3_docs() -> list[dict]:
    docs: list[dict] = []
    docs.append(base.concept(
        "ede-ch03-error-convergence-depth-concept-lesson", CH3, "Numerical Error and Convergence in Depth",
        "Error analysis separates the defect made in one idealized step from the error accumulated along a computed trajectory.", [
        sec(1, "Local truncation error", "For a one-step rule $y_{n+1}=\\Phi_h(x_n,y_n)$, local truncation error compares one step started at the exact value with $y(x_n+h)$. It does not include errors inherited from earlier rows.",
            mc(1, "Which comparison defines a one-step local truncation error at $x_n$?", O["error"], ["Exact $y(x_n+h)$ versus one update begun at exact $y(x_n)$", "Exact $y(x_n)$ versus the initial datum", "Two numerical values from different endpoints", "The slope versus the step size"], 0, "Begin the numerical rule with exact current data and compare its next value with the exact next value.", "localglobal")),
        sec(2, "Taylor expansion for Euler", "Taylor's formula gives $y(x+h)=y(x)+hy'(x)+\\frac12h^2y''(\\xi)$. Euler retains the first two terms, so its one-step defect is proportional to $h^2$ when $y''$ is bounded.",
            num(2, "For $y'=y$, $y(0)=1$, Euler with $h=0.1$ gives $1.1$. Using $e^{0.1}=1.105170186$, find the absolute one-step defect.", O["error"], .005170186, "$|1.105170186-1.1|=0.005170186$.", 1e-8),
            ("ch03-error-propagation.svg", "One-step defects feeding an accumulated endpoint error along a numerical mesh.")),
        sec(3, "From local to global error", "Over a fixed interval, roughly $1/h$ steps accumulate and propagate local defects. Under stability and smoothness assumptions, Euler's $O(h^2)$ local error therefore produces $O(h)$ global error.",
            mc(3, "If Euler's global error is in its asymptotic range, what should halving $h$ approximately do?", O["error"], ["Halve the error", "Quarter the error", "Leave it unchanged", "Double the error"], 0, "First-order global error has the form $C h$, so replacing $h$ by $h/2$ halves it.", "order")),
        sec(4, "Assumptions behind an order claim", "An order statement needs more than a named method. The exact solution and required derivatives must remain bounded on the interval, stage evaluations must stay in the model domain, and the update must be stable enough not to amplify defects uncontrollably.",
            mc(4, "Which fact most directly supports the Taylor estimate for Euler's local error?", O["error"], ["$y''$ is bounded on the step", "$y$ is positive at one point", "The interval contains an integer", "The step count is even"], 0, "A bound on the omitted second-derivative term controls the Taylor remainder.", "order")),
        sec(5, "Step halving and empirical order", "For errors $E_h\\approx C h^p$, the ratio $E_h/E_{h/2}\\approx2^p$. Thus $p\\approx\\log_2(E_h/E_{h/2})$ when both computations are in the asymptotic regime and use the same endpoint and reference.",
            num(5, "Errors are $0.032$ for $h$ and $0.008$ for $h/2$. Estimate the observed order $p$.", O["error"], 2, "$E_h/E_{h/2}=4=2^2$, so $p=2$.", 1e-8)),
        sec(6, "Accuracy, roundoff, and cost", "Smaller steps reduce truncation error but require more evaluations and more floating-point operations. Eventually roundoff and cancellation may dominate, so a defensible comparison reports endpoint error, evaluation count, and arithmetic precision.",
            mc(6, "Which report supports the fairest method comparison?", O["compare"], ["Same IVP and endpoint, reference error, evaluations, and precision", "Only the number of steps", "Errors at different endpoints", "Only the method names"], 0, "Accuracy and work must be measured on the same task with the same numerical precision.", "cost")),
    ]))
    docs.append(base.worked("ede-ch03-error-convergence-depth-worked-examples", CH3, "Numerical Error and Convergence: Worked Examples", [
        ex("we01", "Euler's one-step defect", "Analyze one Euler step for $y'=y$, $y(0)=1$, with step $h$.",
           ("Write the exact and Euler next values.", "$y(h)=e^h$ and $Y_1=1+h$.", ["exact value", "Euler update"]),
           ("Expand the difference.", "$e^h-(1+h)=h^2/2+h^3/6+\\cdots$, so the leading local defect is $h^2/2$.", ["Taylor expansion", "leading term"]),
           ("Confirm the order and sign.", "The ratio of the defect to $h^2$ tends to $1/2$, and the positive defect agrees with the convex exact curve lying above its tangent.", ["order check", "curvature interpretation"])),
        ex("we02", "A step-halving table", "Use Euler for $y'=y$, $y(0)=1$ to approximate $y(1)$ with $h=0.5$ and $h=0.25$.",
           ("Write the repeated update.", "$Y_N=(1+h)^N$ with $N=1/h$.", ["recurrence", "common endpoint"]),
           ("Compute both approximations and errors.", "$Y_2=2.25$, $E_{0.5}=0.468282$; $Y_4=2.44140625$, $E_{0.25}=0.276876$ using $e=2.718282$.", ["two approximations", "two errors"]),
           ("Interpret the ratio.", "$E_{0.5}/E_{0.25}\\approx1.69$; it is moving toward the first-order asymptotic ratio $2$ but coarse steps are not yet fully asymptotic.", ["ratio", "qualified conclusion"])),
        ex("we03", "Accuracy per evaluation", "Compare Euler with $h=0.1$ and RK4 with $h=0.5$ on a unit interval.",
           ("Count work before comparing error.", "Euler uses $10$ evaluations; two RK4 steps use $2\\times4=8$ evaluations.", ["Euler cost", "RK4 cost"]),
           ("Use supplied common-endpoint errors.", "If the errors are $1.2\\times10^{-2}$ and $3.0\\times10^{-4}$, RK4 is both cheaper by this count and more accurate in this run.", ["same endpoint", "reference errors"]),
           ("State the limited conclusion.", "The comparison applies to this IVP, interval, implementation, and precision; it is not a universal timing theorem.", ["assumptions", "no overgeneralization"])),
    ]))

    docs.append(base.concept(
        "ede-ch03-two-stage-methods-depth-concept-lesson", CH3, "Two-Stage Methods and Quadrature",
        "Second-order two-stage rules differ in stage location and weighting even when they share the same formal order.", [
        sec(1, "A general two-stage rule", "Let $k_1=f(x_n,y_n)$, $k_2=f(x_n+\\theta h,y_n+\\theta h k_1)$, and update $y_{n+1}=y_n+h(\\sigma k_1+\\rho k_2)$. The parameters specify both where the second slope is sampled and how the slopes are combined.",
            mc(1, "In the general two-stage rule, what does $\\theta$ control?", O["twostage"], ["The second stage's location and predicted state", "The number of unknown functions", "The exact solution", "The initial condition"], 0, "$\\theta$ places the second stage at $x_n+\\theta h$ and advances its predicted state by the same fraction.", "stage"),
            ("ch03-two-stage-family.svg", "Stage locations and weights for endpoint-average, source-defined Heun, and midpoint methods.")),
        sec(2, "Second-order conditions", "Matching the Taylor expansion through terms of order $h^2$ requires $\\sigma+\\rho=1$ and $\\rho\\theta=1/2$. These conditions create a family rather than one unique method.",
            mc(2, "Which parameter choice satisfies both second-order conditions?", O["twostage"], ["$\\rho=1$, $\\theta=1/2$, $\\sigma=0$", "$\\rho=1$, $\\theta=1$, $\\sigma=1$", "$\\rho=0$, $\\theta=1/2$, $\\sigma=1$", "$\\rho=1/2$, $\\theta=1/2$, $\\sigma=1/2$"], 0, "$0+1=1$ and $1(1/2)=1/2$.", "stage")),
        sec(3, "Endpoint-average Improved Euler", "The endpoint-average rule uses $\\theta=1$ and $\\sigma=\\rho=1/2$. It predicts an endpoint with Euler, evaluates the endpoint slope there, and averages the two slopes. It is also called explicit trapezoid and is often called Heun's method outside this source.",
            num(3, "For $y'=y^2$, $y_0=1$, $h=0.2$, endpoint-average Improved Euler uses slopes $1$ and $1.44$. Find $y_1$.", O["twostage"], 1.244, "$y_1=1+0.2(1+1.44)/2=1.244$.", 1e-8)),
        sec(4, "Source-defined Heun and midpoint", "The source calls $\\theta=2/3$, $\\sigma=1/4$, $\\rho=3/4$ Heun's method. Midpoint uses $\\theta=1/2$, $\\sigma=0$, $\\rho=1$. Naming conventions vary, so formulas—not labels—must determine the stages.",
            mc(4, "Which description matches the source-defined Heun rule?", O["twostage"], ["Sample at $2h/3$ and weight slopes $1/4,3/4$", "Sample only at the start", "Sample at $h/2$ and discard that slope", "Average exact endpoint values"], 0, "The source-defined Heun parameters are $\\theta=2/3$, $\\sigma=1/4$, and $\\rho=3/4$.", "naming")),
        sec(5, "Geometry and evaluation cost", "Every explicit two-stage rule uses two evaluations per step. A fair comparison therefore distinguishes step count from evaluation count and plots the actual stage location rather than treating the second slope as an endpoint slope in every method.",
            num(5, "How many evaluations of $f$ are used by 12 steps of an explicit two-stage method?", O["compare"], 24, "$12\\times2=24$ evaluations.", 0)),
        sec(6, "Quadrature as a special IVP", "When $y'=g(x)$, Euler accumulates left rectangles. Endpoint-average Improved Euler accumulates trapezoids because its two slopes are $g(x_n)$ and $g(x_{n+1})$.",
            num(6, "Apply one endpoint-average step to $y'=x^2$, $y(0)=0$, with $h=0.5$.", O["twostage"], .0625, "$y_1=0+0.5[0^2+0.5^2]/2=0.0625$.", 1e-8),
            ("ch03-ode-quadrature-connection.svg", "Euler rectangles and endpoint-average trapezoids viewed as numerical IVP updates.")),
    ]))
    docs.append(base.worked("ede-ch03-two-stage-methods-depth-worked-examples", CH3, "Two-Stage Methods and Quadrature: Worked Examples", [
        ex("we01", "Three second-order updates", "For $y'=y^2$, $y(0)=1$, take one step with $h=0.2$ using three two-stage rules.",
           ("Compute the common first slope.", "$k_1=1$. Endpoint-average predicts $1.2$; source-Heun predicts $1+\\frac23(0.2)=1.133333$; midpoint predicts $1.1$.", ["three stage states", "common k1"]),
           ("Evaluate and weight the second slopes.", "The results are $1.244$ (endpoint-average), $1.242667$ (source-Heun), and $1.242$ (midpoint).", ["correct locations", "correct weights"]),
           ("Compare with the exact value.", "The exact solution $1/(1-x)$ gives $1.25$ at $x=0.2$; all three undershoot, with different errors despite sharing second order.", ["reference", "distinct errors"])),
        ex("we02", "The trapezoid connection", "Interpret endpoint-average Improved Euler for $y'=x^2$, $y(0)=0$ on $[0,1]$ with $h=0.5$.",
           ("Identify the quadrature data.", "The slopes are $g(0)=0$, $g(0.5)=0.25$, and $g(1)=1$.", ["mesh", "slope values"]),
           ("Add two trapezoids.", "$Y_2=\\frac{0.5}{2}[0+2(0.25)+1]=0.375$.", ["composite trapezoid", "value"]),
           ("Check against integration.", "$\\int_0^1x^2dx=1/3$, so the error is $0.041667$ and is positive because the function is convex.", ["exact integral", "error sign"])),
        ex("we03", "Equal evaluation budgets", "Compare Euler and midpoint with a budget of four evaluations on $[0,1]$.",
           ("Translate budget into step sizes.", "Euler can take four steps, $h=0.25$; midpoint can take two steps, $h=0.5$.", ["evaluation count", "step sizes"]),
           ("Apply both to the stated IVP.", "For $y'=x$, $y(0)=0$, Euler gives $0.375$ while midpoint gives $0.5$.", ["Euler sum", "midpoint sum"]),
           ("Use the exact reference.", "$y(1)=1/2$, so midpoint is exact for this linear integrand while Euler has error $0.125$.", ["exact value", "fair comparison"])),
    ]))

    docs.append(base.concept(
        "ede-ch03-rk4-backward-depth-concept-lesson", CH3, "RK4 and Backward Integration",
        "RK4 accuracy depends on evaluating each intermediate state correctly and respecting the direction of integration.", [
        sec(1, "Four linked RK stages", "Classical RK4 uses $k_1$ at the start, $k_2$ and $k_3$ at successively predicted midpoint states, and $k_4$ at the predicted endpoint. Reusing $y_n$ at a later stage destroys the method.",
            mc(1, "Which state is used for $k_3$?", O["rk4"], ["$y_n+h k_2/2$", "$y_n$", "$y_n+h k_1$", "$y_n+h k_4$"], 0, "$k_3=f(x_n+h/2,y_n+h k_2/2)$.", "stage"),
            ("ch03-rk4-stage-geometry.svg", "The four RK4 stage states and their weighted combination.")),
        sec(2, "State dependence matters", "For $f(x,y)$, each stage changes both the evaluation point and the provisional state. Only for $f(x)$ alone do the state predictions disappear from the slope evaluations.",
            mc(2, "For which equation do RK4 stage states not affect slope values?", O["rk4"], ["$y'=\\sin x$", "$y'=x+y$", "$y'=y^2$", "$y'=xy$"], 0, "$f(x)=\\sin x$ does not depend on the provisional value of $y$.", "stage")),
        sec(3, "Multi-step RK4 tables", "After each weighted update, the new $(x_{n+1},y_{n+1})$ becomes the start of the next four-stage calculation. A table should store stages separately and must not round them prematurely.",
            num(3, "For $y'=y$, one RK4 step of size $0.2$ multiplies the state by $1.2214$. Starting from $1$, what is the two-step value using this rounded multiplier?", O["rk4"], 1.49181796, "$1.2214^2=1.49181796$.", 1e-8)),
        sec(4, "Fourth-order refinement", "For a fixed endpoint in the asymptotic regime, RK4 global error behaves like $C h^4$. Halving $h$ should reduce the error by about $2^4=16$.",
            num(4, "An RK4 endpoint error is $0.0016$ for $h$. Predict its asymptotic error for $h/2$.", O["rk4"], .0001, "$0.0016/16=0.0001$.", 1e-9)),
        sec(5, "Backward steps", "A one-step method can integrate from right to left by using $h<0$. The stage formulas are unchanged; the negative step moves every stage and the final update in the decreasing-$x$ direction.",
            num(5, "Use one backward Euler step for $y'=y$ from $(1,e)$ with $h=-0.1$. Using $e=2.7182818$, find the estimate at $0.9$.", O["backward"], 2.44645362, "$e+(-0.1)e=0.9e=2.44645362$.", 1e-8)),
        sec(6, "A forward-time transformation", "With a reflected independent variable, a right-end IVP can be rewritten for forward stepping. If $z(s)=y(-s)$, then $z'(s)=-f(-s,z)$; both the reflected input and the minus sign must be retained.",
            mc(6, "If $y'=x+y$ and $z(s)=y(-s)$, which equation does $z$ satisfy?", O["backward"], ["$z'=s-z$", "$z'=-s-z$", "$z'=s+z$", "$z'=-s+z$"], 0, "$z'=-f(-s,z)=-(-s+z)=s-z$.", "backward"),
            ("ch03-backward-integration.svg", "A right-end initial value reflected into a forward-stepping transformed problem.")),
    ]))
    docs.append(base.worked("ede-ch03-rk4-backward-depth-worked-examples", CH3, "RK4 and Backward Integration: Worked Examples", [
        ex("we01", "A nonlinear RK4 step", "Use RK4 on $y'=x+y$, $y(0)=1$, with $h=0.2$.",
           ("Compute the four slopes.", "$k_1=1$, $k_2=1.2$, $k_3=1.22$, and $k_4=1.444$.", ["four stages", "updated states"]),
           ("Apply the weighted update.", "$Y_1=1+\\frac{0.2}{6}(1+2(1.2)+2(1.22)+1.444)=1.2428$.", ["weights", "value"]),
           ("Compare with the exact solution.", "$y=2e^x-x-1$ gives $1.242805516$ at $0.2$, so the absolute error is about $5.52\\times10^{-6}$.", ["exact check", "error"])),
        ex("we02", "Two RK4 rows", "Apply two RK4 steps of size $0.2$ to $y'=y$, $y(0)=1$.",
           ("Form the RK4 multiplier.", "For this linear equation the step multiplier is $R=1+h+h^2/2+h^3/6+h^4/24=1.2214$.", ["stability polynomial", "h=0.2"]),
           ("Advance two rows.", "$Y_1=1.2214$ and $Y_2=1.2214^2=1.49181796$.", ["row one", "row two"]),
           ("Check the endpoint.", "$e^{0.4}=1.491824698$, giving absolute error about $6.74\\times10^{-6}$.", ["endpoint", "reference error"])),
        ex("we03", "Right-to-left integration", "Approximate $y(0.5)$ for $y'=y$, given $y(1)=e$, using one RK4 step $h=-0.5$.",
           ("Respect the negative step in all stages.", "$k_1=e$, $k_2=0.75e$, $k_3=0.8125e$, and $k_4=0.59375e$.", ["negative h", "four states"]),
           ("Combine the slopes.", "$Y= e-\\frac{0.5e}{6}[1+2(0.75)+2(0.8125)+0.59375]=0.606770833e\\approx1.649374$.", ["weighted sum", "backward value"]),
           ("Verify direction and accuracy.", "The endpoint is $0.5$ and the exact value $e^{0.5}\\approx1.648721$, so the method moved left and erred by about $6.53\\times10^{-4}$.", ["left endpoint", "exact check"])),
    ]))

    docs.append(base.concept(
        "ede-ch03-semilinear-methods-depth-concept-lesson", CH3, "Semilinear Numerical Methods",
        "A known complementary solution can absorb the linear part before a numerical method advances the remaining nonlinear factor.", [
        sec(1, "Recognize semilinear structure", "A semilinear first-order equation has the form $y'+p(x)y=h(x,y)$. The coefficient term is linear in $y$ even though the right side may be nonlinear.",
            mc(1, "Which equation is in semilinear form?", O["semilinear"], ["$y'+xy=y^2$", "$yy'=x$", "$y''+y=0$", "$y'=\\sin x$ with no identified linear part"], 0, "The first equation explicitly separates the linear term $xy$ from the nonlinear term $y^2$.", "semilinear")),
        sec(2, "Use a complementary solution", "Choose a nonzero $y_1$ satisfying $y_1'+p(x)y_1=0$. This factor captures the homogeneous linear behavior on an interval where it does not vanish.",
            sym(2, "Give a nonzero complementary solution of $y'+2y=0$.", O["semilinear"], "e^{-2x}", "$y_1=e^{-2x}$ satisfies $y_1'+2y_1=0$.", ("x",))),
        sec(3, "Transform with $y=u y_1$", "Substitution gives $y'+py=u'y_1$ because the terms involving $y_1'+py_1$ cancel. The transformed equation is $u'=h(x,u y_1)/y_1$.",
            mc(3, "For $y'+y=y^2$ and $y=u e^{-x}$, what equation does $u$ satisfy?", O["semilinear"], ["$u'=u^2e^{-x}$", "$u'=u^2e^x$", "$u'=-u$", "$u'=e^{-x}$"], 0, "$u'e^{-x}=u^2e^{-2x}$, so $u'=u^2e^{-x}$.", "semilinear"),
            ("ch03-semilinear-transform.svg", "A semilinear equation factored into complementary linear behavior and a transformed numerical state.")),
        sec(4, "Advance the transformed state", "Apply Euler or a two-stage rule to $u'=H(x,u)$, then reconstruct $y_n=u_n y_1(x_n)$. Comparing only $u$ values with direct $y$ values is meaningless; both must be expressed in the original variable.",
            num(4, "For $u'=u^2e^{-x}$, $u(0)=0.5$, one Euler step with $h=0.2$ gives $u_1=0.55$. Find reconstructed $y_1=0.55e^{-0.2}$.", O["semilinear"], .450302, "$0.55e^{-0.2}\\approx0.450302$.", 1e-6)),
        sec(5, "Extend the method to RK4", "The same transformation can be combined with RK4. All four stages evaluate the transformed right side $H(x,u)$, and reconstruction occurs at the updated mesh point.",
            mc(5, "In semilinear RK4, which function should the four stages evaluate?", O["semilinear"], ["The transformed right side $H(x,u)$", "Only $p(x)$", "The exact solution $y(x)$", "The initial condition repeatedly"], 0, "RK4 advances the transformed IVP, so its stages use $H(x,u)$.", "semilinear")),
        sec(6, "Equivalence and domain warnings", "The transformation is valid only where the chosen $y_1$ is nonzero and all terms are defined. A transformed method may improve accuracy when it captures dominant linear behavior, but it is not automatically superior on every equation or interval.",
            mc(6, "What must be checked before claiming the transformed and original IVPs are equivalent?", O["semilinear"], ["$y_1$ is nonzero and both right sides are defined on the interval", "The step size is an integer", "The nonlinear term vanishes", "Euler is exact"], 0, "Division by $y_1$ and every transformed evaluation require a common valid interval.", "semilinear")),
    ]))
    docs.append(base.worked("ede-ch03-semilinear-methods-depth-worked-examples", CH3, "Semilinear Numerical Methods: Worked Examples", [
        ex("we01", "Direct versus semilinear Euler", "For $y'+y=y^2$, $y(0)=0.5$, compare one direct and transformed Euler step with $h=0.2$.",
           ("Build both update equations.", "Directly, $y'=-y+y^2$; with $y=u e^{-x}$, $u'=u^2e^{-x}$ and $u(0)=0.5$.", ["direct RHS", "transformed RHS"]),
           ("Advance and reconstruct.", "Direct Euler gives $0.45$. Transformed Euler gives $u_1=0.55$ and $y_1=0.55e^{-0.2}\\approx0.450302$.", ["two updates", "reconstruction"]),
           ("Compare to the exact value.", "The separable exact solution gives $y(0.2)\\approx0.450166$; transformed Euler is closer in this step, without proving universal superiority.", ["reference", "qualified comparison"])),
        ex("we02", "Transformed Improved Euler", "Use endpoint-average Improved Euler on the transformed IVP $u'=u^2e^{-x}$, $u(0)=0.5$, $h=0.2$.",
           ("Predict the endpoint.", "$H(0,0.5)=0.25$, so $u^*=0.55$.", ["first slope", "predictor"]),
           ("Correct and reconstruct.", "$H(0.2,0.55)\\approx0.247642$; hence $u_1\\approx0.549764$ and $y_1=u_1e^{-0.2}\\approx0.450111$.", ["endpoint slope", "corrected u", "reconstructed y"]),
           ("Check the gain and domain.", "The exact value is about $0.450166$, so the error is about $5.5\\times10^{-5}$; $e^{-x}$ is nonzero on the step.", ["error", "nonzero factor"])),
        ex("we03", "Semilinear RK4 as quadrature", "For $y'+2y=\\sin x$, $y(0)=0$, transform and take one RK4 step of size $0.2$.",
           ("Remove the linear part.", "With $y=u e^{-2x}$, $u'=e^{2x}\\sin x$ and $u(0)=0$.", ["complementary factor", "transformed equation"]),
           ("Apply RK4 to $u$.", "Using the four values of $e^{2x}\\sin x$ at $0,0.1,0.1,0.2$ gives $u(0.2)\\approx0.0261376$.", ["four transformed stages", "u update"]),
           ("Reconstruct and verify scale.", "$y(0.2)\\approx0.0261376e^{-0.4}=0.0175205$; the integral formula $e^{-2x}\\int_0^xe^{2s}\\sin s\\,ds$ gives about $0.0175184$.", ["reconstruction", "integral check"])),
    ]))
    return docs


def ch4_docs() -> list[dict]:
    docs: list[dict] = []
    modules = []
    modules.append(base.concept("ede-ch04-growth-input-inference-depth-concept-lesson", CH4, "Growth, Decay, Input, and Parameter Inference", "Rate constants become meaningful only after measurements, units, and model assumptions are connected.", [
        sec(1,"Infer an exponential parameter","For $Q'=kQ$, two measurements give $Q(t_2)/Q(t_1)=e^{k(t_2-t_1)}$. Ratios remove the unknown scale and determine $k$ with inverse-time units.",num(1,"A quantity grows from 20 to 30 in 5 hours. Find $k$ in $Q'=kQ$.",O["inference"],.081093,"$k=\\ln(30/20)/5\\approx0.081093$ h$^{-1}$.",1e-6),("ch04-parameter-inference.svg","Measurements determining an exponential rate and a production-removal equilibrium.")),
        sec(2,"Doubling time and half-life","If $k>0$, doubling time is $\\ln2/k$. If $k<0$, half-life is $\\ln2/|k|$. The sign belongs to the differential equation, not to the time interval.",num(2,"A decay constant is $k=-0.035$ day$^{-1}$. Find the half-life in days.",O["inference"],19.8042,"$t_{1/2}=\\ln2/0.035\\approx19.8042$ days.",.001)),
        sec(3,"Reverse-time questions","An exponential model is algebraically reversible: $Q(0)=Q(T)e^{-kT}$. Interpreting a past value still requires the same constant-rate assumptions to have held throughout the interval.",num(3,"An account grows continuously at $4\\%$ per year and is worth $5000$ after 6 years. Find its present value.",O["inference"],3933.14,"$5000e^{-0.04(6)}\\approx3933.14$.",.01)),
        sec(4,"Production with proportional removal","For $Q'=a-kQ$ with $a,k>0$, the equilibrium is $Q_*=a/k$ and $Q=Q_*+(Q_0-Q_*)e^{-kt}$. The transient sign shows whether the state rises or falls toward the limit.",num(4,"For $Q'=12-0.3Q$, find the equilibrium value.",O["growth"],40,"$Q_*=12/0.3=40$.",0)),
        sec(5,"Continuous deposits","A continuously deposited amount obeys $A'=rA+d$. Its solution separates growth of the initial principal from accumulated deposits. The model differs from periodic deposits made at discrete times.",sym(5,"Solve $A'=0.05A+1000$, $A(0)=0$.",O["growth"],"20000(e^{0.05t}-1)","The equilibrium-form solution gives $A=20000(e^{0.05t}-1)$.",( "t",))),
        sec(6,"Assumptions and observations","A fitted exponential does not by itself validate constant environment, unlimited resources, continuous compounding, or unchanged production. Residuals and mechanism checks decide whether extrapolation is defensible.",mc(6,"Which observation most directly challenges constant proportional growth?",O["growth"],["The estimated rate falls systematically as the state grows","The state remains positive","Time is measured in days","Two measurements agree exactly"],0,"A rate that changes with state contradicts a constant proportional-rate parameter.","parameter")),
    ]))
    modules.append(base.worked("ede-ch04-growth-input-inference-depth-worked-examples",CH4,"Growth and Parameter Inference: Worked Examples",[
        ex("we01","Dating by radioactive decay","A sample retains 35% of its original isotope; the half-life is 5730 years.",( "Convert half-life to a decay constant.","$k=-\\ln2/5730$ yr$^{-1}$.",["negative k","units"]),("Solve the fraction equation.","$0.35=e^{kt}$ gives $t=\\ln(0.35)/k\\approx8678$ years.",["fraction","logarithm"]),("State the assumption.","The age estimate assumes the initial ratio and decay rate were valid and the sample remained closed.",["model assumption","positive time"])),
        ex("we02","Production and removal","A tracer obeys $Q'=8-0.2Q$, $Q(0)=10$.",( "Find the equilibrium and transient form.","$Q_*=40$ and $Q=40+Ce^{-0.2t}$.",["equilibrium","transient"]),("Apply the initial value.","$C=-30$, so $Q=40-30e^{-0.2t}$.",["constant","solution"]),("Verify behavior.","$Q'=6e^{-0.2t}=8-0.2Q$, $Q(0)=10$, and $Q\\to40$.",["ODE","initial value","limit"])),
        ex("we03","Continuous versus annual deposits","Compare continuous deposits at $1200$ dollars/year with $100$ deposited at each month-end, using a stated $6\\%$ continuous rate for one year.",( "Write both models.","Continuous: $A'=0.06A+1200$. Discrete: sum twelve deposits with their remaining growth times.",["two models","timing distinction"]),("Compute the continuous result.","$A_c=20000(e^{0.06}-1)\\approx1236.73$ dollars.",["solution","value"]),("Interpret rather than equate them.","The monthly model is a geometric sum and differs because deposits do not enter continuously; either comparison must use a declared timing convention.",["model distinction","units"])),
    ]))

    modules.append(base.concept("ede-ch04-cooling-variable-mixing-depth-concept-lesson",CH4,"Cooling and Variable-Volume Mixing","Cooling and mixing are both balance models, but their parameters, state variables, and validity intervals differ.",[
        sec(1,"Infer a cooling constant","For constant ambient temperature $T_a$, $T-T_a=(T_0-T_a)e^{-kt}$. A measurement of excess-temperature ratio determines $k$.",num(1,"A body cools from $90$ to $55$ C in a $20$ C room in 10 min. Find $k$.",O["inference"],.0693147,"The excess halves: $35/70=1/2=e^{-10k}$, so $k=\\ln2/10$.",1e-6)),
        sec(2,"Infer an event time","Once $k$ is known, a measured temperature can be solved backward for elapsed time. The ambient shift must occur before taking logarithms.",num(2,"With $T=20+70e^{-0.0693147t}$, when is $T=37.5$ C?",O["inference"],20,"The excess ratio is $17.5/70=1/4$, which takes two half-lives of 10 min.",.001)),
        sec(3,"Amount versus concentration","If $Q(t)$ is solute amount and $V(t)$ is volume, the well-mixed concentration is $Q/V$. Outflow amount rate is volumetric flow times this concentration.",mc(3,"A tank contains $Q$ grams in $V$ liters and drains at 3 L/min. What is the solute outflow rate?",O["mixing"],["$3Q/V$ grams/min","$Q/3V$ grams/min","$3Q$ liters/min","$V/3Q$ grams/min"],0,"Flow times concentration is $3(Q/V)$ grams per minute.","amount"),("ch04-variable-volume-tank.svg","A changing-volume tank with separate amount, concentration, inflow, outflow, and capacity labels.")),
        sec(4,"Build the signed balance","The governing equation is $Q'=$ solute inflow rate minus solute outflow rate. Every term must have amount-per-time units and the outflow concentration is the current tank concentration.",mc(4,"Brine enters at 4 L/min and 1 g/L; mixture leaves at 2 L/min. Which input term belongs in $Q'$?",O["mixing"],["$4$ g/min","$1/4$ g/min","$2Q/V$ g/min","$4V$ g/min"],0,"The incoming amount rate is $(4\\text{ L/min})(1\\text{ g/L})=4$ g/min.","units")),
        sec(5,"Changing volume","Unequal volumetric rates give $V(t)=V_0+(r_{in}-r_{out})t$. This expression must replace a frozen initial volume in the outflow term.",mc(5,"A 50-L tank has 4 L/min entering and 2 L/min leaving. What is $V(t)$?",O["variablemix"],["$50+2t$","$50-2t$","$50+6t$","$50$"],0,"The net volume rate is $4-2=2$ L/min.","volume")),
        sec(6,"Capacity and validity","A mathematical solution may continue after a physical tank overflows or empties. The maximal model interval ends at the first capacity, emptying, or assumption failure.",num(6,"The tank volume is $50+2t$ L and capacity is 100 L. Find the first overflow time in minutes.",O["variablemix"],25,"Solve $50+2t=100$ to get $t=25$ min.",0)),
    ]))
    modules.append(base.worked("ede-ch04-cooling-variable-mixing-depth-worked-examples",CH4,"Cooling and Variable-Volume Mixing: Worked Examples",[
        ex("we01","Cooling from two observations","A sample is 90 C when placed in a 20 C room and is 55 C after 10 min.",( "Shift by ambient temperature.","$T-20=70e^{-kt}$.",["ambient shift","initial excess"]),("Infer the parameter.","$35=70e^{-10k}$ gives $k=\\ln2/10\\approx0.0693147$ min$^{-1}$.",["ratio","k units"]),("Predict and check.","At 20 min, $T=20+70(1/2)^2=37.5$ C, between the initial and ambient temperatures.",["prediction","physical range"])),
        ex("we02","Unequal-flow mixing","A 50-L tank starts fresh. Brine enters at 4 L/min and 1 g/L; mixture leaves at 2 L/min.",( "Construct volume and balance.","$V=50+2t$ and $Q'=4-2Q/(50+2t)$, $Q(0)=0$.",["changing volume","balance"]),("Solve the linear IVP.","An integrating factor is $50+2t$; integration gives $Q=(200t+4t^2)/(50+2t)$ grams.",["integrating factor","solution"]),("Verify the physical interval.","For a 100-L capacity, $0\\le t<25$ min; substitution verifies the ODE on that interval.",["capacity","ODE check"])),
        ex("we03","Emptying-time domain","An 80-L tank has 3 L/min entering and 7 L/min leaving.",( "Find the volume law.","$V(t)=80-4t$ L.",["net rate","volume"]),("Locate the boundary.","$V=0$ at $t=20$ min, so concentration terms $Q/V$ become singular there.",["emptying time","singularity"]),("State the model interval.","The well-mixed ODE is physically valid on $0\\le t<20$, subject to the mixing assumption.",["half-open physical interval","assumption"])),
    ]))

    modules.append(base.concept("ede-ch04-resistance-escape-mechanics-depth-concept-lesson",CH4,"Mechanics with Resistance and Escape","A mechanics ODE is trustworthy only after direction, force law, units, and the active motion branch are declared.",[
        sec(1,"Force, mass, and sign conventions","Choose a positive direction before writing $m v'=\\sum F$. Weight is $mg$, not $g$ alone, and every resistance force points opposite the current velocity.",mc(1,"Downward is positive for a falling mass with linear drag. Which equation is correct?",O["mechanics"],["$mv'=mg-bv$","$mv'=g+bv$","$v'=mg+bv$","$mv'=-mg-bv$"],0,"Gravity is positive downward and drag is negative when $v>0$.","drag"),("ch04-resistance-branches.svg","Force and velocity arrows for upward and downward branches with linear and quadratic resistance.")),
        sec(2,"Linear resistance","For downward motion with $m v'=mg-bv$, velocity approaches $v_T=mg/b$. The transient decays at rate $b/m$.",num(2,"A 2-kg falling object has $b=0.5$ kg/s and $g=9.8$ m/s$^2$. Find terminal speed.",O["mechanics"],39.2,"$v_T=mg/b=2(9.8)/0.5=39.2$ m/s.",1e-8)),
        sec(3,"Upward and downward branches","If upward is positive, linear drag is $-bv$ automatically on either branch, but a quadratic law is commonly written $-b|v|v$. Replacing it by $-bv^2$ reverses the force incorrectly when $v<0$.",mc(3,"Which expression always opposes velocity?",O["drag"],["$-b|v|v$","$-bv^2$","$+b|v|v$","$bg$"],0,"$|v|v$ has the sign of $v$, so its negative opposes either direction.","drag")),
        sec(4,"Apex and return questions","During upward motion, solve only until the first time $v=0$. The downward branch then begins with new sign behavior; position follows from integrating velocity and may require a second equation or quadrature.",num(4,"For $v'=-(1+v^2)$, $v(0)=1$, the solution satisfies $\\arctan v=\\pi/4-t$. Find the apex time.",O["drag"],.785398,"At the apex $v=0$, so $t=\\pi/4\\approx0.785398$.",1e-6)),
        sec(5,"Inverse-square gravity","Far from a planet, gravitational acceleration varies as $-GM/r^2$. With $v=dr/dt$, the identity $r''=v,dv/dr$ reduces the autonomous second-order equation.",mc(5,"Which reduced equation follows from $r''=-GM/r^2$?",O["drag"],["$v\\,dv/dr=-GM/r^2$","$dv/dr=-GM/r^2$","$v'=-GM/r$","$v^2=-GM/r^2$"],0,"The chain rule gives $r''=dv/dt=(dv/dr)(dr/dt)=v,dv/dr$.","phase"),("ch04-inverse-square-escape.svg","Radial speed and inverse-square attraction with the escape-energy threshold.")),
        sec(6,"Escape velocity","Integration gives $v^2/2-GM/r=C$. Requiring nonnegative limiting speed as $r\\to\\infty$ yields the threshold $v_{esc}=\\sqrt{2GM/r_0}$.",num(6,"If $2GM/r_0=121$ km$^2$/s$^2$, find escape speed in km/s.",O["drag"],11,"$v_{esc}=\\sqrt{121}=11$ km/s.",0)),
    ]))
    modules.append(base.worked("ede-ch04-resistance-escape-mechanics-depth-worked-examples",CH4,"Mechanics with Resistance and Escape: Worked Examples",[
        ex("we01","Falling with linear resistance","Solve $v'=9.8-0.5v$, $v(0)=0$, with downward positive.",( "Identify equilibrium and rate.","$v_T=9.8/0.5=19.6$ m/s and the transient rate is $0.5$ s$^{-1}$.",["terminal speed","rate"]),("Solve the IVP.","$v(t)=19.6(1-e^{-0.5t})$.",["solution","initial value"]),("Verify direction and limit.","$v'=9.8e^{-0.5t}=9.8-0.5v$, $v\\ge0$, and $v\\to19.6$.",["ODE","sign","limit"])),
        ex("we02","Upward quadratic-drag branch","Solve $v'=-(1+v^2)$, $v(0)=1$, until the apex.",( "Separate on the upward branch.","$dv/(1+v^2)=-dt$.",["branch","separation"]),("Apply initial data.","$\\arctan v=\\pi/4-t$, so $v=\\tan(\\pi/4-t)$.",["integration","constant"]),("Locate the branch endpoint.","The first $v=0$ occurs at $t=\\pi/4$; the upward formula is used on $0\\le t\\le\\pi/4$.",["apex","valid interval"])),
        ex("we03","Escape-speed derivation","A particle is launched radially from $r_0$ under $r''=-GM/r^2$.",( "Reduce using velocity as a function of radius.","$v,dv/dr=-GM/r^2$.",["chain rule","reduction"]),("Integrate from initial data.","$\\frac12(v^2-v_0^2)=GM(1/r-1/r_0)$.",["integral","constant"]),("Apply the escape condition.","At threshold $v\\to0$ as $r\\to\\infty$, giving $v_0=\\sqrt{2GM/r_0}$.",["infinite-radius limit","threshold"])),
    ]))

    modules.append(base.concept("ede-ch04-autonomous-second-order-depth-concept-lesson",CH4,"Autonomous Second-Order Foundations","Phase lines motivate the direction analysis, but a second-order autonomous equation evolves in the state plane $(y,v)$.",[
        sec(1,"First-order phase lines as a bridge","For $y'=f(y)$, zeros of $f$ are equilibria and signs between zeros set one-dimensional arrows. A second-order state needs both position and velocity, so one phase line is no longer enough.",mc(1,"Why is $y$ alone insufficient to specify a second-order autonomous state?",O["autonomous"],["Different velocities at the same position produce different motion","The equation has no derivatives","Every solution is constant","Time must be complex"],0,"Second-order initial data include both $y$ and $y'$.","phase")),
        sec(2,"Introduce velocity","Set $v=y'$. Then $y''=f(y,y')$ becomes the first-order system $y'=v$, $v'=f(y,v)$ in the phase plane.",mc(2,"Which system represents $y''=-y$?",O["energy"],["$y'=v$, $v'=-y$","$y'=-y$, $v'=v$","$y'=v'$, $v=-y$","$y'=y$, $v'=-v$"],0,"Velocity is $v=y'$ and acceleration is $v'=y''=-y$.","phase"),("ch04-autonomous-phase-reduction.svg","A second-order autonomous equation reduced to a first-order phase-plane system and a velocity-versus-position equation.")),
        sec(3,"Use $v$ as a function of $y$","Where a trajectory can be treated as $v(y)$, the chain rule gives $y''=dv/dt=(dv/dy)(dy/dt)=v,dv/dy$. This reduction may lose information at turning points unless branches are tracked.",mc(3,"What replaces $y''$ when $v=y'$ is treated as a function of $y$?",O["energy"],["$v\\,dv/dy$","$dv/dy$","$v^2$","$dy/dv$"],0,"The chain rule multiplies $dv/dy$ by $dy/dt=v$.","phase")),
        sec(4,"Phase trajectories","A solution maps time to $(y(t),v(t))$. Its tangent vector is $(v,f(y,v))$, so direction requires both components rather than the slope of an un-oriented level curve.",mc(4,"At $(y,v)=(1,-2)$ for $y''=-y$, which way does the state initially move?",O["autonomous"],["Toward smaller $y$ and smaller $v$","Toward larger $y$ and smaller $v$","Toward smaller $y$ and larger $v$","It is stationary"],0,"$(y',v')=(v,-y)=(-2,-1)$, so both coordinates decrease.","direction")),
        sec(5,"Equilibria","A phase-plane equilibrium requires $y'=v=0$ and $v'=f(y,0)=0$. Solving only $f(y,0)=0$ can falsely include points with nonzero velocity.",mc(5,"Which points are equilibria of $y''=y-y^3$?",O["autonomous"],["$(y,v)=(-1,0),(0,0),(1,0)$","Every point with $v=0$","Every point with $y=0$","$(1,1)$ only"],0,"Both $v=0$ and $y-y^3=0$ are required.","phase")),
        sec(6,"Initial data select a curve and direction","An initial pair $(y_0,v_0)$ selects a phase trajectory and its orientation. A first integral may identify the curve, while the sign of $v_0$ identifies which way it is traversed.",mc(6,"For $y''=-y$ and $y^2+v^2=4$, what does $(y_0,v_0)=(0,2)$ determine beyond the circle?",O["energy"],["The initial direction of travel","A different energy level","That the state is an equilibrium","That time stops"],0,"The positive initial velocity fixes the orientation along the selected energy circle.","direction")),
    ]))
    modules.append(base.worked("ede-ch04-autonomous-second-order-depth-worked-examples",CH4,"Autonomous Second-Order Equations: Worked Examples",[
        ex("we01","Reduction through $v(y)$","Reduce $y''=-y$ using $v=y'$.",( "Apply the chain rule.","$v\\,dv/dy=-y$.",["v substitution","chain rule"]),("Integrate the trajectory equation.","$v^2/2+y^2/2=C$, or $v^2+y^2=C_1$.",["integration","first integral"]),("Check against the system.","Differentiating $v^2+y^2$ in time gives $2v(-y)+2yv=0$.",["time derivative","conservation"])),
        ex("we02","Orient a phase trajectory","For $y''=-y$, use initial data $y(0)=0$, $v(0)=2$.",( "Select the energy curve.","$v^2+y^2=4$.",["initial data","circle"]),("Find the initial tangent.","$(y',v')=(2,0)$ at $(0,2)$, so motion begins to the right.",["vector field","orientation"]),("Connect to the time solution.","$y=2\\sin t$, $v=2\\cos t$ traces the circle clockwise from its top point.",["explicit check","trajectory direction"])),
        ex("we03","Restoring-force stability","Analyze $y''=-4y$ near $(0,0)$.",( "Check the force sign.","For $y>0$, acceleration is negative; for $y<0$, it is positive, always restoring toward zero.",["signs","restoring force"]),("Find a first integral.","$v^2/2+2y^2=C$ gives closed ellipses.",["energy","closed curves"]),("Classify the equilibrium.","Nearby states remain on nearby bounded ellipses, so the equilibrium is stable but not asymptotically stable.",["bounded motion","classification"])),
    ]))

    modules.append(base.concept("ede-ch04-energy-damping-phase-depth-concept-lesson",CH4,"Energy, Oscillation, and Damping","First integrals organize conservative motion; damping replaces closed energy curves with trajectories of decreasing energy.",[
        sec(1,"Conservative first integrals","For $y''+p(y)=0$, let $P'(y)=p(y)$. Multiplying by $y'$ gives $d[\\frac12v^2+P(y)]/dt=0$, so energy is constant.",mc(1,"Which quantity is conserved for $y''+4y=0$?",O["energy"],["$v^2/2+2y^2$","$v+4y$","$v^2/2-2y^2$","$4v+y$"],0,"Here $P(y)=2y^2$, so kinetic plus potential energy is constant.","energy"),("ch04-conservative-energy-levels.svg","Potential wells, energy levels, turning points, and their phase-plane curves.")),
        sec(2,"Kinetic and potential energy","Allowed positions satisfy $P(y)\\le E$ because $v^2/2=E-P(y)\\ge0$. Turning points occur where $v=0$ and $P(y)=E$.",num(2,"For $E=v^2/2+2y^2=8$, find the positive turning point.",O["energy"],2,"At a turning point $v=0$, so $2y^2=8$ and $y=2$.",0)),
        sec(3,"Spring phase curves","A linear spring produces elliptical phase curves. Their orientation follows $y'=v$, and no nonzero trajectory spirals inward without damping.",mc(3,"What does a closed phase ellipse indicate?",O["energy"],["Periodic conservative motion","Monotone escape","Energy loss each cycle","A single equilibrium point"],0,"A closed energy level corresponds to repeated oscillation at constant energy.","energy")),
        sec(4,"Pendulum separatrices","For $y''+\\sin y=0$, energy is $E=v^2/2+1-\\cos y$. The level $E=2$ passes through unstable upright equilibria and separates oscillations from rotations.",mc(4,"For the normalized pendulum, which energy is the separatrix?",O["energy"],["$E=2$","$E=0$","$E=1/2$","Every energy"],0,"At the upright point $y=\\pi$, $v=0$, so $E=1-\\cos\\pi=2$.","energy")),
        sec(5,"Damped systems","For $y''+c y'+p(y)=0$, the phase system is $y'=v$, $v'=-cv-p(y)$. The mechanical energy satisfies $E'=-cv^2\\le0$ when $c>0$.",mc(5,"What is $E'$ for $y''+0.5y'+y=0$?",O["damping"],["$-0.5v^2$","$+0.5v^2$","$-y^2$","$0$"],0,"Multiplying the equation by $v$ leaves the dissipative term $-0.5v^2$.","damping"),("ch04-damped-phase-portraits.svg","Closed conservative orbits contrasted with inward damped trajectories and decreasing energy.")),
        sec(6,"Inward phase trajectories","Damping usually turns closed conservative curves into inward trajectories. Energy decreases strictly except at instants with $v=0$, so crossing outward to a higher energy level is impossible.",mc(6,"Which observation is incompatible with positive viscous damping and no external forcing?",O["damping"],["A trajectory crosses repeatedly to higher energy levels","Amplitude decreases","Energy is momentarily stationary at a turning point","The state approaches equilibrium"],0,"With $E'=-cv^2\\le0$, mechanical energy cannot increase.","damping")),
    ]))
    modules.append(base.worked("ede-ch04-energy-damping-phase-depth-worked-examples",CH4,"Energy and Damping: Worked Examples",[
        ex("we01","Spring energy","For $y''+4y=0$, $y(0)=1$, $v(0)=0$.",( "Derive the energy.","$E=v^2/2+2y^2$ is constant.",["potential","first integral"]),("Apply initial data.","$E=2$, so $v^2+4y^2=4$.",["constant","phase ellipse"]),("Verify turning points.","At $v=0$, $y=\\pm1$; the initial point is one turning point and the motion remains bounded.",["turning points","boundedness"])),
        ex("we02","Pendulum energy classification","For $y''+\\sin y=0$, start at $y=0$ with speed $v_0$.",( "Evaluate initial energy.","$E=v_0^2/2$ because $1-\\cos0=0$.",["energy","initial state"]),("Compare with the barrier.","The upright barrier is $E=2$, so $|v_0|=2$ is the separatrix threshold.",["barrier","threshold"]),("Classify the motion.","$|v_0|<2$ oscillates, $|v_0|=2$ approaches an upright equilibrium, and $|v_0|>2$ rotates.",["three regimes","separatrix"])),
        ex("we03","Damped energy audit","For $y''+0.5y'+y=0$, define $E=(v^2+y^2)/2$.",( "Differentiate along a solution.","$E'=vv'+yy'=v(-0.5v-y)+yv=-0.5v^2$.",["chain rule","system substitution"]),("Infer monotonicity.","$E'\\le0$, with equality only when $v=0$ at that instant.",["sign","turning point"]),("Interpret the portrait.","No trajectory can move to a higher energy circle; non-equilibrium motion loses amplitude and spirals toward the origin.",["inward motion","equilibrium"])),
    ]))

    modules.append(base.concept("ede-ch04-curve-family-geometry-depth-concept-lesson",CH4,"Curve Families, Envelopes, and Orthogonal Fields","A family-to-ODE derivation must eliminate parameters without silently discarding branches or geometric restrictions.",[
        sec(1,"Eliminate a family parameter","Differentiate a one-parameter relation once and use the original relation to remove the parameter. The resulting ODE describes local slopes of family members where the algebra is valid.",mc(1,"For $y=cx^2$, which ODE results after eliminating $c$?",O["curves"],["$y'=2y/x$","$y'=2cx$","$y'=y/x^2$","$y''=0$"],0,"Since $c=y/x^2$, differentiation gives $y'=2cx=2y/x$ for $x\\ne0$.","branch")),
        sec(2,"Lost branches and envelopes","Division or solving for a parameter can remove singular members or an envelope. The derived equation must be checked against the original family and against values where the elimination step was invalid.",mc(2,"Why inspect a factor divided out during elimination?",O["curvefields"],["Its zero set may represent a lost branch or envelope","It changes the independent variable","It guarantees orthogonality","It supplies an initial condition"],0,"Division excludes the factor's zero set, which may still have geometric meaning.","branch"),("ch04-curve-envelope.svg","A one-parameter line family tangent to its envelope with the eliminated parameter and singular curve marked.")),
        sec(3,"Tangent-line families","For $y=cx-c^2$, differentiation gives $y'=c$, so elimination yields $y=xy'-(y')^2$. The envelope comes from optimizing over $c$ and is not merely another fixed-$c$ line.",mc(3,"What is the envelope of $y=cx-c^2$?",O["curvefields"],["$y=x^2/4$","$y=x^2$","$y=-x^2/4$","$y=x/2$"],0,"$\\partial y/\\partial c=x-2c=0$ gives $c=x/2$ and $y=x^2/4$.","branch")),
        sec(4,"Translate geometric conditions","Statements about tangent intercepts, normals, or angles must be expressed using the point $(x,y)$ and slope $y'$. A diagram helps identify signed lengths before algebra begins.",mc(4,"A tangent at $(x,y)$ has x-intercept $a$. Which relation follows from point-slope form?",O["curvefields"],["$y'=y/(x-a)$","$y'=(x-a)/y$","$y'=y/x$","$y'=a$"],0,"Setting $Y=0$ at $X=a$ in $Y-y=y'(X-x)$ gives $-y=y'(a-x)$.","branch")),
        sec(5,"Orthogonal trajectories","At a regular intersection, perpendicular slopes satisfy $m_1m_2=-1$. Vertical or zero slopes require geometric care rather than blind division by zero.",mc(5,"The family slope is $-x/y$. What is the regular orthogonal slope?",O["curves"],["$y/x$","$x/y$","$-y/x$","$-x/y$"],0,"The negative reciprocal of $-x/y$ is $y/x$.","orthogonal"),("ch04-orthogonal-field-lines.svg","Level curves crossed at right angles by heat-flow or force-field trajectories.")),
        sec(6,"Physical field-line interpretations","Isotherms and equipotentials are level curves. Heat-flow lines or conservative force lines follow gradient directions and therefore meet regular level curves orthogonally.",mc(6,"Why do gradient field lines meet regular level curves orthogonally?",O["curvefields"],["The gradient is normal to a level curve","Their slopes are always equal","Every level curve is a circle","The parameter is constant in time"],0,"Directional change along a level curve is zero, so its tangent is perpendicular to the gradient.","orthogonal")),
    ]))
    modules.append(base.worked("ede-ch04-curve-family-geometry-depth-worked-examples",CH4,"Curve Families and Orthogonal Fields: Worked Examples",[
        ex("we01","A line family and its envelope","Analyze $y=cx-c^2$.",( "Eliminate the parameter locally.","$y'=c$, hence $y=xy'-(y')^2$.",["differentiate","eliminate c"]),("Find the envelope.","$x-2c=0$ gives $c=x/2$ and envelope $y=x^2/4$.",["stationary parameter","envelope"]),("Verify tangency.","At $x=2c$, the envelope slope $x/2=c$ equals the line slope, so each line is tangent there.",["same point","same slope"])),
        ex("we02","A fixed tangent intercept","Find curves whose tangent always meets the x-axis at fixed $a$.",( "Translate the geometry.","Point-slope form at the intercept gives $y'=y/(x-a)$.",["intercept","slope equation"]),("Solve the ODE.","$dy/y=dx/(x-a)$, so $y=C(x-a)$ on intervals not crossing $a$.",["separation","family"]),("Check the geometry.","Each solution is itself a line through $(a,0)$, so every tangent has the required intercept.",["substitution","geometric check"])),
        ex("we03","Circles and radial trajectories","Find trajectories orthogonal to $x^2+y^2=c^2$.",( "Find the circle slope.","Differentiation gives $y'=-x/y$ where $y\\ne0$.",["differentiate","regular region"]),("Use the negative reciprocal.","Orthogonal curves satisfy $y'=y/x$.",["perpendicular slope","ODE"]),("Integrate and interpret.","$dy/y=dx/x$ gives $y=Cx$, radial lines that cross concentric circles normally; axis cases are included geometrically.",["family","axis warning","field interpretation"])),
    ]))
    docs.extend(modules)
    return docs


CHUNKS = {
    "ede-ch03-error-convergence-depth": ["0142", "0143", "0144", "0145"],
    "ede-ch03-two-stage-methods-depth": ["0158", "0168", "0169", "0170", "0171", "0176"],
    "ede-ch03-rk4-backward-depth": ["0176", "0177", "0178", "0179", "0180", "0183", "0184"],
    "ede-ch03-semilinear-methods-depth": ["0145", "0146", "0147", "0148", "0149", "0150", "0151", "0152", "0165", "0166", "0167", "0182"],
    "ede-ch04-growth-input-inference-depth": [f"{i:04d}" for i in range(194, 204)],
    "ede-ch04-cooling-variable-mixing-depth": [f"{i:04d}" for i in range(208, 223)],
    "ede-ch04-resistance-escape-mechanics-depth": [f"{i:04d}" for i in range(223, 239)],
    "ede-ch04-autonomous-second-order-depth": [f"{i:04d}" for i in range(238, 247)],
    "ede-ch04-energy-damping-phase-depth": [f"{i:04d}" for i in range(246, 261)],
    "ede-ch04-curve-family-geometry-depth": [f"{i:04d}" for i in range(262, 279)],
}


def chunk_ids(aid: str) -> list[str]:
    key = aid.removesuffix("-concept-lesson").removesuffix("-worked-examples")
    return [f"{SRC}:chunk-{c}" for c in CHUNKS[key]]


def objective_ids(doc: dict) -> list[str]:
    found: list[str] = []
    for _, _, item in assessment_items(doc):
        for obj in item.get("skills", []):
            if obj.startswith("ede-") and obj not in found:
                found.append(obj)
    return found or [doc["topicId"]]


def assessment_items(doc: dict):
    if doc["assessmentType"] == "conceptLesson":
        for section in doc["lesson"]["sections"]:
            yield section["check"]["id"], section["title"], section["check"]
    else:
        for example in doc["workedExamples"]:
            for step in example["steps"]:
                yield step["id"], f"{example['title']}: {step['title']}", step


def attach_media(docs: list[dict]) -> None:
    visual_map = {
        "ede-ch03-error-convergence-depth-concept-lesson": (1, "ch03-error-propagation.svg"),
        "ede-ch03-two-stage-methods-depth-concept-lesson": (0, "ch03-two-stage-family.svg"),
        "ede-ch03-rk4-backward-depth-concept-lesson": (0, "ch03-rk4-stage-geometry.svg"),
        "ede-ch03-semilinear-methods-depth-concept-lesson": (2, "ch03-semilinear-transform.svg"),
        "ede-ch04-growth-input-inference-depth-concept-lesson": (0, "ch04-parameter-inference.svg"),
        "ede-ch04-cooling-variable-mixing-depth-concept-lesson": (2, "ch04-variable-volume-tank.svg"),
        "ede-ch04-resistance-escape-mechanics-depth-concept-lesson": (0, "ch04-resistance-branches.svg"),
        "ede-ch04-autonomous-second-order-depth-concept-lesson": (1, "ch04-autonomous-phase-reduction.svg"),
        "ede-ch04-energy-damping-phase-depth-concept-lesson": (0, "ch04-conservative-energy-levels.svg"),
        "ede-ch04-curve-family-geometry-depth-concept-lesson": (1, "ch04-curve-envelope.svg"),
    }
    for doc in docs:
        if doc["id"] in visual_map:
            idx, name = visual_map[doc["id"]]
            # Existing explicit media is retained; this guard prevents duplicates.
            section = doc["lesson"]["sections"][idx]
            if not section.get("media"):
                section["media"] = media(name, name.removesuffix(".svg").replace("-", " "))


def write_assessments(docs: list[dict]) -> None:
    for doc in docs:
        (ASSESS / f"{doc['id']}.yaml").write_text(
            yaml.dump(doc, Dumper=base.LiteralDumper, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")


def write_manifests(docs: list[dict]) -> None:
    out = REF / "content-manifests"
    for doc in docs:
        data = {"schemaVersion": 1, "id": f"{doc['id']}-manifest", "categoryId": CAT,
                "topicId": doc["topicId"], "assessmentId": doc["id"],
                "objectiveIds": objective_ids(doc), "sourceId": SRC,
                "sourceChunkIds": chunk_ids(doc["id"]), "reviewState": "approved"}
        (out / f"{doc['id']}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


GOVERNING = {
    O["error"]: "Taylor remainder, one-step defect, global error propagation, and empirical order",
    O["twostage"]: "two-stage order conditions and the specified stage location and weights",
    O["rk4"]: "classical RK4 stage states and the 1-2-2-1 weighted update",
    O["backward"]: "negative-step integration or the reflected-variable chain rule",
    O["semilinear"]: "the substitution y=u y1 with y1 solving the complementary linear equation",
    O["compare"]: "common-endpoint reference error and right-hand-side evaluation cost",
    O["growth"]: "a constant-input proportional-removal balance",
    O["inference"]: "exponential ratios, logarithms, and parameter units",
    O["mixing"]: "solute inflow minus outflow with concentration Q/V",
    O["variablemix"]: "V(t)=V0+(rin-rout)t and the first physical boundary",
    O["mechanics"]: "Newton's second law with a declared positive direction",
    O["drag"]: "direction-dependent resistance or inverse-square energy balance",
    O["autonomous"]: "the phase system y'=v, v'=f(y,v)",
    O["energy"]: "v dv/dy reduction and the conservative first integral",
    O["damping"]: "E'=-c v^2 and inward phase-plane motion",
    O["curves"]: "parameter elimination and negative-reciprocal slopes",
    O["curvefields"]: "envelope checks, geometric slope translation, and gradient orthogonality",
}


def blueprint_bank(docs: list[dict], chapter: int) -> None:
    topic = CH3 if chapter == 3 else CH4
    path = REF / "question-blueprints" / f"{topic}-blueprints.json"
    bank = json.loads(path.read_text(encoding="utf-8"))
    ids = {d["id"] for d in docs}
    bank["blueprints"] = [b for b in bank["blueprints"] if b.get("assessmentId") not in ids]
    counter = 1
    for doc in docs:
        chunks = chunk_ids(doc["id"])
        for item_id, title, item in assessment_items(doc):
            obj = next((x for x in item.get("skills", []) if x in GOVERNING), objective_ids(doc)[0])
            prompt = item.get("prompt", item.get("instruction", title))
            sig = f"{doc['id']}::{item_id}::{obj}::{prompt[:72]}"
            bank["blueprints"].append({
                "id": f"{doc['id']}-bp-{counter:03d}", "assessmentId": doc["id"], "questionId": item_id,
                "objectiveId": obj, "questionType": item.get("type", "freeResponse"), "sourceChunks": chunks,
                "reviewState": "approved", "givens": prompt,
                "unknown": f"Determine and justify the requested result for {title}.",
                "representationRequirement": "Use the linked original diagram when the prompt depends on geometry, stage location, balance flow, or phase direction.",
                "governingPrinciple": GOVERNING.get(obj, obj),
                "methodSteps": [f"Identify the applicable relation: {GOVERNING.get(obj, obj)}.",
                                "Substitute the stated data and carry out the calculation or classification in order.",
                                "Verify the result against the original equation, direction, units, reference, or domain."],
                "misconception": f"The learner may trigger a registered {obj} misconception by using the wrong sign, stage, state, branch, or domain.",
                "difficultyEvidence": item.get("difficultyEvidence", "Requires method selection and an independent equation, unit, domain, or qualitative check."),
                "verification": "Recompute independently and substitute into the governing equation; also check units, sign, endpoint, and domain where applicable.",
                "answerVerificationMethod": "Recompute independently and substitute into the governing equation; also check units, sign, endpoint, and domain where applicable.",
                "variationAxes": ["scenario and governing equation", f"unknown represented as {item.get('type','freeResponse')}", f"method branch {obj}"],
                "reasoningSignature": sig,
                "difficultyDimensions": item.get("difficultyDimensions", ["modelOrDerivation", "verification"]),
                "prerequisiteObjectiveIds": ["ede-ch02-first-order-equations-linear-ivps"],
                "extensionObjectiveIds": ["ede-ch05-linear-second-order-equations-curriculum"] if chapter == 4 else ["ede-ch04-first-order-applications-growth-decay"],
            })
            counter += 1
    bank["reviewState"] = "approved"
    path.write_text(json.dumps(bank, indent=2) + "\n", encoding="utf-8")


def refresh_packets_curriculum() -> None:
    objectives = {
        3: [
            (O["twostage"], ["0168", "0169", "0170", "0171", "0176"]),
            (O["semilinear"], ["0145", "0146", "0147", "0148", "0149", "0150", "0151", "0152", "0165", "0166", "0167", "0182"]),
            (O["backward"], ["0183", "0184"]),
        ],
        4: [
            (O["inference"], [f"{i:04d}" for i in range(194, 204)]),
            (O["variablemix"], [f"{i:04d}" for i in range(208, 223)]),
            (O["drag"], [f"{i:04d}" for i in range(223, 239)]),
            (O["energy"], [f"{i:04d}" for i in range(238, 253)]),
            (O["damping"], [f"{i:04d}" for i in range(253, 261)]),
            (O["curvefields"], [f"{i:04d}" for i in range(262, 279)]),
        ],
    }
    for chapter, topic in [(3, CH3), (4, CH4)]:
        path = REF / "packets" / f"packet-{topic}-v1.json"
        packet = json.loads(path.read_text(encoding="utf-8"))
        by_id = {x["id"]: x for x in packet["objectives"]}
        if chapter == 3:
            by_id["ede-ch03-numerical-methods-euler-updates"]["chunkIds"] = [
                f"{SRC}:chunk-{i:04d}" for i in range(133, 142)
            ]
            by_id[O["error"]]["chunkIds"] = [f"{SRC}:chunk-{i:04d}" for i in range(142, 146)]
            by_id["ede-ch03-numerical-methods-improved-euler"]["chunkIds"] = [
                f"{SRC}:chunk-0158", *[f"{SRC}:chunk-{i:04d}" for i in range(168, 177)]
            ]
            by_id[O["rk4"]]["chunkIds"] = [f"{SRC}:chunk-{i:04d}" for i in range(176, 183)]
        for oid, chunks in objectives[chapter]:
            by_id[oid] = {"id": oid, "chunkIds": [f"{SRC}:chunk-{c}" for c in chunks]}
        packet["objectives"] = list(by_id.values())
        packet["reviewState"] = "approved"
        packet["reviewNotes"] = ["Selected equations and diagram-bearing chunks were reviewed after pypdf-v1 extraction; tracked artifacts retain chunk IDs only."]
        path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")

    path = REF / "curriculum-manifests" / "elementary-differential-equations-bvp.yaml"
    data = json.loads(path.read_text(encoding="utf-8"))
    additions = {
        3: [
            (O["twostage"], "Derive and apply the source's second-order two-stage family and its quadrature connections.", [O["error"]]),
            (O["semilinear"], "Transform semilinear IVPs with a complementary solution before applying numerical updates.", ["ede-ch02-first-order-equations-linear-ivps"]),
            (O["backward"], "Integrate an IVP backward using negative steps or a verified reflected-variable transformation.", ["ede-ch03-numerical-methods-euler-updates"]),
        ],
        4: [
            (O["inference"], "Infer rate parameters and event times from growth, decay, cooling, or input-model observations.", [O["growth"]]),
            (O["variablemix"], "Solve and delimit unequal-flow mixing models with changing volume.", [O["mixing"]]),
            (O["drag"], "Analyze direction-dependent resistance and derive the inverse-square escape threshold.", [O["mechanics"]]),
            (O["energy"], "Reduce autonomous second-order equations and interpret conservative phase-plane energy levels.", [O["mechanics"]]),
            (O["damping"], "Use energy decay to interpret damped autonomous phase trajectories.", [O["energy"], O["mechanics"]]),
            (O["curvefields"], "Analyze envelopes, geometric tangent conditions, and orthogonal physical field lines.", [O["curves"]]),
        ],
    }
    for chapter, cid in [(3, "ede-ch03-numerical-methods-curriculum"), (4, "ede-ch04-first-order-applications-curriculum")]:
        group = next(x for x in data["objectives"] if x["id"] == cid)
        by_id = {x["id"]: x for x in group["objectives"]}
        for oid, title, prereqs in additions[chapter]:
            by_id[oid] = {"id": oid, "title": title, "prerequisiteIds": prereqs,
                          "requiredActivities": ["conceptLesson", "guidedWorkedExample"], "sourceIds": [SRC]}
        group["objectives"] = list(by_id.values())
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def release_manifest(docs: list[dict], chapter: int) -> None:
    topic = CH3 if chapter == 3 else CH4
    rid = "ede-ch03-numerical-depth-supplemental-assessment-release" if chapter == 3 else "ede-ch04-applications-depth-supplemental-assessment-release"
    data = {"schemaVersion": 1, "id": rid, "categoryId": CAT, "topicId": topic, "areaId": AREA,
            "packetId": f"packet-{topic}-v1", "releaseKind": "supplemental", "publicationStatus": "published",
            "sourceReviewState": "approved", "artifacts": []}
    for doc in docs:
        data["artifacts"].append({"id": doc["id"], "assessmentType": doc["assessmentType"],
            "learningGoal": "learn", "activityType": doc["navigation"]["activityType"],
            "objectiveIds": objective_ids(doc), "plannedCount": 6 if doc["assessmentType"] == "conceptLesson" else 3,
            "publicationStatus": "published"})
    name = "ede-ch03-numerical-depth-supplemental.json" if chapter == 3 else "ede-ch04-applications-depth-supplemental.json"
    (REF / "assessment-release-manifests" / name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def repair_canonical() -> None:
    p = ASSESS / "ede-ch03-numerical-methods-concept-lesson.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    s4 = next(s for s in d["lesson"]["sections"] if s["id"] == "s4")
    s4["title"] = "Endpoint-average Improved Euler and related two-stage rules"
    s4["content"] = ("Endpoint-average Improved Euler (also called explicit trapezoid and often called Heun's method in other texts) predicts an endpoint and averages the starting and predicted endpoint slopes. This source reserves Heun's name for the second-order choice with stage location $2h/3$ and weights $1/4,3/4$; midpoint samples at $h/2$ and uses that slope for the update. Formulas, not names, determine the stages.")
    s4["check"]["prompt"] = "For $y'=x+y$, $(x_0,y_0)=(0,1)$, and $h=0.4$, endpoint-average Improved Euler predicts $y^*=1.4$. What corrected value results?"
    s4["check"]["explanation"] = "Solution: The slopes are $1$ and $f(0.4,1.4)=1.8$, so $y_1=1+0.4(1+1.8)/2=1.56$.\n\nWhy it works: Endpoint-average Improved Euler uses the starting slope and the predicted endpoint slope; the formula avoids ambiguity among naming conventions."
    p.write_text(yaml.dump(d, Dumper=base.LiteralDumper, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")

    p = ASSESS / "ede-ch03-numerical-methods-worked-examples.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    w = next(x for x in d["workedExamples"] if x["id"] == "we02")
    w["title"] = "Endpoint-average Improved Euler: average slopes"
    w["problem"] = w["problem"].replace("improved-Euler", "endpoint-average Improved Euler")
    for step in w["steps"]:
        step["prompt"] = step["prompt"].replace("Heun", "endpoint-average Improved Euler")
        step["explanation"] = step["explanation"].replace("Heun", "endpoint-average Improved Euler")
    p.write_text(yaml.dump(d, Dumper=base.LiteralDumper, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")

    p = ASSESS / "ede-ch04-first-order-applications-concept-lesson.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    s5 = next(s for s in d["lesson"]["sections"] if s["id"] == "s5")
    s5["title"] = "Autonomous second-order equations and phase planes"
    s5["content"] = ("For $y''=f(y,y')$, set $v=y'$ to obtain the phase-plane system $y'=v$, $v'=f(y,v)$. Where $v$ can be viewed as a function of $y$, the chain rule gives $y''=v\\,dv/dy$. An equilibrium requires both $v=0$ and $f(y,0)=0$; initial position and velocity select a trajectory and its direction.")
    s5["check"] = mc(5, "For $y''=-y$, what is the phase-plane velocity at the state $(y,v)=(1,2)$?", O["autonomous"], ["$(y',v')=(2,-1)$", "$(1,2)$", "$(-1,2)$", "$(2,1)$"], 0, "The system is $y'=v$, $v'=-y$, so the vector is $(2,-1)$.", "phase")
    s5["check"]["id"] = "chk-05"
    p.write_text(yaml.dump(d, Dumper=base.LiteralDumper, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")

    for aid in ["ede-ch03-numerical-methods-concept-lesson", "ede-ch03-numerical-methods-worked-examples", "ede-ch04-first-order-applications-concept-lesson"]:
        mp = REF / "content-manifests" / f"{aid}.json"
        data = json.loads(mp.read_text(encoding="utf-8"))
        if aid.startswith("ede-ch03"):
            data["sourceChunkIds"] = sorted(set(data["sourceChunkIds"] + [f"{SRC}:chunk-0168", f"{SRC}:chunk-0171"]))
        else:
            data["sourceChunkIds"] = sorted(set(data["sourceChunkIds"] + [f"{SRC}:chunk-0238", f"{SRC}:chunk-0240", f"{SRC}:chunk-0246"]))
        data["reviewState"] = "approved"
        mp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def refresh_core_blueprints() -> None:
    targets = {
        CH3: {("ede-ch03-numerical-methods-concept-lesson", "chk-04"),
              ("ede-ch03-numerical-methods-worked-examples", "we2-s1"),
              ("ede-ch03-numerical-methods-worked-examples", "we2-s2"),
              ("ede-ch03-numerical-methods-worked-examples", "we2-s3")},
        CH4: {("ede-ch04-first-order-applications-concept-lesson", "chk-05")},
    }
    for topic, pairs in targets.items():
        path = REF / "question-blueprints" / f"{topic}-blueprints.json"
        bank = json.loads(path.read_text(encoding="utf-8"))
        for bp in bank["blueprints"]:
            if (bp.get("assessmentId"), bp.get("questionId")) in pairs:
                bp["reviewState"] = "approved"
                bp["givens"] = "Use the corrected learner prompt and its declared stage, state, or phase-plane data."
                bp["unknown"] = "Apply the source-faithful numerical naming convention or autonomous second-order reduction."
                bp["governingPrinciple"] = "Formula-defined two-stage updates" if topic == CH3 else "The system y'=v, v'=f(y,v) and y''=v dv/dy"
                bp["methodSteps"] = ["Identify the formula or phase variables.", "Compute using the declared states and signs.", "Verify against the original ODE and naming/domain convention."]
                bp["misconception"] = "Confusing method names with formulas or treating a second-order state as a first-order phase line."
                bp["answerVerificationMethod"] = "Recompute the stages or phase vector and substitute into the original equation."
                bp["variationAxes"] = ["method or equation", "stage/state representation", "verification requirement"]
                bp["reasoningSignature"] = f"{bp['assessmentId']}::{bp['questionId']}::canonical-source-correction"
        path.write_text(json.dumps(bank, indent=2) + "\n", encoding="utf-8")


def issue_signals() -> None:
    path = ROOT / "data" / "issue-signals.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    entries = data if isinstance(data, list) else data["issueSignals"]
    existing = {x["id"] for x in entries}
    descriptions = {
        SIGNALS["order"]: "Infers the wrong convergence order or applies a step-size ratio outside a comparable endpoint calculation.",
        SIGNALS["stage"]: "Evaluates a numerical stage at the wrong location or state, or applies incompatible stage weights.",
        SIGNALS["naming"]: "Selects a numerical rule by an ambiguous name instead of its explicitly stated stage formula.",
        SIGNALS["cost"]: "Compares step counts while ignoring right-hand-side evaluations, endpoints, references, or precision.",
        SIGNALS["semilinear"]: "Transforms or reconstructs a semilinear equation incorrectly or ignores the complementary factor's domain.",
        SIGNALS["backward"]: "Loses the negative step or reflected-variable sign during backward integration.",
        SIGNALS["quadrature"]: "Confuses the rectangle, midpoint, or trapezoid accumulation implied by an IVP update.",
        SIGNALS["parameter"]: "Infers a rate parameter with the wrong logarithmic ratio, sign, units, or time origin.",
        SIGNALS["volume"]: "Uses the initial tank volume after unequal flows have made volume time-dependent.",
        SIGNALS["amount"]: "Confuses solute amount with concentration or omits flow times concentration in a balance.",
        SIGNALS["drag"]: "Uses a resistance sign or quadratic-drag branch that does not oppose the current velocity.",
        SIGNALS["terminal"]: "Misidentifies the zero-acceleration terminal state or the inverse-square escape threshold.",
        SIGNALS["phase"]: "Confuses position, velocity, acceleration, or the two conditions required for a phase-plane equilibrium.",
        SIGNALS["direction"]: "Orients a phase trajectory without using the vector $(y',v')$ or the initial velocity.",
        SIGNALS["energy"]: "Uses an incorrect potential sign or treats a nonconservative trajectory as a constant-energy curve.",
        SIGNALS["damping"]: "Reverses the sign of energy loss or predicts outward motion without external forcing.",
        SIGNALS["branch"]: "Drops a curve branch or envelope during parameter elimination or division.",
        SIGNALS["orthogonal"]: "Uses the same, reciprocal-only, or sign-only slope instead of the negative reciprocal where regular.",
    }
    additions = []
    for sid, desc in descriptions.items():
        if sid not in existing:
            additions.append(
                f'\n- id: "{sid}"\n'
                f'  description: "{desc}"\n'
                f'  domains: ["{CAT}"]\n'
            )
    if additions:
        path.write_text(path.read_text(encoding="utf-8").rstrip() + "\n" + "".join(additions), encoding="utf-8")


def svg_assets() -> None:
    assets = {
        "ch03-error-propagation.svg": ("Error propagation", ["exact state", "one-step defect", "propagated error", "endpoint error"]),
        "ch03-two-stage-family.svg": ("Two-stage family", ["k1 at start", "endpoint average", "Heun at 2h/3", "midpoint at h/2"]),
        "ch03-rk4-stage-geometry.svg": ("RK4 stages", ["k1 start", "k2 midpoint", "k3 updated midpoint", "k4 endpoint"]),
        "ch03-ode-quadrature-connection.svg": ("ODE and quadrature", ["y'=g(x)", "Euler rectangles", "endpoint slopes", "trapezoid sum"]),
        "ch03-semilinear-transform.svg": ("Semilinear transform", ["y'+py=h", "choose y1", "y=u y1", "advance u", "reconstruct y"]),
        "ch03-backward-integration.svg": ("Backward integration", ["right-end data", "negative h", "reflect variable", "verify left endpoint"]),
        "ch04-parameter-inference.svg": ("Parameter inference", ["measure ratio", "take logarithm", "infer rate", "predict and check"]),
        "ch04-variable-volume-tank.svg": ("Variable-volume tank", ["flow in", "Q/V", "flow out", "V(t)", "capacity boundary"]),
        "ch04-resistance-branches.svg": ("Resistance branches", ["choose direction", "gravity", "drag opposes v", "apex", "downward branch"]),
        "ch04-inverse-square-escape.svg": ("Escape threshold", ["r0 and v0", "-GM/r^2", "energy integral", "r to infinity"]),
        "ch04-autonomous-phase-reduction.svg": ("Autonomous reduction", ["y''=f(y,y')", "v=y'", "y'=v", "v'=f(y,v)", "phase trajectory"]),
        "ch04-conservative-energy-levels.svg": ("Conservative energy", ["potential well", "turning point", "closed level", "separatrix"]),
        "ch04-damped-phase-portraits.svg": ("Damped phase portrait", ["E'=-cv^2", "lower energy", "inward trajectory", "equilibrium"]),
        "ch04-curve-envelope.svg": ("Curve envelope", ["one-parameter lines", "eliminate c", "envelope", "tangent contact"]),
        "ch04-orthogonal-field-lines.svg": ("Orthogonal fields", ["level curve", "tangent", "gradient normal", "flow line"]),
    }
    MEDIA.mkdir(parents=True, exist_ok=True)
    for name, (title, labels) in assets.items():
        width = 900
        n = len(labels)
        box = 145
        gap = (width - 60 - n * box) / max(1, n - 1)
        parts = []
        for i, label in enumerate(labels):
            x = 30 + i * (box + gap)
            parts.append(f'<rect x="{x:.1f}" y="105" width="{box}" height="70" rx="12" fill="#ffffff" stroke="#277da1" stroke-width="3"/><text x="{x+box/2:.1f}" y="146" text-anchor="middle">{label}</text>')
            if i < n - 1:
                x2 = x + box
                parts.append(f'<path d="M{x2:.1f} 140H{x2+gap-8:.1f}" stroke="#c65d32" stroke-width="4" marker-end="url(#a)"/>')
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="280" viewBox="0 0 900 280" role="img" aria-labelledby="t d"><title id="t">{title}</title><desc id="d">A labeled reasoning diagram for {title.lower()}.</desc><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#c65d32"/></marker></defs><rect width="900" height="280" rx="24" fill="#f4f8fb"/><text x="450" y="55" text-anchor="middle" font-family="Arial" font-size="26" font-weight="700">{title}</text><g font-family="Arial" font-size="16">{''.join(parts)}</g></svg>'''
        (MEDIA / name).write_text(svg, encoding="utf-8")

    def wrap(title: str, desc: str, body: str) -> str:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="360" viewBox="0 0 900 360" role="img" aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{desc}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#c65d32"/></marker></defs><rect width="900" height="360" rx="24" fill="#f4f8fb"/><text x="450" y="40" text-anchor="middle" font-family="Arial" font-size="25" font-weight="700">{title}</text>{body}</svg>'''

    custom = {
        "ch03-rk4-stage-geometry.svg": wrap("RK4 stage geometry", "Four stage evaluations at the start, two updated midpoint states, and the endpoint.", '''<g font-family="Arial" font-size="17"><path d="M90 260H820" stroke="#555" stroke-width="4" marker-end="url(#arrow)"/><text x="835" y="266">x</text><g stroke="#277da1" stroke-width="4" fill="#fff"><circle cx="150" cy="230" r="10"/><circle cx="450" cy="185" r="10"/><circle cx="450" cy="120" r="10"/><circle cx="750" cy="80" r="10"/></g><g fill="none" stroke="#c65d32" stroke-width="4" marker-end="url(#arrow)"><path d="M160 225Q300 205 438 187"/><path d="M160 225Q300 145 438 123"/><path d="M460 117Q610 80 738 81"/></g><path d="M450 110V260M150 220V260M750 70V260" stroke="#7a8a99" stroke-dasharray="6 6"/><text x="125" y="295">x_n, k1</text><text x="390" y="300">x_n+h/2</text><text x="475" y="190">k2 state</text><text x="475" y="122">k3 updated state</text><text x="710" y="300">x_n+h</text><text x="770" y="85">k4</text></g>'''),
        "ch03-two-stage-family.svg": wrap("Second-order two-stage family", "Stage locations and weights for three related second-order rules.", '''<g font-family="Arial" font-size="17"><g stroke="#555" stroke-width="3"><path d="M210 105H790"/><path d="M210 190H790"/><path d="M210 275H790"/></g><g fill="#277da1"><circle cx="210" cy="105" r="9"/><circle cx="790" cy="105" r="9"/><circle cx="210" cy="190" r="9"/><circle cx="597" cy="190" r="9"/><circle cx="210" cy="275" r="9"/><circle cx="500" cy="275" r="9"/></g><text x="35" y="111">Endpoint average</text><text x="35" y="196">Source Heun</text><text x="35" y="281">Midpoint</text><text x="200" y="78">0</text><text x="780" y="78">h</text><text x="610" y="176">2h/3</text><text x="510" y="261">h/2</text><text x="320" y="130">weights 1/2, 1/2</text><text x="320" y="215">weights 1/4, 3/4</text><text x="320" y="300">weights 0, 1</text></g>'''),
        "ch04-variable-volume-tank.svg": wrap("Changing-volume mixing balance", "A tank with unequal inflow and outflow, current concentration Q over V, and a capacity boundary.", '''<g font-family="Arial" font-size="18"><path d="M300 95V300H650V95" fill="#fff" stroke="#277da1" stroke-width="5"/><path d="M305 190H645V295H305Z" fill="#b9e3ee"/><path d="M70 135H300" stroke="#c65d32" stroke-width="8" marker-end="url(#arrow)"/><path d="M650 245H835" stroke="#c65d32" stroke-width="8" marker-end="url(#arrow)"/><path d="M290 120H660" stroke="#d62828" stroke-width="3" stroke-dasharray="10 8"/><text x="80" y="115">r_in, concentration c_in</text><text x="675" y="225">r_out, Q/V</text><text x="420" y="240" font-size="24">Q(t), V(t)</text><text x="670" y="125" fill="#d62828">capacity</text><text x="350" y="330">V(t)=V0+(r_in-r_out)t</text></g>'''),
        "ch04-resistance-branches.svg": wrap("Resistance opposes motion", "Force arrows for upward and downward motion, showing gravity and drag directions.", '''<g font-family="Arial" font-size="18"><path d="M230 285V80" stroke="#277da1" stroke-width="7" marker-end="url(#arrow)"/><circle cx="230" cy="190" r="28" fill="#fff" stroke="#277da1" stroke-width="4"/><path d="M190 190V275" stroke="#c65d32" stroke-width="7" marker-end="url(#arrow)"/><path d="M270 190V270" stroke="#c65d32" stroke-width="7" marker-end="url(#arrow)"/><text x="125" y="185">v&gt;0 upward</text><text x="145" y="300">mg</text><text x="275" y="300">drag</text><path d="M650 90V290" stroke="#277da1" stroke-width="7" marker-end="url(#arrow)"/><circle cx="650" cy="190" r="28" fill="#fff" stroke="#277da1" stroke-width="4"/><path d="M610 190V275" stroke="#c65d32" stroke-width="7" marker-end="url(#arrow)"/><path d="M690 190V105" stroke="#c65d32" stroke-width="7" marker-end="url(#arrow)"/><text x="710" y="185">v&lt;0 downward</text><text x="565" y="300">mg</text><text x="700" y="95">drag</text><text x="245" y="70">chosen positive</text><text x="665" y="320">quadratic drag: -b|v|v</text></g>'''),
        "ch04-autonomous-phase-reduction.svg": wrap("Autonomous phase plane", "Position-velocity axes, a phase trajectory, its initial state, and the local direction vector.", '''<g font-family="Arial" font-size="18"><path d="M100 290H820M450 325V70" stroke="#555" stroke-width="3" marker-end="url(#arrow)"/><text x="830" y="296">y</text><text x="462" y="75">v</text><ellipse cx="450" cy="195" rx="270" ry="105" fill="none" stroke="#277da1" stroke-width="6"/><circle cx="260" cy="120" r="9" fill="#d62828"/><path d="M260 120Q315 90 365 92" fill="none" stroke="#c65d32" stroke-width="5" marker-end="url(#arrow)"/><text x="175" y="95">(y0,v0)</text><text x="530" y="105">trajectory selected by initial data</text><rect x="610" y="245" width="210" height="55" rx="10" fill="#fff" stroke="#277da1" stroke-width="3"/><text x="715" y="278" text-anchor="middle">(y',v')=(v,f(y,v))</text></g>'''),
        "ch04-conservative-energy-levels.svg": wrap("Conservative energy levels", "Nested phase curves, turning points, and a separatrix around a potential well.", '''<g font-family="Arial" font-size="18"><path d="M90 290H820M450 320V65" stroke="#555" stroke-width="3"/><ellipse cx="450" cy="190" rx="110" ry="65" fill="none" stroke="#277da1" stroke-width="4"/><ellipse cx="450" cy="190" rx="210" ry="115" fill="none" stroke="#277da1" stroke-width="4"/><path d="M120 190C230 45 670 45 780 190C670 335 230 335 120 190Z" fill="none" stroke="#d62828" stroke-width="5" stroke-dasharray="10 7"/><circle cx="240" cy="190" r="8" fill="#c65d32"/><circle cx="660" cy="190" r="8" fill="#c65d32"/><text x="210" y="220">turning</text><text x="625" y="220">turning</text><text x="650" y="75" fill="#d62828">separatrix</text><text x="470" y="180">energy well</text><text x="825" y="296">y</text><text x="462" y="75">v</text></g>'''),
        "ch04-damped-phase-portraits.svg": wrap("Damped phase portrait", "An inward spiral crossing successively lower conservative energy levels toward equilibrium.", '''<g font-family="Arial" font-size="18"><path d="M100 285H810M450 320V70" stroke="#555" stroke-width="3"/><g fill="none" stroke="#9ab7c5" stroke-width="2"><ellipse cx="450" cy="190" rx="280" ry="120"/><ellipse cx="450" cy="190" rx="190" ry="82"/><ellipse cx="450" cy="190" rx="100" ry="44"/></g><path d="M170 190C170 65 730 65 730 190C730 300 270 300 270 190C270 105 630 105 630 190C630 255 355 255 355 190C355 145 545 145 545 190C545 220 430 220 430 190C430 175 465 175 465 190" fill="none" stroke="#c65d32" stroke-width="5" marker-end="url(#arrow)"/><circle cx="450" cy="190" r="8" fill="#277da1"/><text x="600" y="90">E decreases</text><text x="475" y="215">equilibrium</text><text x="815" y="292">y</text><text x="462" y="75">v</text></g>'''),
        "ch04-curve-envelope.svg": wrap("A curve family and its envelope", "Several lines y equals cx minus c squared tangent to the parabolic envelope y equals x squared over four.", '''<g font-family="Arial" font-size="18"><path d="M70 300H830M150 330V65" stroke="#555" stroke-width="3"/><g stroke="#7a8a99" stroke-width="2"><path d="M100 245L800 105"/><path d="M100 290L800 80"/><path d="M100 210L800 140"/><path d="M100 160L800 230"/></g><path d="M120 305Q450 50 790 305" fill="none" stroke="#d62828" stroke-width="6"/><g fill="#277da1"><circle cx="310" cy="190" r="7"/><circle cx="450" cy="135" r="7"/><circle cx="590" cy="190" r="7"/></g><text x="610" y="95">family members</text><text x="610" y="290" fill="#d62828">envelope y=x^2/4</text><text x="330" y="180">tangent contact</text></g>'''),
        "ch04-orthogonal-field-lines.svg": wrap("Orthogonal level and flow lines", "Concentric level curves crossed normally by radial gradient or flow lines.", '''<g font-family="Arial" font-size="18"><g transform="translate(450 195)" fill="none" stroke="#277da1" stroke-width="4"><circle r="55"/><circle r="105"/><circle r="155"/></g><g stroke="#c65d32" stroke-width="4" marker-end="url(#arrow)"><path d="M450 195L450 60"/><path d="M450 195L720 195"/><path d="M450 195L260 70"/><path d="M450 195L650 315"/></g><path d="M605 195h28M605 195v-28" stroke="#333" stroke-width="3"/><text x="665" y="180">90 degrees</text><text x="110" y="100" fill="#277da1">level curves</text><text x="650" y="330" fill="#c65d32">gradient / flow lines</text></g>'''),
    }
    for name, svg in custom.items():
        (MEDIA / name).write_text(svg, encoding="utf-8")


def main() -> None:
    c3, c4 = ch3_docs(), ch4_docs()
    attach_media(c3 + c4)
    repair_canonical()
    write_assessments(c3 + c4)
    write_manifests(c3 + c4)
    blueprint_bank(c3, 3)
    blueprint_bank(c4, 4)
    refresh_core_blueprints()
    refresh_packets_curriculum()
    release_manifest(c3, 3)
    release_manifest(c4, 4)
    issue_signals()
    svg_assets()
    print(f"generated {len(c3)} Chapter 3 and {len(c4)} Chapter 4 assessments")


if __name__ == "__main__":
    main()

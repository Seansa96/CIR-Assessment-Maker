"""Draft structured learner feedback for unstructured Calc II series content.

This tool is deliberately opt-in: it reports candidates by default and only writes
when --apply is provided. It never replaces an existing structured explanation.
"""
import argparse
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
TOPICS = {
    "sequences-series", "sequence-fundamentals", "series-fundamentals", "geometric-telescoping-series",
    "convergence-tests", "ratio-root-tests", "alternating-series", "absolute-conditional-convergence",
    "arithmetic-series", "power-series", "taylor-maclaurin", "series-approximation-error",
    "power-taylor-review", "infinite-series-review",
}

class Dumper(yaml.SafeDumper): pass
def represent(dumper, value):
    value = re.sub(r"[ \t]+\n", "\n", value)
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|" if "\\" in value else None)
Dumper.add_representer(str, represent)

def represent_float(dumper, value):
    """Emit decimal-compatible numeric scalars for the .NET YAML reader."""
    rendered = format(value, ".15f").rstrip("0").rstrip(".")
    return dumper.represent_scalar("tag:yaml.org,2002:float", rendered or "0")
Dumper.add_representer(float, represent_float)

def answer_text(question):
    answer = question.get("answer", {})
    if "choiceId" in answer:
        return next((str(c.get("text", "")) for c in question.get("choices", []) if c.get("id") == answer["choiceId"]), "the stated correct choice")
    if "choiceIds" in answer:
        selected = {str(x) for x in answer["choiceIds"]}
        return ", ".join(str(c.get("text", "")) for c in question.get("choices", []) if str(c.get("id")) in selected)
    return str(answer.get("expectedLatex") or answer.get("expectedValue") or answer.get("expected") or "the stated conclusion")

def convergence_feedback(question):
    text = " ".join(str(question.get(key, "")) for key in ("prompt", "instruction", "title"))
    text += " " + " ".join(str(x) for x in question.get("skills", []))
    text += " " + str(question.get("explanation", ""))
    text = text.lower()
    if "alternating" in text or "conditional" in text:
        return (
            "Why it works: Write the series as $\\sum(-1)^n b_n$. The Alternating Series Test requires $b_n\\ge0$, eventual decrease, and $b_n\\to0$; then test $\\sum b_n$ separately to distinguish absolute from conditional convergence.",
            "Common trap: Alternation alone is not enough. A series can pass the Alternating Series Test yet fail absolute convergence."
        )
    if "ratio" in text or "factorial" in text:
        return (
            "Why it works: Form $L=\\lim_{n\\to\\infty}|a_{n+1}/a_n|$ after cancelling common factors. The Ratio Test gives absolute convergence for $L<1$, divergence for $L>1$, and no conclusion for $L=1$.",
            "Common trap: Do not reverse the ratio or treat $L=1$ as convergence; factorial cancellation must be completed before taking the limit."
        )
    if "root" in text or "nth root" in text or "n-th root" in text:
        return (
            "Why it works: Form $L=\\limsup_{n\\to\\infty}\\sqrt[n]{|a_n|}$. The Root Test gives absolute convergence for $L<1$, divergence for $L>1$, and is inconclusive at $L=1$.",
            "Common trap: The root test is especially useful when a whole expression is raised to the $n$th power; do not omit the absolute value."
        )
    if "p-series" in text or "1/n^p" in text:
        return (
            "Why it works: Match the positive tail to $\\sum 1/n^p$. Its threshold is strict: it converges only when $p>1$ and diverges for $p\\le1$.",
            "Common trap: The harmonic boundary $p=1$ diverges, so replacing $p>1$ with $p\\ge1$ changes the conclusion."
        )
    if "geometric" in text:
        return (
            "Why it works: First rewrite the term as $ar^n$. A geometric series converges exactly when $|r|<1$; its finite sum formula is valid only in that regime.",
            "Common trap: A negative ratio still needs $|r|<1$; alternating signs do not make $r=-1$ converge."
        )
    if "integral" in text:
        return (
            "Why it works: The Integral Test compares the positive tail $a_n=f(n)$ with the improper integral of a continuous, positive, eventually decreasing function $f$. The integral and series then have the same convergence behavior.",
            "Common trap: An antiderivative by itself is not enough; positivity and eventual decrease are required hypotheses."
        )
    if "limit comparison" in text or "dominant" in text:
        return (
            "Why it works: For positive terms, choose a benchmark $b_n$ with the same leading behavior and compute $L=\\lim a_n/b_n$. A finite positive limit means $a_n$ and $b_n$ converge or diverge together.",
            "Common trap: The comparison limit need not equal $1$; any finite positive constant transfers the convergence classification."
        )
    if "comparison" in text:
        return (
            "Why it works: Direct comparison uses nonnegative terms. An upper bound by a convergent benchmark proves convergence, while a lower bound by a divergent benchmark proves divergence.",
            "Common trap: The inequality direction matters: an upper bound by a divergent series and a lower bound by a convergent series prove nothing."
        )
    if "term" in text or "divergence test" in text:
        return (
            "Why it works: Convergence of $\\sum a_n$ requires the necessary condition $a_n\\to0$. A nonzero limit, an infinite limit, or no limit immediately proves divergence.",
            "Common trap: $a_n\\to0$ is necessary but not sufficient; the harmonic series is the standard counterexample."
        )
    return (
        "Why it works: Identify the series structure, verify the selected test's hypotheses, and then apply its stated convergence criterion to the tail of the series.",
        "Common trap: A test conclusion is valid only after its hypotheses and the relevant limiting or comparison calculation have been checked."
    )

def power_taylor_feedback(question):
    text = " ".join(str(question.get(key, "")) for key in ("prompt", "instruction", "title"))
    text += " " + " ".join(str(x) for x in question.get("skills", []))
    text += " " + str(question.get("explanation", ""))
    text = text.lower()
    if any(token in text for token in ("remainder", "error bound", "error", "accuracy", "approximate", "approximation")):
        return (
            "Why it works: For a Taylor polynomial $T_n$, use the applicable remainder theorem rather than the next written term alone. Check the derivative bound and the interval between the expansion center and the target value, then evaluate the resulting upper bound for $|R_n(x)|$.",
            "Common trap: The first omitted term is not automatically an error bound. State the theorem's hypotheses, use the correct derivative order, and keep the degree $n$ distinct from the first omitted index $n+1$."
        )
    if "radius" in text or "interval" in text or "endpoint" in text:
        return (
            "Why it works: First apply the Ratio or Root Test to obtain the open radius condition $|x-c|<R$. Then test each endpoint separately in the original series, because endpoint behavior is not determined by the ratio calculation.",
            "Common trap: Do not substitute endpoints into a simplified inequality and stop; each endpoint may converge, diverge, or have a different inclusion status."
        )
    if "definition" in text or "derivative" in text or "maclaurin" in text or "taylor" in text:
        return (
            "Why it works: The Taylor formula is $\\sum_{n=0}^{\\infty} f^{(n)}(a)(x-a)^n/n!$. Compute derivatives at the center, divide by $n!$, and preserve the power $(x-a)^n$ before analyzing convergence.",
            "Common trap: Do not confuse the derivative value with its Taylor coefficient; the factorial belongs in every coefficient, including the constant term where $0!=1$."
        )
    if "known series" in text or "transform" in text or "representation" in text:
        return (
            "Why it works: Start with a known power-series identity inside its stated interval, then make each algebraic substitution, multiplication, differentiation, or integration term by term. Carry the same transformation into the interval of convergence.",
            "Common trap: A transformed series inherits an interval only after the substitution is translated back to $x$; differentiation or integration can change endpoint inclusion."
        )
    if "power series" in text:
        return (
            "Why it works: Treat the expression as a series in $(x-c)$ and use a convergence test on its coefficients to find the radius. Its value function is obtained only where the series converges.",
            "Common trap: The radius describes the open interval; the two endpoints still require independent convergence tests."
        )
    return (
        "Why it works: State the series identity or approximation theorem being used, carry out the indicated coefficient or bound calculation, and check the resulting convergence or accuracy condition.",
        "Common trap: Keep the expansion center, polynomial degree, and interval/endpoint conditions visible throughout the calculation."
    )

def foundations_feedback(question):
    text = " ".join(str(question.get(key, "")) for key in ("prompt", "instruction", "title"))
    text += " " + " ".join(str(x) for x in question.get("skills", []))
    text += " " + str(question.get("explanation", ""))
    text = text.lower()
    if "telescop" in text or "partial fraction" in text:
        return (
            "Why it works: Rewrite the general term so consecutive partial-sum terms cancel. Write $S_N$ explicitly, cancel only terms that occur with opposite signs, and then take $N\\to\\infty$ to obtain the infinite-series result.",
            "Common trap: Do not cancel nonadjacent terms by inspection without writing $S_N$; the surviving last term usually depends on $N$ and must be sent to its limit."
        )
    if "arithmetic" in text or "common difference" in text:
        return (
            "Why it works: An arithmetic sequence has constant difference $d$, so $a_n=a_1+(n-1)d$. For a finite sum, use $S_n=n(a_1+a_n)/2$ after identifying the correct first and last terms.",
            "Common trap: The $n$th term has $(n-1)d$, not $nd$; distinguish the number of terms from the index of the final term."
        )
    if "partial sum" in text or "sequence of partial" in text:
        return (
            "Why it works: A series $\\sum a_n$ is defined through its partial sums $S_N=\\sum_{n=1}^{N}a_n$. The series converges precisely when the sequence $S_N$ has a finite limit.",
            "Common trap: Terms approaching zero do not guarantee that the partial sums converge; separate the term test from an actual convergence test."
        )
    if "monotone" in text or "bounded" in text:
        return (
            "Why it works: The Monotone Convergence Theorem says an increasing sequence bounded above, or a decreasing sequence bounded below, has a finite limit. Establish both monotonicity and the appropriate bound before concluding convergence.",
            "Common trap: Boundedness alone does not imply a sequence converges; for example, $(-1)^n$ is bounded but oscillates."
        )
    if "sequence" in text or "limit" in text:
        return (
            "Why it works: Evaluate the long-run behavior of $a_n$ using limit laws, dominant terms, or a standard limit. A sequence converges only when its terms approach one finite number from all sufficiently large indices.",
            "Common trap: Checking several numerical terms suggests a pattern but does not prove a limit; account for sign changes, growth rates, and subsequences."
        )
    return (
        "Why it works: Translate the stated series or sequence into its defining formula, carry out the required partial-sum or limit calculation, and state the resulting convergence conclusion with its condition.",
        "Common trap: Keep finite partial sums separate from the limit that defines an infinite series or convergent sequence."
    )

def enrich(question, olympiad=False, feedback=convergence_feedback):
    original = (question.get("explanation") or "").strip()
    if "Solution:" in original and "Why it works:" in original:
        return False
    selected = answer_text(question)
    answer = question.get("answer", {})
    solution = original.split("\n\nWhy it works:", 1)[0].strip()
    solution = re.sub(r"\s*Therefore the answer is (?:the stated conclusion|[^.]+)\.\s*$", "", solution)
    if not solution.startswith("Solution:"):
        solution = f"Solution: {solution}"
    check_model = answer.get("checkModel")
    if len(solution.split()) < 12 and isinstance(check_model, str) and check_model.strip():
        solution += f" Answer check: {check_model.strip()}"
    why, trap = feedback(question)
    conclusion = "" if selected == "the stated conclusion" else f" Therefore the answer is {selected}."
    parts = [
        f"{solution}{conclusion}",
        why,
        trap,
    ]
    if question.get("type") == "multipleChoice":
        wrong = [str(c.get("text", "")) for c in question.get("choices", []) if c.get("id") != answer.get("choiceId")]
        principle = why.removeprefix("Why it works: ").split(". ")[0]
        parts.append("Why the other choices fail: " + "; ".join(f"{choice} conflicts with this criterion: {principle}" for choice in wrong) + ".")
    if olympiad:
        parts.extend([
            "Prerequisites: Taylor and Maclaurin expansions, remainder estimates, asymptotic/error reasoning, and the prerequisite theorem named in the prompt.",
            "Further study: Review the relevant Taylor remainder theorem and a proof or derivation of the error estimate before attempting related extrapolation or error-propagation problems.",
        ])
    question["explanation"] = "\n\n".join(parts)
    return True

def remove_repeated_conclusions(question):
    explanation = question.get("explanation") or ""
    repaired = re.sub(
        r"(?P<conclusion>Therefore the answer is .+?)(?:\.\s*(?P=conclusion)){1,}\.",
        r"\g<conclusion>.",
        explanation)
    if repaired == explanation:
        return False
    question["explanation"] = repaired
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write drafts into files with unstructured explanations.")
    parser.add_argument("--repair-repetition", action="store_true", help="Remove duplicated conclusion sentences without changing structured reasoning.")
    parser.add_argument("paths", nargs="*", type=Path, help="Optional assessment files to inspect.")
    args = parser.parse_args()
    changed_paths = []

    paths = args.paths or ASSESSMENTS.glob("calc2-*.yaml")
    for path in paths:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            # A malformed legacy file is left for a focused syntax repair rather
            # than risking a lossy rewrite during explanation enrichment.
            continue
        if data.get("topicId") not in TOPICS or data.get("assessmentType") not in {"workedExample", "quiz", "test"}:
            continue
        olympiad = data.get("authoring", {}).get("difficultyTier") == "olympiad"
        convergence_topics = {"convergence-tests", "ratio-root-tests", "alternating-series", "absolute-conditional-convergence", "geometric-telescoping-series"}
        power_topics = {"power-series", "taylor-maclaurin", "series-approximation-error", "power-taylor-review"}
        foundation_topics = {"sequences-series", "sequence-fundamentals", "series-fundamentals", "arithmetic-series", "infinite-series-review"}
        feedback = power_taylor_feedback if data.get("topicId") in power_topics else foundations_feedback if data.get("topicId") in foundation_topics else convergence_feedback
        changed = False
        if data.get("assessmentType") == "workedExample":
            for example in data.get("workedExamples", []):
                for step in example.get("steps", []):
                    changed = (remove_repeated_conclusions(step) if args.repair_repetition else enrich(step, False, feedback)) or changed
        else:
            for question in data.get("questions", []):
                changed = (remove_repeated_conclusions(question) if args.repair_repetition else enrich(question, olympiad, feedback)) or changed
        if changed:
            changed_paths.append(path)
            if args.apply:
                path.write_text(yaml.dump(data, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8")

    action = "Updated" if args.apply else "Would update"
    for path in changed_paths:
        print(f"{action}: {path.resolve().relative_to(ROOT)}")


if __name__ == "__main__":
    main()

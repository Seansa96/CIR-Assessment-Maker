"""Create the first four original AoPS Volume 1 reference files and question banks.

The local PDF is used only for chapter location and instructional concepts. Questions,
examples, and prose produced here are original authoring material.
"""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assessment-reference" / "aops-volume-1"

CHAPTERS = [
    (1, "exponents-and-logarithms", "Exponents and Logarithms", "aops-exponents-logarithms", "pdf 15-26; printed 1-12", ["integer exponent laws", "fractional exponents and radicals", "rationalizing denominators", "logarithms as inverse exponents"], "Rewrite to a common base before comparing powers; state domain restrictions before applying a logarithm or an even root."),
    (2, "complex-numbers", "Complex Numbers", "aops-complex-numbers", "pdf 27-30; printed 13-16", ["the imaginary unit", "addition and multiplication", "powers of i", "real and imaginary parts"], "Keep real and imaginary parts separate, and reduce powers of i modulo four before expanding large expressions."),
    (3, "linear-equations", "Linear Equations", "aops-linear-equations", "pdf 31-41; printed 17-27", ["one-variable equations", "two-variable systems", "word-problem translation", "checking solutions"], "Define variables and units first; solve algebraically, then substitute into each original condition."),
    (4, "proportions", "Proportions", "aops-proportions", "pdf 42-52; printed 28-38", ["direct variation", "inverse variation", "conversion factors", "percent change"], "Write the invariant ratio or product explicitly and preserve units; a percent change is measured relative to the original amount."),
]

DETAILS = {
1: r'''## Concept model

An exponent describes repeated multiplication, so exponent laws are consequences of grouping factors rather than rules to memorize independently. For a nonzero base $a$, multiplying $a^m$ and $a^n$ combines $m+n$ copies of the same factor; dividing removes copies and gives $a^{m-n}$. A negative exponent records a reciprocal, not a negative value: $a^{-n}=1/a^n$. The zero exponent follows from $a^m/a^m=1=a^{m-m}$, so it requires $a\ne0$.

Fractional exponents connect powers to roots: $a^{p/q}$ means take a real $q$th root when defined, then raise it to the $p$th power. The order matters when signs or even roots are involved. In real-number work, an even root needs a nonnegative radicand, and $\sqrt{x^2}=|x|$, not automatically $x$. Rationalizing a denominator is a representation choice: multiply numerator and denominator by a factor that turns the denominator into a rational expression without changing the value.

A logarithm is an inverse-exponent statement: $\log_b x=y$ exactly when $b^y=x$, with $b>0$, $b\ne1$, and $x>0$. Its product, quotient, and power rules come from exponent laws. They apply to products or quotients inside one logarithm; they do not distribute across addition.

## Strategy selection

1. Normalize bases before comparing or combining powers. Factor numerical bases or use a substitution such as $u=a^k$ when repeated powers occur.
2. For radicals, identify the index, sign domain, and whether a perfect-power factor can leave the radical.
3. For logarithmic equations, first state the positive-argument conditions; convert to exponential form when it reveals the unknown cleanly.
4. Verify by evaluating the original expression or equation, especially after squaring, taking roots, or clearing denominators.

## Misconceptions to target

- $a^m+a^n$ cannot be changed to $a^{m+n}$.
- $(a+b)^n$ is not generally $a^n+b^n$.
- $\log(x+y)$ does not split into two logs.
- An equation such as $x^2=c$ may have two real solutions, while $\sqrt{c}$ names the principal nonnegative root.

## Lesson-authoring moves

Use one trace that asks learners to justify each exponent law from factors, one domain-check example involving an even root or log argument, and one method-selection comparison between factoring, common-base rewriting, and a logarithm. Good checks ask which transformation is legal and why.''',
2: r'''## Concept model

Complex numbers extend the real number system so that $x^2+1=0$ has solutions. Define $i$ by $i^2=-1$; every complex number can then be written uniquely as $a+bi$, where $a$ and $b$ are real. Equality is componentwise: $a+bi=c+di$ only when $a=c$ and $b=d$. This representation is the invariant behind addition, subtraction, and simplification.

Addition combines like components. Multiplication uses ordinary distributive algebra followed by $i^2=-1$. The powers of $i$ repeat with period four: $i,i^2,i^3,i^4=1$, so a large exponent should be reduced modulo four. Conjugates, $a+bi$ and $a-bi$, have a real product $a^2+b^2$; this gives a principled way to divide by a nonreal denominator without changing the value.

## Strategy selection

1. Rewrite every expression in $a+bi$ form before comparing, adding, or multiplying.
2. For a power of $i$, reduce the exponent modulo four before doing any other work.
3. For a quotient with denominator $a+bi$, multiply top and bottom by $a-bi$, then collect real and imaginary parts.
4. For square roots of negative reals, factor out $-1$ and use $\sqrt{-1}=i$; do not use real-root rules outside their domain.

## Misconceptions to target

- $\sqrt{ab}=\sqrt a\sqrt b$ needs domain care; applying it blindly to negative factors creates contradictions.
- $i$ is not a variable that can be cancelled or assigned a real value.
- A complex number is zero only if both components are zero.
- $(a+bi)^2$ requires the middle term $2abi$.

## Lesson-authoring moves

Build a trace from a product to standard form, then ask learners to identify the exact step where $i^2$ becomes $-1$. Include an equality check, a high-power cycle question, and a conjugate-based division example. Verification should multiply a proposed quotient back by the original denominator.''',
3: r'''## Concept model

A linear equation states that a variable appears only to the first power after simplification. Solving is not “moving terms”; it is applying the same reversible operation to both sides until the variable is isolated. In a system, a solution is an ordered pair that makes every equation true simultaneously. Elimination and substitution are two representations of the same constraint intersection.

Word problems require modeling before algebra. Choose variables with units, translate each sentence into an equation, and decide whether the requested answer is a variable, a total, a difference, or a rate. A valid algebraic result can still be invalid in context: a negative count, impossible time, or inconsistent unit is rejected by the original conditions.

## Strategy selection

1. Simplify each side, collect variable terms, and track any operation that may be nonreversible.
2. Use substitution when a variable is already isolated or has coefficient $1$; use elimination when coefficients can be matched cheaply.
3. For word problems, make a relationship table for rate-time-distance, price-quantity-total, or mixture amount-concentration before writing equations.
4. Check each candidate in every original equation and in the story constraints.

## Misconceptions, classification, and traps

After simplification, $0=0$ means every value satisfying the domain works; a false statement such as $0=5$ means no solution. Do not divide by an expression containing a variable without recording that it may be zero. Do not add equations unless the resulting combination preserves the intended system relationship.

## Lesson-authoring moves

Teach one one-variable equation with fractions, one system solved two ways, and one word problem whose units expose an incorrect setup. Embedded checks should ask learners to name the invariant (“both sides remain equal”), choose elimination versus substitution, and reject a contextually impossible answer.''',
4: r'''## Concept model

A proportion is an equality of ratios. Direct variation has the invariant $y/x=k$ and model $y=kx$; inverse variation has invariant $xy=k$ and model $y=k/x$. The equation is more reliable than verbal shortcuts because it preserves which quantities grow together and which trade off. Conversion factors are ratios equal to one, so multiplying by them changes units without changing the underlying quantity.

Percent is a relative comparison: percent change is $(\text{new}-\text{old})/\text{old}\times100\%$. The denominator is the original reference amount, which explains why a 20% increase followed by a 20% decrease does not restore the starting value. Units are part of every proportional statement and should cancel visibly.

## Strategy selection

1. Determine whether the situation keeps a ratio constant, keeps a product constant, or merely compares two quantities once.
2. Write the invariant with units before substituting numbers.
3. Use a chain of conversion factors whose unwanted units cancel; invert a factor when its unit orientation is wrong.
4. For percent, identify the baseline, compute the absolute change if useful, and convert back to a meaningful final quantity.

## Misconceptions to target

- Cross multiplication is a consequence of an equality of fractions, not a replacement for deciding whether a relationship is proportional.
- Inverse variation is not “subtracting when one grows.”
- Percentages cannot be added unless they share the same reference amount.
- A conversion factor with unmatched units signals an inverted or missing ratio.

## Lesson-authoring moves

Contrast direct and inverse variation using the same numerical table, require unit cancellation in a conversion problem, and include a successive-percent-change counterexample. Strong checks ask for the invariant, the baseline quantity, and a verification by substituting into the original relationship.'''
}

def ref(ch, slug, title, topic, pages, concepts, guidance):
    sections = "\n".join(f"- **{c.title()}**: recognize the structure, name the relevant condition, and verify the result in the original setting." for c in concepts)
    return f"""# Chapter {ch}: {title}

## Source scope

- Local source: *The Art of Problem Solving, Volume 1: The Basics*.
- Location: {pages}.
- Current AoPS topic: `{topic}`.
- This file is an original instructional paraphrase. It records concepts and authoring guidance; it does not reproduce source exercises, solutions, diagrams, or extended passages.

## Purpose and prerequisites

This chapter develops reliable symbolic reasoning before learners move to mixed contest problems. Learners should be comfortable with arithmetic operations, signed numbers, and reading an equation as a claim that must be checked.

{DETAILS[ch]}

## Assessment skills and evidence

- `apply-{slug}`: carries out a correct calculation or derivation.
- `select-{slug}-method`: names a method and the structural cue that justifies it.
- `check-{slug}-restrictions`: identifies domains, units, or exceptional cases before transforming.
- `verify-{slug}-solutions`: checks a candidate against the original representation.

Concept lessons should teach the reason before the shortcut; quizzes should test a trace, a restriction, or a competing method rather than a vocabulary definition.
"""

def q(chapter, slug, topic, n, tier):
    # Original, parameterized prompts with distinct numeric data and solution guidance.
    a, b, c = n + 2, n + 3, n + 5
    if chapter == 1:
        prompt = f"Simplify the original expression $({a}^{{{b}}}\\cdot {a}^{{-{n%4+1}}})/{a}^{{{c%3+1}}}$ as a single power of {a}."
        ans = str(b - (n % 4 + 1) - (c % 3 + 1))
        outline = "Combine exponents only after confirming the base is identical; subtract exponents for division."
        trap = "Adding exponents during division or cancelling bases across a sum."
    elif chapter == 2:
        prompt = f"Compute the original complex number $( {a}+{b}i )({c}-{n%5+1}i)$ and state its real and imaginary parts."
        real = a*c + b*(n%5+1); imag = b*c - a*(n%5+1)
        ans = f"{real}+{imag}i"
        outline = "Distribute all four products and replace $i^2$ with $-1$ before collecting parts."
        trap = "Treating $i^2$ as $1$ or combining real and imaginary parts prematurely."
    elif chapter == 3:
        x = n + 4; y = n + 7
        prompt = f"Solve the original system $x+y={x+y}$ and $2x-y={2*x-y}$, then verify both equations."
        ans = f"x={x}, y={y}"
        outline = "Eliminate one variable by addition or substitution, then check both original equations."
        trap = "Checking only the transformed equation or changing one side without the other."
    else:
        value = (n + 4) * (n % 3 + 2)
        prompt = f"A quantity varies directly with $x$. If it is {value} when $x={n+4}$, find its value when $x={n+7}$."
        ans = str((n % 3 + 2) * (n + 7))
        outline = "Find the constant of proportionality from the first pair, then apply it to the new input."
        trap = "Adding a fixed amount when the relationship is multiplicative."
    archetypes = ["recognition", "direct-application", "condition-check", "changed-condition", "synthesis"]
    return {"id": f"aops-v1-ch{chapter:02d}-q{n:03d}", "skillIds": [f"apply-{slug}", f"check-{slug}-restrictions"], "archetype": archetypes[(n-1) % len(archetypes)], "difficulty": tier, "questionType": "freeResponse", "prompt": prompt, "answer": ans, "solutionOutline": outline, "commonTrap": trap, "intendedUse": "quiz-test-bank"}

def bank(ch, slug, title, topic, pages):
    items = []
    for n in range(1, 41):
        tier = "foundational" if n <= 12 else "multi-step" if n <= 28 else "contest-transfer" if n <= 36 else "proof-strategy"
        items.append(q(ch, slug, topic, n, tier))
    return {"metadata": {"id": f"aops-v1-ch{ch:02d}-{slug}-bank", "title": f"AoPS Volume 1 Chapter {ch}: {title} Question Bank", "chapter": ch, "topicIds": [topic], "sourcePageRange": pages, "originalAuthoring": True, "distribution": {"foundational": 12, "multi-step": 16, "contest-transfer": 8, "proof-strategy": 4}}, "items": items}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = ["# AoPS Volume 1 Reference Index", "", "Local source: *The Art of Problem Solving, Volume 1: The Basics* (user-provided PDF).", "", "Files are original paraphrases and original question banks. Do not copy source exercises, solutions, or extended passages.", "", "## Batch 1"]
    for ch, slug, title, topic, pages, concepts, guidance in CHAPTERS:
        (OUT / f"chapter-{ch:02d}-{slug}.md").write_text(ref(ch, slug, title, topic, pages, concepts, guidance), encoding="utf-8")
        (OUT / f"chapter-{ch:02d}-{slug}-question-bank.yaml").write_text(yaml.safe_dump(bank(ch, slug, title, topic, pages), sort_keys=False, allow_unicode=True), encoding="utf-8")
        index.append(f"- Chapter {ch}: [{title}](chapter-{ch:02d}-{slug}.md) -> `{topic}` ({pages})")
    (OUT / "aops-volume-1-index.md").write_text("\n".join(index) + "\n", encoding="utf-8")

if __name__ == "__main__": main()

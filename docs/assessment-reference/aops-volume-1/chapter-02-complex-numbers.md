# Chapter 2: Complex Numbers

## Source scope

- Local source: *The Art of Problem Solving, Volume 1: The Basics*.
- Location: pdf 27-30; printed 13-16.
- Current AoPS topic: `aops-complex-numbers`.
- This file is an original instructional paraphrase. It records concepts and authoring guidance; it does not reproduce source exercises, solutions, diagrams, or extended passages.

## Purpose and prerequisites

This chapter develops reliable symbolic reasoning before learners move to mixed contest problems. Learners should be comfortable with arithmetic operations, signed numbers, and reading an equation as a claim that must be checked.

## Concept model

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

Build a trace from a product to standard form, then ask learners to identify the exact step where $i^2$ becomes $-1$. Include an equality check, a high-power cycle question, and a conjugate-based division example. Verification should multiply a proposed quotient back by the original denominator.

## Assessment skills and evidence

- `apply-complex-numbers`: carries out a correct calculation or derivation.
- `select-complex-numbers-method`: names a method and the structural cue that justifies it.
- `check-complex-numbers-restrictions`: identifies domains, units, or exceptional cases before transforming.
- `verify-complex-numbers-solutions`: checks a candidate against the original representation.

Concept lessons should teach the reason before the shortcut; quizzes should test a trace, a restriction, or a competing method rather than a vocabulary definition.

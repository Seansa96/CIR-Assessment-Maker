# Chapter 1: Exponents and Logarithms

## Source scope

- Local source: *The Art of Problem Solving, Volume 1: The Basics*.
- Location: pdf 15-26; printed 1-12.
- Current AoPS topic: `aops-exponents-logarithms`.
- This file is an original instructional paraphrase. It records concepts and authoring guidance; it does not reproduce source exercises, solutions, diagrams, or extended passages.

## Purpose and prerequisites

This chapter develops reliable symbolic reasoning before learners move to mixed contest problems. Learners should be comfortable with arithmetic operations, signed numbers, and reading an equation as a claim that must be checked.

## Concept model

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

Use one trace that asks learners to justify each exponent law from factors, one domain-check example involving an even root or log argument, and one method-selection comparison between factoring, common-base rewriting, and a logarithm. Good checks ask which transformation is legal and why.

## Assessment skills and evidence

- `apply-exponents-and-logarithms`: carries out a correct calculation or derivation.
- `select-exponents-and-logarithms-method`: names a method and the structural cue that justifies it.
- `check-exponents-and-logarithms-restrictions`: identifies domains, units, or exceptional cases before transforming.
- `verify-exponents-and-logarithms-solutions`: checks a candidate against the original representation.

Concept lessons should teach the reason before the shortcut; quizzes should test a trace, a restriction, or a competing method rather than a vocabulary definition.

# Chapter 8: What Numbers Really Are

## Source scope

- Local source: *The Art of Problem Solving, Volume 1: The Basics*.
- Location: pdf 89-94; printed 75-80.
- Current AoPS topic: `aops-number-systems`.
- This file is an original paraphrase for curriculum authoring; it does not reproduce source exercises, solutions, or prose.

## Purpose and prerequisites

Number-system questions make implicit assumptions explicit. Learners should know integer arithmetic, fractions, decimals, and square roots. The chapter organizes the nesting $\mathbb N\subset\mathbb Z\subset\mathbb Q\subset\mathbb R\subset\mathbb C$ and emphasizes that a classification claim needs a definition or proof, not a calculator display.

## Concept model

Natural numbers are positive counting numbers (a course must state whether it includes zero); integers extend them with zero and negatives. A rational number is a quotient $p/q$ of integers with $q\ne0$. In lowest terms, numerator and denominator share no positive factor greater than one. A terminating decimal is rational, and a repeating decimal is rational because a power-of-ten shift lets its repeating tail be subtracted away. Conversely, a rational decimal must terminate or repeat.

Real numbers include rationals and irrationals such as $\sqrt2$; complex numbers add multiples of $i$. The standard proof that $\sqrt2$ is irrational assumes $p/q$ is a lowest-terms representation, squares it, and forces both $p$ and $q$ even, contradicting lowest terms. The proof works because parity and prime factors are tracked precisely; asserting that a decimal “looks nonrepeating” is not proof of irrationality.

## Strategy selection

1. Identify the smallest relevant number set and use its definition: a quotient for rationality, a perfect-square test for many square roots, or a closure property for operations.
2. Convert a terminating decimal by its place value. Convert a repeating decimal by setting $x$ equal to the decimal, multiplying by a suitable power of ten, and subtracting.
3. To prove an irrationality statement, assume a fraction is in lowest terms and seek a divisibility contradiction, usually with a prime factor.
4. Separate statements about real solutions from statements about complex solutions; the allowed universe changes the answer.

## Misconceptions to target

- Not every decimal approximation establishes irrationality or equality.
- A fraction is rational even if its decimal expansion is long; denominator zero is never allowed.
- An irrational number plus an irrational number can be rational, so closure claims need counterexamples or conditions.
- $\sqrt{a+b}$ usually cannot be split into separate square roots.
- “Not an integer” does not imply irrational: $1/2$ is rational.

## Lesson-authoring moves

Have learners classify a mixed list by the smallest set, then justify each boundary case. Include a repeating-decimal derivation and a deliberately flawed irrationality proof whose lowest-terms step is missing. Ask for counterexamples to careless closure claims, and distinguish a number’s exact category from a decimal approximation.

## Assessment skills and evidence

- `classify-number-sets`: identifies the smallest applicable set with justification.
- `convert-decimals-and-fractions`: converts terminating and repeating decimals exactly.
- `prove-irrationality`: uses a lowest-terms contradiction coherently.
- `reason-about-closure`: tests a proposed closure statement with proof or counterexample.
- `check-number-system-restrictions`: states denominator, root, and real-versus-complex conditions.

# Chapter 7: Special Factorizations and Clever Manipulations

## Source scope

- Local source: *The Art of Problem Solving, Volume 1: The Basics*.
- Location: pdf 81-88; printed 67-74.
- Current AoPS topic: `aops-special-factorizations`.
- This is original instructional guidance, not copied source wording, exercises, or derivations.

## Purpose and prerequisites

This chapter teaches algebra as a way to expose structure. Learners should expand and factor basic polynomials. The practical purpose is to avoid expensive arithmetic and unnecessary solving: a carefully chosen identity can turn a large difference of powers, a symmetric expression, or a reciprocal condition into a short calculation.

## Concept model

Core identities include $a^2-b^2=(a-b)(a+b)$, $a^3-b^3=(a-b)(a^2+ab+b^2)$, and $a^3+b^3=(a+b)(a^2-ab+b^2)$. The square identities $(a+b)^2=a^2+2ab+b^2$ and $(a-b)^2=a^2-2ab+b^2$ convert information about a sum and a product into information about squares. These are equations valid for every permitted input; they are tools for rewriting, not patterns to be used by visual resemblance alone.

Clever manipulation means deciding what expression would connect known information to a target. If $x+1/x$ is known, squaring gives $x^2+1/x^2$ after subtracting 2; cubing supplies $x^3+1/x^3$ after accounting for $3(x+1/x)$. Multiplying through by a common denominator can reveal a factorization, but only when the denominators are nonzero. Symmetry in $a,b$ often suggests tracking $a+b$ and $ab$ rather than solving for $a$ and $b$ separately.

## Strategy selection

1. Before expanding, scan for a difference of squares, sum/difference of cubes, a near-square, or a symmetric pair.
2. Compare the target with the information given. Add and subtract a deliberately chosen term only if it creates a known identity.
3. With reciprocal expressions, first state nonzero restrictions and clear denominators in a reversible way.
4. Verify an identity by expansion when introducing it, and verify a numerical answer against the given relation.

## Misconceptions to target

- $a^2+b^2$ does not factor over the reals as $(a+b)(a-b)$.
- A difference of cubes has a plus in its quadratic factor; a sum of cubes has a minus.
- Cancelling terms across addition is invalid; factor first.
- Symmetric information may determine a target without determining either variable individually.
- Multiplying by a variable expression requires noting when it could be zero.

## Lesson-authoring moves

Pair an unwieldy numerical difference of squares with its short factored calculation. Follow a reciprocal-sum question by asking learners to build the square identity instead of solving for the variable. Include a false factorization and require expansion to diagnose it. Strong checks ask which term to add, which invariant pair $(a+b,ab)$ is useful, or why a denominator restriction matters.

## Assessment skills and evidence

- `recognize-special-factorizations`: selects and applies an identity from structure.
- `manipulate-symmetric-expressions`: uses sum/product information without unnecessary solving.
- `clear-denominators-safely`: records and preserves nonzero restrictions.
- `design-algebraic-rewrites`: chooses a purposeful added term or transformation.
- `verify-algebraic-identities`: expands or tests a claim to establish validity.


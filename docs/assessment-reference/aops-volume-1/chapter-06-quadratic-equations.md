# Chapter 6: Quadratic Equations

## Source scope

- Local source: *The Art of Problem Solving, Volume 1: The Basics*.
- Location: pdf 66-80; printed 52-66.
- Current AoPS topic: `aops-quadratic-equations`.
- This original paraphrase records reusable reasoning and does not copy source problems or solutions.

## Purpose and prerequisites

Quadratics appear whenever a changing quantity depends on a product, an area, a square, or a two-step process. Learners should manipulate linear equations and factor integers. The aim is not to apply a formula automatically: it is to recognize a second-degree relationship, put it into a solvable form, select an efficient method, and retain only solutions valid in the original situation.

## Concept model

A quadratic polynomial has the form $ax^2+bx+c$ with $a\ne0$. Its roots are values of $x$ making the polynomial zero. Factoring uses the zero-product property: if $(ux+v)(wx+y)=0$, one factor must be zero. For a monic quadratic with roots $r,s$, expansion gives $x^2-(r+s)x+rs$; the sum and product of roots therefore encode the middle and constant coefficients.

When factoring is not useful, completing the square gives the quadratic formula $x=(-b\pm\sqrt{b^2-4ac})/(2a)$. The discriminant $b^2-4ac$ predicts real-root behavior: positive gives two distinct real roots, zero a repeated real root, and negative no real roots (but two conjugate complex roots when complex numbers are allowed). A disguised quadratic often becomes ordinary after a substitution such as $u=x^2$, provided the substitution is reversed and its restrictions are checked.

## Strategy selection

1. Rearrange to one side equal to zero and identify $a,b,c$ without losing signs.
2. Factor when integer or simple rational factors are visible; use the formula or completing the square when they are not.
3. For an expression with repeated structure, name the repeated expression $u$ before expanding into a higher-degree mess.
4. For equations involving radicals or denominators, record restrictions first and substitute every candidate into the original equation after squaring or clearing a denominator.

## Misconceptions to target

- The quadratic formula’s $\pm$ produces two branches, not a decorative symbol.
- $\sqrt{b^2}$ is $|b|$, and a square root equation can introduce extraneous candidates after squaring.
- A negative discriminant means no real roots, not no complex roots.
- Factoring a polynomial is different from dividing an equation by an expression that might be zero.
- Vieta-style root relations apply to the correctly normalized polynomial, including signs.

## Lesson-authoring moves

Present the same quadratic in factorable, completed-square, and formula forms so learners can compare information each representation reveals. Include a substitution problem where one algebraic root fails the substitution’s domain, and a radical equation whose check removes an extraneous value. Ask learners to explain the method cue rather than merely name a formula.

## Assessment skills and evidence

- `solve-quadratic-equations`: factors, completes squares, or applies the formula correctly.
- `analyze-discriminants`: predicts number and type of roots.
- `use-quadratic-substitution`: reduces a disguised quadratic and reverses it safely.
- `apply-root-coefficient-relations`: connects roots with coefficients.
- `verify-quadratic-solutions`: checks candidates against original restrictions.


# Olympiad Algebra Reference

Olympiad algebra heavily focuses on structural manipulation, bounding, and functional relationships. Standard tools from high school algebra are often stretched to their theoretical limits.

## 1. Inequalities
Inequalities are a massive part of Olympiad mathematics, especially at the USAMO/IMO level.
- **AM-GM (Arithmetic Mean - Geometric Mean)**: For non-negative reals $x_1, x_2, \dots, x_n$, $\frac{x_1 + \dots + x_n}{n} \ge \sqrt[n]{x_1 \dots x_n}$. Equality holds iff all $x_i$ are equal.
- **Cauchy-Schwarz Inequality**: $(a_1^2 + \dots + a_n^2)(b_1^2 + \dots + b_n^2) \ge (a_1b_1 + \dots + a_nb_n)^2$. Powerful for dealing with fractions via Titu's Lemma (Engel's Form).
- **Jensen's Inequality**: For a convex function $f$, the secant line lies above the graph: $\frac{f(x_1) + \dots + f(x_n)}{n} \ge f\left(\frac{x_1 + \dots + x_n}{n}\right)$. Reverse the inequality for concave functions.
- **Advanced Smoothing**: Muirhead's Inequality and Schur's Inequality are used for homogenizing and bounding symmetric polynomials.

## 2. Polynomials and Roots
- **Vieta's Formulas**: Relates the coefficients of a polynomial to sums and products of its roots. For $P(x) = a_n x^n + \dots + a_0$, the sum of the roots taken $k$ at a time is $(-1)^k \frac{a_{n-k}}{a_n}$.
- **Newton's Sums**: A recursive formula to find the sum of the $k$-th powers of the roots of a polynomial. Very useful when Vieta's formulas become too messy to compute directly.
- **Symmetric Polynomials**: Any symmetric polynomial can be expressed in terms of the elementary symmetric polynomials (which are the components of Vieta's formulas).

## 3. Functional Equations
A functional equation asks to find all functions $f(x)$ satisfying a given relation.
- **Cauchy's Functional Equation**: The solution to $f(x+y) = f(x) + f(y)$ for continuous (or monotonic, or bounded) functions over the reals is $f(x) = cx$.
- **Standard Substitutions**: $x=y=0$, $x=y$, $x=-y$. The goal is to establish injectivity, surjectivity, parity (odd/even), or fixed points.
- **Symmetry Swaps**: If an equation is symmetric in $x$ and $y$, swapping them often yields a new equation that can be subtracted from the original.

## Common Problem Architectures
When authoring `workedExample` assessments, guide the learner to:
1. (For inequalities) Check the equality conditions first to guess the bound. Homogenize if necessary.
2. (For polynomials) Decide between bashing with Vieta's or setting up a Newton's Sums recurrence.
3. (For functional equations) Plug in zeroes or establish injectivity/surjectivity as step 1.

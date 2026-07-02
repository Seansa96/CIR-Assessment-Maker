# Olympiad Trigonometry Reference

This reference covers the advanced trigonometric techniques necessary for competitive math up to the AIME and USAMO levels, heavily inspired by classical texts such as "103 Trigonometry Problems".

## 1. Advanced Identities and Bashes
- **Sum-to-Product & Product-to-Sum**: Critical for telescoping series involving sines and cosines. 
  - $\sin A \pm \sin B = 2 \sin(\frac{A \pm B}{2}) \cos(\frac{A \mp B}{2})$
- **Telescoping Sums**: Recognizing patterns like $\frac{1}{\sin x} - \frac{1}{\tan x} = \tan(x/2)$ to collapse massive series.
- **Chebyshev Polynomials**: Expressing $\cos(nx)$ as a polynomial of $\cos(x)$. Useful for bounding problems and finding roots of specific high-degree polynomials.

## 2. Complex Numbers in Trigonometry
- **Euler's Formula**: $e^{i\theta} = \cos \theta + i \sin \theta$. Often allows geometry and trigonometry problems to be solved purely algebraically.
- **De Moivre's Theorem**: $(\cos \theta + i \sin \theta)^n = \cos(n\theta) + i \sin(n\theta)$. Used for deriving multiple-angle formulas quickly.
- **Roots of Unity Filter**: Using the sum of roots of unity to isolate terms in a binomial expansion, which frequently appears disguised as a trig sum.

## 3. Trigonometric Substitutions in Algebra
- A powerful technique for solving inequalities or systems of equations.
- **Substitution 1**: If $x^2 + y^2 = 1$, let $x = \cos \theta, y = \sin \theta$.
- **Substitution 2**: If $x,y,z > 0$ and $xy + yz + zx = 1$, let $x = \tan A, y = \tan B, z = \tan C$ where $A+B+C = 90^\circ$.
- **Substitution 3**: If $x+y+z = xyz$, let $x = \tan A, y = \tan B, z = \tan C$ where $A+B+C = 180^\circ$.

## 4. Geometric Applications
- **Law of Sines / Law of Cosines**: Fundamental bashes for side-angle-side problems.
- **Tangent Identities**: In $\triangle ABC$, $\tan A + \tan B + \tan C = \tan A \tan B \tan C$.

## Common Problem Architectures
When authoring `workedExample` assessments, guide the learner to:
1. Identify the structural form (e.g., polynomial roots vs. telescoping sum).
2. Choose the correct domain (real vs. complex).
3. Apply De Moivre's or Euler's if the powers are high.
4. Simplify using sum-to-product.

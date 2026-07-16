# Chapter 7: Techniques of Integration

## Introduction

In Differential Calculus, we learned that every function formed by combining basic elementary functions (polynomials, exponentials, logarithms, trigonometric, and inverse trigonometric functions) using arithmetic operations or composition has a derivative that is also an elementary function. We can compute these derivatives mechanically using the Product, Quotient, and Chain rules.

However, Integral Calculus is fundamentally different. The antiderivative of an elementary function is not guaranteed to be an elementary function. For example, the function $f(x) = e^{-x^2}$ is crucial in probability (as the bell curve), yet its antiderivative cannot be expressed in terms of any finite combination of elementary functions. We say its antiderivative is "nonelementary."

When an elementary antiderivative *does* exist, finding it is often more of an art than a mechanical science. While differentiation is systematic, integration requires pattern recognition, strategic substitutions, and algebraic manipulation. This chapter is dedicated to developing a robust toolkit for finding antiderivatives.

---

## 7.1 Integration by Parts

### 7.1.1 The Theory and Formula
Every differentiation rule has a corresponding integration rule. The Substitution Rule corresponds to the Chain Rule. The rule that corresponds to the Product Rule is called **Integration by Parts**.

Let $f(x)$ and $g(x)$ be differentiable functions. The Product Rule states:
$$ \frac{d}{dx} [f(x)g(x)] = f(x)g'(x) + g(x)f'(x) $$

If we integrate both sides with respect to $x$, we obtain:
$$ \int \frac{d}{dx} [f(x)g(x)] \, dx = \int f(x)g'(x) \, dx + \int g(x)f'(x) \, dx $$
$$ f(x)g(x) = \int f(x)g'(x) \, dx + \int g(x)f'(x) \, dx $$

Rearranging this equation gives us the standard formula for Integration by Parts:
$$ \int f(x)g'(x) \, dx = f(x)g(x) - \int g(x)f'(x) \, dx $$

To make this easier to remember, we typically use the differentials $u = f(x)$ and $v = g(x)$. Then $du = f'(x) \, dx$ and $dv = g'(x) \, dx$. The formula becomes:
> **Integration by Parts Formula:**
> $$ \int u \, dv = uv - \int v \, du $$

### 7.1.2 Strategy for Choosing $u$ and $dv$
The goal of integration by parts is to take a difficult integral $\int u \, dv$ and transform it into an easier integral $\int v \, du$. 
Therefore, our choice of $u$ and $dv$ is critical:
1. $dv$ must be a portion of the integrand that is relatively easy to integrate to find $v$.
2. $u$ must be a portion of the integrand whose derivative $du$ makes the resulting integral $\int v \, du$ simpler than the original.

A highly effective heuristic for choosing $u$ is the **LIATE** acronym. You should choose $u$ to be the function that appears highest on this list:
- **L**ogarithmic functions ($\ln x$, $\log_2 x$)
- **I**nverse trigonometric functions ($\arctan x$, $\arcsin x$)
- **A**lgebraic functions ($x^2$, $3x^5$, polynomials)
- **T**rigonometric functions ($\sin x$, $\cos x$)
- **E**xponential functions ($e^x$, $2^x$)

The remaining part of the integrand, along with $dx$, becomes $dv$.

### 7.1.3 Worked Examples

**Example 1: Basic Application**
Evaluate $\int x \cos x \, dx$.

*Solution:*
The integrand is the product of an algebraic function ($x$) and a trigonometric function ($\cos x$). According to LIATE, Algebraic comes before Trigonometric. 
Let $u = x$ and $dv = \cos x \, dx$.
Differentiating $u$ and integrating $dv$:
$$ du = dx $$
$$ v = \sin x $$
Apply the formula:
$$ \int u \, dv = uv - \int v \, du $$
$$ \int x \cos x \, dx = x \sin x - \int \sin x \, dx $$
$$ = x \sin x - (-\cos x) + C = x \sin x + \cos x + C $$

**Example 2: When $dv = dx$**
Evaluate $\int \ln x \, dx$.

*Solution:*
This doesn't initially look like a product, but we can treat it as a product of $\ln x$ and $1$. By LIATE, Logarithmic is at the top.
Let $u = \ln x$ and $dv = dx$.
Then $du = \frac{1}{x} \, dx$ and $v = x$.
$$ \int \ln x \, dx = x \ln x - \int x \left(\frac{1}{x}\right) \, dx $$
$$ = x \ln x - \int 1 \, dx = x \ln x - x + C $$

**Example 3: Repeated Integration by Parts**
Evaluate $\int t^2 e^t \, dt$.

*Solution:*
Let $u = t^2$ and $dv = e^t \, dt$.
Then $du = 2t \, dt$ and $v = e^t$.
$$ \int t^2 e^t \, dt = t^2 e^t - 2\int t e^t \, dt $$
We are left with an integral $\int t e^t \, dt$ which still requires integration by parts. 
Let $U = t$ and $dV = e^t \, dt$.
Then $dU = dt$ and $V = e^t$.
$$ \int t e^t \, dt = t e^t - \int e^t \, dt = t e^t - e^t $$
Substitute this back into our original equation:
$$ \int t^2 e^t \, dt = t^2 e^t - 2(t e^t - e^t) + C = t^2 e^t - 2t e^t + 2e^t + C $$

### 7.1.4 The "Boomerang" Integral
Some integrals will never simplify down to a basic elementary form, but instead cycle back to their original form. We can use this to solve for the integral algebraically.

**Example 4: The Boomerang**
Evaluate $I = \int e^x \sin x \, dx$.

*Solution:*
Let $u = \sin x$ and $dv = e^x \, dx$. (Note: Choosing $u=e^x$ works equally well here).
$du = \cos x \, dx$ and $v = e^x$.
$$ I = e^x \sin x - \int e^x \cos x \, dx $$
Apply parts again to the new integral. Let $U = \cos x$ and $dV = e^x \, dx$.
$dU = -\sin x \, dx$ and $V = e^x$.
$$ \int e^x \cos x \, dx = e^x \cos x - \int e^x (-\sin x) \, dx = e^x \cos x + \int e^x \sin x \, dx $$
Notice that the integral on the right is exactly our original integral $I$. Substitute this back:
$$ I = e^x \sin x - (e^x \cos x + I) $$
$$ I = e^x \sin x - e^x \cos x - I $$
Add $I$ to both sides:
$$ 2I = e^x (\sin x - \cos x) $$
$$ I = \frac{e^x}{2}(\sin x - \cos x) + C $$

### 7.1.5 Reduction Formulas
A reduction formula allows us to express an integral involving a power $n$ in terms of an integral involving a lower power (like $n-1$ or $n-2$).

**Example 5: Sine Reduction Formula**
Prove the reduction formula for $\int \sin^n x \, dx$, where $n \ge 2$:
$$ \int \sin^n x \, dx = -\frac{1}{n} \cos x \sin^{n-1} x + \frac{n-1}{n} \int \sin^{n-2} x \, dx $$

*Proof:*
Write $\sin^n x = \sin^{n-1} x \sin x$.
Let $u = \sin^{n-1} x$ and $dv = \sin x \, dx$.
$du = (n-1)\sin^{n-2} x \cos x \, dx$ and $v = -\cos x$.
$$ \int \sin^n x \, dx = -\cos x \sin^{n-1} x - \int (-\cos x)(n-1)\sin^{n-2} x \cos x \, dx $$
$$ = -\cos x \sin^{n-1} x + (n-1) \int \sin^{n-2} x \cos^2 x \, dx $$
Use the identity $\cos^2 x = 1 - \sin^2 x$:
$$ = -\cos x \sin^{n-1} x + (n-1) \int \sin^{n-2} x (1 - \sin^2 x) \, dx $$
$$ = -\cos x \sin^{n-1} x + (n-1) \int \sin^{n-2} x \, dx - (n-1) \int \sin^n x \, dx $$
Let $I = \int \sin^n x \, dx$. The equation is:
$$ I = -\cos x \sin^{n-1} x + (n-1) \int \sin^{n-2} x \, dx - (n-1)I $$
$$ I + (n-1)I = -\cos x \sin^{n-1} x + (n-1) \int \sin^{n-2} x \, dx $$
$$ nI = -\cos x \sin^{n-1} x + (n-1) \int \sin^{n-2} x \, dx $$
Divide by $n$ to complete the proof.

---

## 7.2 Trigonometric Integrals

We can evaluate integrals involving powers of trigonometric functions by using a combination of trigonometric identities and the substitution rule.

### 7.2.1 Integrals of the form $\int \sin^m x \cos^n x \, dx$

**Case 1: The power of cosine is odd ($n = 2k + 1$).**
If $n$ is odd, we save one cosine factor to serve as the $du$ in our substitution, and convert the remaining even power of cosine into sines using the Pythagorean identity $\cos^2 x = 1 - \sin^2 x$.
$$ \int \sin^m x \cos^{2k+1} x \, dx = \int \sin^m x (\cos^2 x)^k \cos x \, dx = \int \sin^m x (1 - \sin^2 x)^k \cos x \, dx $$
Substitute $u = \sin x$, then $du = \cos x \, dx$.

**Case 2: The power of sine is odd ($m = 2k + 1$).**
If $m$ is odd, we save one sine factor and convert the remaining even power of sine into cosines using $\sin^2 x = 1 - \cos^2 x$.
$$ \int \sin^{2k+1} x \cos^n x \, dx = \int (\sin^2 x)^k \cos^n x \sin x \, dx = \int (1 - \cos^2 x)^k \cos^n x \sin x \, dx $$
Substitute $u = \cos x$, then $du = -\sin x \, dx$.
*(Note: If both powers are odd, either Case 1 or Case 2 can be used. It is usually easier to convert the smaller power).*

**Case 3: Both powers are even.**
If both $m$ and $n$ are even, we use the half-angle identities to reduce the degree of the integrand:
$$ \sin^2 x = \frac{1 - \cos(2x)}{2} $$
$$ \cos^2 x = \frac{1 + \cos(2x)}{2} $$
It is also frequently useful to use the double-angle identity for sine: $\sin x \cos x = \frac{1}{2}\sin(2x)$.

**Example 6: Odd Power of Cosine**
Evaluate $\int \sin^2 x \cos^3 x \, dx$.
*Solution:*
Since $n=3$ is odd, save one cosine factor:
$$ \int \sin^2 x \cos^2 x \cos x \, dx = \int \sin^2 x (1 - \sin^2 x) \cos x \, dx $$
Let $u = \sin x$, $du = \cos x \, dx$.
$$ \int u^2(1 - u^2) \, du = \int (u^2 - u^4) \, du = \frac{u^3}{3} - \frac{u^5}{5} + C = \frac{1}{3}\sin^3 x - \frac{1}{5}\sin^5 x + C $$

**Example 7: Even Powers**
Evaluate $\int \cos^4 x \, dx$.
*Solution:*
Both powers are even ($m=0, n=4$). We use half-angle identities.
$$ \cos^4 x = (\cos^2 x)^2 = \left( \frac{1 + \cos 2x}{2} \right)^2 = \frac{1}{4} (1 + 2\cos 2x + \cos^2 2x) $$
We must apply the half-angle identity again to $\cos^2 2x$:
$$ \cos^2 2x = \frac{1 + \cos 4x}{2} $$
So the integrand becomes:
$$ \frac{1}{4} \left( 1 + 2\cos 2x + \frac{1}{2} + \frac{1}{2}\cos 4x \right) = \frac{3}{8} + \frac{1}{2}\cos 2x + \frac{1}{8}\cos 4x $$
Integrating term by term:
$$ \int \left( \frac{3}{8} + \frac{1}{2}\cos 2x + \frac{1}{8}\cos 4x \right) \, dx = \frac{3}{8}x + \frac{1}{4}\sin 2x + \frac{1}{32}\sin 4x + C $$

### 7.2.2 Integrals of the form $\int \tan^m x \sec^n x \, dx$

**Case 1: The power of secant is even ($n = 2k$).**
Save a factor of $\sec^2 x$ (to serve as $du$) and convert the remaining secants to tangents using $\sec^2 x = 1 + \tan^2 x$.
Substitute $u = \tan x$, $du = \sec^2 x \, dx$.

**Case 2: The power of tangent is odd ($m = 2k + 1$).**
Save a factor of $\sec x \tan x$ (to serve as $du$) and convert the remaining tangents to secants using $\tan^2 x = \sec^2 x - 1$.
Substitute $u = \sec x$, $du = \sec x \tan x \, dx$.

**Case 3: $m$ is even and $n$ is odd.**
This is the most difficult case. There is no simple substitution. We must express the integrand in terms of secants (using $\tan^2 x = \sec^2 x - 1$) and then use integration by parts (specifically the secant reduction formula). The integral of $\sec^3 x$ is a classic example of this case.

**Example 8: Integral of $\sec^3 x$**
Evaluate $I = \int \sec^3 x \, dx$.
*Solution:*
Use integration by parts. Let $u = \sec x$ and $dv = \sec^2 x \, dx$.
$du = \sec x \tan x \, dx$ and $v = \tan x$.
$$ I = \sec x \tan x - \int \sec x \tan^2 x \, dx $$
Convert $\tan^2 x$ to $\sec^2 x - 1$:
$$ I = \sec x \tan x - \int \sec x (\sec^2 x - 1) \, dx $$
$$ I = \sec x \tan x - \int \sec^3 x \, dx + \int \sec x \, dx $$
$$ I = \sec x \tan x - I + \ln|\sec x + \tan x| $$
$$ 2I = \sec x \tan x + \ln|\sec x + \tan x| $$
$$ I = \frac{1}{2}(\sec x \tan x + \ln|\sec x + \tan x|) + C $$

---

## 7.3 Trigonometric Substitution

When an integrand contains a radical expression of the form $\sqrt{a^2 - x^2}$, $\sqrt{a^2 + x^2}$, or $\sqrt{x^2 - a^2}$, standard algebraic substitutions often fail. In these cases, we can use the Pythagorean trigonometric identities to eliminate the radical by substituting a trigonometric function for $x$.

### 7.3.1 The Three Cases

**1. Expression: $\sqrt{a^2 - x^2}$**
- Substitution: $x = a \sin \theta$, where $-\pi/2 \le \theta \le \pi/2$
- Differential: $dx = a \cos \theta \, d\theta$
- Simplification: $\sqrt{a^2 - a^2 \sin^2 \theta} = \sqrt{a^2(1 - \sin^2 \theta)} = \sqrt{a^2 \cos^2 \theta} = a \cos \theta$
- Note: The domain restriction on $\theta$ ensures that $\cos \theta \ge 0$, so $\sqrt{\cos^2 \theta} = |\cos \theta| = \cos \theta$.

**2. Expression: $\sqrt{a^2 + x^2}$**
- Substitution: $x = a \tan \theta$, where $-\pi/2 < \theta < \pi/2$
- Differential: $dx = a \sec^2 \theta \, d\theta$
- Simplification: $\sqrt{a^2 + a^2 \tan^2 \theta} = \sqrt{a^2(1 + \tan^2 \theta)} = \sqrt{a^2 \sec^2 \theta} = a \sec \theta$

**3. Expression: $\sqrt{x^2 - a^2}$**
- Substitution: $x = a \sec \theta$, where $0 \le \theta < \pi/2$ or $\pi \le \theta < 3\pi/2$
- Differential: $dx = a \sec \theta \tan \theta \, d\theta$
- Simplification: $\sqrt{a^2 \sec^2 \theta - a^2} = \sqrt{a^2(\sec^2 \theta - 1)} = \sqrt{a^2 \tan^2 \theta} = a \tan \theta$

### 7.3.2 Returning to the Original Variable
After evaluating the trigonometric integral with respect to $\theta$, you must express the final answer in terms of $x$. This is universally done by drawing a **reference right triangle**.

**Example 9: Sine Substitution**
Evaluate $\int \frac{\sqrt{9 - x^2}}{x^2} \, dx$.
*Solution:*
The radical is of the form $\sqrt{a^2 - x^2}$ with $a=3$.
Let $x = 3 \sin \theta$, so $dx = 3 \cos \theta \, d\theta$.
The radical becomes $\sqrt{9 - 9\sin^2 \theta} = 3 \cos \theta$.
Substitute into the integral:
$$ \int \frac{3 \cos \theta}{(3 \sin \theta)^2} (3 \cos \theta) \, d\theta = \int \frac{9 \cos^2 \theta}{9 \sin^2 \theta} \, d\theta = \int \cot^2 \theta \, d\theta $$
Use the identity $\cot^2 \theta = \csc^2 \theta - 1$:
$$ \int (\csc^2 \theta - 1) \, d\theta = -\cot \theta - \theta + C $$
To return to $x$, draw a right triangle. Since $\sin \theta = x/3$, the opposite side is $x$ and the hypotenuse is $3$. By the Pythagorean theorem, the adjacent side is $\sqrt{9 - x^2}$.
Thus, $\cot \theta = \frac{\text{adjacent}}{\text{opposite}} = \frac{\sqrt{9 - x^2}}{x}$.
And $\theta = \arcsin(x/3)$.
$$ \int \frac{\sqrt{9 - x^2}}{x^2} \, dx = -\frac{\sqrt{9 - x^2}}{x} - \arcsin\left(\frac{x}{3}\right) + C $$

### 7.3.3 Completing the Square
If a quadratic expression under a radical (or in a denominator) has a linear term (e.g., $ax^2 + bx + c$), we must complete the square to put it into one of the three standard forms before using trigonometric substitution.

**Example 10: Completing the Square**
Evaluate $\int \frac{dx}{\sqrt{x^2 + 4x + 13}}$.
*Solution:*
Complete the square: $x^2 + 4x + 13 = (x^2 + 4x + 4) + 9 = (x + 2)^2 + 9$.
Let $u = x+2$, so $du = dx$. The integral is $\int \frac{du}{\sqrt{u^2 + 9}}$.
This matches the form $\sqrt{u^2 + a^2}$ with $a=3$.
Let $u = 3 \tan \theta$, so $du = 3 \sec^2 \theta \, d\theta$. The radical becomes $3 \sec \theta$.
$$ \int \frac{3 \sec^2 \theta}{3 \sec \theta} \, d\theta = \int \sec \theta \, d\theta = \ln|\sec \theta + \tan \theta| + C $$
From $u = 3 \tan \theta$, $\tan \theta = u/3$. The hypotenuse of the triangle is $\sqrt{u^2 + 9}$.
So $\sec \theta = \frac{\sqrt{u^2+9}}{3}$.
$$ \ln\left| \frac{\sqrt{u^2+9}}{3} + \frac{u}{3} \right| + C = \ln\left| \frac{\sqrt{(x+2)^2+9} + (x+2)}{3} \right| + C $$

---

## 7.4 Integration of Rational Functions by Partial Fractions

A rational function is a ratio of polynomials: $f(x) = \frac{P(x)}{Q(x)}$.
We can integrate any rational function by expressing it as a sum of simpler fractions, a technique called **Partial Fraction Decomposition**.

### 7.4.1 Long Division (The First Step)
If the degree of the numerator $P(x)$ is greater than or equal to the degree of the denominator $Q(x)$, the fraction is called **improper**. You MUST perform polynomial long division first.
$$ \frac{P(x)}{Q(x)} = S(x) + \frac{R(x)}{Q(x)} $$
where the degree of the remainder $R(x)$ is strictly less than the degree of $Q(x)$. You then perform partial fraction decomposition on the proper fraction $\frac{R(x)}{Q(x)}$.

### 7.4.2 The Four Cases of Denominators

**Case 1: $Q(x)$ is a product of distinct linear factors.**
$Q(x) = (a_1 x + b_1)(a_2 x + b_2) \dots (a_k x + b_k)$.
The decomposition takes the form:
$$ \frac{P(x)}{Q(x)} = \frac{A_1}{a_1 x + b_1} + \frac{A_2}{a_2 x + b_2} + \dots + \frac{A_k}{a_k x + b_k} $$

**Case 2: $Q(x)$ is a product of linear factors, some of which are repeated.**
If the factor $(a x + b)$ appears $r$ times, we must include a fraction for *every* power from 1 to $r$:
$$ \frac{P(x)}{Q(x)} = \dots + \frac{A_1}{ax + b} + \frac{A_2}{(ax + b)^2} + \dots + \frac{A_r}{(ax + b)^r} + \dots $$

**Case 3: $Q(x)$ contains irreducible quadratic factors, none of which is repeated.**
An irreducible quadratic is one that cannot be factored into real numbers ($b^2 - 4ac < 0$).
For each irreducible quadratic $ax^2 + bx + c$, the numerator must be a general linear expression:
$$ \frac{P(x)}{Q(x)} = \dots + \frac{Ax + B}{ax^2 + bx + c} + \dots $$

**Case 4: $Q(x)$ contains a repeated irreducible quadratic factor.**
If $(ax^2 + bx + c)$ appears $r$ times, the decomposition is:
$$ \dots + \frac{A_1 x + B_1}{ax^2 + bx + c} + \frac{A_2 x + B_2}{(ax^2 + bx + c)^2} + \dots + \frac{A_r x + B_r}{(ax^2 + bx + c)^r} $$

### 7.4.3 Finding the Constants (Heaviside Cover-Up and Equating Coefficients)

**Example 11: Distinct Linear Factors**
Evaluate $\int \frac{x^2 + 2x - 1}{2x^3 + 3x^2 - 2x} \, dx$.
*Solution:*
The denominator factors as $x(2x^2 + 3x - 2) = x(2x - 1)(x + 2)$.
Set up the decomposition:
$$ \frac{x^2 + 2x - 1}{x(2x - 1)(x + 2)} = \frac{A}{x} + \frac{B}{2x - 1} + \frac{C}{x + 2} $$
Multiply by the common denominator:
$$ x^2 + 2x - 1 = A(2x - 1)(x + 2) + B(x)(x + 2) + C(x)(2x - 1) $$
We can find the constants by choosing strategic values for $x$ that zero out terms:
- Let $x = 0$: $-1 = A(-1)(2) \implies -1 = -2A \implies A = 1/2$.
- Let $x = 1/2$: $(1/2)^2 + 2(1/2) - 1 = B(1/2)(5/2) \implies 1/4 = 5B/4 \implies B = 1/5$.
- Let $x = -2$: $(-2)^2 + 2(-2) - 1 = C(-2)(-5) \implies -1 = 10C \implies C = -1/10$.
Now integrate:
$$ \int \left( \frac{1/2}{x} + \frac{1/5}{2x - 1} - \frac{1/10}{x + 2} \right) \, dx = \frac{1}{2}\ln|x| + \frac{1}{10}\ln|2x - 1| - \frac{1}{10}\ln|x + 2| + C $$

---

## 7.5 Strategy for Integration

When faced with an integral in the wild, you will not be told which section of the textbook it comes from. You must develop a systematic strategy.

1. **Simplify the Integrand if Possible:** Use algebraic manipulation or trigonometric identities to simplify.
2. **Look for an Obvious Substitution:** Find some function $u = g(x)$ in the integrand whose derivative $du = g'(x)dx$ is also present.
3. **Classify the Integrand According to its Form:**
   - *Trig Functions:* Use identities (7.2).
   - *Rational Functions:* Use Partial Fractions (7.4).
   - *Radicals:* Use Trig Substitution (7.3) or a Rationalizing Substitution.
   - *Product of a Polynomial and a Transcendental Function:* Use Integration by Parts (7.1).
4. **Try Again:** If the first three steps fail, try:
   - Clever substitutions (e.g., $u = \sqrt{x}$).
   - Integration by parts even if it doesn't look like a product.
   - Manipulate the integrand (multiply by a conjugate).

---

## 7.8 Improper Integrals

Until now, all definite integrals $\int_a^b f(x) \, dx$ required two conditions:
1. The interval $[a, b]$ is finite.
2. The function $f(x)$ is continuous on $[a, b]$, or has only a finite number of jump discontinuities.

Integrals that violate either of these conditions are called **Improper Integrals**. They are defined in terms of limits.

### 7.8.1 Type 1: Infinite Intervals
If the interval of integration is infinite, we replace the infinity with a variable $t$ and take the limit as $t$ approaches infinity.
$$ \int_a^\infty f(x) \, dx = \lim_{t \to \infty} \int_a^t f(x) \, dx $$
$$ \int_{-\infty}^b f(x) \, dx = \lim_{t \to -\infty} \int_t^b f(x) \, dx $$
If the limit exists and is a finite number, the improper integral **converges**. If the limit does not exist (or is $\pm \infty$), the integral **diverges**.

If both bounds are infinite, we split the integral at any real number $a$:
$$ \int_{-\infty}^\infty f(x) \, dx = \int_{-\infty}^a f(x) \, dx + \int_a^\infty f(x) \, dx $$
The integral converges only if *both* limits converge independently.

**The p-test for Integrals:**
The integral $\int_1^\infty \frac{1}{x^p} \, dx$ is a benchmark for convergence.
- If $p > 1$, the integral **converges** to $\frac{1}{p-1}$.
- If $p \le 1$, the integral **diverges**.

### 7.8.2 Type 2: Discontinuous Integrands
If $f(x)$ has a vertical asymptote at an endpoint $b$ (i.e., $f(x) \to \pm\infty$ as $x \to b^-$), we define the integral as a limit approaching the asymptote:
$$ \int_a^b f(x) \, dx = \lim_{t \to b^-} \int_a^t f(x) \, dx $$

If $f$ has a vertical asymptote at an interior point $c$ in $[a,b]$, we must split the integral:
$$ \int_a^b f(x) \, dx = \lim_{t \to c^-} \int_a^t f(x) \, dx + \lim_{t \to c^+} \int_t^b f(x) \, dx $$
Both limits must converge for the overall integral to converge.

**Example 12: A Hidden Asymptote**
Evaluate $\int_0^3 \frac{1}{x-1} \, dx$.
*Solution:*
WARNING: If you naively integrate and evaluate from 0 to 3, you get $\ln|2| - \ln|-1| = \ln 2$. This is WRONG!
The integrand has a vertical asymptote at $x=1$, which is inside the interval $[0, 3]$. We must split the integral.
$$ \int_0^3 \frac{1}{x-1} \, dx = \lim_{t \to 1^-} \int_0^t \frac{1}{x-1} \, dx + \lim_{s \to 1^+} \int_s^3 \frac{1}{x-1} \, dx $$
Let's evaluate the first limit:
$$ \lim_{t \to 1^-} [\ln|x-1|]_0^t = \lim_{t \to 1^-} (\ln|t-1| - \ln|-1|) = \lim_{t \to 1^-} \ln|t-1| = -\infty $$
Since one piece diverges, the entire integral **diverges**.

### 7.8.3 The Comparison Theorem for Integrals
Sometimes we cannot evaluate an improper integral exactly, but we only need to know if it converges or diverges. We can compare the integrand to a simpler, known integrand.

> **Comparison Theorem:**
> Suppose $f$ and $g$ are continuous functions with $f(x) \ge g(x) \ge 0$ for $x \ge a$.
> 1. If $\int_a^\infty f(x) \, dx$ converges, then $\int_a^\infty g(x) \, dx$ converges. (If the larger converges, the smaller must converge).
> 2. If $\int_a^\infty g(x) \, dx$ diverges, then $\int_a^\infty f(x) \, dx$ diverges. (If the smaller diverges, the larger must diverge).

**Example 13: Using Comparison**
Does $\int_1^\infty \frac{\sin^2 x}{x^2 + 1} \, dx$ converge or diverge?
*Solution:*
Since $0 \le \sin^2 x \le 1$, we know that:
$$ 0 \le \frac{\sin^2 x}{x^2 + 1} \le \frac{1}{x^2 + 1} \le \frac{1}{x^2} $$
We know that $\int_1^\infty \frac{1}{x^2} \, dx$ converges by the p-test ($p=2 > 1$). 
Therefore, by the Comparison Theorem, the smaller integral $\int_1^\infty \frac{\sin^2 x}{x^2 + 1} \, dx$ must also converge.

### 7.8.4 Advanced Topic: The Gamma Function
An incredibly important improper integral in advanced mathematics is the **Gamma Function**, defined as:
$$ \Gamma(z) = \int_0^\infty t^{z-1} e^{-t} \, dt $$
For any integer $n > 0$, using integration by parts reveals a remarkable property:
$$ \Gamma(n) = (n-1)! $$
The Gamma function effectively interpolates the factorial function for non-integer values!

---

## 7.9 Advanced Integration Techniques (100+1 Problems)

For students preparing for Olympiads or higher-level mathematical physics, standard calculus integration is often insufficient. The problems found in *100+1 Problems in Advanced Calculus* require deep insight, parameterized integrals, and non-standard substitutions.

### 7.9.1 Feynman's Trick (Differentiation Under the Integral Sign)
Also known as the **Leibniz Integral Rule**, this technique involves introducing a parameter $\alpha$ into the integrand, differentiating the integral with respect to $\alpha$, and then integrating the result back to solve the original problem.

Suppose we want to evaluate an integral $I = \int_a^b f(x) \, dx$ that is stubbornly difficult. We define a parameterized function:
$$ I(\alpha) = \int_a^b f(x, \alpha) \, dx $$
By Leibniz's Rule, if $f(x, \alpha)$ and its partial derivative with respect to $\alpha$ are continuous:
$$ \frac{d}{d\alpha} I(\alpha) = \int_a^b \frac{\partial}{\partial \alpha} f(x, \alpha) \, dx $$
This new integral is often much easier to evaluate.

**Example 14: Differentiation Under the Integral Sign**
Evaluate $I = \int_0^\infty \frac{\sin x}{x} \, dx$ (The Dirichlet Integral).

*Solution:*
Introduce a damping parameter $\alpha > 0$:
$$ I(\alpha) = \int_0^\infty \frac{\sin x}{x} e^{-\alpha x} \, dx $$
Differentiate with respect to $\alpha$:
$$ I'(\alpha) = \int_0^\infty \frac{\partial}{\partial \alpha} \left( \frac{\sin x}{x} e^{-\alpha x} \right) \, dx $$
$$ I'(\alpha) = \int_0^\infty \frac{\sin x}{x} (-x e^{-\alpha x}) \, dx = -\int_0^\infty \sin x \, e^{-\alpha x} \, dx $$
This is a standard "boomerang" integral (see Example 4). Using integration by parts twice yields:
$$ I'(\alpha) = -\frac{1}{\alpha^2 + 1} $$
Now, integrate $I'(\alpha)$ with respect to $\alpha$ to recover $I(\alpha)$:
$$ I(\alpha) = \int -\frac{1}{\alpha^2 + 1} \, d\alpha = -\arctan(\alpha) + C $$
To find $C$, notice that as $\alpha \to \infty$, the damping term $e^{-\alpha x} \to 0$, so $I(\infty) = 0$.
$$ 0 = -\arctan(\infty) + C \implies 0 = -\frac{\pi}{2} + C \implies C = \frac{\pi}{2} $$
Thus, $I(\alpha) = \frac{\pi}{2} - \arctan(\alpha)$.
Our original integral is $I(0)$:
$$ I(0) = \frac{\pi}{2} - \arctan(0) = \frac{\pi}{2} $$

### 7.9.2 The Weierstrass Substitution
When faced with a rational function of sines and cosines, $\int R(\sin x, \cos x) \, dx$, the **Weierstrass substitution** (or half-angle substitution) will *always* convert it into an integral of a rational function of a polynomial, which can then be solved via partial fractions.

Let $t = \tan(x/2)$. Using trigonometric identities, one can prove:
- $\sin x = \frac{2t}{1+t^2}$
- $\cos x = \frac{1-t^2}{1+t^2}$
- $dx = \frac{2}{1+t^2} dt$

**Example 15: The Weierstrass Substitution**
Evaluate $\int \frac{1}{3 + 5\cos x} \, dx$.

*Solution:*
Substitute $t = \tan(x/2)$:
$$ \int \frac{1}{3 + 5\left(\frac{1-t^2}{1+t^2}\right)} \left(\frac{2}{1+t^2}\right) dt $$
Multiply numerator and denominator by $(1+t^2)$:
$$ \int \frac{2}{3(1+t^2) + 5(1-t^2)} \, dt = \int \frac{2}{3 + 3t^2 + 5 - 5t^2} \, dt $$
$$ = \int \frac{2}{8 - 2t^2} \, dt = \int \frac{1}{4 - t^2} \, dt $$
Use partial fractions:
$$ \frac{1}{(2-t)(2+t)} = \frac{1/4}{2-t} + \frac{1/4}{2+t} $$
$$ \int \left( \frac{1/4}{2-t} + \frac{1/4}{2+t} \right) \, dt = -\frac{1}{4}\ln|2-t| + \frac{1}{4}\ln|2+t| + C = \frac{1}{4}\ln\left|\frac{2+t}{2-t}\right| + C $$
Substitute back $t = \tan(x/2)$:
$$ = \frac{1}{4}\ln\left|\frac{2+\tan(x/2)}{2-\tan(x/2)}\right| + C $$

### 7.9.3 Exploiting Symmetry
Advanced calculus problems often leverage symmetry to avoid integration entirely.
If $f(x)$ is continuous on $[-a, a]$:
1. If $f$ is even ($f(-x) = f(x)$), then $\int_{-a}^a f(x) \, dx = 2 \int_0^a f(x) \, dx$.
2. If $f$ is odd ($f(-x) = -f(x)$), then $\int_{-a}^a f(x) \, dx = 0$.

Another powerful symmetry property for bounds $[0, \pi/2]$ is:
$$ \int_0^{\pi/2} f(\sin x) \, dx = \int_0^{\pi/2} f(\cos x) \, dx $$
This is proven using the substitution $u = \pi/2 - x$.

**Example 16: King's Property**
Evaluate $I = \int_0^{\pi/2} \frac{\sqrt{\sin x}}{\sqrt{\sin x} + \sqrt{\cos x}} \, dx$.

*Solution:*
Use the substitution $u = \pi/2 - x$, so $dx = -du$. The bounds flip from $\pi/2$ to $0$.
Since $\sin(\pi/2 - u) = \cos u$ and $\cos(\pi/2 - u) = \sin u$:
$$ I = \int_0^{\pi/2} \frac{\sqrt{\cos u}}{\sqrt{\cos u} + \sqrt{\sin u}} \, du $$
Notice the denominator is identical to the original integral! Add the two integrals together:
$$ I + I = \int_0^{\pi/2} \frac{\sqrt{\sin x}}{\sqrt{\sin x} + \sqrt{\cos x}} \, dx + \int_0^{\pi/2} \frac{\sqrt{\cos x}}{\sqrt{\cos x} + \sqrt{\sin x}} \, dx $$
$$ 2I = \int_0^{\pi/2} \frac{\sqrt{\sin x} + \sqrt{\cos x}}{\sqrt{\sin x} + \sqrt{\cos x}} \, dx = \int_0^{\pi/2} 1 \, dx = \frac{\pi}{2} $$
$$ I = \frac{\pi}{4} $$

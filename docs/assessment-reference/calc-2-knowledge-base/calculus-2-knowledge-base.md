# Calculus 2 Knowledge Base

This knowledge base serves as the central reference for authoring Calculus 2 concept lessons, worked examples, and glossaries. It covers the core topics typically found in a rigorous Calculus 2 curriculum (e.g., Stewart's Calculus Early Transcendentals Chapters 6-11).

## 1. Techniques of Integration

### Integration by Parts
Based on the product rule for differentiation: $\int u \, dv = uv - \int v \, du$.
- **LIATE Rule:** Choose $u$ based on the first type of function that appears in this list: **L**ogarithmic, **I**nverse trigonometric, **A**lgebraic, **T**rigonometric, **E**xponential.

### Trigonometric Integrals
- **Powers of Sine and Cosine ($\int \sin^m x \cos^n x \, dx$):**
  - If $m$ is odd: Save one sine factor and use $\sin^2 x = 1 - \cos^2 x$.
  - If $n$ is odd: Save one cosine factor and use $\cos^2 x = 1 - \sin^2 x$.
  - If both are even: Use half-angle identities: $\sin^2 x = \frac{1 - \cos(2x)}{2}$, $\cos^2 x = \frac{1 + \cos(2x)}{2}$.

### Trigonometric Substitution
Used for integrals involving radicals:
- $\sqrt{a^2 - x^2}$: Let $x = a \sin \theta$. Identity: $1 - \sin^2 \theta = \cos^2 \theta$.
- $\sqrt{a^2 + x^2}$: Let $x = a \tan \theta$. Identity: $1 + \tan^2 \theta = \sec^2 \theta$.
- $\sqrt{x^2 - a^2}$: Let $x = a \sec \theta$. Identity: $\sec^2 \theta - 1 = \tan^2 \theta$.

### Partial Fractions
Used for integrating rational functions $P(x)/Q(x)$.
- **Distinct Linear Factors:** $\frac{1}{(x-a)(x-b)} = \frac{A}{x-a} + \frac{B}{x-b}$
- **Repeated Linear Factors:** $\frac{1}{(x-a)^2} = \frac{A}{x-a} + \frac{B}{(x-a)^2}$
- **Irreducible Quadratic Factors:** $\frac{1}{(x^2+px+q)} = \frac{Ax+B}{x^2+px+q}$

### Improper Integrals
- **Type 1 (Infinite Intervals):** $\int_a^\infty f(x) \, dx = \lim_{t \to \infty} \int_a^t f(x) \, dx$.
- **Type 2 (Discontinuous Integrands):** If $f(x)$ has an infinite discontinuity at $b$, $\int_a^b f(x) \, dx = \lim_{t \to b^-} \int_a^t f(x) \, dx$.

## 2. Applications of Integration

### Area Between Curves
$A = \int_a^b [f(x) - g(x)] \, dx$, where $f(x) \ge g(x)$ for all $x$ in $[a, b]$.

### Volumes of Solids of Revolution
- **Disk/Washer Method:** $V = \pi \int_a^b ([R(x)]^2 - [r(x)]^2) \, dx$. Best when slicing perpendicular to the axis of revolution.
- **Cylindrical Shells:** $V = 2\pi \int_a^b (\text{radius})(\text{height}) \, dx = 2\pi \int_a^b x f(x) \, dx$. Best when slicing parallel to the axis of revolution.

### Arc Length & Surface Area
- **Arc Length:** $L = \int_a^b \sqrt{1 + [f'(x)]^2} \, dx$.
- **Surface Area of Revolution:** $S = 2\pi \int_a^b f(x) \sqrt{1 + [f'(x)]^2} \, dx$ (rotated about x-axis).

### Physics Applications
- **Work:** $W = \int_a^b F(x) \, dx$. For springs: Hooke's Law $F(x) = kx$.
- **Hydrostatic Force:** $F = \int_a^b \rho g \cdot (\text{depth}) \cdot (\text{width}) \, dy$.
- **Center of Mass (Centroid):** $\bar{x} = \frac{1}{A} \int_a^b x [f(x) - g(x)] \, dx$, $\bar{y} = \frac{1}{A} \int_a^b \frac{1}{2} ([f(x)]^2 - [g(x)]^2) \, dx$.

## 3. Sequences and Series

### Sequences
- A sequence $\{a_n\}$ converges if $\lim_{n \to \infty} a_n = L$.
- **Monotonic Sequence Theorem:** Every bounded, monotonic sequence converges.

### Series Convergence Tests
- **Divergence Test:** If $\lim_{n \to \infty} a_n \neq 0$, the series $\sum a_n$ diverges.
- **Geometric Series:** $\sum_{n=0}^\infty a r^n$ converges to $\frac{a}{1-r}$ if $|r| < 1$.
- **p-Series:** $\sum_{n=1}^\infty \frac{1}{n^p}$ converges if $p > 1$, diverges if $p \le 1$.
- **Integral Test:** If $f(x)$ is continuous, positive, and decreasing, $\sum f(n)$ and $\int_1^\infty f(x) \, dx$ either both converge or both diverge.
- **Comparison Test:** If $0 \le a_n \le b_n$ and $\sum b_n$ converges, then $\sum a_n$ converges.
- **Limit Comparison Test:** If $\lim_{n \to \infty} \frac{a_n}{b_n} = c > 0$, both series converge or both diverge.
- **Alternating Series Test:** $\sum (-1)^n b_n$ converges if $b_{n+1} \le b_n$ and $\lim b_n = 0$.
- **Ratio Test:** Let $L = \lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right|$. Converges absolutely if $L < 1$.
- **Root Test:** Let $L = \lim_{n \to \infty} \sqrt[n]{|a_n|}$. Converges absolutely if $L < 1$.

### Power Series & Taylor Series
- **Power Series:** $\sum_{n=0}^\infty c_n (x-a)^n$. The radius of convergence $R$ is found via the Ratio Test.
- **Taylor Series:** $f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(a)}{n!} (x-a)^n$. (Maclaurin if $a=0$).

## 4. Parametric Equations and Polar Coordinates

### Parametric Curves
- Defined by $x = f(t)$, $y = g(t)$.
- **Derivative:** $\frac{dy}{dx} = \frac{dy/dt}{dx/dt}$.
- **Second Derivative:** $\frac{d^2y}{dx^2} = \frac{\frac{d}{dt}(dy/dx)}{dx/dt}$.
- **Arc Length:** $L = \int_\alpha^\beta \sqrt{(dx/dt)^2 + (dy/dt)^2} \, dt$.

### Polar Coordinates
- Conversion: $x = r \cos \theta$, $y = r \sin \theta$, $r^2 = x^2 + y^2$, $\tan \theta = y/x$.
- **Area:** $A = \int_a^b \frac{1}{2} r^2 \, d\theta$.
- **Arc Length:** $L = \int_a^b \sqrt{r^2 + (dr/d\theta)^2} \, d\theta$.

## 5. Introduction to Differential Equations

### Basics
- An equation containing an unknown function and its derivatives.
- **Order:** The highest derivative present.
- **Linear:** The dependent variable and its derivatives appear to the first power.

### Separable Equations
- Can be written as $\frac{dy}{dx} = g(x) f(y)$.
- Solved by separating variables: $\int \frac{1}{f(y)} \, dy = \int g(x) \, dx$.

### First-Order Linear Equations
- Standard form: $\frac{dy}{dx} + P(x)y = Q(x)$.
- **Integrating Factor:** $I(x) = e^{\int P(x) \, dx}$.
- Multiply both sides by $I(x)$ to get $\frac{d}{dx}[I(x)y] = I(x)Q(x)$, then integrate.

### Models
- **Population Growth:** $\frac{dP}{dt} = kP \implies P(t) = P_0 e^{kt}$.
- **Logistic Growth:** $\frac{dP}{dt} = kP(1 - \frac{P}{M})$.
- **Newton's Law of Cooling:** $\frac{dT}{dt} = k(T - T_s)$.
- **Predator-Prey (Lotka-Volterra):** 
  - $\frac{dR}{dt} = kR - aRW$ (Rabbits/Prey)
  - $\frac{dW}{dt} = -rW + bRW$ (Wolves/Predators)

# Calculus Question Bank

**Legend:**
- `[C]` Conceptual — understanding definitions, behaviors, relationships
- `[P]` Procedural — step-by-step calculation
- `[CT]` Critical Thinking — multi-step, proof-adjacent, application
- `[N]` Novel — unusual framing, graphical, "what if," reverse engineering

---

## Calculus 2

### Topic 1: Integration Techniques

#### Integration by Parts

**Q1.** `[C]` State the formula for integration by parts and explain what the LIATE rule is used for.

**Q2.** `[P]` Evaluate $\int x e^{3x} dx$.
> **Answer:** Let $u=x$, $dv = e^{3x}dx$. Then $du=dx$, $v=\frac{1}{3}e^{3x}$. Result: $\frac{x}{3}e^{3x} - \frac{1}{9}e^{3x} + C$.

**Q3.** `[P]` Evaluate $\int \ln(x) dx$.
> **Answer:** Let $u=\ln x$, $dv=dx$. Then $du=\frac{1}{x}dx$, $v=x$. Result: $x\ln x - x + C$.

**Q4.** `[P]` Evaluate $\int x^2 \sin(x) dx$.
> **Answer:** Apply IBP twice. Final: $-x^2\cos x + 2x\sin x + 2\cos x + C$.

**Q5.** `[P]` Evaluate $\int e^x \cos(x) dx$.
> **Answer:** Apply IBP twice and solve for the integral. $I = e^x\cos x + e^x\sin x - I \implies I = \frac{1}{2}e^x(\sin x + \cos x) + C$.

**Q6.** `[P]` Evaluate $\int x^3 \ln(x) dx$.
> **Answer:** $u=\ln x$, $dv=x^3dx$. $v=\frac{x^4}{4}$. Result: $\frac{x^4 \ln x}{4} - \frac{x^4}{16} + C$.

**Q7.** `[CT]` Evaluate $\int (\ln x)^2 dx$.
> **Answer:** Apply IBP twice. First: $u=(\ln x)^2$, $dv=dx$. After two applications: $x(\ln x)^2 - 2x\ln x + 2x + C$.

**Q8.** `[CT]` Show that $\int_0^\infty x^n e^{-x} dx = n!$ for positive integers $n$, using integration by parts recursively.
> **Answer:** Establish the reduction formula $I_n = n I_{n-1}$ via IBP. Base case $I_0 = 1$. Then $I_n = n!$.

**Q9.** `[N]` Given that $\int f(x) dx = F(x)$, evaluate $\int x f'(x) dx$ in terms of $F$.
> **Answer:** IBP: $u=x$, $dv=f'(x)dx$. Then $\int x f'(x)dx = xf(x) - \int f(x)dx = xf(x) - F(x) + C$.

**Q10.** `[N]` Evaluate $\int \sin^{-1}(x) dx$.
> **Answer:** IBP with $u=\sin^{-1}x$, $dv=dx$. $v=x$, $du=\frac{1}{\sqrt{1-x^2}}dx$. Result: $x\sin^{-1}x + \sqrt{1-x^2} + C$.

---

#### Trigonometric Integrals

**Q11.** `[C]` When evaluating $\int \sin^m x \cos^n x \, dx$, when do you use the half-angle identity vs. saving a factor and substituting?
> **Answer:** If either $m$ or $n$ is odd, save one factor of sin or cos and use $\sin^2+\cos^2=1$ to substitute. If both are even, use half-angle identities: $\sin^2x=\frac{1-\cos 2x}{2}$, $\cos^2x=\frac{1+\cos 2x}{2}$.

**Q12.** `[P]` Evaluate $\int \sin^3(x) \cos^2(x) dx$.
> **Answer:** Save $\sin x$: $\int (1-\cos^2 x)\cos^2 x \sin x \, dx$. Let $u=\cos x$: $-\int(1-u^2)u^2 du = -\frac{u^3}{3}+\frac{u^5}{5}+C = -\frac{\cos^3x}{3}+\frac{\cos^5x}{5}+C$.

**Q13.** `[P]` Evaluate $\int \sin^2(x)\cos^2(x) dx$.
> **Answer:** Use $\sin^2\cos^2 = \frac{1}{4}\sin^2(2x) = \frac{1}{8}(1-\cos(4x))$. Result: $\frac{x}{8} - \frac{\sin(4x)}{32} + C$.

**Q14.** `[P]` Evaluate $\int \tan^3(x) \sec^3(x) dx$.
> **Answer:** Rewrite as $\int \tan^2x \sec^2 x \sec x \tan x \, dx$. Let $u=\sec x$: $\int (u^2-1)u^2 du = \frac{u^5}{5} - \frac{u^3}{3} + C = \frac{\sec^5 x}{5} - \frac{\sec^3 x}{3} + C$.

**Q15.** `[P]` Evaluate $\int_0^{\pi/2} \sin^4(x) dx$.
> **Answer:** Use half-angle identity twice. $\sin^4 x = \frac{3}{8} - \frac{1}{2}\cos(2x) + \frac{1}{8}\cos(4x)$. Integral from $0$ to $\pi/2$ is $\frac{3\pi}{16}$.

**Q16.** `[CT]` Evaluate $\int \sec^3(x) dx$.
> **Answer:** IBP: $u=\sec x$, $dv=\sec^2 x \, dx$. After solving: $I = \frac{1}{2}\sec x \tan x + \frac{1}{2}\ln|\sec x + \tan x| + C$.

**Q17.** `[N]` Without computing, explain whether $\int_0^\pi \sin^n(x) dx$ is the same for all odd positive integers $n$ and justify.
> **Answer:** No. For odd $n$, the integral is positive but its value decreases as $n$ increases, since $\sin^n x \le \sin^{n-1} x$ on $(0,\pi)$. The integrals have the Wallis formula values: $I_n = \frac{(n-1)!!}{n!!} \cdot 2$ for even arguments of the double factorial.

---

#### Trigonometric Substitution

**Q18.** `[C]` What three substitutions are used in trigonometric substitution, and for which radical expression is each appropriate?
> **Answer:** $\sqrt{a^2-x^2} \to x=a\sin\theta$; $\sqrt{a^2+x^2} \to x=a\tan\theta$; $\sqrt{x^2-a^2} \to x=a\sec\theta$.

**Q19.** `[P]` Evaluate $\int \frac{dx}{\sqrt{9-x^2}}$.
> **Answer:** $x=3\sin\theta$. Integral becomes $\int d\theta = \theta + C = \sin^{-1}(x/3) + C$.

**Q20.** `[P]` Evaluate $\int \frac{x^2 dx}{\sqrt{4-x^2}}$.
> **Answer:** $x=2\sin\theta$. Integral becomes $4\int \sin^2\theta \, d\theta = 2\theta - 2\sin\theta\cos\theta + C = 2\sin^{-1}(x/2) - \frac{x\sqrt{4-x^2}}{2} + C$.

**Q21.** `[P]` Evaluate $\int \frac{dx}{(x^2+4)^{3/2}}$.
> **Answer:** $x=2\tan\theta$. Integral becomes $\frac{1}{4}\int\cos\theta \, d\theta = \frac{\sin\theta}{4} + C = \frac{x}{4\sqrt{x^2+4}} + C$.

**Q22.** `[P]` Evaluate $\int \frac{\sqrt{x^2-25}}{x} dx$.
> **Answer:** $x=5\sec\theta$. $\int \frac{5\tan\theta}{5\sec\theta} \cdot 5\sec\theta\tan\theta \, d\theta = 5\int\tan^2\theta \, d\theta = 5(\tan\theta - \theta) + C = \sqrt{x^2-25} - 5\sec^{-1}(x/5) + C$.

**Q23.** `[CT]` Evaluate $\int_0^1 \frac{x^2}{\sqrt{1-x^4}} dx$ using the substitution $x^2 = \sin\theta$.
> **Answer:** Let $x^2 = \sin\theta$, so $2x\,dx = \cos\theta \,d\theta$. Rewrite integrand; after simplification the integral becomes $\frac{1}{2}\int_0^{\pi/2} \sqrt{\sin\theta}\,d\theta$, which can be expressed with the Beta function as $\frac{\Gamma(3/4)\Gamma(1/2)}{4\Gamma(5/4)}$.

**Q24.** `[N]` Complete the square, then use trig substitution: $\int \frac{dx}{\sqrt{-x^2+6x-5}}$.
> **Answer:** $-x^2+6x-5 = -(x^2-6x+9)+4 = 4-(x-3)^2$. Let $u=x-3$, then $\sin^{-1}\left(\frac{x-3}{2}\right) + C$.

---

#### Partial Fractions

**Q25.** `[C]` Describe when partial fraction decomposition is applicable and what form the decomposition takes when the denominator has (a) distinct linear factors, (b) repeated linear factors, (c) irreducible quadratic factors.

**Q26.** `[P]` Evaluate $\int \frac{4x+1}{x^2-x-6} dx$.
> **Answer:** Factor: $(x-3)(x+2)$. Decompose: $\frac{A}{x-3} + \frac{B}{x+2}$. $A=\frac{13}{5}$, $B=\frac{7}{5}$. Integral: $\frac{13}{5}\ln|x-3| + \frac{7}{5}\ln|x+2| + C$.

**Q27.** `[P]` Evaluate $\int \frac{x^2+2x-1}{x^3-x} dx$.
> **Answer:** Factor denominator: $x(x-1)(x+1)$. Decompose with constants $A=1/1$, $B=1$, $C=-1$. $\ln|x| + \ln|x-1| - \ln|x+1| + C$.

**Q28.** `[P]` Evaluate $\int \frac{2x^2+3}{x(x^2+3)} dx$.
> **Answer:** Decompose as $\frac{A}{x} + \frac{Bx+C}{x^2+3}$. $A=1, B=1, C=0$. $\ln|x| + \frac{1}{2}\ln(x^2+3) + C$.

**Q29.** `[P]` Evaluate $\int \frac{dx}{x^2(x-1)}$.
> **Answer:** Decompose: $\frac{A}{x} + \frac{B}{x^2} + \frac{C}{x-1}$. $A=-1, B=-1, C=1$. $-\ln|x|+\frac{1}{x}+\ln|x-1|+C$.

**Q30.** `[CT]` Evaluate $\int \frac{x^3}{x^2-1} dx$ (note the degree of numerator exceeds denominator).
> **Answer:** Long divide first: $x^3 \div (x^2-1) = x + \frac{x}{x^2-1}$. Decompose $\frac{x}{x^2-1} = \frac{1/2}{x-1}+\frac{1/2}{x+1}$. Result: $\frac{x^2}{2}+\frac{1}{2}\ln|x-1|+\frac{1}{2}\ln|x+1|+C$.

**Q31.** `[N]` Express $\int_0^1 \frac{x^4(1-x)^4}{1+x^2} dx$ as a combination of known constants. (Hint: This integral famously equals $\frac{22}{7}-\pi$.)
> **Answer:** The result is $\frac{22}{7}-\pi \approx 0.00126$. This is a well-known identity showing $22/7 > \pi$ since the integrand is always positive on $[0,1]$.

---

#### Improper Integrals

**Q32.** `[C]` Explain the difference between a Type 1 and Type 2 improper integral. Give one example of each.

**Q33.** `[P]` Determine whether $\int_1^\infty \frac{1}{x^2} dx$ converges and find its value if it does.
> **Answer:** $\lim_{b\to\infty} [-1/x]_1^b = \lim_{b\to\infty}(-1/b+1)=1$. Converges to $1$.

**Q34.** `[P]` Determine whether $\int_1^\infty \frac{1}{x} dx$ converges.
> **Answer:** $\lim_{b\to\infty}[\ln x]_1^b = \infty$. Diverges.

**Q35.** `[P]` Evaluate $\int_0^1 \frac{1}{\sqrt{x}} dx$.
> **Answer:** $\lim_{a\to 0^+}[2\sqrt{x}]_a^1 = 2-0 = 2$. Converges to $2$.

**Q36.** `[P]` Determine whether $\int_{-\infty}^\infty \frac{1}{1+x^2} dx$ converges and find its value.
> **Answer:** $[\arctan x]_{-\infty}^\infty = \pi/2 - (-\pi/2) = \pi$. Converges to $\pi$.

**Q37.** `[CT]` Use the comparison test to show $\int_1^\infty \frac{\sin^2 x}{x^2} dx$ converges.
> **Answer:** Since $\sin^2 x \le 1$, we have $\frac{\sin^2 x}{x^2} \le \frac{1}{x^2}$. Since $\int_1^\infty \frac{1}{x^2} dx$ converges, by comparison, the given integral also converges.

**Q38.** `[N]` Evaluate the Gaussian integral $\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}$ by squaring the integral and converting to polar coordinates.
> **Answer:** Let $I = \int_{-\infty}^\infty e^{-x^2}dx$. Then $I^2 = \int\!\!\int e^{-(x^2+y^2)}dA = \int_0^{2\pi}\int_0^\infty e^{-r^2} r\,dr\,d\theta = 2\pi\cdot\frac{1}{2} = \pi$. So $I=\sqrt{\pi}$.

---

### Topic 2: Sequences and Series

**Q39.** `[C]` State the definition of convergence for a sequence $\{a_n\}$.

**Q40.** `[C]` Explain why the Nth-Term Divergence Test can only be used to prove divergence, never convergence.
> **Answer:** If $\lim a_n \neq 0$, the series diverges. But if $\lim a_n = 0$, the series may still diverge (e.g., the harmonic series).

**Q41.** `[P]` Determine whether $\sum_{n=1}^\infty \frac{n}{n+1}$ converges.
> **Answer:** $\lim_{n\to\infty} \frac{n}{n+1} = 1 \neq 0$. Diverges by Nth-Term Test.

**Q42.** `[P]` Find the sum: $\sum_{n=0}^\infty \frac{(-1)^n}{3^n}$.
> **Answer:** Geometric series with $a=1$, $r=-1/3$. Sum $= \frac{1}{1-(-1/3)} = \frac{1}{4/3} = \frac{3}{4}$.

**Q43.** `[P]` Use the Integral Test to determine convergence of $\sum_{n=1}^\infty \frac{1}{n^2+1}$.
> **Answer:** $\int_1^\infty \frac{1}{x^2+1}dx = [\arctan x]_1^\infty = \pi/2 - \pi/4 = \pi/4$. Since the integral converges, the series converges.

**Q44.** `[P]` Use the Comparison Test to determine convergence of $\sum_{n=1}^\infty \frac{1}{n^2+\sqrt{n}}$.
> **Answer:** $\frac{1}{n^2+\sqrt{n}} < \frac{1}{n^2}$. Since $\sum 1/n^2$ converges (p-series, $p=2>1$), the given series converges.

**Q45.** `[P]` Apply the Ratio Test to $\sum_{n=1}^\infty \frac{n!}{n^n}$.
> **Answer:** $L = \lim \frac{(n+1)!/(n+1)^{n+1}}{n!/n^n} = \lim \frac{n^n}{(n+1)^n} = \lim \left(\frac{n}{n+1}\right)^n = \frac{1}{e} < 1$. Converges.

**Q46.** `[P]` Determine convergence of $\sum_{n=1}^\infty \frac{(-1)^n}{\sqrt{n}}$.
> **Answer:** Alternating series. $b_n = 1/\sqrt{n}$ is decreasing and $\lim b_n = 0$. Converges by AST.

**Q47.** `[P]` Determine whether $\sum_{n=1}^\infty \frac{(-1)^n}{\sqrt{n}}$ converges absolutely.
> **Answer:** $\sum 1/\sqrt{n}$ is a p-series with $p=1/2 \le 1$. Diverges. So the alternating series converges conditionally but NOT absolutely.

**Q48.** `[CT]` Find the sum of the telescoping series $\sum_{n=1}^\infty \frac{1}{n(n+1)}$.
> **Answer:** Partial fractions: $\frac{1}{n} - \frac{1}{n+1}$. Partial sums: $S_k = 1 - \frac{1}{k+1} \to 1$.

**Q49.** `[CT]` For the series $\sum_{n=2}^\infty \frac{1}{n(\ln n)^2}$, determine convergence using the Integral Test.
> **Answer:** $\int_2^\infty \frac{dx}{x(\ln x)^2}$. Let $u=\ln x$: $\int_{\ln 2}^\infty \frac{du}{u^2} = \left[-1/u\right]_{\ln 2}^\infty = \frac{1}{\ln 2}$. Converges.

**Q50.** `[N]` Can a series with all positive terms converge if its terms are unbounded? Explain.
> **Answer:** No. If the terms are unbounded, then $a_n \not\to 0$, so by the Nth-Term Divergence Test, the series diverges.

**Q51.** `[N]` Construct a series that diverges but whose partial sums are bounded. Is this possible?
> **Answer:** No. If partial sums are bounded and monotone increasing (positive terms), by the Monotone Convergence Theorem the series converges. The condition "bounded partial sums" with positive terms implies convergence.

---

### Topic 3: Power, Taylor, and Maclaurin Series

**Q52.** `[C]` What is the difference between a Taylor series and a Maclaurin series?

**Q53.** `[C]` Explain what the radius of convergence $R$ means geometrically on the number line.

**Q54.** `[P]` Find the Maclaurin series for $f(x) = e^{-2x}$.
> **Answer:** Substitute $-2x$ into $e^u = \sum \frac{u^n}{n!}$. Result: $\sum_{n=0}^\infty \frac{(-2)^n x^n}{n!}$.

**Q55.** `[P]` Find the radius of convergence of $\sum_{n=1}^\infty \frac{(x+3)^n}{n \cdot 4^n}$.
> **Answer:** Ratio test: $L=|x+3|/4 < 1 \implies |x+3| < 4$. $R = 4$.

**Q56.** `[P]` Find the interval of convergence of $\sum_{n=1}^\infty \frac{(x-2)^n}{n}$.
> **Answer:** $R=1$, centered at $x=2$. Interval $(1,3)$. At $x=3$: $\sum 1/n$ diverges. At $x=1$: $\sum (-1)^n/n$ converges. IOC: $[1,3)$.

**Q57.** `[P]` Use the Maclaurin series for $\sin x$ to write the series for $\sin(x^2)$.
> **Answer:** $\sin(x^2) = \sum_{n=0}^\infty \frac{(-1)^n x^{4n+2}}{(2n+1)!}$.

**Q58.** `[P]` Find the Taylor series for $f(x) = \frac{1}{x}$ centered at $a=2$.
> **Answer:** $\frac{1}{x} = \frac{1}{2+(x-2)} = \frac{1}{2} \cdot \frac{1}{1+(x-2)/2} = \frac{1}{2}\sum_{n=0}^\infty \frac{(-1)^n (x-2)^n}{2^n}$.

**Q59.** `[P]` Use the identity $\arctan x = \int_0^x \frac{1}{1+t^2} dt$ to derive the Maclaurin series for $\arctan x$.
> **Answer:** $\frac{1}{1+t^2} = \sum(-1)^n t^{2n}$. Integrate term by term: $\arctan x = \sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{2n+1}$.

**Q60.** `[CT]` Use Taylor series to evaluate $\lim_{x\to 0} \frac{\sin x - x}{x^3}$.
> **Answer:** $\sin x = x - x^3/6 + \ldots$ So $\sin x - x = -x^3/6 + \ldots$ Thus $\frac{\sin x - x}{x^3} \to -\frac{1}{6}$.

**Q61.** `[CT]` Evaluate $\int_0^{0.5} e^{-x^2} dx$ accurate to within $10^{-4}$.
> **Answer:** $e^{-x^2} = 1 - x^2 + x^4/2 - x^6/6 + \ldots$ Integrate: $x - x^3/3 + x^5/10 - x^7/42 + \ldots$ at $x=0.5$. Evaluate and stop when term $< 10^{-4}$. Result $\approx 0.4612$.

**Q62.** `[N]` Without computing derivatives, find the coefficient of $x^5$ in the Maclaurin series for $x\sin(x^2)$.
> **Answer:** $\sin(u) = u - u^3/6 + \ldots$ So $\sin(x^2) = x^2 - x^6/6 + \ldots$. Multiply by $x$: $x^3 - x^7/6 + \ldots$. Coefficient of $x^5$ is $0$.

**Q63.** `[N]` Find a power series representation for $f(x) = \ln\left(\frac{1+x}{1-x}\right)$.
> **Answer:** $\ln(1+x) = \sum \frac{(-1)^{n+1}x^n}{n}$ and $\ln(1-x)=-\sum \frac{x^n}{n}$. Subtracting: $2\sum_{n=0}^\infty \frac{x^{2n+1}}{2n+1} = 2(x + x^3/3 + x^5/5 + \ldots)$.

---

### Topic 4: Parametric and Polar

**Q64.** `[C]` Given $x=f(t)$, $y=g(t)$, state the formula for $\frac{dy}{dx}$ in terms of $t$.
> **Answer:** $\frac{dy}{dx} = \frac{dy/dt}{dx/dt} = \frac{g'(t)}{f'(t)}$.

**Q65.** `[P]` Find the slope of the tangent line to the curve $x = t^2 - 1$, $y = t^3 - 3t$ at $t=1$.
> **Answer:** $dx/dt=2t$, $dy/dt=3t^2-3$. At $t=1$: $dx/dt=2$, $dy/dt=0$. Slope $= 0/2 = 0$.

**Q66.** `[P]` Find the arc length of the curve $x=\cos t$, $y=\sin t$ for $0 \le t \le 2\pi$.
> **Answer:** $L = \int_0^{2\pi}\sqrt{(-\sin t)^2+(\cos t)^2}dt = \int_0^{2\pi} dt = 2\pi$.

**Q67.** `[P]` Find the arc length of $x=\frac{1}{3}t^3$, $y=\frac{1}{2}t^2$ for $0\le t\le 1$.
> **Answer:** $\sqrt{t^4+t^2}dt = t\sqrt{t^2+1}dt$. $L = \int_0^1 t\sqrt{t^2+1}dt = \frac{1}{3}(2)^{3/2}-\frac{1}{3} = \frac{2\sqrt{2}-1}{3}$.

**Q68.** `[P]` Convert the point $(r,\theta)=(4, 2\pi/3)$ to rectangular coordinates.
> **Answer:** $x=4\cos(2\pi/3)=4(-1/2)=-2$, $y=4\sin(2\pi/3)=4(\sqrt{3}/2)=2\sqrt{3}$. Point: $(-2, 2\sqrt{3})$.

**Q69.** `[P]` Find the area enclosed by $r = 3\cos\theta$.
> **Answer:** $A = \frac{1}{2}\int_0^{\pi}(3\cos\theta)^2 d\theta = \frac{9}{2}\int_0^\pi \cos^2\theta d\theta = \frac{9\pi}{4}$.

**Q70.** `[P]` Find the area inside $r=2$ and outside $r=2\cos\theta$.
> **Answer:** Find intersections: $\cos\theta=1 \implies \theta=0, \pi$. Area = $\frac{1}{2}\int_{-\pi/2}^{\pi/2}[4 - 4\cos^2\theta]d\theta = 2\int_{-\pi/2}^{\pi/2}(1-\cos^2\theta)d\theta = 2(\pi/2) - \pi/2 = \pi - \pi/2 \cdot 2 = \pi - \pi = 0$... Re-examine: Area inside $r=2$, outside $r=2\cos\theta$: $\frac{1}{2}\int_{\pi/2}^{3\pi/2}4d\theta + \frac{1}{2}\int_{-\pi/2}^{\pi/2}(4-4\cos^2\theta)d\theta = 2\pi$.

**Q71.** `[CT]` Find the length of the polar curve $r = e^\theta$ from $\theta=0$ to $\theta=2\pi$.
> **Answer:** $L = \int_0^{2\pi}\sqrt{r^2+(dr/d\theta)^2}d\theta = \int_0^{2\pi}\sqrt{e^{2\theta}+e^{2\theta}}d\theta = \sqrt{2}[e^\theta]_0^{2\pi} = \sqrt{2}(e^{2\pi}-1)$.

**Q72.** `[N]` A particle moves along the parametric curve $x(t) = \int_0^t \cos(s^2)ds$, $y(t) = \int_0^t \sin(s^2)ds$ (the Euler/Cornu spiral). What is the speed of the particle at time $t$?
> **Answer:** $\frac{dx}{dt} = \cos(t^2)$, $\frac{dy}{dt} = \sin(t^2)$. Speed $= \sqrt{\cos^2(t^2)+\sin^2(t^2)} = 1$. The particle always moves at unit speed.

---

## Calculus 3

### Topic 5: Vectors, Lines, and Planes

**Q73.** `[C]` What does the sign of $\vec{a}\cdot\vec{b}$ tell you about the angle between the vectors?
> **Answer:** Positive $\implies$ acute angle; zero $\implies$ perpendicular; negative $\implies$ obtuse angle.

**Q74.** `[P]` Find a unit vector in the direction of $\vec{v}=\langle 3,-4,0\rangle$.
> **Answer:** $|\vec{v}|=5$. Unit vector: $\langle 3/5, -4/5, 0\rangle$.

**Q75.** `[P]` Find $\vec{a}\times\vec{b}$ where $\vec{a}=\langle 1,2,3\rangle$ and $\vec{b}=\langle 4,5,6\rangle$.
> **Answer:** $\vec{a}\times\vec{b}=\langle 2\cdot6-3\cdot5, 3\cdot4-1\cdot6, 1\cdot5-2\cdot4\rangle = \langle -3, 6, -3\rangle$.

**Q76.** `[P]` Find the equation of the plane through $(1,2,3)$ with normal vector $\vec{n}=\langle 2,-1,4\rangle$.
> **Answer:** $2(x-1)-(y-2)+4(z-3)=0 \implies 2x-y+4z=12$.

**Q77.** `[P]` Find the distance from the point $(2,1,-1)$ to the plane $x+2y+2z=5$.
> **Answer:** $d = \frac{|1(2)+2(1)+2(-1)-5|}{\sqrt{1+4+4}} = \frac{|2+2-2-5|}{3} = \frac{3}{3} = 1$.

**Q78.** `[P]` Find the angle between the planes $x+y+z=1$ and $x-y+z=0$.
> **Answer:** $\cos\theta = \frac{|\vec{n_1}\cdot\vec{n_2}|}{|\vec{n_1}||\vec{n_2}|} = \frac{|1-1+1|}{\sqrt{3}\cdot\sqrt{3}} = \frac{1}{3}$. $\theta = \cos^{-1}(1/3)$.

**Q79.** `[CT]` Find the volume of the parallelepiped with edges $\vec{a}=\langle 1,2,3\rangle$, $\vec{b}=\langle 0,1,2\rangle$, $\vec{c}=\langle 0,0,1\rangle$.
> **Answer:** $|(\vec{a}\times\vec{b})\cdot\vec{c}| = |\det\begin{bmatrix}1&2&3\\0&1&2\\0&0&1\end{bmatrix}| = |1| = 1$.

**Q80.** `[N]` If $|\vec{a}|=3$, $|\vec{b}|=4$, and $\vec{a}\cdot\vec{b}=6$, find $|\vec{a}\times\vec{b}|$.
> **Answer:** $|\vec{a}\times\vec{b}|=|\vec{a}||\vec{b}|\sin\theta$. First find $\cos\theta = 6/(3\cdot4)=1/2$, so $\theta=\pi/3$ and $\sin\theta=\sqrt{3}/2$. $|\vec{a}\times\vec{b}|=3\cdot4\cdot\frac{\sqrt{3}}{2}=6\sqrt{3}$.

---

### Topic 6: Partial Derivatives and Optimization

**Q81.** `[C]` Explain the geometric meaning of $f_x(a,b)$ on the surface $z=f(x,y)$.
> **Answer:** $f_x(a,b)$ is the slope of the tangent line to the surface in the direction of the positive $x$-axis at the point $(a,b,f(a,b))$.

**Q82.** `[P]` Find all partial derivatives of $f(x,y)=x^3y^2+e^{xy}$.
> **Answer:** $f_x=3x^2y^2+ye^{xy}$, $f_y=2x^3y+xe^{xy}$.

**Q83.** `[P]` Verify Clairaut's Theorem: show $f_{xy}=f_{yx}$ for $f=x^2\sin(y)$.
> **Answer:** $f_x=2x\sin y$, $f_{xy}=2x\cos y$. $f_y=x^2\cos y$, $f_{yx}=2x\cos y$. Equal. ✓

**Q84.** `[P]` Find the equation of the tangent plane to $z=x^2+2y^2$ at $(1,-1,3)$.
> **Answer:** $f_x=2x=2$, $f_y=4y=-4$ at $(1,-1)$. Plane: $z-3=2(x-1)-4(y+1) \implies z=2x-4y-3$.

**Q85.** `[P]` Find the critical points of $f(x,y)=x^3+y^3-3xy$ and classify them.
> **Answer:** $f_x=3x^2-3y=0$, $f_y=3y^2-3x=0$. From first: $y=x^2$. Sub: $3x^4-3x=0 \implies x(x^3-1)=0$. Points: $(0,0)$ and $(1,1)$. $D=f_{xx}f_{yy}-f_{xy}^2=6x\cdot6y-(-3)^2=36xy-9$. At $(0,0)$: $D=-9<0$ (saddle). At $(1,1)$: $D=36-9=27>0$, $f_{xx}=6>0$ (local min).

**Q86.** `[P]` Find the maximum and minimum values of $f(x,y)=x^2+y^2$ subject to $x^2+xy+y^2=3$ using Lagrange multipliers.
> **Answer:** $\nabla f = \lambda \nabla g$: $\langle 2x,2y\rangle = \lambda\langle 2x+y, x+2y\rangle$. By symmetry, try $y=x$: $g: 3x^2=3\implies x=\pm1$. $f=2$. Try $y=-x$: $g: -x^2=3$ (no real solutions). Try solving the system: from $2x=\lambda(2x+y)$ and $2y=\lambda(x+2y)$, divide to get $x/y=(2x+y)/(x+2y)$. Cross multiply: $2x^2+xy=2xy+y^2 \implies 2x^2-xy-y^2=0 \implies (2x+y)(x-y)=0$. Either $y=-2x$ or $y=x$. Proceed similarly. The min is $2$ and max is $6$.

**Q87.** `[CT]` Find the point on the plane $x+2y+3z=6$ closest to the origin.
> **Answer:** Minimize $f=x^2+y^2+z^2$ subject to $g: x+2y+3z=6$. Lagrange: $\langle 2x,2y,2z\rangle=\lambda\langle1,2,3\rangle$. So $x=\lambda/2, y=\lambda, z=3\lambda/2$. Substitute: $\lambda/2+2\lambda+9\lambda/2=6\implies 7\lambda=6\implies\lambda=6/7$. Point: $(3/7, 6/7, 9/7)$.

**Q88.** `[N]` Without computing, explain how the method of Lagrange multipliers generalizes finding extrema on closed bounded intervals.
> **Answer:** On a bounded closed region in $\mathbb{R}^1$, we check endpoints (the boundary constraint $x=a$ or $x=b$) and interior critical points. Lagrange multipliers extends this: we find interior critical points ($\nabla f=0$) plus boundary critical points by enforcing the constraint $\nabla f = \lambda \nabla g$.

---

### Topic 7: Multiple Integrals

**Q89.** `[C]` Explain the geometric meaning of $\iint_R f(x,y)dA$ when $f(x,y) \ge 0$.
> **Answer:** It gives the volume of the solid between the surface $z=f(x,y)$ and the $xy$-plane over the region $R$.

**Q90.** `[P]` Evaluate $\int_0^1\int_0^{2}(x+2y)dy\,dx$.
> **Answer:** Inner: $[xy+y^2]_0^2=2x+4$. Outer: $[x^2+4x]_0^1=5$.

**Q91.** `[P]` Evaluate $\int_0^1\int_x^1 \sin(y^2)dy\,dx$ by reversing the order of integration.
> **Answer:** Region: $0\le x\le y\le 1$. Reverse: $\int_0^1\int_0^y \sin(y^2)dx\,dy = \int_0^1 y\sin(y^2)dy = [-\frac{1}{2}\cos(y^2)]_0^1 = \frac{1-\cos 1}{2}$.

**Q92.** `[P]` Evaluate the double integral over the disk $x^2+y^2\le 4$: $\iint_D (x^2+y^2)dA$.
> **Answer:** Polar: $\int_0^{2\pi}\int_0^2 r^2 \cdot r\,dr\,d\theta = 2\pi \cdot [r^4/4]_0^2 = 2\pi\cdot 4 = 8\pi$.

**Q93.** `[P]` Find the volume of the solid bounded above by $z=4-x^2-y^2$ and below by $z=0$.
> **Answer:** $\iint_D (4-x^2-y^2)dA$ where $D$ is $x^2+y^2\le 4$. Polar: $\int_0^{2\pi}\int_0^2(4-r^2)r\,dr\,d\theta=2\pi[2r^2-r^4/4]_0^2=2\pi(8-4)=8\pi$.

**Q94.** `[P]` Evaluate the triple integral $\int_0^1\int_0^{2}\int_0^{3}xyz\,dz\,dy\,dx$.
> **Answer:** $[xyz^2/2]_0^3=9xy/2$. $\int_0^2 9xy/2\,dy=[9xy^2/4]_0^2=9x$. $\int_0^1 9x\,dx=9/2$.

**Q95.** `[CT]` Evaluate $\iiint_E z\,dV$ where $E$ is the region bounded above by $z=\sqrt{4-x^2-y^2}$ and below by the plane $z=0$.
> **Answer:** Hemisphere of radius 2. Use spherical: $z=\rho\cos\phi$, $dV=\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$. $\int_0^{2\pi}\int_0^{\pi/2}\int_0^2 \rho\cos\phi\cdot\rho^2\sin\phi\,d\rho\,d\phi\,d\theta = 2\pi\cdot[r^4/4]_0^2\cdot[\sin^2\phi/2]_0^{\pi/2}=2\pi\cdot 4\cdot\frac{1}{2}=4\pi$.

**Q96.** `[N]` Use a Jacobian to compute $\iint_R (x+y)^2 dA$ where $R$ is the square bounded by $x+y=0, x+y=1, x-y=0, x-y=1$.
> **Answer:** Let $u=x+y$, $v=x-y$. Then $x=(u+v)/2$, $y=(u-v)/2$. Jacobian $=|J|=1/2$. Region becomes $0\le u\le 1$, $0\le v\le 1$. $\int_0^1\int_0^1 u^2 \cdot\frac{1}{2}\,dv\,du = \frac{1}{2}\cdot\frac{1}{3}=\frac{1}{6}$.

---

### Topic 8: Vector Calculus

**Q97.** `[C]` Explain what it means for a vector field to be conservative and state two equivalent conditions.
> **Answer:** Conservative means $\vec{F}=\nabla f$ for some scalar potential $f$. Equivalent: (1) $\oint_C \vec{F}\cdot d\vec{r}=0$ for every closed curve; (2) In simply connected domains, $\nabla\times\vec{F}=\vec{0}$.

**Q98.** `[P]` Evaluate $\int_C \vec{F}\cdot d\vec{r}$ where $\vec{F}=\langle 2xy, x^2\rangle$ along $y=x^2$ from $(0,0)$ to $(1,1)$.
> **Answer:** Check if conservative: $\partial(2xy)/\partial y = 2x = \partial(x^2)/\partial x$. Yes. Potential $f: f_x=2xy\implies f=x^2y+g(y)$. $f_y=x^2=x^2 \implies g'(y)=0$. $f=x^2y$. Integral $=f(1,1)-f(0,0)=1$.

**Q99.** `[P]` Calculate $\oint_C \vec{F}\cdot d\vec{r}$ where $\vec{F}=\langle -y, x\rangle$ and $C$ is the unit circle (counterclockwise).
> **Answer:** $\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=1-(-1)=2$. By Green's: $\iint_D 2\,dA = 2\pi(1)^2 = 2\pi$.

**Q100.** `[P]` Find the divergence of $\vec{F}=\langle x^2y, y^3z, z^2x\rangle$.
> **Answer:** $\nabla\cdot\vec{F}=2xy+3y^2z+2zx$.

**Q101.** `[P]` Evaluate $\iint_S \vec{F}\cdot d\vec{S}$ where $\vec{F}=\langle x,y,z\rangle$ and $S$ is the closed unit sphere.
> **Answer:** Divergence Theorem: $\nabla\cdot\vec{F}=3$. $\iiint_E 3\,dV=3\cdot\frac{4\pi}{3}=4\pi$.

**Q102.** `[CT]` Verify Green's Theorem for $\vec{F}=\langle y^2, x\rangle$ over the region $D$ bounded by $y=x$ and $y=x^2$.
> **Answer:** Direct: Two curve integrals. Via Green's: $\iint_D(1-2y)dA = \int_0^1\int_{x^2}^x(1-2y)dy\,dx$. Evaluate and compare.

**Q103.** `[CT]` Use Stokes' Theorem to evaluate $\oint_C \vec{F}\cdot d\vec{r}$ for $\vec{F}=\langle yz, xz, xy\rangle$, where $C$ is the boundary of the triangle with vertices $(1,0,0)$, $(0,1,0)$, $(0,0,1)$.
> **Answer:** $\nabla\times\vec{F}=\langle x-x, y-y, z-z\rangle=\vec{0}$. So $\vec{F}$ is conservative, and the line integral is $0$.

**Q104.** `[N]` Explain physically why $\nabla\times(\nabla f)=\vec{0}$ for any smooth scalar function $f$.
> **Answer:** If $\vec{F}=\nabla f$ (conservative), the work around any closed loop is zero. By Stokes' theorem, $\oint_C \vec{F}\cdot d\vec{r}=\iint_S(\nabla\times\vec{F})\cdot d\vec{S}=0$ for all surfaces $S$, which forces $\nabla\times\vec{F}=\vec{0}$.

**Q105.** `[N]` Explain physically why $\nabla\cdot(\nabla\times\vec{F})=0$ (the divergence of a curl is always zero).
> **Answer:** By the Divergence Theorem, the outward flux of $\nabla\times\vec{F}$ through any closed surface equals $\iiint \nabla\cdot(\nabla\times\vec{F})dV$. But by Stokes' theorem applied to the boundary (which is empty for a closed surface), the flux is also $0$. So $\nabla\cdot(\nabla\times\vec{F})=0$.

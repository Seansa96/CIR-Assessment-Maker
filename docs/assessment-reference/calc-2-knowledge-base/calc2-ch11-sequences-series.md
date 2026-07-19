# Chapter 11: Infinite Sequences and Series

## Introduction

In calculus, we are often concerned with the behavior of processes that continue indefinitely. The paradox of Zeno, which asks how one can traverse an infinite number of halfway points to reach a destination in finite time, is fundamentally a question about infinite series. 

In this chapter, we formalize the concept of an infinite list of numbers (a sequence) and the infinite sum of those numbers (a series). These concepts are the bedrock of higher mathematics, allowing us to approximate highly complex non-polynomial functions (like $\sin x$ and $e^x$) using infinite polynomials known as Power Series.

---

## 11.1 Sequences

### 11.1.1 Formal Definition and Limits
A sequence is an ordered list of numbers: $a_1, a_2, a_3, \dots, a_n, \dots$. Formally, a sequence is a function whose domain is the set of positive integers.

We say that a sequence $\{a_n\}$ **converges** to a limit $L$, written $\lim_{n \to \infty} a_n = L$, if the terms $a_n$ approach $L$ as $n$ becomes very large.
> **Formal ($\varepsilon-N$) Definition of a Limit of a Sequence:**
> $\lim_{n \to \infty} a_n = L$ means that for every real number $\varepsilon > 0$, there exists an integer $N$ such that if $n > N$, then $|a_n - L| < \varepsilon$.

If the limit does not exist (or is infinite), the sequence **diverges**.

### 11.1.2 Limit Laws and The Squeeze Theorem
The limit laws for sequences perfectly mirror the limit laws for real-valued functions. If $\{a_n\}$ and $\{b_n\}$ are convergent sequences:
- $\lim_{n \to \infty} (a_n \pm b_n) = \lim_{n \to \infty} a_n \pm \lim_{n \to \infty} b_n$
- $\lim_{n \to \infty} (c a_n) = c \lim_{n \to \infty} a_n$
- $\lim_{n \to \infty} (a_n b_n) = (\lim_{n \to \infty} a_n)(\lim_{n \to \infty} b_n)$

> **The Squeeze Theorem for Sequences:**
> If $a_n \le b_n \le c_n$ for all $n \ge n_0$ and $\lim a_n = \lim c_n = L$, then $\lim b_n = L$.

**Example 1: Using the Squeeze Theorem**
Find the limit of the sequence $a_n = \frac{\sin(n)}{n}$.

*Solution:*
Since the sine function is bounded, we know that $-1 \le \sin(n) \le 1$.
Divide all parts of the inequality by $n$ (since $n > 0$):
$$ -\frac{1}{n} \le \frac{\sin(n)}{n} \le \frac{1}{n} $$
We know that $\lim_{n \to \infty} -\frac{1}{n} = 0$ and $\lim_{n \to \infty} \frac{1}{n} = 0$.
By the Squeeze Theorem, $\lim_{n \to \infty} \frac{\sin(n)}{n} = 0$.

### 11.1.3 Monotonic Sequences
A sequence is **nondecreasing** if $a_n \le a_{n+1}$ for all $n$, and **nonincreasing** if $a_n \ge a_{n+1}$ for all $n$. A sequence is **monotone** if it has either property. “Strictly increasing” and “strictly decreasing” use strict inequalities, but strictness is not required by the monotone convergence theorem.
A sequence is **bounded above** if there is a number $M$ such that $a_n \le M$ for all $n$.

> **Monotonic Sequence Theorem:**
> Every bounded, monotonic sequence is convergent.
> *(Proof of this theorem relies on the Completeness Axiom of the real numbers).*

---

## 11.2 Infinite Series

An infinite series is the sum of the terms of an infinite sequence:
$$ \sum_{n=1}^\infty a_n = a_1 + a_2 + a_3 + \dots $$
To determine if an infinite sum evaluates to a finite number, we look at the sequence of its **partial sums**, $s_n$:
$s_1 = a_1$
$s_2 = a_1 + a_2$
$s_n = \sum_{i=1}^n a_i$

If the sequence of partial sums $\{s_n\}$ converges to a limit $S$, then the series **converges** and its sum is $S$. Otherwise, the series **diverges**.

### 11.2.1 The Geometric Series
The geometric series is one of the very few series where we can explicitly find the sum.
$$ \sum_{n=1}^\infty a r^{n-1} = a + ar + ar^2 + \dots $$
The $n$th partial sum is $s_n = a \frac{1 - r^n}{1 - r}$.
- If $|r| < 1$, then $r^n \to 0$ as $n \to \infty$. The series **converges**, and its sum is $S = \frac{a}{1 - r}$.
- If $|r| \ge 1$, the sequence $r^n$ does not converge to 0, and the series **diverges**.

**Example 2: A Geometric Series**
Find the sum of the series $\sum_{n=1}^\infty 5 \left(-\frac{2}{3}\right)^{n-1}$.

*Solution:*
This is a geometric series with $a = 5$ and $r = -2/3$. Since $|-2/3| < 1$, it converges.
$$ S = \frac{a}{1 - r} = \frac{5}{1 - (-2/3)} = \frac{5}{5/3} = 3 $$

### 11.2.2 Telescoping Series
A telescoping series is one where intermediate terms cancel out in the partial sum, leaving only the first and last terms.

**Example 3: Telescoping Sum**
Evaluate $\sum_{n=1}^\infty \frac{1}{n(n+1)}$.

*Solution:*
Using partial fractions, $\frac{1}{n(n+1)} = \frac{1}{n} - \frac{1}{n+1}$.
Write out the $n$th partial sum:
$$ s_n = \left(1 - \frac{1}{2}\right) + \left(\frac{1}{2} - \frac{1}{3}\right) + \left(\frac{1}{3} - \frac{1}{4}\right) + \dots + \left(\frac{1}{n} - \frac{1}{n+1}\right) $$
Notice the massive cancellation. Everything cancels except the first and last terms:
$$ s_n = 1 - \frac{1}{n+1} $$
Now take the limit as $n \to \infty$:
$$ \lim_{n \to \infty} \left( 1 - \frac{1}{n+1} \right) = 1 - 0 = 1 $$

### 11.2.3 The Test for Divergence
If a series is going to converge to a finite number, the numbers we are adding must eventually become infinitely small.
> **The Divergence Test:**
> If $\lim_{n \to \infty} a_n \neq 0$ (or does not exist), then the series $\sum_{n=1}^\infty a_n$ diverges.

*Crucial Warning:* The converse is FALSE. If the limit is 0, the test is inconclusive. The harmonic series $\sum \frac{1}{n}$ has terms that approach 0, yet the series diverges to infinity!

---

## Topic source modules for assessment authoring

The following modules are the source of truth for the five opening Infinite Series
topics in the application. Assessment authors should build questions from the
distinctions, proof obligations, and failure modes below rather than merely swapping
numbers in a stock convergence-test prompt.

### Sequences and Series Overview (`sequences-series`)

#### Why the distinction exists

A sequence and a series can use the same symbols while describing different limiting
processes. The sequence $(a_n)$ asks what happens to one term far out in the list. The
series $\sum a_n$ creates a new sequence

$$S_N=\sum_{n=1}^{N}a_n$$

and asks what happens to the accumulated total. Confusing these objects creates the
most persistent error in the unit: concluding that $\sum a_n$ converges merely because
$a_n\to0$. The harmonic example separates the ideas decisively:

$$\frac1n\to0,\qquad \sum_{n=1}^{\infty}\frac1n\text{ diverges}.$$

The correct implication points in only one direction. If $S_N\to S$, then
$a_N=S_N-S_{N-1}\to S-S=0$. Thus convergence of the series forces a zero term limit.
A zero term limit does not control how quickly positive contributions accumulate and
therefore cannot prove convergence.

#### How to reason from partial sums

Whenever cancellation or a closed finite-sum identity is visible, work with $S_N$
before taking any limit. Keeping $N$ finite makes each algebraic step legitimate and
prevents informal statements such as “the last term at infinity vanishes.” The workflow
is:

1. define the finite partial sum with its actual starting index;
2. simplify that finite expression;
3. identify every boundary term that survives;
4. take $N\to\infty$ only after the finite identity is established;
5. if approximation is involved, compute $R_N=S-S_N$ or bound the tail directly.

Changing finitely many terms can change the value of a convergent sum, but it cannot
change whether the series converges. This is useful for convergence classification but
must not be used when the requested quantity is the exact sum.

#### Recognition and misconception checks

- Wording such as “the terms approach” points to $(a_n)$; wording such as “the sum
  approaches” points to $(S_N)$.
- A finite partial sum is an ordinary finite number. The infinite series is a limit,
  not a partial sum with an infinite upper index substituted into an algebraic formula.
- Bounded terms do not imply bounded partial sums. The constant sequence $a_n=1$ is
  bounded, while its partial sums equal $N$.
- Positive terms make $S_N$ nondecreasing. A positive-term series converges exactly
  when those partial sums are also bounded above.

### Sequence Fundamentals (`sequence-fundamentals`)

#### Limit proofs and useful representations

An $\varepsilon$–$N$ proof must solve the inequality $|a_n-L|<\varepsilon$ for an
integer threshold. For $a_n=1/n$, choosing any integer $N>1/\varepsilon$ ensures
$n>N\Rightarrow1/n<\varepsilon$. Questions should test the construction of the
threshold and the role of “eventually,” rather than asking only for the definition.

For algebraic sequences, divide numerator and denominator by the dominant power of
$n$. For oscillatory sequences, isolate a bounded factor and squeeze it with a factor
that tends to zero. For exponentials and factorials, compare successive magnitudes or
rewrite logarithmically when direct algebra hides the growth rate.

Subsequences provide a clean divergence proof. If two subsequences approach different
limits, the full sequence cannot converge. For example, the even and odd subsequences
of $(-1)^n$ approach $1$ and $-1$. This is stronger and more precise than saying the
terms “bounce around.”

#### Monotone convergence workflow

The monotone convergence theorem is particularly valuable for recursive sequences,
where a direct formula may be unavailable. “Monotone” means nondecreasing or
nonincreasing; strict inequalities are not required. To use the theorem:

1. inspect early terms and solve the fixed-point equation only to guess a candidate
   bound and possible limit;
2. prove the bound by induction, including the base case;
3. prove monotonicity, often by factoring $a_{n+1}-a_n$ or comparing nonnegative
   squares;
4. invoke the theorem only after both properties are proved;
5. pass the now-established limit through continuous functions in the recurrence;
6. reject algebraic fixed points that conflict with the proved bounds.

Solving $L=f(L)$ before proving convergence supplies candidates, not a convergence
proof. A recurrence may have several fixed points, or an orbit may fail to approach
any of them.

#### Selection cues and traps

- Rational expression in $n$: dominant-power limit laws.
- Bounded oscillation multiplied by a vanishing factor: squeeze theorem.
- Alternating sequence with nonvanishing amplitude: inspect even and odd subsequences.
- Recursive definition: invariant bounds plus monotonicity.
- “Bounded” alone is insufficient; $(-1)^n$ is the standard counterexample.
- “Monotone” alone is insufficient; $a_n=n$ is increasing but unbounded.

### Geometric and Telescoping Series (`geometric-telescoping-series`)

#### Geometric structure and indexing

A series is geometric when the ratio of consecutive nonzero terms is a constant $r$.
For

$$a+ar+\cdots+ar^{N-1},$$

multiplying by $r$ and subtracting gives

$$(1-r)S_N=a(1-r^N),\qquad
S_N=\frac{a(1-r^N)}{1-r}\quad(r\ne1).$$

The infinite formula $a/(1-r)$ is valid only when $|r|<1$, because exactly then
$r^N\to0$. Authors must make the first included term explicit: a series starting at
$n=0$ and one starting at $n=1$ generally have different first terms even if their
summands look similar.

The exact geometric tail after $N$ included terms is

$$R_N=\frac{ar^N}{1-r}$$

when $a$ is the $n=0$ term. For an alternating ratio, the signed remainder and its
absolute error should be distinguished.

#### Telescoping as a finite identity

Telescoping is cancellation in the finite partial sum, not a convergence test that can
be declared from appearance. A summand of the form $u_n-u_{n+k}$ produces $k$ boundary
terms at each end. For $k=1$,

$$\sum_{n=m}^{N}(u_n-u_{n+1})=u_m-u_{N+1}.$$

For $k=2$,

$$\sum_{n=m}^{N}(u_n-u_{n+2})
=u_m+u_{m+1}-u_{N+1}-u_{N+2}.$$

The surviving lower terms depend on the starting index. Partial fractions often reveal
this form, but logarithms, radicals, factorial expressions, and products can telescope
after applying an identity. Infinite products must be handled through finite products
first; informal symbols such as “$\infty/\infty$” are not values or proofs.

#### Method selection and verification

- Constant consecutive ratio: geometric formula, after checking $|r|<1$.
- Rational term with shifted linear factors: partial fractions, then inspect cancellation.
- Difference $f(n+1)-f(n)$: write several finite terms to locate boundaries.
- Logarithm of a ratio: use $\log(x/y)=\log x-\log y$ and then telescope.
- Difference of radicals: rationalization may expose a shifted reciprocal difference.
- Always substitute a small $N$ into the derived $S_N$ formula to catch an index error.

### Alternating Series (`alternating-series`)

#### What the theorem proves

Write the series as $\sum(-1)^n b_n$ or $\sum(-1)^{n-1}b_n$ with $b_n\ge0$. The
alternating-series test proves convergence if:

1. $b_n\to0$; and
2. $b_n$ is eventually nonincreasing.

“Eventually” matters: finitely many early increases do not affect convergence. The
theorem does not prove absolute convergence, does not require a known exact sum, and
does not apply merely because some negative terms occur.

The proof explains the error estimate. Even partial sums and odd partial sums approach
the same limit from opposite sides, with the true sum trapped between consecutive
partial sums. Therefore

$$|R_N|=|S-S_N|\le b_{N+1}.$$

The error has the sign of the first omitted term when the conventional alternating
pattern and monotone hypotheses hold. This permits one-sided bounds as well as an
absolute-error guarantee.

#### How to verify monotonicity

Use the least expensive valid method:

- compare $b_{n+1}$ and $b_n$ algebraically when they are rational expressions;
- study $b_{n+1}/b_n\le1$ when products, powers, or factorials are present;
- embed $b_n=f(n)$ and show $f'(x)\le0$ on a tail interval;
- if monotonicity fails at a few initial indices, state the index after which it holds.

The term-limit check is independent and cannot be inferred from alternating signs.
For $(-1)^n(1+1/n)$, magnitudes decrease but approach $1$, so the series diverges by
the term test.

#### Remainder-bound workflow

To guarantee $|R_N|<\varepsilon$, solve $b_{N+1}<\varepsilon$ and respect whether the
requested inequality is strict. A theorem bound of exactly $\varepsilon$ does not prove
an error strictly below $\varepsilon$. When asked for the least integer $N$, verify the
candidate works and the preceding integer fails the sufficient inequality.

### Absolute and Conditional Convergence (`absolute-conditional-convergence`)

#### Classification is a two-question decision

For a signed series $\sum a_n$, first ask whether $\sum|a_n|$ converges.

- If it does, $\sum a_n$ is absolutely convergent; no second convergence test is needed.
- If $\sum|a_n|$ diverges, determine independently whether $\sum a_n$ converges.
- If the signed series converges while the absolute-value series diverges, convergence
  is conditional.
- If the signed series itself diverges, it is simply divergent; “conditionally
  divergent” is not a valid classification.

The theorem that absolute convergence implies convergence follows from decomposing
$a_n$ into positive and negative parts, each bounded by $|a_n|$, or from the Cauchy
criterion and the triangle inequality.

#### Choosing tests for the absolute-value series

After removing signs, choose a test from the magnitude structure:

- rational powers of $n$: direct or limit comparison with a $p$-series;
- factorials and exponentials: ratio test;
- quantities raised to the $n$th power: root test;
- positive decreasing expressions tied naturally to an antiderivative: integral test.

The comparison direction is part of the proof. To prove convergence, bound above by a
known convergent series. To prove divergence, bound below by a known divergent series.
Limit comparison requires a finite positive comparison limit; a limit of $0$ or
$\infty$ can sometimes support a one-sided conclusion, but not the standard
same-behavior theorem.

#### Parameter boundaries and rearrangement

Parameterized classifications should separate theorem thresholds before combining
them. For

$$\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n^p},$$

the term test gives divergence for $p\le0$, the alternating-series test gives signed
convergence for $p>0$, and the $p$-series theorem gives absolute convergence only for
$p>1$. Hence the series is conditional on $0<p\le1$.

Absolute convergence permits arbitrary rearrangement without changing the sum.
Conditional convergence does not: rearrangement can change the sum or destroy
convergence. This is why the distinction is structural, not merely a label attached
after a convergence test.

---

## 11.3 - 11.7 Tests for Convergence

Because finding explicit sums (like in geometric or telescoping series) is extremely rare, we instead use logical tests to determine *if* a series converges.

### 11.3 The Integral Test
If the terms of a series match a continuous function, we can compare the sum of the rectangles to the area under the curve.

> **The Integral Test:**
> Suppose $f$ is a continuous, positive, decreasing function on $[1, \infty)$ and let $a_n = f(n)$. Then the series $\sum_{n=1}^\infty a_n$ is convergent if and only if the improper integral $\int_1^\infty f(x) \, dx$ is convergent.

**The p-series:** $\sum_{n=1}^\infty \frac{1}{n^p}$.
By the integral test, this converges if $p > 1$ and diverges if $p \le 1$.

### 11.4 The Comparison Tests
**The Direct Comparison Test:**
Suppose $\sum a_n$ and $\sum b_n$ are series with positive terms.
1. If $\sum b_n$ converges and $a_n \le b_n$, then $\sum a_n$ converges. (Smaller than a converging series converges).
2. If $\sum b_n$ diverges and $a_n \ge b_n$, then $\sum a_n$ diverges. (Larger than a diverging series diverges).

**The Limit Comparison Test:**
If $\lim_{n \to \infty} \frac{a_n}{b_n} = c > 0$, then both series share the same fate (both converge or both diverge). This is incredibly useful for rational functions where we compare to the dominant terms.

**Example 4: Limit Comparison**
Determine if $\sum_{n=1}^\infty \frac{3n+5}{\sqrt{n^4+1}}$ converges or diverges.

*Solution:*
For large $n$, the dominant term in the numerator is $3n$ and in the denominator is $\sqrt{n^4} = n^2$.
Let's compare to $b_n = \frac{n}{n^2} = \frac{1}{n}$.
$$ \lim_{n \to \infty} \frac{a_n}{b_n} = \lim_{n \to \infty} \frac{3n^2+5n}{\sqrt{n^4+1}} = 3 $$
Since the limit is a positive finite number, both series share the same fate. Because $\sum \frac{1}{n}$ is a divergent harmonic series, the original series diverges.

### 11.5 The Alternating Series Test
An alternating series has terms that alternate in sign: $\sum (-1)^{n-1} b_n = b_1 - b_2 + b_3 - \dots$
> **Alternating Series Test (AST):**
> An alternating series converges if it satisfies two conditions:
> 1. $b_{n+1} \le b_n$ for all $n$ (the sequence of absolute values is decreasing).
> 2. $\lim_{n \to \infty} b_n = 0$.

### 11.6 Absolute Convergence and the Ratio Test
A series $\sum a_n$ is called **absolutely convergent** if the series of absolute values $\sum |a_n|$ is convergent.
If a series is absolutely convergent, it is guaranteed to be convergent. 
If a series converges, but its absolute value diverges, it is called **conditionally convergent** (e.g., the alternating harmonic series $\sum \frac{(-1)^{n-1}}{n}$).

> **The Ratio Test:**
> Let $L = \lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right|$.
> - If $L < 1$, the series $\sum a_n$ is absolutely convergent.
> - If $L > 1$, the series is divergent.
> - If $L = 1$, the test is inconclusive.
>
> If the ratio limit does not exist, the basic form is inconclusive; a limsup
> version can sometimes be used but must be stated explicitly.

The ratio test is heavily favored when factorials ($n!$) or exponential terms ($c^n$) are present.

**Example 5: The Ratio Test**
Determine if $\sum_{n=1}^\infty \frac{n^3}{3^n}$ converges.

*Solution:*
$$ L = \lim_{n \to \infty} \left| \frac{(n+1)^3}{3^{n+1}} \cdot \frac{3^n}{n^3} \right| = \lim_{n \to \infty} \left( \frac{n+1}{n} \right)^3 \frac{1}{3} = (1)^3 \cdot \frac{1}{3} = \frac{1}{3} $$
Since $L < 1$, the series converges absolutely.

---

## 11.8 Power Series

A power series is an infinite polynomial:
$$ \sum_{n=0}^\infty c_n (x-a)^n = c_0 + c_1(x-a) + c_2(x-a)^2 + \dots $$
Where $x$ is a variable and the $c_n$'s are constants called the coefficients. The series is "centered" at $a$.

For any power series, there are only three possibilities for its domain of convergence:
1. The series converges only when $x = a$. (Radius $R = 0$)
2. The series converges for all $x$. (Radius $R = \infty$)
3. There is a positive number $R$ such that the series converges if $|x-a| < R$ and diverges if $|x-a| > R$. The interval is $(a-R, a+R)$. The endpoints $x = a-R$ and $x = a+R$ must be tested individually using chapter 11.3-11.7 tests!

We use the Ratio Test to find the radius of convergence $R$.

---

## 11.10 Taylor and Maclaurin Series

If a function $f(x)$ has a power series representation at $a$, what must the coefficients $c_n$ be?
By differentiating the power series repeatedly and evaluating at $x=a$, we find:
$$ c_n = \frac{f^{(n)}(a)}{n!} $$
Thus, the **Taylor Series** of $f$ centered at $a$ is:
$$ f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(a)}{n!} (x-a)^n = f(a) + \frac{f'(a)}{1!}(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \dots $$
If $a = 0$, this is called the **Maclaurin Series**.

### Important Maclaurin Series Expansions
Memorizing these is essentially mandatory:
- $\frac{1}{1-x} = \sum_{n=0}^\infty x^n \quad (-1 < x < 1)$
- $e^x = \sum_{n=0}^\infty \frac{x^n}{n!} \quad (\text{all } x)$
- $\sin x = \sum_{n=0}^\infty \frac{(-1)^n}{(2n+1)!} x^{2n+1} \quad (\text{all } x)$
- $\cos x = \sum_{n=0}^\infty \frac{(-1)^n}{(2n)!} x^{2n} \quad (\text{all } x)$

### Taylor's Inequality (The Remainder Theorem)
Just because we can write a Taylor series doesn't mean it actually equals the function $f(x)$ everywhere. We must prove that the remainder $R_n(x) = f(x) - T_n(x)$ approaches 0 as $n \to \infty$.
> **Taylor's Inequality:**
> If $|f^{(n+1)}(x)| \le M$ for $|x-a| \le d$, then the remainder $R_n(x)$ satisfies:
> $$ |R_n(x)| \le \frac{M}{(n+1)!} |x-a|^{n+1} \quad \text{for } |x-a| \le d $$
Because factorials grow vastly faster than exponentials, $\frac{|x|^{n+1}}{(n+1)!} \to 0$, which proves that the Taylor series for $\sin x, \cos x, e^x$ converge to the actual functions.

---

## 11.12 Advanced Series (100+1 Problems)

In Olympiad mathematics, series are used to prove irrationality, evaluate seemingly impossible limits, and solve complex combinatorics.

### 11.12.1 Proving the Irrationality of $e$
The Maclaurin series for $e^x$ evaluated at $x=1$ gives $e = \sum_{n=0}^\infty \frac{1}{n!}$.
We can use this to prove $e$ is irrational.
**Proof by Contradiction:**
Assume $e$ is rational, so $e = a/b$ where $a, b$ are positive integers.
Multiply the series by $b!$:
$$ b! e = b! \left( 1 + \frac{1}{1!} + \frac{1}{2!} + \dots + \frac{1}{b!} + \frac{1}{(b+1)!} + \dots \right) $$
Since $e = a/b$, the left side is $b! (a/b) = a(b-1)!$, which is an integer.
On the right side, the terms up to $\frac{1}{b!}$ multiplied by $b!$ are all integers. Let their sum be $K$.
The remaining "tail" is:
$$ x = \frac{b!}{(b+1)!} + \frac{b!}{(b+2)!} + \dots = \frac{1}{b+1} + \frac{1}{(b+1)(b+2)} + \dots $$
This tail $x$ is strictly greater than 0. Furthermore, it is strictly less than a geometric series with ratio $\frac{1}{b+1}$, which sums to $\frac{1}{b}$. Thus $0 < x < 1$.
But we have: Integer = Integer $+ x \implies x$ must be an integer.
This contradicts $0 < x < 1$. Thus, $e$ must be irrational.

### 11.12.2 Dirichlet's Test for Convergence
The Alternating Series Test is actually a special case of a much more powerful theorem used in advanced calculus.
> **Dirichlet's Test:**
> If $\{a_n\}$ is a sequence whose partial sums $A_n = \sum_{k=1}^n a_k$ are bounded (there exists $M$ such that $|A_n| \le M$ for all $n$), and $\{b_n\}$ is a decreasing sequence that converges to 0, then the series $\sum_{n=1}^\infty a_n b_n$ converges.

If we let $a_n = (-1)^n$, the partial sums oscillate between -1 and 0, which is bounded. Thus, Dirichlet's test immediately proves the Alternating Series Test! Dirichlet's test is heavily used to prove the convergence of Fourier series.

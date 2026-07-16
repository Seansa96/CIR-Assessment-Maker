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
A sequence is **increasing** if $a_n < a_{n+1}$ for all $n$, and **decreasing** if $a_n > a_{n+1}$ for all $n$. A sequence is **monotonic** if it is either entirely increasing or entirely decreasing.
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

# Chapter 5: Using the Integers

## Source scope

- Local source: *The Art of Problem Solving, Volume 1: The Basics*.
- Location: pdf 53-65; printed 39-51.
- Current AoPS topic: `aops-integers-number-theory`.
- This is an original instructional paraphrase for assessment authoring, not a reproduction of source exercises or solutions.

## Purpose and prerequisites

Integer problems reward structure over computation. Learners need signed arithmetic and prime factorization; the chapter develops divisibility, positional notation, congruence, and least-common-multiple reasoning. Its central habit is to replace a huge number or expression with the smaller fact that controls the requested property: a factorization, a remainder, or a final digit.

## Concept model

For nonzero integer $d$, saying $d\mid n$ means $n=dk$ for some integer $k$. Divisibility is an existence claim, so it is preserved by addition and subtraction of multiples of $d$. Prime factorization records which prime powers occur in an integer. The gcd contains each shared prime to the smaller exponent; the lcm contains every needed prime to the larger exponent. This yields $\gcd(a,b)\operatorname{lcm}(a,b)=|ab|$ for positive integers.

Base $b$ is a place-value system: the digits of $d_k\cdots d_0$ represent $\sum d_jb^j$, with $0\le d_j<b$. A last digit in base $b$ is a remainder modulo $b$. Congruence, $a\equiv c\pmod m$, means $m\mid(a-c)$; it says that $a$ and $c$ have the same remainder on division by $m$. Addition and multiplication respect congruence, so a difficult calculation may be performed with small representatives instead.

## Strategy selection

1. If the question asks about factors, divisors, gcd, lcm, or exact divisibility, factor into primes before trying arithmetic.
2. If it asks about a last digit, remainder, or a repeating pattern, choose a modulus that matches the target and look for a short cycle.
3. If it asks about a numeral in another base, expand it by place value or convert by repeated division; do not treat its written digits as decimal digits.
4. State the modulus and reduce legally at each step. A congruence is not an ordinary equality, so division or cancellation requires a separate justification.

## Misconceptions to target

- A prime has exactly two positive divisors; $1$ is neither prime nor composite.
- “Divides” points from divisor to dividend: $3\mid 15$, not the reverse.
- A decimal-looking numeral such as $101_2$ is five, not one hundred one.
- Congruent numbers may differ; $17\equiv2\pmod5$ does not mean $17=2$.
- A cycle may begin after a short preperiod, and an exponent should be reduced modulo the cycle length only after the cycle is established.

## Lesson-authoring moves

Use a single number to connect prime factors, divisor count, gcd/lcm, and remainder behavior. Have learners justify a familiar divisibility test using $10\equiv1\pmod9$, then contrast it with an invalid cancellation modulo a composite modulus. Good checks ask for a witness $k$, a chosen modulus and its purpose, or a verification of a base conversion.

## Assessment skills and evidence

- `factor-integers-and-use-divisibility`: factors and applies divisibility facts.
- `use-modular-arithmetic`: computes and reasons with congruence classes.
- `convert-and-reason-in-bases`: expands or converts positional representations.
- `compute-gcd-and-lcm`: selects prime exponents appropriate to gcd or lcm.
- `verify-integer-claims`: checks a proposed factor, remainder, or divisibility statement.


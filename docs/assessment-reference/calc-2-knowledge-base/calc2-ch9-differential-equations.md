# Chapter 9: Differential Equations

## Introduction to Modeling

In previous chapters, we analyzed functions that explicitly defined a relationship between two variables, such as $y = f(x)$. However, many laws of physics, chemistry, and biology are more naturally expressed in terms of *rates of change*. 

A **differential equation** is an equation that contains an unknown function and one or more of its derivatives. The **order** of a differential equation is the order of the highest derivative that occurs in the equation. A function $f$ is called a **solution** of a differential equation if the equation is satisfied when $y = f(x)$ and its derivatives are substituted into the equation.

**Examples of Models:**
- **Population Growth:** The rate of growth of a population is often proportional to the population size: $\frac{dP}{dt} = kP$.
- **Motion of a Spring:** By Newton's Second Law ($F=ma$) and Hooke's Law ($F=-kx$), the differential equation is $m \frac{d^2x}{dt^2} = -kx$.

---

## 9.2 Direction Fields and Euler's Method

### 9.2.1 Direction Fields
For a first-order differential equation of the form $y' = F(x,y)$, we cannot always find an explicit formula for the solution $y(x)$. However, we can analyze its behavior graphically.
At any point $(x,y)$, the equation tells us the slope $y'$ of the solution curve passing through that point. By drawing short line segments with slope $F(x,y)$ at a dense grid of points, we create a **direction field** (or slope field). The solution curves must flow parallel to these line segments.

### 9.2.2 Euler's Method
Euler's method is a numerical approach to approximate the solution to an initial value problem $y' = F(x,y), y(x_0) = y_0$.
Instead of a smooth curve, we approximate the solution using a sequence of connected line segments.
We choose a step size $h$. The approximation is generated iteratively:
$$ x_n = x_{n-1} + h $$
$$ y_n = y_{n-1} + h F(x_{n-1}, y_{n-1}) $$
Euler's method provides a discrete table of values that tracks the solution curve. However, because the slope is only updated at discrete intervals, the approximation tends to drift away from the true solution over long distances (accumulating error).

---

## 9.3 Separable Equations

A **separable equation** is a first-order differential equation in which the expression for $dy/dx$ can be factored as a function of $x$ strictly multiplied by a function of $y$:
$$ \frac{dy}{dx} = g(x) f(y) $$
This is the simplest class of differential equations to solve. We can "separate the variables" by moving all $y$ terms to the left and all $x$ terms to the right:
$$ \frac{1}{f(y)} dy = g(x) dx $$
Integrating both sides yields the implicit solution:
$$ \int \frac{1}{f(y)} \, dy = \int g(x) \, dx $$

### 9.3.1 Worked Examples

**Example 1: Separable Equation**
Solve the differential equation $\frac{dy}{dx} = \frac{x^2}{y^2}$.

*Solution:*
Separate variables by cross-multiplying: 
$$ y^2 dy = x^2 dx $$
Integrate both sides: 
$$ \int y^2 dy = \int x^2 dx \implies \frac{y^3}{3} = \frac{x^3}{3} + C $$
Multiply by 3: 
$$ y^3 = x^3 + 3C $$
Since $C$ is an arbitrary constant, $3C$ is also an arbitrary constant. Let's call it $K$. 
The general solution is $y = \sqrt[3]{x^3 + K}$.

**Example 2: Initial Value Problem**
Solve the initial-value problem: $\frac{dy}{dx} = y \cos x, \quad y(0) = 3$.

*Solution:*
Separate variables:
$$ \frac{dy}{y} = \cos x \, dx $$
Integrate both sides:
$$ \ln|y| = \sin x + C $$
Exponentiate both sides to solve for $y$:
$$ |y| = e^{\sin x + C} = e^C e^{\sin x} $$
Since $e^C$ is a positive constant, we can remove the absolute value by letting $A = \pm e^C$:
$$ y = A e^{\sin x} $$
Use the initial condition $y(0) = 3$:
$$ 3 = A e^{\sin(0)} = A e^0 = A $$
Thus, the specific solution is $y = 3e^{\sin x}$.

### 9.3.2 Orthogonal Trajectories
An **orthogonal trajectory** of a family of curves is a curve that intersects each curve of the family orthogonally (at right angles). This concept is heavily used in physics to describe equipotential lines and electric field lines.

**Example 3: Finding Orthogonal Trajectories**
Find the orthogonal trajectories of the family of curves $x = k y^2$.

*Solution:*
First, find the differential equation that describes the given family (independent of $k$). 
Differentiate $x = ky^2$ implicitly with respect to $x$: 
$$ 1 = 2ky \frac{dy}{dx} $$
Since $k = x/y^2$ (from the original equation), we substitute to eliminate $k$: 
$$ 1 = 2\left(\frac{x}{y^2}\right)y \frac{dy}{dx} = \frac{2x}{y} \frac{dy}{dx} $$
So the differential equation for the given family is $\frac{dy}{dx} = \frac{y}{2x}$.
Because the orthogonal trajectories must intersect at right angles, their tangent lines must have the negative reciprocal slope. The differential equation for the orthogonal trajectories is:
$$ \frac{dy}{dx} = -\frac{2x}{y} $$
This is a separable equation. Separate variables: 
$$ y \, dy = -2x \, dx $$
Integrate: 
$$ \frac{1}{2}y^2 = -x^2 + C \implies x^2 + \frac{1}{2}y^2 = C $$
This represents a family of ellipses.

---

## 9.4 Models for Population Growth

### 9.4.1 The Exponential Model
If resources are unlimited, populations grow at a rate proportional to their size:
$$ \frac{dP}{dt} = kP $$
This is a separable equation yielding the exponential growth function $P(t) = P_0 e^{kt}$.

### 9.4.2 The Logistic Equation
The exponential growth model is unrealistic in the long run because environments have a **carrying capacity** $M$. As $P$ approaches $M$, the growth rate must approach 0.
The **Logistic Equation** accounts for this:
$$ \frac{dP}{dt} = kP \left(1 - \frac{P}{M}\right) $$
Notice that if $P$ is small, $(1 - P/M) \approx 1$, resulting in exponential growth. As $P \to M$, the rate $\frac{dP}{dt} \to 0$.

This is a separable equation:
$$ \frac{dP}{P(1 - P/M)} = k \, dt $$
Using partial fractions, one can solve this to yield the explicit logistic growth function:
> **Logistic Solution:**
> $$ P(t) = \frac{M}{1 + A e^{-kt}} \quad \text{where } A = \frac{M - P_0}{P_0} $$
Notice that $\lim_{t \to \infty} P(t) = M$, confirming that the population stabilizes at the carrying capacity.

---

## 9.5 First-Order Linear Equations

A **first-order linear differential equation** is one that can be put into the standard form:
$$ \frac{dy}{dx} + P(x)y = Q(x) $$
Notice that $y$ and $dy/dx$ only appear to the first power, and they are not multiplied together.

### 9.5.1 The Integrating Factor
We cannot separate variables here. Instead, we multiply both sides by an **integrating factor** $I(x)$, chosen specifically so that the left side becomes the exact derivative of a product:
$$ I(x) \frac{dy}{dx} + I(x)P(x)y = I(x)Q(x) $$
We want the left side to be $\frac{d}{dx} [I(x)y] = I(x) \frac{dy}{dx} + I'(x)y$.
By comparing terms, we need $I'(x) = I(x)P(x)$. This is a separable equation: $\frac{dI}{I} = P(x) dx$.
Integrating gives $\ln|I| = \int P(x) dx$, so we choose:
> **Integrating Factor:**
> $$ I(x) = e^{\int P(x) dx} $$

After multiplying the standard form by $I(x)$, the equation becomes:
$$ \frac{d}{dx} [I(x)y] = I(x)Q(x) $$
Integrate both sides to solve for $y$:
$$ I(x)y = \int I(x)Q(x) \, dx $$

**Example 4: Linear Equation**
Solve the linear equation $x \frac{dy}{dx} - 2y = x^2$ for $x > 0$.

*Solution:*
First, divide by $x$ to get the standard form:
$$ \frac{dy}{dx} - \frac{2}{x}y = x $$
Here $P(x) = -2/x$. Find the integrating factor:
$$ I(x) = e^{\int -2/x dx} = e^{-2\ln x} = (e^{\ln x})^{-2} = x^{-2} = \frac{1}{x^2} $$
Multiply the standard form by $1/x^2$:
$$ \frac{1}{x^2} \frac{dy}{dx} - \frac{2}{x^3}y = \frac{1}{x} $$
The left side collapses exactly into the derivative of the product $(I(x)y)$:
$$ \frac{d}{dx} \left( \frac{1}{x^2} y \right) = \frac{1}{x} $$
Integrate both sides:
$$ \frac{1}{x^2} y = \ln x + C \implies y = x^2 \ln x + C x^2 $$

---

## 9.9 Advanced Differential Equations (100+1 Problems)

While Stewart Calculus stops at first-order linear equations, advanced calculus extends into non-linear forms that can be transformed into linear forms via clever substitutions.

### 9.9.1 Bernoulli Equations
A Bernoulli equation is a non-linear differential equation of the form:
$$ \frac{dy}{dx} + P(x)y = Q(x)y^n $$
where $n \neq 0$ and $n \neq 1$.
This can be transformed into a linear equation by substituting $u = y^{1-n}$.

**Example 5: Solving a Bernoulli Equation**
Solve $y' + y = x y^3$.

*Solution:*
Here $n=3$. We substitute $u = y^{1-3} = y^{-2}$.
Differentiating implicitly, $u' = -2y^{-3} y'$.
Divide the original equation by $y^3$:
$$ y^{-3}y' + y^{-2} = x $$
Substitute $y^{-2} = u$ and $y^{-3}y' = -\frac{1}{2}u'$:
$$ -\frac{1}{2}u' + u = x \implies u' - 2u = -2x $$
This is now a standard first-order linear equation in terms of $u$. The integrating factor is $I(x) = e^{\int -2 dx} = e^{-2x}$.
$$ \frac{d}{dx} (e^{-2x} u) = -2x e^{-2x} $$
Integrating the right side requires integration by parts:
$$ e^{-2x} u = \int -2x e^{-2x} dx = x e^{-2x} + \frac{1}{2}e^{-2x} + C $$
$$ u = x + \frac{1}{2} + C e^{2x} $$
Since $u = y^{-2} = 1/y^2$, the final solution is:
$$ y = \pm \left( x + \frac{1}{2} + C e^{2x} \right)^{-1/2} $$

### 9.9.2 Riccati Equations
A Riccati equation takes the form:
$$ \frac{dy}{dx} = P(x) + Q(x)y + R(x)y^2 $$
If a single particular solution $y_1(x)$ is known, the equation can be transformed into a linear equation via the substitution $y = y_1 + \frac{1}{u}$, or transformed into a second-order linear differential equation via $y = -\frac{u'}{R(x)u}$, which frequently results in Airy's equation or requires Bessel functions (topics typically reserved for a dedicated Differential Equations course).

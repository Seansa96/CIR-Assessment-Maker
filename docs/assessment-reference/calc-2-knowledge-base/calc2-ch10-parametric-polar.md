# Chapter 10: Parametric Equations and Polar Coordinates

## Introduction

Until now, we have predominantly studied curves that can be described by a single function $y = f(x)$. However, the physical universe rarely restricts itself to functions that pass the vertical line test. The trajectory of a planet orbiting the sun, the path of a rollercoaster loop, and the complex spirals found in a nautilus shell require a different mathematical framework.

In this chapter, we introduce two revolutionary ways to describe curves: **Parametric Equations** (which introduce a third "time" variable to track position) and **Polar Coordinates** (which locate points using angles and distances from a pole).

---

## 10.1 Curves Defined by Parametric Equations

Imagine that a particle moves along a curve $C$. It is impossible to describe the entire curve $C$ with an equation of the form $y = f(x)$ if the curve loops back on itself. However, we can express the $x$ and $y$ coordinates of the particle as independent functions of a third variable $t$ (called a parameter, which often represents time):
$$ x = f(t), \quad y = g(t) $$
These are called **parametric equations**. As $t$ varies over an interval $[\alpha, \beta]$, the point $(x, y) = (f(t), g(t))$ traces out a parametric curve $C$. The point $(f(\alpha), g(\alpha))$ is the **initial point**, and $(f(\beta), g(\beta))$ is the **terminal point**.

### 10.1.1 Eliminating the Parameter
To understand the shape of a parametric curve, it is often helpful to eliminate the parameter $t$ to form a Cartesian equation relating $x$ and $y$ directly.

**Example 1: Eliminating the Parameter**
Sketch the curve defined by $x = t^2 - 2t$, $y = t+1$.

*Solution:*
We can easily isolate $t$ in the equation for $y$:
$$ t = y - 1 $$
Substitute this into the equation for $x$:
$$ x = (y-1)^2 - 2(y-1) = y^2 - 2y + 1 - 2y + 2 = y^2 - 4y + 3 $$
This is a standard parabola that opens to the right, with its vertex at $(-1, 2)$. The parameter $t$ dictates that the particle travels along this parabola from bottom to top as $t$ increases.

### 10.1.2 The Cycloid
One of the most famous parametric curves is the **Cycloid**, which traces the path of a point on the edge of a rolling wheel of radius $r$. 
Let $\theta$ be the angle of rotation. The parametric equations for the cycloid are:
$$ x = r(\theta - \sin \theta) $$
$$ y = r(1 - \cos \theta) $$
*(It is virtually impossible to express the cycloid as a single Cartesian equation $y = f(x)$, making parametric equations absolutely essential).*

---

## 10.2 Calculus with Parametric Curves

### 10.2.1 Tangents and First Derivatives
If $x = f(t)$ and $y = g(t)$ are differentiable, we can find the slope of the tangent line $\frac{dy}{dx}$ without needing to eliminate the parameter $t$. By the Chain Rule, $\frac{dy}{dt} = \frac{dy}{dx} \cdot \frac{dx}{dt}$. Rearranging gives:
> **Parametric First Derivative:**
> $$ \frac{dy}{dx} = \frac{\frac{dy}{dt}}{\frac{dx}{dt}} \quad \text{provided } \frac{dx}{dt} \neq 0 $$

- **Horizontal Tangents** occur when $\frac{dy}{dt} = 0$ (and $\frac{dx}{dt} \neq 0$).
- **Vertical Tangents** occur when $\frac{dx}{dt} = 0$ (and $\frac{dy}{dt} \neq 0$).

### 10.2.2 Concavity and Second Derivatives
To find concavity, we need the second derivative $\frac{d^2y}{dx^2}$. 
*Warning:* $\frac{d^2y}{dx^2} \neq \frac{y''(t)}{x''(t)}$! 
Instead, we must apply the chain rule formula to the first derivative $\frac{dy}{dx}$ (which is itself a function of $t$, let's call it $h(t)$).
> **Parametric Second Derivative:**
> $$ \frac{d^2y}{dx^2} = \frac{d}{dx} \left( \frac{dy}{dx} \right) = \frac{\frac{d}{dt} \left( \frac{dy}{dx} \right)}{\frac{dx}{dt}} $$

**Example 2: Tangents and Concavity**
Find the tangent line and concavity of the curve $x = e^t, y = t e^{-t}$ at $t=0$.

*Solution:*
First, find $\frac{dx}{dt} = e^t$ and $\frac{dy}{dt} = e^{-t} - t e^{-t} = e^{-t}(1-t)$.
$$ \frac{dy}{dx} = \frac{e^{-t}(1-t)}{e^t} = e^{-2t}(1-t) $$
At $t=0$: $x=1, y=0$, and slope $m = e^0(1-0) = 1$.
The tangent line is $y - 0 = 1(x - 1) \implies y = x - 1$.
For concavity, differentiate $y'$ with respect to $t$:
$$ \frac{d}{dt}(y') = -2e^{-2t}(1-t) + e^{-2t}(-1) = e^{-2t}(-2 + 2t - 1) = e^{-2t}(2t - 3) $$
$$ \frac{d^2y}{dx^2} = \frac{e^{-2t}(2t - 3)}{e^t} = e^{-3t}(2t - 3) $$
At $t=0$, $\frac{d^2y}{dx^2} = 1(-3) = -3 < 0$, so the curve is **concave downward**.

### 10.2.3 Area, Arc Length, and Surface Area
The standard calculus formulas adapt beautifully to parametric equations via substitution $dx = x'(t)dt$ or $dy = y'(t)dt$.

**Area:** $A = \int_a^b y \, dx = \int_\alpha^\beta g(t) f'(t) \, dt$
**Arc Length:** $L = \int_\alpha^\beta \sqrt{\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2} \, dt$
**Surface Area ($x$-axis):** $S = \int_\alpha^\beta 2\pi y \sqrt{\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2} \, dt$

---

## 10.3 Polar Coordinates

A point $P$ in the Cartesian plane is defined by $(x,y)$, tracking horizontal and vertical distance. In the polar coordinate system, we locate $P$ by giving its polar coordinates $(r, \theta)$, where $r$ is the straight-line distance from the origin (the pole) to $P$, and $\theta$ is the angle measured counterclockwise from the positive $x$-axis.

### 10.3.1 Conversion Equations
By constructing a right triangle, we see the relationship between $(x,y)$ and $(r,\theta)$:
> **Polar to Cartesian:** $x = r \cos \theta, \quad y = r \sin \theta$
> **Cartesian to Polar:** $r^2 = x^2 + y^2, \quad \tan \theta = y/x$

### 10.3.2 Graphing Polar Curves
A polar curve $r = f(\theta)$ traces out points radially as the angle sweeps around the origin.
**Symmetry Tests:**
1. If replacing $\theta$ with $-\theta$ leaves the equation unchanged, the curve is symmetric about the **polar axis ($x$-axis)**. (True for cosine functions).
2. If replacing $\theta$ with $\pi-\theta$ leaves the equation unchanged, the curve is symmetric about the **line $\theta = \pi/2$ ($y$-axis)**. (True for sine functions).
3. If replacing $r$ with $-r$ (or $\theta$ with $\theta+\pi$) leaves the equation unchanged, the curve is symmetric about the **pole (origin)**.

**Families of Curves:**
- **Circles:** $r = a$ (centered at origin), $r = 2a\cos\theta$ (centered on $x$-axis), $r = 2a\sin\theta$ (centered on $y$-axis).
- **Limacons:** $r = a \pm b\cos\theta$ or $r = a \pm b\sin\theta$. If $a=b$, it forms a **Cardioid** (heart shape).
- **Roses:** $r = a\cos(k\theta)$ or $r = a\sin(k\theta)$. If $k$ is odd, it has $k$ petals. If $k$ is even, it has $2k$ petals.

### 10.3.3 Tangents to Polar Curves
To find the Cartesian slope $\frac{dy}{dx}$ of a polar curve $r = f(\theta)$, we parameterize the curve using $\theta$:
$$ x = r \cos \theta = f(\theta) \cos \theta $$
$$ y = r \sin \theta = f(\theta) \sin \theta $$
Using the parametric derivative formula:
$$ \frac{dy}{dx} = \frac{\frac{dy}{d\theta}}{\frac{dx}{d\theta}} = \frac{\frac{dr}{d\theta} \sin \theta + r \cos \theta}{\frac{dr}{d\theta} \cos \theta - r \sin \theta} $$

---

## 10.4 Areas and Lengths in Polar Coordinates

### 10.4.1 Area of a Polar Region
The area of a sector of a circle with radius $r$ and angle $\Delta \theta$ is $\frac{1}{2} r^2 \Delta \theta$.
By Riemann summing infinitely small sectors, the area bounded by a polar curve $r = f(\theta)$ between rays $\theta = a$ and $\theta = b$ is:
> **Polar Area:**
> $$ A = \int_a^b \frac{1}{2} [f(\theta)]^2 \, d\theta = \frac{1}{2} \int_a^b r^2 \, d\theta $$

**Example 3: Area of a Rose Petal**
Find the area of one loop of the four-leaved rose $r = \cos 2\theta$.

*Solution:*
One loop is traced out as the radius goes from 0 to 1 and back to 0. This occurs between $\theta = -\pi/4$ and $\theta = \pi/4$.
$$ A = \int_{-\pi/4}^{\pi/4} \frac{1}{2} r^2 \, d\theta = \frac{1}{2} \int_{-\pi/4}^{\pi/4} \cos^2(2\theta) \, d\theta $$
Use the half-angle identity $\cos^2 x = \frac{1}{2}(1 + \cos 2x)$:
$$ = \frac{1}{2} \int_{-\pi/4}^{\pi/4} \frac{1}{2}(1 + \cos 4\theta) \, d\theta = \frac{1}{4} \left[ \theta + \frac{1}{4}\sin 4\theta \right]_{-\pi/4}^{\pi/4} = \frac{1}{4} \left( \frac{\pi}{4} - \left(-\frac{\pi}{4}\right) \right) = \frac{\pi}{8} $$

### 10.4.2 Arc Length in Polar Coordinates
Applying the parametric arc length formula to $x = r \cos \theta, y = r \sin \theta$ yields a massive simplification due to the identity $\cos^2\theta + \sin^2\theta = 1$. The resulting formula is:
> **Polar Arc Length:**
> $$ L = \int_a^b \sqrt{r^2 + \left(\frac{dr}{d\theta}\right)^2} \, d\theta $$

---

## 10.9 Advanced Parametric and Polar Concepts (100+1 Problems)

### 10.9.1 Curvature
In advanced differential geometry, it is vital to measure how quickly a curve changes direction. This is called **curvature** ($\kappa$). 
For a parametric curve $(x(t), y(t))$, the curvature is defined exactly as:
$$ \kappa = \frac{|x' y'' - y' x''|}{[ (x')^2 + (y')^2 ]^{3/2}} $$
For a polar curve $r(\theta)$, substituting the polar conversions into the curvature formula yields:
$$ \kappa = \frac{|r^2 + 2(r')^2 - r r''|}{[ r^2 + (r')^2 ]^{3/2}} $$
This formula is frequently tested in Olympiad problems involving orbital mechanics, where identifying the points of maximum curvature corresponds to periapsis.

### 10.9.2 The Brachistochrone and Tautochrone Problem
The cycloid $x = r(\theta - \sin\theta), y = r(1-\cos\theta)$ is not just a geometric curiosity; it is the solution to two of the most famous problems in mathematical history.
1. **The Brachistochrone:** The curve of fastest descent. If a bead slides down a frictionless wire between two points, a cycloid path takes the least time—faster than a straight line!
2. **The Tautochrone:** The equal-time curve. If several beads are placed at different heights on an inverted cycloid, they will all reach the bottom at the exact same time, regardless of their starting height. This property is used in the design of highly accurate pendulum clocks.

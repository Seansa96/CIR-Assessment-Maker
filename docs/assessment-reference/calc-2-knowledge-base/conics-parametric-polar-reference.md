# Assessment Reference: Conics, Parametric, and Polar Curves

## 1. Concept Maps

### Conic Sections
- **Circles:** Center $(h, k)$, radius $r$. Equation: $(x-h)^2 + (y-k)^2 = r^2$.
- **Ellipses:** Center $(h, k)$, major axis $2a$, minor axis $2b$, foci distance $c$, where $c^2 = a^2 - b^2$.
- **Hyperbolas:** Center $(h, k)$, transverse axis $2a$, conjugate axis $2b$, foci distance $c$, where $c^2 = a^2 + b^2$.
- **Parabolas:** Vertex $(h, k)$, focus distance $p$. Equation: $(x-h)^2 = 4p(y-k)$ or $(y-k)^2 = 4p(x-h)$.

### Parametric Curves
- **Basics:** Two functions $x=f(t), y=g(t)$ defined on an interval $I$. Represents position over parameter $t$ (often time).
- **Derivatives:** $dy/dx = (dy/dt) / (dx/dt)$. Second derivative $d^2y/dx^2 = \frac{d}{dt}(dy/dx) / (dx/dt)$.
- **Integrals:** Area $= \int y(t)x'(t)dt$. Arc length $= \int \sqrt{(dx/dt)^2 + (dy/dt)^2}dt$.

### Polar Curves
- **Basics:** Coordinate system $(r, \theta)$. Transformations: $x = r \cos \theta$, $y = r \sin \theta$, $r^2 = x^2 + y^2$, $\tan \theta = y/x$.
- **Graph Families:** Lines, circles, cardioids, limacons, roses, lemniscates.
- **Calculus:** Area $= \frac{1}{2} \int r^2 d\theta$. Arc length $= \int \sqrt{r^2 + (dr/d\theta)^2} d\theta$. Tangent slope $dy/dx = \frac{r'(\theta)\sin\theta + r(\theta)\cos\theta}{r'(\theta)\cos\theta - r(\theta)\sin\theta}$.

## 2. Decision Trees

### Identifying Conic Sections from General Equation $Ax^2 + Cy^2 + Dx + Ey + F = 0$
- If $A=C$: Circle.
- If $A=0$ or $C=0$ (but not both): Parabola.
- If $A$ and $C$ have the same sign ($AC > 0$): Ellipse.
- If $A$ and $C$ have opposite signs ($AC < 0$): Hyperbola.

### Area Calculation Method
- Given $y=f(x)$: standard Riemann integral.
- Given $x=f(t), y=g(t)$: parametric area $\int y(t)x'(t)dt$.
- Given $r=f(\theta)$: polar area $\frac{1}{2} \int r^2 d\theta$. (Check for inner loops!).

## 3. Common Errors

### Conics
- Forgetting to factor out the leading coefficient before completing the square.
- Adding the wrong constant to the other side when completing the square (forgetting to multiply by the factored out coefficient).
- Swapping $a^2$ and $b^2$ relationships for ellipses vs hyperbolas.

### Parametric
- Calculating the second derivative as $(d^2y/dt^2) / (d^2x/dt^2)$ instead of the proper chain rule application.
- Ignoring domain restrictions when eliminating the parameter (e.g., $x=\sin t, y=\cos t \implies x^2+y^2=1$, but if $t \in [0, \pi]$, then $y \ge 0$).

### Polar
- Computing slope as $dr/d\theta$ instead of $dy/dx$.
- Missing intersection points because they correspond to different values of $\theta$ or negative $r$.
- Integrating over $[0, 2\pi]$ without realizing the curve traces completely in $[0, \pi]$ (e.g., $r = \cos(2\theta)$ traces in $2\pi$, but $r = \cos\theta$ traces in $\pi$).

## 4. Expected Answer Format Conventions

- Use `symbolicResponse` with `answer.expectedLatex` for exact values (e.g., `\pi / 4`, `\sqrt{2}`).
- Use `numericResponse` for approximations when specifically requested, with an appropriate `tolerance` (e.g., `0.01`).
- Provide fully simplified fractions and radicals when possible.
- In `multipleChoice` questions, distractors should represent the common errors listed above.

## 5. Difficulty Ladder

- **Easy (Recognition/Setup):** Match equations to graphs, evaluate derivatives at specific points given simple functions, identify parameters of a standard form conic.
- **Medium (Calculation):** Complete the square to find conic features, compute tangent line equations, set up area and arc length integrals.
- **Hard (Synthesis):** Find intersection points of complex polar curves, calculate area between two polar curves, identify orientation and restrictions from a parameter elimination.

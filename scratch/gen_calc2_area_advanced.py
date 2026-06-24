import os

def create_yaml(filename, content):
    path = os.path.join(r"c:\Users\SeanS\Downloads\cir_app\data\assessments", filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

area_method_selection = """
schemaVersion: 1
id: calc2-area-curves-method-selection-quiz
title: Area Between Curves - Method Selection
assessmentType: quiz
categoryId: calculus-2
subcategoryIds:
  - area-between-curves
navigation:
  learningGoal: practice
  activityType: focusedPractice
  tags:
    - advanced
    - exam-prep
modeDefault: practice
randomizeQuestions: true
questions:
  - id: area-method-1-dx-vs-dy
    type: multipleChoice
    prompt: |
      Consider the region bounded by $y = \sqrt{x}$, $y = x - 2$, and the $x$-axis. You are asked to set up an integral to find the area of this region. Which of the following statements about the setup is true?
    choices:
      - id: a
        text: 'Integrating with respect to $x$ requires only one integral, but integrating with respect to $y$ requires two.'
      - id: b
        text: 'Integrating with respect to $y$ requires only one integral, but integrating with respect to $x$ requires two.'
      - id: c
        text: 'Both methods require setting up two separate integrals.'
      - id: d
        text: 'Both methods require only one integral.'
    answer:
      choiceId: b
    explanation: |
      Let's analyze the region. The boundaries are $y = \sqrt{x}$ (top curve for some portion), $y = x - 2$ (bottom curve), and $y = 0$ ($x$-axis).
      
      **Integrating with respect to $x$:**
      The region goes from $x = 0$ to $x = 4$.
      From $x = 0$ to $x = 2$, the top boundary is $y = \sqrt{x}$ and the bottom is $y = 0$.
      From $x = 2$ to $x = 4$, the top boundary is $y = \sqrt{x}$ and the bottom is $y = x - 2$.
      Because the bottom boundary changes at $x = 2$, you **must split it into two integrals**:
      $$A = \int_0^2 (\sqrt{x} - 0) \, dx + \int_2^4 (\sqrt{x} - (x - 2)) \, dx$$
      
      **Integrating with respect to $y$:**
      We rewrite the equations in terms of $y$: $x = y^2$ and $x = y + 2$.
      The region goes from $y = 0$ to $y = 2$.
      For all $y$ in $[0, 2]$, the right boundary is always $x = y + 2$ and the left boundary is always $x = y^2$.
      Because the boundaries do not change, you need **only one integral**:
      $$A = \int_0^2 ((y + 2) - y^2) \, dy$$
      
      Thus, integrating with respect to $y$ is much more efficient here and requires only one integral.

  - id: area-method-2-horizontal-slicing
    type: multipleChoice
    prompt: |
      You need to find the area bounded by $x = 2y^2 - 4y$ and $x = 4y - y^2$. To find the intersection points, you should:
    choices:
      - id: a
        text: 'Solve the equations for $y$ in terms of $x$, then set them equal to each other.'
      - id: b
        text: 'Set $2y^2 - 4y = 4y - y^2$ and solve for $y$ to find the integration limits.'
      - id: c
        text: 'Take the derivative of both functions and find where they are equal.'
      - id: d
        text: 'Integrate both functions from $x = -2$ to $x = 4$.'
    answer:
      choiceId: b
    explanation: |
      The functions are already given as $x = f(y)$ and $x = g(y)$. This strongly suggests we should use horizontal slicing (integrate with respect to $y$). 
      
      To find the limits of integration, we must find where the curves intersect by setting the $x$-values equal to each other:
      $$2y^2 - 4y = 4y - y^2$$
      $$3y^2 - 8y = 0$$
      $$y(3y - 8) = 0 \implies y = 0, y = 8/3$$
      
      Attempting to solve for $y$ in terms of $x$ (Choice A) would require the quadratic formula, creating multiple messy radical functions that would be exceptionally difficult to integrate.

  - id: area-method-3-absolute-value
    type: multipleChoice
    prompt: |
      A student sets up the integral $\int_{-2}^{3} (f(x) - g(x)) \, dx$ to find the total area between the curves $y=f(x)$ and $y=g(x)$. However, the curves cross at $x = 1$. How should the total area be correctly represented?
    choices:
      - id: a
        text: '$\int_{-2}^{3} (f(x) - g(x)) \, dx$'
      - id: b
        text: '$\left| \int_{-2}^{3} (f(x) - g(x)) \, dx \right|$'
      - id: c
        text: '$\int_{-2}^{1} (f(x) - g(x)) \, dx + \int_{1}^{3} (g(x) - f(x)) \, dx$ (assuming $f(x) \ge g(x)$ on $[-2, 1]$)'
      - id: d
        text: '$\int_{-2}^{1} (f(x) + g(x)) \, dx - \int_{1}^{3} (f(x) + g(x)) \, dx$'
    answer:
      choiceId: c
    explanation: |
      When curves cross, the "top" and "bottom" functions switch. Total area is defined as the integral of the absolute difference: $\int |f(x) - g(x)| \, dx$.
      
      To calculate this without absolute value bars inside the integral, we must split the integral at the intersection point $x=1$ and ensure we are always subtracting the bottom function from the top function on each interval.
      
      If $f(x) \ge g(x)$ on $[-2, 1]$, then on $[1, 3]$, $g(x)$ must be greater than or equal to $f(x)$ (since they crossed). Therefore, the correct setup is:
      $$\int_{-2}^{1} (f(x) - g(x)) \, dx + \int_{1}^{3} (g(x) - f(x)) \, dx$$
      
      Taking the absolute value of the entire single integral (Choice B) is incorrect because the signed areas will cancel out *before* the absolute value is applied, yielding the net area instead of the total area.
"""

area_tricky = """
schemaVersion: 1
id: calc2-area-curves-tricky-quiz
title: Area Between Curves - Advanced & Tricky Edge Cases
assessmentType: quiz
categoryId: calculus-2
subcategoryIds:
  - area-between-curves
navigation:
  learningGoal: practice
  activityType: focusedPractice
  tags:
    - advanced
    - exam-prep
    - tricky
modeDefault: practice
randomizeQuestions: true
questions:
  - id: tricky-area-1-cubic-crossing
    type: multipleChoice
    prompt: |
      Find the **total area** bounded by the curves $y = x^3 - x^2 - 6x$ and $y = 0$.
    choices:
      - id: a
        text: '$\frac{253}{12}$'
      - id: b
        text: '$\frac{-63}{4}$'
      - id: c
        text: '$\frac{63}{4}$'
      - id: d
        text: '$\frac{343}{12}$'
    answer:
      choiceId: a
    explanation: |
      First, find the intersections by setting the equations equal:
      $$x^3 - x^2 - 6x = 0$$
      $$x(x^2 - x - 6) = 0$$
      $$x(x - 3)(x + 2) = 0 \implies x = -2, 0, 3$$
      
      Because there are three intersection points, the curves cross and the bounded region is split into two parts: $[-2, 0]$ and $[0, 3]$. We must find which function is on top for each interval.
      
      Test $x = -1$: $(-1)^3 - (-1)^2 - 6(-1) = -1 - 1 + 6 = 4 > 0$. So the cubic is on top on $[-2, 0]$.
      Test $x = 1$: $1^3 - 1^2 - 6(1) = -6 < 0$. So the $x$-axis ($y=0$) is on top on $[0, 3]$.
      
      Set up the two integrals for total area:
      $$A = \int_{-2}^{0} (x^3 - x^2 - 6x) \, dx + \int_{0}^{3} (0 - (x^3 - x^2 - 6x)) \, dx$$
      
      Evaluate the first integral:
      $$[\frac{1}{4}x^4 - \frac{1}{3}x^3 - 3x^2]_{-2}^{0} = 0 - (4 - (-\frac{8}{3}) - 12) = 0 - (4 + \frac{8}{3} - 12) = 0 - (-8 + \frac{8}{3}) = \frac{16}{3}$$
      
      Evaluate the second integral:
      $$\int_{0}^{3} (-x^3 + x^2 + 6x) \, dx = [-\frac{1}{4}x^4 + \frac{1}{3}x^3 + 3x^2]_{0}^{3} = (-\frac{81}{4} + 9 + 27) - 0 = 36 - \frac{81}{4} = \frac{144 - 81}{4} = \frac{63}{4}$$
      
      Total Area $= \frac{16}{3} + \frac{63}{4} = \frac{64}{12} + \frac{189}{12} = \frac{253}{12}$.
      
      *Common Error Trap:* If you just integrate from $-2$ to $3$ without splitting, you get $-63/4$, which is the net signed area, not the total enclosed area.

  - id: tricky-area-2-implicit
    type: multipleChoice
    prompt: |
      Which of the following represents the area bounded by the relation $|x| + |y| = 2$?
    choices:
      - id: a
        text: '$\int_{-2}^{2} (2 - |x|) \, dx$'
      - id: b
        text: '$2 \int_{-2}^{2} (2 - |x|) \, dx$'
      - id: c
        text: '$\int_{0}^{2} (2 - x) \, dx$'
      - id: d
        text: '$\int_{-2}^{2} ((2 - x) - (x - 2)) \, dx$'
    answer:
      choiceId: b
    explanation: |
      The equation $|x| + |y| = 2$ represents a square rotated by 45 degrees, centered at the origin, with vertices at $(2,0), (0,2), (-2,0), (0,-2)$.
      
      We can solve for $y$:
      $|y| = 2 - |x| \implies y = 2 - |x|$ (top half) OR $y = -(2 - |x|) = |x| - 2$ (bottom half).
      
      The area is the integral of the top function minus the bottom function from $x = -2$ to $x = 2$:
      $$A = \int_{-2}^{2} [(2 - |x|) - (|x| - 2)] \, dx$$
      $$A = \int_{-2}^{2} (4 - 2|x|) \, dx = 2 \int_{-2}^{2} (2 - |x|) \, dx$$
      
      Alternatively, using symmetry, we can find the area of the quadrant 1 triangle and multiply by 4:
      $$A = 4 \int_{0}^{2} (2 - x) \, dx$$
      
      Choice B matches the simplified full integral.

  - id: tricky-area-3-nonobvious-bounds
    type: multipleChoice
    prompt: |
      Find the area of the region bounded by $y = e^x$, $y = e^{-x}$, and $x = \ln(3)$.
    choices:
      - id: a
        text: '$4/3$'
      - id: b
        text: '$8/3$'
      - id: c
        text: '$e^3 - e^{-3}$'
      - id: d
        text: '$3 - 1/3$'
    answer:
      choiceId: a
    explanation: |
      First, find where the curves $y = e^x$ and $y = e^{-x}$ intersect.
      $$e^x = e^{-x}$$
      Multiply both sides by $e^x$:
      $$e^{2x} = 1 \implies 2x = \ln(1) = 0 \implies x = 0$$
      
      The region is bounded by $x=0$ on the left and $x=\ln(3)$ on the right.
      On the interval $[0, \ln(3)]$, $e^x \ge e^{-x}$ because $x \ge 0$.
      
      Setup the integral:
      $$A = \int_{0}^{\ln(3)} (e^x - e^{-x}) \, dx$$
      
      Evaluate the antiderivative:
      $$[e^x - (-e^{-x})]_{0}^{\ln(3)} = [e^x + e^{-x}]_{0}^{\ln(3)}$$
      
      Substitute the limits:
      $$= (e^{\ln(3)} + e^{-\ln(3)}) - (e^0 + e^{-0})$$
      $$= (3 + 3^{-1}) - (1 + 1)$$
      $$= (3 + \frac{1}{3}) - 2 = 1 + \frac{1}{3} = \frac{4}{3}$$
"""

create_yaml('calc2-area-curves-method-selection-quiz.yaml', area_method_selection)
create_yaml('calc2-area-curves-tricky-quiz.yaml', area_tricky)
print("Generated Area Between Curves advanced files.")

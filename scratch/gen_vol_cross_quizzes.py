import os

def create_yaml(filename, content):
    path = os.path.join(r"c:\Users\SeanS\Downloads\cir_app\data\assessments", filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

vol_easy_quiz = """
schemaVersion: 1
id: calc2-volumes-cross-sections-easy-quiz
title: Volumes by Cross Sections (Easy Quiz)
assessmentType: quiz
categoryId: calculus-2
subcategoryIds:
  - volumes-of-solids
modeDefault: practice
randomizeQuestions: true
tags:
  - calculus
  - volumes
  - cross-sections
questions:
  - id: vol-cross-eq-1
    title: Square Cross Sections on Circle
    type: numericResponse
    prompt: |
      The base of a solid is the region bounded by the circle $x^2 + y^2 = 1$. Cross-sections perpendicular to the $x$-axis are squares. Find the exact volume of the solid.
    answer:
      gradingMode: auto
      expectedLatex: 16/3
      equivalenceMode: numeric
      tolerance: 0.1
    explanation: |
      1. Base length $s = 2y = 2\sqrt{1-x^2}$.
      2. Area of square $A(x) = s^2 = 4(1-x^2)$.
      3. Volume $V = \int_{-1}^1 4(1-x^2) \, dx = 8 \int_0^1 (1-x^2) \, dx = 8[x - x^3/3]_0^1 = 8(2/3) = 16/3$.

  - id: vol-cross-eq-2
    title: Semicircles on Circle
    type: symbolicResponse
    prompt: |
      The base of a solid is the region bounded by $x^2 + y^2 = 4$. Cross-sections perpendicular to the $x$-axis are semicircles. Find the exact volume of the solid.
    answer:
      gradingMode: auto
      expectedLatex: 16\pi/3
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. Base length (diameter) $d = 2\sqrt{4-x^2}$.
      2. Area of semicircle $A(x) = \frac{\pi}{8} d^2 = \frac{\pi}{8} (4)(4-x^2) = \frac{\pi}{2}(4-x^2)$.
      3. Volume $V = \frac{\pi}{2} \int_{-2}^2 (4-x^2) \, dx = \pi \int_0^2 (4-x^2) \, dx = \pi [4x - x^3/3]_0^2 = \pi(8 - 8/3) = 16\pi/3$.

  - id: vol-cross-eq-3
    title: Squares on Parabola Base
    type: numericResponse
    prompt: |
      The base of a solid is the region bounded by $y = 1-x^2$ and the $x$-axis. Cross-sections perpendicular to the $x$-axis are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: 16/15
      equivalenceMode: numeric
      tolerance: 0.1
    explanation: |
      1. Base length $s = 1-x^2$.
      2. $A(x) = (1-x^2)^2 = 1 - 2x^2 + x^4$.
      3. Volume $V = \int_{-1}^1 (1 - 2x^2 + x^4) \, dx = 2[x - 2x^3/3 + x^5/5]_0^1 = 2(1 - 2/3 + 1/5) = 2(15/15 - 10/15 + 3/15) = 2(8/15) = 16/15$.

  - id: vol-cross-eq-4
    title: Squares on Radical Base
    type: numericResponse
    prompt: |
      The base of a solid is the region bounded by $y = \sqrt{x}$, $y = 0$, and $x = 4$. Cross-sections perpendicular to the $x$-axis are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: 8
      equivalenceMode: numeric
      tolerance: 0.1
    explanation: |
      1. Base length $s = \sqrt{x}$.
      2. $A(x) = s^2 = x$.
      3. $V = \int_0^4 x \, dx = [x^2/2]_0^4 = 16/2 = 8$.

  - id: vol-cross-eq-5
    title: Equilateral Triangles on Radical
    type: symbolicResponse
    prompt: |
      The base of a solid is the region bounded by $y = \sqrt{x}$, $y = 0$, and $x = 4$. Cross-sections perpendicular to the $x$-axis are equilateral triangles. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: 2\sqrt{3}
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. Base length $s = \sqrt{x}$.
      2. Area of equilateral triangle $A(x) = \frac{\sqrt{3}}{4}s^2 = \frac{\sqrt{3}}{4}x$.
      3. $V = \int_0^4 \frac{\sqrt{3}}{4}x \, dx = \frac{\sqrt{3}}{4}[x^2/2]_0^4 = \frac{\sqrt{3}}{4}(8) = 2\sqrt{3}$.

  - id: vol-cross-eq-6
    title: Squares Perpendicular to Y-axis
    type: numericResponse
    prompt: |
      The base of a solid is the region bounded by $y = x^2$ and $y = 4$. Cross-sections perpendicular to the **$y$-axis** are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: 32
      equivalenceMode: numeric
      tolerance: 0.1
    explanation: |
      1. Solving for $x$: $x = \pm\sqrt{y}$. Base length $s = 2\sqrt{y}$.
      2. $A(y) = s^2 = 4y$.
      3. $V = \int_0^4 4y \, dy = [2y^2]_0^4 = 2(16) = 32$.

  - id: vol-cross-eq-7
    title: Squares Between Curves
    type: numericResponse
    prompt: |
      The base of a solid is the region bounded by $y = x$ and $y = x^2$. Cross-sections perpendicular to the $x$-axis are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: 1/30
      equivalenceMode: numeric
      tolerance: 0.1
    explanation: |
      1. Intersections at $x=0, 1$. Base length $s = x - x^2$.
      2. $A(x) = (x-x^2)^2 = x^2 - 2x^3 + x^4$.
      3. $V = \int_0^1 (x^2 - 2x^3 + x^4) \, dx = [x^3/3 - x^4/2 + x^5/5]_0^1 = 1/3 - 1/2 + 1/5$.
      4. Common denominator 30: $10/30 - 15/30 + 6/30 = 1/30$.

  - id: vol-cross-eq-8
    title: Semicircles Between Curves
    type: symbolicResponse
    prompt: |
      The base of a solid is the region bounded by $y = x$ and $y = x^2$. Cross-sections perpendicular to the $x$-axis are semicircles. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: \pi/240
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. Base length (diameter) $d = x - x^2$.
      2. $A(x) = \frac{\pi}{8} d^2 = \frac{\pi}{8}(x^2 - 2x^3 + x^4)$.
      3. The integral of the polynomial part is $1/30$.
      4. Volume = $\frac{\pi}{8} \times \frac{1}{30} = \frac{\pi}{240}$.

  - id: vol-cross-eq-9
    title: Isosceles Right Triangles on Circle
    type: numericResponse
    prompt: |
      The base of a solid is the region bounded by $x^2 + y^2 = 9$. Cross-sections perpendicular to the $x$-axis are isosceles right triangles with one leg on the base. Find the volume.
    answer:
      gradingMode: auto
      expectedLatex: 72
      equivalenceMode: numeric
      tolerance: 0.1
    explanation: |
      1. Base length (leg of triangle) $s = 2y = 2\sqrt{9-x^2}$.
      2. Area of triangle $A(x) = \frac{1}{2}s^2 = \frac{1}{2}(4)(9-x^2) = 2(9-x^2)$.
      3. $V = \int_{-3}^3 2(9-x^2) \, dx = 4 \int_0^3 (9-x^2) \, dx = 4[9x - x^3/3]_0^3 = 4(27 - 9) = 4(18) = 72$.

  - id: vol-cross-eq-10
    title: Squares on Exponential
    type: symbolicResponse
    prompt: |
      The base of a solid is the region bounded by $y = e^x$, $y = 0$, $x = 0$, and $x = 1$. Cross-sections perpendicular to the $x$-axis are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: (e^2 - 1)/2
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. Base length $s = e^x$.
      2. $A(x) = (e^x)^2 = e^{2x}$.
      3. $V = \int_0^1 e^{2x} \, dx = [\frac{1}{2}e^{2x}]_0^1 = \frac{e^2 - 1}{2}$.
"""

vol_hard_quiz = """
schemaVersion: 1
id: calc2-volumes-cross-sections-hard-quiz
title: Volumes by Cross Sections (Hard Quiz)
assessmentType: quiz
categoryId: calculus-2
subcategoryIds:
  - volumes-of-solids
modeDefault: practice
randomizeQuestions: true
tags:
  - calculus
  - volumes
  - cross-sections
  - advanced
questions:
  - id: vol-cross-hq-1
    title: Shape Ratio Analysis
    type: symbolicResponse
    prompt: |
      Let $V_s$ be the volume of a solid whose base is $x^2 + y^2 = R^2$ with square cross sections, and $V_e$ be the volume of a solid with the same base but equilateral triangle cross sections. Find the ratio $V_s / V_e$.
    answer:
      gradingMode: auto
      expectedLatex: 4/\sqrt{3}
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. For squares, $A_s(x) = s^2$. For equilateral triangles, $A_e(x) = \frac{\sqrt{3}}{4}s^2$.
      2. The ratio of their areas at any cross section $x$ is constant: $A_s / A_e = 4/\sqrt{3}$.
      3. Therefore, the ratio of their integrated volumes is also $4/\sqrt{3}$.

  - id: vol-cross-hq-2
    title: Squares on Sine Wave
    type: symbolicResponse
    prompt: |
      The base of a solid is bounded by $y = \sin x$ and the $x$-axis for $0 \le x \le \pi$. Cross-sections perpendicular to the $x$-axis are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: \pi/2
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. $A(x) = \sin^2 x$.
      2. $V = \int_0^\pi \sin^2 x \, dx = \int_0^\pi \frac{1 - \cos(2x)}{2} \, dx$.
      3. Evaluate: $[\frac{1}{2}x - \frac{1}{4}\sin(2x)]_0^\pi = \frac{\pi}{2} - 0 = \pi/2$.

  - id: vol-cross-hq-3
    title: Equilateral Triangles on Secant
    type: symbolicResponse
    prompt: |
      The base of a solid is bounded by $y = \sec x$, $x = -\pi/4$, $x = \pi/4$, and the $x$-axis. Cross-sections perpendicular to the $x$-axis are equilateral triangles. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: \sqrt{3}/2
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. $A(x) = \frac{\sqrt{3}}{4} \sec^2 x$.
      2. $V = \int_{-\pi/4}^{\pi/4} \frac{\sqrt{3}}{4} \sec^2 x \, dx = \frac{\sqrt{3}}{4} [\tan x]_{-\pi/4}^{\pi/4}$.
      3. Evaluate: $\frac{\sqrt{3}}{4}(1 - (-1)) = \frac{2\sqrt{3}}{4} = \frac{\sqrt{3}}{2}$.

  - id: vol-cross-hq-4
    title: Squares on Ellipse (X-axis)
    type: numericResponse
    prompt: |
      The base of a solid is bounded by the ellipse $\frac{x^2}{4} + \frac{y^2}{9} = 1$. Cross-sections perpendicular to the **$x$-axis** are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: 96
      equivalenceMode: numeric
      tolerance: 0.1
    explanation: |
      1. Solving for $y$: $y = 3\sqrt{1 - x^2/4}$. The full base width $s = 2y = 6\sqrt{1 - x^2/4}$.
      2. $A(x) = s^2 = 36(1 - x^2/4)$.
      3. $V = \int_{-2}^2 36(1 - x^2/4) \, dx = 2 \int_0^2 36(1 - x^2/4) \, dx = 72[x - \frac{x^3}{12}]_0^2$.
      4. Evaluate: $72(2 - 8/12) = 72(2 - 2/3) = 72(4/3) = 24 \times 4 = 96$.

  - id: vol-cross-hq-5
    title: Squares on Ellipse (Y-axis)
    type: numericResponse
    prompt: |
      The base of a solid is bounded by the ellipse $\frac{x^2}{4} + \frac{y^2}{9} = 1$. Cross-sections perpendicular to the **$y$-axis** are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: 64
      equivalenceMode: numeric
      tolerance: 0.1
    explanation: |
      1. Solving for $x$: $x = 2\sqrt{1 - y^2/9}$. Full base width $s = 2x = 4\sqrt{1 - y^2/9}$.
      2. $A(y) = s^2 = 16(1 - y^2/9)$.
      3. $V = \int_{-3}^3 16(1 - y^2/9) \, dy = 2 \int_0^3 16(1 - y^2/9) \, dy = 32[y - \frac{y^3}{27}]_0^3$.
      4. Evaluate: $32(3 - 27/27) = 32(3 - 1) = 32(2) = 64$.

  - id: vol-cross-hq-6
    title: Hypotenuse on Base
    type: numericResponse
    prompt: |
      The base of a solid is bounded by $y = x^3$, $y = 8$, and the $y$-axis. Cross-sections perpendicular to the **$y$-axis** are isosceles right triangles with their hypotenuse on the base. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: 24/5
      equivalenceMode: numeric
      tolerance: 0.1
    explanation: |
      1. We integrate with respect to $y$. $x = y^{1/3}$. Base width $s = x - 0 = y^{1/3}$.
      2. For an isosceles right triangle with hypotenuse $s$, the area is $A = \frac{1}{4}s^2$.
      3. $A(y) = \frac{1}{4} (y^{1/3})^2 = \frac{1}{4} y^{2/3}$.
      4. $V = \int_0^8 \frac{1}{4} y^{2/3} \, dy = \frac{1}{4} [\frac{3}{5} y^{5/3}]_0^8$.
      5. Evaluate at 8: $\frac{3}{20} (8)^{5/3} = \frac{3}{20} (2^5) = \frac{3}{20}(32) = \frac{96}{20} = \frac{24}{5}$.

  - id: vol-cross-hq-7
    title: Rational Function Semicircles
    type: symbolicResponse
    prompt: |
      The base of a solid is bounded by $y = \frac{1}{x}$, $y = 0$, $x = 1$, and $x = 2$. Cross-sections perpendicular to the $x$-axis are semicircles. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: \pi/16
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. Base width $d = 1/x$.
      2. Area of semicircle $A(x) = \frac{\pi}{8} d^2 = \frac{\pi}{8} \frac{1}{x^2}$.
      3. $V = \int_1^2 \frac{\pi}{8x^2} \, dx = \frac{\pi}{8} [-\frac{1}{x}]_1^2$.
      4. Evaluate: $\frac{\pi}{8} (-1/2 - (-1)) = \frac{\pi}{8} (1/2) = \frac{\pi}{16}$.

  - id: vol-cross-hq-8
    title: Logarithmic Base Squares
    type: symbolicResponse
    prompt: |
      The base of a solid is bounded by $y = \ln x$, $y = 0$, and $x = e$. Cross-sections perpendicular to the $x$-axis are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: e - 2
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. Base width $s = \ln x$.
      2. $A(x) = (\ln x)^2$.
      3. $V = \int_1^e (\ln x)^2 \, dx$.
      4. Use integration by parts twice. The antiderivative of $(\ln x)^2$ is $x(\ln x)^2 - 2x\ln x + 2x$.
      5. Evaluate at $e$: $e(1)^2 - 2e(1) + 2e = e$.
      6. Evaluate at 1: $1(0)^2 - 2(0) + 2(1) = 2$.
      7. Volume = $e - 2$.

  - id: vol-cross-hq-9
    title: Triangular Region Semicircles
    type: symbolicResponse
    prompt: |
      The base of a solid is the triangle bounded by $y = 2 - x$, $y = x$, and the $y$-axis. Cross-sections perpendicular to the $x$-axis are semicircles. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: \pi/6
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. Intersection: $2 - x = x \implies 2x = 2 \implies x = 1$. The region spans from $x=0$ to $x=1$.
      2. Base width $d = (2-x) - x = 2 - 2x = 2(1-x)$.
      3. Area $A(x) = \frac{\pi}{8} d^2 = \frac{\pi}{8} [4(1-x)^2] = \frac{\pi}{2}(1-x)^2$.
      4. $V = \int_0^1 \frac{\pi}{2}(1-x)^2 \, dx = \frac{\pi}{2} [-\frac{1}{3}(1-x)^3]_0^1$.
      5. Evaluate: $\frac{\pi}{2}(0 - (-1/3)) = \frac{\pi}{6}$.

  - id: vol-cross-hq-10
    title: Tangent Squares
    type: symbolicResponse
    prompt: |
      The base of a solid is bounded by $y = \tan x$, $y = 0$, and $x = \pi/4$. Cross-sections perpendicular to the $x$-axis are squares. Find the exact volume.
    answer:
      gradingMode: auto
      expectedLatex: 1 - \pi/4
      equivalenceMode: expression
      tolerance: 0
    explanation: |
      1. Base width $s = \tan x$.
      2. $A(x) = \tan^2 x$.
      3. $V = \int_0^{\pi/4} \tan^2 x \, dx = \int_0^{\pi/4} (\sec^2 x - 1) \, dx$.
      4. Evaluate: $[\tan x - x]_0^{\pi/4} = (1 - \pi/4) - (0 - 0) = 1 - \pi/4$.
"""

create_yaml('calc2-volumes-cross-sections-easy-quiz.yaml', vol_easy_quiz)
create_yaml('calc2-volumes-cross-sections-hard-quiz.yaml', vol_hard_quiz)
print("Created Volumes Cross Sections Quizzes successfully.")

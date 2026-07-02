# Olympiad Geometry Reference

This document serves as the canonical reference base for generating Olympiad-level geometry assessments. It covers theorems and strategies primarily seen on the AMC 10/12, AIME, and USAMO.

## 1. Foundational Tools (AMC Level)
- **Similar Triangles**: The workhorse of competitive geometry. Recognizing similar triangles (AA, SAS, SSS) often breaks a problem wide open.
- **Area Formulas**: 
  - Standard: $K = \frac{1}{2}bh$
  - Trigonometric: $K = \frac{1}{2}ab \sin C$
  - Heron's Formula: $K = \sqrt{s(s-a)(s-b)(s-c)}$
  - Inradius/Circumradius: $K = rs = \frac{abc}{4R}$
- **Angle Chasing**: Utilizing parallel lines, isosceles triangles, and circle properties to track angle measures across a diagram.

## 2. Circle Geometry & Cyclic Quadrilaterals (AIME Level)
- **Power of a Point**: Essential for intersecting chords, secants, and tangents. If chords $AB$ and $CD$ intersect at $P$, then $PA \cdot PB = PC \cdot PD$.
- **Cyclic Quadrilaterals**: A quadrilateral is cyclic if and only if opposite angles sum to $180^\circ$. Allows transferring angles across chords.
- **Ptolemy's Theorem**: For a cyclic quadrilateral $ABCD$, $AB \cdot CD + AD \cdot BC = AC \cdot BD$.
- **Radical Axis**: The locus of points with equal power to two circles. The radical axes of three circles are concurrent at the radical center.

## 3. Advanced Configurations & Theorems (Olympiad Level)
- **Ceva's Theorem**: Determines concurrency of cevians based on side ratios.
- **Menelaus' Theorem**: Determines collinearity of points on the sides of a triangle.
- **Stewart's Theorem**: Relates the length of a cevian to the sides of the triangle: $man + dad = bmb + cnc$ (where $d$ is the cevian splitting side $a$ into $m$ and $n$).
- **Mass Point Geometry**: A technique for finding ratios of lengths along cevians by assigning "masses" to vertices.
- **Inversion**: A transformation that maps circles and lines to circles and lines, often simplifying problems involving multiple tangent circles.
- **Homothety & Spiral Similarity**: Transformations combining scaling and rotation, very powerful for proving points are concyclic or lines are concurrent.

## Common Problem Architectures
When authoring `workedExample` assessments, ensure the steps guide the learner to:
1. Draw a large, accurate diagram.
2. Identify obvious cyclic quadrilaterals or similar triangles.
3. Apply a structural theorem (e.g., Power of a Point) to translate geometric properties into algebraic equations.
4. Bash coordinates or use trigonometry only if synthetic methods stall.

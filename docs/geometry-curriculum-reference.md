# Geometry Curriculum Reference

This document serves as the master specification, scope map, and authoring guide for the Geometry curriculum.

## Scope Map

### Area: Geometry Foundations
- `geometry-foundations`: Basic points, lines, segments, rays, planes.
- `geometry-points-lines-angles`: Angle types, parallel lines, transversals.

### Area: Triangle Geometry
- `geometry-triangles-basics`: Classification, angle sum, exterior angle theorem.
- `geometry-triangle-congruence`: SSS, SAS, ASA, AAS, HL.
- `geometry-triangle-similarity`: AA, SAS, SSS similarity, scale factors.
- `geometry-right-triangles`: Pythagorean theorem, special right triangles (45-45-90, 30-60-90), geometric mean.
- `geometry-triangle-centers`: Centroid, circumcenter, incenter, orthocenter.
- `geometry-triangle-area`: $A = \frac{1}{2}bh$, Heron's, $A = \frac{1}{2}ab\sin C$.
- `geometry-oblique-triangles`: Law of Sines, Law of Cosines, Ambiguous Case.

### Area: Circle Geometry
- `geometry-circles-basics`: Radius, diameter, chord, secant, tangent, circumference, area.
- `geometry-circle-angles-arcs`: Central angles, inscribed angles, intercepted arcs.
- `geometry-circle-chords-secants-tangents`: Tangent/radius perpendicularity, equal chords.
- `geometry-circle-area-sectors-segments`: Sector area, arc length.
- `geometry-power-of-a-point`: Chord-chord, secant-secant, tangent-secant products.

### Area: Quadrilateral Geometry
- `geometry-quadrilaterals-basics`: Parallelogram, rectangle, rhombus, square, kite, trapezoid.
- `geometry-cyclic-quadrilaterals`: Opposite angles supplementary, Ptolemy's theorem.

### Area: Coordinate Geometry
- `geometry-coordinate-geometry`: Slope, distance, midpoint proofs.
- `geometry-circle-equations-coordinate`: Standard circle equation $(x-h)^2 + (y-k)^2 = r^2$.

### Area: Geometric Modeling
- `geometry-geometric-modeling`: Translating scenarios (ladders, shadows, ramps) into geometric models.

### Area: Physics Geometry Applications
- `geometry-physics-applications`: Vectors, force triangles, inclined planes, circular motion.

## Standard Terminology and Notation
- Use standard notation: $\triangle ABC$, $\overline{AB}$, $\angle ABC$.
- Use `$\text{m}\angle ABC$` for the *measure* of an angle.
- Use `$\cong$` for congruent figures or angles, and `=` for equal lengths or measures.
- Use `$\sim$` for similar figures.

## Common Problem Archetypes

### Right Triangles
- **Easy**: Find the hypotenuse given two legs. Identify ratio in 30-60-90.
- **Hard**: Ladder sliding down a wall. Altitude drawn to the hypotenuse (geometric mean theorem).

### Circles
- **Easy**: Find the area of a sector given central angle. Find inscribed angle given intercepted arc.
- **Hard**: Power of a point with an external secant and tangent.

## Authoring Guidelines

### Diagram Usage
- Heavily utilize SVG diagrams for concept lessons and worked examples.
- Diagram files should live in `frontend/public/assessments/geometry/`.
- Provide extremely descriptive `alt` text for all images so that text-only parsing still conveys the math.

### Assessment Pattern per Topic
1. `[topic]-concept-lesson`: Deep explanation with diagrams and embedded checks.
2. `[topic]-worked-example`: Step-by-step, correctness-gated.
3. `[topic]-recall`: Definitions, theorem statements, and formulas.
4. `[topic]-easy-quiz`: 10-15 direct application questions.
5. `[topic]-hard-quiz`: 10-15 complex application / multi-step questions.
6. `[topic]-modeling-test`: Test focused entirely on translating scenarios into geometry.

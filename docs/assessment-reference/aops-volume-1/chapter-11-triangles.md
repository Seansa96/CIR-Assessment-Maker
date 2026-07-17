# Chapter 11: Triangles, a.k.a. Geometry

## Scope

- Local instructional source: *The Art of Problem Solving, Volume 1: The Basics*, pdf 107-131; printed 93-117.
- AoPS topic: `aops-triangles`.
- Original local-textbook reference; it does not reproduce source exercises, diagrams, or solutions.

## Why triangles are the structural unit of geometry

Triangles are rigid: specifying enough corresponding side/angle information fixes their shape, unlike a general quadrilateral. They let a problem convert a diagram into equations about angles, lengths, ratios, and areas. Every polygon can be triangulated, and many circle and coordinate facts reduce to triangles. The central discipline is correspondence: a theorem is useful only when the named parts of the correct triangles match.

**Placeholder: generate separate original SVGs for (1) triangle centers with marked bisectors/medians/altitudes, (2) a right triangle with altitude to the hypotenuse, (3) congruent and similar triangle correspondence, and (4) a labelled triangle with an incircle and altitude. Diagrams must mark only stated equalities and parallelism.**

## Definitions and core theorems

The side lengths of a nondegenerate triangle obey the triangle inequality: each is less than the sum of the other two. Its interior angles sum to $180^\circ$; an exterior angle equals the sum of the two remote interior angles. In a right triangle, $a^2+b^2=c^2$, where $c$ is opposite the right angle. Conversely, if the longest side satisfies that equality the triangle is right; compare $c^2$ with $a^2+b^2$ to classify acute or obtuse triangles.

Congruence means same shape and same size. SSS, SAS, ASA/AAS, and hypotenuse-leg for right triangles are valid criteria; SSA is generally not. Similarity means equal corresponding angles and proportional corresponding sides. AA proves similarity; then one scale factor multiplies every length, perimeter, and altitude, while it squares for area.

The angle bisectors concur at the incenter, equidistant from sides; perpendicular bisectors concur at the circumcenter, equidistant from vertices; medians concur at the centroid in $2:1$ vertex-to-midpoint ratio; altitudes concur at the orthocenter. These are locus facts: e.g., a point equidistant from two sides lies on their angle bisector.

## Proof and calculation tools

One proof of Pythagoras rearranges four congruent right triangles in a square of side $a+b$: comparing the central square $c^2$ with the same total area expressed as $(a+b)^2-2ab$ yields $c^2=a^2+b^2$. Similar right triangles created by an altitude to a right-triangle hypotenuse yield the geometric-mean relations. Triangle area is $\tfrac12 bh$, $\tfrac12ab\sin C$, and $rs$, where $r$ is inradius and $s$ semiperimeter. The last follows by decomposing the triangle into three triangles of height $r$.

Trigonometry is ratio language in a right triangle: $\sin\theta=\text{opposite}/\text{hypotenuse}$, $\cos\theta=\text{adjacent}/\text{hypotenuse}$, and $\tan\theta=\text{opposite}/\text{adjacent}$. Similarity proves these depend only on the angle, not a chosen triangle.

## Selection and error checks

First classify the givens: angle-only suggests similarity; three lengths suggest Pythagoras or inequality; equal marks suggest isosceles/congruence; a center/locus clue suggests a triangle center. Write correspondence order explicitly. Check that a claimed length is positive and that candidate sides satisfy the triangle inequality. Never use a diagram’s apparent scale as a theorem.

## Bank blueprint

Required concepts: `triangle-inequality`, `pythagorean-converse`, `congruence`, `similarity-and-scale`, `triangle-centers`, `right-triangle-trigonometry`, `triangle-area`, and `triangle-proof-strategy`. The bank needs original diagram-based questions with SVG media paths for every configuration-dependent item; advanced prompts should include proof, construction, and mixed-theorem transfer.

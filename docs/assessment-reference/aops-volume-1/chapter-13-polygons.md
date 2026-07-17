# Chapter 13: Polygons

## Scope

- Local instructional source: *The Art of Problem Solving, Volume 1: The Basics*, pdf 141-146; printed 127-132.
- AoPS topic: `aops-polygons`.

## Definitions and global angle structure

A polygon is a simple closed planar figure formed from segments. An $n$-gon has $n$ sides, vertices, and interior angles. A convex polygon contains every segment joining two of its points; a concave polygon has an interior angle greater than $180^\circ$. The distinction matters: uncomplicated triangulation from one vertex works directly in convex polygons, while concave diagrams require care about which diagonals stay inside.

Drawing diagonals from one vertex of a convex $n$-gon creates $n-2$ triangles. Therefore the interior-angle sum is $(n-2)180^\circ$. Taking one exterior turn at each vertex completes exactly one revolution, so the directed exterior-angle sum is $360^\circ$ for every convex polygon. These are proofs, not formulas to memorize without a diagram.

For a regular $n$-gon, all sides and angles agree: each interior angle is $((n-2)180^\circ)/n$, each exterior/central angle is $360^\circ/n$. Regularity adds rotational symmetry and permits decomposition into $n$ congruent isosceles triangles from the center.

**Placeholder: generate SVGs for triangulation of a convex heptagon, directed exterior turns of a regular pentagon, and a regular polygon decomposed into central isosceles triangles with apothem.**

## Length, area, and symmetry

The number of diagonals is $n(n-3)/2$: each vertex joins to $n-3$ nonadjacent vertices, but every diagonal is counted twice. For a regular polygon with perimeter $P$ and apothem $a$, area is $\tfrac12aP$. The proof sums the $n$ center-based triangles, each with area $\tfrac12(\text{side})(a)$. This is the polygon analogue of the triangle inradius formula.

Regular polygon symmetry can establish equal chords, congruent triangles, and rotations. A regular hexagon is especially useful because central angles are $60^\circ$ and its six center triangles are equilateral. Do not transfer those facts to arbitrary hexagons.

## Method selection and errors

Choose interior sum for a total, exterior sum for a missing exterior or regular angle, and central decomposition for regular-polygon area/diagonal questions. State whether angles are interior or exterior. For diagonal counts, distinguish a segment from a vertex-to-vertex path. Never assume a polygon is regular because it looks symmetric.

## Bank blueprint

Required concepts: `polygon-classification`, `interior-angle-sum`, `exterior-angle-sum`, `regular-polygon-angles`, `polygon-diagonals`, `regular-polygon-area`, and `polygon-symmetry`. Advanced items should prove formulas, combine a polygon with circle geometry, or use a non-obvious symmetry; diagram-dependent prompts require SVG media.

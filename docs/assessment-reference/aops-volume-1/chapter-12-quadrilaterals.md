# Chapter 12: Quadrilaterals

## Scope

- Local instructional source: *The Art of Problem Solving, Volume 1: The Basics*, pdf 132-140; printed 118-126.
- AoPS topic: `aops-quadrilaterals`.
- Original instructional reference, not a reproduction of source content.

## Definitions, hierarchy, and proof burden

A quadrilateral has four sides and interior-angle sum $360^\circ$, proved by splitting it along a diagonal into two triangles. A parallelogram has both pairs of opposite sides parallel; its opposite sides and angles are equal, consecutive angles supplementary, and diagonals bisect each other. Conversely, any of several sufficient tests--both pairs of opposite sides equal, one pair opposite sides both parallel and equal, or diagonals bisecting each other--proves a quadrilateral is a parallelogram.

A rectangle is a parallelogram with a right angle; its diagonals are congruent. A rhombus is a parallelogram with four equal sides; its diagonals are perpendicular and bisect opposite angles. A square is both. The converse directions need separate evidence: equal diagonals alone do not prove a square, and perpendicular diagonals alone do not prove a rhombus.

A trapezoid has at least one designated pair of parallel bases under this curriculum’s convention. Its area is $\tfrac12(b_1+b_2)h$, derived by joining two congruent copies into a parallelogram. In an isosceles trapezoid, legs and each base-angle pair are equal; its diagonals are equal. The median segment parallel to bases has length $(b_1+b_2)/2$.

**Placeholder: generate SVGs for a generic parallelogram with diagonal, a rhombus with perpendicular bisecting diagonals, an isosceles trapezoid with altitudes, and a counterexample diagram showing why a converse fails.**

## Areas and diagonals

A parallelogram has area $bh$ because a triangular piece can be shifted to form a rectangle; it is also $ab\sin\theta$. A rhombus/kite with perpendicular diagonals has area $\tfrac12d_1d_2$: its four right triangles have combined area half the product. This formula requires perpendicular diagonals; without that condition, the general diagonal expression includes the sine of their angle.

## Strategy selection

Mark parallel sides, equal sides, and diagonal intersection facts before computing. Use a diagonal to expose congruent triangles, similarity, or triangle area. For classification problems, list the exact property required by the target rather than relying on a visual label. For area, distinguish side length from altitude and choose a base with known perpendicular distance.

## Bank blueprint

Required concepts: `quadrilateral-angle-sum`, `parallelogram-tests`, `rectangle-rhombus-square-properties`, `trapezoid-properties`, `quadrilateral-area`, `diagonal-reasoning`, and `quadrilateral-converses`. Include counterexample and proof items as advanced questions; all configuration-dependent questions require original SVG media.

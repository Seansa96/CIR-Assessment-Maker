# Chapter 9: An Introduction to Circles

## Source, scope, and authoring boundary

- Local instructional source: *The Art of Problem Solving, Volume 1: The Basics*, pdf 95-97; printed 81-83.
- AoPS topic: `aops-circles-introduction`.
- This chapter is original local-textbook content. It records concepts, proofs, and authoring guidance; it does not reproduce source exercises, worked solutions, or diagrams.

## Why circles matter

A circle packages a global condition--constant distance from one fixed point--into a shape with exceptional symmetry. A radius can turn in any direction without changing length. That rotational invariance explains why circumference and area depend on one scale, the radius, and why arcs, sectors, chords, and central angles can be measured consistently. In applied work circles model wheels, turning mechanisms, radial menus, circular buffers, coverage regions, and rotations; in geometry they create equal lengths and equal angles that are not obvious from a sketch.

**Placeholder: generate an SVG showing a circle with center $O$, two radii, a diameter, a chord, a minor arc, a sector, and a tangent at one endpoint. Mark exactly the relationships used below; the drawing must not imply unmarked equalities.**

## Formal definitions and invariants

A circle with center $O$ and radius $r>0$ is the set of points $P$ satisfying $OP=r$. A radius joins $O$ to a point on the circle. A chord joins two circle points; a diameter is a chord through $O$, so its length is $2r$. An arc is a portion of the circumference. A central angle has vertex at $O$ and intercepts an arc; its measure determines the same fraction of the full circle as its degree measure divided by $360^\circ$ (or radian measure divided by $2\pi$). A sector is bounded by two radii and an arc. A tangent touches the circle at one point; its crucial theorem is that it is perpendicular to the radius at that point.

The circumference is $C=2\pi r$ and area is $A=\pi r^2$. These should be treated as scale laws: enlarging a circle by factor $k$ multiplies $C$ by $k$ and $A$ by $k^2$. A fractional arc and sector preserve those fractions:

$$
L_{\text{arc}}=\frac{\theta}{360^\circ}(2\pi r),\qquad
A_{\text{sector}}=\frac{\theta}{360^\circ}(\pi r^2).
$$

For radians, $L=r\theta$ and $A_{\text{sector}}=\tfrac12r^2\theta$; these are not new formulas but the same proportional statements after one full turn is $2\pi$ radians.

## Derivations worth teaching

The constant $\pi$ is defined as $C/d$ for every circle; similarity makes the quotient independent of circle size. Therefore $C=\pi(2r)$. A sector can be decomposed into many thin triangles with height approximately $r$ and bases summing to the arc length. Their total area approaches $\tfrac12rL$; for the whole circle $L=2\pi r$, giving $A=\pi r^2$. This limiting argument explains both the circle-area formula and the radian sector formula. It is a conceptual derivation, not permission to treat a curved boundary as exactly polygonal at a finite stage.

For the tangent-radius theorem, assume a tangent line through $T$ were not perpendicular to $OT$. The perpendicular from $O$ to that line would meet it at another point closer to $O$ than $T$, placing a second point of the line inside the circle. A line through an interior point must cross the circle twice, contradicting tangency. Thus $OT$ is perpendicular to the tangent.

## Strategy selection and failure modes

First identify whether the target is length, area, or an angle; length uses a linear scale, area a squared scale. Then mark the center explicitly and ask whether a given segment is a radius, chord, diameter, or tangent. Use a fractional-circle relationship only when the angle is central or the corresponding arc is explicitly established. Do not infer that a chord is a diameter because it looks long, or that a radius bisects a chord without the missing perpendicular/bisector condition. Keep degree and radian units separate.

## Authoring and assessment blueprint

Foundational items should classify circle objects, compute radius/diameter/circumference/area, and trace sector fractions. Intermediate items should compare scaled circles, infer an arc from a central angle, and use tangent perpendicularity. Advanced items should combine a circle with a triangle, derive a maximum-area argument, prove a tangent fact, or reconcile degree and radian representations. Every diagram-dependent prompt must receive an original SVG under `frontend/public/assessments/aops/`, with alt text describing the marked givens rather than the conclusion.

Required bank concepts: `circle-definitions`, `circumference-and-area`, `arcs-and-sectors`, `circle-similarity-and-scaling`, `tangents-and-radius`, and `circle-proof-strategy`.

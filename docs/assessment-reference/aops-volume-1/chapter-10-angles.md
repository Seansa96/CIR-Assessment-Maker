# Chapter 10: Angles

## Source, scope, and authoring boundary

- Local instructional source: *The Art of Problem Solving, Volume 1: The Basics*, pdf 98-106; printed 84-92.
- AoPS topic: `aops-angles`.
- This is original local-textbook material; it does not reproduce source problem statements, diagrams, or solutions.

## Why angle reasoning is a system

An angle chase is not visual guessing. It is a network of additive constraints caused by straight lines, full turns, parallel lines, triangles, and circles. The purpose of formal names--vertical, supplementary, corresponding, alternate interior, central, inscribed, tangent-chord--is to state which constraint is licensed and which information is still missing. This makes a solution robust when a diagram is deliberately not to scale.

**Placeholder: generate an SVG with two marked parallel lines and a transversal; label one angle and show corresponding, alternate-interior, and same-side-interior positions. A separate SVG is required for central, inscribed, exterior-secant, and tangent-chord angle cases.**

## Definitions and base relations

A segment has two endpoints; a ray has one endpoint and extends indefinitely; a line extends indefinitely both ways. Angle measure in degrees assigns one full turn $360^\circ$; in radians it assigns one full turn $2\pi$. Vertical angles are equal. A linear pair sums to $180^\circ$. Angles around a point sum to $360^\circ$.

If a transversal intersects parallel lines, corresponding angles are equal, alternate interior angles are equal, and same-side interior angles are supplementary. Conversely, any of these relationships can prove the two lines parallel, but the proof must identify the correct pair and a genuine transversal.

For circles: a central angle equals its intercepted arc; an inscribed angle equals half its intercepted arc; an angle formed by two chords inside a circle equals half the sum of intercepted arcs; two secants outside equal half the difference of the far and near intercepted arcs; a tangent-chord angle equals half its intercepted arc. Each theorem has a different vertex location, which is the key recognition cue.

## Proof structure

The exterior-angle theorem follows from triangle sum and a linear pair: if remote interior angles are $A,B$ and adjacent interior angle is $C$, then $A+B+C=180^\circ$ and $C+E=180^\circ$, so $E=A+B$. The inscribed-angle theorem can be reduced to isosceles triangles formed by radii; splitting into cases according to the center’s position avoids assuming a preferred diagram. A diameter subtends a right angle because its intercepted arc is $180^\circ$, so any inscribed angle intercepting it is half that.

## Method selection and safeguards

Record known measures, then propagate only through named equal/supplementary/sum relations. Look for a triangle, a straight line, a full turn, a pair of parallel lines, or a circle configuration. At every circle-angle step name the vertex: center, circle, inside, or outside. Never transfer a conclusion from a converse unless its hypotheses have been established. Angle values may be negative or exceed $180^\circ$ in directed-angle work, but elementary diagram problems normally state the intended range.

## Authoring and assessment blueprint

The bank must cover conversion, line and triangle sums, parallel-line converses, and all circle-angle cases. Intermediate prompts should mix two or three relations and require a reason ledger. Advanced prompts should involve an auxiliary construction, prove a cyclic angle relation, or distinguish two apparently similar circle configurations. Each geometry question whose information depends on placement requires an original SVG and exact alt text. Required bank concepts: `angle-measure`, `parallel-line-angles`, `triangle-exterior-angles`, `circle-angle-theorems`, `angle-chasing`, and `geometry-proof-obligations`.

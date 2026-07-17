# Chapter 14: Angle Chasing

## Scope

- Local instructional source: *The Art of Problem Solving, Volume 1: The Basics*, pdf 147-149; printed 133-135.
- AoPS topic: `aops-angle-chasing`.

## Purpose: controlled information propagation

Angle chasing is the practice of turning local facts into a verified chain of equalities and sums. It is not a separate theorem list: it combines the angle rules of lines, triangles, parallel lines, circles, isosceles figures, and regular polygons. A successful chase maintains a reason ledger: every new label has a source, and the target is reached without assuming visual scale.

**Placeholder: generate original SVGs for a multi-step chase involving parallel lines, an isosceles triangle, and a cyclic quadrilateral. Each label must correspond to a stated given or a derivable relation; diagrams must be intentionally non-scale-dependent.**

## Core moves and proof discipline

Start by marking givens and translating each into a relation: vertical angles equal, linear pairs sum to $180^\circ$, triangle interiors sum to $180^\circ$, and angles around a point sum to $360^\circ$. Add higher-level moves only when their hypotheses are visible: equal sides give isosceles base angles; parallel lines plus a transversal give corresponding/alternate relations; a cyclic quadrilateral gives opposite angles supplementary; an inscribed angle is half its intercepted arc.

Auxiliary lines are justified when they create a useful object: draw a diagonal to create triangles, a radius to invoke isosceles triangles, a line through a parallel direction to move an angle, or a circle only after establishing concyclicity. The proof obligation is twofold: state why the construction is permitted and identify the theorem it unlocks.

## Strategy and error prevention

Work from known labels toward the target, but also work backward: ask what sum or equality would determine the target. Avoid filling a diagram with unlabeled calculations. When two angles look equal, seek a named mechanism; a diagram is evidence of incidence only if explicitly marked. Check the final value against feasibility: interior triangle angles must be positive and sum correctly; an exterior/circle relation must use the correct vertex location.

## Bank blueprint

Required concepts: `angle-chasing-ledger`, `parallel-line-transfer`, `isosceles-triangle-angles`, `cyclic-angle-relations`, `auxiliary-line-selection`, `diagram-assumption-check`, and `geometry-proof-strategy`. Foundational questions trace one relation; intermediate questions combine three; advanced questions require selecting a construction, proving a relation, or identifying why a plausible chase is invalid. Every diagram-dependent item requires original SVG media and meaningful alt text.

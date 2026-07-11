# Computer Arithmetic Algorithms Archetype Map

Source reference: user-provided *Hacker's Delight, 2nd Edition* PDF.

Use rule: use this map for topic coverage and misconception targets only. Do not copy code, exercises, or prose verbatim.

## Areas and Topics
- `caa-machine-integers-bit-models`: Integer representation, word size, signedness, masks, shifts, and two's-complement intuition. Topic IDs: caa-integer-representation.
- `caa-bit-manipulation-fundamentals`: Rightmost-bit tricks, setting, clearing, toggling, extracting, Boolean identities, and branchless patterns. Topic IDs: caa-bitwise-fundamentals.
- `caa-power-two-and-alignment`: Detecting powers of two, rounding to boundaries, alignment, and boundary crossing. Topic IDs: caa-power-two-alignment.
- `caa-overflow-bounds-safe-arithmetic`: Overflow detection, saturating arithmetic, arithmetic bounds, average without overflow, and multiword operations. Topic IDs: caa-overflow-safe-arithmetic.
- `caa-popcounts-bit-scans`: Popcount, parity, leading zeros, trailing zeros, and first or last set-bit location. Topic IDs: caa-popcount-bit-scans.
- `caa-word-searching-packed-data`: Zero-byte detection, byte-wise masks, packed comparisons, and bit-run searches. Topic IDs: caa-packed-word-search.
- `caa-bit-permutations-rearrangement`: Bit/byte reversal, shuffling, compress/extract, expand/insert, and bit matrix transpose. Topic IDs: caa-bit-permutations.
- `caa-multiplication-division`: Multiword multiplication, multiplication by constants, division algorithms, division by constants, and magic-number intuition. Topic IDs: caa-integer-multiply-divide.
- `caa-integer-elementary-functions-area`: Integer square roots, logarithms, exponentiation, and refinement methods. Topic IDs: caa-integer-elementary-functions.
- `caa-encodings-checksums-error-correction`: Gray code, CRC concepts, Hamming codes, and SEC-DED intuition. Topic IDs: caa-encodings-error-correction.
- `caa-floating-point-approximation-area`: IEEE layout, conversion intuition, bitwise comparison, and approximation capstones. Topic IDs: caa-floating-point-approximation.

## Current Coverage
Each topic now has a first-pass Concept Lesson, Recall Drill, Worked Example, and Easy Quiz. The first-pass assessments are intentionally focused on mental models, small fixed-width examples, edge cases, and explanation rather than copying the book's dense algorithm catalog.

The category currently includes:
- 11 Concept Lessons
- 11 Recall Drills
- 12 Worked Examples
- 12 Easy Quizzes
- 11 Hard Quizzes

Extra Worked Example coverage exists for the rightmost-bit identities because those patterns are the gateway to many later topics.

## Future Expansion Notes
- Add code questions for `isPowerOfTwo`, `popcount`, `clearRightmostSetBit`, and `roundUpPowerOfTwo` after learner-facing conceptual coverage is stable.
- Add guided projects only when the project runner can support low-level files and deterministic fixed-width test cases smoothly.
- Expand the multiplication/division, CRC, error-correction, and floating-point topics with deeper examples once the learner has the earlier bit-model material in place.

# C++ Files, Strings, and Formatting

## Purpose and scope

This reference supports the `cpp-files-strings` curriculum area. It is the
authoring source for assessments about:

- `cpp-working-with-files`: stream state, text and binary I/O, paths, buffering,
  error handling, and safe update strategies;
- `cpp-strings-formatting`: `std::string`, character processing, tokenization,
  searching, transformations, parsing, and formatted output.

The companion question bank contains the supplied string-programming and
file-I/O sets. Repetitive prompt variants are consolidated into one stronger
item per distinct operation. Each item has a precise function contract,
representative cases, a sample C++ solution, and a teaching explanation so it
can be adapted into a code question, worked example, quiz trace, or test
scenario without inventing its answer during generation.

## String representation and invariants

`std::string` owns a contiguous sequence of `char` values. Its `size()` is the
number of stored code units, not necessarily the number of user-perceived
characters. Indexing is constant time, but insertion or erasure in the middle
can move every later character. Algorithms should state whether they are
ASCII-only, byte-oriented, or Unicode-aware. The current exercises explicitly
use ASCII unless a prompt says otherwise.

When passing a string that is not modified, prefer `std::string_view` for a
non-owning view or `const std::string&` when a stable string object is useful.
Return an owning `std::string` when the result must outlive the input. An
in-place algorithm may accept `std::string&` and document that mutation.

Character classification functions from `<cctype>` accept either `EOF` or a
value representable as `unsigned char`. Passing a negative signed `char` has
undefined behavior. Use a conversion such as:

```cpp
const auto u = static_cast<unsigned char>(ch);
if (std::isalpha(u)) {
    // ...
}
```

Likewise, convert the result of `std::toupper` or `std::tolower` back to `char`.

## Core string strategies

### One-pass scan

Counting, filtering, case conversion, delimiter insertion, and stateful
validation usually need one left-to-right pass. State should represent only
what the next character needs: a count, the previous digit, whether the next
letter should be uppercase, or the current run length. A one-pass solution is
normally `O(n)` time.

### Two pointers

Reversing a string or only selected characters uses indices that move inward.
For “reverse only vowels,” advance the left pointer until it reaches a vowel,
advance the right pointer until it reaches a vowel, swap, and repeat. The
invariant is that everything outside the two pointers is already final.

### Frequency table or set

For ASCII data, `std::array<int, 256>` gives predictable fixed storage and
constant-time lookup. `std::unordered_map<char, int>` makes the intent clear
when the alphabet is not fixed. `std::unordered_set<char>` is suitable for
membership or uniqueness. State whether case and whitespace count, because
those choices change the answer.

### Stack and dynamic programming

Nested delimiters require last-opened, first-closed behavior, so a stack is the
natural representation. Generating balanced parentheses uses backtracking with
two counts: opens used and closes used. A valid prefix never has more closes
than opens.

Longest-valid-parentheses and longest-palindromic-substring problems require
more than simple counting. A stack of unmatched positions, interval expansion,
or dynamic programming preserves positional information that a frequency table
cannot.

### Tokenization

Whitespace-separated words can be read with `std::istringstream`. If exact
spacing or punctuation must be preserved, scan the original string and operate
on word intervals instead. The prompt must define what counts as a word and
whether punctuation belongs to it.

## File I/O foundations

Use `std::ifstream` for input, `std::ofstream` for output, and `std::fstream`
when both are required. Opening a stream is an operation that can fail; check
the stream before using it. `std::getline` reads a full line, while formatted
extraction with `operator>>` skips leading whitespace and reads a token.

Stream state matters:

- `good()` means no state flag is set;
- `eof()` means an extraction attempted to read past the end;
- `fail()` covers format failures and other recoverable extraction failures;
- `bad()` signals a serious I/O failure.

Do not write `while (!stream.eof())`. Attempt the read in the loop condition:

```cpp
std::string line;
while (std::getline(input, line)) {
    // process a line that was actually read
}
```

For filesystem paths, prefer `std::filesystem::path`. Text mode can translate
line endings; binary mode preserves bytes. Random access uses `seekg`/`tellg`
for the get position and `seekp`/`tellp` for the put position. Updating a file
safely often means writing a temporary file, flushing and closing it, and then
renaming it over the destination rather than editing the original in place.

## Formatting foundations

Modern C++ offers `std::format` where the standard library implementation
supports it. Stream formatting remains important for portability and stateful
output:

- `std::setw` applies only to the next field;
- `std::setfill` persists;
- `std::fixed` and `std::scientific` select floating-point notation;
- `std::setprecision` means digits after the decimal in fixed notation but
  significant digits in default notation;
- `std::left`, `std::right`, `std::hex`, `std::dec`, `std::showbase`, and
  `std::boolalpha` change persistent stream flags.

Save and restore formatting state in reusable output functions so callers do
not inherit surprising flags. Locale-aware thousands separators are distinct
from manually inserting commas into a decimal digit string.

## Complexity and selection guidance

Prefer standard algorithms such as `std::reverse`, `std::sort`,
`std::transform`, `std::count_if`, and `std::ranges` operations when they
express the whole operation clearly. Hand-written loops are appropriate when
the exercise teaches an invariant, combines several conditions in one pass, or
must preserve exact delimiters.

Repeated concatenation can be linear overall when appending to a reserved
`std::string`, but repeated insertion at the front is quadratic. Reserve a
known upper bound or append to an output buffer. For large files, stream data
incrementally rather than reading the entire file unless the algorithm truly
requires random access to all content.

## Assessment authoring rules

1. Keep each generated assessment assigned to exactly one topic.
2. Preserve the bank item ID in generated provenance.
3. State ASCII-only assumptions directly; do not imply byte algorithms are
   Unicode-correct.
4. A code assessment must expose the exact function signature and edge cases.
5. Worked examples should explain the invariant and trace at least one
   nontrivial case, not merely display the final program.
6. Multiple-choice adaptations should ask learners to predict behavior,
   identify a bug, select an invariant, or compare complexity.
7. Distractors should represent realistic errors: signed-`char` misuse,
   out-of-range indexing, failure to preserve spacing, wrong tie rules, or
   confusing a substring with a subsequence.

# C++ Advanced Types, Casting & Vectors: Agent Implementation Plan

## Overview

Add two new assessments to the `c++-types-and-variables` topic that extend the existing
[`cpp-types-variables-concept-lesson.yaml`](file:///c:/Users/SeanS/Downloads/cir_app_antigravity/data/assessments/cpp-types-variables-concept-lesson.yaml):

1. **`cpp-advanced-types-casting-concept-lesson`** — A concept lesson covering `unsigned` types,
   `struct`, `enum`/`enum class`, `std::vector<T>` as a typed container, and explicit type casting
   (`static_cast`, implicit narrowing, integer division trap).

2. **`cpp-grade-calculator-directed-project`** — A small directed project (~20 min) that reads a
   list of numeric grades from the user into a `std::vector<double>`, computes the average with a
   `static_cast` required to avoid integer-division error, and prints a letter-grade summary.

---

## Source Contract

| Field | Value |
|---|---|
| Source ID | `src-20260720055310-28e9c62cfc` |
| Title | *Introducing C++: The Easy Way To Start Learning Modern C++* |
| License | Reuse terms not recorded — write **original** instructional content grounded in the concepts; do not copy prose verbatim |
| Status | `draft` (use for grounding only) |
| Chunk count | 431 |

**Authorized chunks for the concept lesson:**

| Chunk ID | Content summary |
|---|---|
| `chunk-0102` | `std::vector` basics; `push_back`; range-based `for` loop |
| `chunk-0103` | Adding/inserting elements; iterators and begin/end |
| `chunk-0105` | Indexing via `[]`; moving through elements |
| `chunk-0107` | `std::vector<double>`; reading into a vector with `push_back`; `while` + `has_value` pattern |
| `chunk-0108` | Narrowing conversion; `int` vs `double` in vector; compiler warning for narrowing |
| `chunk-0112` | `{}` vs `()` distinction; `std::vector` with initializer list |
| `chunk-0113` | `static_cast` to convert `int` to `double`; summary of sequential containers |

> [!IMPORTANT]
> The existing source is `draft` status. Do not copy prose. Write entirely original instructional text
> that is *grounded in* the concepts from those chunks.

---

## File 1 — Concept Lesson

**Output path:** `data/assessments/cpp-advanced-types-casting-concept-lesson.yaml`

> [!WARNING]
> This is a **new** file. Do not modify any existing file.

### Assessment Header

```yaml
schemaVersion: 1
id: cpp-advanced-types-casting-concept-lesson
title: 'C++ Advanced Types, Casting, and Vectors'
assessmentType: conceptLesson
categoryId: c++
topicId: c++-types-and-variables
navigation:
  learningGoal: learn
  activityType: conceptLesson
  tags:
    - c++
    - c++-types-and-variables
    - cpp
    - types
    - casting
    - vector
skills:
  - Apply Types, Variables, and I/O in C++
  - cpp-advanced-types-casting
  - c++-types-and-variables
```

### Required Sections (7 total)

Each section must follow the same structure as the existing concept lesson (see `cpp-types-variables-concept-lesson.yaml` for the exact YAML shape), with a `content`, optional `media`, and a **`check`** question.

---

#### Section 1 — `unsigned` and Sized Integer Types (`s-atc-01`)

**Content must cover:**
- `unsigned int`: stores only non-negative values; doubles the positive range but wraps around at 0
  (underflow) — e.g. `unsigned int x = 0; x--; // wraps to 4294967295`
- `long long` vs `long` vs `int`: guaranteed minimum sizes (`int` ≥ 16 bits, `long long` ≥ 64 bits)
- `size_t`: the unsigned type returned by `sizeof()` and `.size()` — always use it when storing sizes
  and counts returned by the standard library
- Rule of thumb: prefer `int` for general-purpose signed arithmetic; switch to `long long` when values
  exceed ~2 billion; use `unsigned` only when the domain is genuinely non-negative and wrap-around behavior
  is acceptable

**Check question (multipleChoice):** A variable will hold the number of bytes in a file, which can
exceed 4 billion. Which type should you use? (`long long` ✓, `int`, `unsigned int`, `short`)

---

#### Section 2 — Grouping Related Data with `struct` (`s-atc-02`)

**Content must cover:**
- A `struct` groups named, typed fields into one value:
  ```cpp
  struct Student {
      std::string name;
      int age;
      double gpa;
  };
  Student s{"Alice", 20, 3.8};
  std::cout << s.name << ": " << s.gpa << "\n";
  ```
- Accessing members with `.`
- A struct is a *value type*: assigning one struct to another copies all fields
- When to use a `struct` vs separate variables: whenever fields logically belong together as one entity

**Check question (multipleChoice):** After `Student a = s;`, you set `a.gpa = 4.0`. What is `s.gpa`?
(`3.8` still ✓, `4.0` — confusion about copy vs reference, `undefined behavior`, `compile error`)

Distractor `b` signal: `struct-copy-confusion`

---

#### Section 3 — Scoped Enumerations with `enum class` (`s-atc-03`)

**Content must cover:**
- A plain `enum` leaks its enumerators into the enclosing scope and implicitly converts to `int` — this is
  a well-known source of bugs
- `enum class` (scoped enum) fixes both: enumerators must be qualified (`Color::Red`) and there is no
  implicit integer conversion
  ```cpp
  enum class Direction { North, South, East, West };
  Direction d = Direction::North;
  // int n = d; // Error: no implicit conversion
  ```
- When to use `enum class`: any time you have a fixed set of named states or categories (direction, weekday,
  status code, etc.)
- Casting back to `int` explicitly with `static_cast<int>(d)` when the underlying value is needed

**Check question (selectAll):** Which statements are true about `enum class`?
- (a) Enumerators must be qualified with the enum name ✓
- (b) An `enum class` value implicitly converts to `int` ✗ — `enum-class-implicit-int-confusion`
- (c) `enum class` prevents name collisions in the enclosing scope ✓
- (d) `enum class` values can be used in a `switch` statement ✓

---

#### Section 4 — `std::vector<T>`: A Typed, Resizable Sequence (`s-atc-04`)

**Content must cover:**
- Include: `#include <vector>`
- Declaration: `std::vector<double> scores;` — type parameter `T` specifies what the vector holds
- Adding elements: `scores.push_back(92.5);` appends to the end
- Size: `scores.size()` returns `size_t` — the current element count
- Indexed access: `scores[i]` (no bounds check) vs `scores.at(i)` (throws `std::out_of_range`)
- Range-based for loop:
  ```cpp
  for (double score : scores) {
      std::cout << score << "\n";
  }
  ```
- Why prefer `std::vector` over raw arrays for most tasks: automatic resizing, standard library
  compatibility, and safer interfaces

**Check question (multipleChoice):** `std::vector<int> v = {10, 20, 30}; v.push_back(40);`. What
does `v.size()` return? (`4` ✓, `3` — push_back-ignored confusion, `40` — value-not-size confusion,
`1` — only-last-element confusion)

---

#### Section 5 — Implicit Narrowing Conversion (`s-atc-05`)

**Content must cover:**
- C++ *implicitly* converts between numeric types when they are compatible, but a narrowing conversion
  silently loses information:
  ```cpp
  double d = 9.99;
  int i = d;   // i == 9; the fractional part is truncated, not rounded
  ```
- Braced initialization `{}` prevents narrowing at compile time:
  ```cpp
  int i{9.99};  // Error: narrowing conversion
  ```
- Integer division: `7 / 2` evaluates to `3` because both operands are `int`. The result type is
  determined by the operands, not by the variable that receives the result.
- The narrowing trap in vector initializers (from chunk-0108): `std::vector<int> v{1, 2.5};` is a
  compile error because `2.5` narrows to `int`

**Check question (multipleChoice):** What is the value of `result` after `int result = 9 / 2;`?
(`4` ✓, `4.5`, `5` — rounding confusion, `9` — division-ignored confusion)

Distractor signals: `floating-point-division-assumed`, `integer-rounding-confusion`

---

#### Section 6 — Explicit Type Casting with `static_cast` (`s-atc-06`)

**Content must cover:**
- `static_cast<TargetType>(expression)`: the C++ way to convert types explicitly and safely at compile time
- Fixing integer division: cast one operand to `double` *before* the division:
  ```cpp
  int total = 45, count = 10;
  double avg = static_cast<double>(total) / count;  // 4.5
  // NOT: static_cast<double>(total / count)        // still 4.0
  ```
- The position of the cast matters: casting the *result* of integer division gives 4.0, not 4.5
- Converting `int` ↔ `double`: casting to `int` truncates (does not round)
- When to use `static_cast` vs leaving an implicit conversion:
  - Use it whenever you intend to lose information or change the calculation path
  - It also serves as documentation of intent

**Check question (multipleChoice):**

```cpp
int a = 7, b = 3;
double result = static_cast<double>(a / b);
```

What is `result`? (`2.0` ✓ — integer division happens first, `2.333...` — cast-position confusion,
`3.0` — rounding confusion, `7.0` — numerator confusion)

> [!IMPORTANT]
> This is the **core misconception** that the directed project will test. Make the distractor
> `2.333...` carry `issueSignal: cast-position-error` and explain clearly in `Why the other choices fail:`
> that casting the *result* of integer division is too late — the truncation already happened.

---

#### Section 7 — Choosing the Right Type (`s-atc-07`)

**Content must cover:**
- A decision table to close the lesson:

  | Situation | Recommended type |
  |---|---|
  | General integer arithmetic | `int` |
  | Integer that may exceed ~2 billion | `long long` |
  | Non-negative count or size | `size_t` |
  | Decimal / fractional values | `double` |
  | Single character | `char` |
  | True/false flag | `bool` |
  | Fixed set of named states | `enum class` |
  | Group of related named fields | `struct` |
  | Resizable typed sequence | `std::vector<T>` |

- Remind learners: **always initialize** (`int x{};` not `int x;`) and **always prefer `static_cast`**
  over C-style casts `(int)x`

**Check question (selectAll):** Which of these are good reasons to use `static_cast` instead of a
C-style cast `(int)x`?
- (a) `static_cast` fails at compile time if the conversion is not valid ✓
- (b) `static_cast` is faster at runtime ✗ — no runtime difference
- (c) `static_cast` makes the conversion intent visible in the code ✓
- (d) `static_cast` is checked by the compiler for type compatibility ✓

---

## File 2 — Directed Project

**Output path:** `data/assessments/cpp-grade-calculator-directed-project.yaml`

> [!WARNING]
> This is a **new** file. Model its structure exactly after
> [`cpp-type-explorer-directed-project.yaml`](file:///c:/Users/SeanS/Downloads/cir_app_antigravity/data/assessments/cpp-type-explorer-directed-project.yaml).

### Assessment Header

```yaml
schemaVersion: 1
id: cpp-grade-calculator-directed-project
title: 'Grade Average Calculator'
assessmentType: directedProject
categoryId: c++
topicId: c++-types-and-variables
navigation:
  learningGoal: practice
  activityType: directedProject
  tags:
    - c++
    - c++-types-and-variables
    - cpp
    - vector
    - static_cast
    - type-casting
    - directedproject
skills:
  - Apply Types, Variables, and I/O in C++
  - cpp-advanced-types-casting
  - c++-types-and-variables
```

### Summary and Estimate

```yaml
directedProject:
  summary: >-
    Build a command-line grade calculator. You will collect numeric grades
    into a std::vector<double>, compute an average using static_cast to
    avoid the integer-division trap, and display a letter-grade result.
  estimatedTimeMinutes: 20
```

### Required Phases and Steps

---

#### Phase 1 — `phase-setup` — Project Setup and Data Collection

**Step 1 (`step-declare-vector`):** Create a new project `GradeCalculator.cpp`. Declare a
`std::vector<double> grades;` and a loop that reads doubles from the user until they type `-1` (sentinel).
Use `while (std::cin >> input && input >= 0)` and `grades.push_back(input)`.

*Checklist:*
- `[ ]` Declared `std::vector<double> grades`
- `[ ]` Loop correctly reads grades until -1 is entered
- `[ ]` Each valid grade is appended with `push_back`

*Notes prompt:* "How many elements did `grades.size()` report after entering 5 grades?"

---

#### Phase 2 — `phase-calculate` — Computing the Average with Casting

**Step 2 (`step-sum-and-cast`):** After the loop, compute the sum by iterating over the vector with a
range-based for loop. Then compute the average:

```cpp
double sum = 0.0;
for (double g : grades) {
    sum += g;
}
double average = sum / static_cast<double>(grades.size());
```

Instruct the student to try **without** the cast first — `sum / grades.size()` — and explain why it can
still give a wrong result (`.size()` returns `size_t`, which is unsigned; dividing `double` by `size_t`
*does* work, but it is clearer and safer to cast explicitly, and the pattern carries over to `int / int`
cases where casting is mandatory).

*Checklist:*
- `[ ]` Computed `sum` with a range-based for loop over the vector
- `[ ]` Used `static_cast<double>(grades.size())` in the average calculation
- `[ ]` Printed the average with at least one decimal place using `std::fixed` and `std::setprecision(1)`

*Notes prompt:* "What would the average be if you forgot the cast and both operands were `int`? Try
computing `int total = 45; int count = 10; std::cout << total / count;` to see."

---

#### Phase 3 — `phase-letter-grade` — Letter Grade and Output

**Step 3 (`step-letter-grade`):** Write a series of `if`/`else if` conditions to assign a `char` letter
grade variable based on the computed average:

| Average | Letter |
|---|---|
| >= 90.0 | 'A' |
| >= 80.0 | 'B' |
| >= 70.0 | 'C' |
| >= 60.0 | 'D' |
| < 60.0 | 'F' |

Print a formatted summary:

```
Grades entered: 5
Average: 87.4
Letter grade: B
```

**Step 4 (`step-edge-case`):** Handle the edge case where no grades were entered (vector is empty).
Guard the average computation with `if (!grades.empty())` before dividing to avoid dividing by zero.
Print a message like `"No grades entered."` if the vector is empty.

*Checklist:*
- `[ ]` `char` variable used to store letter grade
- `[ ]` Correct `if`/`else if` thresholds (90/80/70/60)
- `[ ]` Final output shows count, average, and letter grade
- `[ ]` Empty-vector edge case handled before computing average

*Notes prompt:* "Why is it important to use `double` comparisons for the thresholds instead of `int`?
What would happen if `average` were exactly `80.0` and you compared it to `80`?"

---

## Authoring Quality Checklist

- `[ ]` All section `check` explanations use exactly `Solution:`, `Why it works:`, and
  `Why the other choices fail:` headings
- `[ ]` No generic distractor text (e.g., "This conflicts with the definition"). Every distractor bullet
  names a specific misconception (e.g., "Choice b assumes `static_cast` is checked at runtime, but it is
  a compile-time construct with no runtime overhead.")
- `[ ]` `issueSignals` attached to all incorrect `selectAll` choices
- `[ ]` All code in `content` fields uses fenced code blocks with `cpp` language tag
- `[ ]` No double-quoted YAML strings containing backslashes; use block scalars (`|` or `>`) for any
  multi-line code or explanation content

---

## Validation Commands

After authoring both files, run:

```powershell
python scripts/validate_s2c_content.py data/assessments/cpp-advanced-types-casting-concept-lesson.yaml
python scripts/validate_s2c_content.py data/assessments/cpp-grade-calculator-directed-project.yaml

dotnet test backend\QuizApp.sln --no-restore
```

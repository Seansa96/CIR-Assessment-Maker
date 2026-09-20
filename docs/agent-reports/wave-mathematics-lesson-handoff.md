# Wave Equation Concept Lesson: Agent Handoff Plan

## Purpose

Draft a new **S2C-compliant, source-grounded** concept lesson for the `physics-wave-mechanics` topic that
replaces weak existing coverage with a complete, calculus-based treatment of the linear wave equation. This
document provides a GPT agent all context needed to author the file without accessing the live application
or the source PDFs.

---

## Source Contract (Extraction Gate)

Before drafting any content, note that the source has **already been imported and approved**.

| Field | Value |
|---|---|
| Source ID | `src-20260720001005-93652b69c4` |
| Title | OpenStax University Physics, Volume 1 |
| License | **CC BY 4.0** — original instruction may be freely composed from concepts in this source |
| Status | `approved` |
| Chunk count | 1696 |
| Extractor | `pypdf-v1` |

**Authorized source chunks for this lesson** (all from `src-20260720001005-93652b69c4`):

| Chunk ID | Content summary |
|---|---|
| `chunk-1374` | Electromagnetic vs mechanical waves; wave overview |
| `chunk-1375` | Period, frequency, crest, trough; seagull transverse wave model |
| `chunk-1377` | Wavelength, amplitude, equilibrium; propagation velocity |
| `chunk-1378` | Transverse vs longitudinal waves |
| `chunk-1384` | Pulse definition; constant-shape propagation |
| `chunk-1385` | Snapshot graphs; sinusoidal wave on string |
| `chunk-1386` | Constructing $y = A\sin(kx)$; motivation for wave number $k$ |
| `chunk-1387` | Full sinusoidal form $y = A\sin(kx - \omega t + \phi)$; phase |
| `chunk-1388` | Example 16.3: reading $A$, $k$, $\omega$, $\lambda$, $T$, $v$ from a wave function |
| `chunk-1389` | Deriving $\lambda$ from $k$; period from $\omega$; speed direction from sign |
| `chunk-1390` | History graphs; measuring period |
| `chunk-1391` | First partial derivatives; transverse velocity and acceleration |
| `chunk-1392` | **The Linear Wave Equation** — second partial derivatives; $\partial^2 y/\partial x^2 = (1/v^2)\partial^2 y/\partial t^2$ |
| `chunk-1393` | Superposition; sum of two wave functions also a solution |

> [!IMPORTANT]
> Do NOT copy text verbatim from any chunk. Write original instructional prose that is grounded in the
> concepts from those chunks. The S2C contract (`skills/source-to-curriculum/SKILL.md`) forbids verbatim
> source extraction in assessment YAML.

---

## Curriculum Manifest

A manifest file must exist at:
```
docs/assessment-reference/curriculum-manifests/physics-wave-mathematics-s2c.yaml
```

It should declare:
```yaml
schemaVersion: 1
sourceId: src-20260720001005-93652b69c4
categoryId: physics-1
areaId: physics-waves
topics:
  - id: physics-wave-mechanics
    objectives:
      - phys-wave-pde-derivation
      - phys-wave-sinusoidal-form
      - phys-wave-partial-derivatives
      - phys-wave-parameter-reading
      - phys-wave-phase-shifts
      - phys-wave-sine-cosine-quadrature
      - phys-wave-boundary-conditions
      - phys-wave-general-form
    sourceChunks:
      - src-20260720001005-93652b69c4:chunk-1374
      - src-20260720001005-93652b69c4:chunk-1375
      - src-20260720001005-93652b69c4:chunk-1377
      - src-20260720001005-93652b69c4:chunk-1378
      - src-20260720001005-93652b69c4:chunk-1384
      - src-20260720001005-93652b69c4:chunk-1385
      - src-20260720001005-93652b69c4:chunk-1386
      - src-20260720001005-93652b69c4:chunk-1387
      - src-20260720001005-93652b69c4:chunk-1388
      - src-20260720001005-93652b69c4:chunk-1389
      - src-20260720001005-93652b69c4:chunk-1390
      - src-20260720001005-93652b69c4:chunk-1391
      - src-20260720001005-93652b69c4:chunk-1392
      - src-20260720001005-93652b69c4:chunk-1393
requiredActivities:
  focusedTopic: [conceptLesson, recallDrill, guidedWorkedExample]
```

---

## Output File

Write the new concept lesson to:
```
data/assessments/wave-mathematics-concept-lesson.yaml
```

> [!WARNING]
> This file **already exists** and contains weak content. **Overwrite it** entirely. Do not merge with the
> old content.

---

## Target Assessment Contract

```yaml
schemaVersion: 1
id: wave-mathematics-concept-lesson
title: 'Mathematics of Waves: Complete Calculus Treatment'
assessmentType: conceptLesson
categoryId: physics-1
topicId: physics-wave-mechanics
navigation:
  learningGoal: learn
  activityType: conceptLesson
  tags:
    - physics-1
    - physics-traveling-waves
    - openstax-vol1
```

---

## Required Sections (10 total)

Write a `lesson.sections[]` array with exactly the following ten sections, in order. Each section must have:
- a unique `id` (e.g. `s-wm-01`)
- a meaningful `title`
- a `content` block scalar (YAML `|` or `>-`) that is **substantive prose** (≥ 4 sentences)
- an inline `check` with a **specific, context-sensitive** multiple-choice question (not a generic "which statement is correct" template)

### Section 1 — Physical Setup and Wave Types (`s-wm-01`)
*Ground truth from `chunk-1374`, `chunk-1375`, `chunk-1377`, `chunk-1378`.*

Cover:
- Mechanical vs electromagnetic waves; transverse vs longitudinal distinction.
- Define the medium, disturbance, and equilibrium position.
- Define $A$ (amplitude), $\lambda$ (wavelength), $T$ (period), $f$ (frequency), and propagation velocity $v$.
- State $v = f\lambda$ with units.

**Check question**: Give a concrete scenario (e.g. a seagull bobbing on water waves) and ask what the frequency is, given period $T$.

---

### Section 2 — Snapshot and History Graphs (`s-wm-02`)
*Ground truth from `chunk-1384`, `chunk-1385`, `chunk-1390`.*

Cover:
- A *snapshot graph* plots $y$ vs $x$ at a fixed time. One full repetition = $\lambda$.
- A *history graph* plots $y$ vs $t$ at a fixed position. One full repetition = $T$.
- Reading $A$ and $\lambda$ from a snapshot, and $A$ and $T$ from a history graph.
- The wave moves the pattern rightward by $v \Delta t$ after time $\Delta t$ — this is the key link between the two graphs.

**Check question**: A snapshot shows two peaks separated by 0.40 m. A history graph at one point shows period 0.25 s. Calculate the wave speed $v$.

---

### Section 3 — Constructing the Wave Number $k$ (`s-wm-03`)
*Ground truth from `chunk-1386`.*

Cover:
- A complete spatial cycle spans $2\pi$ radians and a distance $\lambda$, so $k = 2\pi/\lambda$ (units: rad/m).
- Analogously, $\omega = 2\pi/T = 2\pi f$ (units: rad/s).
- The instantaneous displacement of any point is $y(x) = A\sin(kx)$ at $t=0$ for a rightward wave.
- Show the dimensional consistency of $kx$ being dimensionless (rad).

**Check question**: A wave has wavelength 0.30 m. Compute $k$ to three significant figures.

---

### Section 4 — The Full Sinusoidal Wave Function (`s-wm-04`)
*Ground truth from `chunk-1387`.*

Cover:
- For a wave moving in the $+x$ direction: $y(x, t) = A\sin(kx - \omega t + \phi)$.
- For a wave moving in the $-x$ direction: $y(x, t) = A\sin(kx + \omega t + \phi)$.
- The *phase* of the wave is $\Phi = kx - \omega t + \phi$; the *initial phase* $\phi$ accounts for the wave's state at $(x=0, t=0)$.
- Cosine form: $y = A\cos(kx - \omega t)$ is equivalent to the sine form with $\phi = \pi/2$ — this is the *quadrature* relationship. One can always convert using $\cos\theta = \sin(\theta + \pi/2)$.
- Why the sign of $\omega t$ determines direction: a constant phase $kx - \omega t = C$ implies $x = (C + \omega t)/k$, so $x$ increases with $t$ (rightward propagation).

**Check question**: A wave is described by $y = 0.05\sin(8\pi x + 6\pi t)$ (SI units). In which direction does it travel, and what is its speed?

---

### Section 5 — Reading Parameters from a Wave Function (`s-wm-05`)
*Ground truth from `chunk-1388`, `chunk-1389`.*

Cover the complete **parameter-reading workflow**:

| Parameter | Symbol | Read from function | Units |
|---|---|---|---|
| Amplitude | $A$ | coefficient of sine/cosine | m |
| Wave number | $k$ | coefficient of $x$ | rad/m |
| Angular frequency | $\omega$ | coefficient of $t$ | rad/s |
| Wavelength | $\lambda = 2\pi/k$ | derived | m |
| Period | $T = 2\pi/\omega$ | derived | s |
| Frequency | $f = \omega/(2\pi)$ | derived | Hz |
| Wave speed | $v = \omega/k$ | derived | m/s |
| Initial phase | $\phi$ | constant offset | rad |

Walk through an explicit worked example (different numbers from OpenStax's Example 16.3 to avoid copying) — e.g., $y(x,t) = 0.12\sin(4.0x - 24t + \pi/6)$ — and extract all eight parameters with units.

**Check question**: Given $y = 0.08\cos(5x - 20t)$, what is the wavelength?

---

### Section 6 — First Partial Derivatives: Transverse Velocity and Acceleration (`s-wm-06`)
*Ground truth from `chunk-1391`.*

Cover:
- The *transverse velocity* of a particle in the medium: $v_y = \partial y/\partial t = -A\omega\cos(kx - \omega t + \phi)$. Note the cosine — it is $\pi/2$ out of phase with the displacement (another appearance of the quadrature relationship).
- The *transverse acceleration*: $a_y = \partial v_y/\partial t = \partial^2 y/\partial t^2 = -A\omega^2\sin(kx - \omega t + \phi) = -\omega^2 y$. This is SHM.
- Emphasize: the wave speed $v$ (propagation) and the transverse velocity $v_y$ are fundamentally different quantities.
- Maximum transverse speed is $A\omega$; maximum transverse acceleration is $A\omega^2$.

**Check question**: For the wave $y = 0.10\sin(2x - 4t)$ (SI), write the expression for transverse velocity and find its maximum magnitude.

---

### Section 7 — Second Partial Derivatives and the Wave Equation (`s-wm-07`)
*Ground truth from `chunk-1392`.*

Cover:
- Take $\partial^2 y/\partial x^2 = -k^2 A\sin(kx - \omega t + \phi) = -k^2 y$.
- Take $\partial^2 y/\partial t^2 = -\omega^2 A\sin(kx - \omega t + \phi) = -\omega^2 y$.
- Dividing: $\frac{\partial^2 y}{\partial x^2} = \frac{k^2}{\omega^2}\frac{\partial^2 y}{\partial t^2} = \frac{1}{v^2}\frac{\partial^2 y}{\partial t^2}$ — the **linear wave equation**.
- State clearly: **any** function of the form $f(x \pm vt)$ satisfies this PDE, not just sinusoids. The sinusoidal solution is the special case for periodic waves.

**Check question**: Show that $y = B(x - 3t)^2$ satisfies the wave equation $\partial^2 y/\partial x^2 = (1/v^2)\partial^2 y/\partial t^2$. What is $v$?

---

### Section 8 — General Traveling-Wave Form and Constant-Phase Argument (`s-wm-08`)

Cover:
- Formal argument: if $y = f(x - vt)$, then by chain rule $\partial y/\partial x = f'$ and $\partial y/\partial t = -vf'$; second derivatives give $\partial^2 y/\partial x^2 = f''$ and $\partial^2 y/\partial t^2 = v^2 f''$, so the PDE is satisfied identically.
- The *constant-phase* derivation of wave speed: hold $kx - \omega t = C$, differentiate with respect to $t$: $k(dx/dt) - \omega = 0 \Rightarrow v = dx/dt = \omega/k$.
- A *cosine* wave vs a *sine* wave: these are identical modulo a phase offset. The choice between them corresponds to initial conditions: $\phi = 0$ gives $y(0,0) = 0$ (sine); $\phi = \pi/2$ gives $y(0,0) = A$ (cosine). Neither is "more fundamental."

**Check question**: A wave travels in the $-x$ direction with speed 3 m/s. Its displacement at $(x=0, t=0)$ is zero and initially increasing. Write the wave function $y(x,t)$ using $A = 0.05$ m, $f = 6$ Hz.

---

### Section 9 — Spatial, Temporal, and Phase Shifts (`s-wm-09`)

Cover:
- A *spatial shift* $x_0$ replaces $x$ with $x - x_0$, shifting the wave pattern rightward by $x_0$.
- A *temporal shift* $t_0$ replaces $t$ with $t - t_0$, effectively starting the wave later in time.
- General initial phase $\phi$ encodes both: $\phi = kx_0 - \omega t_0$ for a wave that was at position $x_0$ at time $t_0$.
- Boundary condition example: a string is driven at $x = 0$ with $y(0,t) = A\sin(\omega t)$. The solution propagating rightward is $y(x,t) = A\sin(\omega t - kx) = A\sin(-(kx - \omega t))$. Note this equals $-A\sin(kx - \omega t)$, which is valid with $\phi = \pi$.

**Check question**: A wave is $y = 0.04\sin(3x - 12t + \pi/4)$. At what position $x$ does the displacement equal $A$ at $t = 0$?

---

### Section 10 — Verification Workflow and Physical Interpretation (`s-wm-10`)
*Ground truth from `chunk-1392`, `chunk-1393`.*

Teach the four-step verification procedure students should apply to any wave function:
1. **Dimensional check**: confirm $kx$ and $\omega t$ are dimensionless, $A$ has displacement units.
2. **Substitution check**: compute $\partial^2 y/\partial x^2$ and $\partial^2 y/\partial t^2$ and verify the PDE holds.
3. **Parameter extraction**: read $A$, $k$, $\omega$, $\lambda$, $T$, $f$, $v$ and confirm they are physically reasonable.
4. **Initial/boundary condition check**: evaluate $y(0,0)$, $v_y(0,0)$ and confirm they match the stated starting conditions.

Cover superposition briefly: the linearity of the PDE means any linear combination $Ay_1 + By_2$ also satisfies the wave equation — this is what permits interference and Fourier synthesis.

**Check question** (selectAll): Which of the following are required checks when verifying that a proposed function $y(x,t)$ is a valid solution to the wave equation? (a) Verify dimensional consistency of $kx$ and $\omega t$. (b) Substitute into $\partial^2 y/\partial x^2 = (1/v^2)\partial^2 y/\partial t^2$ and confirm equality. (c) Check that $y$ is sinusoidal — non-sinusoidal functions cannot satisfy the wave equation. (d) Confirm that $A$, $\lambda$, and $T$ have physically reasonable values.

*(Correct: a, b, d. Distractor c captures the common misconception that only sinusoids satisfy the wave PDE.)*

---

## S2C Authoring Requirements Checklist

Every section `check` and any standalone questions added in related assessments **must** satisfy:

- `[ ]` Each `multipleChoice` check has exactly 4 choices: one correct, three plausible-but-wrong distractors.
- `[ ]` Each distractor names a **specific, prompt-specific misconception** — never reuse generic distractors like "No motion" or "A constant displacement" across questions.
- `[ ]` The `explanation` field for each check uses **exactly** the headings:
  - `Solution:` (step-by-step reasoning)
  - `Why it works:` (physical or mathematical insight)
  - `Why the other choices fail:` (one bullet per distractor, naming the specific error)
- `[ ]` `selectAll` checks include `issueSignals` on each wrong choice.
- `[ ]` No YAML double-quoted strings contain unescaped LaTeX backslashes. Use block scalars (`|` or `>-`) or single-quoted strings for any LaTeX.
- `[ ]` All inline math uses `$...$`; all display math uses `$$...$$`. No `\(...\)` or `\[...\]`.

---

## Related Files to Repair (Separate Task)

The following **existing** files contain generic boilerplate explanations ("This follows from the sinusoidal traveling-wave equation.") that also need rewriting to full S2C quality, but leave them for a follow-up task:

- `traveling-waves-concept-lesson.yaml` — all 8 section checks use identical distractor set `[No motion, A constant displacement, A standing-only pattern]`
- `wave-mathematics-worked-example.yaml` — explanations lack structured `Solution:` / `Why it works:` headings

---

## Validation Commands

After writing the file, run both of the following and fix any reported violations before declaring the task complete:

```powershell
python scripts/validate_s2c_content.py data/assessments/wave-mathematics-concept-lesson.yaml

dotnet test backend\QuizApp.sln --no-restore
```

Also run the LaTeX delimiter scan to catch any legacy `\(...\)` or `\[...\]` that slipped through:
```powershell
rg -n '\\\\(|\\\\)|\\\\[|\\\\]' data/assessments/wave-mathematics-concept-lesson.yaml
```

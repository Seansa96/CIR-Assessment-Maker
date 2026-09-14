# Young & Freedman University Physics — Chapter 26 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry corresponds exactly to a selected Chapter 26 prompt. Refer to the companion note for circuit diagrams.

# Problem 26.1

## Key concept

Resistance is proportional to wire length; the two semicircles between opposite points are parallel branches.

## Worked solution

1. Each straight segment has resistance $R/3$.
2. The circle uses one third of the original wire, so each semicircle has resistance $(R/3)/2=R/6$.
3. The two semicircles are in parallel:
$$
R_{\rm circle}=(R/6)\parallel(R/6)=R/12.
$$
4. Add the two straight series segments:
$$
R_{ab}=R/3+R/12+R/3=3R/4.
$$

## Why it works

Current must pass through the straight pieces but has two identical paths around the circle between the connection points.

## Issue signals

- `wire-length-resistance-scaling-error`
- `parallel-resistance-reduction-error`

# Problem 26.3

## Key concept

The original power identifies the battery voltage, and series resistors share one current.

## Worked solution

1. From the original resistor, use $P_1=V^2/R_1$ to find battery voltage:
$$
V=\sqrt{P_1R_1}.
$$
2. With the second resistor in series, calculate $R_{\rm eq}=R_1+R_2$.
3. Find total dissipation:
$$
P_{\rm total}=\frac{V^2}{R_{\rm eq}}.
$$

## Why it works

Adding series resistance reduces current at fixed battery voltage, so total power differs from simply adding the original resistor powers.

## Issue signals

- `power-resistance-voltage-formula-error`
- `series-current-condition-missed`

# Problem 26.5

## Key concept

Equivalent resistance is found by identifying series and parallel paths, using symmetry or Kirchhoff rules when simple reduction is not possible.

## Worked solution

1. Label the terminals and all junctions in the triangular array shown in the figure.
2. Identify any pairs of resistors that are in true series (their shared node has no other connection) or true parallel (same two endpoints).
3. Reduce those groups step by step; if no direct reduction remains, use nodal potentials or Kirchhoff's junction and loop rules.
4. Compute $R_{\rm eq}=V_{\rm test}/I_{\rm test}$ for a chosen test voltage.

## Why it works

Series and parallel formulas are valid only when the circuit connectivity meets their definitions; Kirchhoff’s laws handle the remaining network structure.

## Issue signals

- `resistors-misidentified-as-series`
- `resistors-misidentified-as-parallel`

# Problem 26.7

## Key concept

An ammeter reads the branch current that flows through it; internal battery resistance is in series with the external equivalent resistance.

## Worked solution

1. Reduce the external resistor network shown in the figure to an equivalent resistance $R_{\rm ext}$.
2. Add battery internal resistance: $R_{\rm total}=r+R_{\rm ext}$.
3. Calculate total current $I=\mathcal{E}/R_{\rm total}$.
4. If the ammeter lies in a branch after a split, use current division or a node equation to obtain its branch current.

## Why it works

The internal resistance reduces the terminal voltage under load, and Kirchhoff’s junction rule distributes current among parallel branches.

## Issue signals

- `internal-resistance-omitted`
- `ammeter-branch-current-confused-with-total-current`

# Problem 26.9

## Key concept

In a series circuit, all resistors carry identical current and voltage drops add to the battery terminal voltage.

## Worked solution

1. Use the three values from Exercise 26.8 and calculate $R_{\rm eq}=R_1+R_2+R_3$.
2. Include any specified battery internal resistance in the total series resistance.
3. Compute $I=\mathcal{E}/R_{\rm total}$.
4. Find each resistor's voltage drop $V_i=IR_i$ and power $P_i=I^2R_i$ to answer the repeated parts.

## Why it works

There is only one conducting path, so the same charge per second crosses every resistor.

## Issue signals

- `series-resistance-sum-error`
- `series-current-not-equal-error`

# Problem 26.45

## Key concept

In an RC charging circuit, the instantaneous resistor voltage is $IR$ and capacitor voltage is $\mathcal E-IR$.

## Worked solution

1. At the stated instant, calculate the resistor drop $V_R=IR$.
2. Apply Kirchhoff’s loop rule:
$$
V_C=\mathcal E-V_R=\mathcal E-IR.
$$
3. Use capacitor relation $Q=CV_C$.
4. Report the magnitude of charge on either plate.

## Why it works

The source voltage is split between the resistor and capacitor at every moment during charging; increasing capacitor charge reduces current.

## Issue signals

- `rc-loop-voltage-sign-error`
- `capacitor-charge-voltage-ratio-error`

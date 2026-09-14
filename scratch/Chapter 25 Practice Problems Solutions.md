# Young & Freedman University Physics — Chapter 25 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading matches exactly one selected Chapter 25 prompt.

# Problem 25.1

## Key concept

Current is charge per time: $I=\Delta Q/\Delta t$.

## Worked solution

1. Record the lightning current and duration from the prompt.
2. Calculate transferred charge:
$$
\Delta Q=I\Delta t.
$$
3. Divide by elementary charge if the number of electrons is requested:
$$
N=\frac{|\Delta Q|}{e}.
$$

## Why it works

Electric current measures the rate at which charge crosses a chosen surface, regardless of the microscopic source of the current.

## Issue signals

- `current-charge-time-ratio-error`
- `elementary-charge-factor-error`

# Problem 25.3

## Key concept

Use $I=Ne/t$, $J=I/A$, and $v_d=J/(ne)$ for charge flow, current density, and electron drift speed.

## Worked solution

1. Electron flow rate is $N/t=I/e$.
2. Convert the wire diameter to radius and calculate $A=\pi(d/2)^2$.
3. Calculate $J=I/A$.
4. Calculate drift speed $v_d=I/(neA)$.
5. If diameter doubles, electron rate stays fixed at fixed current, while area quadruples; $J$ and $v_d$ become one-fourth as large.

## Why it works

The same total current can be carried through a larger cross section with lower current density and slower average carrier drift.

## Issue signals

- `diameter-used-as-radius`
- `drift-velocity-area-dependence-error`

# Problem 25.5

## Key concept

Electron drift speed is $v_d=I/(neA)$, so travel time through length $L$ is $t=L/v_d$.

## Worked solution

1. Compute the cross-sectional area of the 12-gauge wire.
2. Use $v_d=I/(neA)$ and then $t=L/v_d$.
3. Repeat with the 6-gauge diameter and same $L$, $I$, and carrier density.
4. State the general scaling: for fixed current, $v_d\propto1/A\propto1/d^2$.

## Why it works

A thicker wire contains more mobile charge carriers per unit length, so each carrier’s average drift speed can be lower for the same current.

## Issue signals

- `drift-velocity-area-dependence-error`
- `wire-diameter-squared-scaling-error`

# Problem 25.7

## Key concept

For time-varying current, transferred charge is $\Delta Q=\int I(t)\,dt$.

## Worked solution

1. Use the supplied current function and the stated beginning and ending times.
2. Evaluate
$$
\Delta Q=\int_{t_i}^{t_f}I(t)\,dt.
$$
3. The constant current that transfers the same charge is
$$
I_{\rm avg}=\frac{\Delta Q}{t_f-t_i}.
$$

## Why it works

Current is the derivative of charge with respect to time, so integrating current recovers the accumulated charge.

## Issue signals

- `current-time-integral-error`
- `average-current-definition-error`

# Problem 25.9

## Key concept

Current from entering ions is $I=\Delta Q/\Delta t=Nq/\Delta t$.

## Worked solution

1. Use the stated number of ions per meter and the charge of one ion.
2. Multiply to find total charge entering one meter of axon: $\Delta Q=Nq$.
3. Convert $10\ \text{ms}$ to seconds.
4. Calculate $I=\Delta Q/\Delta t$ and give sign/direction if requested.

## Why it works

The axon current is simply the rate at which the ionic charge crosses the cell membrane.

## Issue signals

- `millisecond-unit-conversion-error`
- `ion-charge-multiplication-error`

# Problem 25.21

## Key concept

Resistance of a uniform material is $R=\rho L/A$.

## Worked solution

1. The path length between opposite cube faces is $L=1.80\ \text{m}$.
2. The cross-sectional area perpendicular to current is $A=(1.80\ \text{m})^2$.
3. Use aluminum resistivity from the table in $R=\rho L/A$.

## Why it works

Resistance increases with the path length that carriers travel and decreases with the cross-sectional area available for their flow.

## Issue signals

- `resistance-length-area-ratio-error`
- `cube-cross-sectional-area-error`

# Young & Freedman University Physics — Chapter 20 Practice Problems Solutions

> [!note] Worked-solution companion
> Entries correspond exactly to selected Chapter 20 problems. Use the companion note for original cycle diagrams.

# Problem 20.1

## Key concept

For one heat-engine cycle, energy conservation gives $Q_H=W+Q_C$ and efficiency is $e=W/Q_H$.

## Worked solution

1. Treat the discarded heat magnitude as $Q_C=4300\ \text{J}$.
2. Calculate input heat:
$$
Q_H=2200\ \text{J}+4300\ \text{J}.
$$
3. Calculate $e=2200\ \text{J}/Q_H$ and express as a percentage.

## Why it works

Because the engine returns to its initial state each cycle, its net internal-energy change is zero, so incoming heat becomes work plus rejected heat.

## Issue signals

- `engine-energy-balance-sign-error`
- `thermal-efficiency-denominator-error`

# Problem 20.3

## Key concept

Engine efficiency, rejected heat, fuel mass, and power all follow from input heat per cycle.

## Worked solution

1. Compute $e=W/Q_H$ from the supplied input heat and $3700\ \text{J}$ work.
2. Find rejected heat $Q_C=Q_H-W$.
3. Use fuel mass $m=Q_H/q_{\rm combustion}$, with consistent energy-per-mass units.
4. Multiply work per cycle by $60.0\ \text{cycles/s}$ for power; convert watts to kilowatts and horsepower.

## Why it works

The chemical energy of the fuel supplies the engine's input heat; each identical cycle repeats the same work and heat partition.

## Issue signals

- `thermal-efficiency-denominator-error`
- `power-cycle-rate-conversion-error`

# Problem 20.5

## Key concept

Net work of a heat-engine cycle is the signed area inside its pV loop, and heat on each leg follows from $Q=\Delta U+W$.

## Worked solution

1. Read each state’s pressure and volume from the figure and use $pV=nRT$ to determine temperatures.
2. For the curved path marked $Q/T=0$, set $Q=0$ and use the given $\gamma$ relation for the adiabatic leg.
3. Calculate work for each path: $W=p\Delta V$ for constant-pressure segments and use $W=-\Delta U$ for the adiabatic segment.
4. Add the leg works to get $W_{\rm net}$; add only positive heat transfers for $Q_H$, then calculate $e=W_{\rm net}/Q_H$.

## Why it works

The first law applies to each part of the cycle, while the enclosed pV area gives total work because the system returns to its initial state.

## Issue signals

- `pV-cycle-work-sign-error`
- `adiabatic-heat-transfer-not-zero`

# Problem 20.7

## Key concept

The ideal Otto-cycle efficiency is $e=1-1/r^{\gamma-1}$.

## Worked solution

1. Insert the supplied air value of $\gamma$ and compression ratio $r=8.8$:
$$
e_1=1-\frac1{8.8^{\gamma-1}}.
$$
2. Repeat with $r=9.6$.
3. Subtract $e_1$ from $e_2$ to find the efficiency increase, reporting percentage points if appropriate.

## Why it works

Greater compression raises the temperature swing over which the ideal cycle operates, increasing the fraction of input heat convertible to work.

## Issue signals

- `otto-efficiency-exponent-error`
- `percent-vs-percentage-point-error`

# Problem 20.9

## Key concept

For a refrigerator, coefficient of performance is $K=Q_C/W$, and $Q_H=Q_C+W$.

## Worked solution

1. Rearrange $K=Q_C/W$ to $W=Q_C/K$.
2. Add the required work to the extracted cold-reservoir heat:
$$
Q_H=Q_C+W.
$$
3. Report both quantities per cycle.

## Why it works

The motor’s work is added to the heat removed from the cold space, so the high-temperature reservoir receives both.

## Issue signals

- `cop-ratio-inverted`
- `refrigerator-energy-balance-sign-error`

# Problem 20.39

## Key concept

Heat transfer between internal body temperature and the cooler surface changes entropy by $\Delta S=Q/T_{\rm surface}-Q/T_{\rm body}$.

## Worked solution

1. Convert food energy to joules:
$$
Q=(2.50\ \text{g})(9.3\ \text{Cal/g})(4186\ \text{J/Cal})(0.80).
$$
2. Convert $37^\circ\text{C}$ and $30^\circ\text{C}$ to kelvins.
3. Calculate $\Delta S=Q(1/T_s-1/T_b)$.
4. State the positive sign: the transfer to the cooler surface increases total entropy.

## Why it works

Moving a fixed amount of heat from a warmer region to a cooler region creates a larger entropy increase at the lower temperature than the decrease at the higher temperature.

## Issue signals

- `food-calorie-joule-conversion-error`
- `entropy-temperature-kelvin-error`

# Problem 20.53

## Key concept

Carnot efficiency depends only on the endpoint reservoir temperatures: $e=1-T_C/T_H$.

## Worked solution

1. For the first Carnot engine, write $Q_I=Q_H(T_I/T_H)$.
2. The second engine receives $Q_I$ and rejects $Q_C=Q_I(T_C/T_I)$.
3. Substitute to show $Q_C=Q_H(T_C/T_H)$.
4. Thus composite efficiency is
$$
e_{\rm composite}=1-\frac{Q_C}{Q_H}=1-\frac{T_C}{T_H},
$$
identical to the original Carnot engine.

## Why it works

Reversible Carnot stages can be cascaded without changing the total entropy transfer between the same two endpoint reservoirs.

## Issue signals

- `carnot-temperature-ratio-error`
- `intermediate-reservoir-double-counting`

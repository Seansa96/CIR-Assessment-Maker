# Young & Freedman University Physics — Chapter 24 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading corresponds exactly to a selected Chapter 24 prompt.

# Problem 24.1

## Key concept

For a vacuum parallel-plate capacitor, $\Delta V=Ed$, $C=Q/\Delta V$, and $C=\epsilon_0A/d$.

## Worked solution

1. Convert $2.50\ \text{mm}$ to meters and compute $\Delta V=Ed$.
2. Calculate $C=Q/\Delta V$ using $Q=80.0\ \text{nC}$.
3. Rearrange $C=\epsilon_0A/d$ to obtain $A=Cd/\epsilon_0$.
4. Cross-check by using $E=\sigma/\epsilon_0=Q/(\epsilon_0A)$.

## Why it works

Between sufficiently large oppositely charged plates, the field is nearly uniform and the capacitor’s geometry determines both field and capacitance.

## Issue signals

- `parallel-plate-capacitance-formula-error`
- `millimeter-or-nanocoulomb-unit-error`

# Problem 24.3

## Key concept

The relations $Q=C\Delta V$, $C=\epsilon_0A/d$, $E=\Delta V/d$, and $\sigma=Q/A$ describe an air parallel-plate capacitor.

## Worked solution

1. Find potential difference from $\Delta V=Q/C$.
2. Solve $A=Cd/\epsilon_0$ after converting the gap to meters.
3. Calculate field magnitude $E=\Delta V/d$.
4. Calculate the plate surface-charge magnitude $\sigma=Q/A$.

## Why it works

All four quantities are connected by the same uniform-field capacitor model, so calculating one pair provides the rest.

## Issue signals

- `charge-voltage-capacitance-ratio-error`
- `parallel-plate-capacitance-formula-error`

# Problem 24.5

## Key concept

With a battery connected, voltage remains constant; parallel-plate capacitance scales as $C=\epsilon_0A/d$.

## Worked solution

1. Calculate the original capacitance $C=\epsilon_0\pi R^2/d$ and charge $Q=CV$.
2. If separation doubles, capacitance halves, so at fixed battery voltage $Q$ halves.
3. If plate radius doubles, area becomes four times larger, so capacitance and fixed-voltage charge both become four times larger.

## Why it works

The battery transfers charge as needed to maintain its terminal voltage while a geometry change alters the capacitance.

## Issue signals

- `battery-connected-voltage-not-fixed`
- `area-radius-scaling-error`

# Problem 24.7

## Key concept

Use the parallel-plate expression $C=\epsilon_0A/d$ and compare plate separation with penny diameter to assess the infinite-sheet approximation.

## Worked solution

1. Obtain the area of a penny from its diameter: $A=\pi R^2$.
2. Rearrange $d=\epsilon_0A/C$ using the required capacitance.
3. Compare $d$ with the penny radius or diameter.
4. The infinite-sheet approximation is justified only when the separation is much smaller than the lateral plate dimensions.

## Why it works

Fringing fields are negligible near the central region only for plates that are large compared with their separation.

## Issue signals

- `penny-area-geometry-error`
- `infinite-sheet-approximation-criterion-error`

# Problem 24.9

## Key concept

For a specified stored charge and voltage, first find $C=Q/V$; then use $d=\epsilon_0A/C$.

## Worked solution

1. Convert $240.0\ \text{pC}$ to coulombs.
2. Calculate $C=Q/(42.0\ \text{V})$.
3. Use $d=\epsilon_0A/C$ to find the original separation.
4. If separation doubles, capacitance halves; maintaining the same $Q$ requires twice the potential difference because $V=Q/C$.

## Why it works

At fixed plate area, increasing separation reduces capacitance, so a larger voltage is required to place the same charge on the plates.

## Issue signals

- `picocoulomb-unit-conversion-error`
- `fixed-charge-vs-fixed-voltage-condition-confused`

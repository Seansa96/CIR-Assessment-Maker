# Young & Freedman University Physics — Chapter 28 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading matches exactly one selected Chapter 28 prompt. Refer to the companion question note for all diagrams.

# Problem 28.1

## Key concept

The nonrelativistic magnetic field of a moving point charge is
$$
\vec B=\frac{\mu_0}{4\pi}\frac{q\,\vec v\times\hat r}{r^2}.
$$

## Worked solution

1. Form the displacement vector from the instantaneous charge position to the specified observation point.
2. Calculate its magnitude $r$ and unit vector $\hat r$.
3. Evaluate the cross product $\vec v\times\hat r$.
4. Multiply by $\mu_0q/(4\pi r^2)$, retaining the charge sign.

## Why it works

Only a moving charge produces this magnetic field, and the field direction is perpendicular to both the charge velocity and the line toward the observation point.

## Issue signals

- `moving-charge-biot-savart-cross-product-error`
- `charge-sign-field-direction-error`

# Problem 28.3

## Key concept

The moving electron’s field magnitude is $B=\mu_0|q|v\sin\theta/(4\pi r^2)$.

## Worked solution

1. For each labeled point, use the figure to determine the angle between $\vec v$ and $\vec r$.
2. Points on the velocity line have $\sin\theta=0$, hence zero magnetic field.
3. For perpendicular locations, insert $\sin\theta=1$ and the stated distance.
4. Use the right-hand rule for a positive charge, then reverse direction for the electron.

## Why it works

The cross product in the moving-charge field vanishes exactly along the charge’s line of motion and is largest in the transverse plane.

## Issue signals

- `moving-charge-field-angle-error`
- `electron-field-direction-error`

# Problem 28.5

## Key concept

Apply the moving point-charge field equation separately at each Cartesian observation point.

## Worked solution

1. For each point, calculate $\vec r=\vec r_{\rm point}-\vec r_q$.
2. Evaluate $\vec v\times\hat r$ and identify directions that give zero because $\vec r\parallel\vec v$.
3. Use $B=\mu_0|q|v\sin\theta/(4\pi r^2)$ for the magnitude.
4. Convert each vector result to $\hat\imath$, $\hat\jmath$, and $\hat k$ notation.

## Why it works

The instantaneous field is determined by the point charge’s velocity and the observer’s relative position at that instant.

## Issue signals

- `moving-charge-biot-savart-cross-product-error`
- `observation-position-vector-error`

# Problem 28.7

## Key concept

Magnetic fields from moving charges superpose, and force on a moving charge is $\vec F=q\vec v\times\vec B$.

## Worked solution

1. For each of the three stated relative speed/charge cases, use the figure’s geometry to calculate each moving charge’s field at $P$.
2. Reverse the lower charge’s field direction because that charge is negative.
3. Add the signed field vectors for the net $\vec B$ at $P$.
4. Use the given charge velocity and $\vec F=q\vec v\times\vec B$ to determine force direction.

## Why it works

The magnetic field is a vector superposition, and the sign of a source charge reverses the field it creates for the same velocity.

## Issue signals

- `charge-sign-field-direction-error`
- `magnetic-field-vector-superposition-error`

# Problem 28.9

## Key concept

The magnetic field direction from a moving negative charge reverses relative to the usual positive-charge right-hand rule.

## Worked solution

1. Construct $\vec r$ from the origin to the specified point.
2. Use $B=\mu_0|q|v\sin\theta/(4\pi r^2)$ for magnitude.
3. Apply the right-hand rule to $\vec v\times\hat r$ for positive charge, then reverse the result because $q<0$.
4. Report magnitude and direction in unit-vector or named-axis form.

## Why it works

The sign of the source charge appears directly in the moving-charge field expression, so it reverses the magnetic-field direction.

## Issue signals

- `negative-source-charge-field-direction-error`
- `moving-charge-field-angle-error`

# Problem 28.37

## Key concept

The field of a long straight wire is $B=\mu_0I/(2\pi r)$; multiple wire fields add as vectors.

## Worked solution

1. From the figure, calculate each wire-to-point distance and use $B_i=\mu_0I_i/(2\pi r_i)$.
2. Use the right-hand rule to assign each field into or out of the page at $P$.
3. Add the signed magnitudes to obtain the expression in $I_1$, $I_2$, and $R$.
4. Set $I_1=I_2$ in the expression for the requested special case.

## Why it works

Each infinite straight wire produces circular field lines, so only their directions at the observation point determine whether contributions reinforce or cancel.

## Issue signals

- `straight-wire-field-distance-error`
- `magnetic-field-vector-superposition-error`

# Problem 28.65

## Key concept

The axial field of one circular loop is
$$
B(z)=\frac{\mu_0IR^2}{2(R^2+z^2)^{3/2}}.
$$

## Worked solution

1. Use $R=0.200\ \text{m}$ and evaluate the one-loop field at the requested point on line $ab$.
2. Determine each loop’s signed axial distance from the point.
3. Add the two equal-direction axial fields.
4. Use symmetry at the midpoint if that is the requested location.

## Why it works

Every current element on a loop contributes an axial component in the same direction at a point on its symmetry axis.

## Issue signals

- `circular-loop-axial-field-distance-error`
- `two-loop-field-superposition-error`

# Problem 28.73

## Key concept

Maximum loop torque is $\tau_{\max}=\mu B=IAB$, where $A=\pi R^2$ for a single circular turn.

## Worked solution

1. Use the ring’s center field $B_{\rm ring}=\mu_0I/(2R)$ to solve for its current $I$.
2. Calculate loop area $A=\pi R^2$.
3. Evaluate $\tau_{\max}=IAB_{\rm ext}$.
4. Orient the loop’s magnetic moment perpendicular to the external field for maximum torque.

## Why it works

Torque tends to align the loop’s magnetic dipole moment with the external field, and the sine factor is largest at $90^\circ$.

## Issue signals

- `loop-center-field-formula-error`
- `magnetic-torque-orientation-error`

# Problem 28.85

## Key concept

Magnetization is dipole moment per volume, so average moment per atom is $\mu_{\rm atom}=M/n_{\rm atom}$.

## Worked solution

1. Calculate atom number density:
$$
n_{\rm atom}=\frac{\rho}{M_{\rm mol}}N_A.
$$
2. Divide the stated magnetization by number density: $\mu_{\rm atom}=M/n_{\rm atom}$.
3. Divide by Bohr magneton $\mu_B$ to express the result in Bohr magnetons.

## Why it works

The macroscopic magnetization is the vector sum of atomic magnetic moments per unit volume.

## Issue signals

- `molar-mass-unit-conversion-error`
- `magnetization-vs-dipole-density-confused`

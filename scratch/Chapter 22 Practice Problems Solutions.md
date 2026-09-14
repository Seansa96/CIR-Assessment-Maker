# Young & Freedman University Physics — Chapter 22 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry matches exactly one selected Chapter 22 prompt.

# Problem 22.1

## Key concept

Electric flux through a flat surface in a uniform field is $\Phi_E=EA\cos\theta$, where $\theta$ is measured from the surface normal.

## Worked solution

1. Insert the given field magnitude, area, and normal-field angle into $\Phi_E=EA\cos\theta$.
2. The shape does not matter for a flat surface with the same area and orientation in a uniform field.
3. Flux magnitude is largest at $\theta=0^\circ$ and smallest at $\theta=90^\circ$.

## Why it works

Flux counts the component of area perpendicular to the field, which is the projected area $A\cos\theta$.

## Issue signals

- `flux-angle-measured-from-plane-error`
- `electric-flux-cosine-error`

# Problem 22.3

## Key concept

For a radial point-charge field, sphere flux is $\Phi_E=E(4\pi r^2)=q/\epsilon_0$.

## Worked solution

1. Multiply the measured field at $r=0.150\ \text{m}$ by sphere area $4\pi r^2$.
2. Apply Gauss’s law $q=\epsilon_0\Phi_E$.
3. Give charge magnitude; determine sign only if the measured field direction is supplied.

## Why it works

The field is normal and equal in magnitude everywhere on a sphere centered on a point charge.

## Issue signals

- `sphere-area-formula-error`
- `gausss-law-charge-flux-error`

# Problem 22.5

## Key concept

Close the hemispherical surface with its circular base and use zero net flux through the closed surface when no charge is enclosed.

## Worked solution

1. Add the flat circular disk to create a closed hemisphere.
2. The disk has outward normal opposite the field, so $\Phi_{\rm disk}=-E\pi R^2$.
3. Since enclosed charge is zero, $\Phi_{\rm curved}+\Phi_{\rm disk}=0$.
4. Therefore $\Phi_{\rm curved}=E\pi R^2$.

## Why it works

Gauss’s law lets an open-surface flux be found by adding an imaginary surface whose flux is simple to calculate.

## Issue signals

- `hemisphere-area-used-for-flux`
- `closed-surface-flux-sign-error`

# Problem 22.7

## Key concept

Net electric flux through a closed boundary is $\Phi_E=q_{\rm enclosed}/\epsilon_0$.

## Worked solution

1. Convert the stated picocoulomb cell charge to coulombs.
2. Calculate $|\Phi_E|=|q|/\epsilon_0$.
3. Since the cell charge is negative, field lines and net flux point inward.

## Why it works

Gauss’s law links the net outward flux to enclosed charge; negative enclosed charge produces negative (inward) flux.

## Issue signals

- `picocoulomb-unit-conversion-error`
- `negative-charge-flux-direction-error`

# Problem 22.9

## Key concept

A uniformly charged thin spherical shell has zero field inside and outside field $E=kQ/r^2$.

## Worked solution

1. Just inside the shell, choose a Gaussian sphere with no enclosed charge: $E=0$.
2. Just outside, use $E=kQ/R^2$, where $R$ is the sphere radius.
3. At $5.00\ \text{cm}$ beyond the surface, use $r=R+0.0500\ \text{m}$ in $E=kQ/r^2$.
4. Set direction outward for positive paint charge and inward for negative paint charge.

## Why it works

Spherical symmetry makes the external field identical to the field of a point charge $Q$ at the center, while an internal Gaussian surface encloses no shell charge.

## Issue signals

- `shell-inside-field-not-zero`
- `distance-from-center-vs-surface-error`

# Problem 22.17

## Key concept

Immediately outside an isolated spherical conductor, $E=k|Q|/R^2$.

## Worked solution

1. Convert diameter to radius: $R=0.160\ \text{m}$.
2. Solve $|Q|=ER^2/k$ using the stated surface field.
3. Divide by elementary charge: $N=|Q|/e$.
4. Because electrons are added, the conductor's net charge is negative.

## Why it works

All excess charge resides on a conductor’s surface, and its external spherically symmetric field has the point-charge form.

## Issue signals

- `diameter-used-as-radius`
- `elementary-charge-factor-error`

# Problem 22.57

## Key concept

For a slab with density $\rho(x)$, use a symmetric Gaussian pillbox and integrate charge density to obtain enclosed charge.

## Worked solution

1. Use the density law from Problem 22.56 as modified by the stated positive constant.
2. For a pillbox of face area $A$ extending symmetrically to $\pm x$, write
$$
Q_{\rm enc}=A\int_{-x}^{x}\rho(x')\,dx'.
$$
3. The two faces contribute $2EA$ to flux.
4. Set $2EA=Q_{\rm enc}/\epsilon_0$ and solve $E(x)$, assigning its direction away from positive charge.

## Why it works

Planar symmetry makes the field perpendicular to the slab and equal in magnitude on the two pillbox faces, while the nonuniform density is handled by integration.

## Issue signals

- `nonuniform-charge-density-integral-error`
- `gaussian-pillbox-flux-factor-error`

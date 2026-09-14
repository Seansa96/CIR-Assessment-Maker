# Young & Freedman University Physics — Chapter 27 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry matches a selected Chapter 27 prompt. Refer to the companion note for preserved figures.

# Problem 27.1

## Key concept

Magnetic force on a moving charge is $\vec F=q\vec v\times\vec B$.

## Worked solution

1. Write the supplied velocity and each magnetic-field vector in component form.
2. Calculate $\vec v\times\vec B$ with a determinant.
3. Multiply by the signed charge $q$.
4. Check that the force is perpendicular to both $\vec v$ and $\vec B$.

## Why it works

The magnetic part of the Lorentz force is a cross product, which selects the velocity component perpendicular to the field and fixes a perpendicular direction.

## Issue signals

- `magnetic-cross-product-component-error`
- `charge-sign-direction-error`

# Problem 27.3

## Key concept

Use the right-hand rule for $\vec F=q\vec v\times\vec B$; reverse it for a negative charge.

## Worked solution

1. Point fingers north for $\vec v$ and curl toward vertically upward $\vec B$.
2. The positive-charge force direction from the right-hand rule is compared with the observed eastward deflection to determine the sign.
3. Because velocity and field are perpendicular, calculate magnitude $F=|q|vB$.
4. Give the force direction consistent with the observed deflection.

## Why it works

Magnetic force cannot be parallel to either velocity or field and reverses direction when charge sign reverses.

## Issue signals

- `right-hand-rule-direction-error`
- `charge-sign-direction-error`

# Problem 27.5

## Key concept

Magnetic force magnitude is $F=|q|vB\sin\theta$.

## Worked solution

1. Use electron charge magnitude $e$.
2. Rearrange:
$$
v=\frac{F}{eB\sin\theta}.
$$
3. Substitute the given force, field, and angle.

## Why it works

Only the velocity component perpendicular to the magnetic field experiences magnetic force.

## Issue signals

- `magnetic-force-sine-angle-error`
- `electron-charge-magnitude-error`

# Problem 27.7

## Key concept

One force measurement constrains only the magnetic-field component perpendicular to the particle’s velocity.

## Worked solution

1. Write $\vec F=q\vec v\times\vec B$ using the supplied vectors.
2. Expand into x-, y-, and z-component equations.
3. Solve the independent equations for the field components they determine.
4. Explain that any component parallel to $\vec v$ is undetermined because $\vec v\times\vec B_{\parallel}=0$.
5. Compute $\vec v\cdot\vec B$ and use $\vec v\cdot\vec B=vB\cos\theta$ for the requested angle.

## Why it works

The cross product measures perpendicularity, while the dot product measures the parallel component.

## Issue signals

- `magnetic-field-parallel-component-overclaimed`
- `cross-product-component-error`

# Problem 27.9

## Key concept

Use observed Lorentz-force directions for particles with known charge signs to solve for the unknown magnetic field.

## Worked solution

1. Write one vector equation $\vec F_p=e\vec v_p\times\vec B$ for the proton.
2. Write a second $\vec F_e=-e\vec v_e\times\vec B$ for the electron.
3. Solve the simultaneous component equations for $\vec B$.
4. Insert this field into $\vec F=-e\vec v\times\vec B$ for the final electron.

## Why it works

Different velocity directions provide independent constraints; the electron’s negative charge reverses the positive-charge force direction.

## Issue signals

- `electron-charge-sign-error`
- `magnetic-cross-product-component-error`

# Problem 27.17

## Key concept

Velocity perpendicular to $\vec B$ causes circular motion while velocity parallel to $\vec B$ remains unchanged, producing a helix.

## Worked solution

1. Split the stated velocity into $v_\perp$ and $v_\parallel$.
2. Use circular radius $r=mv_\perp/(|q|B)$.
3. The cyclotron period is $T=2\pi m/(|q|B)$.
4. The helical pitch is $p=v_\parallel T$.
5. Use the charge sign and right-hand rule for sense of rotation.

## Why it works

The magnetic force is always perpendicular to velocity, so it bends only the transverse motion and does no work.

## Issue signals

- `parallel-velocity-magnetic-force-error`
- `cyclotron-radius-component-error`

# Problem 27.65

## Key concept

Loop torque is $\tau=NIAB\sin\theta$, and circular-loop area scales with diameter squared.

## Worked solution

1. Triple the diameter, so the radius triples.
2. Area becomes $A' = 9A$.
3. With all other quantities unchanged, $\tau'=9\tau$.

## Why it works

Magnetic torque is proportional to magnetic dipole moment $\mu=NIA$, which is proportional to loop area.

## Issue signals

- `diameter-area-scaling-error`
- `magnetic-torque-area-dependence-error`

# Problem 27.69

## Key concept

The force on a current-carrying wire is $\vec F=I\vec L\times\vec B$; equilibrium along the incline requires it to balance $Mg\sin\theta$.

## Worked solution

1. Use the figure to determine the angle between the wire and vertical magnetic field.
2. Find magnetic force magnitude $F_B=ILB\sin\phi$ and use the right-hand rule for its direction.
3. Resolve $F_B$ along the incline.
4. Set the uphill component equal to $Mg\sin\theta$ and solve for the required current; choose its direction so the force is uphill.

## Why it works

On a frictionless incline, the only component that can oppose gravity’s downhill component is the magnetic force component parallel to the surface.

## Issue signals

- `wire-magnetic-force-direction-error`
- `incline-force-component-error`

# Problem 27.71

## Key concept

Gauss’s law for magnetism requires net magnetic flux through every closed surface to be zero.

## Worked solution

1. Use a cylinder from $z=0$ to $z=L$ with radius $r$.
2. The end-cap flux is $\pi r^2[B_z(L)-B_z(0)]=\pi r^2bL$.
3. The curved-surface flux is $2\pi rL B_r(r)$.
4. Set their sum to zero:
$$
B_r(r)=-\frac{br}{2}.
$$
5. Sketch lines with an axial component increasing with $z$ and inward radial component for $b>0$.

## Why it works

Magnetic field lines never begin or end; any increasing upward flux must be balanced by radial inward flux through the cylinder wall.

## Issue signals

- `magnetic-gauss-law-flux-factor-error`
- `magnetic-field-line-source-sink-error`

# Problem 27.83

## Key concept

Integrate $d\vec F=I\,d\vec\ell\times\vec B$ around the voice coil; only the field component that produces a common axial force survives.

## Worked solution

1. Resolve the stated field into axial and radial components relative to the coil.
2. For each tangential current element, calculate $d\vec F=I,d\vec\ell\times\vec B$.
3. Radial force components cancel around the loop by symmetry; axial components add.
4. Multiply the axial contribution for one turn by $N=50$, then use the current direction and right-hand rule for sign.

## Why it works

The nonuniform/radial field orientation breaks the usual uniform-field cancellation and gives every tangential wire element an axial force component in the same direction.

## Issue signals

- `voice-coil-symmetry-cancellation-error`
- `wire-magnetic-force-direction-error`

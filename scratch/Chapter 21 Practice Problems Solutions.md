# Young & Freedman University Physics — Chapter 21 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading matches a selected Chapter 21 prompt. Refer to the companion note for preserved figures.

# Problem 21.1

## Key concept

Charge is quantized: $Q=Ne$, and the number of atoms follows from mass and molar mass.

## Worked solution

1. Calculate excess-electron count $N_e=|Q|/e$.
2. Calculate moles of lead from the given sphere mass and lead molar mass.
3. Convert moles to atoms with $N_{\rm atoms}=nN_A$.
4. Divide $N_e/N_{\rm atoms}$ for excess electrons per lead atom.

## Why it works

The macroscopic net charge is the tiny imbalance between the numbers of electrons and protons.

## Issue signals

- `elementary-charge-factor-error`
- `moles-to-atoms-conversion-error`

# Problem 21.3

## Key concept

Estimate total electrons from body mass, average nucleon mass, and the approximate electron-to-nucleon ratio.

## Worked solution

1. State a reasonable body mass and approximate composition assumption, such as waterlike material with roughly one electron per two nucleons.
2. Estimate atom or nucleon count from $m/m_{\rm nucleon}$.
3. Multiply by the assumed electron fraction.
4. Calculate combined electron charge $Q=-N_ee$.

## Why it works

Ordinary matter is nearly electrically neutral because positive proton charge nearly cancels the huge negative charge of its electrons.

## Issue signals

- `order-of-magnitude-estimate-error`
- `electron-charge-sign-error`

# Problem 21.5

## Key concept

The propagation speed of a signal follows distance divided by travel time, $v=d/\Delta t$.

## Worked solution

1. Extract the neuron length and signal-delay data from the prompt.
2. Convert all lengths and times to SI units.
3. Calculate $v=d/\Delta t$.
4. Compare with the relevant biological or physical speed scale requested.

## Why it works

Speed measures the rate at which the disturbance advances along the neuron, independent of the microscopic mechanism that carries it.

## Issue signals

- `speed-distance-time-ratio-error`
- `millisecond-unit-conversion-error`

# Problem 21.7

## Key concept

Set Coulomb attraction equal to one person's weight: $kq^2/r^2=mg$.

## Worked solution

1. Use $q=1.0\ \text{C}$ and the stated average human mass.
2. Set $kq^2/r^2=mg$.
3. Solve $r=\sqrt{kq^2/(mg)}$.
4. Interpret the unusually large separation as evidence that one coulomb is an enormous everyday charge.

## Why it works

The inverse-square electric force is extraordinarily strong compared with gravity for macroscopic charges.

## Issue signals

- `coulomb-force-inverse-square-error`
- `electric-force-vs-weight-equation-error`

# Problem 21.9

## Key concept

Coulomb's law gives $F=k|q_1q_2|/r^2$.

## Worked solution

1. For equal charges, set $F=kq^2/r^2$ and solve $q=\sqrt{Fr^2/k}$.
2. For charges $q$ and $4q$, set $F=4kq^2/r^2$.
3. Solve for the smaller charge, then multiply by four for the larger one.

## Why it works

Force depends on the product of the two charges, so a specified ratio fixes each charge once the product is known.

## Issue signals

- `coulomb-law-square-root-error`
- `charge-ratio-product-error`

# Problem 21.11

## Key concept

Equal charged spheres have repulsive Coulomb force that produces acceleration $a=F/m$ for each.

## Worked solution

1. Write $ma=kq^2/r^2$ for either sphere.
2. Solve $q=\sqrt{mar^2/k}$.
3. Divide by $e$ to find the number of added electrons.
4. State that both spheres accelerate away from one another because both carry negative charge.

## Why it works

Equal and opposite electrostatic forces act on the two spheres, and like charges repel.

## Issue signals

- `coulomb-force-newtons-law-link-error`
- `electron-addition-charge-sign-error`

# Problem 21.17

## Key concept

The net electric force on a charge is the vector sum of individual Coulomb-force vectors.

## Worked solution

1. Reproduce the geometry and values from Example 21.3.
2. Calculate each force vector on the named charge with $\vec F_i=kq q_i\hat r_i/r_i^2$.
3. Resolve noncollinear forces into Cartesian components.
4. Add components and obtain net magnitude and direction.

## Why it works

Electric forces obey superposition: each source charge contributes independently to the total force.

## Issue signals

- `electric-force-vector-superposition-error`
- `component-sign-error`

# Problem 21.35

## Key concept

An electron accelerated by a uniform electric field gains kinetic energy equal to the field's work.

## Worked solution

1. Use the force and field-region distance from Exercise 21.33.
2. Calculate work $W=qE\Delta x$ with the sign chosen for the electron’s displacement.
3. Apply $K_f=K_i+W$ and solve $v_f=\sqrt{2K_f/m_e}$.

## Why it works

The field transfers energy to the charged particle; the work-energy theorem converts that energy increase into speed.

## Issue signals

- `electron-charge-sign-error`
- `electric-work-energy-error`

# Problem 21.37

## Key concept

The proton's net force is the vector sum of two attractive Coulomb forces toward the electrons.

## Worked solution

1. From the figure, determine each electron-proton separation and each force direction.
2. Calculate each magnitude $F_i=ke^2/r_i^2$.
3. Resolve the force vectors into components, using symmetry if applicable.
4. Add components for net magnitude and direction.

## Why it works

Opposite charges attract, and component addition correctly combines forces that are not along the same line.

## Issue signals

- `electric-force-vector-superposition-error`
- `attraction-direction-error`

# Problem 21.47

## Key concept

The electric field from a point charge is $\vec E=kq\hat r/r^2$, directed toward a negative source charge.

## Worked solution

1. Assign coordinates to the three charges and the off-axis point from the figure.
2. Form displacement vectors from each charge to point $P$.
3. Calculate each field vector, resolving into parallel and perpendicular components.
4. Add components, then compute magnitude and direction of $\vec E_{\rm net}$.

## Why it works

Field is a vector property of space; the test charge is not needed to determine it, and contributions from all sources superpose.

## Issue signals

- `negative-charge-field-direction-error`
- `electric-field-component-sum-error`

# Problem 21.73

## Key concept

Static equilibrium of the charged ball balances gravity, tension, and horizontal electric force.

## Worked solution

1. Draw $mg$ downward, $qE$ horizontal, and tension along the string.
2. With the string angle measured from the vertical wall, use
$$
T\cos\theta=mg,\qquad T\sin\theta=|q|E.
$$
3. Divide to get $E=mg\tan\theta/|q|$.
4. Use the sign of the excess charge and the observed deflection to determine the field direction.

## Why it works

The tension components independently balance the vertical weight and horizontal electrical force.

## Issue signals

- `string-angle-component-error`
- `electric-field-direction-from-charge-error`

# Problem 21.97

## Key concept

Integrate the electric field from infinitesimal charge elements on the quarter-circle.

## Worked solution

1. Use linear charge density $\lambda=Q/(\pi R/2)$ and $dq=\lambda R\,d\theta$.
2. Each element is distance $R$ from the origin, so $dE=k|dq|/R^2$.
3. Resolve the field directed toward the negative element:
$$
dE_x=dE\cos\theta,\qquad dE_y=dE\sin\theta.
$$
4. Integrate from $0$ to $\pi/2$ with the appropriate negative signs.

## Why it works

All source elements are the same distance from the origin, while their differing directions are handled by component integration.

## Issue signals

- `arc-charge-element-error`
- `negative-charge-field-direction-error`

# Problem 21.103

## Key concept

An infinite charged sheet produces field magnitude $|\sigma|/(2\epsilon_0)$ on either side; fields add by superposition.

## Worked solution

1. Draw the field direction from the positive sheet away from it and from the negative sheet toward it.
2. Divide space into regions on each side of and between the two planes.
3. Add the two sheet fields in each region using $E_0=\sigma/(2\epsilon_0)$.
4. Express each result with the unit vector normal to the sheets, including zero field outside when equal opposite sheets are paired.

## Why it works

Each infinite sheet has uniform field independent of distance, so cancellation and reinforcement depend only on the region's side of each sheet.

## Issue signals

- `infinite-sheet-field-factor-error`
- `electric-field-direction-superposition-error`

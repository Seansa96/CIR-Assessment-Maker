# Young & Freedman University Physics — Chapter 13 Practice Problems Solutions

> [!note] Worked-solution companion
> Entries match the assigned Chapter 13 problems exactly. Refer to the companion prompt note for preserved diagrams and given numerical data.

# Problem 13.1

## Key concept

Newtonian gravitational force is $F=GMm/r^2$.

## Worked solution

1. Write the two pulls on the Moon: $F_S=GM_SM_M/r_{SM}^2$ and $F_E=GM_EM_M/r_{EM}^2$.
2. Divide them; the Moon mass and $G$ cancel:
$$F_S/F_E=(M_S/M_E)(r_{EM}/r_{SM})^2.$$
3. Insert Appendix F values and interpret the larger force.

## Why it works

Both Earth and Sun exert the same inverse-square law on the same Moon, so their force ratio is determined entirely by source masses and separations.

## Issue signals

- `inverse-square-ratio-error`
- `orbital-force-interpretation-error`

# Problem 13.3

## Key concept

Each astronaut experiences the same gravitational force magnitude but a different acceleration, $a=F/m$.

## Worked solution

1. Draw one attractive force along the line joining the astronauts on each free-body diagram.
2. Compute $F=Gm_1m_2/r^2$, then $a_1=F/m_1$ and $a_2=F/m_2$.
3. Under the constant-acceleration approximation, use relative acceleration $a_1+a_2$ in $20.0=\tfrac12(a_1+a_2)t^2$.
4. State that the acceleration increases as separation shrinks because gravity varies as $1/r^2$.

## Why it works

The force vectors point toward each other, so the closing acceleration is the sum of their individual acceleration magnitudes.

## Issue signals

- `relative-acceleration-not-summed`
- `inverse-square-dependence-missed`

# Problem 13.5

## Key concept

The released sphere's acceleration is the vector sum of gravitational fields from the two fixed spheres.

## Worked solution

1. From the figure, draw a field vector toward each attracting sphere.
2. Calculate each magnitude with $g_i=Gm_i/r_i^2$.
3. Resolve vectors into horizontal and vertical components using the diagram geometry.
4. Add components and use $a=\sqrt{a_x^2+a_y^2}$ and $\tan^{-1}(a_y/a_x)$ for magnitude and direction.

## Why it works

Gravitational fields superpose linearly, and the test sphere's own mass cancels from $F=ma$.

## Issue signals

- `gravitational-field-vector-sum-error`
- `component-sign-error`

# Problem 13.7

## Key concept

Compare the Moon's pull with weight by dividing two gravitational forces.

## Worked solution

1. Calculate lunar force $F_M=GM_Mm/r_M^2$.
2. Calculate Earth force $F_E=mg$ or $GM_Em/R_E^2$.
3. Form $F_M/F_E$; the person's mass cancels.

## Why it works

Weight is Earth’s gravitational pull, so the comparison uses the same force law and a common test mass.

## Issue signals

- `moon-distance-unit-conversion-error`
- `force-ratio-inverted`

# Problem 13.9

## Key concept

Between two attracting masses, the net field can vanish only where their opposing field magnitudes are equal.

## Worked solution

1. Let $x$ be the distance from the mass $m$ toward the mass $3m$.
2. Set $Gm/x^2=G(3m)/(1.00-x)^2$ and solve for the point between them.
3. Test a slight displacement along the line: it produces a force away from equilibrium, so that direction is unstable.
4. Test a slight perpendicular displacement: both pulls have restoring components toward the line, so that direction is stable.

## Why it works

The equilibrium is a saddle point of gravitational potential: restoring in one direction and anti-restoring in another.

## Issue signals

- `field-balance-distance-error`
- `equilibrium-stability-direction-error`

# Problem 13.11

## Key concept

Gravitational acceleration falls off as $g(r)=GM_E/r^2$.

## Worked solution

1. Divide $g(r)$ by surface gravity $g_0=GM_E/R_E^2$.
2. Solve $g/g_0=(R_E/r)^2$ for $r$.
3. The requested altitude is $h=r-R_E$.

## Why it works

Using a ratio eliminates the need to calculate $GM_E$ separately.

## Issue signals

- `inverse-square-root-error`
- `altitude-vs-center-distance-error`

# Problem 13.29

## Key concept

For a spherical planet, surface gravity and average density determine mass and radius through $g=GM/R^2$ and $M=\rho(4\pi R^3/3)$.

## Worked solution

1. Record the planet data and convert all reported astronomical units to SI units.
2. Combine $g=GM/R^2$ with the supplied mass, radius, orbital, or density relation stated in the prompt.
3. Solve algebraically before substituting values.
4. Check that the result has appropriate units and physical scale.

## Why it works

The gravitational field outside a spherically symmetric planet is the same as if its entire mass were concentrated at its center.

## Issue signals

- `astronomical-unit-conversion-error`
- `surface-gravity-radius-error`

# Problem 13.41

## Key concept

At a body's surface, weight is $W=GMm/R^2$.

## Worked solution

1. Convert the given Earth weight to mass with $m=W_E/g_E$.
2. Use neutron-star radius $R_{NS}=10\ \text{km}$ and solar mass in $W_{NS}=GM_Sm/R_{NS}^2$.
3. Compare with Earth weight as a reasonableness check.

## Why it works

The neutron star has roughly solar mass packed into a vastly smaller radius, making its surface gravitational field enormous.

## Issue signals

- `neutron-star-diameter-used-as-radius`
- `weight-mass-confused`

# Problem 13.57

## Key concept

The exact change in gravitational potential energy is $\Delta U=GM_Em(1/R_E-1/(R_E+h))$, while $mgh$ is the constant-$g$ approximation.

## Worked solution

1. Form the relative error between $mgh$ and the exact $\Delta U$.
2. Cancel the common factor $GM_Em$ after replacing $g$ by $GM_E/R_E^2$.
3. Set the error magnitude equal to $0.01$ and solve for $h/R_E$.
4. Multiply the resulting fraction by $R_E$ for the numerical altitude.

## Why it works

The approximation overestimates the potential-energy increase because gravity weakens above the surface.

## Issue signals

- `exact-potential-energy-sign-error`
- `relative-error-definition-error`

# Problem 13.59

## Key concept

The short fall determines local $g$, and the planet mass follows from $g=GM/R^2$.

## Worked solution

1. From rest, use $\Delta y=\tfrac12gt^2$ to calculate the local gravitational acceleration.
2. Convert the planet radius to meters.
3. Rearrange $g=GM/R^2$ to $M=gR^2/G$.

## Why it works

The stated fall distance is tiny relative to the planet radius, so treating $g$ as constant over that fall is justified.

## Issue signals

- `free-fall-factor-of-two-error`
- `planet-radius-unit-conversion-error`

# Problem 13.65

## Key concept

Conservation of mechanical energy with the exact gravitational potential handles drops comparable to Earth’s radius.

## Worked solution

1. Set initial radius $r_i=R_E+h$ and final radius $r_f=R_E$.
2. Apply
$$
-\frac{GM_Em}{r_i}=-\frac{GM_Em}{R_E}+\frac12mv^2.
$$
3. Cancel $m$ and solve:
$$
v=\sqrt{2GM_E\left(\frac1{R_E}-\frac1{R_E+h}\right)}.
$$

## Why it works

The gravitational force changes substantially over a large altitude, so constant-$g$ kinematics is not generally valid.

## Issue signals

- `constant-g-used-outside-range`
- `gravitational-potential-sign-error`

# Problem 13.73

## Key concept

For an object orbiting the Sun, total mechanical energy $\tfrac12mv^2-GM_Sm/r$ is conserved.

## Worked solution

1. Write energy conservation at the two stated Sun distances:
$$
\frac12v_1^2-\frac{GM_S}{r_1}=\frac12v_2^2-\frac{GM_S}{r_2}.
$$
2. Rearrange for $v_2^2=v_1^2+2GM_S(1/r_2-1/r_1)$.
3. Insert the supplied initial speed and distances, then take the positive square root.

## Why it works

Gravity is conservative, so a comet speeds up as it falls closer to the Sun.

## Issue signals

- `orbital-energy-sign-error`
- `distance-reciprocal-order-error`

# Problem 13.79

## Key concept

The total energy of a circular orbit is $E=-GMm/(2r)$.

## Worked solution

1. Convert each orbital altitude to center-to-spacecraft radius: $r_1=R_M+2000\ \text{km}$ and $r_2=R_M+4000\ \text{km}$.
2. Calculate
$$
W=\Delta E=-\frac{GM_Mm}{2r_2}+\frac{GM_Mm}{2r_1}.
$$
3. Report the positive work required.

## Why it works

Although the higher circular orbit has less negative total energy, the engines must supply energy to reach it.

## Issue signals

- `altitude-vs-orbit-radius-error`
- `circular-orbit-energy-factor-error`

# Problem 13.83

## Key concept

The field of a ring on its symmetry axis is obtained by adding the axial components from all ring elements.

## Worked solution

1. Every ring element is the same distance $\sqrt{a^2+x^2}$ from the sphere center.
2. The transverse force components cancel by symmetry; add only the axial components.
3. Multiply the resulting field by the sphere mass or integrate over the sphere as directed by the prompt.
4. State the force direction: toward the ring.

## Why it works

Rotational symmetry cancels all components perpendicular to the shared axis.

## Issue signals

- `symmetry-component-cancellation-missed`
- `ring-distance-geometry-error`

# Problem 13.89

## Key concept

Build the field of a disk from concentric rings and integrate their axial gravitational-force components.

## Worked solution

1. With surface density $\sigma=M/(\pi a^2)$, a ring has $dm=2\pi r\sigma\,dr$.
2. Its axial force contribution is
$$
dF=\frac{Gm x\,dm}{(x^2+r^2)^{3/2}}.
$$
3. Integrate from $r=0$ to $a$ and give the direction toward the disk.
4. For $x\gg a$, expand the result to show $F\to GMm/x^2$.

## Why it works

The disk is an extended mass distribution, but at large distance its finite size becomes negligible and it behaves like a point mass.

## Issue signals

- `disk-ring-mass-element-error`
- `axial-force-component-error`

# Young & Freedman University Physics — Chapter 23 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading corresponds exactly to a selected Chapter 23 prompt. Refer to the companion note for original figures and complete numerical notation.

# Problem 23.1

## Key concept

Work done by an electrostatic force is path independent: $W_{\rm elec}=q_2(V_i-V_f)$.

## Worked solution

1. Find source-charge potential at each endpoint: $V=kq_1/r$.
2. Calculate $\Delta U=q_2(V_f-V_i)$.
3. The electric-force work is $W_{\rm elec}=-\Delta U$.
4. Keep the signs of both charges in the calculation.

## Why it works

The field of a stationary point charge is conservative, so only the initial and final distances from the source matter.

## Issue signals

- `electric-work-potential-sign-error`
- `point-charge-distance-error`

# Problem 23.3

## Key concept

Assembling charges from infinity requires external work equal to the final electrostatic potential energy.

## Worked solution

1. There are three proton pairs in an equilateral triangle.
2. Each pair contributes $ke^2/a$.
3. Add the pair energies:
$$
U=3\frac{ke^2}{a}.
$$
4. The required assembly work is $W_{\rm ext}=U$.

## Why it works

Bringing like charges together against their mutual repulsion increases the system's stored electric potential energy.

## Issue signals

- `charge-pair-count-error`
- `electrostatic-energy-sign-error`

# Problem 23.5

## Key concept

With gravity ignored, mechanical energy is conserved: $K_i+U_i=K_f+U_f$.

## Worked solution

1. Write $U(r)=kq_1q_2/r$ using the signs of the two sphere charges.
2. For part (a), solve
$$
\frac12mv_f^2=\frac12mv_i^2+U(r_i)-U(r_f).
$$
3. At closest approach in part (b), set the moving sphere’s speed to zero and solve $K_i+U(r_i)=U(r_{\min})$.
4. Check whether the charges repel or attract to interpret the result.

## Why it works

The electrostatic force trades kinetic and potential energy without dissipating energy.

## Issue signals

- `electric-potential-energy-sign-error`
- `turning-point-kinetic-energy-not-zero`

# Problem 23.7

## Key concept

The electric potential energy of a molecular charge configuration is the sum over distinct charge pairs, $U=\sum_{i<j}kq_iq_j/r_{ij}$.

## Worked solution

1. Reuse the molecular charges and separations established in Exercise 21.24.
2. List each distinct guanine–cytosine interacting pair once.
3. Compute $kq_iq_j/r_{ij}$ for every pair and add signed values.
4. Interpret negative total energy as a bound attractive configuration.

## Why it works

Potential energy is additive over pair interactions, with unlike charges lowering and like charges raising the total.

## Issue signals

- `electric-potential-energy-pair-count-error`
- `charge-sign-in-pair-energy-error`

# Problem 23.9

## Key concept

For two released protons, electric potential energy converts to kinetic energy and force increases as separation decreases.

## Worked solution

1. Initial energy is $U_i=ke^2/r_i$ and initial kinetic energy is zero.
2. At very large separation, $U\to0$; divide the total kinetic energy equally between identical protons:
$$
2\left(\frac12mv_{\max}^2\right)=\frac{ke^2}{r_i}.
$$
3. Maximum speed occurs as separation approaches infinity.
4. Use $a=ke^2/(mr^2)$ at the initial separation for maximum acceleration.

## Why it works

The protons repel, so they continuously accelerate apart while their force weakens with increasing separation.

## Issue signals

- `two-particle-energy-sharing-error`
- `maximum-force-separation-error`

# Problem 23.11

## Key concept

The potential energy of three point charges is the sum of the three pairwise interaction energies.

## Worked solution

1. Identify the three distinct separations from the prompt or figure.
2. Write
$$
U=k\left(\frac{q_1q_2}{r_{12}}+\frac{q_1q_3}{r_{13}}+\frac{q_2q_3}{r_{23}}\right).
$$
3. Substitute signed charges and evaluate.
4. Use the sign of $U$ to describe whether the configuration is energetically bound relative to infinity.

## Why it works

Electrostatic potential energy is a scalar, so pair contributions add directly rather than by vector addition.

## Issue signals

- `electric-potential-energy-pair-count-error`
- `charge-sign-in-pair-energy-error`

# Problem 23.43

## Key concept

An isolated charged conductor is an equipotential, so its center has the same potential as its surface.

## Worked solution

1. A field directed toward the center means the sphere charge is negative.
2. Use surface field magnitude $E=k|Q|/R^2$ to solve $Q=-ER^2/k$.
3. The conductor potential is
$$
V_{\rm center}=V_{\rm surface}=\frac{kQ}{R}=-ER.
$$

## Why it works

The electric field inside a conductor in electrostatic equilibrium is zero, so potential cannot vary anywhere within it.

## Issue signals

- `conductor-center-potential-not-equal-surface`
- `electric-field-charge-sign-error`

# Problem 23.71

## Key concept

The self-energy is the work needed to assemble a continuously distributed charge from infinity.

## Worked solution

1. Build the uniform sphere shell by shell. A shell of charge $dq$ at radius $r$ is added to already enclosed charge $q(r)$.
2. Its incremental work is $dU=V(r)dq=kq(r)dq/r$.
3. Express $q(r)=Q(r^3/R^3)$ and $dq=3Qr^2dr/R^3$.
4. Integrate from $0$ to $R$ to obtain
$$
U=\frac35\frac{kQ^2}{R}.
$$

## Why it works

Each added layer must be brought through the electric potential created by all charge that has already been assembled inside it.

## Issue signals

- `charge-assembly-integral-error`
- `uniform-sphere-self-energy-coefficient-error`

# Problem 23.77

## Key concept

Potential difference is the negative line integral of electric field: $\Delta V=-\int\vec E\cdot d\vec\ell$.

## Worked solution

1. Take the piecewise radial field from Problem 22.45.
2. Identify the conductor radius and insulating-shell radius from that problem.
3. Integrate $-E(r)\,dr$ across each radial region between the two specified surfaces.
4. Add the region contributions with consistent limits to obtain the requested potential difference.

## Why it works

Electrostatic field is conservative, so the radial integral provides the potential difference independent of path.

## Issue signals

- `potential-field-integral-sign-error`
- `piecewise-electric-field-region-error`

# Problem 23.89

## Key concept

For an alpha particle near a stationary lead nucleus, total mechanical energy and angular momentum are conserved.

## Worked solution

1. Take initial kinetic energy $K_i=p^2/(2m)$ and repulsive potential $U_i=kq_\alpha q_{Pb}/r_i\approx0$ at large initial distance.
2. At closest approach, radial speed is zero but tangential motion remains: $L=mrv_t$.
3. Write
$$
K_i=\frac{L^2}{2mr_{\min}^2}+\frac{kq_\alpha q_{Pb}}{r_{\min}}.
$$
4. Insert each stated angular momentum and solve the resulting quadratic for the positive $r_{\min}$.

## Why it works

Nonzero angular momentum supplies a centrifugal kinetic-energy term, preventing a near-miss trajectory from approaching as closely as a head-on collision.

## Issue signals

- `angular-momentum-term-omitted`
- `closest-approach-radial-speed-confused-with-total-speed`

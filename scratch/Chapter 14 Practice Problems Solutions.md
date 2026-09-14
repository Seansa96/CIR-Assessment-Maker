# Young & Freedman University Physics — Chapter 14 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry matches a heading in the Chapter 14 practice-problems note. Use that note for the original figures.

# Problem 14.1

## Key concept

Frequency, period, and angular frequency are related by $T=1/f$ and $\omega=2\pi f$.

## Worked solution

1. For the sung B-flat, use $f=466\ \text{Hz}$.
2. Calculate $T=1/f$ for one vocal-cord cycle.
3. Calculate $\omega=2\pi f$.
4. For the hearing part, use the given eardrum period in the same two formulas.

## Why it works

Frequency counts cycles per second, period is seconds per cycle, and angular frequency expresses the same cycling rate in radians per second.

## Issue signals

- `frequency-period-reciprocal-error`
- `angular-frequency-factor-error`

# Problem 14.3

## Key concept

The vibration count over a known time gives frequency directly.

## Worked solution

1. Calculate $f=N/\Delta t=440/0.500$.
2. Find $\omega=2\pi f$.
3. Find $T=1/f$.

## Why it works

The tuning fork completes equal cycles at a constant rate, so total cycles divided by elapsed time is its frequency.

## Issue signals

- `frequency-period-reciprocal-error`
- `angular-frequency-factor-error`

# Problem 14.5

## Key concept

In SHM, phase change determines travel time: $\Delta t=\Delta\theta/\omega$.

## Worked solution

1. Calculate $\omega=2\pi f$ from the stated frequency.
2. Locate the two stated positions on an $x$ versus phase cycle.
3. Determine the smallest forward phase advance $\Delta\theta$ between them.
4. Evaluate $\Delta t=\Delta\theta/\omega$; the amplitude is useful for locating positions but does not change the period.

## Why it works

Uniform phase advance maps each fraction of an oscillation cycle to the same fraction of its period.

## Issue signals

- `shm-phase-fraction-error`
- `amplitude-used-to-change-period`

# Problem 14.7

## Key concept

For a mass-spring oscillator, $\omega=\sqrt{k/m}$, $f=\omega/(2\pi)$, and $T=1/f$.

## Worked solution

1. Use $T=1/(6.00\ \text{Hz})$.
2. Compute $\omega=2\pi(6.00\ \text{Hz})$.
3. Rearrange the spring relation to $m=k/\omega^2$ and insert the given $k$.

## Why it works

The spring restoring force produces an acceleration proportional to displacement, and the inertia $m$ controls how quickly the mass responds.

## Issue signals

- `spring-frequency-formula-inverted`
- `angular-frequency-factor-error`

# Problem 14.9

## Key concept

From an extreme position, an SHM object takes one-quarter period to reach equilibrium and one-half period to reach the opposite extreme.

## Worked solution

1. The object is initially at $x=A$ and at rest, so it begins at a positive turning point.
2. Mark the stated destination positions on the oscillation cycle.
3. Express each required travel as the appropriate fraction of $T=0.900\ \text{s}$.
4. Multiply that fraction by the period.

## Why it works

The sinusoidal motion is symmetric, with fixed timing between turning points and equilibrium crossings.

## Issue signals

- `shm-quarter-period-timing-error`
- `initial-phase-misidentified`

# Problem 14.33

## Key concept

The total energy of a spring oscillator is $E=\tfrac12kA^2$.

## Worked solution

1. At displacement $x$, write $U=\tfrac12kx^2$.
2. If elastic potential energy equals kinetic energy, each equals $E/2=\tfrac14kA^2$.
3. Set $\tfrac12kx^2=\tfrac14kA^2$ and solve:
$$|x|=A/\sqrt2.$$

## Why it works

Energy shifts continuously between spring potential energy and kinetic energy while their sum remains fixed.

## Issue signals

- `total-energy-amplitude-error`
- `equal-energy-algebra-error`

# Problem 14.79

## Key concept

The small-angle frequency of a physical pendulum is $f=(1/2\pi)\sqrt{Mgd/I_p}$.

## Worked solution

1. Find the square frame's center of mass: it lies at its geometric center, a distance $d=L/\sqrt2$ from the upper-corner pivot.
2. Add the four rod inertias about the pivot, using direct integration or the parallel-axis theorem.
3. Substitute total mass $M=4m$, $d$, and $I_p$ into $f=(1/2\pi)\sqrt{Mgd/I_p}$.

## Why it works

For a small angular displacement, gravity supplies a restoring torque approximately equal to $-Mgd\theta$.

## Issue signals

- `physical-pendulum-center-distance-error`
- `parallel-axis-term-omitted`

# Problem 14.87

## Key concept

The time from one turning point to the opposite turning point is half a simple pendulum's period.

## Worked solution

1. Identify the supplied swing time as $T/2$, then calculate $T$.
2. Use $T=2\pi\sqrt{\ell/g_N}$ to find Newtonia's surface gravity $g_N$.
3. Convert the measured circumference to radius with $R=C/(2\pi)$.
4. Use $g_N=GM/R^2$ to obtain $M=g_NR^2/G$.

## Why it works

The pendulum period measures local gravity, while the planetary circumference provides the radius needed to convert surface gravity into mass.

## Issue signals

- `half-period-swing-time-error`
- `circumference-radius-conversion-error`

# Problem 14.97

## Key concept

For a small angular displacement, the spring force produces a restoring torque proportional to angle.

## Worked solution

1. The lower end moves horizontally by approximately $(L/2)\theta$ for small $\theta$.
2. The spring force magnitude is $F\approx k(L/2)\theta$.
3. Its torque magnitude about the pivot is $\tau\approx-(L/2)F=-kL^2\theta/4$.
4. With rod inertia $I=ML^2/12$, write $I\ddot\theta=-(kL^2/4)\theta$ and identify $\omega=\sqrt{3k/M}$.
5. Hence $T=2\pi\sqrt{M/(3k)}$.

## Why it works

The small-angle approximation makes the torque linear in displacement, which is the defining condition for SHM.

## Issue signals

- `small-angle-linearization-error`
- `rod-inertia-axis-error`

# Problem 14.99

## Key concept

An L-shaped rigid body on a sharp pivot is a physical pendulum.

## Worked solution

1. Locate the composite center of mass by averaging the centers of the two equal rods.
2. Compute its distance $d$ from the sharp edge using the figure geometry.
3. Add the two rods' inertias about the edge using the parallel-axis theorem.
4. Use $f=(1/2\pi)\sqrt{Mgd/I_p}$ with total mass $M=2m$.

## Why it works

Gravity provides a restoring torque about the pivot, and the object's distributed mass determines its rotational inertia.

## Issue signals

- `composite-center-of-mass-error`
- `physical-pendulum-inertia-error`

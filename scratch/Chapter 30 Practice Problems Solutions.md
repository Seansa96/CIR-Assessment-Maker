# Young & Freedman University Physics — Chapter 30 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry matches exactly one selected Chapter 30 prompt.

# Problem 30.1

## Key concept

Mutual induction gives $|\mathcal E_2|=M|di_1/dt|$, and mutual inductance is symmetric: $M_{12}=M_{21}$.

## Worked solution

1. Multiply the given mutual inductance by the stated uniform current-change rate:
$$
|\mathcal E_2|=M\left|\frac{di_1}{dt}\right|.
$$
2. Since $di/dt$ is constant, the induced-emf magnitude is constant.
3. Swap which coil carries the changing current and use the same $M$ to find the induced emf in the other coil.

## Why it works

The flux linkage produced in either coil per unit current in the other is the same reciprocal property of the two-coil system.

## Issue signals

- `mutual-inductance-current-rate-error`
- `mutual-inductance-symmetry-missed`

# Problem 30.3

## Key concept

The central field of a long solenoid is $B=\mu_0N_1I/\ell$, and mutual inductance is flux linkage in the outer coil per solenoid current.

## Worked solution

1. Calculate the solenoid cross-sectional area $A=\pi(d/2)^2$.
2. Field inside the solenoid is $B=\mu_0N_1I/\ell$.
3. Flux through one turn of the second coil is $\Phi=BA$.
4. Multiply by $N_2$ and divide by $I$:
$$
M=\frac{N_2\Phi}{I}=\frac{\mu_0N_1N_2A}{\ell}.
$$

## Why it works

The second coil links the nearly uniform magnetic flux produced inside the long solenoid.

## Issue signals

- `solenoid-area-diameter-error`
- `mutual-inductance-turn-count-error`

# Problem 30.5

## Key concept

For coaxial toroidal solenoids, mutual inductance comes from the flux of one toroid through every turn of the other.

## Worked solution

1. Use the toroid field $B(r)=\mu_0N_1I/(2\pi r)$ within the core.
2. Integrate the field across the stated toroid cross section to obtain flux per turn of the second toroid.
3. Multiply by $N_2$ and divide by $I$ for $M$.
4. Use the given radii and cross-sectional dimensions consistently; invoke the mean-radius approximation only if the prompt permits it.

## Why it works

The toroidal field is confined mainly to the common core and varies as $1/r$, so its flux must be integrated across the core geometry.

## Issue signals

- `toroid-field-radius-dependence-error`
- `mutual-inductance-flux-linkage-error`

# Problem 30.7

## Key concept

For a thin toroidal solenoid, $L=\mu_0N^2A/(2\pi r)$ and self-induced emf magnitude is $|\mathcal E|=L|di/dt|$.

## Worked solution

1. Convert the stated average radius and cross-sectional area to SI units.
2. Rearrange the inductance formula:
$$
N=\sqrt{\frac{L(2\pi r)}{\mu_0A}}.
$$
3. Use the result for part (a).
4. For part (b), solve $|di/dt|=|\mathcal E|/L$.

## Why it works

Inductance measures flux linkage per current and grows as the square of turn count; a changing current produces voltage proportional to its rate of change.

## Issue signals

- `toroid-inductance-turn-count-error`
- `self-induced-emf-rate-error`

# Problem 30.9

## Key concept

The self-induced emf magnitude obeys $|\mathcal E|=L|di/dt|$.

## Worked solution

1. Use the given emf and current-change rate:
$$
L=\frac{|\mathcal E|}{|di/dt|}.
$$
2. Insert the values, including $0.0160\ \text{V}$ and $0.0640\ \text{A/s}$.
3. For later parts, use this same $L$ in $\mathcal E=-L,di/dt$, keeping the minus sign for Lenz’s-law direction.

## Why it works

An inductor resists changes in its own current, with a voltage proportional to how rapidly that current is being changed.

## Issue signals

- `self-induced-emf-rate-error`
- `inductor-emf-lenzs-law-sign-error`

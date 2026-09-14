# Young & Freedman University Physics — Chapter 29 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry corresponds exactly to a selected Chapter 29 prompt. Refer to the companion note for original figures.

# Problem 29.1

## Key concept

Faraday’s law for one loop is $\mathcal E=-d\Phi_B/dt$, with $\Phi_B=BA\cos\theta$.

## Worked solution

1. The field is perpendicular to the loop, so $\Phi_B=BA$.
2. With constant area, calculate $|\mathcal E|=A|dB/dt|$.
3. Use Lenz’s law to identify the induced field direction that opposes the decreasing original flux.
4. Use the right-hand rule to identify current direction if requested.

## Why it works

An induced current responds to a change in magnetic flux, not to the magnetic field value by itself.

## Issue signals

- `faradays-law-flux-rate-error`
- `lenzs-law-direction-error`

# Problem 29.3

## Key concept

The integrated induced emf determines total charge: $Q=(1/R)\int\mathcal E\,dt$.

## Worked solution

1. Initial coil flux linkage is $NAB$ and final linkage is zero.
2. Use Faraday’s law:
$$
\int\mathcal E\,dt=-\Delta(N\Phi_B)=NAB.
$$
3. With $I=\mathcal E/R$, obtain $Q=NAB/R$ in magnitude.
4. For the credit card, explain that alternating magnetized regions create changing flux and a time-varying voltage pattern; speed changes timing and amplitude but not the ordered pattern itself.

## Why it works

Total charge depends on total flux change, so it is independent of how rapidly the coil is turned or card is swiped, within operating limits.

## Issue signals

- `induced-charge-flux-change-error`
- `swipe-speed-vs-flux-change-confused`

# Problem 29.5

## Key concept

Removing a loop from a uniform perpendicular field changes its flux from $BA$ to zero.

## Worked solution

1. Calculate area $A=\pi(0.120\ \text{m})^2$.
2. Average emf magnitude is
$$
|\mathcal E_{\rm avg}|=\frac{BA}{\Delta t}.
$$
3. The upward external flux is decreasing, so the induced current creates an upward field.
4. Viewed from above, use the right-hand rule: an upward induced field requires counterclockwise current.

## Why it works

Lenz’s law makes the induced magnetic effect oppose the loss of the original flux.

## Issue signals

- `circle-area-radius-error`
- `lenzs-law-direction-error`

# Problem 29.7

## Key concept

The field of a long wire is $B=\mu_0i/(2\pi r)$, and changing current changes the loop’s magnetic flux.

## Worked solution

1. For an upward current, use the right-hand rule to determine the field direction to the right of the wire, and calculate its magnitude.
2. A strip of width $dr$ and length $\ell$ has flux $d\Phi=B\ell\,dr$.
3. Integrate over the loop’s near and far distances:
$$
\Phi=\frac{\mu_0i\ell}{2\pi}\ln\!\left(\frac{r_{\rm far}}{r_{\rm near}}\right).
$$
4. Differentiate and apply Faraday’s law:
$$
\mathcal E=-\frac{\mu_0\ell}{2\pi}\ln\!\left(\frac{r_{\rm far}}{r_{\rm near}}\right)\frac{di}{dt}.
$$
5. Substitute the stated numerical values and apply Lenz’s law for direction.

## Why it works

The wire field varies as $1/r$, so the loop flux must be obtained by integrating narrow strips rather than multiplying one field value by total area.

## Issue signals

- `straight-wire-field-integration-error`
- `lenzs-law-direction-error`

# Problem 29.9

## Key concept

At constant perpendicular field, induced emf magnitude is $|\mathcal E|=B|dA/dt|$.

## Worked solution

1. Relate circumference and radius: $C=2\pi r$, so $r=C/(2\pi)$.
2. Area is $A=\pi r^2=C^2/(4\pi)$.
3. Differentiate:
$$
\frac{dA}{dt}=\frac{C}{2\pi}\frac{dC}{dt}.
$$
4. Calculate the circumference after $9.0\ \text{s}$, then evaluate $|\mathcal E|=B|dA/dt|$.
5. As flux decreases, use Lenz’s law to choose the current that reinforces the original field.

## Why it works

The shrinking loop reduces the area threaded by the fixed magnetic field, causing a changing flux even though $B$ is constant.

## Issue signals

- `circumference-to-area-derivative-error`
- `lenzs-law-direction-error`

# Problem 29.63

## Key concept

Inside a uniformly current-filled cylindrical wire, $B(r)=\mu_0Ir/(2\pi R^2)$.

## Worked solution

1. Use Ampère’s law for an interior radius $r$: enclosed current is $I(r^2/R^2)$.
2. Solve $B(2\pi r)=\mu_0I r^2/R^2$ for $B(r)$.
3. A narrow rectangular strip of length $W$ and width $dr$ has $d\Phi=B(r)W\,dr$.
4. Integrate from the wire center to its edge:
$$
\Phi=\int_0^R\frac{\mu_0I r}{2\pi R^2}W\,dr=\frac{\mu_0IW}{4\pi}.
$$

## Why it works

Current enclosed by an Amperian circle increases with $r^2$, so the interior magnetic field grows linearly with radial distance.

## Issue signals

- `interior-wire-ampere-law-error`
- `magnetic-flux-strip-integral-error`

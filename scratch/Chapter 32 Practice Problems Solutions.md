# Young & Freedman University Physics — Chapter 32 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading matches exactly one selected Chapter 32 prompt. Refer to the companion note for diagrams.

# Problem 32.1

## Key concept

Light travels in vacuum at $c$, so distance and travel time obey $d=ct$.

## Worked solution

1. Convert the Moon–Earth distance from kilometers to meters.
2. Calculate $t=d/c$ and report in seconds.
3. For Sirius, convert $8.61\ \text{yr}$ to seconds.
4. Calculate $d=ct$ and convert the result to kilometers.

## Why it works

In vacuum, all electromagnetic waves travel at the universal speed $c$.

## Issue signals

- `light-travel-distance-time-ratio-error`
- `year-to-second-conversion-error`

# Problem 32.3

## Key concept

For a vacuum electromagnetic wave, $E=cB$, and $\vec E\times\vec B$ points in the propagation direction.

## Worked solution

1. Calculate magnetic-field magnitude from $B=E/c$.
2. Use the given propagation direction and electric-field direction.
3. Choose the magnetic-field direction perpendicular to both so that $\vec E\times\vec B$ points along the stated propagation direction.

## Why it works

The electric field, magnetic field, and direction of propagation form a mutually perpendicular right-handed set.

## Issue signals

- `electric-magnetic-field-ratio-inverted`
- `em-wave-right-hand-rule-error`

# Problem 32.5

## Key concept

For electromagnetic radiation in vacuum, $f=c/\lambda$, $T=1/f$, and $k=2\pi/\lambda$.

## Worked solution

1. Convert $0.10\ \text{nm}$ to meters.
2. Calculate frequency $f=c/\lambda$.
3. Calculate period $T=1/f$.
4. Calculate wave number $k=2\pi/\lambda$.

## Why it works

X rays travel at light speed in vacuum; their short wavelength therefore corresponds to a very high frequency and large wave number.

## Issue signals

- `nanometer-unit-conversion-error`
- `wave-number-two-pi-factor-error`

# Problem 32.7

## Key concept

The relevant Maxwell equations show that changing magnetic field creates curling electric field and changing electric field creates curling magnetic field.

## Worked solution

1. For the narrow Faraday-law rectangle, write the line integral as the difference of the two long-side electric-field contributions.
2. Approximate flux as $B_z\Delta x\Delta y$ and take the limiting ratio to obtain the stated partial-derivative relation between $\partial E_y/\partial x$ and $\partial B_z/\partial t$.
3. Repeat the narrow-rectangle logic with the Ampère–Maxwell law for the second relation linking $\partial B_z/\partial x$ and $\partial E_y/\partial t$.
4. Track signs from the chosen loop orientation.

## Why it works

The local differential forms of Maxwell’s equations are the limit of their integral forms applied to an infinitesimal loop.

## Issue signals

- `maxwell-equation-partial-derivative-sign-error`
- `faraday-ampere-law-confused`

# Problem 32.9

## Key concept

In air, electromagnetic waves have approximately $v=c$, so $f=c/\lambda$ and $\lambda=c/f$.

## Worked solution

1. Convert every wavelength to meters before using $f=c/\lambda$.
2. Calculate frequencies for the stated kilometer, intermediate, and nanometer wavelengths.
3. For gamma rays and the AM station, calculate $\lambda=c/f$.
4. Convert each requested wavelength to both meters and nanometers.

## Why it works

Air changes light speed by only a tiny amount in this context, so the vacuum speed $c$ is an appropriate approximation.

## Issue signals

- `em-wave-speed-frequency-wavelength-error`
- `wavelength-unit-conversion-error`

# Problem 32.47

## Key concept

Absorption and reflection have different radiation pressures: $p_{\rm abs}=S/c$ and $p_{\rm refl}=2S/c$.

## Worked solution

1. Convert electric-field amplitude to average intensity:
$$
S_{\rm avg}=\frac12c\epsilon_0E_0^2.
$$
2. Calculate each reflector’s force from pressure times area, using $S/c$ for absorption and $2S/c$ for reflection.
3. The two forces act at equal lever arms but generate opposite torques; subtract their magnitudes.
4. Treat the two reflector masses as point masses at $0.500\ \text{m}$, giving $I=2m(0.500)^2$.
5. Calculate $\alpha=\tau_{\rm net}/I$ and give direction toward the side with the greater force’s rotational effect.

## Why it works

Reflecting light reverses photon momentum and transfers twice the normal momentum of absorption, so the two equal-area reflectors experience unequal radiation forces.

## Issue signals

- `radiation-pressure-reflection-factor-error`
- `point-mass-rotational-inertia-error`

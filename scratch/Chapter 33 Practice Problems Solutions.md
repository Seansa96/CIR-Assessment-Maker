# Young & Freedman University Physics — Chapter 33 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading matches exactly one selected Chapter 33 prompt. Refer to the companion note for diagrams.

# Problem 33.1

## Key concept

The law of reflection makes the incident and reflected angles equal when measured from the mirror normal.

## Worked solution

1. Draw the incident point, the target midpoint on the second mirror, and the mirror-intersection corner using the figure dimensions.
2. Reflect the target point across the first mirror; the required two-segment reflected path becomes a straight line to the image point.
3. Use right-triangle geometry to find the angle of that straight line relative to the first mirror.
4. Convert to the requested incidence angle relative to the normal.

## Why it works

Reflecting the target across a plane mirror converts the equal-angle reflection condition into a straight-line path construction.

## Issue signals

- `reflection-angle-normal-vs-surface-error`
- `mirror-image-geometry-error`

# Problem 33.3

## Key concept

In a medium of refractive index $n$, light speed is $v=c/n$ and wavelength is $\lambda=\lambda_0/n$.

## Worked solution

1. Calculate speed $v=c/1.47$.
2. Calculate liquid wavelength $\lambda=(650\ \text{nm})/1.47$.
3. Note that frequency remains unchanged on entering the liquid.

## Why it works

The material slows the wave propagation while the boundary condition fixes frequency, so wavelength decreases in the same ratio as speed.

## Issue signals

- `refractive-index-speed-ratio-inverted`
- `frequency-changes-at-boundary-error`

# Problem 33.5

## Key concept

Refractive index is $n=c/v$, and frequency is related to wavelength by $f=v/\lambda$ in the medium.

## Worked solution

1. Use the stated light speed in quartz to calculate $n=c/v$.
2. Use the wavelength information supplied in the prompt with $f=v/\lambda$.
3. If asked for vacuum wavelength, use $\lambda_0=n\lambda$.

## Why it works

Frequency does not change across a boundary; refractive index captures the resulting change in speed and wavelength.

## Issue signals

- `refractive-index-speed-ratio-inverted`
- `medium-wavelength-vacuum-wavelength-confused`

# Problem 33.7

## Key concept

Reflection preserves the angle to the normal, and refraction obeys Snell’s law $n_1\sin\theta_1=n_2\sin\theta_2$.

## Worked solution

1. Convert the given angle with the surface to incidence angle with the normal: $\theta_1=90^\circ-\alpha$.
2. The reflected ray has the same normal angle $\theta_r=\theta_1$, then convert back to an angle with the surface.
3. For refraction, use $\sin\theta_2=(n_{\rm air}/1.66)\sin\theta_1$.
4. Convert $\theta_2$ from normal angle to surface angle.

## Why it works

Both reflection and Snell’s law use angles measured from the normal, not from the surface.

## Issue signals

- `refraction-angle-normal-vs-surface-error`
- `snells-law-index-ratio-error`

# Problem 33.9

## Key concept

Snell’s law determines refractive index, and speed in the material is $v=c/n$.

## Worked solution

1. Use $n_{\rm air}\sin\theta_{\rm air}=n_{\rm plastic}\sin\theta_{\rm plastic}$ with $n_{\rm air}\approx1$.
2. Solve
$$
n_{\rm plastic}=\frac{\sin\theta_{\rm air}}{\sin\theta_{\rm plastic}}.
$$
3. Calculate $v=c/n_{\rm plastic}$.

## Why it works

The bending angles determine how much light slows in the plastic relative to air.

## Issue signals

- `snells-law-index-ratio-error`
- `refractive-index-speed-ratio-inverted`

# Problem 33.33

## Key concept

Malus’s law for initially polarized light is $I=I_0\cos^2\theta$.

## Worked solution

1. From the first condition, write $I_1=I_0\cos^2\theta$.
2. For desired intensity $I_2$, write $I_2=I_0\cos^2\phi$.
3. Divide the equations:
$$
\cos^2\phi=\frac{I_2}{I_1}\cos^2\theta.
$$
4. Solve for the angle $\phi$ in the physically relevant range.

## Why it works

A polarizer transmits only the component of the electric-field oscillation along its transmission axis; intensity is proportional to field amplitude squared.

## Issue signals

- `malus-law-square-omitted`
- `polarizer-angle-reference-error`

# Young & Freedman University Physics — Chapter 36 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading matches exactly one selected Chapter 36 prompt. Refer to the companion note for diagrams.

# Problem 36.1

## Key concept

Single-slit diffraction minima satisfy $a\sin\theta=m\lambda$; for a small angle, $y\approx L\sin\theta$.

## Worked solution

1. Use the first minimum, so $m=1$.
2. With $y_1=1.35\ \text{mm}$ and $L=2.00\ \text{m}$, use $\sin\theta\approx y_1/L$.
3. Calculate
$$
\lambda=a\frac{y_1}{L}
$$
with $a=0.750\ \text{mm}$.
4. Convert the final wavelength to nanometers if appropriate.

## Why it works

At the first dark fringe, contributions from corresponding halves of the slit cancel pairwise because their path difference is one-half wavelength.

## Issue signals

- `single-slit-minimum-order-error`
- `millimeter-to-meter-conversion-error`

# Problem 36.3

## Key concept

Dark fringes occur when $a\sin\theta=m\lambda$, with physically allowed $|\sin\theta|\le1$.

## Worked solution

1. Find the largest possible order from $m\le a/\lambda$.
2. Take the largest integer $m_{\max}$ not exceeding that ratio.
3. There are two dark fringes for each positive order, so total count is $2m_{\max}$.
4. For the most distant dark fringe, calculate $\theta=\sin^{-1}(m_{\max}\lambda/a)$.

## Why it works

The sine of a real observation angle cannot exceed one, which limits how many path-difference orders can occur.

## Issue signals

- `diffraction-order-limit-error`
- `dark-fringe-double-sided-count-error`

# Problem 36.5

## Key concept

Sound diffraction through a slit follows the same minima condition $a\sin\theta=m\lambda$.

## Worked solution

1. For each possible positive integer $m$, calculate $\sin\theta_m=m\lambda/a$.
2. Keep only orders with $m\lambda/a\le1$.
3. At screen distance $L=8.00\ \text{m}$, use $y_m=L\tan\theta_m$.
4. Give the zero-intensity distances symmetrically on both sides of the centerline.

## Why it works

Wave interference across the width of the opening creates the same destructive path-difference conditions for sound as for light.

## Issue signals

- `single-slit-minimum-order-error`
- `screen-distance-tangent-vs-sine-error`

# Problem 36.7

## Key concept

First single-slit minimum gives $a\sin\theta_1=\lambda$, and water-wave wavelength is $\lambda=v/f$.

## Worked solution

1. Convert $75.0\ \text{crests/min}$ to frequency in hertz.
2. Calculate wavelength $\lambda=v/f$ from the stated wave speed.
3. Use the shore geometry to find $\theta_1=\tan^{-1}(y/L)$ for the first no-wave location.
4. Solve hole width $a=\lambda/\sin\theta_1$.
5. Other no-wave angles satisfy $\sin\theta_m=m\lambda/a$ for allowed integer $m$.

## Why it works

The barrier opening acts as a single slit, and the first intensity zero bounds the central diffraction maximum.

## Issue signals

- `wave-frequency-crest-rate-conversion-error`
- `single-slit-minimum-order-error`

# Problem 36.9

## Key concept

Doorway diffraction uses sound wavelength $\lambda=v/f$ and single-slit minima $a\sin\theta=m\lambda$.

## Worked solution

1. Use air sound speed and $f=1250\ \text{Hz}$ to calculate $\lambda=v/f$.
2. For a $1.00\ \text{m}$ door, find allowed minimum orders from $m\lambda/a\le1$.
3. Calculate each minimum angle $\theta_m=\sin^{-1}(m\lambda/a)$.
4. Interpret the angular width of the central maximum as the region where sound is readily heard.

## Why it works

When wavelength is not negligible compared with doorway width, wavefronts spread noticeably rather than propagating only straight ahead.

## Issue signals

- `sound-wavelength-frequency-error`
- `diffraction-order-limit-error`

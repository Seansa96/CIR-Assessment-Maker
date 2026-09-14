# Young & Freedman University Physics — Chapter 15 Practice Problems Solutions

> [!note] Worked-solution companion
> Entries correspond exactly to the Chapter 15 answer-key-backed practice prompts.

# Problem 15.1

## Key concept

For a wave, $v=f\lambda$ and $T=1/f$.

## Worked solution

1. Use the stated speed of sound and $f=784\ \text{Hz}$ to calculate $\lambda=v/f$.
2. Calculate one vibration time with $T=1/f$, then convert seconds to milliseconds.
3. An octave higher doubles frequency, so its wavelength is one-half the wavelength in part (a).

## Why it works

At fixed medium and temperature, sound speed stays essentially fixed, so wavelength is inversely proportional to frequency.

## Issue signals

- `wave-speed-frequency-wavelength-error`
- `octave-frequency-ratio-error`

# Problem 15.3

## Key concept

Wave speed is crest-to-crest wavelength divided by period, $v=\lambda/T$.

## Worked solution

1. Convert $800\ \text{km}$ to meters and $1.0\ \text{h}$ to seconds.
2. Evaluate $v=\lambda/T$ in m/s.
3. Convert that result to km/h using $3.6\ \text{km/h}$ per m/s.
4. Relate the large speed and long wavelength to the wide area affected by a tsunami.

## Why it works

One period is the time required for one full wavelength of the wave pattern to move past a fixed point.

## Issue signals

- `wave-period-unit-conversion-error`
- `wave-speed-frequency-wavelength-error`

# Problem 15.5

## Key concept

The wave relation $v=f\lambda$ applies to sound and light; changing medium changes speed and wavelength but not frequency.

## Worked solution

1. For audible sound, use $\lambda=v_{\rm air}/f$ at the lowest and highest stated frequencies.
2. For visible light, use $f=c/\lambda$ at $400\ \text{nm}$ and $700\ \text{nm}$.
3. For the cavitron, calculate $\lambda=v_{\rm air}/(23\ \text{kHz})$.
4. In bodily fluid use the same frequency with $\lambda=v_{\rm fluid}/f$.

## Why it works

Frequency is fixed by the source; a new medium changes the propagation speed, so wavelength adjusts accordingly.

## Issue signals

- `nanometer-unit-conversion-error`
- `frequency-changes-between-media`

# Problem 15.7

## Key concept

A traveling sinusoidal wave has the form $y=A\cos(kx-\omega t+\phi)$ for motion in $+x$.

## Worked solution

1. Use $f=v/\lambda$, $T=1/f$, and $k=2\pi/\lambda$.
2. The stated direction fixes the minus sign in $kx-\omega t$.
3. Use the condition at $x=0,t=0$ to choose the phase $\phi$ so the displacement is maximum upward.
4. Substitute the requested $x$ and $t$ into the resulting wave function.
5. For the next maximum upward displacement, advance the local phase by $2\pi$ and solve for elapsed time.

## Why it works

Points on the string oscillate with the same angular frequency while their phase varies linearly with position.

## Issue signals

- `traveling-wave-direction-sign-error`
- `wave-number-vs-angular-frequency-confused`

# Problem 15.9

## Key concept

An acceptable traveling-wave function obeys $\partial^2y/\partial x^2=(1/v^2)\partial^2y/\partial t^2$.

## Worked solution

1. For each candidate function, differentiate twice with respect to $x$ and twice with respect to $t$.
2. Check whether the two expressions have the required proportionality and a positive $v^2$.
3. For the valid part-(b) wave, calculate
$$
v_y=\frac{\partial y}{\partial t},\qquad a_y=\frac{\partial^2y}{\partial t^2}.
$$
4. Preserve the chain-rule factors of $\omega$ and $\omega^2$.

## Why it works

The wave equation constrains how spatial curvature and transverse acceleration must be related for a disturbance that propagates at speed $v$.

## Issue signals

- `wave-equation-derivative-error`
- `chain-rule-angular-frequency-error`

# Problem 15.29

## Key concept

For isotropic radiation, intensity follows the inverse-square law $I\propto1/r^2$.

## Worked solution

1. Identify the two distances from the star and the supplied intensity at one distance.
2. Use
$$
\frac{I_2}{I_1}=\left(\frac{r_1}{r_2}\right)^2.
$$
3. Solve for the requested intensity or distance, keeping units consistent.

## Why it works

The same emitted power spreads over spherical surfaces whose areas grow as $4\pi r^2$.

## Issue signals

- `inverse-square-ratio-error`
- `distance-unit-conversion-error`

# Problem 15.45

## Key concept

Average power transported by a sinusoidal wave on a string is proportional to $\mu\omega^2A^2v$.

## Worked solution

1. Take the wave parameters and string properties from the referenced exercise.
2. Calculate angular frequency $\omega=2\pi f$ and wave speed $v=\sqrt{F_T/\mu}$ when needed.
3. Substitute into
$$
P_{\rm avg}=\frac12\mu\omega^2A^2v.
$$
4. Apply any requested change in amplitude, frequency, or tension through the corresponding power-law factor.

## Why it works

The wave carries energy in both the moving string elements and the stretched string, and the average energy flow depends quadratically on amplitude and frequency.

## Issue signals

- `wave-power-amplitude-dependence-error`
- `angular-frequency-factor-error`

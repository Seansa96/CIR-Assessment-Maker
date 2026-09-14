# Young & Freedman University Physics — Chapter 16 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry matches a selected Chapter 16 prompt. Consult the companion question note for original figures and full numerical notation.

# Problem 16.1

## Key concept

For a plane sound wave, pressure amplitude and displacement amplitude are related by $\Delta p_{\max}=Bks_{\max}=\rho v\omega s_{\max}$.

## Worked solution

1. Take the sound speed, frequency, and displacement amplitude from the referenced example.
2. Calculate $\omega=2\pi f$.
3. Use $\Delta p_{\max}=\rho v\omega s_{\max}$ with air density at the stated conditions.
4. Compare the result with the pressure reference given in the question.

## Why it works

Compression and rarefaction change pressure in proportion to the spatial gradient of the medium's displacement.

## Issue signals

- `sound-pressure-amplitude-formula-error`
- `angular-frequency-factor-error`

# Problem 16.3

## Key concept

At fixed displacement amplitude, sound pressure amplitude is proportional to frequency.

## Worked solution

1. Convert $0.0200\ \text{mm}$ to meters.
2. For each frequency, calculate $\omega=2\pi f$.
3. Use $\Delta p_{\max}=\rho v\omega s_{\max}$.
4. Compare each pressure amplitude with $30\ \text{Pa}$, the pain threshold.

## Why it works

At higher frequency the air elements reverse direction more rapidly, producing stronger pressure variations for the same displacement amplitude.

## Issue signals

- `millimeter-to-meter-conversion-error`
- `sound-pressure-frequency-dependence-error`

# Problem 16.5

## Key concept

The wavelength of a sound wave in a specified medium is $\lambda=v/f$.

## Worked solution

1. For whale sound, use $\lambda=v_{\rm seawater}/(17\ \text{Hz})$.
2. For the dolphin part, identify its stated frequency and propagation medium.
3. Apply $\lambda=v/f$ after converting all quantities to SI units.
4. Explain the physical scale using the resulting wavelength.

## Why it works

Frequency is set by the animal's source; the speed is controlled by the medium, so their quotient gives wavelength.

## Issue signals

- `wave-speed-frequency-wavelength-error`
- `medium-speed-misidentified`

# Problem 16.7

## Key concept

Simultaneous arrival means the sound-travel times through air and water are equal.

## Worked solution

1. Calculate the friend's straight-line air distance from the horn using the horizontal separation and horn height in the figure.
2. Find air travel time $t=d_{\rm air}/v_{\rm air}$.
3. The diver's total path includes the horn's height above water plus the unknown depth below water.
4. Set $(h_{\rm air}+d_{\rm water})/v_{\rm water}=t$ and solve for $d_{\rm water}$.

## Why it works

The different sound speeds are accommodated by different distances when the two sounds reach their listeners at the same instant.

## Issue signals

- `simultaneous-travel-time-equation-error`
- `air-and-water-paths-confused`

# Problem 16.9

## Key concept

In an ideal gas, sound speed is proportional to $\sqrt{T}$, and wavelength is $\lambda=v/f$ for a fixed oscillator frequency.

## Worked solution

1. The target wavelength sets target sound speed: $v_2=f\lambda_2$.
2. Use the initial speed and initial absolute temperature in
$$
\frac{v_2}{v_1}=\sqrt{\frac{T_2}{T_1}}.
$$
3. Solve $T_2=T_1(v_2/v_1)^2$.
4. Convert the final kelvin temperature to Celsius if requested.

## Why it works

Raising an ideal gas's temperature increases molecular thermal speed and the speed at which compressions propagate.

## Issue signals

- `celsius-used-in-temperature-ratio`
- `sound-speed-temperature-square-error`

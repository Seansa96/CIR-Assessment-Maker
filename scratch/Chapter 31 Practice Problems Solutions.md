# Young & Freedman University Physics — Chapter 31 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading corresponds exactly to a selected Chapter 31 prompt. Refer to the companion note for circuit diagrams.

# Problem 31.1

## Key concept

For sinusoidal current, $I_{\rm rms}=I_0/\sqrt2$.

## Worked solution

1. The delicate filament limit applies to instantaneous current, so set peak current $I_0=1.50\ \text{A}$.
2. Calculate
$$
I_{\rm rms}=\frac{1.50\ \text{A}}{\sqrt2}.
$$
3. Do not use $1.50\ \text{A}$ as the rms value, since peak current would then exceed the safe limit.

## Why it works

Rms current is the equivalent heating current, while instantaneous sinusoidal current reaches a larger peak value each cycle.

## Issue signals

- `rms-vs-peak-current-confused`
- `sinusoid-square-root-two-factor-error`

# Problem 31.3

## Key concept

For $v(t)=V_0\sin\omega t$, rms voltage is $V_{\rm rms}=V_0/\sqrt2$ and the signed average over a complete cycle is zero.

## Worked solution

1. Insert the stated voltage amplitude into $V_{\rm rms}=V_0/\sqrt2$.
2. Average $V_0\sin\omega t$ over any complete period; positive and negative halves cancel.
3. Report average potential difference as zero.

## Why it works

The sinusoidal waveform is symmetric about zero, but squaring it for heating calculations gives a positive nonzero rms value.

## Issue signals

- `rms-vs-average-voltage-confused`
- `sinusoid-square-root-two-factor-error`

# Problem 31.5

## Key concept

In a pure inductor, voltage leads current by $90^\circ$, and $V_0=I_0X_L=I_0\omega L$.

## Worked solution

1. State phase relation: source voltage leads current by $90^\circ$.
2. Use the given inductance, voltage amplitude, and frequency to calculate $X_L=\omega L$.
3. Solve current amplitude $I_0=V_0/X_L$ or solve the requested parameter from the same relation.

## Why it works

An inductor’s voltage is proportional to the time derivative of current, which shifts a sinusoid one quarter cycle ahead.

## Issue signals

- `inductor-phase-lead-lag-error`
- `inductive-reactance-frequency-error`

# Problem 31.7

## Key concept

For a pure capacitor, $I_0=V_0/X_C=\omega CV_0$.

## Worked solution

1. Calculate angular frequency $\omega=2\pi(60.0\ \text{Hz})$.
2. Rearrange:
$$
C=\frac{I_0}{\omega V_0}.
$$
3. Insert the stated voltage and desired current amplitudes.

## Why it works

Capacitive current is proportional to the rate of voltage change, which rises with frequency and capacitance.

## Issue signals

- `capacitive-reactance-ratio-inverted`
- `frequency-to-angular-frequency-error`

# Problem 31.9

## Key concept

Inductive and capacitive reactances are $X_L=\omega L$ and $X_C=1/(\omega C)$.

## Worked solution

1. Calculate $\omega=2\pi(80.0\ \text{Hz})$.
2. For part (a), evaluate $X_L=\omega(3.00\ \text{H})$.
3. For part (b), rearrange $L=X_L/\omega$.
4. For part (c), use $X_C=1/(\omega C)$ with the stated capacitance.
5. For part (d), rearrange $C=1/(\omega X_C)$.

## Why it works

Inductors oppose current changes more strongly at high frequency, whereas capacitors offer less opposition at high frequency.

## Issue signals

- `inductive-capacitive-reactance-confused`
- `frequency-to-angular-frequency-error`

# Problem 31.41

## Key concept

Series resonance occurs at $\omega_0=1/\sqrt{LC}$.

## Worked solution

1. Calculate capacitor area $A=(0.0450\ \text{m})^2$ and capacitance $C=\epsilon_0A/d$.
2. Calculate solenoid area and turn number from its geometry and turns-per-centimeter density.
3. Use solenoid inductance $L=\mu_0N^2A/\ell$.
4. Substitute into $\omega_0=1/\sqrt{LC}$.

## Why it works

At resonance, inductive and capacitive reactances have equal magnitude and opposite phase, so they cancel in a series circuit.

## Issue signals

- `resonance-frequency-lc-inverse-error`
- `solenoid-turn-density-conversion-error`

# Problem 31.51

## Key concept

For a series L-R-C circuit, the output across the L-R combination is found from the magnitude ratio of its impedance to total impedance.

## Worked solution

1. Write output impedance magnitude:
$$
|Z_{LR}|=\sqrt{R^2+(\omega L)^2}.
$$
2. Write total series impedance:
$$
|Z|=\sqrt{R^2+\left(\omega L-\frac1{\omega C}\right)^2}.
$$
3. Therefore
$$
\frac{V_{\rm out}}{V_s}=\frac{|Z_{LR}|}{|Z|}.
$$
4. At small $\omega$, use $X_C\gg R,X_L$ to show the ratio is proportional to $\omega$.
5. At large $\omega$, $X_L$ dominates both numerator and denominator, so the ratio approaches $1$.

## Why it works

At low frequency the capacitor blocks most of the source voltage; at high frequency its reactance becomes negligible and nearly all voltage appears across the L-R output branch.

## Issue signals

- `ac-impedance-magnitude-error`
- `high-pass-limit-analysis-error`

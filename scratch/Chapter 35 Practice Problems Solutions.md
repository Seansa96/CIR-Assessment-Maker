# Young & Freedman University Physics — Chapter 35 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading matches exactly one selected Chapter 35 prompt. Refer to the companion note for diagrams.

# Problem 35.1

## Key concept

For two in-phase sources, constructive interference occurs at path difference $\Delta r=m\lambda$ and cancellation at $\Delta r=(m+\tfrac12)\lambda$.

## Worked solution

1. Use the geometry in the figure: $r_B=1.50\ \text{m}$ and express $r_A$ from speaker separation and walker coordinate $x$.
2. Form $\Delta r=|r_A-r_B|$.
3. Set $\Delta r=m(0.340\ \text{m})$ for maxima and solve for allowed $x$ values.
4. Set $\Delta r=(m+\tfrac12)(0.340\ \text{m})$ for minima and retain only values in the stated range.

## Why it works

The two coherent speaker waves arrive in phase for whole-wavelength path differences and out of phase for half-integer differences.

## Issue signals

- `two-source-path-difference-error`
- `constructive-destructive-condition-confused`

# Problem 35.3

## Key concept

Interference intensity follows $I=I_1+I_2+2\sqrt{I_1I_2}\cos\phi$.

## Worked solution

1. Identify the two supplied source intensities and their phase difference or path difference.
2. Convert a path difference to phase using $\phi=2\pi\Delta r/\lambda$ when needed.
3. Substitute into the intensity formula.
4. Check limiting cases: in-phase gives $(\sqrt{I_1}+\sqrt{I_2})^2$ and opposite phase gives $(\sqrt{I_1}-\sqrt{I_2})^2$.

## Why it works

Electric-field amplitudes, not intensities, superpose; squaring the resulting amplitude produces the interference term.

## Issue signals

- `intensities-added-without-interference-term`
- `path-difference-to-phase-error`

# Problem 35.5

## Key concept

For in-phase antennas on the same line, constructive interference requires an integer-wavelength path difference.

## Worked solution

1. Compute wavelength $\lambda=c/(120\ \text{MHz})$.
2. Use the point’s location between the antennas to write its two path lengths in terms of $x$.
3. Their difference is the difference of those distances.
4. Set $\Delta r=m\lambda$ and retain solutions that lie between the antennas.

## Why it works

In-phase transmitters reinforce when their propagation phases differ by an integer multiple of $2\pi$.

## Issue signals

- `radio-wavelength-frequency-error`
- `two-source-path-difference-error`

# Problem 35.7

## Key concept

The observer’s sound level follows constructive or destructive interference from the two in-phase speakers.

## Worked solution

1. Use the figure to calculate path lengths from each speaker to the observer.
2. Find $\Delta r=|r_1-r_2|$.
3. Compare $\Delta r$ to $m\lambda$ and $(m+\tfrac12)\lambda$ for $\lambda=2.0\ \text{m}$.
4. State whether the sound is reinforced, canceled, or intermediate; calculate phase and intensity if the prompt asks.

## Why it works

Sound waves from coherent in-phase speakers superpose according to their travel-phase difference at the listener.

## Issue signals

- `two-source-path-difference-error`
- `constructive-destructive-condition-confused`

# Problem 35.9

## Key concept

For double-slit bright fringes at small angle, $y_m=m\lambda L/d$.

## Worked solution

1. Use fringe order $m=20$, distance $L=1.20\ \text{m}$, and measured position $y_{20}=10.6\ \text{mm}$.
2. Use helium wavelength supplied by the problem context or reference data.
3. Rearrange:
$$
d=\frac{m\lambda L}{y_m}.
$$
4. Convert the final separation to an appropriate small-length unit.

## Why it works

Each successive bright fringe corresponds to one additional wavelength of path difference between the two slit waves.

## Issue signals

- `double-slit-fringe-order-error`
- `millimeter-to-meter-conversion-error`

# Problem 35.51

## Key concept

Reflected thin-film interference depends on both optical path $2nt$ and phase reversals at interfaces.

## Worked solution

1. Compare indices: reflection from air to film ($1\to1.750$) undergoes a $\pi$ phase reversal; reflection from film to glass ($1.750\to1.50$) does not.
2. There is one phase reversal, so reflected constructive interference occurs when
$$
2nt=\left(m+\frac12\right)\lambda_0.
$$
3. Use the “just thick enough” condition to choose the smallest positive integer order.
4. Apply the temperature-change data and the film’s thermal expansion relationship to find the requested changed thickness, wavelength, or temperature condition.

## Why it works

The path phase acquired inside the film combines with interface phase changes, so the interference condition differs from the no-phase-reversal case.

## Issue signals

- `thin-film-phase-reversal-count-error`
- `optical-path-index-factor-error`

# Problem 35.53

## Key concept

The intensity of two equal-amplitude waves depends on their phase difference as $I=4I_0\cos^2(\phi/2)$.

## Worked solution

1. Start with the given two-slit intensity expression.
2. Identify $\phi$ as the phase difference and express it in terms of path difference or angle when requested.
3. Use maxima at $\phi=2m\pi$ and minima at $\phi=(2m+1)\pi$.
4. Apply the supplied intensity fractions to solve the required phase or angular condition.

## Why it works

Adding two equal sinusoidal fields yields a resultant amplitude proportional to $\cos(\phi/2)$; intensity is its square.

## Issue signals

- `two-wave-intensity-phase-factor-error`
- `constructive-destructive-phase-condition-error`

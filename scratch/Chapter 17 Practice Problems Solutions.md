# Young & Freedman University Physics — Chapter 17 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry corresponds exactly to a selected Chapter 17 prompt.

# Problem 17.1

## Key concept

Convert Celsius to Fahrenheit with $T_F=\tfrac95T_C+32$.

## Worked solution

1. For each stated Celsius temperature, multiply by $9/5$.
2. Add $32$ to obtain degrees Fahrenheit.
3. Preserve negative signs before performing the multiplication.

## Why it works

The Celsius and Fahrenheit scales have different zero points and different degree sizes, requiring both a scale factor and offset.

## Issue signals

- `celsius-fahrenheit-offset-omitted`
- `temperature-conversion-factor-inverted`

# Problem 17.3

## Key concept

Temperature changes convert by $\Delta T_C=\tfrac59\Delta T_F$; no $32^\circ$ offset is used for a difference.

## Worked solution

1. Subtract initial from final Fahrenheit temperature for each event.
2. Convert each change using $\Delta T_C=\tfrac59\Delta T_F$.
3. Retain the sign: warming is positive and cooling is negative.

## Why it works

The two scales differ only in degree size when comparing intervals; their arbitrary zero locations cancel.

## Issue signals

- `temperature-difference-offset-added`
- `temperature-change-sign-error`

# Problem 17.5

## Key concept

A change of one kelvin has the same size as a change of one Celsius degree, while Fahrenheit differences use a factor of $9/5$.

## Worked solution

1. The stated cooling is $\Delta T=-10.0\ \text{K}$.
2. Therefore $\Delta T=-10.0\ ^\circ\text{C}$.
3. Convert the interval: $\Delta T_F=\tfrac95(-10.0\ ^\circ\text{C})$.

## Why it works

Kelvin and Celsius scales have identically sized increments even though their zero values differ.

## Issue signals

- `kelvin-celsius-difference-confused`
- `temperature-change-sign-error`

# Problem 17.7

## Key concept

At constant volume for an ideal gas, pressure is proportional to absolute temperature: $p/T=\text{constant}$.

## Worked solution

1. Convert the initial triple-point temperature and final freezing temperature to kelvins.
2. Write
$$
p_2=p_1\frac{T_2}{T_1}.
$$
3. Insert the stated $1.35\ \text{atm}$ and report the resulting pressure.

## Why it works

At fixed volume, cooling reduces molecular collision momentum and rate in direct proportion to absolute temperature.

## Issue signals

- `celsius-used-in-gas-law-ratio`
- `constant-volume-gas-law-error`

# Problem 17.9

## Key concept

A constant-volume gas thermometer extrapolates a linear pressure-temperature relation to estimate absolute zero.

## Worked solution

1. Use the triple-point and boiling-point pairs $(T_C,p)$ to calculate the line slope $\Delta p/\Delta T_C$.
2. Write the line equation and set $p=0$ to find the extrapolated Celsius temperature.
3. For the ideal-gas comparison, use $p/T=\text{constant}$ with kelvin temperatures.
4. Compare the predicted value with the measured relation and state whether the gas obeys it precisely.

## Why it works

An ideal gas has pressure directly proportional to absolute temperature at fixed volume; real gases only approach that behavior at low density.

## Issue signals

- `linear-extrapolation-slope-error`
- `celsius-used-in-gas-law-ratio`

# Problem 17.19

## Key concept

Overflow equals the liquid's volume expansion minus the flask's volume expansion.

## Worked solution

1. Let $V_0$ be the stated initial flask volume and calculate $\Delta T$.
2. Mercury expansion is $\Delta V_{Hg}=\beta_{Hg}V_0\Delta T$.
3. Flask expansion makes additional room $\Delta V_g=\beta_gV_0\Delta T$.
4. Set the observed overflow to $\Delta V_{Hg}-\Delta V_g$ and solve for $\beta_g$.

## Why it works

The mercury overflows only by the amount its expansion exceeds the simultaneous expansion of the container.

## Issue signals

- `container-expansion-omitted`
- `volume-expansion-sign-error`

# Problem 17.27

## Key concept

When both kettle and water change temperature with no heat loss, total heat is the sum $Q=mc\Delta T$ for each.

## Worked solution

1. Calculate the common temperature rise $\Delta T$.
2. Write
$$
Q=m_{Al}c_{Al}\Delta T+m_w c_w\Delta T.
$$
3. Substitute the two masses and appropriate specific heats.
4. Factor $\Delta T$ as a check on units.

## Why it works

Both materials reach the same final temperature, but each stores heat according to its own mass and specific heat.

## Issue signals

- `kettle-heat-capacity-omitted`
- `specific-heat-unit-error`

# Problem 17.55

## Key concept

The available boiling energy is a stated fraction of impact kinetic energy, and vaporization requires heating water to $100^\circ\text{C}$ plus latent heat.

## Worked solution

1. Calculate asteroid kinetic energy $K=\tfrac12Mv^2$ and take $0.0100K$.
2. For each kilogram of initial water, calculate
$$
q=c_w(100^\circ\text{C}-T_i)+L_v.
$$
3. Divide the available energy by $q$ to get the boiled-water mass.
4. Compare with the given reference water mass if requested.

## Why it works

Energy is first needed to warm liquid water to its boiling point; the much larger latent heat then changes phase without further temperature rise.

## Issue signals

- `impact-energy-fraction-error`
- `latent-heat-omitted`

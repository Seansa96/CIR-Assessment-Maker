# Young & Freedman University Physics — Chapter 18 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry matches exactly one selected Chapter 18 prompt.

# Problem 18.1

## Key concept

The ideal gas law is $pV=nRT$, and moles can be obtained from $n=m/M$.

## Worked solution

1. Convert the helium mass and molar mass to consistent units, then calculate $n=m/M$.
2. Convert the tank volume from liters to cubic meters and temperature to kelvins.
3. Use $p=nRT/V$ to calculate pressure in pascals.
4. Divide by $1.01325\times10^5\ \text{Pa/atm}$ for atmospheres.

## Why it works

The ideal gas law connects the amount of gas, its absolute temperature, its volume, and the momentum-transfer pressure it produces.

## Issue signals

- `liter-to-cubic-meter-conversion-error`
- `kelvin-temperature-omitted`

# Problem 18.3

## Key concept

At constant temperature and amount of gas, Boyle's law gives $p_1V_1=p_2V_2$.

## Worked solution

1. Record the initial pressure and the two stated volumes.
2. Rearrange Boyle's law:
$$
p_2=p_1\frac{V_1}{V_2}.
$$
3. Substitute the values and report the final pressure in the requested units.

## Why it works

Doubling the available volume at fixed temperature halves the molecular collision rate per unit area, and hence halves pressure.

## Issue signals

- `boyles-law-ratio-inverted`
- `constant-temperature-condition-missed`

# Problem 18.5

## Key concept

For an ideal gas, density is $\rho=pM/(RT)$.

## Worked solution

1. Identify each atmosphere's predominant gas and obtain its molar mass $M$ from the periodic table.
2. Convert each pressure to pascals and use each stated temperature in kelvins.
3. Calculate $\rho=pM/(RT)$ separately for Mars, Venus, and Titan.
4. Compare the results with $1.20\ \text{kg/m}^3$ for Earth's air.

## Why it works

At the same temperature, higher pressure or higher molar mass means more mass per unit volume; higher temperature decreases density.

## Issue signals

- `molar-mass-unit-error`
- `kelvin-temperature-omitted`

# Problem 18.7

## Key concept

For a fixed amount of ideal gas, $pV/T$ is constant; gauge pressure must first be converted to absolute pressure.

## Worked solution

1. Use $p_{2,\rm abs}=p_{2,\rm gauge}+p_{\rm atm}$.
2. Convert the initial temperature to kelvins.
3. Rearrange the combined gas law:
$$
T_2=T_1\frac{p_2V_2}{p_1V_1}.
$$
4. Substitute the given cylinder volumes and pressures, then convert back to Celsius if requested.

## Why it works

The gas law requires absolute pressure because gas pressure is proportional to molecular collision activity above vacuum, not above atmospheric pressure.

## Issue signals

- `gauge-pressure-used-as-absolute`
- `kelvin-temperature-omitted`

# Problem 18.9

## Key concept

The combined gas law relates two equilibrium states of the same sealed amount of gas.

## Worked solution

1. Convert both stated temperatures to kelvins and all volumes to a common unit.
2. Use
$$
\frac{p_1V_1}{T_1}=\frac{p_2V_2}{T_2}.
$$
3. Solve:
$$
p_2=p_1\frac{V_1T_2}{V_2T_1}.
$$
4. Keep the pressure absolute because the initial pressure is specified as absolute.

## Why it works

Compressing the gas raises collision rate, while heating raises molecular speeds; the combined law accounts for both effects.

## Issue signals

- `combined-gas-law-ratio-error`
- `celsius-used-in-gas-law-ratio`

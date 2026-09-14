# Young & Freedman University Physics — Chapter 19 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry matches exactly one selected Chapter 19 prompt. Use the companion note for the original pV diagrams.

# Problem 19.1

## Key concept

For an isobaric ideal-gas process, $V\propto T$ and the work done by the gas is $W=p\Delta V=nR\Delta T$.

## Worked solution

1. Sketch a horizontal line on a $pV$ diagram because pressure stays constant; volume increases as temperature rises.
2. Convert both temperatures to kelvins only if calculating a ratio; their difference may be used in kelvins directly.
3. Calculate $W=nR(T_f-T_i)$ for $n=2.00\ \text{mol}$.
4. Report positive work because the gas expands.

## Why it works

At constant pressure, the area under the horizontal pV path is $p\Delta V$, and the ideal gas law converts that directly to $nR\Delta T$.

## Issue signals

- `isobaric-work-formula-error`
- `temperature-difference-conversion-error`

# Problem 19.3

## Key concept

For a quasistatic process, work is the signed area under the $pV$ curve: $W=\int p\,dV$.

## Worked solution

1. Write the pressure as the supplied function of volume.
2. Set the integration limits from the initial volume to the final volume.
3. Evaluate $W_{\rm by}=\int_{V_i}^{V_f}p(V)\,dV$.
4. For compression, the result for work done by the gas is negative; reverse the sign if the question asks work done on the gas.

## Why it works

Each infinitesimal volume change contributes $p\,dV$ of boundary work, and integration sums those contributions along the path.

## Issue signals

- `work-on-vs-work-by-sign-error`
- `pV-integral-limit-error`

# Problem 19.5

## Key concept

For an isothermal ideal-gas process, $W_{\rm by}=nRT\ln(V_f/V_i)=nRT\ln(p_i/p_f)$.

## Worked solution

1. Since $468\ \text{J}$ is done on the gas, set $W_{\rm by}=-468\ \text{J}$.
2. Use
$$
W_{\rm by}=nRT\ln\!\left(\frac{p_i}{p_f}\right).
$$
3. Solve for $p_i=p_f\exp[W_{\rm by}/(nRT)]$.
4. Sketch an isotherm curving downward to the right; the compression path runs toward smaller volume and higher pressure.

## Why it works

At fixed temperature, ideal-gas internal energy is unchanged, and $pV$ remains constant along the hyperbolic isotherm.

## Issue signals

- `isothermal-logarithm-ratio-error`
- `work-on-vs-work-by-sign-error`

# Problem 19.7

## Key concept

Net work in a cyclic pV process equals the signed area enclosed by its loop.

## Worked solution

1. Trace the loop in its indicated direction.
2. Calculate the enclosed geometric area, or add work from each path segment.
3. Assign positive net work for a clockwise loop and negative net work for a counterclockwise loop.
4. Because initial and final states match, note that $\Delta U=0$ and net heat equals net work.

## Why it works

The path dependence of work leaves the enclosed area after all expansion and compression contributions are combined.

## Issue signals

- `cyclic-work-area-sign-error`
- `state-function-vs-path-function-confused`

# Problem 19.9

## Key concept

At constant pressure, $W_{\rm by}=p\Delta V$; the first law is $\Delta U=Q-W_{\rm by}$.

## Worked solution

1. Calculate the expansion work:
$$
W_{\rm by}=(1.65\times10^5\ \text{Pa})(0.320-0.110\ \text{m}^3).
$$
2. Use the supplied heat input in $\Delta U=Q-W_{\rm by}$.
3. State that the first law applies to any system, so ideal-gas behavior is not needed for these two calculations.

## Why it works

Work depends on the given pressure-volume path and the first law is the general conservation-of-energy statement for thermodynamic systems.

## Issue signals

- `constant-pressure-work-error`
- `first-law-sign-error`

# Problem 19.57

## Key concept

The reaction heat raises the chemicals' temperature and supplies their spray kinetic energy.

## Worked solution

1. Calculate thermal energy per unit mass with $q_{\rm thermal}=c_w(T_f-T_i)$.
2. Calculate kinetic energy per unit mass with $q_{\rm kinetic}=\tfrac12v^2$.
3. Add the terms:
$$
q_{\rm reaction}=c_w\Delta T+\frac12v^2.
$$
4. Convert the result to the requested energy-per-mass units.

## Why it works

Energy released by the chemical reaction is partitioned into internal (thermal) energy and organized kinetic energy of the expelled spray.

## Issue signals

- `specific-heat-temperature-change-error`
- `kinetic-energy-per-mass-error`

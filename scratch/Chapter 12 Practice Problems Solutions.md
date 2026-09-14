# Young & Freedman University Physics — Chapter 12 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading corresponds exactly to the answer-key-backed Chapter 12 problem note. Refer to the companion prompt note for its preserved figures.

# Problem 12.1

## Key concept

A cylindrical rod has volume $V=\pi(d/2)^2L$, and its mass is density times volume.

## Worked solution

1. Convert the given length and diameter to meters.
2. Calculate the rod volume with $V=\pi(d/2)^2L$.
3. Use the tabulated density of iron and evaluate $m=\rho V$.
4. If weight is requested, multiply the mass by $g$.

## Why it works

Density is mass per unit volume, so a material's density determines the mass of an object once its geometry is known.

## Issue signals

- `diameter-used-as-radius`
- `length-unit-conversion-error`

# Problem 12.3

## Key concept

Average density is $\rho=m/V$; compare the calculated value with the reference density of gold.

## Worked solution

1. Convert each stated rectangular dimension to consistent units.
2. Calculate $V=\ell wh$.
3. Divide the stated mass by that volume.
4. Compare the result to the tabulated density of pure gold and state whether the claimed material is plausible.

## Why it works

For a homogeneous sample, density is an intrinsic material property independent of the sample's size.

## Issue signals

- `rectangular-volume-error`
- `mass-unit-conversion-error`

# Problem 12.5

## Key concept

Equal masses of different-density spheres have volumes inversely proportional to density.

## Worked solution

1. Set the common mass equal in $m=\rho(4\pi r^3/3)$ for aluminum and lead.
2. Cancel the common factors.
3. Solve

$$
\frac{r_{\rm Al}}{r_{\rm Pb}}=
\left(\frac{\rho_{\rm Pb}}{\rho_{\rm Al}}\right)^{1/3}.
$$

4. Insert the table densities.

## Why it works

A lower-density material needs a larger volume, and thus a larger radius, to contain the same mass.

## Issue signals

- `density-ratio-inverted`
- `radius-volume-power-error`

# Problem 12.7

## Key concept

The material volume of a hollow pipe is the outer-cylinder volume minus the inner-cylinder volume.

## Worked solution

1. Convert the given diameters to radii in meters.
2. Evaluate

$$
V=\pi L(R_{\rm out}^2-R_{\rm in}^2).
$$

3. Use $m=\rho_{\rm Cu}V$.
4. Convert to weight with $W=mg$ if the question asks how much the pipe weighs.

## Why it works

The empty cylindrical core displaces no copper, so it must be removed from the outer geometric volume.

## Issue signals

- `inner-volume-not-subtracted`
- `diameter-used-as-radius`

# Problem 12.9

## Key concept

The gauge pressure at depth is $p_g=\rho gh$.

## Worked solution

1. Convert $0.500\ \text{km}$ to meters and use Martian $g$ for the former Martian ocean.
2. Compute $p_g=\rho_{\rm fresh}g_{\rm Mars}h$.
3. Set this equal to Earth's ocean gauge pressure, $\rho_{\rm ocean}g_{\rm Earth}h_{\rm Earth}$.
4. Solve for the equivalent Earth depth.

## Why it works

Hydrostatic pressure depends only on the weight per unit area of the fluid column above the point.

## Issue signals

- `gauge-and-absolute-pressure-confused`
- `depth-unit-conversion-error`

# Problem 12.17

## Key concept

For a snorkeler, atmospheric pressure inside the lungs is lower than the outside water pressure by $\rho gh$.

## Worked solution

1. Use freshwater density and the stated lung depth.
2. Evaluate

$$
\Delta p=p_{\rm outside}-p_{\rm inside}=\rho gh.
$$

3. Report the pressure difference in pascals and, if helpful, in atmospheres.

## Why it works

The open snorkel keeps the lung air at surface atmospheric pressure while the surrounding water pressure rises with depth.

## Issue signals

- `gauge-and-absolute-pressure-confused`
- `hydrostatic-pressure-formula-error`

# Problem 12.19

## Key concept

The pressure difference across the hatch produces an upward fluid force $\Delta pA$ that must be overcome along with the hatch weight.

## Worked solution

1. Find the outside ocean pressure at $30\ \text{m}$: $p_{\rm out}=p_{\rm atm}+\rho gh$.
2. Use $p_{\rm in}=1.0\ \text{atm}$ and calculate $\Delta p=p_{\rm out}-p_{\rm in}$.
3. The upward water force is $F_p=\Delta pA$.
4. The required downward push is the pressure force minus the hatch's downward weight, using the direction shown in the problem.

## Why it works

Pressure acts normal to each side of the hatch; only the pressure difference creates an unbalanced fluid force.

## Issue signals

- `pressure-difference-area-force-error`
- `hatch-weight-direction-error`

# Problem 12.27

## Key concept

The loss of apparent weight in water is the buoyant force, equal to the weight of displaced water.

## Worked solution

1. Calculate $F_B=17.50\ \text{N}-11.20\ \text{N}$.
2. Use $F_B=\rho_{\rm water}gV$ to find the sample volume.
3. Its mass is $m=W_{\rm air}/g$.
4. Calculate the density $\rho_{\rm sample}=m/V$.

## Why it works

Archimedes' principle equates the buoyant force to the weight of the fluid the fully submerged sample displaces.

## Issue signals

- `buoyant-force-sign-error`
- `apparent-weight-treated-as-mass`

# Problem 12.43

## Key concept

For a jet that rises to height $h$, its launch kinetic energy per unit mass is $v^2/2=gh$.

## Worked solution

1. At the top of the stream, take the water speed and gauge pressure as zero.
2. Apply Bernoulli's equation between the large main and the top of the jet; the main speed is negligible.
3. The required gauge pressure is

$$
p_g=\rho gh.
$$

4. Substitute $h=15.0\ \text{m}$.

## Why it works

The pressure energy in the main is transformed into gravitational potential energy of the rising water stream.

## Issue signals

- `bernoulli-height-term-omitted`
- `gauge-and-absolute-pressure-confused`

# Problem 12.45

## Key concept

Continuity gives $A_1v_1=A_2v_2$, and Bernoulli's equation relates the resulting speed change to pressure.

## Worked solution

1. Because $A_2=2A_1$, use continuity to get $v_2=v_1/2$.
2. The pipeline is horizontal, so set

$$
p_1+\frac12\rho v_1^2=p_2+\frac12\rho v_2^2.
$$

3. Solve for $p_2$ and keep gauge pressures throughout.

## Why it works

In a horizontal ideal flow, a lower speed corresponds to a higher pressure.

## Issue signals

- `continuity-ratio-inverted`
- `bernoulli-velocity-term-sign-error`

# Problem 12.47

## Key concept

Flow rate fixes speed through $Q=Av$, while Bernoulli's equation predicts the lower pressure at a constriction.

## Worked solution

1. Convert the stated discharge rate to $\text{m}^3/\text{s}$.
2. Calculate $v_1=Q/(\pi r_1^2)$ and $v_2=Q/(\pi r_2^2)$.
3. For the horizontal pipe, use

$$
p_2=p_1+\frac12\rho(v_1^2-v_2^2).
$$

4. Report the resulting absolute pressure because the given pressure is absolute.

## Why it works

The smaller radius requires faster flow, and that extra kinetic-energy density comes from pressure energy.

## Issue signals

- `flow-rate-area-speed-error`
- `absolute-and-gauge-pressure-confused`

# Problem 12.61

## Key concept

At the sink threshold, the barge displaces its maximum freshwater volume, and its cargo capacity is the maximum buoyant mass minus the barge's steel mass.

## Worked solution

1. From the figure, calculate the maximum displaced volume from the outside dimensions at the waterline.
2. The supported total mass is $m_{\rm disp}=\rho_{\rm water}V_{\rm disp}$.
3. Calculate the volume of steel plates (bottom plus four sides, using the stated thickness) and their mass from steel density.
4. Subtract steel mass from supported mass to get the coal capacity; compare the coal volume at its density with the barge's interior volume.

## Why it works

Floating equilibrium requires the boat-plus-cargo weight to equal the weight of displaced water.

## Issue signals

- `displaced-volume-misidentified`
- `plate-thickness-volume-error`

# Problem 12.65

## Key concept

For a wood-and-lead composite just submerged, total weight equals the buoyant force from the total displaced volume.

## Worked solution

1. Calculate the wood volume $V_w=(0.600)(0.250)(0.080)$ and mass $m_w=\rho_wV_w$.
2. Let $V_\ell$ be the required lead volume, so lead mass is $\rho_\ell V_\ell$.
3. At the sinking threshold write

$$
\rho_wV_w+\rho_\ell V_\ell=\rho_{\rm water}(V_w+V_\ell).
$$

4. Solve for $V_\ell$.

## Why it works

At complete submersion, both the wood and lead occupy displaced-water volume while their combined weight must exactly equal the buoyant force.

## Issue signals

- `buoyant-volume-omitted`
- `density-balance-equation-error`

# Problem 12.81

## Key concept

Moving the anchor from the barge to the water changes the barge displacement by the difference between the anchor's weight and its buoyant force.

## Worked solution

1. On deck, the anchor increases barge displacement by its full mass, $m$.
2. Suspended underwater, it transmits its apparent weight $mg-F_B$ to the barge through the rope.
3. Calculate $F_B=\rho_{\rm water}g(m/\rho_{\rm iron})$.
4. Divide the reduction in supported force, $F_B$, by $\rho_{\rm water}gA_{\rm barge}$ to find the change in draft; use the stated geometry for any water-level change requested.

## Why it works

The water now supports part of the anchor directly, so the barge does not need to displace as much water.

## Issue signals

- `apparent-weight-misunderstood`
- `buoyant-force-area-link-error`

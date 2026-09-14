# Young & Freedman University Physics — Chapter 11 Practice Problems Solutions

> [!note] Worked-solution companion
> Each heading matches the corresponding answer-key-backed prompt in the Chapter 11 practice note.

# Problem 11.1

## Key concept

The center of gravity is the mass-weighted average position, $x_{\rm cm}=\sum m_ix_i/\sum m_i$.

## Worked solution

1. Set the left end as $x=0$ and the right end as $x=0.500\ \text{m}$.
2. The uniform bar's mass acts at $x=0.250\ \text{m}$.
3. Evaluate

$$
x_{\rm cm}=\frac{(0.055)(0)+(0.120)(0.250)+(0.110)(0.500)}
{0.055+0.120+0.110}.
$$

4. Place the fulcrum directly under that value of $x_{\rm cm}$.

## Why it works

At the center of mass, the total gravitational torque about the support is zero.

## Issue signals

- `uniform-bar-center-misplaced`
- `mass-weighted-average-error`

# Problem 11.3

## Key concept

The desired composite center of gravity fixes the location of the clamp through a mass-weighted average.

## Worked solution

1. The rod's center is at $x=1.00\ \text{m}$.
2. Set the specified composite center to $1.20\ \text{m}$:

$$
(1.80)(1.00)+(2.40)x=(1.80+2.40)(1.20).
$$

3. Solve the linear equation for the clamp's center position $x$.

## Why it works

The numerator of $x_{\rm cm}$ is the sum of each mass times its position.

## Issue signals

- `uniform-rod-center-misplaced`
- `center-of-mass-equation-error`

# Problem 11.5

## Key concept

A rigid body in static equilibrium has both zero net force and zero net torque.

## Worked solution

1. Draw forces on the ladder: its weight at the midpoint, the cable force at its stated point and direction, and the pivot force at $A$.
2. Take torques about $A$ to eliminate the unknown pivot force.
3. Set the signed torque from the cable equal to the signed torque from the ladder weight, using each force's perpendicular lever arm.
4. Use $\sum F_x=0$ and $\sum F_y=0$ to find the pin-force components if requested.

## Why it works

Choosing the pivot as the torque origin removes all forces that act through the pivot from the torque equation.

## Issue signals

- `torque-angle-misidentified`
- `equilibrium-torque-sign-error`

# Problem 11.7

## Key concept

The support forces equal the total weight, and their torque balance determines the motor's location.

## Worked solution

1. Vertical force balance gives the motor weight:

$$
W=400\ \text{N}+600\ \text{N}=1000\ \text{N}.
$$

2. Take torques about the end where the $400\ \text{N}$ force acts.
3. Set $600(2.00)=1000x$ and solve for $x$ from that end.

## Why it works

The two support forces provide counteracting torques that must balance the motor's gravitational torque.

## Issue signals

- `force-balance-omitted`
- `torque-reference-distance-error`

# Problem 11.9

## Key concept

At the breaking threshold, one cable reaches its limiting tension while force and torque equilibrium both remain satisfied.

## Worked solution

1. Let the added weight be $w$ at distance $x$ from cable A.
2. Force balance: $T_A+T_B=350+w$.
3. Torque balance about A: $T_B(1.50)=350(0.750)+wx$.
4. Test the limiting values $T_A\le500.0\ \text{N}$ and $T_B\le400.0\ \text{N}$; choose the placement that lets both limits be reached consistently.

## Why it works

The best placement shares the load as effectively as the cable-strength constraints allow.

## Issue signals

- `cable-tension-constraint-missed`
- `equilibrium-torque-sign-error`

# Problem 11.11

## Key concept

The support forces on a diving board follow directly from static force and torque balance.

## Worked solution

1. Draw the diver's weight at the stated location and the two vertical support forces on the board.
2. Choose either support as the torque origin.
3. Set $\sum\tau=0$ to solve for one support force.
4. Use $\sum F_y=0$ to solve for the other and interpret any negative result as a downward support force.

## Why it works

The supports can exert forces in opposite directions; that is often necessary to keep a board with an overhanging load in equilibrium.

## Issue signals

- `support-force-direction-assumed`
- `equilibrium-torque-sign-error`

# Problem 11.27

## Key concept

Young's modulus is stress divided by strain:

$$
Y=\frac{F/A}{\Delta L/L}=\frac{FL}{A\Delta L}.
$$

## Worked solution

1. Convert the extension $0.20\ \text{cm}$ to meters.
2. Substitute the stated force, original length, cross-sectional area, and extension into $Y=FL/(A\Delta L)$.
3. Report the result in pascals.

## Why it works

Stress measures force per area, while strain is the dimensionless fractional elongation.

## Issue signals

- `extension-unit-conversion-error`
- `stress-and-strain-confused`

# Problem 11.35

## Key concept

Bulk modulus and compressibility are

$$
B=-\frac{\Delta p}{\Delta V/V},\qquad \kappa=\frac1B.
$$

## Worked solution

1. Convert all volume and pressure changes to consistent SI units.
2. Calculate the fractional volume change $\Delta V/V$.
3. Substitute the signed decrease in volume into the bulk-modulus definition, ensuring $B$ is positive.
4. Take the reciprocal for the compressibility.

## Why it works

Materials that change very little in volume for a large pressure increase have a large bulk modulus and small compressibility.

## Issue signals

- `volume-change-sign-error`
- `fractional-volume-change-error`

# Problem 11.39

## Key concept

Breaking stress is the breaking force divided by the wire's cross-sectional area.

## Worked solution

1. Convert the diameter $1.84\ \text{mm}$ to meters and calculate $A=\pi(d/2)^2$.
2. Calculate the tensile stress:

$$
\sigma=\frac{90.8\ \text{N}}{A}.
$$

3. Report the result in pascals, or megapascals when appropriate.

## Why it works

Stress is an intensity: the same force is more damaging when concentrated on a smaller cross-sectional area.

## Issue signals

- `diameter-used-as-radius`
- `area-unit-conversion-error`

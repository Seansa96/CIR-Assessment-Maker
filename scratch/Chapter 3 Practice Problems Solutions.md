# Young & Freedman University Physics - Chapter 3 Practice Problems Solutions

> [!note] Companion solutions
> Original worked-study notes for the paired Chapter 3 prompt set. Results are checked against the textbook's odd-numbered-problem answer appendix.

# Problem 3.1

## Key concept

Average velocity is the displacement vector divided by elapsed time.

## Worked solution

1. Subtract the initial coordinates from the final coordinates to form $\Delta\vec r$.
2. Divide each component by the stated time interval.
3. The average-velocity components are $1.4\ \text{m/s}$ and $-1.3\ \text{m/s}$; its magnitude is $1.9\ \text{m/s}$ at $317^\circ$ from $+x$.

## Why it works

Position vectors subtract componentwise, and direction follows from the signs of the components.

## Issue signals

- `coordinate-subtraction-order`
- `inverse-tangent-quadrant-error`

# Problem 3.3

## Key concept

Differentiate the position vector to obtain instantaneous velocity; use endpoint displacement for average velocity.

## Worked solution

1. Evaluate $[\vec r(t_2)-\vec r(t_1)]/(t_2-t_1)$ for the average velocity.
2. Differentiate each component of $\vec r(t)$ for $\vec v(t)$ and evaluate it at the requested time.
3. The requested velocities are $7.1\ \text{cm/s}$ at $45^\circ$; $5.0\ \text{cm/s}$ at $90^\circ$; $7.1\ \text{cm/s}$ at $45^\circ$; and $11\ \text{cm/s}$ at $27^\circ$ for the listed parts.

## Why it works

The derivative vector is tangent to the trajectory, while the average velocity points along the secant displacement.

## Issue signals

- `average-versus-instantaneous-velocity`
- `component-derivative-error`
- `inverse-tangent-quadrant-error`

# Problem 3.5

## Key concept

Average acceleration is the change in velocity vector divided by the time interval.

## Worked solution

1. Subtract the initial velocity components from the final velocity components.
2. Divide by the stated elapsed time to obtain $a_x=-8.67\ \text{m/s}^2$ and $a_y=-2.33\ \text{m/s}^2$.
3. The acceleration magnitude is $8.98\ \text{m/s}^2$, directed at $195^\circ$ from $+x$.

## Why it works

Acceleration depends on the difference between velocity vectors, not on the difference between their magnitudes.

## Issue signals

- `velocity-magnitudes-subtracted-as-vectors`
- `component-subtraction-order`
- `inverse-tangent-quadrant-error`

# Problem 3.7

## Key concept

For a planar position vector $\vec r(t)=x(t)\hat\imath+y(t)\hat\jmath$, velocity and acceleration are its first and second derivatives.

## Worked solution

1. Differentiate the supplied component functions: $\vec v=a\hat\imath-2bt\hat\jmath$ and $\vec a=-2b\hat\jmath$.
2. Evaluate at the requested time and use $\sqrt{v_x^2+v_y^2}$ for speed.
3. The listed results include $5.4\ \text{m/s}$ at $297^\circ$, $2.4\ \text{m/s}^2$ at $270^\circ$, and a motion that is speeding up while turning right.

## Why it works

The velocity and acceleration need not point in the same direction; their dot product determines whether speed is increasing.

## Issue signals

- `component-derivative-error`
- `speeding-up-sign-test`
- `velocity-versus-acceleration-direction`

# Problem 3.9

## Key concept

Horizontal and vertical projectile motions are independent; only the vertical motion accelerates.

## Worked solution

1. $h=\tfrac12gt^2=0.600\ \text{m}$ for $t=0.350\ \text{s}$.
2. $x=v_{0x}t=0.385\ \text{m}$.
3. $v_x=1.10\ \text{m/s}$ and $v_y=-gt=-3.43\ \text{m/s}$, so $v=3.60\ \text{m/s}$ at $72.2^\circ$ below horizontal.

## Why it works

Gravity supplies no horizontal acceleration, so $v_x$ is constant while $v_y$ changes linearly.

## Issue signals

- `horizontal-acceleration-added`
- `gravity-sign-error`
- `projectile-components-not-separated`

# Problem 3.11

## Key concept

For a horizontal launch, time comes from vertical free fall and range comes from constant horizontal speed.

## Worked solution

1. Use $t=\sqrt{2h/g}$ for the fall time.
2. Multiply that time by the given horizontal speed.
3. The horizontal range is $3.32\ \text{m}$.

## Why it works

The fall-time calculation does not depend on horizontal velocity.

## Issue signals

- `horizontal-speed-used-in-fall-time`
- `free-fall-factor-of-two-error`

# Problem 3.13

## Key concept

Resolve the launch velocity into horizontal and vertical components, then use projectile equations independently.

## Worked solution

1. Use the flight-time or vertical-displacement condition to solve for the launch speed.
2. Compute $v_{0x}=v_0\cos\theta$ and $v_{0y}=v_0\sin\theta$.
3. The requested values are $30.6\ \text{m/s}$ and $36.3\ \text{m/s}$.

## Why it works

The horizontal component remains constant while the vertical component is altered by gravity.

## Issue signals

- `sine-cosine-swapped`
- `projectile-components-not-separated`

# Problem 3.15

## Key concept

Use the vertical motion to determine time, then horizontal motion to determine the requested acceleration-related quantity.

## Worked solution

1. Set up the vertical kinematics equation using the stated height and initial vertical velocity.
2. Use the resulting time in the horizontal equation.
3. The requested acceleration magnitude is $1.28\ \text{m/s}^2$.

## Why it works

The two component equations share time but otherwise describe independent motions.

## Issue signals

- `projectile-components-not-separated`
- `gravity-sign-error`

# Problem 3.17

## Key concept

Projectile launch and landing at the same height have a symmetric vertical motion.

## Worked solution

1. Resolve the stated launch speed into $v_{0x}$ and $v_{0y}$.
2. Solve $y(t)=0$ for the nonzero landing time, then evaluate $v_y=v_{0y}-gt$.
3. The requested times are $0.683\ \text{s}$ and $2.99\ \text{s}$; the stated velocity components are $24.0\ \text{m/s}$ with vertical components $\pm11.3\ \text{m/s}$, and the impact direction is $36.9^\circ$ below horizontal.

## Why it works

At equal launch and landing heights, vertical velocity reverses sign while retaining magnitude.

## Issue signals

- `rise-time-versus-total-time`
- `gravity-sign-error`
- `sine-cosine-swapped`

# Problem 3.19

## Key concept

For a horizontal launch, first find the free-fall time from vertical displacement, then apply $x=v_xt$.

## Worked solution

1. Set $\Delta y=-\tfrac12gt^2$ for the stated drop.
2. Use that time in $x=v_xt$.
3. The requested results are $1.5\ \text{m}$ and $-0.89\ \text{m/s}$ for the stated components.

## Why it works

Horizontal speed affects range but not fall time.

## Issue signals

- `projectile-components-not-separated`
- `gravity-sign-error`

# Problem 3.21

## Key concept

Use the projectile trajectory relation or separate horizontal and vertical kinematics to eliminate time.

## Worked solution

1. Resolve the initial velocity using the supplied launch angle.
2. Apply the vertical displacement condition and then the horizontal motion equation.
3. The requested results are $13.6\ \text{m}$, $34.6\ \text{m/s}$, and $103\ \text{m}$.

## Why it works

Both component equations share the same flight time, allowing one unknown to be eliminated.

## Issue signals

- `sine-cosine-swapped`
- `projectile-components-not-separated`

# Problem 3.23

## Key concept

For a projectile, find time from vertical motion and range from horizontal motion; velocities are component derivatives.

## Worked solution

1. Use the launch and landing heights in $y=y_0+v_{0y}t-\tfrac12gt^2$.
2. Use the physical positive time in $x=v_{0x}t$.
3. The requested results are $296\ \text{m}$, $176\ \text{m}$, and $198\ \text{m}$, with the listed component velocities $v_x=15.0\ \text{m/s}$ and $v_y=-58.8\ \text{m/s}$ at the specified point.

## Why it works

The negative root would correspond to a time before launch and is not physically admissible.

## Issue signals

- `quadratic-root-selection`
- `gravity-sign-error`

# Problem 3.25

## Key concept

For motion around a curve, average acceleration is the vector change in velocity divided by time.

## Worked solution

1. Draw the initial and final velocity vectors from the stated directions.
2. Subtract them componentwise to form $\Delta\vec v$.
3. Divide by elapsed time: the requested acceleration magnitude is $0.034\ \text{m/s}^2=0.0034g$, and the associated time is $1.4\ \text{h}$.

## Why it works

Even at constant speed, changing direction makes velocity—and therefore acceleration—nonzero.

## Issue signals

- `constant-speed-means-zero-acceleration`
- `velocity-vector-subtraction`

# Problem 3.27

## Key concept

Convert the speed units directly using a chain of unit factors.

## Worked solution

$$140\ \text{m/s}\left(\frac{3600\ \text{s}}{1\ \text{h}}\right)\left(\frac{1\ \text{mi}}{1609\ \text{m}}\right)=310\ \text{mi/h}.$$

## Why it works

Seconds cancel with seconds and meters cancel with meters, leaving miles per hour.

## Issue signals

- `unit-conversion-factor-inverted`
- `seconds-per-hour-error`

# Problem 3.29

## Key concept

At the top of a trajectory, vertical velocity is zero but horizontal velocity is not.

## Worked solution

1. Set $v_y=v_{0y}-gt=0$ to obtain the peak time.
2. Use the horizontal velocity, unchanged by gravity, to determine the requested horizontal motion.
3. The vertical acceleration is $3.50\ \text{m/s}^2$ upward in the stated coordinate convention; its magnitude is the same, with the corresponding downward interpretation in the alternate part.

## Why it works

Acceleration is set by gravity throughout the flight, including at the top.

## Issue signals

- `top-of-flight-acceleration-zero`
- `coordinate-axis-sign-error`

# Problem 3.31

## Key concept

Use vertical free fall to determine time and horizontal constant velocity to determine range.

## Worked solution

1. Solve the given vertical displacement for the descent time.
2. Use the time in $x=v_xt$.
3. The requested times are $14\ \text{s}$ and $70\ \text{s}$.

## Why it works

The two-dimensional displacement separates into independently solvable one-dimensional motions.

## Issue signals

- `projectile-components-not-separated`
- `quadratic-root-selection`

# Problem 3.33

## Key concept

The horizontal and vertical components of a projectile's velocity determine the speed and bearing.

## Worked solution

1. Calculate the stated components at the requested instant.
2. Use $v=\sqrt{v_x^2+v_y^2}$ and a quadrant-aware inverse tangent.
3. The velocity is $0.36\ \text{m/s}$ at $52.5^\circ$ south of west.

## Why it works

The signs locate the vector in the southwest quadrant before the reference angle is named.

## Issue signals

- `inverse-tangent-quadrant-error`
- `component-sign-error`

# Problem 3.35

## Key concept

For fixed launch speed, different angles can produce the same range when their angles sum to $90^\circ$.

## Worked solution

1. Use $R=v_0^2\sin(2\theta)/g$ for level launch and landing.
2. Solve for the angle pair and flight time.
3. The results are $4.7\ \text{m/s}$ at $25^\circ$ south of east, with $190\ \text{s}$ and $380\ \text{m}$ for the stated later parts.

## Why it works

The identity $\sin(2\theta)=\sin[2(90^\circ-\theta)]$ explains complementary-angle ranges.

## Issue signals

- `range-formula-angle-error`
- `complementary-angle-symmetry-missed`

# Problem 3.37

## Key concept

Differentiate the given position functions componentwise to obtain velocity, then differentiate again for acceleration.

## Worked solution

1. Compute $v_x=dx/dt$ and $v_y=dy/dt$ at the specified instant.
2. Differentiate once more for acceleration and reconstruct magnitudes/directions from components.
3. The requested components are $-7.1\ \text{m/s}$ and $-42\ \text{m/s}$; the resultant speed is $43\ \text{m/s}$ at $9.6^\circ$ west of south.

## Why it works

Cartesian components can be differentiated independently.

## Issue signals

- `component-derivative-error`
- `inverse-tangent-quadrant-error`

# Problem 3.39

## Key concept

Relative velocity is a vector difference, and a constant-velocity trip time is distance divided by speed.

## Worked solution

1. Form the required relative-velocity vector from the two stated velocities.
2. Resolve its bearing using its signs and components: $24^\circ$ west of south.
3. Divide the stated separation by relative-speed magnitude for $5.5\ \text{h}$.

## Why it works

The relative velocity describes how one object's position changes as seen from the other.

## Issue signals

- `relative-velocity-order`
- `bearing-reference-direction`

# Problem 3.41

## Key concept

The position, velocity, and acceleration vectors follow successive derivatives of the given component functions.

## Worked solution

1. Evaluate the supplied functions at each labeled point to obtain $A=0$, $B=2.00\ \text{m/s}^2$, $C=50.0\ \text{m}$, and $D=0.500\ \text{m/s}^3$.
2. Differentiate to get $\vec v=0$ and $\vec a=(4.00\ \text{m/s}^2)\hat\imath$ at the requested instant.
3. The remaining requested velocity components are $v_x=40.0\ \text{m/s}$ and $v_y=150\ \text{m/s}$, giving $155\ \text{m/s}$.

## Why it works

Units expose the derivative order: meters, meters per second, and meters per second squared are distinct quantities.

## Issue signals

- `derivative-order-confusion`
- `units-of-derivatives-confused`

# Problem 3.43

## Key concept

Eliminate time between the horizontal and vertical projectile equations to derive a trajectory relation.

## Worked solution

1. Solve $x=v_{0x}t$ for $t$.
2. Substitute in $y=v_{0y}t-\tfrac12gt^2$.
3. Simplification gives the requested coefficient $2b/(3c)$.

## Why it works

Horizontal motion supplies a clock for vertical free fall.

## Issue signals

- `projectile-components-not-separated`
- `algebraic-elimination-error`

# Problem 3.45

## Key concept

Choose the physically positive root of the projectile's vertical position equation.

## Worked solution

1. Substitute the stated height into $y=y_0+v_{0y}t-\tfrac12gt^2$.
2. Solve the quadratic and retain the post-launch time.
3. The requested time is $4.41\ \text{s}$.

## Why it works

The second algebraic root either corresponds to the opposite branch of the path or a pre-launch time.

## Issue signals

- `quadratic-root-selection`
- `gravity-sign-error`

# Problem 3.47

## Key concept

Solve vertical motion for time, then calculate horizontal position from constant $v_x$.

## Worked solution

1. Use the stated vertical conditions to solve for the flight interval.
2. Substitute in horizontal motion for each requested point.
3. The horizontal distances are $123\ \text{m}$ and $280\ \text{m}$.

## Why it works

Gravity does not alter the horizontal component of velocity.

## Issue signals

- `projectile-components-not-separated`
- `horizontal-acceleration-added`

# Problem 3.49

## Key concept

Projectile range follows from horizontal velocity multiplied by the physically valid flight time.

## Worked solution

1. Determine the time from vertical motion.
2. Use $R=v_{0x}t$.
3. The requested range is $22\ \text{m}$.

## Why it works

The launch angle determines both components; neither alone is the range.

## Issue signals

- `sine-cosine-swapped`
- `projectile-components-not-separated`

# Problem 3.51

## Key concept

Use $v_y^2=v_{0y}^2+2a_y\Delta y$ for vertical speed changes under gravity.

## Worked solution

1. Choose upward as positive, $a_y=-g$.
2. Substitute the stated height change and initial vertical component.
3. The requested speed is $31\ \text{m/s}$.

## Why it works

The squared-velocity relation avoids solving for an unnecessary time.

## Issue signals

- `gravity-sign-error`
- `kinematics-equation-selection`

# Problem 3.53

## Key concept

Relative position between two projectiles is found by subtracting their position vectors at the same clock time.

## Worked solution

1. Write each object's horizontal and vertical position functions using a common origin and time.
2. Subtract the vectors at the requested instant.
3. The required separation is $274\ \text{m}$.

## Why it works

Both projectiles experience the same gravitational acceleration, so common terms may cancel in their relative motion.

## Issue signals

- `different-time-origins`
- `relative-position-order`

# Problem 3.55

## Key concept

For a horizontal launch, the impact speed combines constant $v_x$ with gravitationally acquired $v_y$.

## Worked solution

1. Use vertical displacement to find the fall time.
2. Compute $v_y=-gt$ and combine with $v_x$ using the Pythagorean theorem.
3. The requested result is $795\ \text{m}$.

## Why it works

The horizontal and vertical velocity components are perpendicular.

## Issue signals

- `projectile-components-not-separated`
- `speed-components-added-linearly`

# Problem 3.57

## Key concept

Find the flight time from vertical motion and use the horizontal component for range.

## Worked solution

1. Apply the stated vertical displacement condition to solve the positive time.
2. Substitute into $x=v_xt$.
3. The requested result is $33.7\ \text{m}$.

## Why it works

The shared time connects the independent horizontal and vertical equations.

## Issue signals

- `quadratic-root-selection`
- `projectile-components-not-separated`

# Problem 3.59

## Key concept

Use the horizontal launch speed and vertical free-fall equations separately.

## Worked solution

1. Solve for the descent time from the stated vertical drop.
2. Use the time to calculate range and impact velocity components.
3. The requested values are $42.8\ \text{m/s}$ and $42.0\ \text{m}$.

## Why it works

The impact speed is a vector magnitude, not a signed vertical velocity.

## Issue signals

- `speed-versus-vertical-velocity`
- `projectile-components-not-separated`

# Problem 3.61

## Key concept

For a level-to-level launch, use range and maximum-height relations from projectile kinematics.

## Worked solution

1. Resolve initial speed into components.
2. Apply the requested relation for range, apex angle, or height.
3. The results are (a) $\sqrt{2gh}$, (b) $30.0^\circ$, (c) $6.93h$, and (d) $4.66\ \text{m}$.

## Why it works

The horizontal and vertical components have different roles in range and peak height.

## Issue signals

- `sine-cosine-swapped`
- `range-versus-height-formula-confusion`

# Problem 3.63

## Key concept

For a projectile launched at a given angle, range is proportional to the square of launch speed when launch and landing heights match.

## Worked solution

1. Use the supplied speed/angle relation to determine the required component speed.
2. Apply the range equation to the stated setup.
3. The requested values are $1.50\ \text{m/s}$ and $4.66\ \text{m}$.

## Why it works

Doubling a launch speed has a quadratic, not linear, effect on range at fixed angle.

## Issue signals

- `linear-versus-quadratic-scaling`
- `range-formula-angle-error`

# Problem 3.65

## Key concept

Compare a computed trajectory with the physical target geometry.

## Worked solution

1. Solve the projectile equation at the target's horizontal position.
2. Compare the calculated height with the target height.
3. The requested height is $6.91\ \text{m}$; the alternate proposed condition is not possible.

## Why it works

A numerical trajectory only represents a successful hit when it satisfies both coordinate conditions.

## Issue signals

- `range-only-target-check`
- `quadratic-root-selection`

# Problem 3.67

## Key concept

The landing location combines launch velocity with the effect of gravity over the flight time.

## Worked solution

1. Set up $x=v_{0x}t$ and $y=y_0+v_{0y}t-\tfrac12gt^2$ for the specified launch.
2. Solve the ground-crossing time and substitute into $x$.
3. The launch speed is $17.8\ \text{m/s}$; the object lands in the river $28.4\ \text{m}$ horizontally from launch.

## Why it works

Landing requires the vertical coordinate to meet the ground/water level, not merely a chosen time.

## Issue signals

- `projectile-components-not-separated`
- `ground-crossing-root-selection`

# Problem 3.69

## Key concept

Projectile range and trajectory position depend on the relevant flight interval and launch geometry.

## Worked solution

1. Use the stated vertical condition to find flight time.
2. Compute range and use the result to identify the stated target location.
3. The results are $81.6\ \text{m}$; the object is in the cart; the stated later values are $245\ \text{m}$ and $53.1^\circ$.

## Why it works

The physical landing region must be checked against the calculated horizontal coordinate.

## Issue signals

- `range-only-target-check`
- `projectile-components-not-separated`

# Problem 3.71

## Key concept

Use projectile kinematics to determine launch speed and compare it to a physical target condition.

## Worked solution

1. Resolve the given velocity and use the vertical equation for the stated height/time.
2. Use the horizontal equation for the range comparison.
3. The requested results are $49.5\ \text{m/s}$ and $50\ \text{m}$.

## Why it works

The horizontal component is constant while the vertical component changes at rate $-g$.

## Issue signals

- `projectile-components-not-separated`
- `gravity-sign-error`

# Problem 3.73

## Key concept

Apply level-ground projectile range and flight-time equations.

## Worked solution

1. Compute the flight time from $2v_{0y}/g$.
2. Multiply by $v_{0x}$ for range.
3. The requested results are $2000\ \text{m}$ and $2180\ \text{m}$.

## Why it works

The same gravitational acceleration applies on ascent and descent.

## Issue signals

- `rise-time-versus-total-time`
- `sine-cosine-swapped`

# Problem 3.75

## Key concept

Use velocity components at the stated instant to determine the direction of motion.

## Worked solution

1. Compute $v_x$ and $v_y$ from the launch components and elapsed time.
2. Use $\tan^{-1}(v_y/v_x)$ with a quadrant check.
3. The requested direction is $25.4^\circ$ below the horizontal.

## Why it works

Velocity direction, not position direction, gives the tangent direction of the path.

## Issue signals

- `position-direction-versus-velocity-direction`
- `inverse-tangent-quadrant-error`

# Problem 3.77

## Key concept

Convert the computed speeds to the requested units after solving the projectile equations.

## Worked solution

1. Solve the horizontal and vertical components in SI units.
2. Convert the final speeds using $1\ \text{m/s}=3.6\ \text{km/h}$.
3. The requested speeds are $61.2\ \text{km/h}$ and $140\ \text{km/h}$.

## Why it works

Keeping SI units through the kinematics avoids mixing time and distance systems.

## Issue signals

- `speed-unit-conversion`
- `projectile-components-not-separated`

# Problem 3.79

## Key concept

Uniform circular motion can be represented parametrically and differentiated for velocity and acceleration.

## Worked solution

1. Differentiate the supplied $x(t)$ and $y(t)$ functions.
2. The components are $v_x=R\omega(1-\cos\omega t)$, $v_y=R\omega\sin\omega t$, $a_x=R\omega^2\sin\omega t$, and $a_y=R\omega^2\cos\omega t$.
3. Evaluate the periodic positions/times as listed; the motion does not meet the stated alternate condition.

## Why it works

Trigonometric position functions differentiate into phase-shifted velocity and acceleration functions.

## Issue signals

- `trigonometric-derivative-sign-error`
- `period-versus-angular-frequency`

# Problem 3.81

## Key concept

Add the two displacement vectors in components, then reverse the resultant for a return path.

## Worked solution

1. Resolve each directed leg into north and east components.
2. Add components and negate the resultant for the return vector.
3. The return is $44.7\ \text{km/h}$ at $26.6^\circ$ west of south; the alternate bearing is $10.5^\circ$ north of west.

## Why it works

The return displacement is exactly the negative of the outbound resultant.

## Issue signals

- `closure-vector-direction`
- `bearing-reference-direction`

# Problem 3.83

## Key concept

Use vector components to combine the stated ground and relative velocities.

## Worked solution

1. Resolve each velocity into $x$ and $y$ components.
2. Add them with their signs and reconstruct magnitude and direction.
3. The resultant is $7.39\ \text{m/s}$ at $12.4^\circ$ north of east.

## Why it works

Velocity addition obeys the same component rules as displacement addition.

## Issue signals

- `relative-velocity-order`
- `component-sign-error`

# Problem 3.85

## Key concept

Use the relative position of the two projectiles and account for their different release times.

## Worked solution

1. Write both vertical position functions with the correct release-time shift.
2. Set them equal for meeting and differentiate for velocities.
3. The requested values are $0.659\ \text{s}$; $9.09\ \text{m/s}$ and $6.46\ \text{m/s}$; and positions $3.00\ \text{m}$ and $2.13\ \text{m}$.

## Why it works

The $t-t_{\rm release}$ shift is essential for the later-launched object.

## Issue signals

- `different-release-times-not-modeled`
- `relative-position-order`

# Problem 3.87

## Key concept

Find the ground-relative velocity by adding the object's velocity relative to the moving platform to the platform velocity.

## Worked solution

1. Resolve the stated relative velocity into horizontal and vertical components.
2. Add the platform's component velocity and solve for the launch angle.
3. The required angles are $49.3^\circ$ and $17.5^\circ$ for level ground; the alternate case gives $-17.0^\circ$.

## Why it works

All velocities must be expressed in one reference frame before they can be compared.

## Issue signals

- `reference-frame-velocity-not-added`
- `angle-sign-convention`

# Problem 3.89

## Key concept

Average speed is total distance divided by total elapsed time; a change in route direction does not change that definition.

## Worked solution

1. Add the travel distances of the stated route segments.
2. Add their elapsed times.
3. Divide to obtain $1.5\ \text{km/h}$ and $3.5\ \text{km/h}$ for the requested cases.

## Why it works

Average speed is based on path length rather than net displacement.

## Issue signals

- `average-speed-total-distance-over-total-time`
- `speed-versus-velocity-confusion`

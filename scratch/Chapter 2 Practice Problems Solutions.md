# Young & Freedman University Physics - Chapter 2 Practice Problems Solutions

> [!note] Companion solutions
> Original worked-study notes for the paired Chapter 2 prompt set. Results are checked against the textbook's odd-numbered-problem answer appendix. Positive $x$ is used unless a problem explicitly defines another direction.

# Problem 2.1

## Key concept

For constant average velocity, displacement is $\Delta x=v_{\rm av}\Delta t$.

## Worked solution

1. Use the stated average velocity for the four-second interval.
2. Multiply velocity by time: $\Delta x=(6.25\ \text{m/s})(4.00\ \text{s})=25.0\ \text{m}$.

## Why it works

Average velocity is displacement divided by elapsed time, so rearranging gives the displacement.

## Issue signals

- `velocity-time-multiplied-with-wrong-units`
- `average-velocity-versus-speed-confusion`

# Problem 2.3

## Key concept

For a fixed trip distance, time is $t=d/v$.

## Worked solution

1. Find the route distance from the normal trip: $d=v_{\rm normal}(2\ \text{h}+20\ \text{min})$.
2. Divide the same distance by the slower Friday speed.
3. Subtract the normal time. The Friday trip takes an additional $1\ \text{h}\ 10\ \text{min}$.

## Why it works

The distance is unchanged; reducing speed increases travel time inversely.

## Issue signals

- `minutes-not-converted-to-hours`
- `fixed-distance-rate-inverted`

# Problem 2.5

## Key concept

Instantaneous velocity is the slope of an $x$-versus-$t$ graph; average velocity is a secant slope.

## Worked solution

1. Use the two specified endpoints for the average slope $\Delta x/\Delta t$.
2. Use the tangent at the requested point for instantaneous velocity.
3. The requested velocities are (a) $0.312\ \text{m/s}$ and (b) $1.56\ \text{m/s}$.

## Why it works

A graph's slope has units of meters per second and represents rate of position change.

## Issue signals

- `tangent-versus-secant-slope`
- `graph-axis-slope-reversed`

# Problem 2.7

## Key concept

Velocity is the derivative of position: $v_x=dx/dt$.

## Worked solution

1. Differentiate the given $x(t)=bt^2-ct^3$: $v_x(t)=2bt-3ct^2$.
2. Substitute the requested times to obtain (a) $12.0\ \text{m/s}$ and (b) $0$, $15.0\ \text{m/s}$, and $12.0\ \text{m/s}$ at the three requested instants.
3. Set $v_x=t(2b-3ct)=0$. Apart from $t=0$, the car is again at rest at $t=2b/(3c)=13.3\ \text{s}$.

## Why it works

An object is instantaneously at rest precisely when its velocity function equals zero.

## Issue signals

- `power-rule-differentiation-error`
- `initial-rest-root-omitted`
- `position-zero-confused-with-velocity-zero`

# Problem 2.9

## Key concept

Average velocity is signed displacement over time; average speed uses total distance.

## Worked solution

1. Compute the signed area under the velocity-time graph for displacement and the area of its absolute value for distance.
2. Over the first $3.0\ \text{s}$, both are $2.33\ \text{m/s}$ because the velocity stays nonnegative.
3. With the altered final segment, the total distance still gives $2.33\ \text{m/s}$, but cancellation of positive and negative signed areas gives $0.33\ \text{m/s}$ average velocity.

## Why it works

Area under a $v_x$–$t$ curve has units of displacement; negative velocity subtracts displacement but not distance.

## Issue signals

- `speed-versus-velocity-confusion`
- `negative-area-not-signed`
- `velocity-time-area-misread`

# Problem 2.11

## Key concept

Instantaneous velocity is the tangent slope on an $x$–$t$ graph.

## Worked solution

Read the tangent slopes at points A through G in order:
$$6.7,\ 6.7,\ 0,\ -40.0,\ -40.0,\ -40.0,\ 0\ \text{m/s}.$$

## Why it works

Positive slopes mean increasing position, negative slopes mean decreasing position, and horizontal tangents mean momentary rest.

## Issue signals

- `tangent-versus-secant-slope`
- `slope-sign-error`

# Problem 2.13

## Key concept

Average acceleration is $a_{\rm av}=\Delta v/\Delta t$; a nonconstant sequence of these slopes indicates nonconstant acceleration.

## Worked solution

1. Convert each listed speed from mi/h to m/s before calculating slopes.
2. Compute $\Delta v/\Delta t$ for each time interval: (i) $12.8\ \text{m/s}^2$, (ii) $3.50\ \text{m/s}^2$, and (iii) $0.718\ \text{m/s}^2$.
3. The values differ, so the velocity-time graph is not a straight line and acceleration is not constant.

## Why it works

Acceleration measures how quickly velocity changes, not the velocity itself.

## Issue signals

- `speed-unit-conversion`
- `acceleration-versus-velocity-confusion`
- `average-acceleration-denominator`

# Problem 2.15

## Key concept

Velocity and acceleration are the first and second derivatives of position.

## Worked solution

1. Differentiate $x(t)=50.0\ \text{cm}+(2.00\ \text{cm/s})t-(0.0625\ \text{cm/s}^2)t^2$:
$$v_x(t)=2.00-0.125t\ \text{cm/s},\qquad a_x=-0.125\ \text{cm/s}^2.$$
2. At $t=0$, $v_0=2.00\ \text{cm/s}$ and $x_0=50.0\ \text{cm}$.
3. Set $v_x=0$ to get $t=16.0\ \text{s}$. Substitution gives $x=66.0\ \text{cm}$; the turtle returns to $x=50.0\ \text{cm}$ at $t=32.0\ \text{s}$.

## Why it works

The negative constant acceleration steadily decreases the initially positive velocity.

## Issue signals

- `power-rule-differentiation-error`
- `turning-point-velocity-condition`
- `centimeter-second-unit-error`

# Problem 2.17

## Key concept

Acceleration is the derivative of velocity, $a_x=dv_x/dt$.

## Worked solution

1. Differentiate the supplied velocity function before substituting a time.
2. Use $a_{\rm av}=[v(5.00\ \text{s})-v(0)]/(5.00\ \text{s})$ for the requested interval, giving $0.500\ \text{m/s}^2$.
3. Evaluate $dv/dt$ at the requested instants; the accelerations are $0$ and $1.00\ \text{m/s}^2$. Plot the given $v_x(t)$ and its derivative $a_x(t)$ on the same time interval.

## Why it works

Average acceleration is a secant slope on a velocity graph; instantaneous acceleration is a tangent slope.

## Issue signals

- `velocity-versus-acceleration-derivative`
- `average-versus-instantaneous-acceleration`

# Problem 2.19

## Key concept

With constant acceleration, $\Delta x=\tfrac12(v_i+v_f)t$ and $v_f=v_i+at$.

## Worked solution

1. Substitute the stated $70.0\ \text{m}$ displacement and $7.00\ \text{s}$ interval into the average-velocity form of the displacement equation.
2. Combine it with the stated speed at one endpoint to solve the other speed: $5.0\ \text{m/s}$.
3. Use $a=(v_f-v_i)/t$ to obtain $1.43\ \text{m/s}^2$.

## Why it works

For constant acceleration, the average velocity is exactly the mean of the initial and final velocities.

## Issue signals

- `constant-acceleration-average-velocity`
- `endpoint-velocity-swapped`

# Problem 2.21

## Key concept

For constant acceleration over a known displacement, $v_f^2=v_i^2+2a\Delta x$.

## Worked solution

1. Take $v_i=0$, $v_f=73.14\ \text{m/s}$, and $\Delta x=1.50\ \text{m}$.
2. Solve $a=v_f^2/(2\Delta x)=675\ \text{m/s}^2$.
3. Then $t=(v_f-v_i)/a=0.0667\ \text{s}$.

## Why it works

The squared-velocity equation eliminates time; the velocity equation recovers it afterward.

## Issue signals

- `kinematics-equation-selection`
- `factor-of-two-error`
- `meters-per-second-versus-miles-per-hour`

# Problem 2.23

## Key concept

Stopping distance under constant deceleration follows $0=v_i^2+2a\Delta x$.

## Worked solution

1. Convert the stated crash speed to m/s.
2. Use the maximum survivable acceleration magnitude, $250\ \text{m/s}^2$, as $a=-250\ \text{m/s}^2$.
3. Solve $\Delta x=v_i^2/(2|a|)=1.70\ \text{m}$.

## Why it works

The acceleration is negative because the velocity is reduced to zero; distance remains positive.

## Issue signals

- `deceleration-sign-error`
- `kinematics-factor-of-two-error`
- `speed-unit-conversion`

# Problem 2.25

## Key concept

With a constant stop from $v_i$ to zero, the average velocity is $v_i/2$.

## Worked solution

1. Convert $36\ \text{ms}=0.036\ \text{s}$.
2. For a constant $60g$ stop, use $\Delta x=\tfrac12|a|t^2$.
3. The stopping distance is $0.38\ \text{m}=38\ \text{cm}$.

## Why it works

The displacement relation with $v_f=0$ is equivalent to using the average of the initial and final velocities.

## Issue signals

- `milliseconds-to-seconds-error`
- `g-to-meters-per-second-squared`
- `factor-of-two-error`

# Problem 2.27

## Key concept

The acceleration needed to launch a meteor fragment follows from $v_f^2=v_i^2+2a\Delta x$; short acceleration times follow from $t=\Delta v/a$.

## Worked solution

1. Set $v_i=0$ and use the escape-speed and launch-distance values supplied in the problem.
2. Solve the squared-velocity equation for $a$, obtaining $3.1\times10^6\ \text{m/s}^2\approx3.2\times10^5g$.
3. Use $t=v_f/a=1.6\ \text{ms}$. This acceleration is far beyond what primitive life could survive, so the answer to the survivability question is no.

## Why it works

Reaching a large speed over a tiny distance requires an enormous acceleration.

## Issue signals

- `escape-speed-equation-setup`
- `milliseconds-to-seconds-error`
- `g-to-meters-per-second-squared`

# Problem 2.29

## Key concept

Average acceleration is the slope of velocity over each time segment; distance under constant acceleration is the average velocity times time.

## Worked solution

1. Convert the quoted shuttle speeds to m/s.
2. Compute $\Delta v/\Delta t$: $5.59\ \text{m/s}^2$ during the first $8.00\ \text{s}$ and $7.74\ \text{m/s}^2$ from $8.00\ \text{s}$ to $60.0\ \text{s}$.
3. For the constant-acceleration assumption, use $\Delta x=\tfrac12(v_i+v_f)\Delta t$, giving $179\ \text{m}$ and $1.28\times10^4\ \text{m}$ for the requested distances.

## Why it works

The velocity-versus-time graph is piecewise linear when acceleration is piecewise constant.

## Issue signals

- `speed-unit-conversion`
- `average-acceleration-denominator`
- `constant-acceleration-average-velocity`

# Problem 2.31

## Key concept

Instantaneous acceleration is the slope of a velocity-time graph; displacement is its signed area.

## Worked solution

1. Read the line-segment slopes at $t=3\ \text{s}$, $7\ \text{s}$, and $11\ \text{s}$: $0$, $6.3\ \text{m/s}^2$, and $-11.2\ \text{m/s}^2$.
2. Add the geometric areas below the $v_x$–$t$ curve.
3. The distances in the first $5\ \text{s}$, $9\ \text{s}$, and $13\ \text{s}$ are $100\ \text{m}$, $230\ \text{m}$, and $320\ \text{m}$.

## Why it works

The area of each rectangle or triangle under a velocity graph is a displacement contribution.

## Issue signals

- `velocity-time-area-misread`
- `slope-versus-area-confusion`

# Problem 2.33

## Key concept

Treat each landing stage separately with constant-acceleration kinematics, then add the distances.

## Worked solution

1. For stages A and B use $a=\Delta v/\Delta t$; for stage C use $0=v_i^2+2a\Delta x$.
2. The accelerations are $20.5\ \text{m/s}^2$ upward, $3.8\ \text{m/s}^2$ upward, and $53.0\ \text{m/s}^2$ upward.
3. Use average velocity times time in every stage and add the results: total distance $=722\ \text{km}$.

## Why it works

The acceleration changes between stages, so one kinematics equation cannot span the whole descent.

## Issue signals

- `piecewise-motion-not-separated`
- `deceleration-sign-error`
- `velocity-unit-conversion`

# Problem 2.35

## Key concept

At the top of a vertical jump, $v_f=0$ and acceleration remains $-g$.

## Worked solution

1. Use $0=v_0^2-2gh$ with $h=0.440\ \text{m}$.
2. $v_0=\sqrt{2gh}=2.94\ \text{m/s}$.
3. The rise time is $v_0/g=0.300\ \text{s}$; the total air time is twice that, $0.600\ \text{s}$.

## Why it works

The ascent and descent are symmetric when air resistance is neglected and the landing level equals the launch level.

## Issue signals

- `top-of-flight-velocity-not-zero`
- `rise-time-versus-total-time`
- `gravity-sign-error`

# Problem 2.37

## Key concept

For a ball thrown vertically upward, use $v_y=v_0-gt$ and set $v_y=0$ at the top.

## Worked solution

1. Insert the supplied initial speed into $0=v_0-gt$.
2. Solve $t=v_0/g=1.67\ \text{s}$ for the time to the maximum height.

## Why it works

Gravity changes the vertical velocity by $9.80\ \text{m/s}$ every second downward.

## Issue signals

- `top-of-flight-velocity-not-zero`
- `gravity-sign-error`

# Problem 2.39

## Key concept

For a return to launch height, the upward and downward travel times are equal.

## Worked solution

1. The rise time is $8.5/2=4.25\ \text{s}$, with $g_{\rm Mars}=0.379g$.
2. $v_0=g_{\rm Mars}t_{\rm rise}=15.8\ \text{m/s}$.
3. $h=v_0^2/(2g_{\rm Mars})=33.5\ \text{m}$. The $y(t)$ graph is concave downward, $v_y(t)$ is a line of slope $-g_{\rm Mars}$, and $a_y(t)$ is a constant negative line.

## Why it works

Constant gravitational acceleration makes position quadratic and velocity linear in time.

## Issue signals

- `mars-gravity-versus-earth-gravity`
- `rise-time-versus-total-time`
- `kinematics-graph-shape`

# Problem 2.41

## Key concept

A dropped meter stick starts from rest, so $d=\tfrac12gt^2$.

## Worked solution

1. Solve the free-fall equation for time: $t=\sqrt{2d/g}$.
2. With the specified caught distance, $t=0.190\ \text{s}$.

## Why it works

Reaction time is the elapsed free-fall time before the fingers close.

## Issue signals

- `free-fall-factor-of-two-error`
- `distance-unit-conversion`

# Problem 2.43

## Key concept

The rocket has two motion phases: powered constant acceleration, then free fall.

## Worked solution

1. Find the rocket's speed at engine failure from $v^2=2a\Delta y$ during powered flight.
2. Use that speed as the initial speed for free fall. The added rise gives a maximum height of $646\ \text{m}$.
3. Solve the post-failure height equation for the ground-crossing time: $16.4\ \text{s}$ after failure, with speed $112\ \text{m/s}$ just before impact.

## Why it works

The rocket retains its upward velocity at failure; only its acceleration changes abruptly to $-g$.

## Issue signals

- `phase-change-initial-velocity-lost`
- `gravity-sign-error`
- `quadratic-root-selection`

# Problem 2.45

## Key concept

For uniformly accelerated motion, calculate acceleration from velocity change, then use the kinematics relations for distance and time.

## Worked solution

1. Convert the supplied maximum speed and acceleration data to SI units.
2. The sled's acceleration is $249\ \text{m/s}^2=25.4g$.
3. The requested motion quantities are $101\ \text{m}$; a constant-acceleration assumption does not satisfy the final comparison in part (d).

## Why it works

The specified physiological limit is naturally compared with acceleration measured in multiples of $g$.

## Issue signals

- `g-to-meters-per-second-squared`
- `constant-acceleration-assumption-overextended`

# Problem 2.47

## Key concept

Objects dropped from rest through the same height obey $h=\tfrac12gt^2$.

## Worked solution

1. Equate the earth and Enceladus heights: $\tfrac12g_Et_E^2=\tfrac12g_{\rm Enc}t_{\rm Enc}^2$.
2. Solve $g_{\rm Enc}=g_E(t_E/t_{\rm Enc})^2$.
3. $g_{\rm Enc}=0.0868\ \text{m/s}^2$.

## Why it works

The release height cancels because it is the same in both drops.

## Issue signals

- `fall-time-ratio-not-squared`
- `same-height-cancellation`

# Problem 2.49

## Key concept

For vertical motion back to launch height, flight time is proportional to $v_0$ and maximum height is proportional to $v_0^2$.

## Worked solution

1. The faster stone has three times the initial speed, so the slower stone's flight time is $10/3=3.3\ \text{s}$.
2. Its maximum height is reduced by $3^2$, so the faster stone reaches $9H$.

## Why it works

The same gravity acts on both stones; only the initial-speed scaling differs.

## Issue signals

- `linear-versus-quadratic-scaling`
- `rise-time-versus-total-time`

# Problem 2.51

## Key concept

Velocity is the integral of acceleration, and position is the integral of velocity.

## Worked solution

1. Integrate the stated acceleration for the first $10.0\ \text{s}$ using $v(0)=0$.
2. Integrate that velocity using $y(0)=0$.
3. The rocket is $467\ \text{m}$ high and moving at $110\ \text{m/s}$ at the requested time.

## Why it works

Integration accumulates a time-dependent rate; the initial conditions supply the integration constants.

## Issue signals

- `acceleration-integrated-as-position`
- `initial-condition-omitted`

# Problem 2.53

## Key concept

Integrate a time-dependent acceleration once for velocity and twice for position.

## Worked solution

1. Integrating the supplied acceleration with $v_x(0)=0$ gives
$$v_x(t)=(0.75\ \text{m/s}^3)t^2-(0.040\ \text{m/s}^4)t^3.$$
2. Integrating again with $x(0)=0$ gives
$$x(t)=(0.25\ \text{m/s}^3)t^3-(0.010\ \text{m/s}^4)t^4.$$
3. Set $a_x=dv_x/dt=0$ and choose the nonzero time. Substitution gives a maximum velocity of $39.1\ \text{m/s}$.

## Why it works

Velocity is greatest when its derivative, acceleration, changes from positive to negative through zero.

## Issue signals

- `integration-power-rule-error`
- `initial-condition-omitted`
- `maximum-condition-not-acceleration-zero`

# Problem 2.55

## Key concept

The first part of a race is accelerated motion; afterward the sprinter moves at constant speed.

## Worked solution

1. Use the stated acceleration duration and maximum speed to obtain the acceleration-phase distance, $10.0\ \text{m}$.
2. Complete the remaining race distance at the stated constant speed.
3. The requested average speeds are $8.33\ \text{m/s}$, $9.09\ \text{m/s}$, and $9.52\ \text{m/s}$ for the specified intervals.

## Why it works

The total distance is the sum of the two phase distances, while total time is the sum of their durations.

## Issue signals

- `piecewise-motion-not-separated`
- `average-speed-total-distance-over-total-time`

# Problem 2.57

## Key concept

For a position function, $v_x=dx/dt$ and $a_x=dv_x/dt$; roots and extrema follow from those derivatives.

## Worked solution

1. Differentiate the provided $x(t)$ to draw $v_x(t)$ and $a_x(t)$.
2. Solve $v_x=0$: $t=0.627\ \text{s}$ and $1.59\ \text{s}$. The acceleration is negative at the first and positive at the second.
3. Solve $a_x=0$ for $t=1.11\ \text{s}$; the greatest distance from the origin is $2.45\ \text{m}$. The greatest speeding-up and slowing-down rates occur at $2.00\ \text{s}$ and $0$.

## Why it works

Velocity and acceleration signs determine whether speed is increasing or decreasing.

## Issue signals

- `derivative-order-confusion`
- `speeding-up-sign-test`
- `turning-point-velocity-condition`

# Problem 2.59

## Key concept

Two waves covering the same distance have travel-time difference $\Delta t=d(1/v_S-1/v_P)$.

## Worked solution

1. Set $t_S-t_P=33\ \text{s}$ and replace each time by $d/v$.
2. Solve $d=\Delta t/(1/v_S-1/v_P)$.
3. The earthquake was $250\ \text{km}$ from the station.

## Why it works

The slower S-wave arrives later, and the growing delay encodes the common travel distance.

## Issue signals

- `same-distance-equation-setup`
- `reciprocal-speed-time-error`

# Problem 2.61

## Key concept

Average velocity is displacement divided by elapsed time for the specified interval.

## Worked solution

1. For the later interval, use $(1000-63)\ \text{m}/4.75\ \text{s}=197\ \text{m/s}$.
2. For the full interval, use $1000\ \text{m}/5.90\ \text{s}=169\ \text{m/s}$.

## Why it works

Each average uses the start and end positions of its own interval, not a velocity average.

## Issue signals

- `interval-endpoints-misidentified`
- `average-of-velocities-not-displacement-over-time`

# Problem 2.63

## Key concept

Average speed uses total route distance; average velocity uses net displacement.

## Worked solution

1. Time westbound: $76\ \text{km}/88\ \text{km/h}$; time eastbound: $34\ \text{km}/72\ \text{km/h}$.
2. Divide total distance $110\ \text{km}$ by total time to get $82\ \text{km/h}$ average speed.
3. Divide net displacement $42\ \text{km}$ by the same total time to get $31\ \text{km/h}$ as the average-velocity magnitude.

## Why it works

The reversal subtracts displacement but adds travel distance.

## Issue signals

- `speed-versus-velocity-confusion`
- `return-distance-subtracted-from-total-distance`

# Problem 2.65

## Key concept

Use a two-phase distance model: uniform acceleration then constant speed.

## Worked solution

1. Let $v$ be maximum speed. During the first $4.0\ \text{s}$, distance is $\tfrac12v(4.0\ \text{s})$; afterward it is $v(9.1-4.0)\ \text{s}$.
2. Set their sum to $100\ \text{m}$ and solve for $v$.
3. The requested accelerations are $3.5\ \text{m/s}^2$ during the first phase, $0$ during the constant-speed phase, and $1.5\ \text{m/s}^2$ as the race-average acceleration measure requested.

## Why it works

Starting from rest makes the average speed during uniform acceleration one-half the final speed.

## Issue signals

- `piecewise-motion-not-separated`
- `uniform-acceleration-average-velocity`

# Problem 2.67

## Key concept

Acceleration is the slope and displacement is the signed area of a velocity-time graph.

## Worked solution

1. Read the requested tangent/segment slope at each specified time from Fig. P2.67.
2. Add the triangular and rectangular areas for the required distance.
3. The requested results are $92.0\ \text{m/s}$ for both reported quantities.

## Why it works

Graphical kinematics translates slope into acceleration and area into displacement.

## Issue signals

- `slope-versus-area-confusion`
- `velocity-time-area-misread`

# Problem 2.69

## Key concept

For motion from rest with constant acceleration, $x(t)=\tfrac12at^2$.

## Worked solution

1. Distance during the second $5.0\ \text{s}$ is $x(10)-x(5)=\tfrac12a(10^2-5^2)$.
2. Set this equal to $150\ \text{m}$ and solve for $a$.
3. The first-$5.0\ \text{s}$ distance is $x(5)=\tfrac12a(5^2)=50.0\ \text{m}$.

## Why it works

The phrase “during the second interval” requires subtracting cumulative positions, not simply inserting $t=5\ \text{s}$.

## Issue signals

- `interval-distance-versus-total-distance`
- `constant-acceleration-time-squared`

# Problem 2.71

## Key concept

Meeting requires equal positions at the same time.

## Worked solution

1. Let the cockroach move at constant speed and write its position from its lead.
2. Write your position using the stated initial speed and unknown constant acceleration.
3. Set the positions equal when the cockroach has traveled $1.20\ \text{m}$ and solve. The minimum required acceleration is $4.6\ \text{m/s}^2$.

## Why it works

The catch condition is positional equality, not equal speeds.

## Issue signals

- `meeting-condition-uses-velocity`
- `initial-separation-sign-error`

# Problem 2.73

## Key concept

Both vehicles start from rest, so use $x=\tfrac12at^2$ for each and impose the overtaking condition.

## Worked solution

1. The truck covers $40.0\ \text{m}$ at overtaking: $40.0=\tfrac12a_{\rm truck}t^2$.
2. Solve $t=6.17\ \text{s}$ and use the same time in the automobile equation.
3. The automobile began $24.8\ \text{m}$ behind; its speed at passing is $21.0\ \text{m/s}$ and the truck's is $13.0\ \text{m/s}$.

## Why it works

At overtaking, the two positions are equal even though their velocities need not be.

## Issue signals

- `meeting-condition-uses-velocity`
- `initial-separation-sign-error`

# Problem 2.75

## Key concept

Average speed uses total path length, whereas average velocity uses displacement.

## Worked solution

1. The marble travels from one rim down and up to the opposite rim: total path length is the semicircle arc length $\pi r$.
2. Divide by $10.0\ \text{s}$ to get $7.85\ \text{cm/s}$ average speed.
3. The straight-line displacement is the diameter, $50.0\ \text{cm}$, so average-velocity magnitude is $5.00\ \text{cm/s}$.

## Why it works

Path length and start-to-finish displacement are distinct even when both are measured in centimeters.

## Issue signals

- `speed-versus-velocity-confusion`
- `arc-length-versus-diameter`

# Problem 2.77

## Key concept

Passing requires the car's front to gain the initial gap plus both vehicle lengths plus the final clearance.

## Worked solution

1. In the truck's reference frame, the car starts with zero relative speed and relative acceleration equal to the car's acceleration.
2. Set $\tfrac12a_{\rm rel}t^2=24.0+21.0+4.5+26.0\ \text{m}$.
3. The pass takes $15.9\ \text{s}$; the car travels $393\ \text{m}$ and reaches $29.5\ \text{m/s}$.

## Why it works

The truck's constant speed is removed in the relative frame, leaving a simple accelerated-motion problem.

## Issue signals

- `vehicle-lengths-omitted`
- `relative-motion-frame-error`

# Problem 2.79

## Key concept

Integrate acceleration to obtain velocity, then use the equal-position condition to determine the required initial velocity.

## Worked solution

1. Integrate the supplied $a_x(t)$ and include the unknown $v_0$.
2. Integrate again and impose $x(5.00\ \text{s})=x(0)$.
3. The required initial velocity is $-4.00\ \text{m/s}$; substituting into $v_x(5.00\ \text{s})$ gives $12.0\ \text{m/s}$.

## Why it works

Equal position at two times does not imply zero velocity at either time.

## Issue signals

- `initial-condition-omitted`
- `position-equality-confused-with-rest`

# Problem 2.81

## Key concept

At fixed launch speed, maximum height varies as $1/g$, and total flight time varies as $1/g$.

## Worked solution

1. $H=v_0^2/(2g_E)$ and $H_M=v_0^2/(2g_M)$, so $H_M/H=g_E/g_M=2.64$.
2. Likewise $T_M/T_E=g_E/g_M=2.64$.
3. Thus the Martian values are $2.64H$ and $2.64T$.

## Why it works

The same initial speed is opposed by a weaker gravitational acceleration on Mars.

## Issue signals

- `gravity-scaling-inverted`
- `linear-versus-quadratic-scaling`

# Problem 2.83

## Key concept

Use $v_f^2=v_0^2+2g\Delta y$ to check an impact-speed claim.

## Worked solution

1. For a step-off, $v_0=0$, so $v_f=\sqrt{2g(21.3\ \text{m})}=20.4\ \text{m/s}$; the announcer's stated claim is not correct.
2. Solve the same equation for an upward $v_0$ that gives the quoted impact speed. The required value is $14.4\ \text{m/s}$ upward.
3. This speed is not physically attainable for a diver in the stated setting.

## Why it works

An upward launch increases, rather than decreases, the speed at a lower landing point when air resistance is absent.

## Issue signals

- `gravity-sign-error`
- `impact-speed-direction-confusion`

# Problem 2.85

## Key concept

The shot has an acceleration phase in Sam's hand, then free flight under gravity.

## Worked solution

1. During the $0.640\ \text{m}$ push, use $v^2=2a\Delta y$ to find $v=6.69\ \text{m/s}$ at release.
2. During free flight, use $0=v^2-2g\Delta y$; its maximum height above ground is $4.49\ \text{m}$.
3. Solve the free-flight position equation for the descending crossing of $1.83\ \text{m}$. Sam has $1.42\ \text{s}$.

## Why it works

The release point supplies the initial position and velocity for the second phase.

## Issue signals

- `phase-change-initial-velocity-lost`
- `quadratic-root-selection`
- `gravity-sign-error`

# Problem 2.87

## Key concept

Vertical juggling is free fall; both balls have the same downward acceleration after release.

## Worked solution

1. For the first ball, set its maximum rise to $3.0\ \text{m}$: $v_0=7.7\ \text{m/s}$ and rise time $0.78\ \text{s}$.
2. Give the second ball initial speed $\tfrac23v_0$ at that instant.
3. Equate the two vertical position functions. They meet $0.59\ \text{s}$ after the second throw, $1.3\ \text{m}$ above the hand.

## Why it works

Subtracting the two position equations cancels the common gravitational term.

## Issue signals

- `different-release-times-not-modeled`
- `top-of-flight-velocity-not-zero`

# Problem 2.89

## Key concept

Use one constant-acceleration phase for the powered helicopter and a second free-fall phase after shutdown.

## Worked solution

1. Use the $10.0\ \text{s}$ powered interval to find the shutdown height and upward speed.
2. Continue with $a=-g$ to obtain the helicopter's maximum height, $380\ \text{m}$.
3. Apply the jet-pack and free-fall timing conditions in the subsequent phase; the requested separation/position values are $184\ \text{m}$ and the stated associated result.

## Why it works

Changing the engine state changes acceleration, so the motion must be modeled piecewise.

## Issue signals

- `piecewise-motion-not-separated`
- `phase-change-initial-velocity-lost`

# Problem 2.91

## Key concept

The can's initial velocity equals the upward scaffolding speed at the instant it is nudged off.

## Worked solution

1. Set the ground as $y=0$ and solve $0=15.0+v_0(3.25)-\tfrac12g(3.25)^2$ for the release speed.
2. Use $v=v_0-gt$ at impact; its speed is $20.5\ \text{m/s}$.
3. Evaluate the height when the can passes the other painter's hands. It does pass the catch position, so the answer is yes.

## Why it works

“Dropped” from a moving platform does not mean initially at rest relative to the ground.

## Issue signals

- `moving-platform-initial-velocity-ignored`
- `gravity-sign-error`

# Problem 2.93

## Key concept

At release, the canister shares the rocket's current upward velocity; afterward the rocket and canister have different accelerations.

## Worked solution

1. Find the common velocity at $235\ \text{m}$ from the rocket's constant-acceleration motion.
2. Use that velocity in the canister's free-fall equation to find its impact time, while continuing the rocket's accelerated motion for the same time.
3. The rocket is $945\ \text{m}$ high at impact, and the canister's total travel distance is $393\ \text{m}$.

## Why it works

The canister rises after release before falling, so total distance is its rise plus its descent, not simply $235\ \text{m}$.

## Issue signals

- `phase-change-initial-velocity-lost`
- `total-distance-versus-displacement`
- `rocket-and-canister-acceleration-confused`

# Problem 2.95

## Key concept

Set the two position functions equal to find meeting times, then differentiate each position function for velocities.

## Worked solution

1. Compare $x_A(t)$ and $x_B(t)$ just after $t=0$; car A is ahead.
2. Solve $x_A(t)=x_B(t)$, giving $t=2.27\ \text{s}$ and $5.73\ \text{s}$.
3. Substitute into each velocity function for the requested values: $1.00\ \text{s}$ and $4.33\ \text{s}$ at the indicated comparisons, with $2.67\ \text{s}$ for the final requested event.

## Why it works

Position equality identifies meetings; velocity equality would answer a different question.

## Issue signals

- `meeting-condition-uses-velocity`
- `quadratic-root-selection`

# Problem 2.97

## Key concept

The runner has constant velocity; the bus starts from rest with constant acceleration.

## Worked solution

1. Use $x_{\rm runner}=v_rt$ and $x_{\rm bus}=40.0+\tfrac12a_bt^2$.
2. Set the positions equal. The first root gives $t=9.55\ \text{s}$ and $x=47.8\ \text{m}$; the bus speed then is $1.62\ \text{m/s}$.
3. The second root is the later re-meeting after the bus has become faster. The runner does not catch the bus at the reduced proposed speed; the minimum catching speed is $3.69\ \text{m/s}$, at $21.7\ \text{s}$ and $80.0\ \text{m}$.

## Why it works

The two roots of the position equation represent two possible intersections of the motion graphs.

## Issue signals

- `second-quadratic-root-discarded`
- `meeting-condition-uses-velocity`
- `tangent-condition-for-minimum-speed`

# Problem 2.99

## Key concept

Each ball's motion is free fall, but their clocks start one second apart.

## Worked solution

1. Write the first ball's position from its launch time and the second ball's position from its delayed release time.
2. Equate positions only after the second ball exists.
3. The requested results are (a) $8.18\ \text{m/s}$; (b) $0.411\ \text{m}$ and $1.15\ \text{km}$; (c) $9.80\ \text{m/s}$; and (d) $4.90\ \text{m/s}$.

## Why it works

Using the same time origin for both expressions is essential; the delayed ball has no motion before release.

## Issue signals

- `different-release-times-not-modeled`
- `gravity-sign-error`
- `position-equality-versus-velocity-equality`

# Young & Freedman University Physics — Chapter 10 Practice Problems Solutions

> [!note] Worked-solution companion
> Each entry corresponds exactly to a problem heading in the accompanying practice-problems note. The solution paths use the textbook problem data and preserve the diagrams in the prompt note as the visual reference.

# Problem 10.1

## Key concept

The torque magnitude is $\tau=rF\sin\phi$, where $\phi$ is the angle from the position vector to the force; its sign follows the right-hand rule.

## Worked solution

1. In each sketch, identify the perpendicular lever arm or use $\tau=rF\sin\phi$ with $r=4.00\ \text{m}$ and $F=10.0\ \text{N}$.
2. A force through $O$ has zero lever arm and therefore zero torque.
3. For each nonzero case, calculate the magnitude from the appropriate sine factor.
4. Curl the right-hand fingers from the rod's position vector toward the force: counterclockwise is out of the page and clockwise is into the page.

## Why it works

Only the force component perpendicular to the position vector can change the rod's rotational motion about $O$.

## Issue signals

- `torque-angle-misidentified`
- `right-hand-rule-direction-error`

# Problem 10.3

## Key concept

Net torque is the signed sum of the torques from all forces about the pivot.

## Worked solution

1. Take counterclockwise torque as positive.
2. For each force in the figure, determine the shortest perpendicular distance from $O$ to its line of action, or calculate $rF\sin\phi$.
3. Assign a positive sign to a force that tends to turn the plate counterclockwise and a negative sign to one that tends to turn it clockwise.
4. Add the three signed torques to obtain the net torque about the central axis.

## Why it works

Torque is additive, and the direction of the angular-acceleration tendency is determined independently for each force.

## Issue signals

- `torque-sign-error`
- `perpendicular-lever-arm-error`

# Problem 10.5

## Key concept

The vector torque from a force applied at position $\vec r$ is the cross product $\vec\tau=\vec r\times\vec F$.

## Worked solution

1. Draw $\vec r$ from the origin to the force application point and place $\vec F$ at that point.
2. Use the right-hand rule from $\vec r$ toward $\vec F$ to predict the torque direction.
3. Compute the determinant

$$
\vec\tau=
\begin{vmatrix}
\hat{\imath}&\hat{\jmath}&\hat{k}\\
r_x&r_y&r_z\\
F_x&F_y&F_z
\end{vmatrix}.
$$

4. Check that the nonzero component points in the predicted direction.

## Why it works

The cross product automatically selects the force component perpendicular to $\vec r$ and gives the axis-direction of the rotational effect.

## Issue signals

- `cross-product-component-error`
- `right-hand-rule-direction-error`

# Problem 10.9

## Key concept

For constant angular acceleration, net torque and angular acceleration are related by $\tau=I\alpha$.

## Worked solution

1. Since the flywheel starts at rest, calculate $\alpha=\Delta\omega/\Delta t$ from the stated final angular speed and $8.00\ \text{s}$ interval.
2. Convert any rotation rate to rad/s before using it.
3. Multiply by the given moment of inertia: $\tau=I\alpha$.
4. The torque points in the direction that produces the stated increase in angular velocity.

## Why it works

This is the rotational analogue of $F=ma$: a larger inertia requires a larger torque to produce the same angular acceleration.

## Issue signals

- `rpm-to-radians-conversion-error`
- `moment-of-inertia-omitted`

# Problem 10.39

## Key concept

The angular momentum of a rigid body rotating about a fixed axis is $L=I\omega$.

## Worked solution

1. Model the second hand as a slender rod about one end, so $I=\tfrac13ML^2$.
2. Convert $M=6.00\ \text{g}$ to kilograms and $L=15.0\ \text{cm}$ to meters.
3. A second hand completes one revolution in $60.0\ \text{s}$, hence $\omega=2\pi/60.0$.
4. Evaluate $L=I\omega$.

## Why it works

Each element of the hand has the same angular speed but a different linear speed; the rod inertia accounts for that distribution.

## Issue signals

- `wrong-rod-inertia-axis`
- `angular-speed-period-error`

# Problem 10.75

## Key concept

The yo-yo combines translation and rotation, with the no-slip condition $a=b\alpha$ at its axle.

## Worked solution

1. The two disks have total mass $2m$ and total inertia $I=2(\tfrac12mR^2)=mR^2$.
2. Apply Newton's second law to the downward translation:

$$
2mg-T=2ma.
$$

3. Apply the rotational equation about the center: $Tb=I\alpha$.
4. Substitute $\alpha=a/b$ and solve simultaneously:

$$
a=\frac{2gb^2}{R^2+2b^2},\qquad
\alpha=\frac{a}{b},\qquad
T=2m(g-a).
$$

## Why it works

Tension both reduces the downward translational acceleration and provides the torque that spins the yo-yo.

## Issue signals

- `no-slip-constraint-missed`
- `two-disk-inertia-error`

# Problem 10.79

## Key concept

Static friction on the rough slope makes the ball roll without slipping, but the smooth slope cannot change its rotational energy.

## Worked solution

1. For a hollow spherical shell, use $I=\tfrac23MR^2$ and $v=R\omega$ at the bottom.
2. The initial energy $Mgh$ becomes

$$
Mgh=\frac12Mv^2+\frac12\left(\frac23MR^2\right)\frac{v^2}{R^2}
=\frac56Mv^2.
$$

3. On the smooth uphill side, the translational kinetic energy converts to gravitational potential energy, while the rotational kinetic energy remains unchanged.
4. Thus $Mg h'=\tfrac12Mv^2$, giving $h'=\tfrac35h$.

## Why it works

With no friction on the smooth side, there is no torque about the ball's center to slow its spin. Energy is conserved; it is simply partitioned between elevation and continuing rotation.

## Issue signals

- `rolling-kinetic-energy-omitted`
- `friction-role-misunderstood`

# Chapter 4: Motion in Two and Three Dimensions

## 4.1 Displacement and Velocity Vectors
In 2D and 3D, position is described by a position vector $\vec{r}$:
$$ \vec{r} = x\hat{i} + y\hat{j} + z\hat{k} $$
Displacement is the change in the position vector:
$$ \Delta\vec{r} = \vec{r}_f - \vec{r}_i $$
Velocity is the derivative of the position vector:
$$ \vec{v} = \frac{d\vec{r}}{dt} = \frac{dx}{dt}\hat{i} + \frac{dy}{dt}\hat{j} + \frac{dz}{dt}\hat{k} = v_x\hat{i} + v_y\hat{j} + v_z\hat{k} $$

## 4.2 Acceleration Vector
Acceleration is the derivative of the velocity vector:
$$ \vec{a} = \frac{d\vec{v}}{dt} = a_x\hat{i} + a_y\hat{j} + a_z\hat{k} $$
Importantly, because velocity is a vector, an object can accelerate by changing its speed OR by changing its direction (or both).

## 4.3 Projectile Motion
Projectile motion describes an object moving in two dimensions under the influence of gravity alone. The key insight is that the horizontal and vertical motions are completely independent of each other.
- **Horizontal Motion**: Constant velocity ($a_x = 0$).
  $$ x = x_0 + (v_0 \cos \theta)t $$
- **Vertical Motion**: Constant acceleration ($a_y = -g$).
  $$ y = y_0 + (v_0 \sin \theta)t - \frac{1}{2}gt^2 $$
  $$ v_y = v_0 \sin \theta - gt $$

> **Placeholder:** This explanation requires generation of media showing the parabolic trajectory of a projectile and the independence of x and y velocity vectors.

## 4.4 Uniform and Nonuniform Circular Motion
### Uniform Circular Motion
When an object moves in a circle at a constant speed $v$, its velocity vector is constantly changing direction. This requires a **centripetal acceleration** directed toward the center of the circle:
$$ a_c = \frac{v^2}{r} $$
The period $T$ (time for one revolution) is $T = \frac{2\pi r}{v}$.

### Nonuniform Circular Motion
If the speed of the object is also changing, it has a **tangential acceleration** $a_t = \frac{dv}{dt}$ in addition to the radial (centripetal) acceleration $a_r = \frac{v^2}{r}$. The total acceleration is the vector sum: $\vec{a} = \vec{a}_t + \vec{a}_r$.

## 4.5 Relative Motion in One and Two Dimensions
Velocities are relative to the frame of reference from which they are measured. If frame $B$ moves with velocity $\vec{v}_{BA}$ relative to frame $A$, and a particle $P$ moves with velocity $\vec{v}_{PB}$ relative to $B$, then the velocity of $P$ relative to $A$ is:
$$ \vec{v}_{PA} = \vec{v}_{PB} + \vec{v}_{BA} $$
This vector addition applies to planes in crosswinds, boats crossing rivers, etc.

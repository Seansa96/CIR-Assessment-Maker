# Chapter 3: Motion Along a Straight Line

## 3.1 Position, Displacement, and Average Velocity
- **Position ($x$)**: The location of a particle with respect to a chosen reference point (origin).
- **Displacement ($\Delta x$)**: The change in position of the particle. It is a vector quantity.
  $$ \Delta x = x_f - x_i $$
- **Distance**: The total length of the path traveled. It is a scalar quantity and is always positive.
- **Average Velocity ($v_{avg}$)**: The displacement divided by the time interval.
  $$ v_{avg} = \frac{\Delta x}{\Delta t} $$
- **Average Speed**: Total distance traveled divided by the time interval.

## 3.2 Instantaneous Velocity and Speed
- **Instantaneous Velocity ($v$)**: The velocity of a particle at a specific instant in time. It is the derivative of position with respect to time.
  $$ v = \lim_{\Delta t \to 0} \frac{\Delta x}{\Delta t} = \frac{dx}{dt} $$
- **Instantaneous Speed**: The magnitude of the instantaneous velocity.

> **Placeholder:** This explanation requires generation of media showing position-time graphs and the tangent line representing instantaneous velocity.

## 3.3 Average and Instantaneous Acceleration
- **Average Acceleration ($a_{avg}$)**: The change in velocity divided by the time interval.
  $$ a_{avg} = \frac{\Delta v}{\Delta t} $$
- **Instantaneous Acceleration ($a$)**: The derivative of velocity with respect to time (or the second derivative of position).
  $$ a = \frac{dv}{dt} = \frac{d^2x}{dt^2} $$

## 3.4 Motion with Constant Acceleration
When acceleration is constant, the kinematic equations simplify greatly. These four equations are foundational for solving 1D motion problems:
1. $v = v_0 + at$
2. $x = x_0 + v_0 t + \frac{1}{2}at^2$
3. $v^2 = v_0^2 + 2a(x - x_0)$
4. $x - x_0 = \frac{1}{2}(v_0 + v)t$

## 3.5 Free Fall
An important case of constant acceleration is **free fall**. Near the surface of the Earth, any object falling freely (ignoring air resistance) experiences a constant downward acceleration due to gravity:
$$ a = -g \approx -9.8 \, \text{m/s}^2 $$
The standard kinematic equations can be directly applied by substituting $a = -g$ and often using $y$ for vertical displacement.

## 3.6 Finding Velocity and Displacement from Acceleration
If the acceleration is not constant but given as a function of time $a(t)$, we can use integration to find velocity and position:
$$ v(t) = v(0) + \int_0^t a(t') \, dt' $$
$$ x(t) = x(0) + \int_0^t v(t') \, dt' $$

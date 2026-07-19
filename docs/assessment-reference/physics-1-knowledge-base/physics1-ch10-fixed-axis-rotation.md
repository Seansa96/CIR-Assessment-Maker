# Chapter 10: Fixed-Axis Rotation

This chapter explores the kinematics and dynamics of rigid bodies rotating about a fixed axis.

## 10.1 Rotational Variables
The analogy between linear and rotational kinematics:
*   **Angular Position ($\theta$)**: Equivalent to linear position ($x$). Measured in radians.
*   **Angular Velocity ($\omega$)**: The rate of change of angular position. $\omega = \frac{d\theta}{dt}$.
*   **Angular Acceleration ($\alpha$)**: The rate of change of angular velocity. $\alpha = \frac{d\omega}{dt}$.

**Kinematic Equations (for constant $\alpha$):**
*   $\omega = \omega_0 + \alpha t$
*   $\theta = \theta_0 + \omega_0 t + \frac{1}{2} \alpha t^2$
*   $\omega^2 = \omega_0^2 + 2\alpha(\theta - \theta_0)$

## 10.2 Relating Angular and Translational Quantities
For a point at distance $r$ from the axis of rotation:
*   **Arc length / Position**: $s = r\theta$
*   **Tangential Velocity**: $v_t = r\omega$
*   **Tangential Acceleration**: $a_t = r\alpha$
*   **Centripetal Acceleration**: $a_c = \frac{v^2}{r} = r\omega^2$

## 10.3 Moment of Inertia (Rotational Inertia)
*   **Moment of Inertia ($I$)**: The rotational analog of mass. It depends on both the mass of the body and how that mass is distributed relative to the axis of rotation.
*   For discrete particles: $I = \sum m_i r_i^2$
*   For continuous bodies: $I = \int r^2 dm$
*   **Parallel-Axis Theorem**: $I = I_{cm} + Md^2$, where $I_{cm}$ is the moment of inertia through the center of mass, $M$ is total mass, and $d$ is the distance between the parallel axes.

## 10.4 Torque
*   **Torque ($\vec{\tau}$)**: The rotational equivalent of force, measuring the tendency of a force to cause rotation.
*   $\vec{\tau} = \vec{r} \times \vec{F}$
*   Magnitude: $\tau = rF\sin\theta = F_\perp r = F r_\perp$, where $r_\perp$ is the lever arm.

## 10.5 Newton's Second Law for Rotation
The net torque acting on a rigid body is proportional to its angular acceleration.
$$ \sum \tau = I\alpha $$

## 10.6 Rotational Work and Energy
*   **Rotational Kinetic Energy**: $K_{rot} = \frac{1}{2} I\omega^2$
*   **Work done by a torque**: $W = \int \tau d\theta$
*   **Power**: $P = \frac{dW}{dt} = \tau\omega$

## Media Requirements
*   Placeholder: This explanation requires generation of media showing an arbitrary rigid body with an applied force vector $\vec{F}$ at position $\vec{r}$ relative to a pivot, demonstrating the lever arm and the angle $\theta$.

# Chapter 10 Fixed-Axis Rotation

INTRODUCTION 
CHAPTER 10 
Fixed-Axis Rotation 
10.1 Rotational Variables 
10.2 Rotation with Constant Angular Acceleration 
10.3 Relating Angular and Translational Quantities 
10.4 Moment of Inertia and Rotational Kinetic Energy 
10.5 Calculating Moments of Inertia 
10.6 Torque 
10.7 Newton’s Second Law for Rotation 
10.8 Work and Power for Rotational Motion 
In previous chapters, we described motion (kinematics) and how to change motion (dynamics), 
and we defined important concepts such as energy for objects that can be considered as point masses. Point 
masses, by definition, have no shape and so can only undergo translational motion. However, we know from 
everyday life that rotational motion is also very important and that many objects that move have both translation 
and rotation. The wind turbines in our chapter opening image are a prime example of how rotational motion impacts 
our daily lives, as the market for clean energy sources continues to grow. 
We begin to address rotational motion in this chapter, starting with fixed-axis rotation. Fixed-axis rotation describes 
the rotation around a fixed axis of a rigid body; that is, an object that does not deform as it moves. We will show how 
to apply all the ideas we’ve developed up to this point about translational motion to an object rotating around a fixed 
axis. In the next chapter, we extend these ideas to more complex rotational motion, including objects that both 
rotate and translate, and objects that do not have a fixed rotational axis. 
FIGURE 10.1 Brazos wind farm in west Texas. During 2019, wind farms in the United States had an average power output of 34 gigawatts, 
which is enough to power 28 million homes. (credit: modification of work by U.S. Department of Energy) 
CHAPTER OUTLINE 

10.1 Rotational Variables 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Describe the physical meaning of rotational variables as applied to fixed-axis rotation 
• Explain how angular velocity is related to tangential speed 
• Calculate the instantaneous angular velocity given the angular position function 
• Find the angular velocity and angular acceleration in a rotating system 
• Calculate the average angular acceleration when the angular velocity is changing 
• Calculate the instantaneous angular acceleration given the angular velocity function 
So far in this text, we have mainly studied translational motion, including the variables that describe it: 
displacement, velocity, and acceleration. Now we expand our description of motion to rotation—specifically, 
rotational motion about a fixed axis. We will find that rotational motion is described by a set of related variables 
similar to those we used in translational motion. 
Angular Velocity 
Uniform circular motion (discussed previously in Motion in Two and Three Dimensions) is motion in a circle at 
constant speed. Although this is the simplest case of rotational motion, it is very useful for many situations, and we 
use it here to introduce rotational variables. 
In Figure 10.2, we show a particle moving in a circle. The coordinate system is fixed and serves as a frame of 
reference to define the particle’s position. Its position vector from the origin of the circle to the particle sweeps out 
the angle , which increases in the counterclockwise direction as the particle moves along its circular path. The 
angle  is called the angular position of the particle. As the particle moves in its circular path, it also traces an arc 
length s. The particle may complete more than one revolution around the circle, and so the angle  may be greater 
than 
, and the arc length s may be greater than the circumference, 
. 
FIGURE 10.2 A particle follows a circular path. As it moves counterclockwise, it sweeps out a positive angle  with respect to the x-axis and 
traces out an arc length s. 
The angle is related to the radius of the circle and the arc length by 
The angle , the angular position of the particle along its path, has units of radians (rad). There are 
 radians in 
 Note that the radian measure is a ratio of length measurements, and therefore is a dimensionless quantity. As 
the particle moves along its circular path, its angular position changes and it undergoes angular displacements 
We can write infinitesimal displacement tangent to the circle using polar coordinates, as shown in Figure 10.3. 
10.1 
10.2 
10 • Fixed-Axis Rotation
Access for free at openstax.org

FIGURE 10.3 The position vector and arc-length vector both lie in the xy-plane and are perpendicular to each other. Note that as the 
point rotates, the coordinate system also rotates and the directions of the unit vectors change. 
The magnitude of the angular velocity, denoted by , is the time rate of change of the angle  as the particle moves 
in its circular path. The instantaneous angular velocity is defined as the limit in which 
 in the average 
angular velocity 
: 
where  is the angle of rotation (Figure 10.2). The units of angular velocity are radians per second (rad/s). Angular 
velocity can also be referred to as the rotation rate in radians per second. In many situations, we are given the 
rotation rate in revolutions/s or cycles/s. To find the angular velocity, we must multiply revolutions/s by 
, since 
there are 
 radians in one complete revolution. Since the direction of a positive angle in a circle is 
counterclockwise, we take counterclockwise rotations as being positive and clockwise rotations as negative. 
We can see how angular velocity is related to the tangential speed of the particle by differentiating Equation 10.1 
with respect to time. We rewrite Equation 10.1 as 
Taking the derivative with respect to time and noting that the radius r is a constant, we have 
where 
. Here 
 is just the tangential speed 
 of the particle in Figure 10.2. Thus, by using Equation 10.3, 
we arrive at 
That is, the tangential speed of the particle is its angular velocity times the radius of the circle. From Equation 10.4, 
we see that the tangential speed of the particle increases with its distance from the axis of rotation for a constant 
angular velocity. This effect is shown in Figure 10.4. Two particles are placed at different radii on a rotating disk with 
a constant angular velocity. As the disk rotates, the tangential speed increases linearly with the radius from the axis 
of rotation. In Figure 10.4, we see that 
 and 
. But the disk has a constant angular velocity, so 
. This means 
 or 
. Thus, since 
, 
. 
10.3 
10.4 
10.1 • Rotational Variables

FIGURE 10.4 Two particles on a rotating disk have different tangential speeds, depending on their distance to the axis of rotation. 
Up until now, we have discussed the magnitude of the angular velocity 
 which is a scalar quantity—the 
change in angular position with respect to time. The vector 
 is the vector associated with the angular velocity and 
points along the axis of rotation. This is useful because when a rigid body is rotating, we want to know both the axis 
of rotation and the direction that the body is rotating about the axis, clockwise or counterclockwise. The angular 
velocity 
 gives us this information. The angular velocity 
 has a direction determined by what is called the right-
hand rule. The right-hand rule is such that if the fingers of your right hand wrap counterclockwise from the x-axis 
(the direction in which  increases) toward the y-axis, your thumb points in the direction of the positive z-axis 
(Figure 10.5). An angular velocity 
 that points along the positive z-axis therefore corresponds to a 
counterclockwise rotation, whereas an angular velocity 
 that points along the negative z-axis corresponds to a 
clockwise rotation. 
FIGURE 10.5 For counterclockwise rotation in the coordinate system shown, the angular velocity points in the positive z-direction by the 
right-hand-rule. 
One can state a cross product relation to the vector of the tangential velocity as stated in Equation 10.4. Therefore, 
we have 
10.5 
10 • Fixed-Axis Rotation
Access for free at openstax.org

That is, the tangential velocity is the cross product of the angular velocity and the position vector, as shown in Figure 
10.6. From part (a) of this figure, we see that with the angular velocity in the positive z-direction, the rotation in the 
xy-plane is counterclockwise. In part (b), the angular velocity is in the negative z-direction, giving a clockwise 
rotation in the xy-plane. 
FIGURE 10.6 The vectors shown are the angular velocity, position, and tangential velocity. (a) The angular velocity points in the positive 
z-direction, giving a counterclockwise rotation in the xy-plane. (b) The angular velocity points in the negative z-direction, giving a clockwise 
rotation. 
EXAMPLE 10.1 
Rotation of a Flywheel 
A flywheel rotates such that it sweeps out an angle at the rate of 
 radians. The wheel rotates 
counterclockwise when viewed in the plane of the page. (a) What is the angular velocity of the flywheel? (b) What 
direction is the angular velocity? (c) How many radians does the flywheel rotate through in 30 s? (d) What is the 
tangential speed of a point on the flywheel 10 cm from the axis of rotation? 
Strategy 
The functional form of the angular position of the flywheel is given in the problem as 
, so by taking the 
derivative with respect to time, we can find the angular velocity. We use the right-hand rule to find the angular 
velocity. To find the angular displacement of the flywheel during 30 s, we seek the angular displacement 
, where 
the change in angular position is between 0 and 30 s. To find the tangential speed of a point at a distance from the 
axis of rotation, we multiply its distance times the angular velocity of the flywheel. 
Solution 
a. 
. We see that the angular velocity is a constant. 
b. By the right-hand rule, we curl the fingers in the direction of rotation, which is counterclockwise in the plane of 
the page, and the thumb points in the direction of the angular velocity, which is out of the page. 
c. 
. 
d. 
. 
Significance 
In 30 s, the flywheel has rotated through quite a number of revolutions, about 215 if we divide the angular 
displacement by 
. A massive flywheel can be used to store energy in this way, if the losses due to friction are 
minimal. Recent research has considered superconducting bearings on which the flywheel rests, with zero energy 
loss due to friction. 
Angular Acceleration 
We have just discussed angular velocity for uniform circular motion, but not all motion is uniform. Envision an ice 
skater spinning with his arms outstretched—when he pulls his arms inward, his angular velocity increases. Or think 
about a computer’s hard disk slowing to a halt as the angular velocity decreases. We will explore these situations 
10.1 • Rotational Variables

later, but we can already see a need to define an angular acceleration for describing situations where  changes. 
The faster the change in , the greater the angular acceleration. We define the instantaneous angular acceleration 
 as the derivative of angular velocity with respect to time: 
where we have taken the limit of the average angular acceleration, 
 as 
. 
The units of angular acceleration are (rad/s)/s, or 
. 
In the same way as we defined the vector associated with angular velocity 
, we can define , the vector associated 
with angular acceleration (Figure 10.7). If the angular velocity is along the positive z-axis, as in Figure 10.5, and 
is positive, then the angular acceleration  is positive and points along the 
 axis. Similarly, if the angular velocity 
 is along the positive z-axis and 
 is negative, then the angular acceleration is negative and points along the 
axis. 
FIGURE 10.7 The rotation is counterclockwise in both (a) and (b) with the angular velocity in the same direction. (a) The angular 
acceleration is in the same direction as the angular velocity, which increases the rotation rate. (b) The angular acceleration is in the 
opposite direction to the angular velocity, which decreases the rotation rate. 
We can express the tangential acceleration vector as a cross product of the angular acceleration and the position 
vector. This expression can be found by taking the time derivative of 
 and is left as an exercise: 
The vector relationships for the angular acceleration and tangential acceleration are shown in Figure 10.8. 
FIGURE 10.8 (a) The angular acceleration is the positive z-direction and produces a tangential acceleration in a counterclockwise sense. (b) 
The angular acceleration is in the negative z-direction and produces a tangential acceleration in the clockwise sense. 
We can relate the tangential acceleration of a point on a rotating body at a distance from the axis of rotation in the 
same way that we related the tangential speed to the angular velocity. If we differentiate Equation 10.4 with respect 
to time, noting that the radius r is constant, we obtain 
10.6 
10.7 
10 • Fixed-Axis Rotation
Access for free at openstax.org

Thus, the tangential acceleration 
 is the radius times the angular acceleration. Equation 10.4 and Equation 10.8 
are important for the discussion of rolling motion (see Angular Momentum). 
Let’s apply these ideas to the analysis of a few simple fixed-axis rotation scenarios. Before doing so, we present a 
problem-solving strategy that can be applied to rotational kinematics: the description of rotational motion. 
PROBLEM-SOLVING STRATEGY 
Rotational Kinematics 
1. Examine the situation to determine that rotational kinematics (rotational motion) is involved. 
2. Identify exactly what needs to be determined in the problem (identify the unknowns). A sketch of the situation 
is useful. 
3. Make a complete list of what is given or can be inferred from the problem as stated (identify the knowns). 
4. Solve the appropriate equation or equations for the quantity to be determined (the unknown). It can be useful 
to think in terms of a translational analog, because by now you are familiar with the equations of translational 
motion. 
5. Substitute the known values along with their units into the appropriate equation and obtain numerical 
solutions complete with units. Be sure to use units of radians for angles. 
6. Check your answer to see if it is reasonable: Does your answer make sense? 
Now let’s apply this problem-solving strategy to a few specific examples. 
EXAMPLE 10.2 
A Spinning Bicycle Wheel 
A bicycle mechanic mounts a bicycle on the repair stand and starts the rear wheel spinning from rest to a final 
angular velocity of 250 rpm in 5.00 s. (a) Calculate the average angular acceleration in 
. (b) If she now hits the 
brakes, causing an angular acceleration of −87.3 
, how long does it take the wheel to stop? 
Strategy 
The average angular acceleration can be found directly from its definition 
 because the final angular velocity 
and time are given. We see that 
 and 
 is 5.00 s. For part (b), we know the 
angular acceleration and the initial angular velocity. We can find the stopping time by using the definition of average 
angular acceleration and solving for 
, yielding 
Solution 
a. Entering known information into the definition of angular acceleration, we get 
Because 
 is in revolutions per minute (rpm) and we want the standard units of 
 for angular 
acceleration, we need to convert from rpm to rad/s: 
Entering this quantity into the expression for , we get 
10.8 
10.1 • Rotational Variables

b. Here the angular velocity decreases from 26.2 rad/s (250 rpm) to zero, so that 
 is −26.2 rad/s, and  is 
given to be –87.3 
. Thus, 
Significance 
Note that the angular acceleration as the mechanic spins the wheel is small and positive; it takes 5 s to produce an 
appreciable angular velocity. When she hits the brake, the angular acceleration is large and negative. The angular 
velocity quickly goes to zero. 
CHECK YOUR UNDERSTANDING 10.1 
The fan blades on a turbofan jet engine (shown below) accelerate from rest up to a rotation rate of 40.0 rev/s in 20 
s. The increase in angular velocity of the fan is constant in time. (The GE90-110B1 turbofan engine mounted on a 
Boeing 777, as shown, is currently the largest turbofan engine in the world, capable of thrusts of 330–510 kN.) 
(a) What is the average angular acceleration? 
(b) What is the instantaneous angular acceleration at any time during the first 20 s? 
FIGURE 10.9 (credit: “Bubinator”/ Wikimedia Commons) 
EXAMPLE 10.3 
Wind Turbine 
A wind turbine (Figure 10.10) in a wind farm is being shut down for maintenance. It takes 30 s for the turbine to go 
from its operating angular velocity to a complete stop in which the angular velocity function is 
, where  is the time in seconds. If the turbine is rotating counterclockwise 
looking into the page, (a) what are the directions of the angular velocity and acceleration vectors? (b) What is the 
average angular acceleration? (c) What is the instantaneous angular acceleration at 
10 • Fixed-Axis Rotation
Access for free at openstax.org

FIGURE 10.10 A wind turbine that is rotating counterclockwise, as seen head on. 
Strategy 
a. We are given the rotational sense of the turbine, which is counterclockwise in the plane of the page. Using the 
right hand rule (Figure 10.5), we can establish the directions of the angular velocity and acceleration vectors. 
b. We calculate the initial and final angular velocities to get the average angular acceleration. We establish the 
sign of the angular acceleration from the results in (a). 
c. We are given the functional form of the angular velocity, so we can find the functional form of the angular 
acceleration function by taking its derivative with respect to time. 
Solution 
a. Since the turbine is rotating counterclockwise, angular velocity 
 points out of the page. But since the angular 
velocity is decreasing, the angular acceleration  points into the page, in the opposite sense to the angular 
velocity. 
b. The initial angular velocity of the turbine, setting 
. The final angular velocity is zero, so 
the average angular acceleration is 
c. Taking the derivative of the angular velocity with respect to time gives 
Significance 
We found from the calculations in (a) and (b) that the angular acceleration  and the average angular acceleration 
are negative. The turbine has an angular acceleration in the opposite sense to its angular velocity. 
We now have a basic vocabulary for discussing fixed-axis rotational kinematics and relationships between rotational 
variables. We discuss more definitions and connections in the next section. 
10.1 • Rotational Variables

10.2 Rotation with Constant Angular Acceleration 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Derive the kinematic equations for rotational motion with constant angular acceleration 
• Select from the kinematic equations for rotational motion with constant angular acceleration the 
appropriate equations to solve for unknowns in the analysis of systems undergoing fixed-axis rotation 
• Use solutions found with the kinematic equations to verify the graphical analysis of fixed-axis rotation 
with constant angular acceleration 
In the preceding section, we defined the rotational variables of angular displacement, angular velocity, and angular 
acceleration. In this section, we work with these definitions to derive relationships among these variables and use 
these relationships to analyze rotational motion for a rigid body about a fixed axis under a constant angular 
acceleration. This analysis forms the basis for rotational kinematics. If the angular acceleration is constant, the 
equations of rotational kinematics simplify, similar to the equations of linear kinematics discussed in Motion along a 
Straight Line and Motion in Two and Three Dimensions. We can then use this simplified set of equations to describe 
many applications in physics and engineering where the angular acceleration of the system is constant. Rotational 
kinematics is also a prerequisite to the discussion of rotational dynamics later in this chapter. 
Kinematics of Rotational Motion 
Using our intuition, we can begin to see how the rotational quantities 
 
 , and t are related to one another. For 
example, we saw in the preceding section that if a flywheel has an angular acceleration in the same direction as its 
angular velocity vector, its angular velocity increases with time and its angular displacement also increases. On the 
contrary, if the angular acceleration is opposite to the angular velocity vector, its angular velocity decreases with 
time. We can describe these physical situations and many others with a consistent set of rotational kinematic 
equations under a constant angular acceleration. The method to investigate rotational motion in this way is called 
kinematics of rotational motion. 
To begin, we note that if the system is rotating under a constant acceleration, then the average angular velocity 
follows a simple relation because the angular velocity is increasing linearly with time. The average angular velocity is 
just half the sum of the initial and final values: 
From the definition of the average angular velocity, we can find an equation that relates the angular position, 
average angular velocity, and time: 
Solving for , we have 
where we have set 
. This equation can be very useful if we know the average angular velocity of the system. 
Then we could find the angular displacement over a given time period. Next, we find an equation relating , , and t. 
To determine this equation, we start with the definition of angular acceleration: 
We rearrange this to get 
 and then we integrate both sides of this equation from initial values to final 
values, that is, from 
 to t and 
. In uniform rotational motion, the angular acceleration is constant so it can 
be pulled out of the integral, yielding two definite integrals: 
10.9 
10.10 
10 • Fixed-Axis Rotation
Access for free at openstax.org

Setting 
, we have 
We rearrange this to obtain 
where 
 is the initial angular velocity. Equation 10.11 is the rotational counterpart to the linear kinematics 
equation 
. With Equation 10.11, we can find the angular velocity of an object at any specified time t 
given the initial angular velocity and the angular acceleration. 
Let’s now do a similar treatment starting with the equation 
. We rearrange it to obtain 
 and 
integrate both sides from initial to final values again, noting that the angular acceleration is constant and does not 
have a time dependence. However, this time, the angular velocity is not constant (in general), so we substitute in 
what we derived above: 
where we have set 
. Now we rearrange to obtain 
Equation 10.12 is the rotational counterpart to the linear kinematics equation found in Motion Along a Straight Line 
for position as a function of time. This equation gives us the angular position of a rotating rigid body at any time t 
given the initial conditions (initial angular position and initial angular velocity) and the angular acceleration. 
We can find an equation that is independent of time by solving for t in Equation 10.11 and substituting into Equation 
10.12. Equation 10.12 becomes 
or 
Equation 10.10 through Equation 10.13 describe fixed-axis rotation for constant acceleration and are summarized 
in Table 10.1. 
10.11 
10.12 
10.13 
10.2 • Rotation with Constant Angular Acceleration

Angular displacement from average angular velocity 
Angular velocity from angular acceleration 
Angular displacement from angular velocity and angular acceleration 
Angular velocity from angular displacement and angular acceleration 
TABLE 10.1 Kinematic Equations 
Applying the Equations for Rotational Motion 
Now we can apply the key kinematic relations for rotational motion to some simple examples to get a feel for how 
the equations can be applied to everyday situations. 
EXAMPLE 10.4 
Calculating the Acceleration of a Fishing Reel 
A deep-sea fisherman hooks a big fish that swims away from the boat, pulling the fishing line from his fishing reel. 
The whole system is initially at rest, and the fishing line unwinds from the reel at a radius of 4.50 cm from its axis of 
rotation. The reel is given an angular acceleration of 
 for 2.00 s (Figure 10.11). 
(a) What is the final angular velocity of the reel after 2 s? 
(b) How many revolutions does the reel make? 
FIGURE 10.11 Fishing line coming off a rotating reel moves linearly. 
Strategy 
Identify the knowns and compare with the kinematic equations for constant acceleration. Look for the appropriate 
equation that can be solved for the unknown, using the knowns given in the problem description. 
Solution 
a. We are given  and t and want to determine . The most straightforward equation to use is 
, 
since all terms are known besides the unknown variable we are looking for. We are given that 
 (it starts 
from rest), so 
b. We are asked to find the number of revolutions. Because 
, we can find the number of 
revolutions by finding  in radians. We are given  and t, and we know 
 is zero, so we can obtain  by using 
10 • Fixed-Axis Rotation
Access for free at openstax.org

Converting radians to revolutions gives 
Significance 
This example illustrates that relationships among rotational quantities are highly analogous to those among linear 
quantities. The answers to the questions are realistic. After unwinding for two seconds, the reel is found to spin at 
220 rad/s, which is 2100 rpm. (No wonder reels sometimes make high-pitched sounds.) 
In the preceding example, we considered a fishing reel with a positive angular acceleration. Now let us consider 
what happens with a negative angular acceleration. 
EXAMPLE 10.5 
Calculating the Duration When the Fishing Reel Slows Down and Stops 
Now the fisherman applies a brake to the spinning reel, achieving an angular acceleration of 
. How long 
does it take the reel to come to a stop? 
Strategy 
We are asked to find the time t for the reel to come to a stop. The initial and final conditions are different from those 
in the previous problem, which involved the same fishing reel. Now we see that the initial angular velocity is 
 and the final angular velocity  is zero. The angular acceleration is given as 
Examining the available equations, we see all quantities but t are known in 
, making it easiest to use 
this equation. 
Solution 
The equation states 
We solve the equation algebraically for t and then substitute the known values as usual, yielding 
Significance 
Note that care must be taken with the signs that indicate the directions of various quantities. Also, note that the time 
to stop the reel is fairly small because the acceleration is rather large. Fishing lines sometimes snap because of the 
accelerations involved, and fishermen often let the fish swim for a while before applying brakes on the reel. A tired 
fish is slower, requiring a smaller acceleration. 
CHECK YOUR UNDERSTANDING 10.2 
A centrifuge used in DNA extraction spins at a maximum rate of 7000 rpm, producing a “g-force” on the sample that 
is 6000 times the force of gravity. If the centrifuge takes 10 seconds to come to rest from the maximum spin rate: 
(a) What is the angular acceleration of the centrifuge? (b) What is the angular displacement of the centrifuge during 
this time? 
10.2 • Rotation with Constant Angular Acceleration

EXAMPLE 10.6 
Angular Acceleration of a Propeller 
Figure 10.12 shows a graph of the angular velocity of a propeller on an aircraft as a function of time. Its angular 
velocity starts at 30 rad/s and drops linearly to 0 rad/s over the course of 5 seconds. (a) Find the angular 
acceleration of the object and verify the result using the kinematic equations. (b) Find the angle through which the 
propeller rotates during these 5 seconds and verify your result using the kinematic equations. 
FIGURE 10.12 A graph of the angular velocity of a propeller versus time. 
Strategy 
a. Since the angular velocity varies linearly with time, we know that the angular acceleration is constant and 
does not depend on the time variable. The angular acceleration is the slope of the angular velocity vs. time 
graph, 
. To calculate the slope, we read directly from Figure 10.12, and see that 
 at 
 and 
 at 
. Then, we can verify the result using 
. 
b. We use the equation 
 since the time derivative of the angle is the angular velocity, we can find the 
angular displacement by integrating the angular velocity, which from the figure means taking the area under 
the angular velocity graph. In other words: 
Then we use the kinematic equations for constant acceleration to verify the result. 
Solution 
a. Calculating the slope, we get 
We see that this is exactly Equation 10.11 with a little rearranging of terms. 
b. We can find the area under the curve by calculating the area of the right triangle, as shown in Figure 10.13. 
10 • Fixed-Axis Rotation
Access for free at openstax.org

FIGURE 10.13 The area under the curve is the area of the right triangle. 
We verify the solution using Equation 10.12: 
Setting 
, we have 
This verifies the solution found from finding the area under the curve. 
Significance 
We see from part (b) that there are alternative approaches to analyzing fixed-axis rotation with constant 
acceleration. We started with a graphical approach and verified the solution using the rotational kinematic 
equations. Since 
, we could do the same graphical analysis on an angular acceleration-vs.-time curve. The 
area under an 
 curve gives us the change in angular velocity. Since the angular acceleration is constant in this 
section, this is a straightforward exercise. 
10.3 Relating Angular and Translational Quantities 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Given the linear kinematic equation, write the corresponding rotational kinematic equation 
• Calculate the linear distances, velocities, and accelerations of points on a rotating system given the 
angular velocities and accelerations 
In this section, we relate each of the rotational variables to the translational variables defined in Motion Along a 
Straight Line and Motion in Two and Three Dimensions. This will complete our ability to describe rigid-body 
rotations. 
Angular vs. Linear Variables 
In Rotational Variables, we introduced angular variables. If we compare the rotational definitions with the 
definitions of linear kinematic variables from Motion Along a Straight Line and Motion in Two and Three Dimensions, 
we find that there is a mapping of the linear variables to the rotational ones. Linear position, velocity, and 
acceleration have their rotational counterparts, as we can see when we write them side by side: 
10.3 • Relating Angular and Translational Quantities

Linear 
Rotational 
Position 
x 
Velocity 
Acceleration 
Let’s compare the linear and rotational variables individually. The linear variable of position has physical units of 
meters, whereas the angular position variable has dimensionless units of radians, as can be seen from the definition 
of 
, which is the ratio of two lengths. The linear velocity has units of m/s, and its counterpart, the angular 
velocity, has units of rad/s. In Rotational Variables, we saw in the case of circular motion that the linear tangential 
speed of a particle at a radius r from the axis of rotation is related to the angular velocity by the relation 
. 
This could also apply to points on a rigid body rotating about a fixed axis. Here, we consider only circular motion. In 
circular motion, both uniform and nonuniform, there exists a centripetal acceleration (Motion in Two and Three 
Dimensions). The centripetal acceleration vector points inward from the particle executing circular motion toward 
the axis of rotation. The derivation of the magnitude of the centripetal acceleration is given in Motion in Two and 
Three Dimensions. From that derivation, the magnitude of the centripetal acceleration was found to be 
where r is the radius of the circle. 
Thus, in uniform circular motion when the angular velocity is constant and the angular acceleration is zero, we have 
a linear acceleration—that is, centripetal acceleration—since the tangential speed in Equation 10.14 is a constant. If 
nonuniform circular motion is present, the rotating system has an angular acceleration, and we have both a linear 
centripetal acceleration that is changing (because 
 is changing) as well as a linear tangential acceleration. These 
relationships are shown in Figure 10.14, where we show the centripetal and tangential accelerations for uniform 
and nonuniform circular motion. 
FIGURE 10.14 (a) Uniform circular motion: The centripetal acceleration 
 has its vector inward toward the axis of rotation. There is no 
tangential acceleration. (b) Nonuniform circular motion: An angular acceleration produces an inward centripetal acceleration that is 
changing in magnitude, plus a tangential acceleration 
. 
The centripetal acceleration is due to the change in the direction of tangential velocity, whereas the tangential 
10.14 
10 • Fixed-Axis Rotation
Access for free at openstax.org

acceleration is due to any change in the magnitude of the tangential velocity. The tangential and centripetal 
acceleration vectors 
 and 
 are always perpendicular to each other, as seen in Figure 10.14. To complete this 
description, we can assign a total linear acceleration vector to a point on a rotating rigid body or a particle 
executing circular motion at a radius r from a fixed axis. The total linear acceleration vector  is the vector sum of 
the centripetal and tangential accelerations, 
The total linear acceleration vector in the case of nonuniform circular motion points at an angle between the 
centripetal and tangential acceleration vectors, as shown in Figure 10.15. Since 
, the magnitude of the total 
linear acceleration is 
Note that if the angular acceleration is zero, the total linear acceleration is equal to the centripetal acceleration. 
FIGURE 10.15 A particle is executing circular motion and has an angular acceleration. The total linear acceleration of the particle is the 
vector sum of the centripetal acceleration and tangential acceleration vectors. The total linear acceleration vector is at an angle in between 
the centripetal and tangential accelerations. 
Relationships between Rotational and Translational Motion 
We can look at two relationships between rotational and translational motion. 
1. Generally speaking, the linear kinematic equations have their rotational counterparts. Table 10.2 lists the four 
linear kinematic equations and the corresponding rotational counterpart. The two sets of equations look 
similar to each other, but describe two different physical situations, that is, rotation and translation. 
Rotational 
Translational 
TABLE 10.2 Rotational and Translational Kinematic 
Equations 
2. The second correspondence has to do with relating linear and rotational variables in the special case of 
circular motion. This is shown in Table 10.3, where in the third column, we have listed the connecting equation 
that relates the linear variable to the rotational variable. The rotational variables of angular velocity and 
10.15 
10.3 • Relating Angular and Translational Quantities

acceleration have subscripts that indicate their definition in circular motion. 
Rotational 
Translational 
Relationship (
) 
s 
 
TABLE 10.3 Rotational and Translational Quantities: Circular Motion 
EXAMPLE 10.7 
Linear Acceleration of a Centrifuge 
A centrifuge has a radius of 20 cm and accelerates from a maximum rotation rate of 10,000 rpm to rest in 30 
seconds under a constant angular acceleration. It is rotating counterclockwise. What is the magnitude of the total 
acceleration of a point at the tip of the centrifuge at 
 What is the direction of the total acceleration vector? 
Strategy 
With the information given, we can calculate the angular acceleration, which then will allow us to find the tangential 
acceleration. We can find the centripetal acceleration at 
 by calculating the tangential speed at this time. With 
the magnitudes of the accelerations, we can calculate the total linear acceleration. From the description of the 
rotation in the problem, we can sketch the direction of the total acceleration vector. 
Solution 
The angular acceleration is 
Therefore, the tangential acceleration is 
The angular velocity at 
 is 
Thus, the tangential speed at 
 is 
We can now calculate the centripetal acceleration at 
: 
Since the two acceleration vectors are perpendicular to each other, the magnitude of the total linear acceleration is 
Since the centrifuge has a negative angular acceleration, it is slowing down. The total acceleration vector is as 
shown in Figure 10.16. The angle with respect to the centripetal acceleration vector is 
10 • Fixed-Axis Rotation
Access for free at openstax.org

The negative sign means that the total acceleration vector is angled toward the clockwise direction. 
FIGURE 10.16 The centripetal, tangential, and total acceleration vectors. The centrifuge is slowing down, so the tangential acceleration is 
clockwise, opposite the direction of rotation (counterclockwise). 
Significance 
From Figure 10.16, we see that the tangential acceleration vector is opposite the direction of rotation. The 
magnitude of the tangential acceleration is much smaller than the centripetal acceleration, so the total linear 
acceleration vector will make a very small angle with respect to the centripetal acceleration vector. 
CHECK YOUR UNDERSTANDING 10.3 
A boy jumps on a merry-go-round with a radius of 5 m that is at rest. It starts accelerating at a constant rate up to an 
angular velocity of 5 rad/s in 20 seconds. What is the distance travelled by the boy? 
INTERACTIVE 
Check out this PhET simulation (https://openstax.org/l/28ladybugrevolutionrotation) to change the parameters of a 
rotating disk (the initial angle, angular velocity, and angular acceleration), and place bugs at different radial 
distances from the axis. The simulation then lets you explore how circular motion relates to the bugs’ xy-position, 
velocity, and acceleration using vectors or graphs. 
10.4 Moment of Inertia and Rotational Kinetic Energy 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Describe the differences between rotational and translational kinetic energy 
• Define the physical concept of moment of inertia in terms of the mass distribution from the rotational axis 
• Explain how the moment of inertia of rigid bodies affects their rotational kinetic energy 
• Use conservation of mechanical energy to analyze systems undergoing both rotation and translation 
• Calculate the angular velocity of a rotating system when there are energy losses due to nonconservative 
forces 
So far in this chapter, we have been working with rotational kinematics: the description of motion for a rotating rigid 
body with a fixed axis of rotation. In this section, we define two new quantities that are helpful for analyzing 
properties of rotating objects: moment of inertia and rotational kinetic energy. With these properties defined, we will 
10.4 • Moment of Inertia and Rotational Kinetic Energy

have two important tools we need for analyzing rotational dynamics. 
Rotational Kinetic Energy 
Any moving object has kinetic energy. We know how to calculate this for a body undergoing translational motion, but 
how about for a rigid body undergoing rotation? This might seem complicated because each point on the rigid body 
has a different velocity. However, we can make use of angular velocity—which is the same for the entire rigid 
body—to express the kinetic energy for a rotating object. Figure 10.17 shows an example of a very energetic rotating 
body: an electric grindstone propelled by a motor. Sparks are flying, and noise and vibration are generated as the 
grindstone does its work. This system has considerable energy, some of it in the form of heat, light, sound, and 
vibration. However, most of this energy is in the form of rotational kinetic energy. 
FIGURE 10.17 The rotational kinetic energy of the grindstone is converted to heat, light, sound, and vibration. (credit: Zachary David Bell, 
US Navy) 
Energy in rotational motion is not a new form of energy; rather, it is the energy associated with rotational motion, the 
same as kinetic energy in translational motion. However, because kinetic energy is given by 
, and 
velocity is a quantity that is different for every point on a rotating body about an axis, it makes sense to find a way to 
write kinetic energy in terms of the variable , which is the same for all points on a rigid rotating body. For a single 
particle rotating around a fixed axis, this is straightforward to calculate. We can relate the angular velocity to the 
magnitude of the translational velocity using the relation 
, where r is the distance of the particle from the 
axis of rotation and 
 is its tangential speed. Substituting into the equation for kinetic energy, we find 
In the case of a rigid rotating body, we can divide up any body into a large number of smaller masses, each with a 
mass 
 and distance to the axis of rotation 
, such that the total mass of the body is equal to the sum of the 
individual masses: 
. Each smaller mass has tangential speed 
, where we have dropped the subscript t 
for the moment. The total kinetic energy of the rigid rotating body is 
and since 
 for all masses, 
10 • Fixed-Axis Rotation
Access for free at openstax.org

The units of Equation 10.16 are joules (J). The equation in this form is complete, but awkward; we need to find a 
way to generalize it. 
Moment of Inertia 
If we compare Equation 10.16 to the way we wrote kinetic energy in Work and Kinetic Energy, 
, this 
suggests we have a new rotational variable to add to our list of our relations between rotational and translational 
variables. The quantity 
 is the counterpart for mass in the equation for rotational kinetic energy. This is an 
important new term for rotational motion. This quantity is called the moment of inertia I, with units of 
: 
For now, we leave the expression in summation form, representing the moment of inertia of a system of point 
particles rotating about a fixed axis. We note that the moment of inertia of a single point particle about a fixed axis is 
simply 
, with r being the distance from the point particle to the axis of rotation. In the next section, we explore 
the integral form of this equation, which can be used to calculate the moment of inertia of some regular-shaped rigid 
bodies. 
The moment of inertia is the quantitative measure of rotational inertia, just as in translational motion, and mass is 
the quantitative measure of linear inertia—that is, the more massive an object is, the more inertia it has, and the 
greater is its resistance to change in linear velocity. Similarly, the greater the moment of inertia of a rigid body or 
system of particles, the greater is its resistance to change in angular velocity about a fixed axis of rotation. It is 
interesting to see how the moment of inertia varies with r, the distance to the axis of rotation of the mass particles in 
Equation 10.17. Rigid bodies and systems of particles with more mass concentrated at a greater distance from the 
axis of rotation have greater moments of inertia than bodies and systems of the same mass, but concentrated near 
the axis of rotation. In this way, we can see that a hollow cylinder has more rotational inertia than a solid cylinder of 
the same mass when rotating about an axis through the center. Substituting Equation 10.17 into Equation 10.16, the 
expression for the kinetic energy of a rotating rigid body becomes 
We see from this equation that the kinetic energy of a rotating rigid body is directly proportional to the moment of 
inertia and the square of the angular velocity. This is exploited in flywheel energy-storage devices, which are 
designed to store large amounts of rotational kinetic energy. Many carmakers are now testing flywheel energy 
storage devices in their automobiles, such as the flywheel, or kinetic energy recovery system, shown in Figure 
10.18. 
10.16 
10.17 
10.18 
10.4 • Moment of Inertia and Rotational Kinetic Energy

FIGURE 10.18 A KERS (kinetic energy recovery system) flywheel used in cars. (credit: “cmonville”/Flickr) 
The rotational and translational quantities for kinetic energy and inertia are summarized in Table 10.4. The 
relationship column is not included because a constant doesn’t exist by which we could multiply the rotational 
quantity to get the translational quantity, as can be done for the variables in Table 10.3. 
Rotational 
Translational 
TABLE 10.4 Rotational and 
Translational Kinetic Energies and 
Inertia 
EXAMPLE 10.8 
Moment of Inertia of a System of Particles 
Six small washers are spaced 10 cm apart on a rod of negligible mass and 0.5 m in length. The mass of each washer 
is 20 g. The rod rotates about an axis located at 25 cm, as shown in Figure 10.19. (a) What is the moment of inertia 
of the system? (b) If the two washers closest to the axis are removed, what is the moment of inertia of the remaining 
four washers? (c) If the system with six washers rotates at 5 rev/s, what is its rotational kinetic energy? 
10 • Fixed-Axis Rotation
Access for free at openstax.org

FIGURE 10.19 Six washers are spaced 10 cm apart on a rod of negligible mass and rotating about a vertical axis. 
Strategy 
a. We use the definition for moment of inertia for a system of particles and perform the summation to evaluate 
this quantity. The masses are all the same so we can pull that quantity in front of the summation symbol. 
b. We do a similar calculation. 
c. We insert the result from (a) into the expression for rotational kinetic energy. 
Solution 
a. 
. 
b. 
. 
c. 
. 
Significance 
We can see the individual contributions to the moment of inertia. The masses close to the axis of rotation have a 
very small contribution. When we removed them, it had a very small effect on the moment of inertia. 
In the next section, we generalize the summation equation for point particles and develop a method to calculate 
moments of inertia for rigid bodies. For now, though, Figure 10.20 gives values of moment of inertia for common 
object shapes around specified axes. 
10.4 • Moment of Inertia and Rotational Kinetic Energy

FIGURE 10.20 Moment of inertia for common shapes of objects. 
Applying Rotational Kinetic Energy 
Now let’s apply the ideas of rotational kinetic energy and the moment of inertia table to get a feeling for the energy 
associated with a few rotating objects. The following examples will also help get you comfortable using these 
equations. First, let’s look at a general problem-solving strategy for rotational energy. 
PROBLEM-SOLVING STRATEGY 
Rotational Energy 
1. Determine that energy or work is involved in the rotation. 
2. Determine the system of interest. A sketch usually helps. 
3. Analyze the situation to determine the types of work and energy involved. 
4. If there are no losses of energy due to friction and other nonconservative forces, mechanical energy is 
conserved, that is, 
. 
5. If nonconservative forces are present, mechanical energy is not conserved, and other forms of energy, such as 
heat and light, may enter or leave the system. Determine what they are and calculate them as necessary. 
6. Eliminate terms wherever possible to simplify the algebra. 
7. Evaluate the numerical solution to see if it makes sense in the physical situation presented in the wording of 
the problem. 
10 • Fixed-Axis Rotation
Access for free at openstax.org

EXAMPLE 10.9 
Calculating Helicopter Energies 
A typical small rescue helicopter has four blades: Each is 4.00 m long and has a mass of 50.0 kg (Figure 10.21). The 
blades can be approximated as thin rods that rotate about one end of an axis perpendicular to their length. The 
helicopter has a total loaded mass of 1000 kg. (a) Calculate the rotational kinetic energy in the blades when they 
rotate at 300 rpm. (b) Calculate the translational kinetic energy of the helicopter when it flies at 20.0 m/s, and 
compare it with the rotational energy in the blades. 
FIGURE 10.21 (a) Sketch of a four-blade helicopter. (b) A water rescue operation featuring a helicopter from the Auckland Westpac Rescue 
Helicopter Service. (credit b: modification of work by “111 Emergency”/Flickr) 
Strategy 
Rotational and translational kinetic energies can be calculated from their definitions. The wording of the problem 
gives all the necessary constants to evaluate the expressions for the rotational and translational kinetic energies. 
Solution 
a. The rotational kinetic energy is 
We must convert the angular velocity to radians per second and calculate the moment of inertia before we can 
find K. The angular velocity  is 
The moment of inertia of one blade is that of a thin rod rotated about its end, listed in Figure 10.20. The total I 
is four times this moment of inertia because there are four blades. Thus, 
Entering  and I into the expression for rotational kinetic energy gives 
b. Entering the given values into the equation for translational kinetic energy, we obtain 
To compare kinetic energies, we take the ratio of translational kinetic energy to rotational kinetic energy. This 
ratio is 
10.4 • Moment of Inertia and Rotational Kinetic Energy

Significance 
The ratio of translational energy to rotational kinetic energy is only 0.380. This ratio tells us that most of the kinetic 
energy of the helicopter is in its spinning blades. 
EXAMPLE 10.10 
Energy in a Baton 
A person hurls a baton into the air with a velocity of 30.0 m/s at an angle of 
 with respect to the horizontal 
(Figure 10.22). It has a mass of 1.0 kg and is rotating at 10.0 rev/s. The moment of inertia of the baton is given as 
 where 
. (a) What is the total energy of the baton when it leaves the hand? (b) How high does 
the baton go from the elevation of the hand, neglecting air resistance? 
FIGURE 10.22 A baton is hurled into the air at an initial angle of 
. 
Strategy 
We use the definitions of rotational and linear kinetic energy to find the total energy of the system. The problem 
states to neglect air resistance, so we don’t have to worry about energy loss. In part (b), we use conservation of 
mechanical energy to find the maximum height of the baton. 
Solution 
a. Moment of inertia: 
. 
Angular velocity: 
. 
The rotational kinetic energy is therefore 
The translational kinetic energy is 
Thus, the total energy in the baton is 
b. We use conservation of mechanical energy. Since the baton is launched at an angle, we need to write the total 
energies of the system in terms of its linear kinetic energies using the velocity in the x- and y-directions. The 
total energy when the baton leaves the hand is 
10 • Fixed-Axis Rotation
Access for free at openstax.org

The total energy at maximum height is 
By conservation of mechanical energy, 
 so we have, after canceling like terms, 
Since 
, we find 
Significance 
In part (b), the solution demonstrates how energy conservation is an alternative method to solve a problem that 
normally would be solved using kinematics. In the absence of air resistance, the rotational kinetic energy was not a 
factor in the solution for the maximum height. 
CHECK YOUR UNDERSTANDING 10.4 
A nuclear submarine propeller has a moment of inertia of 
. If the submerged propeller has a rotation 
rate of 4.0 rev/s when the engine is cut, what is the rotation rate of the propeller after 5.0 s when water resistance 
has taken 50,000 J out of the system? 
10.5 Calculating Moments of Inertia 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Calculate the moment of inertia for uniformly shaped, rigid bodies 
• Apply the parallel axis theorem to find the moment of inertia about any axis parallel to one already known 
• Calculate the moment of inertia for compound objects 
In the preceding section, we defined the moment of inertia but did not show how to calculate it. In this section, we 
show how to calculate the moment of inertia for several standard types of objects, as well as how to use known 
moments of inertia to find the moment of inertia for a shifted axis or for a compound object. This section is very 
useful for seeing how to apply a general equation to complex objects (a skill that is critical for more advanced 
physics and engineering courses). 
Moment of Inertia 
We defined the moment of inertia I of an object to be 
 for all the point masses that make up the object. 
Because r is the distance to the axis of rotation from each piece of mass that makes up the object, the moment of 
inertia for any object depends on the chosen axis. To see this, let’s take a simple example of two masses at the end 
of a massless (negligibly small mass) rod (Figure 10.23) and calculate the moment of inertia about two different 
axes. In this case, the summation over the masses is simple because the two masses at the end of the barbell can 
be approximated as point masses, and the sum therefore has only two terms. 
In the case with the axis in the center of the barbell, each of the two masses m is a distance R away from the axis, 
giving a moment of inertia of 
In the case with the axis at the end of the barbell—passing through one of the masses—the moment of inertia is 
10.5 • Calculating Moments of Inertia

From this result, we can conclude that it is twice as hard to rotate the barbell about the end than about its center. 
FIGURE 10.23 (a) A barbell with an axis of rotation through its center; (b) a barbell with an axis of rotation through one end. 
In this example, we had two point masses and the sum was simple to calculate. However, to deal with objects that 
are not point-like, we need to think carefully about each of the terms in the equation. The equation asks us to sum 
over each ‘piece of mass’ a certain distance from the axis of rotation. But what exactly does each ‘piece of mass’ 
mean? Recall that in our derivation of this equation, each piece of mass had the same magnitude of velocity, which 
means the whole piece had to have a single distance r to the axis of rotation. However, this is not possible unless we 
take an infinitesimally small piece of mass dm, as shown in Figure 10.24. 
FIGURE 10.24 Using an infinitesimally small piece of mass to calculate the contribution to the total moment of inertia. 
The need to use an infinitesimally small piece of mass dm suggests that we can write the moment of inertia by 
evaluating an integral over infinitesimal masses rather than doing a discrete sum over finite masses: 
This, in fact, is the form we need to generalize the equation for complex shapes. It is best to work out specific 
examples in detail to get a feel for how to calculate the moment of inertia for specific shapes. This is the focus of 
most of the rest of this section. 
A uniform thin rod with an axis through the center 
Consider a uniform (density and shape) thin rod of mass M and length L as shown in Figure 10.25. We want a thin 
rod so that we can assume the cross-sectional area of the rod is small and the rod can be thought of as a string of 
masses along a one-dimensional straight line. In this example, the axis of rotation is perpendicular to the rod and 
passes through the midpoint for simplicity. Our task is to calculate the moment of inertia about this axis. We orient 
the axes so that the z-axis is the axis of rotation and the x-axis passes through the length of the rod, as shown in the 
10.19 
10 • Fixed-Axis Rotation
Access for free at openstax.org

figure. This is a convenient choice because we can then integrate along the x-axis. 
FIGURE 10.25 Calculation of the moment of inertia I for a uniform thin rod about an axis through the center of the rod. 
We define dm to be a small element of mass making up the rod. The moment of inertia integral is an integral over 
the mass distribution. However, we know how to integrate over space, not over mass. We therefore need to find a 
way to relate mass to spatial variables. We do this using the linear mass density  of the object, which is the mass 
per unit length. Since the mass density of this object is uniform, we can write 
If we take the differential of each side of this equation, we find 
since  is constant. We chose to orient the rod along the x-axis for convenience—this is where that choice becomes 
very helpful. Note that a piece of the rod dl lies completely along the x-axis and has a length dx; in fact, 
 in 
this situation. We can therefore write 
, giving us an integration variable that we know how to deal with. 
The distance of each piece of mass dm from the axis is given by the variable x, as shown in the figure. Putting this all 
together, we obtain 
The last step is to be careful about our limits of integration. The rod extends from 
 to 
, since the 
axis is in the middle of the rod at 
. This gives us 
Next, we calculate the moment of inertia for the same uniform thin rod but with a different axis choice so we can 
compare the results. We would expect the moment of inertia to be smaller about an axis through the center of mass 
than the endpoint axis, just as it was for the barbell example at the start of this section. This happens because more 
mass is distributed farther from the axis of rotation. 
A uniform thin rod with axis at the end 
Now consider the same uniform thin rod of mass M and length L, but this time we move the axis of rotation to the 
end of the rod. We wish to ﬁnd the moment of inertia about this new axis (Figure 10.26). The quantity dm is again 
defined to be a small element of mass making up the rod. Just as before, we obtain 
However, this time we have different limits of integration. The rod extends from 
 to 
, since the axis is at 
the end of the rod at 
. Therefore we find 
10.5 • Calculating Moments of Inertia

FIGURE 10.26 Calculation of the moment of inertia I for a uniform thin rod about an axis through the end of the rod. 
Note the rotational inertia of the rod about its endpoint is larger than the rotational inertia about its center 
(consistent with the barbell example) by a factor of four. 
The Parallel-Axis Theorem 
The similarity between the process of finding the moment of inertia of a rod about an axis through its middle and 
about an axis through its end is striking, and suggests that there might be a simpler method for determining the 
moment of inertia for a rod about any axis parallel to the axis through the center of mass. Such an axis is called a 
parallel axis. There is a theorem for this, called the parallel-axis theorem, which we state here but do not derive in 
this text. 
Let’s apply this to the rod examples solved above: 
This result agrees with our more lengthy calculation from above. This is a useful equation that we apply in some of 
the examples and problems. 
CHECK YOUR UNDERSTANDING 10.5 
What is the moment of inertia of a cylinder of radius R and mass m about an axis through a point on the surface, as 
shown below? 
PARALLEL-AXIS THEOREM 
Let m be the mass of an object and let d be the distance from an axis through the object’s center of mass to a 
new axis. Then we have 
10.20 
10 • Fixed-Axis Rotation
Access for free at openstax.org

A uniform thin disk about an axis through the center 
Integrating to find the moment of inertia of a two-dimensional object is a little bit trickier, but one shape is 
commonly done at this level of study—a uniform thin disk about an axis through its center (Figure 10.27). 
FIGURE 10.27 Calculating the moment of inertia for a thin disk about an axis through its center. 
Since the disk is thin, we can take the mass as distributed entirely in the xy-plane. We again start with the 
relationship for the surface mass density, which is the mass per unit surface area. Since it is uniform, the surface 
mass density  is constant: 
Now we use a simplification for the area. The area can be thought of as made up of a series of thin rings, where each 
ring is a mass increment dm of radius r equidistant from the axis, as shown in part (b) of the figure. The infinitesimal 
area of each ring dA is therefore given by the length of each ring (
) times the infinitesimal width of each ring dr: 
The full area of the disk is then made up from adding all the thin rings with a radius range from 0 to R. This radius 
range then becomes our limits of integration for dr, that is, we integrate from 
 to 
. Putting this all 
together, we have 
Note that this agrees with the value given in Figure 10.20. 
Calculating the moment of inertia for compound objects 
Now consider a compound object such as that in Figure 10.28, which depicts a thin disk at the end of a thin rod. This 
cannot be easily integrated to find the moment of inertia because it is not a uniformly shaped object. However, if we 
go back to the initial definition of moment of inertia as a summation, we can reason that a compound object’s 
moment of inertia can be found from the sum of each part of the object: 
It is important to note that the moments of inertia of the objects in Equation 10.21 are about a common axis. In the 
case of this object, that would be a rod of length L rotating about its end, and a thin disk of radius R rotating about an 
axis shifted off of the center by a distance 
, where R is the radius of the disk. Let’s define the mass of the rod 
to be 
 and the mass of the disk to be 
10.21 
10.5 • Calculating Moments of Inertia

FIGURE 10.28 Compound object consisting of a disk at the end of a rod. The axis of rotation is located at A. 
The moment of inertia of the rod is simply 
, but we have to use the parallel-axis theorem to find the moment 
of inertia of the disk about the axis shown. The moment of inertia of the disk about its center is 
 and we 
apply the parallel-axis theorem 
 to find 
Adding the moment of inertia of the rod plus the moment of inertia of the disk with a shifted axis of rotation, we find 
the moment of inertia for the compound object to be 
Applying moment of inertia calculations to solve problems 
Now let’s examine some practical applications of moment of inertia calculations. 
EXAMPLE 10.11 
Person on a Merry-Go-Round 
A 25-kg child stands at a distance 
 from the axis of a rotating merry-go-round (Figure 10.29). The merry-
go-round can be approximated as a uniform solid disk with a mass of 500 kg and a radius of 2.0 m. Find the moment 
of inertia of this system. 
FIGURE 10.29 Calculating the moment of inertia for a child on a merry-go-round. 
Strategy 
This problem involves the calculation of a moment of inertia. We are given the mass and distance to the axis of 
rotation of the child as well as the mass and radius of the merry-go-round. Since the mass and size of the child are 
much smaller than the merry-go-round, we can approximate the child as a point mass. The notation we use is 
. 
Our goal is to find 
. 
10 • Fixed-Axis Rotation
Access for free at openstax.org

Solution 
For the child, 
, and for the merry-go-round, 
. Therefore 
Significance 
The value should be close to the moment of inertia of the merry-go-round by itself because it has much more mass 
distributed away from the axis than the child does. 
EXAMPLE 10.12 
Rod and Solid Sphere 
Find the moment of inertia of the rod and solid sphere combination about the two axes as shown below. The rod has 
length 0.5 m and mass 2.0 kg. The radius of the sphere is 20.0 cm and has mass 1.0 kg. 
Strategy 
Since we have a compound object in both cases, we can use the parallel-axis theorem to find the moment of inertia 
about each axis. In (a), the center of mass of the sphere is located at a distance 
 from the axis of rotation. In 
(b), the center of mass of the sphere is located a distance R from the axis of rotation. In both cases, the moment of 
inertia of the rod is about an axis at one end. Refer to Table 10.4 for the moments of inertia for the individual 
objects. 
a. 
; 
; 
b. 
; 
; 
; 
Significance 
Using the parallel-axis theorem eases the computation of the moment of inertia of compound objects. We see that 
the moment of inertia is greater in (a) than (b). This is because the axis of rotation is closer to the center of mass of 
the system in (b). The simple analogy is that of a rod. The moment of inertia about one end is 
, but the 
moment of inertia through the center of mass along its length is 
. 
10.5 • Calculating Moments of Inertia

EXAMPLE 10.13 
Angular Velocity of a Pendulum 
A pendulum in the shape of a rod (Figure 10.30) is released from rest at an angle of 
. It has a length 30 cm and 
mass 300 g. What is its angular velocity at its lowest point? 
FIGURE 10.30 A pendulum in the form of a rod is released from rest at an angle of 
Strategy 
Use conservation of energy to solve the problem. At the point of release, the pendulum has gravitational potential 
energy, which is determined from the height of the center of mass above its lowest point in the swing. At the bottom 
of the swing, all of the gravitational potential energy is converted into rotational kinetic energy. 
Solution 
The change in potential energy is equal to the change in rotational kinetic energy, 
. 
At the top of the swing: 
. At the bottom of the swing, 
 with respect to the 
lowest point the rod swings. 
At the top of the swing, the rotational kinetic energy is 
. At the bottom of the swing, 
. Therefore: 
or 
Solving for , we have 
Inserting numerical values, we have 
Significance 
Note that the angular velocity of the pendulum does not depend on its mass. 
10 • Fixed-Axis Rotation
Access for free at openstax.org

10.6 Torque 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Describe how the magnitude of a torque depends on the magnitude of the lever arm and the angle the 
force vector makes with the lever arm 
• Determine the sign (positive or negative) of a torque using the right-hand rule 
• Calculate individual torques about a common axis and sum them to find the net torque 
An important quantity for describing the dynamics of a rotating rigid body is torque. We see the application of torque 
in many ways in our world. We all have an intuition about torque, as when we use a large wrench to unscrew a 
stubborn bolt. Torque is at work in unseen ways, as when we press on the accelerator in a car, causing the engine to 
put additional torque on the drive train. Or every time we move our bodies from a standing position, we apply a 
torque to our limbs. In this section, we define torque and make an argument for the equation for calculating torque 
for a rigid body with fixed-axis rotation. 
Defining Torque 
So far we have defined many variables that are rotational equivalents to their translational counterparts. Let’s 
consider what the counterpart to force must be. Since forces change the translational motion of objects, the 
rotational counterpart must be related to changing the rotational motion of an object about an axis. We call this 
rotational counterpart torque. 
In everyday life, we rotate objects about an axis all the time, so intuitively we already know much about torque. 
Consider, for example, how we rotate a door to open it. First, we know that a door opens slowly if we push too close 
to its hinges; it is more efficient to rotate a door open if we push far from the hinges. Second, we know that we 
should push perpendicular to the plane of the door; if we push parallel to the plane of the door, we are not able to 
rotate it. Third, the larger the force, the more effective it is in opening the door; the harder you push, the more 
rapidly the door opens. The first point implies that the farther the force is applied from the axis of rotation, the 
greater the angular acceleration; the second implies that the effectiveness depends on the angle at which the force 
is applied; the third implies that the magnitude of the force must also be part of the equation. Note that for rotation 
in a plane, torque has two possible directions. Torque is either clockwise or counterclockwise relative to the chosen 
pivot point. Figure 10.31 shows counterclockwise rotations. 
FIGURE 10.31 Torque is the turning or twisting effectiveness of a force, illustrated here for door rotation on its hinges (as viewed from 
overhead). Torque has both magnitude and direction. (a) A counterclockwise torque is produced by a force  acting at a distance r from the 
hinges (the pivot point). (b) A smaller counterclockwise torque is produced when a smaller force 
 acts at the same distance r from the 
10.6 • Torque

hinges. (c) The same force as in (a) produces a smaller counterclockwise torque when applied at a smaller distance from the hinges. (d) A 
smaller counterclockwise torque is produced by the same magnitude force as (a) acting at the same distance as (a) but at an angle  that is 
less than 
. 
Now let’s consider how to define torques in the general three-dimensional case. 
FIGURE 10.32 The torque is perpendicular to the plane defined by 
 and its direction is determined by the right-hand rule. 
From the definition of the cross product, the torque  is perpendicular to the plane containing 
 and has 
magnitude 
where  is the angle between the vectors  and . The SI unit of torque is newtons times meters, usually written as 
. The quantity 
 is the perpendicular distance from O to the line determined by the vector  and is 
called the lever arm. Note that the greater the lever arm, the greater the magnitude of the torque. In terms of the 
lever arm, the magnitude of the torque is 
The cross product 
 also tells us the sign of the torque. In Figure 10.32, the cross product 
 is along the 
positive z-axis, which by convention is a positive torque. If 
 is along the negative z-axis, this produces a 
negative torque. 
If we consider a disk that is free to rotate about an axis through the center, as shown in Figure 10.33, we can see 
how the angle between the radius  and the force  affects the magnitude of the torque. If the angle is zero, the 
torque is zero; if the angle is 
, the torque is maximum. The torque in Figure 10.33 is positive because the 
TORQUE 
When a force  is applied to a point P whose position is  relative to O (Figure 10.32), the torque  around O is 
10.22 
10.23 
10 • Fixed-Axis Rotation
Access for free at openstax.org

direction of the torque by the right-hand rule is out of the page along the positive z-axis. The disk rotates 
counterclockwise due to the torque, in the same direction as a positive angular acceleration. 
FIGURE 10.33 A disk is free to rotate about its axis through the center. The magnitude of the torque on the disk is 
.When 
, the 
torque is zero and the disk does not rotate. When 
, the torque is maximum and the disk rotates with maximum angular acceleration. 
Any number of torques can be calculated about a given axis. The individual torques add to produce a net torque 
about the axis. When the appropriate sign (positive or negative) is assigned to the magnitudes of individual torques 
about a specified axis, the net torque about the axis is the sum of the individual torques: 
Calculating Net Torque for Rigid Bodies on a Fixed Axis 
In the following examples, we calculate the torque both abstractly and as applied to a rigid body. 
We first introduce a problem-solving strategy. 
PROBLEM-SOLVING STRATEGY 
Finding Net Torque 
1. Choose a coordinate system with the pivot point or axis of rotation as the origin of the selected coordinate 
system. 
2. Determine the angle between the lever arm  and the force vector. 
3. Take the cross product of 
 to determine if the torque is positive or negative about the pivot point or 
axis. 
4. Evaluate the magnitude of the torque using 
. 
5. Assign the appropriate sign, positive or negative, to the magnitude. 
6. Sum the torques to find the net torque. 
EXAMPLE 10.14 
Calculating Torque 
Four forces are shown in Figure 10.34 at particular locations and orientations with respect to a given xy-coordinate 
system. Find the torque due to each force about the origin, then use your results to find the net torque about the 
origin. 
10.24 
10.6 • Torque

FIGURE 10.34 Four forces producing torques. 
Strategy 
This problem requires calculating torque. All known quantities––forces with directions and lever arms––are given in 
the figure. The goal is to find each individual torque and the net torque by summing the individual torques. Be 
careful to assign the correct sign to each torque by using the cross product of  and the force vector . 
Solution 
Use 
 to find the magnitude and 
 to determine the sign of the torque. 
The magnitude of the torque from force 40 N in the first quadrant is given by 
. 
The cross product of  and  is out of the page, positive. 
The magnitude of the torque from force 20 N in the third quadrant is given by
. 
The cross product of  and  is into the page, so it is negative: 
. 
The magnitude of the torque from force 30 N in the third quadrant is given by 
. 
The cross product of  and  is out of the page, positive. 
The magnitude of the torque from force 20 N in the second quadrant is given by 
. 
The cross product of  and  is out of the page. 
The net magnitude of the torque is therefore 
Significance 
Note that each force that acts in the counterclockwise direction has a positive torque, whereas each force that acts 
in the clockwise direction has a negative torque. The torque is greater when the distance, force, or perpendicular 
components are greater. 
EXAMPLE 10.15 
Calculating Torque on a rigid body 
Figure 10.35 shows several forces acting at different locations and angles on a flywheel. We have 
, 
, and 
. Find the net torque on the flywheel about an axis through the center. 
10 • Fixed-Axis Rotation
Access for free at openstax.org

FIGURE 10.35 Three forces acting on a flywheel. 
Strategy 
We calculate each torque individually, using the cross product, and determine the sign of the torque. Then we sum 
the torques to find the net torque. 
Solution 
We start with 
. If we look at Figure 10.35, we see that 
 makes an angle of 
 with the radius vector . 
Taking the cross product, we see that it is out of the page and so is positive. We also see this from calculating its 
magnitude: 
Next we look at 
. The angle between 
 and  is 
 and the cross product is into the page so the torque is 
negative. Its value is 
When we evaluate the torque due to 
, we see that the angle it makes with  is zero so 
 Therefore, 
does not produce any torque on the flywheel. 
We evaluate the sum of the torques: 
Significance 
The axis of rotation is at the center of mass of the flywheel. Since the flywheel is on a fixed axis, it is not free to 
translate. If it were on a frictionless surface and not fixed in place, 
 would cause the flywheel to translate, as well 
as 
. Its motion would be a combination of translation and rotation. 
CHECK YOUR UNDERSTANDING 10.6 
A large ocean-going ship runs aground near the coastline, similar to the fate of the Costa Concordia, and lies at an 
angle as shown below. Salvage crews must apply a torque to right the ship in order to float the vessel for transport. 
A force of 
 acting at point A must be applied to right the ship. What is the torque about the point of 
10.6 • Torque

contact of the ship with the ground (Figure 10.36)? 
FIGURE 10.36 A ship runs aground and tilts, requiring torque to be applied to return the vessel to an upright position. 
10.7 Newton’s Second Law for Rotation 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Calculate the torques on rotating systems about a fixed axis to find the angular acceleration 
• Explain how changes in the moment of inertia of a rotating system affect angular acceleration with a fixed 
applied torque 
In this section, we put together all the pieces learned so far in this chapter to analyze the dynamics of rotating rigid 
bodies. We have analyzed motion with kinematics and rotational kinetic energy but have not yet connected these 
ideas with force and/or torque. In this section, we introduce the rotational equivalent to Newton’s second law of 
motion and apply it to rigid bodies with fixed-axis rotation. 
Newton’s Second Law for Rotation 
We have thus far found many counterparts to the translational terms used throughout this text, most recently, 
torque, the rotational analog to force. This raises the question: Is there an analogous equation to Newton’s second 
law, 
 which involves torque and rotational motion? To investigate this, we start with Newton’s second law 
for a single particle rotating around an axis and executing circular motion. Let’s exert a force  on a point mass m 
that is at a distance r from a pivot point (Figure 10.37). The particle is constrained to move in a circular path with 
fixed radius and the force is tangent to the circle. We apply Newton’s second law to determine the magnitude of the 
acceleration 
 in the direction of . Recall that the magnitude of the tangential acceleration is proportional 
to the magnitude of the angular acceleration by 
. Substituting this expression into Newton’s second law, we 
obtain 
10 • Fixed-Axis Rotation
Access for free at openstax.org

FIGURE 10.37 An object is supported by a horizontal frictionless table and is attached to a pivot point by a cord that supplies centripetal 
force. A force  is applied to the object perpendicular to the radius r, causing it to accelerate about the pivot point. The force is 
perpendicular to r. 
Multiply both sides of this equation by r, 
Note that the left side of this equation is the torque about the axis of rotation, where r is the lever arm and F is the 
force, perpendicular to r. Recall that the moment of inertia for a point particle is
. The torque applied 
perpendicularly to the point mass in Figure 10.37 is therefore 
The torque on the particle is equal to the moment of inertia about the rotation axis times the angular acceleration. 
We can generalize this equation to a rigid body rotating about a fixed axis. 
The term 
 is a scalar quantity and can be positive or negative (counterclockwise or clockwise) depending upon 
the sign of the net torque. Remember the convention that counterclockwise angular acceleration is positive. Thus, if 
a rigid body is rotating clockwise and experiences a positive torque (counterclockwise), the angular acceleration is 
positive. 
Equation 10.25 is Newton’s second law for rotation and tells us how to relate torque, moment of inertia, and 
rotational kinematics. This is called the equation for rotational dynamics. With this equation, we can solve a whole 
class of problems involving force and rotation. It makes sense that the relationship for how much force it takes to 
rotate a body would include the moment of inertia, since that is the quantity that tells us how easy or hard it is to 
change the rotational motion of an object. 
Deriving Newton’s Second Law for Rotation in Vector Form 
As before, when we found the angular acceleration, we may also find the torque vector. The second law 
tells us the relationship between net force and how to change the translational motion of an object. We have a 
vector rotational equivalent of this equation, which can be found by using Equation 10.7 and Figure 10.8. Equation 
10.7 relates the angular acceleration to the position and tangential acceleration vectors: 
We form the cross product of this equation with  and use a cross product identity (note that 
): 
NEWTON’S SECOND LAW FOR ROTATION 
If more than one torque acts on a rigid body about a fixed axis, then the sum of the torques equals the moment 
of inertia times the angular acceleration: 
10.25 
10.7 • Newton’s Second Law for Rotation

We now form the cross product of Newton’s second law with the position vector 
Identifying the first term on the left as the sum of the torques, and 
 as the moment of inertia, we arrive at 
Newton’s second law of rotation in vector form: 
This equation is exactly Equation 10.25 but with the torque and angular acceleration as vectors. An important point 
is that the torque vector is in the same direction as the angular acceleration. 
Applying the Rotational Dynamics Equation 
Before we apply the rotational dynamics equation to some everyday situations, let’s review a general problem-
solving strategy for use with this category of problems. 
PROBLEM-SOLVING STRATEGY 
Rotational Dynamics 
1. Examine the situation to determine that torque and mass are involved in the rotation. Draw a careful sketch of 
the situation. 
2. Determine the system of interest. 
3. Draw a free-body diagram. That is, draw and label all external forces acting on the system of interest. 
4. Identify the pivot point. If the object is in equilibrium, it must be in equilibrium for all possible pivot 
points––chose the one that simplifies your work the most. 
5. Apply 
, the rotational equivalent of Newton’s second law, to solve the problem. Care must be taken 
to use the correct moment of inertia and to consider the torque about the point of rotation. 
6. As always, check the solution to see if it is reasonable. 
EXAMPLE 10.16 
Calculating the Effect of Mass Distribution on a Merry-Go-Round 
Consider the father pushing a playground merry-go-round in Figure 10.38. He exerts a force of 250 N at the edge of 
the 50.0-kg merry-go-round, which has a 1.50-m radius. Calculate the angular acceleration produced (a) when no 
one is on the merry-go-round and (b) when an 18.0-kg child sits 1.25 m away from the center. Consider the merry-
go-round itself to be a uniform disk with negligible friction. 
FIGURE 10.38 A father pushes a playground merry-go-round at its edge and perpendicular to its radius to achieve maximum torque. 
10.26 
10 • Fixed-Axis Rotation
Access for free at openstax.org

Strategy 
The net torque is given directly by the expression 
, To solve for , we must first calculate the net torque 
(which is the same in both cases) and moment of inertia I (which is greater in the second case). 
Solution 
a. The moment of inertia of a solid disk about this axis is given in Figure 10.20 to be 
We have 
 and 
, so 
To find the net torque, we note that the applied force is perpendicular to the radius and friction is negligible, so 
that 
Now, after we substitute the known values, we find the angular acceleration to be 
b. We expect the angular acceleration for the system to be less in this part because the moment of inertia is 
greater when the child is on the merry-go-round. To find the total moment of inertia I, we first find the child’s 
moment of inertia 
 by approximating the child as a point mass at a distance of 1.25 m from the axis. Then 
The total moment of inertia is the sum of the moments of inertia of the merry-go-round and the child (about 
the same axis): 
Substituting known values into the equation for α gives 
Significance 
The angular acceleration is less when the child is on the merry-go-round than when the merry-go-round is empty, as 
expected. The angular accelerations found are quite large, partly due to the fact that friction was considered to be 
negligible. If, for example, the father kept pushing perpendicularly for 2.00 s, he would give the merry-go-round an 
angular velocity of 13.3 rad/s when it is empty but only 8.89 rad/s when the child is on it. In terms of revolutions per 
second, these angular velocities are 2.12 rev/s and 1.41 rev/s, respectively. The father would end up running at 
about 50 km/h in the first case. 
CHECK YOUR UNDERSTANDING 10.7 
The fan blades on a jet engine have a moment of inertia 
. In 10 s, they rotate counterclockwise from rest 
up to a rotation rate of 20 rev/s. (a) What torque must be applied to the blades to achieve this angular acceleration? 
(b) What is the torque required to bring the fan blades rotating at 20 rev/s to a rest in 20 s? 
10.7 • Newton’s Second Law for Rotation

10.8 Work and Power for Rotational Motion 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
•
Use the work-energy theorem to analyze rotation to find the work done on a system when it is rotated
about a fixed axis for a finite angular displacement
•
Solve for the angular velocity of a rotating rigid body using the work-energy theorem
•
Find the power delivered to a rotating rigid body given the applied torque and angular velocity
•
Summarize the rotational variables and equations and relate them to their translational counterparts
Thus far in the chapter, we have extensively addressed kinematics and dynamics for rotating rigid bodies around a 
fixed axis. In this final section, we define work and power within the context of rotation about a fixed axis, which has 
applications to both physics and engineering. The discussion of work and power makes our treatment of rotational 
motion almost complete, with the exception of rolling motion and angular momentum, which are discussed in 
Angular Momentum. We begin this section with a treatment of the work-energy theorem for rotation. 
Work for Rotational Motion 
Now that we have determined how to calculate kinetic energy for rotating rigid bodies, we can proceed with a 
discussion of the work done on a rigid body rotating about a fixed axis. Figure 10.39 shows a rigid body that has 
rotated through an angle 
 from A to B while under the influence of a force . The external force  is applied to 
point P, whose position is , and the rigid body is constrained to rotate about a fixed axis that is perpendicular to the 
page and passes through O. The rotational axis is fixed, so the vector  moves in a circle of radius r, and the vector 
 is perpendicular to 
FIGURE 10.39 A rigid body rotates through an angle 
 from A to B by the action of an external force  applied to point P. 
The work by the force  is given by Equation 7.2, 
In this equation, 
 is the displacement of point P, not a change in the moment arm. That is: 
Substituting this into the definition of work, we have 
10 • Fixed-Axis Rotation
Access for free at openstax.org

Since  is perpendicular to , we can see that 
, the torque by the force F. Evaluating the work using the net 
torque, we arrive at the expression for the net rotational work done on a rigid body: 
The total work done on a rigid body is the sum of the torques integrated over the angle through which the body 
rotates. The incremental work is 
In a rigid body, all particles rotate through the same angle; thus the work of every external force is equal to the 
torque times the common incremental angle 
. The quantity 
 is the net torque on the body due to 
external forces. 
Similarly, we found the kinetic energy of a rigid body rotating around a fixed axis by summing the kinetic energy of 
each particle that makes up the rigid body. Since the work-energy theorem 
 is valid for each particle, it is 
valid for the sum of the particles and the entire body. 
We give a strategy for using this equation when analyzing rotational motion. 
PROBLEM-SOLVING STRATEGY 
Work-Energy Theorem for Rotational Motion 
1.
Identify the forces on the body and draw a free-body diagram. Calculate the torque for each force.
2.
Calculate the work done during the body’s rotation by every torque.
3.
Apply the work-energy theorem by equating the net work done on the body to the change in rotational kinetic
energy.
Let’s look at two examples and use the work-energy theorem to analyze rotational motion. 
> 
10.27 
10.28 
WORK-ENERGY THEOREM FOR ROTATION 
The work-energy theorem for a rigid body rotating around a fixed axis is 
where 
and the rotational work done by a net force rotating a body from point A to point B is 
10.29 
10.30 
10.8 • Work and Power for Rotational Motion

EXAMPLE 10.17 
Rotational Work and Energy 
A 
 torque is applied to a flywheel that rotates about a fixed axis and has a moment of inertia of 
. If the flywheel is initially at rest, what is its angular velocity after it has turned through eight 
revolutions? 
Strategy 
We apply the work-energy theorem. We know from the problem description what the torque is and the angular 
displacement of the flywheel. Then we can solve for the final angular velocity. 
Solution 
The flywheel turns through eight revolutions, which is 
 radians. The work done by the torque, which is constant 
and therefore can come outside the integral in Equation 10.30, is 
We apply the work-energy theorem: 
With 
, we have 
Therefore, 
This is the angular velocity of the flywheel after eight revolutions. 
Significance 
The work-energy theorem provides an efficient way to analyze rotational motion, connecting torque with rotational 
kinetic energy. 
EXAMPLE 10.18 
Rotational Work: A Pulley 
A string wrapped around the pulley in Figure 10.40 is pulled with a constant downward force  of magnitude 50 N. 
The radius R and moment of inertia I of the pulley are 0.10 m and 
, respectively. If the string does 
not slip, what is the angular velocity of the pulley after 1.0 m of string has unwound? Assume the pulley starts from 
rest. 
10 • Fixed-Axis Rotation
Access for free at openstax.org

FIGURE 10.40 (a) A string is wrapped around a pulley of radius R. (b) The free-body diagram. 
Strategy 
Looking at the free-body diagram, we see that neither , the force on the bearings of the pulley, nor
, the weight 
of the pulley, exerts a torque around the rotational axis, and therefore does no work on the pulley. As the pulley 
rotates through an angle 
  acts through a distance d such that 
Solution 
Since the torque due to  has magnitude 
, we have 
If the force on the string acts through a distance of 1.0 m, we have, from the work-energy theorem, 
Solving for , we obtain 
Power for Rotational Motion 
Power always comes up in the discussion of applications in engineering and physics. Power for rotational motion is 
equally as important as power in linear motion and can be derived in a similar way as in linear motion when the force 
is a constant. The linear power when the force is a constant is 
. If the net torque is constant over the 
angular displacement, Equation 10.25 simplifies and the net torque can be taken out of the integral. In the following 
discussion, we assume the net torque is constant. We can apply the definition of power derived in Power to 
rotational motion. From Work and Kinetic Energy, the instantaneous power (or just power) is defined as the rate of 
doing work, 
If we have a constant net torque, Equation 10.27 becomes 
 and the power is 
or 
10.8 • Work and Power for Rotational Motion

EXAMPLE 10.19 
Torque on a Boat Propeller 
A boat engine operating at 
 is running at 300 rev/min. What is the torque on the propeller shaft? 
Strategy 
We are given the rotation rate in rev/min and the power consumption, so we can easily calculate the torque. 
Solution 
Significance 
It is important to note the radian is a dimensionless unit because its definition is the ratio of two lengths. It 
therefore does not appear in the solution. 
CHECK YOUR UNDERSTANDING 10.8 
A constant torque of 
 is applied to a wind turbine to keep it rotating at 6 rad/s. What is the power 
required to keep the turbine rotating? 
Rotational and Translational Relationships Summarized 
The rotational quantities and their linear analog are summarized in three tables. Table 10.5 summarizes the 
rotational variables for circular motion about a fixed axis with their linear analogs and the connecting equation, 
except for the centripetal acceleration, which stands by itself. Table 10.6 summarizes the rotational and 
translational kinematic equations. Table 10.7 summarizes the rotational dynamics equations with their linear 
analogs. 
Rotational 
Translational 
Relationship 
TABLE 10.5 Rotational and Translational Variables: 
Summary 
10.31 
10 • Fixed-Axis Rotation
Access for free at openstax.org

Rotational 
Translational 
TABLE 10.6 Rotational and Translational Kinematic 
Equations: Summary 
Rotational 
Translational 
m 
TABLE 10.7 Rotational and Translational Equations: 
Dynamics 
10.8 • Work and Power for Rotational Motion

Chapter Review 
Key Terms 
angular acceleration time rate of change of angular 
velocity 
angular position angle a body has rotated through in 
a fixed coordinate system 
angular velocity time rate of change of angular 
position 
instantaneous angular acceleration derivative of 
angular velocity with respect to time 
instantaneous angular velocity derivative of angular 
position with respect to time 
kinematics of rotational motion describes the 
relationships among rotation angle, angular velocity, 
angular acceleration, and time 
lever arm perpendicular distance from the line that 
the force vector lies on to a given axis 
linear mass density the mass per unit length  of a 
one dimensional object 
moment of inertia rotational mass of rigid bodies 
that relates to how easy or hard it will be to change 
the angular velocity of the rotating rigid body 
Newton’s second law for rotation sum of the torques 
on a rotating system equals its moment of inertia 
times its angular acceleration 
parallel axis axis of rotation that is parallel to an axis 
about which the moment of inertia of an object is 
known 
parallel-axis theorem if the moment of inertia is 
known for a given axis, it can be found for any axis 
parallel to it 
rotational dynamics analysis of rotational motion 
using the net torque and moment of inertia to find 
the angular acceleration 
rotational kinetic energy kinetic energy due to the 
rotation of an object; this is part of its total kinetic 
energy 
rotational work work done on a rigid body due to the 
sum of the torques integrated over the angle 
through with the body rotates 
surface mass density mass per unit area  of a two 
dimensional object 
torque cross product of a force and a lever arm to a 
given axis 
total linear acceleration vector sum of the 
centripetal acceleration vector and the tangential 
acceleration vector 
Key Equations 
Angular position 
Angular velocity 
Tangential speed 
Angular acceleration 
Tangential acceleration 
Average angular velocity 
Angular displacement 
Angular velocity from constant angular acceleration 
Angular velocity from displacement and 
constant angular acceleration 
Change in angular velocity 
Total acceleration 
Rotational kinetic energy 
Moment of inertia 
Rotational kinetic energy in terms of the 
moment of inertia of a rigid body 
Moment of inertia of a continuous object 
500     10 • Chapter Review
Access for free at openstax.org

Parallel-axis theorem 
Moment of inertia of a compound object 
Torque vector 
Magnitude of torque 
Total torque 
Newton’s second law for rotation 
Incremental work done by a torque 
Work-energy theorem 
Rotational work done by net force 
Rotational power 
Summary 
10.1 Rotational Variables 
• The angular position  of a rotating body is the 
angle the body has rotated through in a fixed 
coordinate system, which serves as a frame of 
reference. 
• The angular velocity of a rotating body about a 
fixed axis is defined as 
, the rotational 
rate of the body in radians per second. The 
instantaneous angular velocity of a rotating body 
 is the derivative with respect 
to time of the angular position , found by taking 
the limit 
 in the average angular velocity 
. The angular velocity relates 
 to the 
tangential speed of a point on the rotating body 
through the relation 
, where r is the 
radius to the point and 
 is the tangential speed 
at the given point. 
• The angular velocity 
 is found using the right-
hand rule. If the fingers curl in the direction of 
rotation about a fixed axis, the thumb points in 
the direction of 
 (see Figure 10.5). 
• If the system’s angular velocity is not constant, 
then the system has an angular acceleration. The 
average angular acceleration over a given time 
interval is the change in angular velocity over this 
time interval, 
. The instantaneous 
angular acceleration is the time derivative of 
angular velocity, 
. The 
angular acceleration  is found by locating the 
angular velocity. If a rotation rate of a rotating 
body is decreasing, the angular acceleration is in 
the opposite direction to 
. If the rotation rate is 
increasing, the angular acceleration is in the 
same direction as 
. 
• The tangential acceleration of a point at a radius 
from the axis of rotation is the angular 
acceleration times the radius to the point. 
10.2 Rotation with Constant Angular Acceleration 
• The kinematics of rotational motion describes 
the relationships among rotation angle (angular 
position), angular velocity, angular acceleration, 
and time. 
• For a constant angular acceleration, the angular 
velocity varies linearly. Therefore, the average 
angular velocity is 1/2 the initial plus final 
angular velocity over a given time period: 
• We used a graphical analysis to find solutions to 
fixed-axis rotation with constant angular 
acceleration. From the relation 
, we 
found that the area under an angular velocity-vs.-
time curve gives the angular displacement, 
. The results of the 
graphical analysis were verified using the 
kinematic equations for constant angular 
acceleration. Similarly, since 
, the area 
under an angular acceleration-vs.-time graph 
10 • Chapter Review     501

gives the change in angular velocity: 
. 
10.3 Relating Angular and Translational Quantities 
• The linear kinematic equations have their 
rotational counterparts such that there is a 
mapping 
. 
• A system undergoing uniform circular motion has 
a constant angular velocity, but points at a 
distance r from the rotation axis have a linear 
centripetal acceleration. 
• A system undergoing nonuniform circular motion 
has an angular acceleration and therefore has 
both a linear centripetal and linear tangential 
acceleration at a point a distance r from the axis 
of rotation. 
• The total linear acceleration is the vector sum of 
the centripetal acceleration vector and the 
tangential acceleration vector. Since the 
centripetal and tangential acceleration vectors 
are perpendicular to each other for circular 
motion, the magnitude of the total linear 
acceleration is 
. 
10.4 Moment of Inertia and Rotational Kinetic Energy 
• The rotational kinetic energy is the kinetic energy 
of rotation of a rotating rigid body or system of 
particles, and is given by 
, where I is 
the moment of inertia, or “rotational mass” of the 
rigid body or system of particles. 
• The moment of inertia for a system of point 
particles rotating about a fixed axis is 
, where 
 is the mass of the point 
particle and 
 is the distance of the point 
particle to the rotation axis. Because of the 
term, the moment of inertia increases as the 
square of the distance to the fixed rotational axis. 
The moment of inertia is the rotational 
counterpart to the mass in linear motion. 
• In systems that are both rotating and translating, 
conservation of mechanical energy can be used if 
there are no nonconservative forces at work. The 
total mechanical energy is then conserved and is 
the sum of the rotational and translational kinetic 
energies, and the gravitational potential energy. 
10.5 Calculating Moments of Inertia 
• Moments of inertia can be found by summing or 
integrating over every ‘piece of mass’ that makes 
up an object, multiplied by the square of the 
distance of each ‘piece of mass’ to the axis. In 
integral form the moment of inertia is 
. 
• Moment of inertia is larger when an object’s mass 
is farther from the axis of rotation. 
• It is possible to find the moment of inertia of an 
object about a new axis of rotation once it is 
known for a parallel axis. This is called the 
parallel axis theorem given by 
, where d is 
the distance from the initial axis to the parallel 
axis. 
• Moment of inertia for a compound object is 
simply the sum of the moments of inertia for 
each individual object that makes up the 
compound object. 
10.6 Torque 
• The magnitude of a torque about a fixed axis is 
calculated by finding the lever arm to the point 
where the force is applied and using the relation 
, where 
 is the perpendicular 
distance from the axis to the line upon which the 
force vector lies. 
• The sign of the torque is found using the right 
hand rule. If the page is the plane containing 
and , then 
 is out of the page for positive 
torques and into the page for negative torques. 
• The net torque can be found from summing the 
individual torques about a given axis. 
10.7 Newton’s Second Law for Rotation 
• Newton’s second law for rotation, 
, 
says that the sum of the torques on a rotating 
system about a fixed axis equals the product of 
the moment of inertia and the angular 
acceleration. This is the rotational analog to 
Newton’s second law of linear motion. 
• In the vector form of Newton’s second law for 
rotation, the torque vector  is in the same 
direction as the angular acceleration . If the 
angular acceleration of a rotating system is 
positive, the torque on the system is also 
positive, and if the angular acceleration is 
negative, the torque is negative. 
10.8 Work and Power for Rotational Motion 
• The incremental work dW in rotating a rigid body 
about a fixed axis is the sum of the torques about 
the axis times the incremental angle 
. 
502     10 • Chapter Review
Access for free at openstax.org

• The total work done to rotate a rigid body 
through an angle  about a fixed axis is the sum 
of the torques integrated over the angular 
displacement. If the torque is a constant as a 
function of , then 
. 
• The work-energy theorem relates the rotational 
work done to the change in rotational kinetic 
energy: 
 where 
• The power delivered to a system that is rotating 
about a fixed axis is the torque times the angular 
velocity, 
. 
Conceptual Questions 
10.1 Rotational Variables 
1 . A clock is mounted on the wall. As you look at it, 
what is the direction of the angular velocity 
vector of the second hand? 
2 . What is the value of the angular acceleration of 
the second hand of the clock on the wall? 
3 . A baseball bat is swung. Do all points on the bat 
have the same angular velocity? The same 
tangential speed? 
4 . The blades of a blender on a counter are rotating 
clockwise as you look into it from the top. If the 
blender is put to a greater speed what direction 
is the angular acceleration of the blades? 
10.2 Rotation with Constant Angular Acceleration 
5 . If a rigid body has a constant angular 
acceleration, what is the functional form of the 
angular velocity in terms of the time variable? 
6 . If a rigid body has a constant angular 
acceleration, what is the functional form of the 
angular position? 
7 . If the angular acceleration of a rigid body is zero, 
what is the functional form of the angular 
velocity? 
8 . A massless tether with a masses tied to both 
ends rotates about a fixed axis through the 
center. Can the total acceleration of the tether/
mass combination be zero if the angular velocity 
is constant? 
10.3 Relating Angular and Translational Quantities 
9 . Explain why centripetal acceleration changes 
the direction of velocity in circular motion but 
not its magnitude. 
10 . In circular motion, a tangential acceleration can 
change the magnitude of the velocity but not its 
direction. Explain your answer. 
11 . Suppose a piece of food is on the edge of a 
rotating microwave oven plate. Does it 
experience nonzero tangential acceleration, 
centripetal acceleration, or both when: (a) the 
plate starts to spin faster? (b) The plate rotates 
at constant angular velocity? (c) The plate slows 
to a halt? 
10.4 Moment of Inertia and Rotational Kinetic Energy 
12 . What if another planet the same size as Earth 
were put into orbit around the Sun along with 
Earth. Would the moment of inertia of the 
system increase, decrease, or stay the same? 
13 . A solid sphere is rotating about an axis through 
its center at a constant rotation rate. Another 
hollow sphere of the same mass and radius is 
rotating about its axis through the center at the 
same rotation rate. Which sphere has a greater 
rotational kinetic energy? 
10.5 Calculating Moments of Inertia 
14 . If a child walks toward the center of a merry-go-
round, does the moment of inertia increase or 
decrease? 
15 . A discus thrower rotates with a discus in his 
hand before letting it go. (a) How does his 
moment of inertia change after releasing the 
discus? (b) What would be a good approximation 
to use in calculating the moment of inertia of the 
discus thrower and discus? 
16 . Does increasing the number of blades on a 
propeller increase or decrease its moment of 
inertia, and why? 
17 . The moment of inertia of a long rod spun around 
an axis through one end perpendicular to its 
length is 
. Why is this moment of inertia 
greater than it would be if you spun a point mass 
m at the location of the center of mass of the rod 
(at L/2) (that would be 
)? 
18 . Why is the moment of inertia of a hoop that has 
a mass M and a radius R greater than the 
moment of inertia of a disk that has the same 
mass and radius? 
10 • Chapter Review     503

10.6 Torque 
19 . What three factors affect the torque created by a 
force relative to a specific pivot point? 
20 . Give an example in which a small force exerts a 
large torque. Give another example in which a 
large force exerts a small torque. 
21 . When reducing the mass of a racing bike, the 
greatest benefit is realized from reducing the 
mass of the tires and wheel rims. Why does this 
allow a racer to achieve greater accelerations 
than would an identical reduction in the mass of 
the bicycle’s frame? 
22 . Can a single force produce a zero torque? 
23 . Can a set of forces have a net torque that is zero 
and a net force that is not zero? 
24 . Can a set of forces have a net force that is zero 
and a net torque that is not zero? 
25 . In the expression 
 can 
 ever be less 
than the lever arm? Can it be equal to the lever 
arm? 
10.7 Newton’s Second Law for Rotation 
26 . If you were to stop a spinning wheel with a 
constant force, where on the wheel would you 
apply the force to produce the maximum 
negative acceleration? 
27 . A rod is pivoted about one end. Two forces 
 are applied to it. Under what 
circumstances will the rod not rotate? 
Problems 
10.1 Rotational Variables 
28 . Calculate the angular velocity of Earth. 
29 . A track star runs a 400-m race on a 400-m 
circular track in 45 s. What is his angular velocity 
assuming a constant speed? 
30 . A wheel rotates at a constant rate of 
. (a) What is its angular 
velocity in radians per second? (b) Through what 
angle does it turn in 10 s? Express the solution 
in radians and degrees. 
31 . A particle moves 3.0 m along a circle of radius 
1.5 m. (a) Through what angle does it rotate? (b) 
If the particle makes this trip in 1.0 s at a 
constant speed, what is its angular velocity? (c) 
What is its acceleration? 
32 . A compact disc rotates at 500 rev/min. If the 
diameter of the disc is 120 mm, (a) what is the 
tangential speed of a point at the edge of the 
disc? (b) At a point halfway to the center of the 
disc? 
33 . Unreasonable results. The propeller of an 
aircraft is spinning at 10 rev/s when the pilot 
shuts off the engine. The propeller reduces its 
angular velocity at a constant 
 for a 
time period of 40 s. What is the rotation rate of 
the propeller in 40 s? Is this a reasonable 
situation? 
34 . A gyroscope slows from an initial rate of 32.0 
rad/s at a rate of 
. How long does it 
take to come to rest? 
35 . On takeoff, the propellers on a UAV (unmanned 
aerial vehicle) increase their angular velocity for 
3.0 s from rest at a rate of 
where t is measured in seconds. (a) What is the 
instantaneous angular velocity of the propellers 
at 
? (b) What is the angular 
acceleration? 
36 . The angular position of a rod varies as 
radians from time 
. The rod has two beads on 
it as shown in the following figure, one at 10 cm 
from the rotation axis and the other at 20 cm from 
the rotation axis. (a) What is the instantaneous 
angular velocity of the rod at 
 (b) What is 
the angular acceleration of the rod? (c) What are 
the tangential speeds of the beads at 
 (d) 
What are the tangential accelerations of the beads 
at 
 (e) What are the centripetal 
accelerations of the beads at 
10.2 Rotation with Constant Angular Acceleration 
37 . A wheel has a constant angular acceleration of 
. Starting from rest, it turns through 
504     10 • Chapter Review
Access for free at openstax.org

300 rad. (a) What is its final angular velocity? (b) 
How much time elapses while it turns through 
the 300 radians? 
38 . During a 6.0-s time interval, a flywheel with a 
constant angular acceleration turns through 500 
radians and acquires an angular velocity of 100 
rad/s. (a) What is the angular velocity at the 
beginning of the 6.0 s? (b) What is the angular 
acceleration of the flywheel? 
39 . The angular velocity of a rotating rigid body 
increases from 500 to 1500 rev/min in 120 s. (a) 
What is the angular acceleration of the body? (b) 
Through what angle does it turn in this 120 s? 
40 . A flywheel slows from 600 to 400 rev/min while 
rotating through 40 revolutions. (a) What is the 
angular acceleration of the flywheel? (b) How 
much time elapses during the 40 revolutions? 
41 . A wheel 1.0 m in radius rotates with an angular 
acceleration of 
. (a) If the wheel’s 
initial angular velocity is 2.0 rad/s, what is its 
angular velocity after 10 s? (b) Through what 
angle does it rotate in the 10-s interval? (c) What 
are the tangential speed and acceleration of a 
point on the rim of the wheel at the end of the 
10-s interval? 
42 . A vertical wheel with a diameter of 50 cm starts 
from rest and rotates with a constant angular 
acceleration of 
 around a fixed axis 
through its center counterclockwise. (a) Where 
is the point that is initially at the bottom of the 
wheel at 
 (b) What is the point’s linear 
acceleration at this instant? 
43 . A circular disk of radius 10 cm has a constant 
angular acceleration of 
; at 
 its 
angular velocity is 2.0 rad/s. (a) Determine the 
disk’s angular velocity at 
. (b) What is 
the angle it has rotated through during this time? 
(c) What is the tangential acceleration of a point 
on the disk at 
44 . The angular velocity vs. time for a fan on a 
hovercraft is shown below. (a) What is the angle 
through which the fan blades rotate in the first 8 
seconds? (b) Verify your result using the 
kinematic equations. 
45 . A rod of length 20 cm has two beads attached to 
its ends. The rod with beads starts rotating from 
rest. If the beads are to have a tangential speed 
of 20 m/s in 7 s, what is the angular acceleration 
of the rod to achieve this? 
10.3 Relating Angular and Translational Quantities 
46 . At its peak, a tornado is 60.0 m in diameter and 
carries 500 km/h winds. What is its angular 
velocity in revolutions per second? 
47 . A man stands on a merry-go-round that is 
rotating at 2.5 rad/s. If the coefficient of static 
friction between the man’s shoes and the merry-
go-round is 
, how far from the axis of 
rotation can he stand without sliding? 
48 . An ultracentrifuge accelerates from rest to 
100,000 rpm in 2.00 min. (a) What is the 
average angular acceleration in 
? (b) What 
is the tangential acceleration of a point 9.50 cm 
from the axis of rotation? (c) What is the 
centripetal acceleration in 
 and multiples of 
g of this point at full rpm? (d) What is the total 
distance traveled during the acceleration by a 
point 9.5 cm from the axis of rotation of the 
ultracentrifuge? 
49 . A wind turbine is rotating counterclockwise at 
0.5 rev/s and slows to a stop in 10 s. Its blades 
are 20 m in length. (a) What is the angular 
acceleration of the turbine? (b) What is the 
centripetal acceleration of the tip of the blades 
at 
 (c) What is the magnitude and 
direction of the total linear acceleration of the 
tip of the blade that lies along the positive x-axis 
at 
50 . What is (a) the angular speed and (b) the linear 
speed of a point on Earth’s surface at latitude 
 N. Take the radius of the Earth to be 6309 
km. (c) At what latitude would your linear speed 
be 10 m/s? 
51 . A child with mass 40 kg sits on the edge of a 
10 • Chapter Review     505

merry-go-round at a distance of 3.0 m from its 
axis of rotation. The merry-go-round accelerates 
from rest up to 0.4 rev/s in 10 s. If the 
coefficient of static friction between the child 
and the surface of the merry-go-round is 0.6, 
does the child fall off before 5 s? 
52 . A bicycle wheel with radius 0.3 m rotates from 
rest to 3 rev/s in 5 s. What is the magnitude and 
direction of the total acceleration vector at the 
edge of the wheel at 1.0 s? 
53 . The angular velocity of a flywheel with radius 1.0 
m varies according to 
. Plot 
 from 
 for 
. 
Analyze these results to explain when 
and when 
 for a point on the flywheel at 
a radius of 1.0 m. 
10.4 Moment of Inertia and Rotational Kinetic Energy 
54 . A system of point particles is shown in the 
following figure. Each particle has mass 0.3 kg 
and they all lie in the same plane. (a) What is the 
moment of inertia of the system about the given 
axis? (b) If the system rotates at 5 rev/s, what is 
its rotational kinetic energy? 
55 . (a) Calculate the rotational kinetic energy of 
Earth on its axis. (b) What is the rotational 
kinetic energy of Earth in its orbit around the 
Sun? 
56 . Calculate the rotational kinetic energy of a 12-kg 
motorcycle wheel if its angular velocity is 120 
rad/s and its inner radius is 0.280 m and outer 
radius 0.330 m. 
57 . A baseball pitcher throws the ball in a motion 
where there is rotation of the forearm about the 
elbow joint as well as other movements. If the 
linear velocity of the ball relative to the elbow 
joint is 20.0 m/s at a distance of 0.480 m from 
the joint and the moment of inertia of the 
forearm is 
, what is the rotational 
kinetic energy of the forearm? 
58 . A diver goes into a somersault during a dive by 
tucking her limbs. If her rotational kinetic energy 
is 100 J and her moment of inertia in the tuck is 
, what is her rotational rate during 
the somersault? 
59 . An aircraft is coming in for a landing at 300 
meters height when the propeller falls off. The 
aircraft is flying at 40.0 m/s horizontally. The 
propeller has a rotation rate of 20 rev/s, a 
moment of inertia of 
, and a mass of 
200 kg. Neglect air resistance so the rotation 
rate does not change as the propeller falls. (a) 
With what translational velocity does the 
propeller hit the ground? (b) What is the rotation 
rate of the propeller at impact? 
60 . An aircraft is coming in for a landing at 300 
meters height when the propeller falls off. When 
it comes off, the propeller has a rotation rate of 
20 rev/s, a moment of inertia of 
, and 
a mass of 200 kg. If air resistance is present and 
reduces the propeller’s rotational kinetic energy 
at impact by 30%, what is the propeller’s 
rotation rate at impact? 
61 . A neutron star of mass 
 and radius 
10 km rotates with a period of 0.02 seconds. 
What is its rotational kinetic energy? 
62 . An electric sander consisting of a rotating disk of 
mass 0.7 kg and radius 10 cm rotates at 15 rev/
s. When applied to a rough wooden wall the 
rotation rate decreases by 20%. (a) What is the 
final rotational kinetic energy of the rotating 
disk? (b) How much has its rotational kinetic 
energy decreased? 
63 . A system consists of a disk of mass 2.0 kg and 
radius 50 cm upon which is mounted an annular 
cylinder of mass 1.0 kg with inner radius 20 cm 
and outer radius 30 cm (see below). The system 
rotates about an axis through the center of the 
disk and annular cylinder at 10 rev/s. (a) What is 
the moment of inertia of the system? (b) What is 
its rotational kinetic energy? 
506     10 • Chapter Review
Access for free at openstax.org

10.5 Calculating Moments of Inertia 
64 . While punting a football, a kicker rotates their 
leg about the hip joint. The moment of inertia of 
the leg is 
 and its rotational kinetic 
energy is 175 J. (a) What is the angular velocity 
of the leg? (b) What is the velocity of tip of the 
punter’s shoe if it is 1.05 m from the hip joint? 
65 . Using the parallel axis theorem, what is the moment 
of inertia of the rod of mass m about the axis shown 
below? 
66 . Find the moment of inertia of the rod in the 
previous problem by direct integration. 
67 . A uniform rod of mass 1.0 kg and length 2.0 m is 
free to rotate about one end (see the following 
figure). If the rod is released from rest at an 
angle of 
 with respect to the horizontal, what 
is the speed of the tip of the rod as it passes the 
horizontal position? 
68 . A pendulum consists of a rod of mass 2 kg and 
length 1 m with a solid sphere at one end with 
mass 0.3 kg and radius 20 cm (see the following 
figure). If the pendulum is released from rest at 
an angle of 
, what is the angular velocity at 
the lowest point? 
69 . A solid sphere of radius 10 cm is allowed to rotate 
freely about an axis. The sphere is given a sharp 
blow so that its center of mass starts from the 
position shown in the following figure with speed 15 
cm/s. What is the maximum angle that the diameter 
makes with the vertical? 
70 . Calculate the moment of inertia by direct integration 
of a thin rod of mass M and length L about an axis 
through the rod at L/3, as shown below. Check your 
answer with the parallel-axis theorem. 
10.6 Torque 
71 . Two flywheels of negligible mass and different radii 
are bonded together and rotate about a common 
axis (see below). The smaller flywheel of radius 30 
cm has a cord that has a pulling force of 50 N on it. 
What pulling force needs to be applied to the cord 
connecting the larger flywheel of radius 50 cm such 
that the combination does not rotate? 
10 • Chapter Review     507

72 . The cylinder head bolts on a car are to be 
tightened with a torque of 62.0 N
. If a 
mechanic uses a wrench of length 20 cm, what 
perpendicular force must he exert on the end of 
the wrench to tighten a bolt correctly? 
73 . (a) When opening a door, you push on it 
perpendicularly with a force of 55.0 N at a 
distance of 0.850 m from the hinges. What 
torque are you exerting relative to the hinges? 
(b) Does it matter if you push at the same height 
as the hinges? There is only one pair of hinges. 
74 . When tightening a bolt, you push 
perpendicularly on a wrench with a force of 165 
N at a distance of 0.140 m from the center of the 
bolt. How much torque are you exerting in 
newton-meters (relative to the center of the 
bolt)? 
75 . What hanging mass must be placed on the cord 
to keep the pulley from rotating (see the 
following figure)? The mass on the frictionless 
plane is 5.0 kg. The mass on the plane is 
connected to a cord that wraps around the 
pulley’s inner radius of 20 cm. The hanging mass 
is connected to a cord that wraps around the 
pulley’s outer radius of 30 cm. 
76 . A simple pendulum consists of a massless tether 
50 cm in length connected to a pivot and a small 
mass of 1.0 kg attached at the other end. What 
is the torque about the pivot when the pendulum 
makes an angle of 
 with respect to the 
vertical? 
77 . Calculate the torque about the z-axis that is out of 
the page at the origin in the following figure, given 
that 
. 
78 . A seesaw has length 10.0 m and uniform mass 10.0 
kg and is resting at an angle of 
 with respect to 
the ground (see the following figure). The pivot is 
located at 6.0 m. What magnitude of force needs to 
be applied perpendicular to the seesaw at the raised 
end so as to allow the seesaw to barely start to 
rotate? 
79 . A pendulum consists of a rod of mass 1 kg and 
length 1 m connected to a pivot with a solid 
sphere attached at the other end with mass 0.5 
kg and radius 30 cm. What is the torque about 
the pivot when the pendulum makes an angle of 
 with respect to the vertical? 
80 . A torque of 
 is required to raise a 
drawbridge (see the following figure). What is the 
tension necessary to produce this torque? Would it 
be easier to raise the drawbridge if the angle  were 
larger or smaller? 
508     10 • Chapter Review
Access for free at openstax.org

81 . A horizontal beam of length 3 m and mass 2.0 kg 
has a mass of 1.0 kg and width 0.2 m sitting at the 
end of the beam (see the following figure). What is 
the torque of the system about the support at the 
wall? 
82 . What force must be applied to end of a rod along 
the x-axis of length 2.0 m in order to produce a 
torque on the rod about the origin of 
? 
83 . What is the torque about the origin of the force 
 if it is applied at the 
point whose position is: 
10.7 Newton’s Second Law for Rotation 
84 . You have a grindstone (a disk) that is 90.0 kg, 
has a 0.340-m radius, and is turning at 90.0 
rpm, and you press a steel axe against it with a 
radial force of 20.0 N. (a) Assuming the kinetic 
coefficient of friction between steel and stone is 
0.20, calculate the angular acceleration of the 
grindstone. (b) How many turns will the stone 
make before coming to rest? 
85 . Suppose you exert a force of 180 N tangential to 
a 0.280-m-radius, 75.0-kg grindstone (a solid 
disk). (a)What torque is exerted? (b) What is the 
angular acceleration assuming negligible 
opposing friction? (c) What is the angular 
acceleration if there is an opposing frictional 
force of 20.0 N exerted 1.50 cm from the axis? 
86 . A flywheel (
) starting from rest 
acquires an angular velocity of 200.0 rad/s while 
subject to a constant torque from a motor for 5 
s. (a) What is the angular acceleration of the 
flywheel? (b) What is the magnitude of the 
torque? 
87 . A constant torque is applied to a rigid body 
whose moment of inertia is 
 around 
the axis of rotation. If the wheel starts from rest 
and attains an angular velocity of 20.0 rad/s in 
10.0 s, what is the applied torque? 
88 . A torque of 50.0 N-m is applied to a grinding 
wheel (
) for 20 s. (a) If it starts 
from rest, what is the angular velocity of the 
grinding wheel after the torque is removed? (b) 
Through what angle does the wheel move while 
the torque is applied? 
89 . A flywheel (
) rotating at 500.0 
rev/min is brought to rest by friction in 2.0 min. 
What is the frictional torque on the flywheel? 
90 . A uniform cylindrical grinding wheel of mass 
50.0 kg and diameter 1.0 m is turned on by an 
electric motor. The friction in the bearings is 
negligible. (a) What torque must be applied to 
the wheel to bring it from rest to 120 rev/min in 
20 revolutions? (b) A tool whose coefficient of 
kinetic friction with the wheel is 0.60 is pressed 
perpendicularly against the wheel with a force of 
40.0 N. What torque must be supplied by the 
motor to keep the wheel rotating at a constant 
angular velocity? 
91 . Suppose when Earth was created, it was not 
rotating. However, after the application of a 
uniform torque for 6 days according to the 
current length of a day, it was rotating at 1 rev/
day. (a) What was the angular acceleration 
during the 6 days? (b) What torque was applied 
to Earth during this period? (c) What force 
tangent to Earth at its equator would produce 
10 • Chapter Review     509

this torque? 
92 . A pulley of moment of inertia 
 is mounted on a 
wall as shown in the following figure. Light strings are 
wrapped around two circumferences of the pulley and 
weights are attached. What are (a) the angular 
acceleration of the pulley and (b) the linear acceleration 
of each weight? Assume the following data: 
. 
93 . A block of mass 3 kg slides down an inclined 
plane at an angle of 
 with a massless tether 
attached to a pulley with mass 1 kg and radius 
0.5 m at the top of the incline (see the following 
figure). The pulley can be approximated as a 
disk. The coefficient of kinetic friction on the 
plane is 0.4. What is the acceleration of the 
block? 
94 . The cart shown below moves across the table top as the 
block falls. What is the acceleration of the cart? Neglect 
friction and assume the following 
data:
95 . A uniform rod of mass and length is held vertically 
by two strings of negligible mass, as shown below. 
(a) Immediately after the string is cut, what is the 
linear acceleration of the free end of the stick? (b) Of 
the middle of the stick? 
96 . A thin stick of mass 0.2 kg and length 
 is 
attached to the rim of a metal disk of mass 
 and radius 
. The stick is free 
to rotate around a horizontal axis through its other 
end (see the following figure). (a) If the combination 
is released with the stick horizontal, what is the 
speed of the center of the disk when the stick is 
vertical? (b) What is the acceleration of the center of 
the disk at the instant the stick is released? (c) At 
the instant the stick passes through the vertical? 
510     10 • Chapter Review
Access for free at openstax.org

10.8 Work and Power for Rotational Motion 
97 . A wind turbine rotates at 20 rev/min. If its power 
output is 2.0 MW, what is the torque produced 
on the turbine from the wind? 
98 . A clay cylinder of radius 20 cm on a potter’s 
wheel spins at a constant rate of 10 rev/s. The 
potter applies a force of 10 N to the clay with his 
hands where the coefficient of friction is 0.1 
between his hands and the clay. What is the 
power that the potter has to deliver to the wheel 
to keep it rotating at this constant rate? 
99 . A uniform cylindrical grindstone has a mass of 
10 kg and a radius of 12 cm. (a) What is the 
rotational kinetic energy of the grindstone when 
it is rotating at 
 (b) After the 
grindstone’s motor is turned off, a knife blade is 
pressed against the outer edge of the grindstone 
with a perpendicular force of 5.0 N. The 
coefficient of kinetic friction between the 
grindstone and the blade is 0.80. Use the work 
energy theorem to determine how many turns 
the grindstone makes before it stops. 
100 . A uniform disk of mass 500 kg and radius 0.25 m 
is mounted on frictionless bearings so it can 
rotate freely around a vertical axis through its 
center (see the following figure). A cord is 
wrapped around the rim of the disk and pulled 
with a force of 10 N. (a) How much work has the 
force done at the instant the disk has completed 
three revolutions, starting from rest? (b) 
Determine the torque due to the force, then 
calculate the work done by this torque at the 
instant the disk has completed three 
revolutions? (c) What is the angular velocity at 
that instant? (d) What is the power output of the 
force at that instant? 
101 . A propeller is accelerated from rest to an angular 
velocity of 1000 rev/min over a period of 6.0 
seconds by a constant torque of 
. (a) What is the moment of 
inertia of the propeller? (b) What power is being 
provided to the propeller 3.0 s after it starts 
rotating? 
102 . A sphere of mass 1.0 kg and radius 0.5 m is 
attached to the end of a massless rod of length 
3.0 m. The rod rotates about an axis that is at 
the opposite end of the sphere (see below). The 
system rotates horizontally about the axis at a 
constant 400 rev/min. After rotating at this 
angular speed in a vacuum, air resistance is 
introduced and provides a force 
 on the 
sphere opposite to the direction of motion. What 
is the power provided by air resistance to the 
system 100.0 s after air resistance is 
introduced? 
103 . A uniform rod of length L and mass M is held 
vertically with one end resting on the floor as 
shown below. When the rod is released, it rotates 
around its lower end until it hits the floor. 
Assuming the lower end of the rod does not slip, 
what is the linear velocity of the upper end when it 
hits the floor? 
104 . An athlete in a gym applies a constant force of 
50 N to the pedals of a bicycle at a rate of the 
pedals moving 60 rev/min. The length of the 
pedal arms is 30 cm. What is the power 
delivered to the bicycle by the athlete? 
105 . A 2-kg block on a frictionless inclined plane at 
 has a cord attached to a pulley of mass 1 kg 
and radius 20 cm (see the following figure). The 
block slides a distance of 0.50 m. (a) What is the 
10 • Chapter Review     511

acceleration of the block down the plane? (b) 
What is the work done by the cord on the pulley? 
106 . Small bodies of mass 
 are attached to 
opposite ends of a thin rigid rod of length L and 
mass M. The rod is mounted so that it is free to 
rotate in a horizontal plane around a vertical axis 
(see below). What distance d from 
 should the 
rotational axis be so that a minimum amount of 
work is required to set the rod rotating at an 
angular velocity 
Additional Problems 
107 . A cyclist is riding such that the wheels of the 
bicycle have a rotation rate of 3.0 rev/s. If the 
cyclist brakes such that the rotation rate of the 
wheels decrease at a rate of 
, how 
long does it take for the cyclist to come to a 
complete stop? 
108 . Calculate the angular velocity of the orbital 
motion of Earth around the Sun. 
109 . A phonograph turntable rotating at 33 1/3 rev/
min slows down and stops in 1.0 min. (a) What is 
the turntable’s angular acceleration, in 
radians/s2, assuming it is constant? (b) How 
many revolutions does the turntable make while 
stopping? 
110 . With the aid of a string, a gyroscope is 
accelerated from rest to 32 rad/s in 0.40 s under 
a constant angular acceleration. (a) What is its 
angular acceleration in 
? (b) How many 
revolutions does it go through in the process? 
111 . Suppose a piece of dust has fallen on a CD. If the 
spin rate of the CD is 500 rpm, and the piece of 
dust is 4.3 cm from the center, what is the total 
distance traveled by the dust in 3 minutes? 
(Ignore accelerations due to getting the CD 
rotating.) 
112 . A system of point particles is rotating about a 
fixed axis at 4 rev/s. The particles are fixed with 
respect to each other. The masses and distances 
to the axis of the point particles are 
, 
, 
. (a) What is the 
moment of inertia of the system? (b) What is the 
rotational kinetic energy of the system? 
113 . Calculate the moment of inertia of a skater given 
the following information. (a) The 60.0-kg skater 
is approximated as a cylinder that has a 
0.110-m radius. (b) The skater with arms 
extended is approximated by a cylinder that is 
52.5 kg, has a 0.110-m radius, and has two 
0.900-m-long arms which are 3.75 kg each and 
extend straight out from the cylinder like rods 
rotated about their ends. 
114 . A stick of length 1.0 m and mass 6.0 kg is free to 
rotate about a horizontal axis through the center. 
Small bodies of masses 4.0 and 2.0 kg are attached 
to its two ends (see the following figure). The stick is 
released from the horizontal position. What is the 
angular velocity of the stick when it swings through 
the vertical? 
115 . A pendulum consists of a rod of length 2 m and 
mass 3 kg with a solid sphere of mass 1 kg and 
radius 0.3 m attached at one end. The axis of 
512     10 • Chapter Review
Access for free at openstax.org

rotation is as shown below. What is the angular 
velocity of the pendulum at its lowest point if it 
is released from rest at an angle of 
116 . Calculate the torque of the 40-N force around the 
axis through O and perpendicular to the plane of the 
page as shown below. 
117 . Two children push on opposite sides of a door 
during play. Both push horizontally and 
perpendicular to the door. One child pushes with 
a force of 17.5 N at a distance of 0.600 m from 
the hinges, and the second child pushes at a 
distance of 0.450 m. What force must the 
second child exert to keep the door from 
moving? Assume friction is negligible. 
118 . The force of 
 is applied at 
. What is the torque of this 
force about the origin? 
119 . An automobile engine can produce 200 N m of 
torque. Calculate the angular acceleration 
produced if 95.0% of this torque is applied to 
the drive shaft, axle, and rear wheels of a car, 
given the following information. The car is 
suspended so that the wheels can turn freely. 
Each wheel acts like a 15.0-kg disk that has a 
0.180-m radius. The walls of each tire act like a 
2.00-kg annular ring that has inside radius of 
0.180 m and outside radius of 0.320 m. The 
tread of each tire acts like a 10.0-kg hoop of 
radius 0.330 m. The 14.0-kg axle acts like a rod 
that has a 2.00-cm radius. The 30.0-kg drive 
shaft acts like a rod that has a 3.20-cm radius. 
120 . A grindstone with a mass of 50 kg and radius 0.8 
m maintains a constant rotation rate of 4.0 rev/s 
by a motor while a knife is pressed against the 
edge with a force of 5.0 N. The coefficient of 
kinetic friction between the grindstone and the 
blade is 0.8. What is the power provided by the 
motor to keep the grindstone at the constant 
rotation rate? 
Challenge Problems 
121 . The angular acceleration of a rotating rigid body 
is given by 
. If the body 
starts rotating from rest at 
, (a) what is the 
angular velocity? (b) Angular position? (c) What 
angle does it rotate through in 10 s? (d) Where 
does the vector perpendicular to the axis of 
rotation indicating 
 at 
 lie at 
? 
122 . Earth’s day has increased by 0.002 s in the last 
century. If this increase in Earth’s period is 
constant, how long will it take for Earth to come 
to rest? 
123 . A disk of mass m, radius R, and area A has a 
surface mass density 
 (see the following 
figure). What is the moment of inertia of the disk 
about an axis through the center? 
124 . Zorch, an archenemy of Rotation Man, decides to 
slow Earth’s rotation to once per 28.0 h by 
exerting an opposing force at and parallel to the 
equator. Rotation Man is not immediately 
concerned, because he knows Zorch can only 
exert a force of 
 (a little greater 
than a Saturn V rocket’s thrust). How long must 
10 • Chapter Review     513

Zorch push with this force to accomplish his 
goal? (This period gives Rotation Man time to 
devote to other villains.) 
125 . A cord is wrapped around the rim of a solid cylinder 
of radius 0.25 m, and a constant force of 40 N is 
exerted on the cord shown, as shown in the 
following figure. The cylinder is mounted on 
frictionless bearings, and its moment of inertia is 
. (a) Use the work energy theorem to 
calculate the angular velocity of the cylinder after 
5.0 m of cord have been removed. (b) If the 40-N 
force is replaced by a 40-N weight, what is the 
angular velocity of the cylinder after 5.0 m of cord 
have unwound? 
514     10 • Chapter Review
Access for free at openstax.org

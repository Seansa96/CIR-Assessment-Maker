# Chapter 4 Motion in Two and Three Dimensions

INTRODUCTION 
CHAPTER 4 
Motion in Two and Three Dimensions 
4.1 Displacement and Velocity Vectors 
4.2 Acceleration Vector 
4.3 Projectile Motion 
4.4 Uniform and Nonuniform Circular Motion 
4.5 Relative Motion in One and Two Dimensions 
To give a complete description of kinematics, we must explore motion in two and three 
dimensions. After all, most objects in our universe do not move in straight lines; rather, they follow curved paths. 
From kicked footballs to the flight paths of birds to the orbital motions of celestial bodies and down to the flow of 
blood plasma in your veins, most motion follows curved trajectories. 
Fortunately, the treatment of motion in one dimension in the previous chapter has given us a foundation on which to 
build, as the concepts of position, displacement, velocity, and acceleration defined in one dimension can be 
expanded to two and three dimensions. Consider the Red Arrows, also known as the Royal Air Force Aerobatic team 
of the United Kingdom. Each jet follows a unique curved trajectory in three-dimensional airspace, as well as has a 
unique velocity and acceleration. Thus, to describe the motion of any of the jets accurately, we must assign to each 
jet a unique position vector in three dimensions as well as a unique velocity and acceleration vector. We can apply 
the same basic equations for displacement, velocity, and acceleration we derived in Motion Along a Straight Line to 
describe the motion of the jets in two and three dimensions, but with some modifications—in particular, the 
inclusion of vectors. 
In this chapter we also explore two special types of motion in two dimensions: projectile motion and circular 
motion. Last, we conclude with a discussion of relative motion. In the chapter-opening picture, each jet has a 
relative motion with respect to any other jet in the group or to the people observing the air show on the ground. 
FIGURE 4.1 The Red Arrows is the aerobatics display team of Britain’s Royal Air Force. Based in Lincolnshire, England, they perform 
precision flying shows at high speeds, which requires accurate measurement of position, velocity, and acceleration in three dimensions. 
(credit: modification of work by Phil Long) 
CHAPTER OUTLINE 

4.1 Displacement and Velocity Vectors 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Calculate position vectors in a multidimensional displacement problem. 
• Solve for the displacement in two or three dimensions. 
• Calculate the velocity vector given the position vector as a function of time. 
• Calculate the average velocity in multiple dimensions. 
Displacement and velocity in two or three dimensions are straightforward extensions of the one-dimensional 
definitions. However, now they are vector quantities, so calculations with them have to follow the rules of vector 
algebra, not scalar algebra. 
Displacement Vector 
To describe motion in two and three dimensions, we must first establish a coordinate system and a convention for 
the axes. We generally use the coordinates x, y, and z to locate a particle at point P(x, y, z) in three dimensions. If the 
particle is moving, the variables x, y, and z are functions of time (t): 
The position vector from the origin of the coordinate system to point P is 
 In unit vector notation, introduced in 
Coordinate Systems and Components of a Vector, 
 is 
Figure 4.2 shows the coordinate system and the vector to point P, where a particle could be located at a particular 
time t. Note the orientation of the x, y, and z axes. This orientation is called a right-handed coordinate system 
(Coordinate Systems and Components of a Vector) and it is used throughout the chapter. 
FIGURE 4.2 A three-dimensional coordinate system with a particle at position P(x(t), y(t), z(t)). 
With our definition of the position of a particle in three-dimensional space, we can formulate the three-dimensional 
displacement. Figure 4.3 shows a particle at time 
 located at 
 with position vector 
 At a later time 
 the 
particle is located at 
 with position vector 
. The displacement vector 
 is found by subtracting 
 from 
 
Vector addition is discussed in Vectors. Note that this is the same operation we did in one dimension, but now the 
vectors are in three-dimensional space. 
4.1 
4.2 
4.3 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

FIGURE 4.3 The displacement 
 is the vector from 
 to 
. 
The following examples illustrate the concept of displacement in multiple dimensions. 
EXAMPLE 4.1 
Polar Orbiting Satellite 
A satellite is in a circular polar orbit around Earth at an altitude of 400 km—meaning, it passes directly overhead at 
the North and South Poles. What is the magnitude and direction of the displacement vector from when it is directly 
over the North Pole to when it is at 
 latitude? 
Strategy 
We make a picture of the problem to visualize the solution graphically. This will aid in our understanding of the 
displacement. We then use unit vectors to solve for the displacement. 
Solution 
Figure 4.4 shows the surface of Earth and a circle that represents the orbit of the satellite. Although satellites are 
moving in three-dimensional space, they follow trajectories of ellipses, which can be graphed in two dimensions. 
The position vectors are drawn from the center of Earth, which we take to be the origin of the coordinate system, 
with the y-axis as north and the x-axis as east. The vector between them is the displacement of the satellite. We 
take the radius of Earth as 6370 km, so the length of each position vector is 6770 km. 
4.1 • Displacement and Velocity Vectors

FIGURE 4.4 Two position vectors are drawn from the center of Earth, which is the origin of the coordinate system, with the y-axis as north 
and the x-axis as east. The vector between them is the displacement of the satellite. 
In unit vector notation, the position vectors are 
Evaluating the sine and cosine, we have 
Now we can find 
, the displacement of the satellite: 
The magnitude of the displacement is 
 The angle the displacement 
makes with the x-axis is 
Significance 
Plotting the displacement gives information and meaning to the unit vector solution to the problem. When plotting 
the displacement, we need to include its components as well as its magnitude and the angle it makes with a chosen 
axis—in this case, the x-axis (Figure 4.5). 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

FIGURE 4.5 Displacement vector with components, angle, and magnitude. 
Note that the satellite took a curved path along its circular orbit to get from its initial position to its final position in 
this example. It also could have traveled 4787 km east, then 11,557 km south to arrive at the same location. Both of 
these paths are longer than the length of the displacement vector. In fact, the displacement vector gives the 
shortest path between two points in one, two, or three dimensions. 
Many applications in physics can have a series of displacements, as discussed in the previous chapter. The total 
displacement is the sum of the individual displacements, only this time, we need to be careful, because we are 
adding vectors. We illustrate this concept with an example of Brownian motion. 
EXAMPLE 4.2 
Brownian Motion 
Brownian motion is a chaotic random motion of particles suspended in a fluid, resulting from collisions with the 
molecules of the fluid. This motion is three-dimensional. The displacements in numerical order of a particle 
undergoing Brownian motion could look like the following, in micrometers (Figure 4.6): 
What is the total displacement of the particle from the origin? 
4.1 • Displacement and Velocity Vectors

FIGURE 4.6 Trajectory of a particle undergoing random displacements of Brownian motion. The total displacement is shown in red. 
Solution 
We form the sum of the displacements and add them as vectors: 
To complete the solution, we express the displacement as a magnitude and direction, 
with respect to the x-axis in the xz-plane. 
Significance 
From the figure we can see the magnitude of the total displacement is less than the sum of the magnitudes of the 
individual displacements. 
Velocity Vector 
In the previous chapter we found the instantaneous velocity by calculating the derivative of the position function 
with respect to time. We can do the same operation in two and three dimensions, but we use vectors. The 
instantaneous velocity vector is now 
Let’s look at the relative orientation of the position vector and velocity vector graphically. In Figure 4.7 we show the 
vectors 
 and 
 which give the position of a particle moving along a path represented by the gray line. As 
 goes to zero, the velocity vector, given by Equation 4.4, becomes tangent to the path of the particle at time t. 
4.4 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

FIGURE 4.7 A particle moves along a path given by the gray line. In the limit as 
 approaches zero, the velocity vector becomes tangent to 
the path of the particle. 
Equation 4.4 can also be written in terms of the components of 
 Since 
we can write 
where 
If only the average velocity is of concern, we have the vector equivalent of the one-dimensional average velocity for 
two and three dimensions: 
EXAMPLE 4.3 
Calculating the Velocity Vector 
The position function of a particle is 
 (a) What is the instantaneous velocity 
and speed at t = 2.0 s? (b) What is the average velocity between 1.0 s and 3.0 s? 
Solution 
Using Equation 4.5 and Equation 4.6, and taking the derivative of the position function with respect to time, we find 
(a) 
Speed 
(b) From Equation 4.7, 
Significance 
We see the average velocity is the same as the instantaneous velocity at t = 2.0 s, as a result of the velocity function 
4.5 
4.6 
4.7 
4.1 • Displacement and Velocity Vectors

being linear. This need not be the case in general. In fact, most of the time, instantaneous and average velocities are 
not the same. 
CHECK YOUR UNDERSTANDING 4.1 
The position function of a particle is 
 (a) What is the instantaneous velocity at t = 3 s? (b) Is the 
average velocity between 2 s and 4 s equal to the instantaneous velocity at t = 3 s? 
The Independence of Perpendicular Motions 
When we look at the three-dimensional equations for position and velocity written in unit vector notation, Equation 
4.2 and Equation 4.5, we see the components of these equations are separate and unique functions of time that do 
not depend on one another. Motion along the x direction has no part of its motion along the y and z directions, and 
similarly for the other two coordinate axes. Thus, the motion of an object in two or three dimensions can be divided 
into separate, independent motions along the perpendicular axes of the coordinate system in which the motion 
takes place. 
To illustrate this concept with respect to displacement, consider a woman walking from point A to point B in a city 
with square blocks. The woman taking the path from A to B may walk east for so many blocks and then north (two 
perpendicular directions) for another set of blocks to arrive at B. How far she walks east is affected only by her 
motion eastward. Similarly, how far she walks north is affected only by her motion northward. 
An example illustrating the independence of vertical and horizontal motions is given by two baseballs. One baseball 
is dropped from rest. At the same instant, another is thrown horizontally from the same height and it follows a 
curved path. A stroboscope captures the positions of the balls at fixed time intervals as they fall (Figure 4.8). 
INDEPENDENCE OF MOTION 
In the kinematic description of motion, we are able to treat the horizontal and vertical components of motion 
separately. In many cases, motion in the horizontal direction does not affect motion in the vertical direction, and 
vice versa. 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

FIGURE 4.8 A diagram of the motions of two identical balls: one falls from rest and the other has an initial horizontal velocity. Each 
subsequent position is an equal time interval. Arrows represent the horizontal and vertical velocities at each position. The ball on the right 
has an initial horizontal velocity whereas the ball on the left has no horizontal velocity. Despite the difference in horizontal velocities, the 
vertical velocities and positions are identical for both balls, which shows the vertical and horizontal motions are independent. 
It is remarkable that for each flash of the strobe, the vertical positions of the two balls are the same. This similarity 
implies vertical motion is independent of whether the ball is moving horizontally. (Assuming no air resistance, the 
vertical motion of a falling object is influenced by gravity only, not by any horizontal forces.) Careful examination of 
the ball thrown horizontally shows it travels the same horizontal distance between flashes. This is because there are 
no additional forces on the ball in the horizontal direction after it is thrown. This result means horizontal velocity is 
constant and is affected neither by vertical motion nor by gravity (which is vertical). Note this case is true for ideal 
conditions only. In the real world, air resistance affects the speed of the balls in both directions. 
The two-dimensional curved path of the horizontally thrown ball is composed of two independent one-dimensional 
motions (horizontal and vertical). The key to analyzing such motion, called projectile motion, is to resolve it into 
motions along perpendicular directions. Resolving two-dimensional motion into perpendicular components is 
possible because the components are independent. 
4.2 Acceleration Vector 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Calculate the acceleration vector given the velocity function in unit vector notation. 
• Describe the motion of a particle with a constant acceleration in three dimensions. 
• Use the one-dimensional motion equations along perpendicular axes to solve a problem in two or three 
dimensions with a constant acceleration. 
• Express the acceleration in unit vector notation. 
Instantaneous Acceleration 
In addition to obtaining the displacement and velocity vectors of an object in motion, we often want to know its 
acceleration vector at any point in time along its trajectory. This acceleration vector is the instantaneous 
acceleration and it can be obtained from the derivative with respect to time of the velocity function, as we have seen 
in a previous chapter. The only difference in two or three dimensions is that these are now vector quantities. Taking 
the derivative with respect to time 
 we find 
4.2 • Acceleration Vector

The acceleration in terms of components is 
Also, since the velocity is the derivative of the position function, we can write the acceleration in terms of the second 
derivative of the position function: 
EXAMPLE 4.4 
Finding an Acceleration Vector 
A particle has a velocity of 
 (a) What is the acceleration function? (b) What is the 
acceleration vector at t = 2.0 s? Find its magnitude and direction. 
Solution 
(a) We take the first derivative with respect to time of the velocity function to find the acceleration. The derivative is 
taken component by component: 
(b) Evaluating 
 gives us the direction in unit vector notation. The magnitude of 
the acceleration is 
Significance 
In this example we find that acceleration has a time dependence and is changing throughout the motion. Let’s 
consider a different velocity function for the particle. 
EXAMPLE 4.5 
Finding a Particle Acceleration 
A particle has a position function 
​
 (a) What is the velocity? (b) What is the 
acceleration? (c) Describe the motion from t = 0 s. 
Strategy 
We can gain some insight into the problem by looking at the position function. It is linear in y and z, so we know the 
acceleration in these directions is zero when we take the second derivative. Also, note that the position in the x 
direction is zero for t = 0 s and t = 10 s. 
Solution 
(a) Taking the derivative with respect to time of the position function, we find 
The velocity function is linear in time in the x direction and is constant in the y and z directions. 
4.8 
​
4.9 
4.10 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

(b) Taking the derivative of the velocity function, we find 
The acceleration vector is a constant in the negative x-direction. 
(c) The trajectory of the particle can be seen in Figure 4.9. Let’s look in the y and z directions first. The particle’s 
position increases steadily as a function of time with a constant velocity in these directions. In the x direction, 
however, the particle follows a path in positive x until t = 5 s, when it reverses direction. We know this from looking 
at the velocity function, which becomes zero at this time and negative thereafter. We also know this because the 
acceleration is negative and constant—meaning, the particle is accelerating in the opposite direction. The particle’s 
position reaches 25 m, where it then reverses direction and begins to accelerate in the negative x direction. The 
position reaches zero at t = 10 s. 
FIGURE 4.9 The particle starts at point (x, y, z) = (0, 0, 0) with position vector 
 as shown with red stars. The projection of the trajectory 
onto the xy-plane is shown with blue dots. The values of y and z increase linearly as a function of time, whereas x has a turning point at t = 5 
s and 25 m, when it reverses direction. At this point, the x component of the velocity becomes negative. At t = 10 s, the particle is back to 0 
m in the x direction. 
Significance 
By graphing the trajectory of the particle, we can better understand its motion, given by the numerical results of the 
kinematic equations. 
CHECK YOUR UNDERSTANDING 4.2 
Suppose the acceleration function has the form 
 where a, b, and c are constants. What can 
be said about the functional form of the velocity function? 
Constant Acceleration 
Multidimensional motion with constant acceleration can be treated the same way as shown in the previous chapter 
for one-dimensional motion. Earlier we showed that three-dimensional motion is equivalent to three one-
4.2 • Acceleration Vector

dimensional motions, each along an axis perpendicular to the others. To develop the relevant equations in each 
direction, let’s consider the two-dimensional problem of a particle moving in the xy plane with constant 
acceleration, ignoring the z-component for the moment. The acceleration vector is 
Each component of the motion has a separate set of equations similar to Equation 3.10–Equation 3.14 of the 
previous chapter on one-dimensional motion. We show only the equations for position and velocity in the x- and 
y-directions. A similar set of kinematic equations could be written for motion in the z-direction: 
Here the subscript 0 denotes the initial position or velocity. Equation 4.11 to Equation 4.18 can be substituted into 
Equation 4.2 and Equation 4.5 without the z-component to obtain the position vector and velocity vector as a 
function of time in two dimensions: 
The following example illustrates a practical use of the kinematic equations in two dimensions. 
EXAMPLE 4.6 
A Skier 
Figure 4.10 shows a skier moving with an acceleration of 
 down a slope of 
 at t = 0. With the origin of the 
coordinate system at the front of the lodge, her initial position and velocity are 
and 
(a) What are the x- and y-components of the skier’s position and velocity as functions of time? (b) What are her 
position and velocity at t = 10.0 s? 
4.11 
4.12 
4.13 
4.14 
4.15 
4.16 
4.17 
4.18 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

FIGURE 4.10 A skier has an acceleration of 
 down a slope of 
 The origin of the coordinate system is at the ski lodge. 
Strategy 
Since we are evaluating the components of the motion equations in the x and y directions, we need to find the 
components of the acceleration and put them into the kinematic equations. The components of the acceleration are 
found by referring to the coordinate system in Figure 4.10. Then, by inserting the components of the initial position 
and velocity into the motion equations, we can solve for her position and velocity at a later time t. 
Solution 
(a) The origin of the coordinate system is at the top of the hill with y-axis vertically upward and the x-axis horizontal. 
By looking at the trajectory of the skier, the x-component of the acceleration is positive and the y-component is 
negative. Since the angle is 
 down the slope, we find 
Inserting the initial position and velocity into Equation 4.12 and Equation 4.13 for x, we have 
For y, we have 
(b) Now that we have the equations of motion for x and y as functions of time, we can evaluate them at t = 10.0 s: 
4.2 • Acceleration Vector

The position and velocity at t = 10.0 s are, finally, 
The magnitude of the velocity of the skier at 10.0 s is 25 m/s, which is 60 mi/h. 
Significance 
It is useful to know that, given the initial conditions of position, velocity, and acceleration of an object, we can find 
the position, velocity, and acceleration at any later time. 
With Equation 4.8 through Equation 4.10 we have completed the set of expressions for the position, velocity, and 
acceleration of an object moving in two or three dimensions. If the trajectories of the objects look something like the 
“Red Arrows” in the opening picture for the chapter, then the expressions for the position, velocity, and acceleration 
can be quite complicated. In the sections to follow we examine two special cases of motion in two and three 
dimensions by looking at projectile motion and circular motion. 
INTERACTIVE 
At this University of Colorado Boulder website (https://openstax.org/l/21phetmotladyb), you can explore the 
position velocity and acceleration of a ladybug with an interactive simulation that allows you to change these 
parameters. 
4.3 Projectile Motion 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Use one-dimensional motion in perpendicular directions to analyze projectile motion. 
• Calculate the range, time of flight, and maximum height of a projectile that is launched and impacts a flat, 
horizontal surface. 
• Find the time of flight and impact velocity of a projectile that lands at a different height from that of 
launch. 
• Calculate the trajectory of a projectile. 
Projectile motion is the motion of an object thrown or projected into the air, subject only to acceleration as a result 
of gravity. The applications of projectile motion in physics and engineering are numerous. Some examples include 
meteors as they enter Earth’s atmosphere, fireworks, and the motion of any ball in sports. Such objects are called 
projectiles and their path is called a trajectory. The motion of falling objects as discussed in Motion Along a Straight 
Line is a simple one-dimensional type of projectile motion in which there is no horizontal movement. In this section, 
we consider two-dimensional projectile motion, and our treatment neglects the effects of air resistance. 
The most important fact to remember here is that motions along perpendicular axes are independent and thus can 
be analyzed separately. We discussed this fact in Displacement and Velocity Vectors, where we saw that vertical and 
horizontal motions are independent. The key to analyzing two-dimensional projectile motion is to break it into two 
motions: one along the horizontal axis and the other along the vertical. (This choice of axes is the most sensible 
because acceleration resulting from gravity is vertical; thus, there is no acceleration along the horizontal axis when 
air resistance is negligible.) As is customary, we call the horizontal axis the x-axis and the vertical axis the y-axis. It 
is not required that we use this choice of axes; it is simply convenient in the case of gravitational acceleration. In 
other cases we may choose a different set of axes. Figure 4.11 illustrates the notation for displacement, where we 
define  to be the total displacement, and  and  are its component vectors along the horizontal and vertical axes, 
respectively. The magnitudes of these vectors are s, x, and y. 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

FIGURE 4.11 The total displacement s of a soccer ball at a point along its path. The vector  has components  and  along the horizontal 
and vertical axes. Its magnitude is s and it makes an angle Φ with the horizontal. 
To describe projectile motion completely, we must include velocity and acceleration, as well as displacement. We 
must find their components along the x- and y-axes. Let’s assume all forces except gravity (such as air resistance 
and friction, for example) are negligible. Defining the positive direction to be upward, the components of 
acceleration are then very simple: 
Because gravity is vertical, 
 If 
 this means the initial velocity in the x direction is equal to the final 
velocity in the x direction, or 
 With these conditions on acceleration and velocity, we can write the 
kinematic Equation 4.11 through Equation 4.18 for motion in a uniform gravitational field, including the rest of the 
kinematic equations for a constant acceleration from Motion with Constant Acceleration. The kinematic equations 
for motion in a uniform gravitational field become kinematic equations with 
Horizontal Motion 
Vertical Motion 
Using this set of equations, we can analyze projectile motion, keeping in mind some important points. 
PROBLEM-SOLVING STRATEGY 
Projectile Motion 
1. Resolve the motion into horizontal and vertical components along the x- and y-axes. The magnitudes of the 
components of displacement  along these axes are x and y. The magnitudes of the components of velocity 
are 
 where v is the magnitude of the velocity and θ is its direction relative to the 
horizontal, as shown in Figure 4.12. 
4.19 
4.20 
4.21 
4.22 
4.23 
4.3 • Projectile Motion

2. Treat the motion as two independent one-dimensional motions: one horizontal and the other vertical. Use the 
kinematic equations for horizontal and vertical motion presented earlier. 
3. Solve for the unknowns in the two separate motions: one horizontal and one vertical. Note that the only 
common variable between the motions is time t. The problem-solving procedures here are the same as those 
for one-dimensional kinematics and are illustrated in the following solved examples. 
4. Recombine quantities in the horizontal and vertical directions to find the total displacement  and velocity 
Solve for the magnitude and direction of the displacement and velocity using 
where Φ is the direction of the displacement 
FIGURE 4.12 (a) We analyze two-dimensional projectile motion by breaking it into two independent one-dimensional motions along the 
vertical and horizontal axes. (b) The horizontal motion is simple, because 
 and 
 is a constant. (c) The velocity in the vertical 
direction begins to decrease as the object rises. At its highest point, the vertical velocity is zero. As the object falls toward Earth again, the 
vertical velocity increases again in magnitude but points in the opposite direction to the initial vertical velocity. (d) The x and y motions are 
recombined to give the total velocity at any given point on the trajectory. 
EXAMPLE 4.7 
A Fireworks Projectile Explodes High and Away 
During a fireworks display, a shell is shot into the air with an initial speed of 70.0 m/s at an angle of 
 above the 
horizontal, as illustrated in Figure 4.13. The fuse is timed to ignite the shell just as it reaches its highest point above 
the ground. (a) Calculate the height at which the shell explodes. (b) How much time passes between the launch of 
the shell and the explosion? (c) What is the horizontal displacement of the shell when it explodes? (d) What is the 
total displacement from the point of launch to the highest point? 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

FIGURE 4.13 The trajectory of a fireworks shell. The fuse is set to explode the shell at the highest point in its trajectory, which is found to be 
at a height of 233 m and 125 m away horizontally. 
Strategy 
The motion can be broken into horizontal and vertical motions in which 
 and 
 We can then define 
and 
 to be zero and solve for the desired quantities. 
Solution 
(a) By “height” we mean the altitude or vertical position y above the starting point. The highest point in any 
trajectory, called the apex, is reached when 
 Since we know the initial and final velocities, as well as the 
initial position, we use the following equation to find y: 
Because 
 and 
 are both zero, the equation simplifies to 
Solving for y gives 
Now we must find 
 the component of the initial velocity in the y direction. It is given by 
 where 
 is the initial velocity of 70.0 m/s and 
 is the initial angle. Thus, 
and y is 
Thus, we have 
Note that because up is positive, the initial vertical velocity is positive, as is the maximum height, but the 
acceleration resulting from gravity is negative. Note also that the maximum height depends only on the vertical 
component of the initial velocity, so that any projectile with a 67.6-m/s initial vertical component of velocity reaches 
a maximum height of 233 m (neglecting air resistance). The numbers in this example are reasonable for large 
fireworks displays, the shells of which do reach such heights before exploding. In practice, air resistance is not 
completely negligible, so the initial velocity would have to be somewhat larger than that given to reach the same 
height. 
4.3 • Projectile Motion

(b) As in many physics problems, there is more than one way to solve for the time the projectile reaches its highest 
point. In this case, the easiest method is to use 
 Because 
 at the apex, this equation reduces 
to simply 
or 
This time is also reasonable for large fireworks. If you are able to see the launch of fireworks, notice that several 
seconds pass before the shell explodes. Another way of finding the time is by using
 This is 
left for you as an exercise to complete. 
(c) Because air resistance is negligible, 
 and the horizontal velocity is constant, as discussed earlier. The 
horizontal displacement is the horizontal velocity multiplied by time as given by 
 where 
 is equal to 
zero. Thus, 
where 
 is the x-component of the velocity, which is given by 
Time t for both motions is the same, so x is 
Horizontal motion is a constant velocity in the absence of air resistance. The horizontal displacement found here 
could be useful in keeping the fireworks fragments from falling on spectators. When the shell explodes, air 
resistance has a major effect, and many fragments land directly below. 
(d) The horizontal and vertical components of the displacement were just calculated, so all that is needed here is to 
find the magnitude and direction of the displacement at the highest point: 
Note that the angle for the displacement vector is less than the initial angle of launch. To see why this is, review 
Figure 4.11, which shows the curvature of the trajectory toward the ground level. 
When solving Example 4.7(a), the expression we found for y is valid for any projectile motion when air resistance is 
negligible. Call the maximum height y = h. Then, 
This equation defines the maximum height of a projectile above its launch position and it depends only on the 
vertical component of the initial velocity. 
CHECK YOUR UNDERSTANDING 4.3 
A rock is thrown horizontally off a cliff 
 high with a velocity of 15.0 m/s. (a) Define the origin of the 
coordinate system. (b) Which equation describes the horizontal motion? (c) Which equations describe the vertical 
motion? (d) What is the rock’s velocity at the point of impact? 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

EXAMPLE 4.8 
Calculating Projectile Motion: Tennis Player 
A tennis player wins a match at Arthur Ashe stadium and hits a ball into the stands at 30 m/s and at an angle 
above the horizontal (Figure 4.14). On its way down, the ball is caught by a spectator 10 m above the point where 
the ball was hit. (a) Calculate the time it takes the tennis ball to reach the spectator. (b) What are the magnitude and 
direction of the ball’s velocity at impact? 
FIGURE 4.14 The trajectory of a tennis ball hit into the stands. 
Strategy 
Again, resolving this two-dimensional motion into two independent one-dimensional motions allows us to solve for 
the desired quantities. The time a projectile is in the air is governed by its vertical motion alone. Thus, we solve for t 
first. While the ball is rising and falling vertically, the horizontal motion continues at a constant velocity. This 
example asks for the final velocity. Thus, we recombine the vertical and horizontal results to obtain  at final time t, 
determined in the first part of the example. 
Solution 
(a) While the ball is in the air, it rises and then falls to a final position 10.0 m higher than its starting altitude. We can 
find the time for this by using Equation 4.22: 
If we take the initial position 
 to be zero, then the final position is y = 10 m. The initial vertical velocity is the 
vertical component of the initial velocity: 
Substituting into Equation 4.22 for y gives us 
Rearranging terms gives a quadratic equation in t: 
Use of the quadratic formula yields t = 3.79 s and t = 0.54 s. Since the ball is at a height of 10 m at two times during 
its trajectory—once on the way up and once on the way down—we take the longer solution for the time it takes the 
ball to reach the spectator: 
4.3 • Projectile Motion

The time for projectile motion is determined completely by the vertical motion. Thus, any projectile that has an 
initial vertical velocity of 21.2 m/s and lands 10.0 m above its starting altitude spends 3.79 s in the air. 
(b) We can find the final horizontal and vertical velocities 
 and 
 with the use of the result from (a). Then, we can 
combine them to find the magnitude of the total velocity vector  and the angle  it makes with the horizontal. Since 
 is constant, we can solve for it at any horizontal location. We choose the starting point because we know both the 
initial velocity and the initial angle. Therefore, 
The final vertical velocity is given by Equation 4.21: 
Since 
 was found in part (a) to be 21.2 m/s, we have 
The magnitude of the final velocity  is 
The direction 
 is found using the inverse tangent: 
Significance 
(a) As mentioned earlier, the time for projectile motion is determined completely by the vertical motion. Thus, any 
projectile that has an initial vertical velocity of 21.2 m/s and lands 10.0 m above its starting altitude spends 3.79 s in 
the air. (b) The negative angle means the velocity is 
 below the horizontal at the point of impact. This result is 
consistent with the fact that the ball is impacting at a point on the other side of the apex of the trajectory and 
therefore has a negative y component of the velocity. The magnitude of the velocity is less than the magnitude of the 
initial velocity we expect since it is impacting 10.0 m above the launch elevation. 
Time of Flight, Trajectory, and Range 
Of interest are the time of flight, trajectory, and range for a projectile launched on a flat horizontal surface and 
impacting on the same surface. In this case, kinematic equations give useful expressions for these quantities, which 
are derived in the following sections. 
Time of flight 
We can solve for the time of flight of a projectile that is both launched and impacts on a flat horizontal surface by 
performing some manipulations of the kinematic equations. We note the position and displacement in y must be 
zero at launch and at impact on an even surface. Thus, we set the displacement in y equal to zero and find 
Factoring, we have 
Solving for t gives us 
This is the time of flight for a projectile both launched and impacting on a flat horizontal surface. Equation 4.24 
4.24 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

does not apply when the projectile lands at a different elevation than it was launched, as we saw in Example 4.8 of 
the tennis player hitting the ball into the stands. The other solution, t = 0, corresponds to the time at launch. The 
time of flight is linearly proportional to the initial velocity in the y direction and inversely proportional to g. Thus, on 
the Moon, where gravity is one-sixth that of Earth, a projectile launched with the same velocity as on Earth would be 
airborne six times as long. 
Trajectory 
The trajectory of a projectile can be found by eliminating the time variable t from the kinematic equations for 
arbitrary t and solving for y(x). We take 
 so the projectile is launched from the origin. The kinematic 
equation for x gives 
Substituting the expression for t into the equation for the position 
 gives 
Rearranging terms, we have 
This trajectory equation is of the form 
 which is an equation of a parabola with coefficients 
Range 
From the trajectory equation we can also find the range, or the horizontal distance traveled by the projectile. 
Factoring Equation 4.25, we have 
The position y is zero for both the launch point and the impact point, since we are again considering only a flat 
horizontal surface. Setting y = 0 in this equation gives solutions x = 0, corresponding to the launch point, and 
corresponding to the impact point. Using the trigonometric identity 
 and setting x = R for range, 
we find 
Note particularly that Equation 4.26 is valid only for launch and impact on a horizontal surface. We see the range is 
directly proportional to the square of the initial speed 
 and 
, and it is inversely proportional to the 
acceleration of gravity. Thus, on the Moon, the range would be six times greater than on Earth for the same initial 
velocity. Furthermore, we see from the factor 
 that the range is maximum at 
 These results are shown in 
Figure 4.15. In (a) we see that the greater the initial velocity, the greater the range. In (b), we see that the range is 
maximum at 
 This is true only for conditions neglecting air resistance. If air resistance is considered, the 
maximum angle is somewhat smaller. It is interesting that the same range is found for two initial launch angles that 
sum to 
 The projectile launched with the smaller angle has a lower apex than the higher angle, but they both 
have the same range. 
4.25 
4.26 
4.3 • Projectile Motion

FIGURE 4.15 Trajectories of projectiles on level ground. (a) The greater the initial speed 
 the greater the range for a given initial angle. 
(b) The effect of initial angle 
 on the range of a projectile with a given initial speed. Note that the range is the same for initial angles of 
and 
 although the maximum heights of those paths are different. 
EXAMPLE 4.9 
Comparing Golf Shots 
A golfer encounters two different situations on different holes. On the second hole they are 120 m from the green 
and want to hit the ball 90 m and let it run onto the green. They angle the shot low to the ground at 
 to the 
horizontal to let the ball roll after impact. On the fourth hole they are 90 m from the green and want to let the ball 
drop with a minimum amount of rolling after impact. Here, they angle the shot at 
 to the horizontal to minimize 
rolling after impact. Both shots are hit and impacted on a level surface. 
(a) What is the initial speed of the ball at the second hole? 
(b) What is the initial speed of the ball at the fourth hole? 
(c) Write the trajectory equation for both cases. 
(d) Graph the trajectories. 
Strategy 
We see that the range equation has the initial speed and angle, so we can solve for the initial speed for both (a) and 
(b). When we have the initial speed, we can use this value to write the trajectory equation. 
Solution 
(a) 
(b) 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

(c) 
(d) Using a graphing utility, we can compare the two trajectories, which are shown in Figure 4.16. 
FIGURE 4.16 Two trajectories of a golf ball with a range of 90 m. The impact points of both are at the same level as the launch point. 
Significance 
The initial speed for the shot at 
 is greater than the initial speed of the shot at 
 Note from Figure 4.16 that if 
the two projectiles were launched at the same speed but at different angles, the projectiles would have the same 
range as long as the angles were less than 
 The launch angles in this example add to give a number greater than 
 Thus, the shot at 
 has to have a greater launch speed to reach 90 m, otherwise it would land at a shorter 
distance. 
CHECK YOUR UNDERSTANDING 4.4 
If the two golf shots in Example 4.9 were launched at the same speed, which shot would have the greatest range? 
When we speak of the range of a projectile on level ground, we assume R is very small compared with the 
circumference of Earth. If, however, the range is large, Earth curves away below the projectile and the acceleration 
resulting from gravity changes direction along the path. The range is larger than predicted by the range equation 
given earlier because the projectile has farther to fall than it would on level ground, as shown in Figure 4.17, which 
is based on a drawing in Newton’s Principia. If the initial speed is great enough, the projectile goes into orbit. Earth’s 
surface drops 5 m every 8000 m. In 1 s an object falls 5 m without air resistance. Thus, if an object is given a 
4.3 • Projectile Motion

horizontal velocity of 8000 m/s (or 18,000 mi/hr) near Earth’s surface, it will go into orbit around the planet because 
the surface continuously falls away from the object. This is roughly the speed of the Space Shuttle in a low Earth 
orbit when it was operational, or any satellite in a low Earth orbit. These and other aspects of orbital motion, such as 
Earth’s rotation, are covered in greater depth in Gravitation. 
FIGURE 4.17 Projectile to satellite. In each case shown here, a projectile is launched from a very high tower to avoid air resistance. With 
increasing initial speed, the range increases and becomes longer than it would be on level ground because Earth curves away beneath its 
path. With a speed of 8000 m/s, orbit is achieved. 
INTERACTIVE 
At PhET Explorations: Projectile Motion (https://openstax.org/l/21phetpromot), learn about projectile motion in 
terms of the launch angle and initial velocity. 
4.4 Uniform and Nonuniform Circular Motion 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Solve for the centripetal acceleration of an object moving on a circular path. 
• Use the equations of circular motion to find the position, velocity, and acceleration of a particle executing 
circular motion. 
• Explain the differences between centripetal acceleration and tangential acceleration resulting from 
nonuniform circular motion. 
• Evaluate centripetal and tangential acceleration in nonuniform circular motion, and find the total 
acceleration vector. 
Uniform circular motion is a specific type of motion in which an object travels in a circle with a constant speed. For 
example, any point on a propeller spinning at a constant rate is executing uniform circular motion. Other examples 
are the second, minute, and hour hands of a watch. It is remarkable that points on these rotating objects are 
actually accelerating, although the rotation rate is a constant. To see this, we must analyze the motion in terms of 
vectors. 
Centripetal Acceleration 
In one-dimensional kinematics, objects with a constant speed have zero acceleration. However, in two- and three-
dimensional kinematics, even if the speed is a constant, a particle can have acceleration if it moves along a curved 
trajectory such as a circle. In this case the velocity vector is changing, or 
 This is shown in Figure 4.18. As 
the particle moves counterclockwise in time 
 on the circular path, its position vector moves from 
 to 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

The velocity vector has constant magnitude and is tangent to the path as it changes from 
 to 
 changing 
its direction only. Since the velocity vector 
 is perpendicular to the position vector 
 the triangles formed by 
the position vectors and 
 and the velocity vectors and 
 are similar. Furthermore, since 
 and 
 the two triangles are isosceles. From these facts we can make the assertion 
 or 
FIGURE 4.18 (a) A particle is moving in a circle at a constant speed, with position and velocity vectors at times  and 
 (b) Velocity 
vectors forming a triangle. The two triangles in the figure are similar. The vector 
 points toward the center of the circle in the limit 
We can find the magnitude of the acceleration from 
The direction of the acceleration can also be found by noting that as 
 and therefore 
 approach zero, the vector 
 approaches a direction perpendicular to 
 In the limit 
 is perpendicular to 
 Since  is tangent to the 
circle, the acceleration 
 points toward the center of the circle. Summarizing, a particle moving in a circle at a 
constant speed has an acceleration with magnitude 
The direction of the acceleration vector is toward the center of the circle (Figure 4.19). This is a radial acceleration 
and is called the centripetal acceleration, which is why we give it the subscript c. The word centripetal comes from 
the Latin words centrum (meaning “center”) and petere (meaning “to seek”), and thus takes the meaning “center 
seeking.” 
4.27 
4.4 • Uniform and Nonuniform Circular Motion

FIGURE 4.19 The centripetal acceleration vector points toward the center of the circular path of motion and is an acceleration in the radial 
direction. The velocity vector is also shown and is tangent to the circle. 
Let’s investigate some examples that illustrate the relative magnitudes of the velocity, radius, and centripetal 
acceleration. 
EXAMPLE 4.10 
Creating an Acceleration of 1 g 
A jet is flying at 134.1 m/s along a straight line and makes a turn along a circular path level with the ground. What 
does the radius of the circle have to be to produce a centripetal acceleration of 1 g on the pilot and jet toward the 
center of the circular trajectory? 
Strategy 
Given the speed of the jet, we can solve for the radius of the circle in the expression for the centripetal acceleration. 
Solution 
Set the centripetal acceleration equal to the acceleration of gravity: 
Solving for the radius, we find 
Significance 
To create a greater acceleration than g on the pilot, the jet would either have to decrease the radius of its circular 
trajectory or increase its speed on its existing trajectory or both. 
CHECK YOUR UNDERSTANDING 4.5 
A flywheel has a radius of 20.0 cm. What is the speed of a point on the edge of the flywheel if it experiences a 
centripetal acceleration of 
Centripetal acceleration can have a wide range of values, depending on the speed and radius of curvature of the 
circular path. Typical centripetal accelerations are given in the following table. 
Object 
Centripetal Acceleration (m/s2 or factors of g) 
Earth around the Sun 
Moon around the Earth 
TABLE 4.1 Typical Centripetal Accelerations 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

Object 
Centripetal Acceleration (m/s2 or factors of g) 
Satellite in geosynchronous orbit 
0.233 
Outer edge of a CD when playing 
Jet in a barrel roll 
(2–3 g) 
Roller coaster 
(5 g) 
Electron orbiting a proton in a simple Bohr model of the atom 
TABLE 4.1 Typical Centripetal Accelerations 
Equations of Motion for Uniform Circular Motion 
A particle executing circular motion can be described by its position vector 
 Figure 4.20 shows a particle 
executing circular motion in a counterclockwise direction. As the particle moves on the circle, its position vector 
sweeps out the angle  with the x-axis. Vector 
 making an angle  with the x-axis is shown with its components 
along the x- and y-axes. The magnitude of the position vector is 
 and is also the radius of the circle, so that 
in terms of its components, 
Here,  is a constant called the angular frequency of the particle. The angular frequency has units of radians (rad) 
per second and is simply the number of radians of angular measure through which the particle passes per second. 
The angle  that the position vector has at any particular time is 
. 
If T is the period of motion, or the time to complete one revolution (
 rad), then 
FIGURE 4.20 The position vector for a particle in circular motion with its components along the x- and y-axes. The particle moves 
counterclockwise. Angle  is the angular frequency  in radians per second multiplied by t. 
Velocity and acceleration can be obtained from the position function by differentiation: 
It can be shown from Figure 4.20 that the velocity vector is tangential to the circle at the location of the particle, 
with magnitude 
 Similarly, the acceleration vector is found by differentiating the velocity: 
4.28 
4.29 
4.4 • Uniform and Nonuniform Circular Motion

From this equation we see that the acceleration vector has magnitude 
 and is directed opposite the position 
vector, toward the origin, because 
EXAMPLE 4.11 
Circular Motion of a Proton 
A proton has speed 
 and is moving in a circle in the xy plane of radius r = 0.175 m. What is its position 
in the xy plane at time 
 At t = 0, the position of the proton is 
 and it circles 
counterclockwise. Sketch the trajectory. 
Solution 
According to Equation 3.5, 
Since the period T is the time it takes an object to go once around a circle, and the distance around a circle is 2πr, we 
have: 
From the given data, the proton has period and angular frequency: 
The position of the particle at 
 with A = 0.175 m is 
From this result we see that the proton is located slightly below the x-axis. This is shown in Figure 4.21. 
4.30 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

FIGURE 4.21 Position vector of the proton at 
 The trajectory of the proton is shown. The angle through which 
the proton travels along the circle is 5.712 rad, which a little less than one complete revolution. 
Significance 
We picked the initial position of the particle to be on the x-axis. This was completely arbitrary. If a different starting 
position were given, we would have a different final position at t = 200 ns. 
Nonuniform Circular Motion 
Circular motion does not have to be at a constant speed. A particle can travel in a circle and speed up or slow down, 
showing an acceleration in the direction of the motion. 
In uniform circular motion, the particle executing circular motion has a constant speed and the circle is at a fixed 
radius. If the speed of the particle is changing as well, then we introduce an additional acceleration in the direction 
tangential to the circle. Such accelerations occur at a point on a top that is changing its spin rate, or any accelerating 
rotor. In Displacement and Velocity Vectors we showed that centripetal acceleration is the time rate of change of the 
direction of the velocity vector. If the speed of the particle is changing, then it has a tangential acceleration that is 
the time rate of change of the magnitude of the velocity: 
The direction of tangential acceleration is tangent to the circle whereas the direction of centripetal acceleration is 
radially inward toward the center of the circle. Thus, a particle in circular motion with a tangential acceleration has a 
total acceleration that is the vector sum of the centripetal and tangential accelerations: 
The acceleration vectors are shown in Figure 4.22. Note that the two acceleration vectors 
 and 
 are 
perpendicular to each other, with 
 in the radial direction and 
 in the tangential direction. The total acceleration 
 points at an angle between 
 and 
4.31 
4.32 
4.4 • Uniform and Nonuniform Circular Motion

FIGURE 4.22 The centripetal acceleration points toward the center of the circle. The tangential acceleration is tangential to the circle at the 
particle’s position. The total acceleration is the vector sum of the tangential and centripetal accelerations, which are perpendicular. 
EXAMPLE 4.12 
Total Acceleration during Circular Motion 
A particle moves in a circle of radius r = 2.0 m. During the time interval from t = 1.5 s to t = 4.0 s its speed varies with 
time according to 
What is the total acceleration of the particle at t = 2.0 s? 
Strategy 
We are given the speed of the particle and the radius of the circle, so we can calculate centripetal acceleration 
easily. The direction of the centripetal acceleration is toward the center of the circle. We find the magnitude of the 
tangential acceleration by taking the derivative with respect to time of 
 using Equation 4.31 and evaluating it at 
t = 2.0 s. We use this and the magnitude of the centripetal acceleration to find the total acceleration. 
Solution 
Centripetal acceleration is 
directed toward the center of the circle. Tangential acceleration is 
Total acceleration is 
and 
 from the tangent to the circle. See Figure 4.23. 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

FIGURE 4.23 The tangential and centripetal acceleration vectors. The net acceleration  is the vector sum of the two accelerations. 
Significance 
The directions of centripetal and tangential accelerations can be described more conveniently in terms of a polar 
coordinate system, with unit vectors in the radial and tangential directions. This coordinate system, which is used for 
motion along curved paths, is discussed in detail later in the book. 
4.5 Relative Motion in One and Two Dimensions 
LEARNING OBJECTIVES 
By the end of this section, you will be able to: 
• Explain the concept of reference frames. 
• Write the position and velocity vector equations for relative motion. 
• Draw the position and velocity vectors for relative motion. 
• Analyze one-dimensional and two-dimensional relative motion problems using the position and velocity 
vector equations. 
Motion does not happen in isolation. If you’re riding in a train moving at 10 m/s east, this velocity is measured 
relative to the ground on which you’re traveling. However, if another train passes you at 15 m/s east, your velocity 
relative to this other train is different from your velocity relative to the ground. Your velocity relative to the other 
train is 5 m/s west. To explore this idea further, we first need to establish some terminology. 
Reference Frames 
To discuss relative motion in one or more dimensions, we first introduce the concept of reference frames. When we 
say an object has a certain velocity, we must state it has a velocity with respect to a given reference frame. In most 
examples we have examined so far, this reference frame has been Earth. If you say a person is sitting in a train 
moving at 10 m/s east, then you imply the person on the train is moving relative to the surface of Earth at this 
velocity, and Earth is the reference frame. We can expand our view of the motion of the person on the train and say 
Earth is spinning in its orbit around the Sun, in which case the motion becomes more complicated. In this case, the 
solar system is the reference frame. In summary, all discussion of relative motion must define the reference frames 
involved. We now develop a method to refer to reference frames in relative motion. This method makes an 
approximation that breaks down near the speed of light, where the more accurate methods or special relativity are 
needed, but is extremely accurate for everyday speeds (Relativity (http://openstax.org/books/university-physics-
volume-3/pages/5-introduction)). 
Relative Motion in One Dimension 
We introduce relative motion in one dimension first, because the velocity vectors simplify to having only two 
possible directions. Take the example of the person sitting in a train moving east. If we choose east as the positive 
direction and Earth as the reference frame, then we can write the velocity of the train with respect to the Earth as 
 east, where the subscripts TE refer to train and Earth. Let’s now say the person gets up out of her 
seat and walks toward the back of the train at 2 m/s. This tells us she has a velocity relative to the reference frame 
4.5 • Relative Motion in One and Two Dimensions

of the train. Since the person is walking west, in the negative direction, we write her velocity with respect to the train 
as 
 We can add the two velocity vectors to find the velocity of the person with respect to Earth. This 
relative velocity is written as 
Note the ordering of the subscripts for the various reference frames in Equation 4.33. The subscripts for the 
coupling reference frame, which is the train, appear consecutively in the right-hand side of the equation. Figure 4.24 
shows the correct order of subscripts when forming the vector equation. 
FIGURE 4.24 When constructing the vector equation, the subscripts for the coupling reference frame appear consecutively on the inside. 
The subscripts on the left-hand side of the equation are the same as the two outside subscripts on the right-hand side of the equation. 
Adding the vectors, we find 
 so the person is moving 8 m/s east with respect to Earth. Graphically, 
this is shown in Figure 4.25. 
FIGURE 4.25 Velocity vectors of the train with respect to Earth, person with respect to the train, and person with respect to Earth. 
Relative Velocity in Two Dimensions 
We can now apply these concepts to describing motion in two dimensions. Consider a particle P and reference 
frames S and 
 as shown in Figure 4.26. The position of the origin of 
 as measured in S is 
 the position of P 
as measured in 
 is 
 and the position of P as measured in S is 
FIGURE 4.26 The positions of particle P relative to frames S and 
 are 
 and 
 respectively. 
From Figure 4.26 we see that 
The relative velocities are the time derivatives of the position vectors. Therefore, 
The velocity of a particle relative to S is equal to its velocity relative to 
 plus the velocity of 
 relative to S. 
4.33 
4.34 
4.35 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

We can extend Equation 4.35 to any number of reference frames. For particle P with velocities 
in frames A, B, and C, 
We can also see how the accelerations are related as observed in two reference frames by differentiating Equation 
4.35: 
We see that if the velocity of 
 relative to S is a constant, then 
 and 
This says the acceleration of a particle is the same as measured by two observers moving at a constant velocity 
relative to each other. 
EXAMPLE 4.13 
Motion of a Car Relative to a Truck 
A truck is traveling south at a speed of 70 km/h toward an intersection. A car is traveling east toward the 
intersection at a speed of 80 km/h (Figure 4.27). What is the velocity of the car relative to the truck? 
FIGURE 4.27 A car travels east toward an intersection while a truck travels south toward the same intersection. 
Strategy 
First, we must establish the reference frame common to both vehicles, which is Earth. Then, we write the velocities 
of each with respect to the reference frame of Earth, which enables us to form a vector equation that links the car, 
the truck, and Earth to solve for the velocity of the car with respect to the truck. 
Solution 
The velocity of the car with respect to Earth is 
 The velocity of the truck with respect to Earth is 
 Using the velocity addition rule, the relative motion equation we are seeking is 
4.36 
4.37 
4.38 
4.5 • Relative Motion in One and Two Dimensions

Here, 
 is the velocity of the car with respect to the truck, and Earth is the connecting reference frame. Since we 
have the velocity of the truck with respect to Earth, the negative of this vector is the velocity of Earth with respect to 
the truck: 
 The vector diagram of this equation is shown in Figure 4.28. 
FIGURE 4.28 Vector diagram of the vector equation 
. 
We can now solve for the velocity of the car with respect to the truck: 
and 
Significance 
Drawing a vector diagram showing the velocity vectors can help in understanding the relative velocity of the two 
objects. 
CHECK YOUR UNDERSTANDING 4.6 
A boat heads due north, moving at 4.5 m/s relative to the water of a river that is running east at 3.0 m/s. What is the 
velocity of the boat with respect to Earth? 
EXAMPLE 4.14 
Flying a Plane in a Wind 
A pilot must fly a plane due north to reach their destination. The plane can fly at 300 km/h in still air. A wind is 
blowing out of the northeast at 90 km/h. (a) In what direction must the pilot head the plane to fly due north? (b) 
What is the speed of the plane relative to the ground? 
Strategy 
The pilot must point the plane somewhat east of north to compensate for the wind velocity. We need to construct a 
vector equation that contains the velocity of the plane with respect to the ground, the velocity of the plane with 
respect to the air, and the velocity of the air with respect to the ground. Since these last two quantities are known, 
we can solve for the velocity of the plane with respect to the ground. We can graph the vectors and use this diagram 
to evaluate the magnitude of the plane’s velocity with respect to the ground. The diagram will also tell us the angle 
the plane’s velocity makes with north with respect to the air, which is the direction the pilot must head the plane. 
4 • Motion in Two and Three Dimensions
Access for free at openstax.org

Solution 
The vector equation is 
 where P = plane, A = air, and G = ground. From the geometry in Figure 
4.29, we can solve easily for the magnitude of the velocity of the plane with respect to the ground and the angle of 
the plane’s heading, 
FIGURE 4.29 Vector diagram for Equation 4.34 showing the vectors 
Known quantities: 
(a) In the x direction we have the following: 
• 
• 
• 
 east of north 
(b) In the y direction we have the following: 
• 
• 
• 
4.5 • Relative Motion in One and Two Dimensions

Chapter Review 
Key Terms 
acceleration vector instantaneous acceleration 
found by taking the derivative of the velocity 
function with respect to time in unit vector notation 
angular frequency 
 rate of change of an angle with 
which an object that is moving on a circular path 
centripetal acceleration component of acceleration 
of an object moving in a circle that is directed 
radially inward toward the center of the circle 
displacement vector vector from the initial position 
to a final position on a trajectory of a particle 
position vector vector from the origin of a chosen 
coordinate system to the position of a particle in 
two- or three-dimensional space 
projectile motion motion of an object subject only to 
the acceleration of gravity 
range maximum horizontal distance a projectile 
travels 
reference frame coordinate system in which the 
position, velocity, and acceleration of an object at 
rest or moving is measured 
relative velocity velocity of an object as observed 
from a particular reference frame, or the velocity of 
one reference frame with respect to another 
reference frame 
tangential acceleration magnitude of which is the 
time rate of change of speed. Its direction is tangent 
to the circle. 
time of flight elapsed time a projectile is in the air 
total acceleration vector sum of centripetal and 
tangential accelerations 
trajectory path of a projectile through the air 
velocity vector vector that gives the instantaneous 
speed and direction of a particle; tangent to the 
trajectory 
Key Equations 
Position vector 
Displacement vector 
Velocity vector 
Velocity in terms of components 
Velocity components 
Average velocity 
Instantaneous acceleration 
Instantaneous acceleration, component form 
Instantaneous acceleration as second 
derivatives of position 
Time of flight 
Trajectory 
Range 
Centripetal acceleration 
Position vector, uniform circular motion 
Velocity vector, uniform circular motion 
Acceleration vector, uniform circular motion 
Tangential acceleration 
Total acceleration 
182     4 • Chapter Review
Access for free at openstax.org

Position vector in frame 
S is the position 
vector in frame 
 plus the vector from the 
origin of S to the origin of 
Relative velocity equation connecting two 
reference frames 
Relative velocity equation connecting more 
than two reference frames 
Relative acceleration equation 
Summary 
4.1 Displacement and Velocity Vectors 
• The position function 
 gives the position as a 
function of time of a particle moving in two or 
three dimensions. Graphically, it is a vector from 
the origin of a chosen coordinate system to the 
point where the particle is located at a specific 
time. 
• The displacement vector 
 gives the shortest 
distance between any two points on the 
trajectory of a particle in two or three 
dimensions. 
• Instantaneous velocity gives the speed and 
direction of a particle at a specific time on its 
trajectory in two or three dimensions, and is a 
vector in two and three dimensions. 
• The velocity vector is tangent to the trajectory of 
the particle. 
• Displacement 
 can be written as a vector sum 
of the one-dimensional displacements 
 along the x, y, and z directions. 
• Velocity 
 can be written as a vector sum of 
the one-dimensional velocities 
along the x, y, and z directions. 
• Motion in any given direction is independent of 
motion in a perpendicular direction. 
4.2 Acceleration Vector 
• In two and three dimensions, the acceleration 
vector can have an arbitrary direction and does 
not necessarily point along a given component of 
the velocity. 
• The instantaneous acceleration is produced by a 
change in velocity taken over a very short 
(infinitesimal) time period. Instantaneous 
acceleration is a vector in two or three 
dimensions. It is found by taking the derivative of 
the velocity function with respect to time. 
• In three dimensions, acceleration 
 can be 
written as a vector sum of the one-dimensional 
accelerations 
 along the x-, 
y-, and z-axes. 
• The kinematic equations for constant 
acceleration can be written as the vector sum of 
the constant acceleration equations in the x, y, 
and z directions. 
4.3 Projectile Motion 
• Projectile motion is the motion of an object 
subject only to the acceleration of gravity, where 
the acceleration is constant, as near the surface 
of Earth. 
• To solve projectile motion problems, we analyze 
the motion of the projectile in the horizontal and 
vertical directions using the one-dimensional 
kinematic equations for x and y. 
• The time of flight of a projectile launched with 
initial vertical velocity 
 on an even surface is 
given by 
This equation is valid only when the projectile 
lands at the same elevation from which it was 
launched. 
• The maximum horizontal distance traveled by a 
projectile is called the range. Again, the equation 
for range is valid only when the projectile lands at 
the same elevation from which it was launched. 
4.4 Uniform and Nonuniform Circular Motion 
• Uniform circular motion is motion in a circle at 
constant speed. 
• Centripetal acceleration 
 is the acceleration a 
particle must have to follow a circular path. 
Centripetal acceleration always points toward 
the center of rotation and has magnitude 
• Nonuniform circular motion occurs when there is 
tangential acceleration of an object executing 
circular motion such that the speed of the object 
is changing. This acceleration is called tangential 
acceleration 
 The magnitude of tangential 
acceleration is the time rate of change of the 
4 • Chapter Review     183

magnitude of the velocity. The tangential 
acceleration vector is tangential to the circle, 
whereas the centripetal acceleration vector 
points radially inward toward the center of the 
circle. The total acceleration is the vector sum of 
tangential and centripetal accelerations. 
• An object executing uniform circular motion can 
be described with equations of motion. The 
position vector of the object is 
 where A is the 
magnitude 
 which is also the radius of the 
circle, and  is the angular frequency. 
4.5 Relative Motion in One and Two Dimensions 
• When analyzing motion of an object, the 
reference frame in terms of position, velocity, 
and acceleration needs to be specified. 
• Relative velocity is the velocity of an object as 
observed from a particular reference frame, and 
it varies with the choice of reference frame. 
• If S and 
 are two reference frames moving 
relative to each other at a constant velocity, then 
the velocity of an object relative to S is equal to 
its velocity relative to 
 plus the velocity of 
relative to S. 
• If two reference frames are moving relative to 
each other at a constant velocity, then the 
accelerations of an object as observed in both 
reference frames are equal. 
Conceptual Questions 
4.1 Displacement and Velocity Vectors 
1 . What form does the trajectory of a particle have 
if the distance from any point A to point B is 
equal to the magnitude of the displacement 
from A to B? 
2 . Give an example of a trajectory in two or three 
dimensions caused by independent 
perpendicular motions. 
3 . If the instantaneous velocity is zero, what can be 
said about the slope of the position function? 
4.2 Acceleration Vector 
4 . If the position function of a particle is a linear 
function of time, what can be said about its 
acceleration? 
5 . If an object has a constant x-component of the 
velocity and suddenly experiences an 
acceleration in the y direction, does the 
x-component of its velocity change? 
6 . If an object has a constant x-component of 
velocity and suddenly experiences an 
acceleration at an angle of 
 in the x direction, 
does the x-component of velocity change? 
4.3 Projectile Motion 
7 . Answer the following questions for projectile 
motion on level ground assuming negligible air 
resistance, with the initial angle being neither 
nor 
 (a) Is the velocity ever zero? (b) When 
is the velocity a minimum? A maximum? (c) Can 
the velocity ever be the same as the initial 
velocity at a time other than at t = 0? (d) Can the 
speed ever be the same as the initial speed at a 
time other than at t = 0? 
8 . Answer the following questions for projectile 
motion on level ground assuming negligible air 
resistance, with the initial angle being neither 
nor 
 (a) Is the acceleration ever zero? (b) Is 
the vector  ever parallel or antiparallel to the 
vector ? (c) Is the vector v ever perpendicular 
to the vector a? If so, where is this located? 
9 . A dime is placed at the edge of a table so it 
hangs over slightly. A quarter is slid horizontally 
on the table surface perpendicular to the edge 
and hits the dime head on. Which coin hits the 
ground first? 
4.4 Uniform and Nonuniform Circular Motion 
10 . Can centripetal acceleration change the speed 
of a particle undergoing circular motion? 
11 . Can tangential acceleration change the speed of 
a particle undergoing circular motion? 
4.5 Relative Motion in One and Two Dimensions 
12 . What frame or frames of reference do you use 
instinctively when driving a car? When flying in a 
commercial jet? 
13 . A basketball player dribbling down the court 
usually keeps his eyes fixed on the players 
around him. He is moving fast. Why doesn’t he 
need to keep his eyes on the ball? 
14 . If someone is riding in the back of a pickup truck 
and throws a softball straight backward, is it 
possible for the ball to fall straight down as 
viewed by a person standing at the side of the 
road? Under what condition would this occur? 
184     4 • Chapter Review
Access for free at openstax.org

How would the motion of the ball appear to the 
person who threw it? 
15 . The hat of a jogger running at constant velocity 
falls off the back of his head. Draw a sketch 
showing the path of the hat in the jogger’s frame 
of reference. Draw its path as viewed by a 
stationary observer. Neglect air resistance. 
16 . A clod of dirt falls from the bed of a moving 
truck. It strikes the ground directly below the 
end of the truck. (a) What is the direction of its 
velocity relative to the truck just before it hits? 
(b) Is this the same as the direction of its 
velocity relative to ground just before it hits? 
Explain your answers. 
Problems 
4.1 Displacement and Velocity Vectors 
17 . The coordinates of a particle in a rectangular 
coordinate system are (1.0, –4.0, 6.0). What is 
the position vector of the particle? 
18 . The position of a particle changes from 
​
 to 
 What is the particle’s 
displacement? 
19 . The 18th hole at Pebble Beach Golf Course is a 
dogleg to the left of length 496.0 m. The fairway 
off the tee is taken to be the x direction. A golfer 
hits his tee shot a distance of 300.0 m, 
corresponding to a displacement 
 and hits his second shot 189.0 
m with a displacement 
 What is the final 
displacement of the golf ball from where it 
started? 
20 . A bird flies straight northeast a distance of 95.0 
km for 3.0 h. With the x-axis due east and the 
y-axis due north, what is the displacement in 
unit vector notation for the bird? What is the 
average velocity for the trip? 
21 . A cyclist rides 5.0 km due east, then 10.0 km 
 west of north. From this point she rides 8.0 
km due west. What is the final displacement 
from where the cyclist started? 
22 . New York Rangers defenseman Daniel Girardi 
stands at the goal and passes a hockey puck 20 
m and 
 from straight down the ice to left wing 
Chris Kreider waiting at the blue line. Kreider 
waits for Girardi to reach the blue line and 
passes the puck directly across the ice to him 10 
m away. What is the final displacement of the 
puck? See the following figure. 
23 . The position of a particle is 
 (a) What is the 
velocity of the particle at 0 s and at 
 s? (b) 
What is the average velocity between 0 s and 
s? 
24 . Clay Matthews, a linebacker for the Green Bay 
Packers, can reach a speed of 10.0 m/s. At the 
start of a play, Matthews runs downfield at 
with respect to the 50-yard line and covers 8.0 
m in 1 s. He then runs straight down the field at 
 with respect to the 50-yard line for 12 m, 
with an elapsed time of 1.2 s. (a) What is 
Matthews’ final displacement from the start of 
the play? (b) What is his average velocity? 
25 . The F-35B Lighting II is a short-takeoff and 
vertical landing fighter jet. If it does a vertical 
takeoff to 20.00-m height above the ground and 
then follows a flight path angled at 
 with 
respect to the ground for 20.00 km, what is the 
final displacement? 
4.2 Acceleration Vector 
26 . The position of a particle is 
 (a) Determine 
its velocity and acceleration as functions of time. 
(b) What are its velocity and acceleration at time 
t = 0? 
27 . A particle’s acceleration is 
 At 
4 • Chapter Review     185

t = 0, its position and velocity are zero. (a) What 
are the particle’s position and velocity as 
functions of time? (b) Find the equation of the 
path of the particle. Draw the x- and y-axes and 
sketch the trajectory of the particle. 
28 . A boat leaves the dock at t = 0 and heads out 
into a lake with an acceleration of 
 A 
strong wind is pushing the boat, giving it an 
additional velocity of 
 (a) 
What is the velocity of the boat at t = 10 s? (b) 
What is the position of the boat at t = 10s? Draw 
a sketch of the boat’s trajectory and position at t 
= 10 s, showing the x- and y-axes. 
29 . The position of a particle for t > 0 is given by 
 (a) What 
is the velocity as a function of time? (b) What is 
the acceleration as a function of time? (c) What 
is the particle’s velocity at t = 2.0 s? (d) What is 
its speed at t = 1.0 s and t = 3.0 s? (e) What is 
the average velocity between t = 1.0 s and t = 
2.0 s? 
30 . The acceleration of a particle is a constant. At t = 
0 the velocity of the particle is 
At t = 4 s the velocity is 
 (a) What is the 
particle’s acceleration? (b) How do the position 
and velocity vary with time? Assume the particle 
is initially at the origin. 
31 . A particle has a position function 
 where the 
arguments of the cosine and sine functions are 
in radians. (a) What is the velocity vector? (b) 
What is the acceleration vector? 
32 . A Lockheed Martin F-35 II Lighting jet takes off 
from an aircraft carrier with a runway length of 
90 m and a takeoff speed 70 m/s at the end of 
the runway. Jets are catapulted into airspace 
from the deck of an aircraft carrier with two 
sources of propulsion: the jet propulsion and the 
catapult. At the point of leaving the deck of the 
aircraft carrier, the F-35’s acceleration 
decreases to a constant acceleration of 
at 
 with respect to the horizontal. (a) What is 
the initial acceleration of the F-35 on the deck of 
the aircraft carrier to make it airborne? (b) Write 
the position and velocity of the F-35 in unit 
vector notation from the point it leaves the deck 
of the aircraft carrier. (c) At what altitude is the 
fighter 5.0 s after it leaves the deck of the 
aircraft carrier? (d) What is its velocity and speed 
at this time? (e) How far has it traveled 
horizontally? 
4.3 Projectile Motion 
33 . A bullet is shot horizontally from shoulder height 
(1.5 m) with an initial speed 200 m/s. (a) How 
much time elapses before the bullet hits the 
ground? (b) How far does the bullet travel 
horizontally? 
34 . A marble rolls off a tabletop 1.0 m high and hits 
the floor at a point 3.0 m away from the table’s 
edge in the horizontal direction. (a) How long is 
the marble in the air? (b) What is the speed of 
the marble when it leaves the table’s edge? (c) 
What is its speed when it hits the floor? 
35 . A dart is thrown horizontally at a speed of 10 m/s at 
the bull’s-eye of a dartboard 2.4 m away, as in the 
following figure. (a) How far below the intended 
target does the dart hit? (b) What does your answer 
tell you about how proficient dart players throw their 
darts? 
36 . An airplane flying horizontally with a speed of 500 
km/h at a height of 800 m drops a crate of supplies 
(see the following figure). If the parachute fails to 
open, how far in front of the release point does the 
crate hit the ground? 
186     4 • Chapter Review
Access for free at openstax.org

37 . Suppose the airplane in the preceding problem 
fires a projectile horizontally in its direction of 
motion at a speed of 300 m/s relative to the 
plane. (a) How far in front of the release point 
does the projectile hit the ground? (b) What is its 
speed when it hits the ground? 
38 . A fastball pitcher can throw a baseball at a 
speed of 40 m/s (90 mi/h). (a) Assuming the 
pitcher can release the ball 16.7 m from home 
plate so the ball is moving horizontally, how long 
does it take the ball to reach home plate? (b) 
How far does the ball drop between the pitcher’s 
hand and home plate? 
39 . A projectile is launched at an angle of 
 and 
lands 20 s later at the same height as it was 
launched. (a) What is the initial speed of the 
projectile? (b) What is the maximum altitude? (c) 
What is the range? (d) Calculate the 
displacement from the point of launch to the 
position on its trajectory at 15 s. 
40 . A basketball player shoots toward a basket 6.1 
m away and 3.0 m above the floor. If the ball is 
released 1.8 m above the floor at an angle of 
above the horizontal, what must the initial speed 
be if it were to go through the basket? 
41 . At a particular instant, a hot air balloon is 100 m 
in the air and descending at a constant speed of 
2.0 m/s. At this exact instant, a girl throws a ball 
horizontally, relative to herself, with an initial 
speed of 20 m/s. When she lands, where will she 
find the ball? Ignore air resistance. 
42 . A man on a motorcycle traveling at a uniform 
speed of 10 m/s throws an empty can straight 
upward relative to himself with an initial speed 
of 3.0 m/s. Find the equation of the trajectory as 
seen by a police officer on the side of the road. 
Assume the initial position of the can is the point 
where it is thrown. Ignore air resistance. 
43 . An athlete can jump a distance of 8.0 m in the 
broad jump. What is the maximum distance the 
athlete can jump on the Moon, where the 
gravitational acceleration is one-sixth that of 
Earth? 
44 . The maximum horizontal distance a boy can 
throw a ball is 50 m. Assume he can throw with 
the same initial speed at all angles. How high 
does he throw the ball when he throws it straight 
upward? 
45 . A rock is thrown off a cliff at an angle of 
 with 
respect to the horizontal. The cliff is 100 m high. 
The initial speed of the rock is 30 m/s. (a) How 
high above the edge of the cliff does the rock 
rise? (b) How far has it moved horizontally when 
it is at maximum altitude? (c) How long after the 
release does it hit the ground? (d) What is the 
range of the rock? (e) What are the horizontal 
and vertical positions of the rock relative to the 
edge of the cliff at t = 2.0 s, t = 4.0 s, and t = 6.0 
s? 
46 . Trying to escape his pursuers, a secret agent skis off 
a slope inclined at 
 below the horizontal at 60 
km/h. To survive and land on the snow 100 m below, 
he must clear a gorge 60 m wide. Does he make it? 
Ignore air resistance. 
47 . A golfer on a fairway is 70 m away from the 
green, which sits below the level of the fairway 
by 20 m. If the golfer hits the ball at an angle of 
 with an initial speed of 20 m/s, how close to 
the green does she come? 
48 . A projectile is shot at a hill, the base of which is 300 
m away. The projectile is shot at 
 above the 
horizontal with an initial speed of 75 m/s. The hill 
can be approximated by a plane sloped at 
 to the 
4 • Chapter Review     187

horizontal. Relative to the coordinate system shown 
in the following figure, the equation of this straight 
line is 
 Where on the hill does 
the projectile land? 
49 . An astronaut on Mars kicks a soccer ball at an 
angle of 
 with an initial velocity of 15 m/s. If 
the acceleration of gravity on Mars is 
, 
(a) what is the range of the soccer kick on a flat 
surface? (b) What would be the range of the 
same kick on the Moon, where gravity is one-
sixth that of Earth? 
50 . Mike Powell holds the record for the long jump 
of 8.95 m, established in 1991. If he left the 
ground at an angle of 
 what was his initial 
speed? 
51 . MIT’s robot cheetah can jump over obstacles 46 
cm high and has speed of 12.0 km/h. (a) If the 
robot launches itself at an angle of 
 at this 
speed, what is its maximum height? (b) What 
would the launch angle have to be to reach a 
height of 46 cm? 
52 . Mt. Asama, Japan, is an active volcano. In 2009, 
an eruption threw solid volcanic rocks that 
landed 1 km horizontally from the crater. If the 
volcanic rocks were launched at an angle of 
with respect to the horizontal and landed 900 m 
below the crater, (a) what would be their initial 
velocity and (b) what is their time of flight? 
53 . Drew Brees of the New Orleans Saints can throw 
a football 23.0 m/s (50 mph). If he angles the 
throw at 
 from the horizontal, what distance 
does it go if it is to be caught at the same 
elevation as it was thrown? 
54 . The Lunar Roving Vehicle used in NASA’s late 
Apollo missions reached an unofficial lunar land 
speed of 
 by astronaut Eugene Cernan. If 
the rover was moving at this speed on a flat 
lunar surface and hit a small bump that 
projected it off the surface at an angle of 
how long would it be “airborne” on the Moon? 
55 . A soccer goal is 2.44 m high. A player kicks the 
ball at a distance 10 m from the goal at an angle 
of 
 The ball hits the crossbar at the top of 
the goal. What is the initial speed of the soccer 
ball? 
56 . Olympus Mons on Mars is the largest volcano in 
the solar system, at a height of 25 km and with a 
radius of 312 km. If you are standing on the 
summit, with what initial velocity would you 
have to fire a projectile from a cannon 
horizontally to clear the volcano and land on the 
surface of Mars? Note that Mars has an 
acceleration of gravity of 
57 . In 1999, Robbie Knievel was the first to jump the 
Grand Canyon on a motorcycle. At a narrow part 
of the canyon (69.0 m wide) and traveling 35.8 
m/s off the takeoff ramp, he reached the other 
side. What was his launch angle? 
58 . You throw a baseball at an initial speed of 15.0 
m/s at an angle of 
 with respect to the 
horizontal. What would the ball’s initial speed 
have to be at 
 on a planet that has twice the 
acceleration of gravity as Earth to achieve the 
same range? Consider launch and impact on a 
horizontal surface. 
59 . Aaron Rodgers throws a football at 20.0 m/s to 
his wide receiver, who is running straight down 
the field at 9.4 m/s. If Aaron throws the football 
when the wide receiver is 10.0 m in front of him, 
(a) at what angle does Aaron have to launch the 
ball so the ball will be at the same height as the 
receiver when the receiver makes it to 20.0 m in 
front of Aaron? (b) Will the receiver be able to 
catch the ball? 
4.4 Uniform and Nonuniform Circular Motion 
60 . A flywheel is rotating at 30 rev/s. What is the 
total angle, in radians, through which a point on 
the flywheel rotates in 40 s? 
61 . A particle travels in a circle of radius 10 m at a 
constant speed of 20 m/s. What is the 
magnitude of the acceleration? 
62 . Cam Newton of the Carolina Panthers throws a 
perfect football spiral at 8.0 rev/s. The radius of 
a pro football is 8.5 cm at the middle of the short 
side. What is the centripetal acceleration of the 
laces on the football? 
63 . A fairground ride spins its occupants inside a 
flying saucer-shaped container. If the horizontal 
circular path the riders follow has an 8.00-m 
radius, at how many revolutions per minute are 
188     4 • Chapter Review
Access for free at openstax.org

the riders subjected to a centripetal acceleration 
equal to that of gravity? 
64 . A runner taking part in the 200-m dash must run 
around the end of a track that has a circular arc 
with a radius of curvature of 30.0 m. The runner 
starts the race at a constant speed. If she 
completes the 200-m dash in 23.2 s and runs at 
constant speed throughout the race, what is her 
centripetal acceleration as she runs the curved 
portion of the track? 
65 . What is the acceleration of Venus toward the 
Sun, assuming a circular orbit? 
66 . An experimental jet rocket travels around Earth 
along its equator just above its surface. At what 
speed must the jet travel if the magnitude of its 
acceleration is g? 
67 . A fan is rotating at a constant 360.0 rev/min. 
What is the magnitude of the acceleration of a 
point on one of its blades 10.0 cm from the axis 
of rotation? 
68 . A point located on the second hand of a large 
clock has a radial acceleration of 
 How 
far is the point from the axis of rotation of the 
second hand? 
4.5 Relative Motion in One and Two Dimensions 
69 . The coordinate axes of the reference frame 
remain parallel to those of , as 
 moves away 
from  at a constant velocity 
 (a) If at time t 
= 0 the origins coincide, what is the position of 
the origin 
 in the S frame as a function of 
time? (b) How is particle position for 
 and 
 as measured in S and 
 respectively, 
related? (c) What is the relationship between 
particle velocities 
 (d) How are 
accelerations 
 related? 
70 . The coordinate axes of the reference frame 
remain parallel to those of S, as 
 moves away 
from S at a constant velocity 
. (a) If at time 
t = 0 the origins coincide, what is the position of 
origin 
 in the S frame as a function of time? (b) 
How is particle position for 
 and 
, as 
measured in S and 
 respectively, related? (c) 
What is the relationship between particle 
velocities 
 (d) How are 
accelerations 
 related? 
71 . The velocity of a particle in reference frame A is 
 The velocity of reference 
frame A with respect to reference frame B is 
 and the velocity of reference frame B 
with respect to C is 
 What is the velocity 
of the particle in reference frame C? 
72 . Raindrops fall vertically at 4.5 m/s relative to the 
earth. What does an observer in a car moving at 
22.0 m/s in a straight line measure as the 
velocity of the raindrops? 
73 . A seagull can fly at a velocity of 9.00 m/s in still 
air. (a) If it takes the bird 20.0 min to travel 6.00 
km straight into an oncoming wind, what is the 
velocity of the wind? (b) If the bird turns around 
and flies with the wind, how long will it take the 
bird to return 6.00 km? 
74 . A ship sets sail from Rotterdam, heading due 
north at 7.00 m/s relative to the water. The local 
ocean current is 1.50 m/s in a direction 
north of east. What is the velocity of the ship 
relative to Earth? 
75 . A boat can be rowed at 8.0 km/h in still water. 
(a) How much time is required to row 1.5 km 
downstream in a river moving 3.0 km/h relative 
to the shore? (b) How much time is required for 
the return trip? (c) In what direction must the 
boat be aimed to row straight across the river? 
(d) Suppose the river is 0.8 km wide. What is the 
velocity of the boat with respect to Earth and 
how much time is required to get to the opposite 
shore? (e) Suppose, instead, the boat is aimed 
straight across the river. How much time is 
required to get across and how far downstream 
is the boat when it reaches the opposite shore? 
76 . A small plane flies at 200 km/h in still air. If the 
wind blows directly out of the west at 50 km/h, 
(a) in what direction must the pilot head her 
plane to move directly north across land and (b) 
how long does it take her to reach a point 300 
km directly north of her starting point? 
77 . A cyclist traveling southeast along a road at 15 
km/h feels a wind blowing from the southwest at 
25 km/h. To a stationary observer, what are the 
speed and direction of the wind? 
78 . A river is moving east at 4.0 m/s. A boat starts 
from the dock heading 
 north of west at 7.0 
m/s. If the river is 1800 m wide, (a) what is the 
velocity of the boat with respect to Earth and (b) 
how long does it take the boat to cross the river? 
4 • Chapter Review     189

Additional Problems 
79 . A Formula One race car is traveling at 89.0 m/s 
along a straight track enters a turn on the race 
track with radius of curvature of 200.0 m. What 
centripetal acceleration must the car have to 
stay on the track? 
80 . A particle travels in a circular orbit of radius 10 
m. Its speed is changing at a rate of 
 at 
an instant when its speed is 40.0 m/s. What is 
the magnitude of the acceleration of the 
particle? 
81 . The driver of a car moving at 90.0 km/h presses 
down on the brake as the car enters a circular 
curve of radius 150.0 m. If the speed of the car 
is decreasing at a rate of 9.0 km/h each second, 
what is the magnitude of the acceleration of the 
car at the instant its speed is 60.0 km/h? 
82 . A race car entering the curved part of the track 
at the Daytona 500 drops its speed from 85.0 
m/s to 80.0 m/s in 2.0 s. If the radius of the 
curved part of the track is 316.0 m, calculate the 
total acceleration of the race car at the 
beginning and ending of reduction of speed. 
83 . An elephant is located on Earth’s surface at a 
latitude 
 Calculate the centripetal acceleration of 
the elephant resulting from the rotation of Earth 
around its polar axis. Express your answer in terms 
of 
 the radius 
 of Earth, and time T for one 
rotation of Earth. Compare your answer with g for 
84 . A proton in a synchrotron is moving in a circle of 
radius 1 km and increasing its speed by 
 (a) What is the proton’s total 
acceleration at t = 5.0 s? (b) At what time does 
the expression for the velocity become 
unphysical? 
85 . A propeller blade at rest starts to rotate from t = 
0 s to t = 5.0 s with a tangential acceleration of 
the tip of the blade at 
 The tip of the 
blade is 1.5 m from the axis of rotation. At t = 
5.0 s, what is the total acceleration of the tip of 
the blade? 
86 . A particle is executing circular motion with a 
constant angular frequency of 
 If 
time t = 0 corresponds to the position of the 
particle being located at y = 0 m and x = 5 m, (a) 
what is the position of the particle at t = 10 s? 
(b) What is its velocity at this time? (c) What is 
its acceleration? 
87 . A particle’s centripetal acceleration is 
 at t = 0 s where it is on the x-axis 
and moving counterclockwise in the xy plane. It 
is executing uniform circular motion about an 
axis at a distance of 5.0 m. What is its velocity at 
t = 10 s? 
88 . A rod 3.0 m in length is rotating at 2.0 rev/s 
about an axis at one end. Compare the 
190     4 • Chapter Review
Access for free at openstax.org

centripetal accelerations at radii of (a) 1.0 m, (b) 
2.0 m, and (c) 3.0 m. 
89 . A particle located initially at 
undergoes a displacement of 
 What is the final 
position of the particle? 
90 . The position of a particle is given by 
 (a) What are 
the particle’s velocity and acceleration as 
functions of time? (b) What are the initial 
conditions to produce the motion? 
91 . A spaceship is traveling at a constant velocity of 
 when its rockets fire, giving it 
an acceleration of 
What is its velocity  s after the rockets fire? 
92 . A crossbow is aimed horizontally at a target 40 
m away. The arrow hits 30 cm below the spot at 
which it was aimed. What is the initial velocity of 
the arrow? 
93 . A long jumper can jump a distance of 8.0 m 
when he takes off at an angle of 
 with respect 
to the horizontal. Assuming he can jump with the 
same initial speed at all angles, how much 
distance does he lose by taking off at 
94 . On planet Arcon, the maximum horizontal range 
of a projectile launched at 10 m/s is 20 m. What 
is the acceleration of gravity on this planet? 
95 . A mountain biker encounters a jump on a race 
course that sends him into the air at 
 to the 
horizontal. If he lands at a horizontal distance of 
45.0 m and 20 m below his launch point, what is 
his initial speed? 
96 . Which has the greater centripetal acceleration, a 
car with a speed of 15.0 m/s along a circular 
track of radius 100.0 m or a car with a speed of 
12.0 m/s along a circular track of radius 75.0 m? 
97 . A geosynchronous satellite orbits Earth at a 
distance of 42,250.0 km and has a period of 1 
day. What is the centripetal acceleration of the 
satellite? 
98 . Two speedboats are traveling at the same speed 
relative to the water in opposite directions in a 
moving river. An observer on the riverbank sees 
the boats moving at 4.0 m/s and 5.0 m/s. (a) 
What is the speed of the boats relative to the 
river? (b) How fast is the river moving relative to 
the shore? 
Challenge Problems 
99 . World’s Longest Par 3. The tee of the world’s 
longest par 3 sits atop South Africa’s Hanglip 
Mountain at 400.0 m above the green and can 
only be reached by helicopter. The horizontal 
distance to the green is 359.0 m. Neglect air 
resistance and answer the following questions. 
(a) If a golfer launches a shot that is 
 with 
respect to the horizontal, what initial velocity 
must she give the ball? (b) What is the time to 
reach the green? 
100 . When a field goal kicker kicks a football as hard as 
he can at 
 to the horizontal, the ball just clears 
the 3-m-high crossbar of the goalposts 45.7 m 
away. (a) What is the maximum speed the kicker can 
impart to the football? (b) In addition to clearing the 
crossbar, the football must be high enough in the air 
early during its flight to clear the reach of the 
onrushing defensive lineman. If the lineman is 4.6 m 
away and has a vertical reach of 2.5 m, can he block 
the 45.7-m field goal attempt? (c) What if the 
lineman is 1.0 m away? 
101 . A truck is traveling east at 80 km/h. At an 
intersection 32 km ahead, a car is traveling north 
at 50 km/h. (a) How long after this moment will 
the vehicles be closest to each other? (b) How 
far apart will they be at that point? 
4 • Chapter Review     191

192     4 • Chapter Review
Access for free at openstax.org

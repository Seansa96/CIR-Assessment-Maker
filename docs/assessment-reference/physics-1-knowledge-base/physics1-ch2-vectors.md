# Chapter 2: Vectors

## 2.1 Scalars and Vectors
Physical quantities are broadly classified into two categories:
- **Scalars**: Quantities that are completely described by a magnitude (with units). Examples: Mass, Temperature, Time, Speed.
- **Vectors**: Quantities that require both a magnitude and a direction to be completely described. Examples: Displacement, Velocity, Force.

Vectors are typically represented by arrows, where the length of the arrow corresponds to the magnitude, and the arrowhead indicates the direction.

> **Placeholder:** This explanation requires generation of media showing visual representations of vector arrows and scalar magnitudes.

## 2.2 Coordinate Systems and Components of a Vector
A vector $\vec{A}$ can be broken down into components along the axes of a coordinate system (usually Cartesian). 
In 2D, the components are:
$$ A_x = A \cos \theta $$
$$ A_y = A \sin \theta $$
where $A$ is the magnitude of the vector and $\theta$ is the angle it makes with the positive x-axis.

The magnitude can be reconstructed from the components using the Pythagorean theorem:
$$ A = \sqrt{A_x^2 + A_y^2} $$
And the direction:
$$ \theta = \tan^{-1}\left(\frac{A_y}{A_x}\right) $$

## 2.3 Algebra of Vectors
Vectors can be added geometrically using the head-to-tail method or the parallelogram method. 
Algebraically, vectors are added by adding their respective components:
$$ \vec{C} = \vec{A} + \vec{B} = (A_x + B_x)\hat{i} + (A_y + B_y)\hat{j} $$

Multiplying a vector by a scalar changes its magnitude and, if the scalar is negative, reverses its direction.

## 2.4 Products of Vectors
There are two ways to multiply vectors:

### The Dot Product (Scalar Product)
The dot product of two vectors yields a scalar:
$$ \vec{A} \cdot \vec{B} = A B \cos \phi = A_x B_x + A_y B_y + A_z B_z $$
where $\phi$ is the angle between the two vectors. The dot product is maximized when vectors are parallel and zero when they are perpendicular.

### The Cross Product (Vector Product)
The cross product of two vectors yields a third vector that is perpendicular to both original vectors:
$$ |\vec{A} \times \vec{B}| = A B \sin \phi $$
The direction is determined by the **Right-Hand Rule**. The cross product is zero when vectors are parallel.
In component form (using determinants):
$$ \vec{A} \times \vec{B} = (A_y B_z - A_z B_y)\hat{i} - (A_x B_z - A_z B_x)\hat{j} + (A_x B_y - A_y B_x)\hat{k} $$

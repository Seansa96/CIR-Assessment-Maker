# Young & Freedman University Physics - Chapter 1 Practice Problems Solutions

> [!note] Companion solutions
> These are original worked-study notes for the paired Chapter 1 problem set. Final numerical results were checked against the textbook's answer appendix. Use the figure in the paired problem note whenever a diagram is referenced.

# Problem 1.1

## Key concept

A conversion factor is a ratio equal to one, so units cancel algebraically.

## Worked solution

1. Use $1\ \text{mi}=1.609\ \text{km}$: $1.00\ \text{mi}(1.609\ \text{km}/\text{mi})=1.61\ \text{km}$.
2. Invert the same conversion and use $1\ \text{km}=1000\ \text{m}$ and $1\ \text{m}=3.281\ \text{ft}$: $1.00\ \text{km}=3.28\times10^3\ \text{ft}$.

## Why it works

Each factor cancels the old unit and leaves the desired one. Three significant figures match the given value.

## Issue signals

- `conversion-factor-inverted`
- `unit-cancellation-missed`

# Problem 1.3

## Key concept

For light in vacuum, $d=ct$, so $t=d/c$.

## Worked solution

1. Convert one foot: $d=0.3048\ \text{m}$.
2. Divide by $c=2.998\times10^8\ \text{m/s}$:
$$t=\frac{0.3048}{2.998\times10^8}=1.02\times10^{-9}\ \text{s}=1.02\ \text{ns}.$$

## Why it works

The speed of light is distance per time, so rearranging it gives a travel time.

## Issue signals

- `speed-equation-rearrangement`
- `nano-prefix-error`

# Problem 1.5

## Key concept

Convert a volume by cubing the length conversion, or convert cubic inches directly to liters.

## Worked solution

1. Use $1\ \text{in}=2.54\ \text{cm}$, so $1\ \text{in}^3=(2.54)^3\ \text{cm}^3=16.387\ \text{cm}^3$.
2. Compute $327\ \text{in}^3(16.387\ \text{cm}^3/\text{in}^3)=5.36\times10^3\ \text{cm}^3$.
3. Since $1000\ \text{cm}^3=1\ \text{L}$, the displacement is $5.36\ \text{L}$.

## Why it works

Volume scales with the cube of a length; a linear conversion alone would be wrong.

## Issue signals

- `linear-versus-cubic-conversion`
- `centimeter-cubed-to-liter-error`

# Problem 1.7

## Key concept

Use dimensional analysis to turn seconds into years.

## Worked solution

$$1.00\times10^9\ \text{s}\left(\frac{1\ \text{d}}{86400\ \text{s}}\right)\left(\frac{1\ \text{y}}{365\ \text{d}}\right)=31.7\ \text{y}.$$

You will be about $31.7$ years older.

## Why it works

The seconds cancel first, then days cancel, leaving years.

## Issue signals

- `seconds-per-day-error`
- `scientific-notation-exponent-error`

# Problem 1.9

## Key concept

Fuel economy in mpg is distance per volume. Convert both the mile and gallon before comparing with km/L.

## Worked solution

1. Convert: $55.0\ \text{mi/gal}(1.609\ \text{km}/\text{mi})(1\ \text{gal}/3.785\ \text{L})=23.4\ \text{km/L}$.
2. Divide the trip distance by the distance per tank after expressing both in common units. The required fuel is $1.4$ tankfuls.

## Why it works

Multiplying a rate by conversion factors preserves the physical rate while changing its units.

## Issue signals

- `mpg-to-kmpl-inverted`
- `trip-distance-unit-mismatch`

# Problem 1.11

## Key concept

Density relates mass and volume: $\rho=m/V$. A sphere has $V=\frac43\pi r^3$.

## Worked solution

1. Rearrange the density relation: $V=m/\rho$.
2. Insert $m=60\ \text{kg}$ and the stated density after converting it to consistent units.
3. Set $m/\rho=\frac43\pi r^3$ and solve:
$$r=\left(\frac{3m}{4\pi\rho}\right)^{1/3}=9.0\ \text{cm}.$$

## Why it works

The mass fixes the required volume, and the sphere-volume formula converts that volume to a radius.

## Issue signals

- `density-rearrangement-error`
- `sphere-volume-formula-error`
- `centimeter-meter-conversion`

# Problem 1.13

## Key concept

Percent error is $|\text{measured}-\text{accepted}|/|\text{accepted}|\times100\%$.

## Worked solution

1. Compare the unwanted stopping offset with the $890\ \text{km}$ trip distance in the same length unit.
2. The ratio is $1.1\times10^{-5}$, so the percent error is $1.1\times10^{-3}\%$.
3. That numerical error is tiny, but the figure demonstrates that an operational error can still be unacceptable when the required stopping precision is high.

## Why it works

Percent error measures the relative size of a discrepancy, not its safety consequence.

## Issue signals

- `percent-versus-fraction-error`
- `mixed-length-units`

# Problem 1.15

## Key concept

Compare the approximation $\pi\times10^7\ \text{s}$ with the accepted number of seconds in a year.

## Worked solution

1. Compute the accepted value: $(365.24\ \text{d})(24\ \text{h/d})(3600\ \text{s/h})$.
2. Use $|\pi\times10^7-t_{\rm year}|/t_{\rm year}\times100\%$.
3. The percent error is $0.45\%$.

## Why it works

The accepted value is the denominator because error is judged relative to the best reference value.

## Issue signals

- `percent-error-denominator`
- `seconds-in-year-error`

# Problem 1.17

## Key concept

An order-of-magnitude estimate checks whether a number is physically plausible before calculation.

## Worked solution

Compare $200$ with typical values: a middle-aged person's mass is roughly $10^2\ \text{kg}$ but not plausibly $200\ \text{kg}$ as an ordinary value; height is near $10^0\ \text{m}$ or $10^2\ \text{cm}$, not $200\ \text{m}$ or $200\ \text{cm}$; $200\ \text{mm}$ is too short; and $200$ months is only about $17$ years. Thus none of the listed interpretations is plausible.

## Why it works

Units determine scale. A bare number is incomplete physical information.

## Issue signals

- `units-omitted`
- `order-of-magnitude-misread`

# Problem 1.19

## Key concept

Estimate a total by multiplying a representative count per page by the number of pages.

## Worked solution

1. Estimate a few hundred words per text page and roughly a thousand pages.
2. Their product is on the order of $10^6$ words.

## Why it works

An estimate needs a defensible scale, not false precision.

## Issue signals

- `estimate-with-false-precision`
- `order-of-magnitude-multiplication`

# Problem 1.21

## Key concept

Lifetime estimates combine a rate with a lifetime.

## Worked solution

1. Estimate blinks per minute, waking minutes per day, and days in a lifetime.
2. Multiplying representative values gives fewer than $4\times10^8$ blinks.

## Why it works

Breaking an unknown total into familiar rates makes the scale checkable.

## Issue signals

- `rate-times-duration-error`
- `estimate-with-false-precision`

# Problem 1.23

## Key concept

Estimate volume, use $m=\rho V$, then multiply mass by price per gram.

## Worked solution

1. Model the pile as a human-sized block, about $50\ \text{cm}^3$.
2. Its mass is $(19.3\ \text{g/cm}^3)(50\ \text{cm}^3)\approx10^3\ \text{g}$ for each small block; using the full human-hiding pile gives a value on the order of $\$70$ million.

## Why it works

The uncertainty in the geometry makes an order-of-magnitude monetary result appropriate.

## Issue signals

- `density-times-volume-error`
- `estimate-scale-error`

# Problem 1.25

## Key concept

A campus total is estimated from students, consumption rate, and academic-year duration.

## Worked solution

Choose reasonable values for enrollment, pizzas per student per week, and teaching weeks. Their product is on the order of $10^4$ pizzas per academic year.

## Why it works

This is a Fermi estimate: the assumptions matter more than an exact-looking number.

## Issue signals

- `rate-times-duration-error`
- `estimate-with-false-precision`

# Problem 1.27

## Key concept

The resultant displacement is the vector from start to finish, not the total route length.

## Worked solution

1. Reproduce the route head-to-tail on a scale drawing.
2. Draw one arrow from the initial point to the final point.
3. Measuring the scale drawing gives $7.8\ \text{km}$ at $38^\circ$ north of east.

## Why it works

Head-to-tail addition preserves each displacement's magnitude and direction.

## Issue signals

- `distance-versus-displacement`
- `bearing-reference-direction`

# Problem 1.29

## Key concept

Returning to the start means the vector sum of all four displacements is zero.

## Worked solution

1. Add the first three route vectors head-to-tail on a scale drawing.
2. The fourth vector must point from that final point back to the start.
3. Its measured magnitude and direction are $144\ \text{m}$, $41^\circ$ south of west.

## Why it works

The missing vector is the negative of the resultant of the known vectors.

## Issue signals

- `closure-vector-direction`
- `bearing-reference-direction`

# Problem 1.31

## Key concept

Components are signed projections onto the coordinate axes.

## Worked solution

Read the horizontal and vertical projections from Fig. E1.28:
$$\begin{aligned}
\vec A&=0\hat\imath-8.00\hat\jmath, &\vec B&=7.50\hat\imath+13.0\hat\jmath,\\
\vec C&=-10.9\hat\imath-5.07\hat\jmath, &\vec D&=-7.99\hat\imath+6.02\hat\jmath
\end{aligned}\qquad(\text{m}).$$

## Why it works

A vertical vector has no $x$-component; a horizontal vector has no $y$-component. The sign comes from direction.

## Issue signals

- `component-sign-error`
- `axis-projection-error`

# Problem 1.33

## Key concept

When an angle is measured from the $y$-axis, the $y$-component is adjacent to that angle.

## Worked solution

1. The given component is $A_y=+13.0\ \text{m}$ and the angle is $32.0^\circ$ counterclockwise from $+y$, so the vector lies in quadrant II.
2. Since $A_y$ is adjacent to the stated angle, $A=A_y/\cos32.0^\circ=15.3\ \text{m}$.
3. The horizontal component points left: $A_x=-A\sin32.0^\circ=-8.12\ \text{m}$.

## Why it works

Which trig function is adjacent depends on the axis from which the angle is measured.

## Issue signals

- `sine-cosine-swapped`
- `component-sign-error`

# Problem 1.35

## Key concept

Add or subtract vectors component by component, then reconstruct magnitude and direction.

## Worked solution

1. From Fig. E1.28, $\vec A=(0,-8.00)\ \text{m}$ and $\vec B=(7.50,13.0)\ \text{m}$.
2. $\vec A+\vec B=(7.50,4.99)\ \text{m}$, so both $\vec A+\vec B$ and $\vec B+\vec A$ have magnitude $9.01\ \text{m}$ and direction $33.7^\circ$ above $+x$.
3. $\vec A-\vec B=(-7.50,-21.0)\ \text{m}$, giving $22.3\ \text{m}$ at $70.3^\circ$ south of west. Reversing it, $\vec B-\vec A=(7.50,21.0)\ \text{m}$ gives $22.3\ \text{m}$ at $70.3^\circ$ north of east.

## Why it works

Components are independent, so vector algebra becomes ordinary signed scalar algebra.

## Issue signals

- `vector-subtraction-order`
- `inverse-tangent-quadrant-error`
- `component-sign-error`

# Problem 1.37

## Key concept

Net displacement is the sum of signed north-south and east-west components.

## Worked solution

1. $R_x=-2.90\ \text{km}$ and $R_y=3.25-1.50=1.75\ \text{km}$.
2. $R=\sqrt{(-2.90)^2+(1.75)^2}=3.39\ \text{km}$.
3. $\tan\theta=1.75/2.90$, so $\theta=31.1^\circ$ north of west.

## Why it works

The negative $x$-component establishes west; the positive $y$-component establishes north.

## Issue signals

- `component-sign-error`
- `distance-versus-displacement`
- `bearing-reference-direction`

# Problem 1.39

## Key concept

Resolve each angled vector into components before combining them.

## Worked solution

1. $\vec A=(2.80\cos60.0^\circ)\hat\imath+(2.80\sin60.0^\circ)\hat\jmath=(1.40\hat\imath+2.42\hat\jmath)\ \text{cm}$; $\vec B=(0.950\hat\imath-1.65\hat\jmath)\ \text{cm}$.
2. Add or subtract the components for each requested vector.
3. The results are (a) $\vec A+\vec B=2.48\ \text{cm}$ at $18.4^\circ$ above $+x$; (b) $\vec A-\vec B=4.09\ \text{cm}$ at $83.7^\circ$ above $+x$; (c) $\vec B-\vec A=4.09\ \text{cm}$ at $263.7^\circ$ from $+x$.

## Why it works

Sketches provide a sign and direction check, but components supply the numerical result.

## Issue signals

- `component-sign-error`
- `vector-subtraction-order`
- `inverse-tangent-quadrant-error`

# Problem 1.41

## Key concept

Unit-vector notation packages components as $\vec A=A_x\hat\imath+A_y\hat\jmath$.

## Worked solution

Using the components in Fig. E1.28,
$$\begin{aligned}
\vec A&=-(8.00\ \text{m})\hat\jmath, &\vec B&=(7.50\ \text{m})\hat\imath+(13.0\ \text{m})\hat\jmath,\\
\vec C&=-(10.9\ \text{m})\hat\imath-(5.07\ \text{m})\hat\jmath, &\vec D&=-(7.99\ \text{m})\hat\imath+(6.02\ \text{m})\hat\jmath.
\end{aligned}$$

## Why it works

Zero components are omitted; the negative sign stays attached to the component, not to the unit vector's direction definition.

## Issue signals

- `unit-vector-component-order`
- `component-sign-error`

# Problem 1.43

## Key concept

Unit vectors make addition and subtraction componentwise.

## Worked solution

1. Resolve the figure vectors: $\vec A=(1.23\ \text{m})\hat\imath+(3.38\ \text{m})\hat\jmath$ and $\vec B=(-2.08\ \text{m})\hat\imath-(1.20\ \text{m})\hat\jmath$.
2. Form $\vec C=3\vec A-4\vec B=(12.0\ \text{m})\hat\imath+(14.9\ \text{m})\hat\jmath$.
3. Hence $C=19.2\ \text{m}$ and $\theta=51.2^\circ$ above $+x$.

## Why it works

The unit vectors are perpendicular basis directions, so their coefficients can be handled independently.

## Issue signals

- `unit-vector-component-order`
- `vector-subtraction-order`
- `inverse-tangent-quadrant-error`

# Problem 1.45

## Key concept

The scalar product is $\vec A\cdot\vec B=A_xB_x+A_yB_y$.

## Worked solution

1. Read the components from Fig. E1.28.
2. Multiply matching components and add them; do not multiply magnitudes unless the included angle is known.
3. The requested products are (a) $-104\ \text{m}^2$, (b) $-148\ \text{m}^2$, and (c) $40.6\ \text{m}^2$.

## Why it works

The dot product measures alignment: opposite-directed components contribute negatively.

## Issue signals

- `dot-product-component-pairing`
- `dot-product-sign-error`

# Problem 1.47

## Key concept

For nonzero vectors, $\vec A\cdot\vec B=AB\cos\theta$.

## Worked solution

1. Calculate each dot product from the listed components.
2. Divide by $AB$ and take $\cos^{-1}$.
3. The angles are (a) $165^\circ$, (b) $28^\circ$, and (c) $90^\circ$.

## Why it works

The dot product determines the cosine of the included angle; a zero dot product means perpendicular vectors.

## Issue signals

- `dot-product-magnitude-confusion`
- `inverse-cosine-domain-or-degree-error`

# Problem 1.49

## Key concept

For planar vectors, the cross product is perpendicular to the plane and follows the right-hand rule.

## Worked solution

1. Use the Fig. E1.28 components in $\vec A\times\vec D=(A_xD_y-A_yD_x)\hat k$.
2. The signed result is $\vec A\times\vec D=-63.9\ \text{m}^2\hat k$.
3. Reversing the order reverses the sign: $\vec D\times\vec A=+63.9\ \text{m}^2\hat k$.

## Why it works

The cross product is anti-commutative: $\vec B\times\vec A=-\vec A\times\vec B$.

## Issue signals

- `cross-product-order-reversed`
- `right-hand-rule-error`

# Problem 1.51

## Key concept

The dot product is scalar; the cross product is a vector perpendicular to the $xy$-plane.

## Worked solution

1. Use the Fig. E1.43 components to compute $\vec A\cdot\vec B=26.62\ \text{m}^2$.
2. Use $A_xB_y-A_yB_x$ for the $\hat k$ component.
3. Thus $\vec A\times\vec B=5.55\ \text{m}^2\hat k$.

## Why it works

Component formulas avoid ambiguity about the included angle and its quadrant.

## Issue signals

- `dot-versus-cross-product-confusion`
- `cross-product-order-reversed`

# Problem 1.53

## Key concept

Magnitude comes from the Pythagorean theorem; vector differences require component subtraction.

## Worked solution

1. $A=\sqrt{(-2)^2+3^2+4^2}=5.38$ and $B=\sqrt{3^2+1^2+(-3)^2}=4.36$.
2. $\vec A-\vec B=-5\hat\imath+2\hat\jmath+7\hat k$.
3. Thus $|\vec A-\vec B|=\sqrt{(-5)^2+2^2+7^2}=8.83$. It is generally not $|A-B|$, because magnitudes do not subtract like vectors unless the vectors are collinear.

## Why it works

Subtracting magnitudes discards direction information.

## Issue signals

- `magnitude-subtracted-as-vector`
- `vector-subtraction-order`

# Problem 1.55

## Key concept

At fixed density, mass is proportional to volume, hence $r\propto M^{1/3}$.

## Worked solution

1. Set $M_p/M_N=(r_p/r_N)^3$ because the planet and Neptune have the same density.
2. Solve $r_p=r_N(M_p/M_N)^{1/3}$ using $M_p=5.5M_E$ and Appendix F data.
3. The radius is $1.64\times10^4\ \text{km}=2.57r_E$.

## Why it works

Equal density makes the unknown density cancel in the mass-to-volume ratio.

## Issue signals

- `radius-mass-linear-scaling`
- `cube-root-omitted`

# Problem 1.57

## Key concept

Mass of a component of a gas sample is density times volume times that component's fraction.

## Worked solution

1. Find oxygen mass per breath: $m_{O_2}=\rho_{\rm air}V(0.20)$.
2. Multiply by breaths per day for the daily oxygen mass, giving $2200\ \text{g}$.
3. Divide the room's oxygen mass by that daily use to obtain a corresponding depth of $2.1\ \text{m}$ of air.

## Why it works

The 20% oxygen fraction is applied to the air mass, not added as a separate volume conversion.

## Issue signals

- `fraction-applied-to-wrong-quantity`
- `density-times-volume-error`

# Problem 1.59

## Key concept

For a cylindrical disk, $V=\pi(d/2)^2t$. Small uncertainties are combined from the contributions of the measured factors.

## Worked solution

1. Substitute the measured diameter and thickness into $V=\pi d^2t/4$.
2. Propagate the stated measurement uncertainties; the diameter contribution is doubled because $d$ is squared.
3. The results are $V=(2.8\pm0.3)\ \text{cm}^3$ and $d/t=170\pm20$.

## Why it works

Relative uncertainty from a power is multiplied by that power.

## Issue signals

- `radius-versus-diameter-error`
- `uncertainty-power-rule-missed`

# Problem 1.61

## Key concept

Estimate atoms by dividing body mass by a representative atomic mass, accounting for the dominant elements.

## Worked solution

1. Model the body primarily as water and carbon-based material, so a typical atomic mass is on the order of $10\ \text{u}$.
2. Convert $1\ \text{u}=1.66\times10^{-27}\ \text{kg}$.
3. Dividing a human-scale mass by a typical atom mass gives about $6\times10^{27}$ atoms.

## Why it works

The result is an estimate because composition varies; its order of magnitude is the meaningful conclusion.

## Issue signals

- `atomic-mass-unit-conversion`
- `estimate-with-false-precision`

# Problem 1.63

## Key concept

A surface-covering estimate is area divided by the area of one bill, multiplied by the bill value.

## Worked solution

1. Convert U.S. area and dollar-bill dimensions to a common unit.
2. Compute number of bills $N=A_{\rm US}/A_{\rm bill}$.
3. The total cost is about $\$9\times10^{14}$; dividing by the U.S. population gives about $\$3\times10^6$ per person.

## Why it works

Area, not volume, controls a one-layer covering.

## Issue signals

- `area-versus-volume-confusion`
- `square-unit-conversion`

# Problem 1.65

## Key concept

If the resultant is due north, horizontal components must cancel.

## Worked solution

1. Let the smaller force be $F$ and the larger be $2F$.
2. Set horizontal balance: $F\sin\phi=(2F)\sin25.0^\circ$.
3. Set vertical sum: $F\cos\phi+(2F)\cos25.0^\circ=460.0\ \text{N}$.
4. Solve: the pulls are $196\ \text{N}$ at $57.7^\circ$ east of north and $392\ \text{N}$ at $25.0^\circ$ west of north.

## Why it works

The requested resultant supplies two independent component equations.

## Issue signals

- `sine-cosine-swapped`
- `horizontal-components-not-canceled`
- `force-ratio-ignored`

# Problem 1.67

## Key concept

Match components of the required resultant to solve for an unknown vector.

## Worked solution

1. Write all three displacement vectors in component form using the stated angles.
2. Impose $\vec A+\vec B=\vec C$ and equate $x$ and $y$ components.
3. The required first-displacement components are $A_x=3.03\ \text{cm}$ and $A_y=8.10\ \text{cm}$; its magnitude is $8.65\ \text{cm}$.

## Why it works

An equality of vectors means equality of each corresponding component.

## Issue signals

- `resultant-component-equation-error`
- `angle-reference-axis-error`

# Problem 1.69

## Key concept

The missing displacement is $-\!(\vec d_1+\vec d_2+\vec d_3)$.

## Worked solution

1. Take east as $+x$ and north as $+y$.
2. Resolve each known cave displacement into $x$ and $y$ components and add them.
3. Negate the sum: the fourth displacement is $144\ \text{m}$, $41^\circ$ south of west.

## Why it works

The final position equals the initial position, so the closed-path vector sum is zero.

## Issue signals

- `closure-vector-direction`
- `component-sign-error`

# Problem 1.71

## Key concept

Add simultaneous forces by resolving the angled force into forward and perpendicular components.

## Worked solution

1. $R_x=480+513\cos32^\circ$ and $R_y=513\sin32^\circ$.
2. $R=\sqrt{R_x^2+R_y^2}=954\ \text{N}$.
3. $\theta=\tan^{-1}(R_y/R_x)=16.8^\circ$ above forward.

## Why it works

Only the second engine contributes a transverse component.

## Issue signals

- `sine-cosine-swapped`
- `inverse-tangent-quadrant-error`

# Problem 1.73

## Key concept

Equal symmetric pulls have transverse components that cancel and axial components that add.

## Worked solution

1. Let either pull have magnitude $F$.
2. Along the arm, $2F\cos32^\circ=5.60\ \text{N}$.
3. Thus $F=3.30\ \text{N}$ for each pull.

## Why it works

Symmetry makes the sideways components equal and opposite.

## Issue signals

- `symmetric-components-not-canceled`
- `sine-cosine-swapped`

# Problem 1.75

## Key concept

Equilibrium requires $\sum\vec F=0$.

## Worked solution

1. Resolve the known $100.0\ \text{N}$ pull and the $124\ \text{N}$ weight into components.
2. The floor force must be their negative resultant: $\vec F_{\rm floor}=-(\vec F_{100}+\vec W)$.
3. Its magnitude is $45.5\ \text{N}$ and its direction is $139^\circ$ in the coordinate convention of the figure.

## Why it works

The equilibrium force closes the force-vector polygon.

## Issue signals

- `equilibrium-sign-error`
- `force-diagram-incomplete`
- `inverse-tangent-quadrant-error`

# Problem 1.77

## Key concept

Screen coordinates use a downward-positive $y$ direction, unlike the usual Cartesian convention.

## Worked solution

1. Subtract initial coordinates from final coordinates, preserving the screen convention.
2. The endpoint is $(87,258)$.
3. The displacement magnitude is $136$ pixels, directed $25^\circ$ below straight left.

## Why it works

Coordinates are meaningful only with their specified axis orientations.

## Issue signals

- `screen-y-axis-sign-error`
- `coordinate-subtraction-order`

# Problem 1.79

## Key concept

The elbow force is found from force balance after resolving the biceps force.

## Worked solution

1. Combine the two downward weights: $20.5+112.0=132.5\ \text{N}$ downward.
2. Resolve the $232\ \text{N}$ biceps pull at the stated forearm angle.
3. Require $\vec F_{\rm elbow}+\vec F_{\rm biceps}+(0,-132.5\ \text{N})=0$.
4. The elbow force is $160\ \text{N}$, $13^\circ$ below horizontal.

## Why it works

The forearm is in equilibrium, so every force must be included in the vector sum.

## Issue signals

- `equilibrium-sign-error`
- `weight-forces-not-combined`
- `sine-cosine-swapped`

# Problem 1.81

## Key concept

The return displacement is the negative of the outward resultant.

## Worked solution

1. Resolve each outward walk using east as $+x$ and north as $+y$.
2. Add the components; negate both to obtain the return vector.
3. The required return is $911\ \text{m}$ at $8.9^\circ$ west of south.

## Why it works

Negating a displacement changes direction but not magnitude.

## Issue signals

- `closure-vector-direction`
- `bearing-reference-direction`
- `component-sign-error`

# Problem 1.83

## Key concept

Set the desired final coordinate, then subtract the known displacements.

## Worked solution

1. Write the first two dog runs as components.
2. The desired final position is $(0,-10.0\ \text{m})$ relative to the start.
3. The needed last vector is $\vec r_{\rm final}-\vec r_{\rm current}$, giving $29.6\ \text{m}$ at $18.6^\circ$ east of south.

## Why it works

Position vectors add to the stated final position.

## Issue signals

- `target-position-versus-displacement`
- `component-sign-error`

# Problem 1.85

## Key concept

Translate the relative-position statements into a common coordinate system.

## Worked solution

1. Put John at the origin and Paul at $(-14.0,0)$ m.
2. Resolve George's stated displacement from Paul into east and south components.
3. The vector from George to John has magnitude $26.2\ \text{m}$ and direction $34.2^\circ$ east of south.

## Why it works

Every position must be measured from the same origin before subtraction.

## Issue signals

- `relative-position-order`
- `bearing-reference-direction`

# Problem 1.87

## Key concept

Dot and cross products give $\tan\theta=|\vec A\times\vec B|/(\vec A\cdot\vec B)$, with the sign of the dot product identifying an obtuse angle.

## Worked solution

1. Form $\cos\theta=(\vec A\cdot\vec B)/(AB)$ and $\sin\theta=|\vec A\times\vec B|/(AB)$.
2. Their ratio gives the reference angle; the negative dot product places $\theta$ in quadrant II.
3. Therefore $\theta=124^\circ$.

## Why it works

The cross-product magnitude loses only the sign of the angle; the dot product supplies that missing information.

## Issue signals

- `obtuse-angle-from-dot-product-missed`
- `dot-versus-cross-product-confusion`

# Problem 1.89

## Key concept

For an angle $\theta$, $(\vec A\cdot\vec B)^2+|\vec A\times\vec B|^2=A^2B^2$.

## Worked solution

1. Insert $A=12.0\ \text{m}$, $B=16.0\ \text{m}$, and the stated dot product.
2. Solve $|\vec A\times\vec B|=\sqrt{A^2B^2-(\vec A\cdot\vec B)^2}$.
3. The magnitude is $170\ \text{m}^2$.

## Why it works

This is the Pythagorean identity $\sin^2\theta+\cos^2\theta=1$ expressed through vector products.

## Issue signals

- `dot-versus-cross-product-confusion`
- `square-root-or-unit-error`

# Problem 1.91

## Key concept

Represent cube edges and diagonals with component vectors, then use the dot-product angle formula.

## Worked solution

1. Let the cube edge length be $a$. Then $\vec{ab}=a\hat k$, $\vec{ad}=a(\hat\imath+\hat\jmath+\hat k)$, and $\vec{ac}=a(\hat\imath+\hat\jmath)$.
2. Apply $\cos\theta=\vec u\cdot\vec v/(uv)$ to each pair.
3. The angles are (a) $54.7^\circ$ and (b) $35.3^\circ$.

## Why it works

The arbitrary edge length cancels, so the angles depend only on cube geometry.

## Issue signals

- `three-dimensional-component-error`
- `dot-product-magnitude-confusion`

# Problem 1.93

## Key concept

Use the stated directions to obtain the included angle, then solve the dot-product equation for the unknown magnitude.

## Worked solution

1. Draw the west-of-south and south-of-east directions to find their included angle.
2. Substitute into $\vec A\cdot\vec B=AB\cos\theta$.
3. Solving for the unknown magnitude gives $28.0\ \text{m}$.

## Why it works

The dot product uses the angle between the vectors, not either bearing alone.

## Issue signals

- `bearing-to-included-angle-error`
- `dot-product-rearrangement-error`

# Problem 1.95

## Key concept

An unknown planar vector is determined by two independent scalar conditions.

## Worked solution

1. Write $\vec C=C_x\hat\imath+C_y\hat\jmath$.
2. Translate $\vec C\perp\vec A$ into $\vec C\cdot\vec A=0$.
3. Translate the stated scalar product with $\vec B$ into $\vec C\cdot\vec B=15.0$.
4. Solve the two linear equations: $C_x=8.0$ and $C_y=6.1$.

## Why it works

Perpendicularity is a dot-product condition, giving one equation for each unknown component.

## Issue signals

- `perpendicular-dot-product-missed`
- `linear-system-setup-error`

# Problem 1.97

## Key concept

Use distributivity of the cross product and the scalar triple-product identity.

## Worked solution

1. Expand $\vec A\times(\vec B\times\vec C)$ and $(\vec A\times\vec B)\times\vec C$ componentwise or by the vector triple-product identity.
2. This proves the requested relation and shows that cross products are not generally associative.
3. Substitute the given magnitudes and directions for part (b); the requested numerical result is $72.2$.

## Why it works

Parentheses matter in a cross-product expression because the intermediate result is a vector with a different direction.

## Issue signals

- `cross-product-associativity-assumed`
- `right-hand-rule-error`

# Problem 1.99

## Key concept

The pass vector equals receiver position minus quarterback position at release.

## Worked solution

1. Add the receiver's initial position and all listed route displacements to get $\vec r_{\rm receiver}$.
2. Write the quarterback's drop as $\vec r_{\rm QB}$.
3. Compute $\vec r_{\rm throw}=\vec r_{\rm receiver}-\vec r_{\rm QB}$.
4. Its magnitude is $38.5\ \text{yd}$, directed $24.6^\circ$ to the right of downfield.

## Why it works

A displacement from one object to another is final position minus initial position, in that order.

## Issue signals

- `relative-position-order`
- `component-sign-error`
- `bearing-reference-direction`

# Physics Question Bank

**Legend:**
- `[C]` Conceptual — understanding definitions, behaviors, relationships
- `[P]` Procedural — step-by-step calculation
- `[CT]` Critical Thinking — multi-step, proof-adjacent, application
- `[N]` Novel — unusual framing, graphical, "what if," reverse engineering

---

## Physics 1: Mechanics

### Topic 1: Kinematics (1D and 2D)

**Q1.** `[C]` What is the difference between speed and velocity? Between distance and displacement?

**Q2.** `[C]` An object has zero velocity but nonzero acceleration. Give a physical example.
> **Answer:** A ball thrown vertically upward at its highest point: $v=0$ but $a=-g \ne 0$.

**Q3.** `[P]` A car starts from rest and accelerates uniformly at $4 \text{ m/s}^2$ for $6 \text{ s}$. Find its final velocity and displacement.
> **Answer:** $v = at = 4(6) = 24 \text{ m/s}$. $x = \frac{1}{2}at^2 = \frac{1}{2}(4)(36) = 72 \text{ m}$.

**Q4.** `[P]` A ball is thrown upward with $v_0 = 20 \text{ m/s}$. How high does it go? How long before it returns to the launch point? ($g=10 \text{ m/s}^2$)
> **Answer:** $v^2=v_0^2-2gh \implies h=v_0^2/(2g)=400/20=20\text{m}$. Time up: $t=v_0/g=2\text{s}$. Total time: $4\text{s}$.

**Q5.** `[P]` A projectile is launched at $30\text{ m/s}$ at $37°$ above horizontal. Find the maximum height, range, and time of flight. ($g=10\text{ m/s}^2$, $\sin37°=0.6$, $\cos37°=0.8$)
> **Answer:** $v_{0x}=24\text{m/s}$, $v_{0y}=18\text{m/s}$. $t_{top}=v_{0y}/g=1.8\text{s}$. $h=v_{0y}^2/(2g)=16.2\text{m}$. Total time $=3.6\text{s}$. Range $=v_{0x}\cdot3.6=86.4\text{m}$.

**Q6.** `[P]` Two trains are $200\text{m}$ apart and approaching each other. Train A moves at $15\text{m/s}$ and train B at $25\text{m/s}$. In how many seconds do they collide?
> **Answer:** Approach speed $=40\text{m/s}$. Time $=200/40=5\text{s}$.

**Q7.** `[P]` A particle's position is $x(t)=3t^3-12t+5\text{m}$. Find when the particle is at rest and whether it momentarily reverses direction.
> **Answer:** $v(t)=9t^2-12=0 \implies t^2=4/3 \implies t=\frac{2}{\sqrt{3}}\approx1.15\text{s}$. $a(t)=18t>0$, so the particle reverses direction.

**Q8.** `[CT]` A stone is dropped from rest. A second stone is thrown downward at $10\text{m/s}$ from the same height $1\text{s}$ later. Find the time at which they have the same velocity.
> **Answer:** $v_1=gt$. $v_2=10+g(t-1)$. Set equal: $gt=10+gt-g \implies g=10$. This is always true! They always differ by $10\text{m/s} - g\cdot(1\text{s}) + g\cdot(1\text{s}) = 10\text{m/s} - 10\text{m/s} = 0$... Re-examine: $v_1=gt$, $v_2=10+g(t-1)=10+gt-g=gt+(10-g)$. With $g=10\text{m/s}^2$: $v_2=gt$. So their velocities are equal for all $t\ge 1\text{s}$.

**Q9.** `[CT]` A ball is thrown horizontally from height $H$ and lands at horizontal distance $R$. Derive the expression for the initial speed $v_0$.
> **Answer:** $H=\frac{1}{2}gt_{land}^2 \implies t_{land}=\sqrt{2H/g}$. $R=v_0 t_{land} \implies v_0=R/t_{land}=R\sqrt{g/(2H)}$.

**Q10.** `[N]` Without using any formulas, explain why the range of a projectile launched at angle $\theta$ equals the range at angle $(90°-\theta)$.
> **Answer:** $R = \frac{v_0^2 \sin(2\theta)}{g}$. Since $\sin(2(90°-\theta))=\sin(180°-2\theta)=\sin(2\theta)$, the range is symmetric about $45°$.

**Q11.** `[N]` A particle moves with acceleration $a(t) = 6t - 4$. At $t=0$, $v=2$ and $x=0$. Find $x(t)$.
> **Answer:** $v(t)=\int a\,dt=3t^2-4t+2$. $x(t)=\int v\,dt=t^3-2t^2+2t$.

**Q12.** `[CT]` A river flows east at $3\text{m/s}$. A swimmer can swim at $5\text{m/s}$ relative to the water. At what angle upstream should she swim to go straight across?
> **Answer:** She must cancel east drift. $5\sin\alpha=3 \implies \alpha=\sin^{-1}(3/5)=37°$ west of north (upstream). Effective speed north: $5\cos\alpha=4\text{m/s}$.

---

### Topic 2: Dynamics (Newton's Laws, Friction, Circular Motion)

**Q13.** `[C]` State Newton's three laws in your own words and give a real-world example for each.

**Q14.** `[C]` A book sits on a table. Identify all forces on the book and the reaction partner for each (Newton's 3rd Law).
> **Answer:** Forces on book: gravity (Earth pulls book down) and normal force (table pushes book up). Reaction pairs: book pulls Earth up; book pushes table down.

**Q15.** `[P]` A $10\text{kg}$ box is on a horizontal surface. A $50\text{N}$ horizontal force is applied. If $\mu_k=0.3$, find the acceleration.
> **Answer:** $N=mg=98\text{N}$. Friction $=\mu_k N=29.4\text{N}$. Net force $=50-29.4=20.6\text{N}$. $a=20.6/10=2.06\text{ m/s}^2$.

**Q16.** `[P]` Find the maximum angle $\theta$ at which a block will remain stationary on a ramp if $\mu_s=0.40$.
> **Answer:** $\tan\theta=\mu_s=0.40 \implies \theta=\arctan(0.40)\approx21.8°$.

**Q17.** `[P]` A $2\text{kg}$ block on a frictionless incline of $30°$ is connected by a string over a massless pulley to a hanging $3\text{kg}$ mass. Find the acceleration.
> **Answer:** Net force $= m_2 g - m_1 g\sin30° = 3(9.8)-2(9.8)(0.5)=29.4-9.8=19.6\text{N}$. Total mass $=5\text{kg}$. $a=19.6/5=3.92\text{ m/s}^2$.

**Q18.** `[P]` A $1500\text{kg}$ car rounds a flat curve of radius $80\text{m}$ at $20\text{m/s}$. What minimum friction force keeps it on the road?
> **Answer:** $f = \frac{mv^2}{r} = \frac{1500(400)}{80} = 7500\text{N}$.

**Q19.** `[P]` What is the minimum speed at the top of a vertical circular loop of radius $5\text{m}$ for a roller coaster to maintain contact with the track? ($g=9.8\text{ m/s}^2$)
> **Answer:** At top, $mg = \frac{mv^2}{r} \implies v_{min}=\sqrt{gr}=\sqrt{9.8\cdot5}=7\text{ m/s}$.

**Q20.** `[CT]` Two blocks A ($3\text{kg}$) and B ($5\text{kg}$) are in contact on a frictionless surface. A force of $24\text{N}$ pushes A into B. Find: (a) the acceleration, (b) the contact force between A and B.
> **Answer:** (a) $a=24/8=3\text{ m/s}^2$. (b) On B alone: $F_{AB}=m_B\cdot a=5(3)=15\text{N}$.

**Q21.** `[CT]` A conical pendulum has a bob of mass $m$, string length $L$, and makes angle $\theta$ with the vertical. Derive the expression for the period $T$ of revolution.
> **Answer:** $T\sin\theta=\frac{mv^2}{r}$ and $T\cos\theta=mg$, where $T$ is string tension, $r=L\sin\theta$. Dividing: $\tan\theta=v^2/(rg)$. Speed $v=2\pi r/T_{period}$. Combining gives $T_{period}=2\pi\sqrt{\frac{L\cos\theta}{g}}$.

**Q22.** `[N]` An object on a frictionless surface is connected by a string to a hanging mass through a hole in the surface. Show that if the hanging mass is in equilibrium, the surface object moves in uniform circular motion.
> **Answer:** The tension in the string equals $mg$ (hanging mass weight). This tension acts as the centripetal force on the surface object: $T=mv^2/r$. With constant $T=Mg$, if $r$ and $m$ are constant, $v$ is constant, so motion is uniform circular motion.

---

### Topic 3: Work, Energy, and Power

**Q23.** `[C]` Explain the Work-Energy Theorem. Is it valid when friction is present?
> **Answer:** $W_{net}=\Delta K$. Yes, it's valid with friction — friction does negative work and removes kinetic energy, which is properly captured by $W_{net}$.

**Q24.** `[P]` How much work does gravity do on a $5\text{kg}$ ball falling $10\text{m}$?
> **Answer:** $W=mgh=5(9.8)(10)=490\text{J}$.

**Q25.** `[P]` A spring with $k=200\text{N/m}$ is compressed $0.15\text{m}$. How much energy is stored?
> **Answer:** $U=\frac{1}{2}kx^2=\frac{1}{2}(200)(0.0225)=2.25\text{J}$.

**Q26.** `[P]` A $70\text{kg}$ person climbs $20\text{m}$ in $30\text{s}$. What is their minimum power output?
> **Answer:** $P=W/t=mgh/t=70(9.8)(20)/30\approx457\text{W}$.

**Q27.** `[P]` A $2\text{kg}$ block slides from rest down a frictionless ramp of height $3\text{m}$ and then along a rough surface with $\mu_k=0.2$ for distance $d$. Find $d$ when the block stops.
> **Answer:** KE at bottom $=mgh=2(9.8)(3)=58.8\text{J}$. Friction force $=\mu_k mg=0.2(2)(9.8)=3.92\text{N}$. $d=W/F=58.8/3.92=15\text{m}$.

**Q28.** `[CT]` A bead slides on a frictionless wire shaped as a parabola $y=x^2$ from $(2,4)$ to $(-1,1)$. Find its final speed if it starts from rest.
> **Answer:** By conservation of energy (frictionless), only height change matters. $\Delta h = 1-4=-3\text{m}$ (drops $3\text{m}$). $v=\sqrt{2g|\Delta h|}=\sqrt{2(9.8)(3)}\approx7.67\text{m/s}$.

**Q29.** `[CT]` Derive the escape velocity from the surface of Earth (mass $M$, radius $R$).
> **Answer:** Set KE equal to gravitational PE: $\frac{1}{2}mv^2=\frac{GMm}{R} \implies v_{esc}=\sqrt{2GM/R}$.

**Q30.** `[N]` A force acts on a particle along the x-axis: $F(x)=3x^2-2x$. Find the work done in moving from $x=0$ to $x=4\text{m}$.
> **Answer:** $W=\int_0^4(3x^2-2x)dx=[x^3-x^2]_0^4=64-16=48\text{J}$.

**Q31.** `[N]` An engine delivers constant power $P$ to a car starting from rest. Show that velocity grows as $v\propto t^{1/2}$.
> **Answer:** $P=Fv=mav$. So $mav=P$. Since $a=dv/dt$: $mv\,dv=P\,dt$. Integrating: $\frac{1}{2}mv^2=Pt \implies v=\sqrt{2Pt/m} \propto t^{1/2}$.

---

### Topic 4: Momentum, Impulse, and Collisions

**Q32.** `[C]` What condition is required for conservation of linear momentum to hold? Explain why internal forces don't affect the total momentum.
> **Answer:** Conservation holds when the net *external* force on the system is zero. Internal forces cancel in Newton's 3rd Law pairs, so they don't change the total momentum.

**Q33.** `[P]` A $0.15\text{kg}$ baseball moving at $40\text{m/s}$ is hit by a bat and reverses direction at $50\text{m/s}$. If the contact time is $0.002\text{s}$, find the average force.
> **Answer:** $J=\Delta p=m(v_f-v_i)=0.15(50-(-40))=13.5\text{N s}$. $F=J/t=13.5/0.002=6750\text{N}$.

**Q34.** `[P]` A $1\text{kg}$ clay ball moving at $6\text{m/s}$ east collides and sticks to a $2\text{kg}$ clay ball moving at $3\text{m/s}$ west. Find the final velocity.
> **Answer:** $p_i=1(6)+2(-3)=0\text{kg m/s}$. $v_f=0/(3)=0$. They come to rest.

**Q35.** `[P]` In a 1D elastic collision, a $3\text{kg}$ ball at $8\text{m/s}$ hits a stationary $1\text{kg}$ ball. Find the final velocities.
> **Answer:** $v_1'=\frac{m_1-m_2}{m_1+m_2}v_1=\frac{2}{4}(8)=4\text{m/s}$. $v_2'=\frac{2m_1}{m_1+m_2}v_1=\frac{6}{4}(8)=12\text{m/s}$.

**Q36.** `[CT]` A $70\text{kg}$ astronaut in space holds a $5\text{kg}$ wrench and throws it at $8\text{m/s}$. What is the astronaut's recoil velocity?
> **Answer:** $m_1v_1=-m_2v_2 \implies 70v_1=-5(8) \implies v_1=-\frac{40}{70}\approx-0.57\text{m/s}$.

**Q37.** `[CT]` In a perfectly inelastic collision, what fraction of kinetic energy is lost when a mass $m$ hits an equal stationary mass $m$ at speed $v_0$?
> **Answer:** $KE_i=\frac{1}{2}mv_0^2$. After: $v_f=v_0/2$, $KE_f=\frac{1}{2}(2m)(v_0/2)^2=\frac{1}{4}mv_0^2$. Fraction lost $=1/2$.

**Q38.** `[N]` A rocket expels gas at speed $v_e$ (relative to rocket). Derive the Tsiolkovsky rocket equation relating velocity change to mass ratio.
> **Answer:** Momentum conservation: $(m+dm)(v+dv)-m\cdot v + (-dm)(-v_e) = 0 \implies m\,dv + v_e\,dm = 0$ (dropping $dm\cdot dv$). $dv = -v_e\frac{dm}{m}$. Integrating: $\Delta v = v_e \ln(m_0/m_f)$.

---

### Topic 5: Rotational Motion and Angular Momentum

**Q39.** `[C]` Explain why an ice skater spins faster when they pull their arms in.
> **Answer:** Angular momentum $L=I\omega$ is conserved (no external torque). Pulling arms in decreases $I$, so $\omega$ must increase.

**Q40.** `[P]` A disk ($I=\frac{1}{2}MR^2$, $M=2\text{kg}$, $R=0.5\text{m}$) starts from rest and accelerates at $\alpha=4\text{rad/s}^2$ for $5\text{s}$. Find the final angular velocity and angular displacement.
> **Answer:** $\omega=\alpha t=20\text{rad/s}$. $\theta=\frac{1}{2}\alpha t^2=50\text{rad}$.

**Q41.** `[P]` Find the torque needed to give a $3\text{kg}$ uniform rod of length $1.2\text{m}$ (pivoting at one end) an angular acceleration of $5\text{rad/s}^2$.
> **Answer:** $I=\frac{1}{3}ML^2=\frac{1}{3}(3)(1.44)=1.44\text{kg m}^2$. $\tau=I\alpha=1.44(5)=7.2\text{N m}$.

**Q42.** `[P]` A $0.5\text{kg}$ ball on a $0.8\text{m}$ string moves in a horizontal circle at $4\text{m/s}$. Find its angular momentum about the center.
> **Answer:** $L=mvr=0.5(4)(0.8)=1.6\text{kg m}^2/\text{s}$.

**Q43.** `[CT]` A solid sphere ($I=\frac{2}{5}MR^2$) and a hollow sphere ($I=\frac{2}{3}MR^2$) of the same mass and radius roll from rest down the same incline. Which reaches the bottom first and why?
> **Answer:** Solid sphere: $a=\frac{5}{7}g\sin\theta$. Hollow sphere: $a=\frac{3}{5}g\sin\theta=\frac{5}{7}g\cdot\frac{21}{25}\sin\theta$. Numerically, $5/7>3/5$, so solid sphere accelerates faster and wins.

**Q44.** `[CT]` A $60\text{kg}$ student sits at the rim of a spinning stool-platform (radius $1.0\text{m}$, $I_{platform}=20\text{kg m}^2$) rotating at $1.5\text{rad/s}$. She moves to the center. What is the new angular velocity?
> **Answer:** $L=I_i\omega_i=(I_{plat}+mr^2)\omega_i=(20+60)\cdot1.5=120\text{kg m}^2/\text{s}$. At center: $I_f=20+0=20\text{kg m}^2$. $\omega_f=L/I_f=120/20=6\text{rad/s}$.

**Q45.** `[N]` Gyroscope: A spinning wheel ($\omega=50\text{rad/s}$, $I=0.1\text{kg m}^2$) is held horizontal by a string at one end of its axle (distance $0.3\text{m}$ from center). What is the precession angular velocity?
> **Answer:** Torque from gravity: $\tau=mgd=(I\omega/d)\cdot g\cdot d=$ well, using $L=I\omega=5\text{kg m}^2/\text{s}$. Weight $mg$ acting at distance $d=0.3\text{m}$: $\tau=mgd$. Precession: $\Omega=\tau/L=mgd/(I\omega)$.

---

### Topic 6: Gravitation and Orbital Mechanics

**Q46.** `[C]` Explain Kepler's three laws in plain language.
> **Answer:** (1) Orbits are ellipses with the Sun at one focus. (2) The line from Sun to planet sweeps equal areas in equal times (conservation of angular momentum). (3) $T^2\propto a^3$ where $a$ is the semi-major axis.

**Q47.** `[P]` The Moon orbits Earth ($M=5.97\times10^{24}\text{kg}$) at radius $3.84\times10^8\text{m}$. Find its orbital period.
> **Answer:** $T=2\pi\sqrt{r^3/(GM)}=2\pi\sqrt{(3.84\times10^8)^3/(6.67\times10^{-11}\cdot5.97\times10^{24})}\approx2.36\times10^6\text{s}\approx27.3\text{ days}$.

**Q48.** `[P]` What is the gravitational field strength $g$ at height $h=R_E$ (one Earth radius) above Earth's surface?
> **Answer:** $g'=GM/(2R_E)^2=g/4\approx2.45\text{ m/s}^2$.

**Q49.** `[CT]` Show that for a circular orbit, the orbital speed $v_{orb}=\sqrt{GM/r}$.
> **Answer:** Set gravitational force equal to centripetal force: $\frac{GMm}{r^2}=\frac{mv^2}{r}$. Solve for $v$: $v=\sqrt{GM/r}$.

**Q50.** `[N]` A satellite in circular orbit at radius $r$ is given a small kick to increase its speed. Does the radius increase or decrease? Explain via energy arguments.
> **Answer:** Total mechanical energy $E=-GMm/(2r)$ (more negative $\implies$ lower orbit). Increasing speed increases KE, but orbital energy is $E=KE+PE=-KE$ for a circular orbit. A higher speed object actually requires a higher orbit. After the kick, the orbit becomes elliptical and the time-average radius is larger.

---

## Physics 2: Electricity, Magnetism, and Thermodynamics

### Topic 7: Electrostatics

**Q51.** `[C]` State Gauss's Law. What makes it useful for calculating electric fields?
> **Answer:** $\oint \vec{E}\cdot d\vec{A}=Q_{enc}/\epsilon_0$. It's useful when the charge distribution has symmetry (spherical, cylindrical, planar), allowing the field to be pulled out of the integral.

**Q52.** `[P]` Use Gauss's Law to find $E$ outside a long line charge with linear charge density $\lambda$.
> **Answer:** Gaussian surface: cylinder of radius $r$, length $L$. $E(2\pi r L)=\lambda L/\epsilon_0 \implies E=\frac{\lambda}{2\pi\epsilon_0 r}$.

**Q53.** `[P]` Find the electric potential at the center of a square of side $a$ with charge $Q$ at each corner.
> **Answer:** Distance from corner to center $=\frac{a\sqrt{2}}{2}$. $V=4\cdot\frac{kQ}{a\sqrt{2}/2}=\frac{8\sqrt{2}kQ}{a}$.

**Q54.** `[P]` A proton ($q=1.6\times10^{-19}\text{C}$, $m=1.67\times10^{-27}\text{kg}$) starts from rest and is accelerated through $V=10^4\text{V}$. Find its final speed.
> **Answer:** $qV=\frac{1}{2}mv^2 \implies v=\sqrt{2qV/m}=\sqrt{2(1.6\times10^{-19})(10^4)/(1.67\times10^{-27})}\approx1.38\times10^6\text{ m/s}$.

**Q55.** `[CT]` A conducting sphere of radius $R$ has total charge $Q$ uniformly distributed. Find $E$ inside, on the surface, and outside.
> **Answer:** Inside ($r<R$): $E=0$ (conductor, all charge on surface). Surface ($r=R$): $E=kQ/R^2$. Outside ($r>R$): $E=kQ/r^2$.

**Q56.** `[N]` Two large parallel plates are separated by $d=5\text{mm}$ and create a uniform field $E=3000\text{V/m}$. An electron is released from the negative plate. How long does it take to reach the positive plate?
> **Answer:** $F=eE=1.6\times10^{-19}\times3000=4.8\times10^{-16}\text{N}$. $a=F/m=4.8\times10^{-16}/9.11\times10^{-31}\approx5.27\times10^{14}\text{m/s}^2$. $d=\frac{1}{2}at^2 \implies t=\sqrt{2d/a}=\sqrt{2(5\times10^{-3})/(5.27\times10^{14})}\approx1.38\times10^{-8}\text{s}$.

---

### Topic 8: Capacitance, Resistance, and DC Circuits

**Q57.** `[C]` What happens to the charge, voltage, and energy stored in a capacitor if a dielectric is inserted after the capacitor is disconnected from the battery?
> **Answer:** Charge stays constant (battery disconnected). Voltage decreases by factor $\kappa$ (dielectric constant). Energy $U=Q^2/(2C)$ decreases (extra energy goes into polarizing the dielectric).

**Q58.** `[P]` Three resistors ($6\Omega$, $12\Omega$, and $4\Omega$) are connected in parallel across a $24\text{V}$ battery. Find the total current drawn from the battery.
> **Answer:** $\frac{1}{R_{eq}}=\frac{1}{6}+\frac{1}{12}+\frac{1}{4}=\frac{2+1+3}{12}=\frac{6}{12}=\frac{1}{2}$. $R_{eq}=2\Omega$. $I=24/2=12\text{A}$.

**Q59.** `[P]` A $12\text{V}$ battery with internal resistance $1\Omega$ is connected to an external $5\Omega$ resistor. Find the terminal voltage and power delivered to the external resistor.
> **Answer:** $I=12/(1+5)=2\text{A}$. Terminal voltage $=12-1(2)=10\text{V}$. $P_{ext}=I^2R_{ext}=4(5)=20\text{W}$.

**Q60.** `[P]` Two capacitors ($C_1=4\mu\text{F}$, $C_2=6\mu\text{F}$) are in series across $30\text{V}$. Find the voltage across each.
> **Answer:** $C_{eq}=\frac{4\times6}{10}=2.4\mu\text{F}$. $Q=C_{eq}V=72\mu\text{C}$. $V_1=Q/C_1=72/4=18\text{V}$. $V_2=Q/C_2=72/6=12\text{V}$.

**Q61.** `[CT]` Use Kirchhoff's Laws to find the current through each branch of a circuit with two batteries ($\mathcal{E}_1=12\text{V}$, $\mathcal{E}_2=6\text{V}$) and three resistors ($R_1=4\Omega$, $R_2=2\Omega$, $R_3=3\Omega$) — loop circuit.
> **Answer:** Apply KVL around two loops. Solve the resulting system of linear equations. (Specific numerical answer depends on exact topology — this prompts systematic application of Kirchhoff's Laws.)

**Q62.** `[N]` A capacitor is initially uncharged and in series with a resistor $R$ and battery $\mathcal{E}$. Sketch $V_C(t)$ and explain physically why current drops to zero as $t\to\infty$.
> **Answer:** $V_C(t)=\mathcal{E}(1-e^{-t/RC})$. As the capacitor charges, the voltage across it increases, reducing the voltage across $R$ and thus the current. At equilibrium $V_C=\mathcal{E}$ and current is zero.

---

### Topic 9: Magnetism

**Q63.** `[C]` A positive charge moves north in a magnetic field pointing east. In what direction is the magnetic force?
> **Answer:** $\vec{F}=q\vec{v}\times\vec{B}$. $\hat{j}\times\hat{i}=-\hat{k}$ (downward). Force is downward.

**Q64.** `[P]` An electron moves at $v=2\times10^6\text{m/s}$ perpendicular to a magnetic field $B=0.5\text{T}$. Find the radius of its circular orbit.
> **Answer:** $r=\frac{mv}{qB}=\frac{(9.11\times10^{-31})(2\times10^6)}{(1.6\times10^{-19})(0.5)}\approx2.28\times10^{-5}\text{m}$.

**Q65.** `[P]` A long straight wire carries $5\text{A}$. Find $B$ at a distance of $10\text{cm}$.
> **Answer:** $B=\frac{\mu_0 I}{2\pi r}=\frac{4\pi\times10^{-7}\times5}{2\pi\times0.1}=10^{-5}\text{T}=10\mu\text{T}$.

**Q66.** `[P]` Two parallel wires $0.04\text{m}$ apart carry $3\text{A}$ and $5\text{A}$ in the same direction. Find the force per unit length between them. Attractive or repulsive?
> **Answer:** $F/L=\frac{\mu_0 I_1 I_2}{2\pi d}=\frac{4\pi\times10^{-7}\times15}{2\pi\times0.04}=7.5\times10^{-5}\text{N/m}$. Attractive (same direction currents attract).

**Q67.** `[CT]` A circular current loop of radius $R$ carries current $I$. Derive the expression for the magnetic field at the center.
> **Answer:** Each element $dl$ contributes $dB=\frac{\mu_0 I dl}{4\pi R^2}$. Integrate over circumference $2\pi R$: $B=\frac{\mu_0 I}{2R}$.

**Q68.** `[N]` The Hall Effect: A current-carrying conductor is placed in a magnetic field perpendicular to the current. Explain what Hall voltage develops and how to determine the sign of the charge carriers.
> **Answer:** Moving charges accumulate on one side, creating an electric field $E_H=v_d B$ (drift speed times B). Hall voltage $V_H=E_H w=v_d Bw$ (width $w$). The sign of $V_H$ depends on whether charge carriers are positive (conventional current) or negative (electrons), allowing carrier sign determination.

---

### Topic 10: Electromagnetic Induction

**Q69.** `[C]` State Faraday's Law and Lenz's Law. How does Lenz's Law follow from energy conservation?
> **Answer:** Faraday: $\varepsilon=-d\Phi_B/dt$. Lenz: Induced current opposes the change in flux. Lenz's Law follows from energy conservation: if the induced current aided flux change, it would amplify itself indefinitely (violating energy conservation).

**Q70.** `[P]` A rectangular loop ($0.2\text{m}\times0.3\text{m}$) is in a uniform field $B=0.5\text{T}$. The field drops to zero in $0.01\text{s}$. Find the induced EMF.
> **Answer:** $|\varepsilon|=\Delta\Phi_B/\Delta t=(0.5\times0.06)/0.01=3\text{V}$.

**Q71.** `[P]` A conducting rod of length $0.4\text{m}$ moves at $5\text{m/s}$ perpendicular to a $0.8\text{T}$ magnetic field. Find the motional EMF.
> **Answer:** $\varepsilon=BLv=0.8(0.4)(5)=1.6\text{V}$.

**Q72.** `[CT]` An inductor $L=50\text{mH}$ carries current $I_0=2\text{A}$. The current drops to zero in $0.1\text{s}$. Find the induced EMF.
> **Answer:** $\varepsilon=-L\frac{dI}{dt}=-0.05\times\frac{0-2}{0.1}=1\text{V}$.

**Q73.** `[N]` A generator rotates a coil ($N$ turns, area $A$) at angular speed $\omega$ in field $B$. Derive the output EMF as a function of time.
> **Answer:** $\Phi=NBA\cos(\omega t)$. $\varepsilon=-d\Phi/dt=NBA\omega\sin(\omega t)$. The maximum EMF is $\varepsilon_0=NBA\omega$.

---

### Topic 11: Thermodynamics

**Q74.** `[C]` State the four laws of thermodynamics (zeroth through third) in plain language.

**Q75.** `[P]` An ideal gas at $300\text{K}$ and $1\text{atm}$ occupies $2\text{L}$. It is compressed adiabatically to $1\text{L}$. Find the new pressure. ($\gamma=5/3$)
> **Answer:** $P_1V_1^\gamma=P_2V_2^\gamma \implies P_2=P_1(V_1/V_2)^\gamma=1(2)^{5/3}\approx3.17\text{atm}$.

**Q76.** `[P]` $1\text{mol}$ of ideal monatomic gas expands isothermally at $400\text{K}$ from $V_1=0.01\text{m}^3$ to $V_2=0.04\text{m}^3$. Calculate $Q$, $W$, and $\Delta U$.
> **Answer:** $\Delta U=0$ (isothermal ideal gas). $W=nRT\ln(V_2/V_1)=8.314(400)\ln(4)=4608\text{J}$. $Q=W=4608\text{J}$.

**Q77.** `[P]` A heat engine takes in $Q_H=1200\text{J}$ and expels $Q_C=800\text{J}$. Find its efficiency and compare to the Carnot efficiency between $T_H=600\text{K}$ and $T_C=400\text{K}$.
> **Answer:** $e=W/Q_H=(Q_H-Q_C)/Q_H=400/1200=33.3\%$. $e_C=1-T_C/T_H=1-2/3=33.3\%$. It achieves Carnot efficiency (ideal).

**Q78.** `[CT]` Show that entropy is a state function for a reversible Carnot cycle by computing $\oint dQ/T$.
> **Answer:** For a Carnot cycle: $\Delta S_{hot}=-Q_H/T_H$ and $\Delta S_{cold}=Q_C/T_C$. For a Carnot engine, $Q_H/T_H=Q_C/T_C$, so total $\oint dS=0$.

**Q79.** `[CT]` A refrigerator uses $500\text{W}$ of power to extract heat from a $-10°\text{C}$ interior and deposit it in a $25°\text{C}$ environment. What is the maximum rate of heat extraction from the interior?
> **Answer:** Max COP $=T_C/(T_H-T_C)=263/(298-263)=263/35\approx7.5$. $\dot{Q}_C=\text{COP}\times W=7.5\times500=3750\text{W}$.

**Q80.** `[N]` Why does entropy always increase for an irreversible process? Give a molecular-level explanation.
> **Answer:** Irreversible processes move a system toward macrostates with more microstates (greater disorder). The probability of a spontaneous transition from high to low multiplicity (entropy decrease) is astronomically small for large systems. Statistically, systems always evolve toward higher entropy.

---

## Intro Quantum Physics

### Topic 12: Wave-Particle Duality and Photoelectric Effect

**Q81.** `[C]` Explain the wave-particle duality of light. What experimental evidence supports each aspect?
> **Answer:** Wave: diffraction and interference (Young's double-slit, gratings). Particle: photoelectric effect and Compton scattering.

**Q82.** `[P]` UV light ($\lambda=150\text{nm}$) hits a metal with work function $\Phi=4.0\text{eV}$. Find the stopping voltage.
> **Answer:** $E=hc/\lambda=1240\text{eV nm}/150\text{nm}=8.27\text{eV}$. $K_{max}=8.27-4.0=4.27\text{eV}$. Stopping voltage $=4.27\text{V}$.

**Q83.** `[P]` Find the threshold wavelength for photoelectric emission from tungsten ($\Phi=4.5\text{eV}$).
> **Answer:** $\lambda_0=hc/\Phi=1240\text{eV nm}/4.5\text{eV}\approx276\text{nm}$.

**Q84.** `[P]` Calculate the de Broglie wavelength of a $1\text{kg}$ ball thrown at $10\text{m/s}$.
> **Answer:** $\lambda=h/(mv)=6.626\times10^{-34}/(1\times10)=6.626\times10^{-35}\text{m}$. Negligibly small compared to any macroscopic object.

**Q85.** `[CT]` In the Compton effect, a photon of wavelength $\lambda_0$ scatters off an electron at angle $\theta$. Derive the Compton shift formula.
> **Answer:** Apply conservation of energy and momentum. Result: $\Delta\lambda=\lambda'-\lambda_0=\frac{h}{m_e c}(1-\cos\theta)$, where $h/m_e c\approx2.43\text{pm}$ is the Compton wavelength.

**Q86.** `[N]` If the photoelectric effect threshold frequency is $f_0$, and light of frequency $2f_0$ is used, the maximum kinetic energy of emitted electrons is $K_1$. If frequency $3f_0$ is used, what is the maximum kinetic energy $K_2$?
> **Answer:** $K_1=h(2f_0)-hf_0=hf_0$. $K_2=h(3f_0)-hf_0=2hf_0=2K_1$.

---

### Topic 13: Schrödinger Equation and Quantum Systems

**Q87.** `[C]` What is the physical interpretation of $|\psi(x)|^2$?
> **Answer:** $|\psi(x)|^2$ is the probability density: the probability of finding the particle in an interval $[x, x+dx]$ is $|\psi(x)|^2 dx$.

**Q88.** `[P]` For a particle in a 1D box of length $L$, write the normalized wavefunction for the $n$-th state.
> **Answer:** $\psi_n(x)=\sqrt{\frac{2}{L}}\sin\left(\frac{n\pi x}{L}\right)$ for $0 \le x \le L$, and $0$ elsewhere.

**Q89.** `[P]` An electron is in the $n=3$ state of a $1\text{nm}$ box. What is its energy?
> **Answer:** $E_3=\frac{9h^2}{8m_e L^2}=9E_1=9\times0.376\text{eV}\approx3.39\text{eV}$.

**Q90.** `[P]` For the ground state of a 1D box, find the probability of finding the particle in the middle third ($L/3 \le x \le 2L/3$).
> **Answer:** $P=\int_{L/3}^{2L/3}\frac{2}{L}\sin^2(\pi x/L)dx=\frac{2}{L}\cdot\frac{L}{3}+\frac{1}{\pi}\sin(2\pi/3)=\frac{2}{3}+\frac{\sqrt{3}}{2\pi}\approx0.789$.

**Q91.** `[CT]` The uncertainty principle: An electron is confined to a nucleus of diameter $10^{-14}\text{m}$. Estimate its minimum kinetic energy.
> **Answer:** $\Delta x\approx10^{-14}\text{m}$. $\Delta p\ge\hbar/(2\Delta x)\approx5.27\times10^{-21}\text{kg m/s}$. $K\approx(\Delta p)^2/(2m_e)\approx1.52\times10^{-11}\text{J}\approx95\text{MeV}$. This energy far exceeds what the nuclear force can supply, showing electrons cannot be confined in nuclei.

**Q92.** `[CT]` Calculate the wavelength of light emitted when a hydrogen atom transitions from $n=4$ to $n=2$.
> **Answer:** $1/\lambda=R_H(1/4-1/16)=R_H\times3/16$. $R_H=1.097\times10^7\text{m}^{-1}$. $\lambda=16/(3\times1.097\times10^7)=486\text{nm}$ (blue-green Balmer series).

**Q93.** `[N]` Explain why quantization of energy levels arises naturally from boundary conditions on the wavefunction.
> **Answer:** For an infinite square well, $\psi$ must be zero at the walls (boundary conditions). The only sinusoidal solutions satisfying this are $\psi\propto\sin(n\pi x/L)$, meaning the wavelength must fit an integer number of half-wavelengths. Through $p=h/\lambda$ and $E=p^2/(2m)$, this forces discrete energy levels.

**Q94.** `[N]` Compare the quantum mechanical result for a particle in a box to the classical prediction. For very large $n$, how do they relate?
> **Answer:** Classically, the probability of finding the particle is uniform: $P=1/L$. Quantum mechanically, $P(x)=\frac{2}{L}\sin^2(n\pi x/L)$. For large $n$, the rapidly oscillating $\sin^2$ averages to $1/L$ over macroscopic scales — the correspondence principle: quantum mechanics reduces to classical mechanics in the limit of large quantum numbers.

**Q95.** `[CT]` The quantum harmonic oscillator has energy levels $E_n=(n+1/2)\hbar\omega$. What is the significance of the $1/2\hbar\omega$ zero-point energy, and how is it related to the uncertainty principle?
> **Answer:** Even in the ground state ($n=0$), the particle has energy $\hbar\omega/2$. This is required by the uncertainty principle: if the particle were at rest at $x=0$, both $\Delta x=0$ and $\Delta p=0$, violating $\Delta x\Delta p\ge\hbar/2$. The zero-point energy represents the minimum kinetic energy required by the uncertainty principle.

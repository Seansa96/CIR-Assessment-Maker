from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
import os, math

OUT = os.path.join(os.path.dirname(__file__), '..', 'output', 'pdf', 'Conceptual Notes.pdf')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, H = letter
NAVY = HexColor('#17324D'); TEAL = HexColor('#137C8B'); GOLD = HexColor('#D9942A')
INK = HexColor('#203040'); PALE = HexColor('#EAF3F5'); PALE2 = HexColor('#F7F2E8'); MUTED = HexColor('#667786')

pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))
styles = getSampleStyleSheet()
body = ParagraphStyle('body', parent=styles['BodyText'], fontName='Arial', fontSize=8.6, leading=10.3, textColor=INK, spaceAfter=2.5)
small = ParagraphStyle('small', parent=body, fontSize=7.2, leading=8.4, textColor=MUTED)
eq = ParagraphStyle('eq', parent=body, fontName='Arial-Bold', fontSize=9.2, leading=11.0, alignment=TA_CENTER, textColor=NAVY)
caption = ParagraphStyle('caption', parent=small, fontSize=6.8, leading=8.0, alignment=TA_CENTER, textColor=MUTED)

def clean_symbols(text):
    replacements = {
        '⃗':'', '∮':'∫', '∇':'grad', '∂':'d', 'Δ':'d', 'ₓ':'x', 'ₜ':'t', 'r̂':'r̂',
    }
    for sub, digit in zip('₀₁₂₃₄₅₆₇₈₉', '0123456789'):
        replacements[sub] = f'<sub>{digit}</sub>'
    for a,b in replacements.items(): text = text.replace(a,b)
    return text

sections = [
('01  ELECTRIC FORCE, FIELDS, AND CONSERVATION', [
 'Charge is a property of matter: electrons carry negative charge, protons positive charge, and charge is conserved in every isolated interaction.',
 'Coulomb force is central and inverse-square: <b>F = k|q<sub>1</sub>q<sub>2</sub>|/r<sup>2</sup></b>. Like charges repel; unlike charges attract along the line joining them.',
 'The electric field is the force a tiny positive test charge would feel: <b>E = F/q</b>. The field exists whether or not a test charge is present.',
 'For a positive source charge, E points away; for a negative source charge, E points toward. The force on a negative test charge is opposite E.',
 'Electric and gravitational fields share the inverse-square pattern, but gravity is always attractive while electric force can attract or repel.',
 'A field diagram is a map of direction and relative strength: lines never cross, crowding means larger magnitude, and arrows show the force on positive charge.',
 'Conservation-law thinking is a fast check: charge can move between objects, but the algebraic total before and after remains fixed.',
 'Units: force is newtons, charge coulombs, field N/C (equivalently V/m). Keep source charge and test charge roles distinct.',
], '<b>Hallmark:</b>  F⃗ = qE⃗   &nbsp;&nbsp; and &nbsp;&nbsp; F⃗<sub>12</sub> = k q<sub>1</sub>q<sub>2</sub>/r<sup>2</sup> r̂'),
('02  SUPERPOSITION, VECTORS, DISTRIBUTIONS, AND DIPOLES', [
 'Fields add by superposition: calculate each source contribution at the same observation point, resolve into components, then add vectors—not magnitudes.',
 'Symmetry can cancel components. At the midpoint of equal like charges, horizontal components cancel; between opposite charges, the fields reinforce in one direction.',
 'For many point charges, <b>E⃗ = Σ kq<sub>i</sub>r̂<sub>i</sub>/r<sub>i</sub><sup>2</sup></b>. Draw a local coordinate system before substituting numbers.',
 'A continuous distribution replaces the sum with an integral: dq = λdx for a line, σdA for a surface, or ρdV for a volume.',
 'An electric dipole is two equal opposite charges separated by distance d. Its dipole moment p⃗ points from negative to positive charge.',
 'Far from a dipole, field strength falls faster than a single-charge field because opposite contributions nearly cancel; direction depends strongly on location.',
 'Field vectors point tangent to field lines. At a point, use the geometry of the source arrangement to anticipate zeroes, maxima, and limiting behavior.',
 'A reliable workflow is: sketch → choose axes → write each vector → project → sum → check units and the limiting case r → ∞.',
], '<b>Dipole idea:</b>  p⃗ = qd⃗  &nbsp;&nbsp; ; far-field scale  E ∝ p/r<sup>3</sup>'),
('03  CONDUCTORS AND ELECTROSTATIC EQUILIBRIUM', [
 'In electrostatic equilibrium, free charges in a conductor have stopped drifting. Therefore the electric field inside the conducting material is zero.',
 'If an internal field remained, mobile charges would accelerate. They rearrange on the surface until their own field cancels the applied field in the metal.',
 'The conductor is an equipotential: if two points had different V, tangential electric forces would drive surface charge along the conductor.',
 'At a surface, E has no tangential component and points perpendicular to the conductor. Just outside, <b>E<sub>⊥</sub> = σ/ε<sub>0</sub></b>.',
 'Charge placed on an isolated conductor resides on the outer surface unless a cavity contains charge. In a cavity, induced inner-surface charge balances the enclosed charge.',
 'Electrostatic shielding follows from the zero interior field: a conducting enclosure protects its interior from external static fields, provided the geometry is closed.',
 'Sharp points accumulate surface charge more densely, producing stronger nearby fields and enabling corona discharge or lightning-rod action.',
 'For conductor questions, identify the material region, cavity, and exterior first; apply Gauss’s law only after the equilibrium constraints are stated.',
], '<b>Surface condition:</b>  E<sub>inside metal</sub> = 0 &nbsp;&nbsp; ; &nbsp;&nbsp; E<sub>just outside</sub> = σ/ε<sub>0</sub>'),
('04  GAUSS’S LAW AND GAUSSIAN-SURFACE SYMMETRY', [
 'Electric flux measures how much field passes through a surface: <b>Φ<sub>E</sub> = ∮ E⃗·dA⃗</b>. The area vector points outward for a closed surface.',
 'Gauss’s law says total outward flux equals enclosed charge divided by ε<sub>0</sub>. Charges outside the surface can alter local field but contribute zero net flux.',
 'The law is always true, but it becomes a shortcut only when symmetry makes E constant in magnitude and direction over useful parts of the surface.',
 'Choose a Gaussian sphere for spherical symmetry, cylinder for an infinite line, and pillbox for an infinite plane or conductor surface.',
 'The surface is imaginary; it is chosen to match the field geometry, not to follow the physical boundary of the charged object.',
 'On a surface where E is constant and perpendicular, Φ = EA. Where E is tangent, E⃗·dA⃗ = 0. Where E varies, integrate or use smaller elements.',
 'Flux is signed: outward field gives positive contribution, inward field negative. Zero net flux does not mean zero field everywhere.',
 'The key physical thought is “count field lines in aggregate”: enclosed charge is the source of net field-line excess through a closed boundary.',
], '<b>Gauss:</b>  ∮ E⃗·dA⃗ = Q<sub>enc</sub>/ε<sub>0</sub>'),
('05  APPLICATIONS OF GAUSS’S LAW', [
 'For an infinite line with linear density λ, use a coaxial cylinder of radius r and length L. Only the curved side contributes: Φ = E(2πrL).',
 'The enclosed charge is λL, so <b>E = λ/(2πε<sub>0</sub>r)</b>. The 1/r dependence reflects cylindrical spreading rather than spherical spreading.',
 'For a spherical shell or point-like spherical distribution, use a Gaussian sphere. Outside, the field is the same as if all net charge were concentrated at the center.',
 'Inside a uniformly charged solid sphere, Q<sub>enc</sub> grows with r<sup>3</sup> while area grows with r<sup>2</sup>, giving E ∝ r.',
 'For a nonuniform sphere, compute Q<sub>enc</sub>(r) = ∫ρ(r′)dV before applying Gauss’s law. Do not substitute total charge inside the interior surface.',
 'A conducting shell has E = 0 in the metal. A Gaussian surface in the metal then forces the enclosed algebraic charge to be zero.',
 'Outside a charged conductor, spherical symmetry is required before replacing the object with a point charge; arbitrary shapes need not have a radial field.',
 'Always state the region—inside, within metal, cavity, or outside—because the enclosed charge and symmetry can change at each boundary.',
], '<b>Line charge result:</b>  E(r) = λ/(2πε<sub>0</sub>r) &nbsp;&nbsp; ; &nbsp;&nbsp; <b>solid sphere:</b> E = ρr/(3ε<sub>0</sub>)'),
('06  ELECTRIC POTENTIAL AND ENERGY', [
 'Potential V is electric potential energy per unit charge. It is a scalar, so contributions from multiple charges add algebraically instead of vectorially.',
 'A potential difference measures work per charge: <b>ΔV = −∫ E⃗·dℓ⃗</b>. A positive charge naturally moves toward lower potential when released.',
 'For a point charge, V = kq/r with V = 0 chosen at infinity. Positive q produces positive V; negative q produces negative V.',
 'Electric potential energy is U = qV. The sign of q matters: a negative charge can lose U while moving toward higher V.',
 'The electric field points in the direction of decreasing potential. In one dimension, E<sub>x</sub> = −dV/dx; a steep potential graph means a strong field.',
 'Equipotential surfaces have constant V, so moving along one requires no electric work and E is perpendicular to the surface.',
 'Use potential for energy and geometry problems; use field for force and acceleration. They describe the same interaction from complementary viewpoints.',
 'Checks: voltage is joules per coulomb, field is volts per metre, and potential must become nearly uniform far from a localized charge distribution.',
], '<b>Field–potential link:</b>  E⃗ = −∇V &nbsp;&nbsp; ; &nbsp;&nbsp; ΔU = qΔV'),
('07  SIMPLE HARMONIC MOTION', [
 'Simple harmonic motion occurs when the restoring force is proportional to displacement and opposite in direction: <b>F = −kx</b>.',
 'For a mass-spring oscillator, Newton’s law gives mx″ = −kx, so ω = √(k/m), T = 2π/ω, and f = 1/T.',
 'The amplitude A is the maximum displacement; it sets the energy but not the period in ideal linear SHM. Phase tells where the cycle begins.',
 'A convenient model is x(t) = A cos(ωt + φ). Then v is shifted by a quarter cycle and acceleration is opposite x.',
 'At turning points, x = ±A, speed is zero, and spring energy is maximum. At equilibrium, x = 0, speed is maximum, and kinetic energy is maximum.',
 'The graphs of x, v, and a are sinusoids with the same period: v leads x by 90°, while a is 180° out of phase with x.',
 'A phasor is a rotating-radius picture whose horizontal projection gives x(t). It turns phase comparisons into geometry.',
 'Energy conservation provides a robust check: E = ½kx<sup>2</sup> + ½mv<sup>2</sup> = ½kA<sup>2</sup> for an undamped oscillator.',
], '<b>SHM:</b>  x″ + ω<sup>2</sup>x = 0 &nbsp;&nbsp; ; &nbsp;&nbsp; ω = √(k/m) &nbsp;&nbsp; ; &nbsp;&nbsp; E = ½kA<sup>2</sup>'),
('08  TRAVELING WAVES AND THE LINEAR WAVE EQUATION', [
 'A traveling wave is a pattern that moves while the medium’s particles oscillate locally. Energy travels with the disturbance; matter usually oscillates about equilibrium.',
 'A right-moving shape is written <b>y(x,t) = f(x − vt)</b>; the minus sign makes a fixed feature occur at larger x as time increases.',
 'For a sinusoid, y = A cos(kx − ωt + φ), where k = 2π/λ, ω = 2πf, and v = ω/k = fλ.',
 'Phase compares locations in the cycle. Points separated by λ are in phase; separation λ/2 means opposite displacement for a sinusoid.',
 'Transverse waves oscillate perpendicular to travel; longitudinal waves oscillate parallel to travel, producing compressions and rarefactions.',
 'The linear wave equation follows from local restoring forces plus inertia: each small element accelerates according to the curvature of its neighbors.',
 'For a string, tension T and linear density μ give v = √(T/μ). Greater tension speeds the wave; greater mass per length slows it.',
 'The linear approximation assumes small slopes and independent superposition. Large amplitudes, nonlinear media, or strong dispersion can break the simple model.',
], '<b>Wave equation:</b>  ∂²y/∂x² = (1/v²) ∂²y/∂t² &nbsp;&nbsp; ; &nbsp;&nbsp; v = fλ'),
('09  REFLECTION, REFRACTION, AND SNELL’S LAW', [
 'Reflection reverses the direction component normal to a boundary while preserving the tangential component. The angle of incidence equals the angle of reflection.',
 'Refraction occurs when wave speed changes across an interface. Frequency is fixed by the source, so wavelength changes according to λ = v/f.',
 'Huygens’ principle treats every point on a wavefront as a source of secondary wavelets. Their envelope predicts the next wavefront and its changed direction.',
 'At an interface, phase must match along the boundary. The tangential wavelength component is therefore continuous, leading to n<sub>1</sub>sinθ<sub>1</sub> = n<sub>2</sub>sinθ<sub>2</sub>.',
 'The refractive index is n = c/v. Entering a slower medium bends the ray toward the normal; entering a faster medium bends it away.',
 'A derivation strategy is geometric: compare equal travel times along the interface, substitute v = c/n, and rearrange the sine ratio.',
 'Reflection and refraction can coexist. The amount of transmitted versus reflected energy depends on the boundary and wave properties.',
 'Watch the angle convention: θ is measured from the normal, not from the surface. Frequency does not jump at the boundary.',
], '<b>Snell:</b>  n<sub>1</sub>sinθ<sub>1</sub> = n<sub>2</sub>sinθ<sub>2</sub> &nbsp;&nbsp; ; &nbsp;&nbsp; f<sub>1</sub> = f<sub>2</sub>'),
('10  SOUND, NOISE, PRESSURE LEVEL, AND SPECTRUM', [
 'Sound is a mechanical disturbance of matter. In air it is primarily longitudinal: oscillating molecules create alternating compressions and rarefactions.',
 'A pure tone has one dominant frequency; noise contains many frequencies with irregular phase and amplitude. A spectrum displays amplitude versus frequency.',
 'Sound pressure variation Δp is the pressure oscillation around atmospheric pressure. Larger pressure amplitude generally means greater perceived loudness.',
 'Intensity is average power per area and, for a sinusoidal sound, scales with pressure amplitude squared. Spherical spreading reduces intensity with distance.',
 'Sound-pressure level uses a logarithm: <b>β = 10 log<sub>10</sub>(I/I<sub>0</sub>)</b> dB. A tenfold intensity ratio changes level by 10 dB.',
 'The reference intensity I<sub>0</sub> is a conventional threshold, so decibels compare ratios rather than absolute linear amounts.',
 'Harmonics are integer multiples of a fundamental frequency. Their relative amplitudes help distinguish instruments and sources with the same pitch.',
 'Frequency determines pitch, amplitude relates to loudness, and waveform/spectrum determines timbre. Do not confuse frequency with propagation speed.',
 'For a wave in a medium, sound speed depends on the medium’s stiffness and inertia; temperature and material properties matter more than source loudness.',
], '<b>Level:</b>  β = 10 log<sub>10</sub>(I/I<sub>0</sub>) &nbsp;&nbsp; ; &nbsp;&nbsp; I ∝ (Δp)<sup>2</sup>'),
('11  ATOMIC MODELS, IONS, AND MOLECULES', [
 'Bohr’s model places a compact nucleus at the center and treats electrons as occupying allowed energy states rather than arbitrary radii. It is a useful bridge between classical force ideas and quantization.',
 'For hydrogen, the inward electric attraction supplies centripetal force: <b>k e<sup>2</sup>/r<sup>2</sup> = m<sub>e</sub>v<sup>2</sup>/r</b>. This balance predicts the speed needed for circular motion at a chosen radius.',
 'The quantum model replaces definite electron orbits with an electron cloud: a probability map for where an electron is likely to be found. Darker or denser regions indicate greater probability, not a solid smear of charge.',
 'Ionization means supplying enough energy to remove a bound electron. The atom becomes a positive ion because it has more protons than electrons; the escaped electron is free.',
 'Atoms tend to gain or lose valence-shell electrons to reach a more stable outer configuration. Alkali metals commonly form Na<sup>+</sup> or K<sup>+</sup>; chlorine commonly forms Cl<sup>−</sup>.',
 'A molecule is a bonded collection of atoms: H<sub>2</sub>, N<sub>2</sub>, and CO are diatomic; H<sub>2</sub>O and CO<sub>2</sub> are triatomic. The formula counts atoms, not net charge.',
 'In multi-electron atoms, each electron feels attraction toward the positive nucleus and repulsion from the other electrons. The net force is a vector sum, so simple one-electron circular pictures are only approximations.',
], '<b>Bohr force balance:</b>  k e<sup>2</sup>/r<sup>2</sup> = m<sub>e</sub>v<sup>2</sup>/r &nbsp;&nbsp; ; &nbsp;&nbsp; ionization: bound electron + energy → free electron + positive ion'),
('12  DIELECTRICS, POLARIZATION, AND DISPLACEMENT', [
 'A microscopic electric dipole consists of equal and opposite charges separated by vector d. Its dipole moment is <b>p = qd</b>, directed from negative charge to positive charge.',
 'A dielectric is an insulating material whose molecules can shift or rotate slightly in an applied field. The material does not conduct freely, but its internal charge separation changes the macroscopic field.',
 'Polarization P is the net dipole moment per volume: <b>P = (1/V)Σp<sub>i</sub></b>. Random dipoles can give nearly zero P; alignment produces a nonzero vector.',
 'The displacement field separates the response of free charge from material polarization: <b>D = ε<sub>0</sub>E + P</b>. In free space P = 0, so D = ε<sub>0</sub>E.',
 'For a linear, isotropic dielectric, polarization is proportional to the applied field: <b>P = ε<sub>0</sub>χ<sub>e</sub>E</b>. Susceptibility χ<sub>e</sub> is dimensionless and measures how easily the material polarizes.',
 'Substitution gives D = ε<sub>0</sub>(1+χ<sub>e</sub>)E = εE, where ε is the material permittivity. This constitutive relation is a model assumption, not a universal law for every material or field strength.',
 'Keep free charge, bound charge, E, P, and D conceptually distinct. E is the physical electric field; P describes dipole response; D is a bookkeeping field especially useful with free charge.',
], '<b>Dielectric chain:</b>  p = qd &nbsp; ; &nbsp; P = (1/V)Σp<sub>i</sub> &nbsp; ; &nbsp; D = ε<sub>0</sub>E + P = εE'),
('13  POINT-CHARGE, IONIC, AND MOLECULAR POTENTIALS', [
 'Electric potential energy tells whether a configuration is energetically favorable. For two point charges, <b>U(r) = kq<sub>1</sub>q<sub>2</sub>/r</b>, with zero chosen at infinite separation.',
 'Like charges give positive U and resist being brought together; opposite charges give negative U and lower their energy as they approach. The sign is a statement about energy, not a separate force direction rule.',
 'Force is the negative slope of the potential-energy curve: <b>F(r) = −dU/dr</b>. A steep slope means a large force; at a minimum, the slope is zero and the configuration is in equilibrium.',
 'Real ions such as Na<sup>+</sup> and Cl<sup>−</sup> are composite particles containing nuclei and electrons. Treating them as point charges is a useful far-field approximation, not a literal description at arbitrarily small r.',
 'The Lennard–Jones form <b>U = C<sub>12</sub>/r<sup>12</sup> − C<sub>6</sub>/r<sup>6</sup></b> models short-range repulsion and longer-range attraction between neutral particles.',
 'At very small separation the repulsive term dominates; at intermediate separation the attractive term can create a potential well; far away both terms vanish and U approaches zero.',
 'For ionic solids or salts, a Coulomb term plus a steep repulsive term gives a Mie-type model. The exact constants depend on the interacting species and chosen approximation.',
], '<b>Potential–force link:</b>  F(r) = −dU/dr &nbsp;&nbsp; ; &nbsp;&nbsp; U<sub>LJ</sub> = C<sub>12</sub>/r<sup>12</sup> − C<sub>6</sub>/r<sup>6</sup>'),
]

derivations = [
('From Coulomb force to field', 'Start with F = kqQ/r². Divide by the test charge q: E = F/q = kQ/r². The test charge disappears, showing that E belongs to the source arrangement. Restore direction with r̂, so E = kQ r̂/r².'),
('Superposition and a continuous charge', 'For separated pieces, E = Σ ΔEᵢ. Let the pieces become infinitesimal: Δq → dq and Σ → ∫. With dq = λ dl, σ dA, or ρ dV, E = k ∫ (dq/r²) r̂. Geometry determines the component integrals.'),
('Why a conductor has E = 0 inside', 'Assume a nonzero field in the metal. Free charge would feel F = qE and keep moving, contradicting equilibrium. Charge therefore rearranges until the interior field cancels. A Gaussian surface wholly inside the metal then has ∫E dot dA = 0, so Qenc = 0.'),
('Gauss law from a spherical field', 'For a point charge, E = kQ/r² and dA is radial, so ∫ E dot dA = E∫dA = (kQ/r²)(4πr²) = 4πkQ = Q/ε₀ because k = 1/(4πε₀). The same flux result extends to any closed surface.'),
('Uniform solid sphere, inside and outside', 'Inside radius r, Qenc = ∫₀ʳ ρ(4πr′²)dr′ = 4πρr³/3. Gauss gives E(4πr²) = Qenc/ε₀, hence E = ρr/(3ε₀). Outside, replace r by R in Qtotal, giving E = kQtotal/r².'),
('Why E = −∇V', 'Work by the field is dW = F dot dℓ = qE dot dℓ. Since dU = −dW and dU = qdV, qdV = −qE dot dℓ. Cancel q: dV = −E dot dℓ. Component-by-component, Eₓ = −∂V/∂x, etc., which combine as E = −∇V.'),
('Mass-spring SHM', 'Hooke’s law gives F = −kx. Newton’s second law gives mx″ = −kx. Divide by m and define ω² = k/m: x″ + ω²x = 0. A cosine satisfies this because d²[cos(ωt)]/dt² = −ω²cos(ωt).'),
('Linear wave equation', 'For y = A cos(kx − ωt), differentiating twice gives yₓₓ = −k²y and yₜₜ = −ω²y. Therefore yₓₓ = (k²/ω²)yₜₜ = (1/v²)yₜₜ because v = ω/k. The equation encodes equal propagation speed in both directions.'),
('Snell law from phase matching', 'During the same time interval, wavefronts advance v₁dt and v₂dt. Matching phase along the boundary makes the tangential distances equal: v₁dt sinθ₁ = v₂dt sinθ₂. Cancel dt and use n = c/v: sinθ₁/sinθ₂ = v₂/v₁ = n₁/n₂, so n₁sinθ₁ = n₂sinθ₂.'),
('Sound level and intensity', 'Intensity is power per area: I = P/A. A spherical wave spreads over A = 4πr², so I₂/I₁ = r₁²/r₂². Define level relative to I₀ by β = 10 log₁₀(I/I₀). A tenfold intensity ratio therefore adds 10 dB.'),
('Bohr balance and ionization', 'For a one-electron atom, set the electric attraction equal to the required centripetal force: ke²/r² = mₑv²/r. This does not by itself create the quantum model; quantization restricts which states are allowed. Ionization then means adding enough energy to move the electron from a bound state to an unbound state, leaving a positive ion.'),
('From dipoles to D = εE', 'Start with one dipole p = qd. Sum all microscopic dipoles in volume V and divide by V to obtain P = (1/V)Σpᵢ. Define D = ε₀E + P. For a linear isotropic material insert P = ε₀χₑE, factor ε₀E, and define ε = ε₀(1+χₑ), giving D = εE.'),
('Reading an interaction-potential graph', 'Plot U against separation r. The point-charge term varies as 1/r; additional short-range physics can create a steep positive wall and an attractive negative well. Differentiate the curve conceptually: negative slope means positive radial force under the chosen outward coordinate, positive slope means inward force, and a horizontal minimum gives F = 0.'),
]

def p(c, text, x, y, w, h, style=body):
    q = Paragraph(clean_symbols(text), style); _, hh = q.wrap(w, h); q.drawOn(c, x, y-hh); return hh

def footer(c, num, total):
    c.setStrokeColor(HexColor('#D7E0E4')); c.setLineWidth(.5); c.line(.55*inch,.43*inch,W-.55*inch,.43*inch)
    c.setFont('Helvetica',7); c.setFillColor(MUTED); c.drawString(.58*inch,.25*inch,'Conceptual Notes  |  Physics 2 Test 1'); c.drawRightString(W-.58*inch,.25*inch,f'{num} / {total}')

def diagram(c, idx, x, y, w, h):
    c.setStrokeColor(TEAL); c.setFillColor(PALE); c.setLineWidth(1.2)
    cx=x+w*.52; cy=y+h*.52
    if idx==0:
        for r in [18,30,42,54]:
            c.circle(cx,cy,r,stroke=1,fill=0)
        c.setFillColor(GOLD); c.circle(cx,cy,9,stroke=0,fill=1); c.setFillColor(NAVY); c.setFont('Helvetica-Bold',8); c.drawCentredString(cx,cy-3,'+q')
        for a in range(0,360,45):
            ax=cx+54*math.cos(math.radians(a)); ay=cy+54*math.sin(math.radians(a)); c.line(cx+12*math.cos(math.radians(a)),cy+12*math.sin(math.radians(a)),ax,ay)
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawCentredString(cx,y+8,'field direction from a positive source')
    elif idx==1:
        c.setFillColor(GOLD); c.circle(cx-35,cy,8,stroke=0,fill=1); c.setFillColor(TEAL); c.circle(cx+35,cy,8,stroke=0,fill=1)
        c.setStrokeColor(TEAL); c.line(cx-27,cy,cx+27,cy)
        for r in [18,30,42]: c.arc(cx-35-r,cy-r, cx-35+r,cy+r, startAng=40, extent=280); c.arc(cx+35-r,cy-r,cx+35+r,cy+r,startAng=220,extent=280)
        c.setFillColor(INK); c.setFont('Helvetica-Bold',8); c.drawCentredString(cx-35,cy-3,'-'); c.drawCentredString(cx+35,cy-3,'+'); c.setFont('Helvetica',7); c.drawCentredString(cx,y+8,'dipole moment points from - to +')
    elif idx==2:
        c.setStrokeColor(NAVY); c.rect(x+w*.25,y+h*.25,w*.5,h*.5,stroke=1,fill=0); c.setFillColor(GOLD); c.circle(cx,cy,5,stroke=0,fill=1)
        for yy in [cy-25,cy,cy+25]: c.setStrokeColor(TEAL); c.line(x+8,yy,x+w*.25,yy); c.line(x+w*.75,yy,x+w-8,yy)
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawCentredString(cx,y+8,'E = 0 inside metal; surface charge shields')
    elif idx in [3,4]:
        r=min(w,h)*.25; c.setStrokeColor(TEAL); c.circle(cx,cy,r,stroke=1,fill=0); c.setFillColor(GOLD); c.circle(cx,cy,5,stroke=0,fill=1)
        for a in range(0,360,30):
            c.setStrokeColor(TEAL); c.line(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a)),cx+min(w,h)*.46*math.cos(math.radians(a)),cy+min(w,h)*.46*math.sin(math.radians(a)))
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawCentredString(cx,y+8,'Gaussian surface: choose symmetry first')
    elif idx==5:
        c.setStrokeColor(TEAL); c.line(x+15,cy,x+w-15,cy); c.setFillColor(GOLD); c.circle(cx-30,cy,7,stroke=0,fill=1); c.setFillColor(NAVY); c.circle(cx+30,cy,7,stroke=0,fill=1)
        for xx in [x+30,x+60,x+90,x+120]: c.setStrokeColor(HexColor('#97B8C0')); c.line(xx,cy-35,xx,cy+35)
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawCentredString(cx,y+8,'equipotential lines; E points downhill in V')
    elif idx==6:
        c.setStrokeColor(NAVY); c.line(x+20,cy,x+w-20,cy); c.setStrokeColor(TEAL); c.line(cx,cy,cx+35,cy+20); c.circle(cx,cy,35,stroke=1,fill=0); c.setFillColor(GOLD); c.circle(cx+35,cy+20,4,stroke=0,fill=1)
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawCentredString(cx,y+8,'phasor projection gives x(t)')
    elif idx==7:
        c.setStrokeColor(TEAL); c.line(x+10,cy,x+w-10,cy); pts=[]
        for i in range(80):
            xx=x+10+(w-20)*i/79; yy=cy+20*math.sin(2*math.pi*i/79); pts.append((xx,yy))
        c.setStrokeColor(GOLD); c.lines([(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]) for i in range(len(pts)-1)])
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawCentredString(cx,y+8,'a shape translates without changing its form')
    elif idx==8:
        c.setStrokeColor(NAVY); c.line(cx, y+15,cx,y+h-15); c.setStrokeColor(TEAL); c.line(x+20,cy+25,x+w-20,cy-20); c.setStrokeColor(GOLD); c.line(x+20,cy-25,x+w-20,cy+20)
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawCentredString(cx,y+8,'angles are measured from the normal')
    elif idx==9:
        c.setStrokeColor(TEAL); c.line(x+15,y+22,x+w-10,y+22); c.line(x+15,y+22,x+15,y+h-15)
        for i in range(1,6):
            xx=x+15+i*(w-25)/6; c.setFillColor(GOLD if i==2 else NAVY); c.rect(xx,y+22,8,12+8*(i==2),stroke=0,fill=1)
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawCentredString(cx,y+8,'spectrum: amplitude versus frequency')
    if idx==10:
        c.setStrokeColor(NAVY); c.circle(cx,cy,19,stroke=1,fill=0); c.setFillColor(GOLD); c.circle(cx,cy,7,stroke=0,fill=1)
        c.setStrokeColor(TEAL); c.circle(cx,cy,35,stroke=1,fill=0); c.setFillColor(INK); c.setFont('Helvetica',7); c.drawString(x+10,y+10,'nucleus'); c.drawString(x+10,y+h-12,'cloud / allowed levels')
    elif idx==11:
        c.setStrokeColor(TEAL); c.roundRect(x+16,y+22,w-32,h-42,8,stroke=1,fill=0); c.setFillColor(GOLD); c.circle(cx-30,cy,5,stroke=0,fill=1); c.setFillColor(NAVY); c.circle(cx,cy,5,stroke=0,fill=1); c.setStrokeColor(TEAL); c.line(cx-24,cy,cx-6,cy); c.setFillColor(INK); c.setFont('Helvetica',7); c.drawString(x+14,y+8,'aligned dipoles'); c.drawString(x+w-72,y+h-12,'E, P, D →')
    elif idx==12:
        c.setStrokeColor(TEAL); c.line(x+15,y+22,x+w-10,y+22); c.line(x+15,y+22,x+15,y+h-15); pts=[]
        for i in range(90):
            rr=0.45+2.55*i/89; uu=1.2/(rr**12)-2.0/(rr**6); xx=x+15+(w-25)*i/89; yy=max(y+28,min(y+h-22,y+45+uu*10)); pts.append((xx,yy))
        c.setStrokeColor(GOLD); c.lines([(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]) for i in range(len(pts)-1)])
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawString(x+22,y+h-14,'repulsive'); c.drawString(x+w-58,y+31,'attractive well')

c = canvas.Canvas(OUT, pagesize=letter)
c.setTitle('Conceptual Notes')
for page,((title, bullets, equation),(dtitle,dtext)) in enumerate(zip(sections,derivations),1):
    c.setFillColor(NAVY); c.rect(0,H-.34*inch,W,.34*inch,stroke=0,fill=1)
    c.setFillColor(colors.white); c.setFont('Helvetica-Bold',8); c.drawString(.58*inch,H-.23*inch,'CIR ASSESSMENT MAKER  |  STUDY HANDOUT')
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold',15); c.drawString(.58*inch,H-.72*inch,title)
    c.setFillColor(TEAL); c.rect(.58*inch,H-.84*inch,.52*inch,.035*inch,stroke=0,fill=1)
    # left text column
    yy=H-1.05*inch; x=.58*inch; tw=3.95*inch
    for b in bullets:
        h=p(c,'• '+b,x,yy,tw,50,body); yy-=h+2
    # right visual panel
    rx=4.72*inch; ry=4.2*inch; rw=2.18*inch; rh=3.32*inch
    c.setFillColor(PALE); c.roundRect(rx,ry,rw,rh,8,stroke=0,fill=1)
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold',8); c.drawCentredString(rx+rw/2,ry+rh-18,'VISUAL MAP')
    diagram(c,page-1,rx+8,ry+34,rw-16,rh-62)
    # derivation box
    dy=1.48*inch; dh=2.28*inch
    c.setFillColor(PALE2); c.roundRect(.58*inch,dy,W-1.16*inch,dh,6,stroke=0,fill=1)
    c.setFillColor(TEAL); c.setFont('Arial-Bold',8); c.drawString(.75*inch,dy+dh-17,'DERIVATION  |  '+dtitle.upper())
    p(c,dtext,.75*inch,dy+dh-27,W-1.5*inch,dh-.38*inch,body)
    # equation box
    ey=.76*inch; eh=.72*inch
    c.setFillColor(PALE2); c.roundRect(.58*inch,ey,W-1.16*inch,eh,6,stroke=0,fill=1)
    p(c,equation,.72*inch,ey+eh-.12*inch,W-1.44*inch,eh-.14*inch,eq)
    if page==len(sections):
        p(c,'References: Young and Freedman, <i>University Physics</i>, chapters on electrostatics and waves. OpenStax, <i>University Physics Volume 1</i>, Chapters 15–17; <i>University Physics Volume 2</i>, Chapters 5–7. Supplied teacher worksheet scans: Physics 2 scans Test 1.',.62*inch,.59*inch,W-1.24*inch,.2*inch,small)
    footer(c,page,len(sections)); c.showPage()
c.save()
print(OUT)

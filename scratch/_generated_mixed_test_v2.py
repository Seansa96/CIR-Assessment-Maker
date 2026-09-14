from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, math

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..')); OUT=os.path.join(ROOT,'output','pdf'); os.makedirs(OUT,exist_ok=True)
TEST=os.path.join(OUT,'Physics 2 Mixed Conceptual and Procedural Test - Version 2.pdf'); KEY=os.path.join(OUT,'Physics 2 Mixed Conceptual and Procedural Test - Version 2 Detailed Answer Key.pdf')
W,H=letter; NAVY=HexColor('#17324D'); TEAL=HexColor('#137C8B'); GOLD=HexColor('#D9942A'); INK=HexColor('#203040'); PALE=HexColor('#EAF3F5'); CREAM=HexColor('#F7F2E8'); MUTED=HexColor('#667786')
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf')); pdfmetrics.registerFont(TTFont('Arial-Bold',r'C:\Windows\Fonts\arialbd.ttf'))
styles=getSampleStyleSheet(); body=ParagraphStyle('body',fontName='Arial',fontSize=9.1,leading=11.2,textColor=INK); small=ParagraphStyle('small',fontName='Arial',fontSize=8.0,leading=9.5,textColor=INK); eq=ParagraphStyle('eq',fontName='Arial-Bold',fontSize=11,leading=14,textColor=NAVY,alignment=1); keybody=ParagraphStyle('keybody',fontName='Arial',fontSize=8.2,leading=9.7,textColor=INK)
def clean(s):
    for a,b in {'⃗':'','∮':'∫','∇':'grad','∂':'d','Δ':'d','⁺':'+','⁻':'-','²':'2','³':'3','¹':'1','⁶':'6','⁷':'7','⁹':'9','½':'1/2','₀':'<sub>0</sub>','₁':'<sub>1</sub>','₂':'<sub>2</sub>','₃':'<sub>3</sub>','₄':'<sub>4</sub>','ₑ':'<sub>e</sub>','ᵣ':'<sub>r</sub>','ₓ':'<sub>x</sub>','ₜ':'<sub>t</sub>','ᵢ':'<sub>i</sub>','ₙ':'<sub>n</sub>'}.items(): s=s.replace(a,b)
    return s.replace('–','-').replace('—','-').replace('−','-').replace('r<R','r &lt; R').replace('r>R','r &gt; R')
def para(c,s,x,y,w,style=body):
    q=Paragraph(clean(s),style); _,h=q.wrap(w,1000); q.drawOn(c,x,y-h); return h
def header(c,title,page,total,kind='COMPREHENSIVE PHYSICS 2 TEST'):
    c.setFillColor(NAVY); c.rect(0,H-.34*inch,W,.34*inch,0,1); c.setFillColor(white); c.setFont('Arial-Bold',8); c.drawString(.58*inch,H-.23*inch,kind)
    c.setFillColor(NAVY); c.setFont('Arial-Bold',15); c.drawString(.58*inch,H-.72*inch,title); c.setFillColor(TEAL); c.rect(.58*inch,H-.84*inch,.52*inch,.035*inch,0,1)
    c.setStrokeColor(HexColor('#D7E0E4')); c.line(.58*inch,.43*inch,W-.58*inch,.43*inch); c.setFillColor(MUTED); c.setFont('Arial',7); c.drawString(.58*inch,.25*inch,'Physics 2'); c.drawRightString(W-.58*inch,.25*inch,f'{page} / {total}')
def box(c,x,y,w,h,fill=PALE): c.setFillColor(fill); c.roundRect(x,y,w,h,7,0,1)
def axes(c,x,y,w,h,xlab='x',ylab='y'):
    c.setStrokeColor(TEAL); c.line(x,y,x+w,y); c.line(x,y,x,y+h); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(x+w-12,y-13,xlab); c.drawString(x-14,y+h-3,ylab)
def shm_graph(c,x,y,w,h):
    axes(c,x,y,w,h,'t','x'); c.setStrokeColor(GOLD); pts=[]
    for i in range(100):
        xx=x+8+(w-16)*i/99; yy=y+h*.52+h*.27*math.cos(2*math.pi*i/99); pts.append((xx,yy))
    c.lines([(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]) for i in range(99)]); c.setFillColor(INK); c.drawString(x+w*.58,y+h*.83,'A'); c.drawString(x+w*.58,y+h*.12,'B')
    c.setStrokeColor(NAVY); c.bezier(x+8,y+h*.2,x+w*.25,y+h*.2,x+w*.55,y+h*.8,x+w-8,y+h*.8)
def wave_graph(c,x,y,w,h):
    axes(c,x,y,w,h,'x','y'); c.setStrokeColor(GOLD); pts=[]
    for i in range(100):
        xx=x+8+(w-16)*i/99; yy=y+h*.52+h*.28*math.sin(4*math.pi*i/99); pts.append((xx,yy))
    c.lines([(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]) for i in range(99)])
def gaussian(c,x,y,r):
    c.setStrokeColor(TEAL); c.circle(x,y,r,1,0); c.setFillColor(GOLD); c.circle(x,y,6,0,1); c.setFillColor(INK); c.setFont('Arial',8); c.drawCentredString(x,y-r-14,'closed Gaussian surface')
def linecharge(c,x,y,w):
    c.setStrokeColor(INK); c.line(x,y,x+w,y); c.setFillColor(GOLD); c.circle(x+w*.25,y,6,0,1); c.circle(x+w*.75,y,6,0,1); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(x+w*.34,y+10,'dq = λ dx'); c.drawString(x+w*.42,y-18,'observation point P')
def potential(c,x,y,w,h):
    axes(c,x,y,w,h,'r','U'); c.setStrokeColor(GOLD); pts=[]
    for i in range(100):
        r=.48+2.5*i/99; u=1/(r**10)-1.8/(r**5); pts.append((x+8+(w-16)*i/99,max(y+8,min(y+h-8,y+h*.42+u*7))))
    c.lines([(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]) for i in range(99)]); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(x+w*.57,y+h*.47,'minimum')
def finish(c): c.save()

def draw_test():
    total=13; c=canvas.Canvas(TEST,pagesize=letter); c.setTitle('Physics 2 Comprehensive Mixed Test')
    # 1 conceptual fill-in
    header(c,'Conceptual Checks',1,total); y=H-1.03*inch; para(c,'Fill each blank with the most precise physics term or relation. Use the sign conventions implied by the statement.',.75*inch,y,6.7*inch); y-=.55*inch
    qs=['1. The electric field is defined as ______ per unit ______.','2. In electrostatic equilibrium, the electric field inside the conducting material is ______.','3. Electric flux through a closed surface depends on the ______ charge, not the charge outside.','4. A right-moving wave can be written y(x,t)=f(______ ).','5. In SHM, acceleration is proportional to displacement and points in the ______ direction.','6. Refraction changes wave ______ but not source frequency.','7. Polarization P is dipole moment per unit ______.','8. Sound in air is primarily a ______ wave of compressions and rarefactions.','9. Force from a potential-energy graph is the ______ derivative of U with respect to r.','10. The common ion formed by chlorine is ______ because chlorine tends to ______ one electron.']
    for q in qs: y-=para(c,q,.85*inch,y,6.4*inch,body)+.17*inch
    box(c,.85*inch,1.0*inch,6.3*inch,1.05*inch,CREAM); para(c,'Short explanation: choose one blank and explain the physical reason for your answer.',1.05*inch,1.82*inch,5.9*inch,small)
    c.showPage()
    # 2 matching
    header(c,'Matching: Visuals to Equations',2,total); y=H-1.03*inch; para(c,'Match each visual description (A–D) to the equation that best represents it (1–4). Write the letter-number pairs and explain one match.',.75*inch,y,6.7*inch); y-=.55*inch
    for i,t in enumerate(['A. A sphere centered on a point charge; E is constant on the surface.','B. A sinusoidal pattern translating right without changing shape.','C. A U(r) curve with a minimum at the stable separation.','D. A dielectric filled with aligned microscopic dipoles.']): y-=para(c,t,.85*inch,y,6.1*inch)+.1*inch
    box(c,.85*inch,3.1*inch,6.3*inch,2.5*inch); para(c,'1.  ∮ E·dA = Q<sub>enc</sub>/ε<sub>0</sub><br/>2.  y(x,t)=f(x−vt)<br/>3.  F(r)=−dU/dr<br/>4.  D=ε<sub>0</sub>E+P',1.1*inch,5.25*inch,5.7*inch,eq); gaussian(c,2.0*inch,1.9*inch,.45*inch); wave_graph(c,3.0*inch,1.1*inch,1.45*inch,.85*inch); potential(c,4.7*inch,1.1*inch,1.7*inch,.85*inch); c.showPage()
    # 3 SHM graphs
    header(c,'Simple Harmonic Motion',3,total); y=H-1.03*inch; para(c,'3. A mass obeys x(t)=A cos(ωt+φ). (a) Draw x versus t for A=0.20 m, ω=4.00 rad/s, φ=0. (b) State the period, maximum speed, and acceleration when x=+A. (c) Of the two graphs below, identify which could represent velocity and justify the phase relationship.',.75*inch,y,6.7*inch); shm_graph(c,1.0*inch,3.9*inch,5.8*inch,2.0*inch); para(c,'Graph A starts at +A; Graph B starts at zero and rises. Circle the graph that can represent v(t) when x(t)=A cos(ωt).',.9*inch,3.45*inch,6.1*inch,body); box(c,1.0*inch,1.25*inch,5.8*inch,.9*inch,CREAM); para(c,'Show the energy relation you would use to find speed at a general position x.',1.2*inch,1.9*inch,5.4*inch,small); c.showPage()
    # 4 wave numerical
    header(c,'Traveling Wave: Multiple Quantities',4,total); y=H-1.03*inch; para(c,'4. A wave is y(x,t)=0.040 cos(6.00x−120t) m, with x in metres and t in seconds. Find (a) amplitude, (b) wavelength, (c) frequency, (d) period, (e) propagation speed and direction, and (f) the transverse velocity at x=0,t=0.',.75*inch,y,6.7*inch); wave_graph(c,1.0*inch,4.25*inch,5.8*inch,1.65*inch); box(c,1.0*inch,2.05*inch,5.8*inch,1.1*inch,CREAM); para(c,'State which parts come from the coefficient, k, and ω before calculating.',1.2*inch,2.85*inch,5.4*inch,small); para(c,'k=2π/λ    ;    ω=2πf    ;    v=ω/k    ;    v<sub>y</sub>=∂y/∂t',1.1*inch,2.45*inch,5.6*inch,eq); c.showPage()
    # 5 calculus kinematics
    header(c,'Calculus Derivations: Constant Acceleration',5,total); y=H-1.03*inch; para(c,'5. Starting from a(t)=dv/dt, use definite integration to prove v<sub>f</sub>=v<sub>i</sub>+at for constant a. Then derive x(t)=x<sub>i</sub>+v<sub>i</sub>t+½at² from dx/dt=v(t). State the initial conditions used in each integration and explain why an integration constant appears.',.75*inch,y,6.7*inch); box(c,1.0*inch,3.9*inch,5.8*inch,1.5*inch,CREAM); para(c,'Required structure: differential statement → integral limits → evaluation → physical interpretation.',1.2*inch,5.05*inch,5.4*inch,body); para(c,'a(t)=dv/dt       ;       v(t)=dx/dt',1.15*inch,4.35*inch,5.5*inch,eq); c.showPage()
    # 6 Gauss
    header(c,'Gauss’s Law: Proof and Application',6,total); y=H-1.03*inch; para(c,'6. (a) Starting with E=kQ/r² for a point charge, derive Gauss’s law for a spherical surface and identify where k=1/(4πε<sub>0</sub>) is used. (b) Apply Gauss’s law to find E(r) outside and inside a uniformly charged solid sphere of radius R and density ρ. (c) Explain why the same shortcut does not work for an arbitrary nonsymmetric charge shape.',.75*inch,y,6.7*inch); gaussian(c,2.0*inch,3.8*inch,.75*inch); box(c,3.1*inch,3.0*inch,3.7*inch,1.6*inch,CREAM); para(c,'Show the surface area, enclosed charge, and region assumptions explicitly.',3.35*inch,4.3*inch,3.2*inch,body); para(c,'Φ<sub>E</sub>=∮E·dA    ;    Q<sub>enc</sub>=ρ(4πr³/3)',3.3*inch,3.35*inch,3.2*inch,eq); c.showPage()
    # 7 trig line charge
    header(c,'Continuous Charge Distribution and Trigonometric Substitution',7,total); y=H-1.03*inch; para(c,'7. A uniformly charged rod of length 2L lies along the x-axis from −L to +L with linear density λ. Point P is on the y-axis a distance a above its midpoint. (a) Explain why horizontal field components cancel. (b) Starting from dE=k dq/r², use dq=λdx and a trigonometric substitution to derive the exact field magnitude at P. (c) Check the limit L→∞.',.75*inch,y,6.7*inch); linecharge(c,1.0*inch,4.45*inch,5.8*inch); c.setStrokeColor(TEAL); c.line(3.9*inch,4.45*inch,3.9*inch,5.5*inch); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(4.0*inch,5.35*inch,'P'); c.drawString(4.0*inch,4.85*inch,'a'); box(c,1.0*inch,2.0*inch,5.8*inch,1.25*inch,CREAM); para(c,'Show a substitution such as x=a tanθ (or an equivalent choice), transform dx and r, update the limits, and resolve the y-component using cos or sin.',1.2*inch,3.0*inch,5.4*inch,body); para(c,'dEᵧ=dE cosθ    ;    r=√(a²+x²)',1.15*inch,2.45*inch,5.5*inch,eq); c.showPage()
    # 8 potential/graphs
    header(c,'Potential Energy and Graph Interpretation',8,total); y=H-1.03*inch; para(c,'8. Consider U(r)=C<sub>12</sub>/r<sup>12</sup>−C<sub>6</sub>/r<sup>6</sup>. (a) Identify the graph below that best matches this expression and explain each region. (b) Derive F(r) by differentiating. (c) State the equilibrium condition and whether the minimum is stable. (d) Compare this model with U=kq₁q₂/r.',.75*inch,y,6.7*inch); potential(c,1.0*inch,3.8*inch,5.8*inch,2.0*inch); box(c,1.0*inch,1.3*inch,5.8*inch,1.0*inch,CREAM); para(c,'Include the physical meaning of sign, slope, and the r→∞ limit.',1.2*inch,2.02*inch,5.4*inch,body); c.showPage()
    # 9 atom/dielectric
    header(c,'Atoms, Ions, and Dielectrics',9,total); y=H-1.03*inch; para(c,'9. (a) Explain the difference between the Bohr picture and the electron-cloud model. (b) Use valence-electron reasoning to predict Na⁺ and Cl⁻. (c) For a linear isotropic dielectric, derive D=εE from p=qd, P=(1/V)Σpᵢ, D=ε<sub>0</sub>E+P, and P=ε<sub>0</sub>χ<sub>e</sub>E. (d) Draw aligned dipoles and label E, P, and D.',.75*inch,y,6.7*inch); box(c,1.0*inch,3.55*inch,5.8*inch,1.75*inch,PALE); c.setStrokeColor(TEAL); c.roundRect(1.25*inch,3.85*inch,2.0*inch,1.1*inch,8,1,0); c.setFillColor(GOLD); c.circle(1.75*inch,4.4*inch,5,0,1); c.setFillColor(NAVY); c.circle(2.35*inch,4.4*inch,5,0,1); c.setStrokeColor(TEAL); c.line(1.8*inch,4.4*inch,2.3*inch,4.4*inch); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(3.7*inch,4.4*inch,'E, P, D →'); para(c,'Use the diagram area for your response and label which quantity is the material response.',1.2*inch,3.15*inch,5.4*inch,small); c.showPage()
    # 10 sound/refraction
    header(c,'Sound and Refraction',10,total); y=H-1.03*inch; para(c,'10. A sound has p<sub>rms,1</sub>=20 μPa at one location and p<sub>rms,2</sub>=60 μPa at another. (a) Find the change in sound-pressure level. (b) Explain why the pressure ratio is squared when converted through intensity. (c) A wave travels from a medium with n₁=1.00 into n₂=1.50 at θ₁=40°. Find θ₂ and state whether the ray bends toward or away from the normal. Draw the interface, normal, incident ray, and refracted ray.',.75*inch,y,6.7*inch); c.setStrokeColor(TEAL); c.line(4.0*inch,2.0*inch,4.0*inch,5.0*inch); c.setStrokeColor(GOLD); c.line(1.5*inch,4.3*inch,4.0*inch,3.8*inch); c.line(4.0*inch,3.8*inch,6.4*inch,4.55*inch); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(4.1*inch,4.8*inch,'normal'); c.drawString(4.2*inch,2.2*inch,'interface'); box(c,1.0*inch,1.0*inch,5.8*inch,.7*inch,CREAM); para(c,'Use Lp=20 log₁₀(p₂/p₁) for a level difference and n₁sinθ₁=n₂sinθ₂ for refraction.',1.2*inch,1.55*inch,5.4*inch,small); c.showPage()
    header(c,'Derivation Synthesis',11,total); y=H-1.03*inch; para(c,'11. Prove each relation from its differential or geometric starting point: (a) from F=−kx and F=mx″, derive the SHM differential equation; (b) from y=A cos(kx−ωt), derive the 1-D wave equation and identify v; (c) from equal phase travel along an interface, derive Snell law. For each, state the physical assumption that makes the derivation valid.',.75*inch,y,6.7*inch); box(c,1.0*inch,3.1*inch,5.8*inch,1.8*inch,CREAM); para(c,'Use separate lines for the physical law, substitution, differentiation or geometry, and final relation.',1.2*inch,4.55*inch,5.4*inch,body); para(c,'x″+ω²x=0    ;    yₓₓ=(1/v²)yₜₜ    ;    n₁sinθ₁=n₂sinθ₂',1.1*inch,3.75*inch,5.6*inch,eq); c.showPage()
    # 12 Coulomb force and field in one and two dimensions
    header(c,'Point Charges: 1D and 2D Force and Field',12,total); y=H-1.03*inch
    para(c,'12. Use k=8.99×10^9 N·m²/C². (a) On the x-axis, q1=+3.0 μC is at x=0 and q2=−2.0 μC is at x=0.40 m. Find the magnitude and direction of the force on q2. (b) A test charge q0=+1.0 μC is at (0,0), q1=+4.0 μC at (0.30,0) m, and q2=+4.0 μC at (0,0.30) m. Find the x- and y-components of the net electric field at q0, then its magnitude and direction. (c) Explain how the force result differs from the field result conceptually.',.75*inch,y,6.7*inch)
    box(c,.8*inch,3.75*inch,6.45*inch,1.45*inch,PALE); para(c,'For full credit: draw displacement vectors, identify attraction/repulsion, write each vector contribution, resolve components, and report units. Leave the lower half of the page for work.',1.05*inch,4.9*inch,5.95*inch,body)
    para(c,'F=k|q1q2|/r²    ;    E=k|q|/r²    ;    Ex=ΣEi,x    ;    Ey=ΣEi,y',1.05*inch,4.15*inch,5.95*inch,eq); c.showPage()
    # 13 hallmark equation memory and applications
    header(c,'Hallmark Equations and Physical Meaning',13,total); y=H-1.03*inch
    para(c,'13. (a) Write the standard forms of Newton’s universal law of gravitation, Coulomb’s law, the electric-field definition, Gauss’s law, the potential-energy relation, the linear wave equation, and the Doppler relation for a stationary observer and moving source. (b) For each, name the physical quantity being predicted and one condition or interpretation that prevents misuse. (c) Applications: predict qualitatively whether perceived frequency increases or decreases when the observer moves toward a sound source; predict how the field of an infinite line changes when distance doubles; and explain why a conductor surface cannot support a tangential electrostatic field.',.75*inch,y,6.7*inch)
    box(c,.8*inch,3.55*inch,6.45*inch,1.8*inch,CREAM); para(c,'Memory bank to complete from understanding, not guessing:<br/>F_g = ______ &nbsp;&nbsp; F_C = ______ &nbsp;&nbsp; E = ______ &nbsp;&nbsp; Φ_E = ______<br/>U = ______ &nbsp;&nbsp; y_xx = ______ &nbsp;&nbsp; f_obs = ______',1.05*inch,4.95*inch,5.95*inch,body)
    para(c,'Use the bottom half to explain the three applications in complete sentences and include one direction sketch.',1.05*inch,3.25*inch,5.95*inch,body); c.showPage()
    finish(c)

def key_page(c,page,total,title,concept,paragraph,steps,equations):
    header(c,'Detailed Answer Key',page,total,'COMPREHENSIVE TEST | ANSWERS'); y=H-1.03*inch; c.setFillColor(TEAL); c.setFont('Arial-Bold',11); c.drawString(.68*inch,y,title.upper()); y-=.25*inch
    box(c,.65*inch,y-2.65*inch,7.0*inch,2.65*inch,PALE); para(c,'Concepts needed: <b>'+concept+'</b>',.85*inch,y-.18*inch,6.55*inch,keybody); para(c,paragraph,.85*inch,y-.52*inch,6.55*inch,keybody); yy=y-1.4*inch
    for n,s in enumerate(steps,1): yy-=para(c,f'<b>{n}.</b> {s}',.85*inch,yy,6.5*inch,keybody)+.06*inch
    ey=y-4.0*inch; box(c,.65*inch,ey-1.35*inch,7.0*inch,1.35*inch,CREAM); c.setFillColor(NAVY); c.setFont('Arial-Bold',8); c.drawString(.85*inch,ey-.18*inch,'FULL WORKED RELATIONS / CHECKS'); yy=ey-.35*inch
    for s in equations: yy-=para(c,s,.85*inch,yy,6.5*inch,eq)+.03*inch
    if page<total: c.showPage()
def draw_key():
    total=13; c=canvas.Canvas(KEY,pagesize=letter); c.setTitle('Physics 2 Comprehensive Mixed Test - Detailed Answer Key')
    key_page(c,1,total,'1  Fill-in conceptual checks','field definition; conductor equilibrium; Gauss law; traveling waves; SHM; refraction; polarization; sound; potential slope; ions','These blanks test vocabulary and the direction of the physical relationships. The important habit is to name the object being described before writing an equation: E belongs to the source arrangement, flux counts net field through a closed boundary, and a wave function describes a moving pattern. Sign and direction are part of the concept, not decorations. For example, the minus sign in SHM says the acceleration restores the equilibrium position, while the minus sign in F=−dU/dr says force points toward decreasing potential energy. Similarly, chlorine becomes negative because it gains an electron, whereas ionization of an atom removes an electron and leaves a positive ion.',[
      '1: force; charge. 2: zero. 3: enclosed. 4: x−vt. 5: opposite. 6: speed. 7: volume. 8: longitudinal. 9: negative first. 10: Cl−; gain.',
      'For the wave blank, x−vt gives a right-moving pattern: keeping f(x−vt) fixed requires x to increase as t increases.',
      'For the potential blank, differentiate with respect to separation and reverse the sign; the slope, not the height alone, determines force.'
    ],['E=F/q','∮E·dA=Qenc/ε0','y=f(x−vt)','F=−dU/dr'])
    key_page(c,2,total,'2  Matching visuals to equations','Gauss symmetry; translation form of a wave; potential-energy slope; dielectric constitutive definition','Matching is a representation problem: identify what a picture is emphasizing before scanning the equation list. A closed Gaussian sphere and a point charge highlight enclosed charge and symmetry, so Gauss’s law is the match. A translated sinusoid is described by a function of x−vt. A potential well is read through its derivative because force is the negative slope. Aligned microscopic dipoles are material polarization, so the displacement definition combines the physical field with P. The same strategy works on unfamiliar diagrams: ask what is constant, what changes, and whether the diagram is geometric, kinematic, energetic, or material-response based.',[
      'A–1: the spherical surface makes E constant and radial, reducing flux to EA.',
      'B–2: x−vt keeps the shape fixed while translating it to the right.',
      'C–3: the minimum has zero slope, so force is zero there; the curve’s slope changes sign around it.',
      'D–4: P summarizes dipoles per volume and D=ε0E+P accounts for the dielectric response.'
    ],['A→1; B→2; C→3; D→4','Φ=EA when E is uniform and normal','D=ε0E+P'])
    key_page(c,3,total,'3  SHM graph and quantities','Hooke law; angular frequency; period; phase; energy conservation; derivative phase shifts','The cosine form starts at maximum positive displacement, so x(0)=A and v(0)=0. Differentiation shifts the phase by a quarter cycle: v(t)=−Aω sin(ωt), meaning velocity initially becomes negative as the mass returns toward equilibrium. At x=+A the acceleration is most negative because the restoring force is largest, while speed is zero. The period is the time for the phase to change by 2π. Energy gives speed at any position without needing to solve for time, because spring and kinetic energy exchange while their sum stays constant in ideal SHM.',[
      'With A=0.20 m and ω=4.00 rad/s: T=2π/ω=1.57 s.',
      'vmax=Aω=(0.20)(4.00)=0.800 m/s.',
      'At x=+A: a=−ω²A=−(4.00)²(0.20)=−3.20 m/s² and v=0.',
      'Graph A is x(t); Graph B can be v(t) because v(0)=0 and v initially decreases for φ=0.',
      '½mv²+½kx²=½kA², so v(x)=±√[(k/m)(A²−x²)].'
    ],['x=A cos(ωt)','v=dx/dt=−Aω sin(ωt)','a=dv/dt=−ω²x','T=2π/ω'])
    key_page(c,4,total,'4  Traveling-wave calculation','amplitude; wave number; angular frequency; wavelength; frequency; period; phase; wave speed; partial derivative','For a sinusoidal wave, compare the given expression term-by-term with y=A cos(kx−ωt). The coefficient outside the cosine is amplitude, the coefficient of x is wave number, and the coefficient of t is angular frequency. The negative sign before ωt means rightward translation. Convert angular quantities using 2π, then use v=ω/k or v=fλ. The requested transverse velocity is a partial derivative: x is held fixed while differentiating with respect to time. This distinguishes particle motion from the propagation speed of the pattern.',[
      'A=0.040 m; k=6.00 rad/m; ω=120 rad/s.',
      'λ=2π/k=1.047 m; f=ω/(2π)=19.10 Hz; T=1/f=0.0524 s.',
      'v=ω/k=20.0 m/s. Since the phase is kx−ωt, the wave travels in +x.',
      'vᵧ=∂y/∂t=0.040(120)sin(6x−120t). At x=t=0, vᵧ=0.',
      'Units check: k is rad/m, ω is rad/s, and their ratio is m/s.'
    ],['y=0.040 cos(6.00x−120t) m','λ=2π/6.00=1.047 m','f=120/(2π)=19.10 Hz','v=120/6.00=20.0 m/s'])
    key_page(c,5,total,'5  Constant-acceleration derivations','derivatives; definite integrals; initial conditions; integration constants; kinematics','These derivations show why the familiar kinematics formulas are consequences of the differential definitions, not independent facts. The first derivation starts with acceleration and uses limits to encode the initial velocity. The second integrates the resulting velocity and uses the initial position. Differentiating the final expressions is the strongest check: it returns the original velocity and acceleration exactly.',[
      'Since dv/dt=a, multiply by dt: dv=a dt. Integrate from vᵢ at t=0 to v at t: v−vᵢ=∫₀ᵗa dt′=at.',
      'Therefore v(t)=vᵢ+at and at t=t_f, v_f=vᵢ+at_f. The constant vᵢ is required by v(0)=vᵢ.',
      'Next use dx/dt=vᵢ+at. Integrate from xᵢ at t=0: x−xᵢ=∫₀ᵗ(vᵢ+at′)dt′=vᵢt+½at².',
      'Hence x(t)=xᵢ+vᵢt+½at². Differentiating once returns vᵢ+at; differentiating twice returns a.'
    ],['dv/dt=a','v_f−v_i=∫₀ᵗa dt=at','v_f=v_i+at','x_f−x_i=∫₀ᵗ(v_i+at′)dt′=v_it+½at²','x_f=x_i+v_it+½at²'])
    key_page(c,6,total,'6  Gauss law proof and sphere','inverse-square field; flux; spherical symmetry; enclosed charge; volume integration','Gauss’s law is especially powerful when symmetry makes the field magnitude constant on a chosen closed surface. The proof begins with the point-charge field and uses the area of a sphere. The application then changes only the enclosed charge according to the region. Outside a uniform sphere, the full charge is enclosed and the result is point-charge-like. Inside, the enclosed charge scales with r³ while the Gaussian area scales with r², producing a field proportional to r. An arbitrary shape lacks a surface on which E is both constant and normal, so Gauss’s law remains true but is no longer a one-line solver.',[
      'For a sphere: Φ=∮E·dA=E(4πr²)=(kQ/r²)(4πr²)=4πkQ=Q/ε0.',
      'Outside (r≥R): Qenc=ρ(4πR³/3), so E=Qenc/(4πε0r²)=ρR³/(3ε0r²).',
      'Inside (r<R): Qenc=ρ(4πr³/3), so E(4πr²)=Qenc/ε0 and E=ρr/(3ε0).',
      'At r=R both expressions agree: E=ρR/(3ε0), providing a boundary check.'
    ],['k=1/(4πε0)','∮E·dA=Qenc/ε0','Einside=ρr/(3ε0)','Eoutside=ρR³/(3ε0r²)'])
    key_page(c,7,total,'7  Finite rod: trig substitution','continuous charge; superposition; symmetry; dq=λdx; component resolution; trigonometric substitution','The field from a continuous rod is built from small charge elements. Symmetry eliminates the horizontal components pair-by-pair, leaving only the vertical component. The trigonometric substitution is useful because r=√(a²+x²) appears in both the inverse-square field and the component factor. Let x=a tanθ: then r=a secθ, dx=a sec²θ dθ, and cosθ=a/r=cosθ. The integral becomes simple and the limits encode the rod endpoints. This is the general pattern to reuse: write dq, write the distance, resolve the component, substitute, then use symmetry.',[
      'dE=k dq/r²=kλ dx/(a²+x²). The vertical component is dEᵧ=dE cosθ, with cosθ=a/r.',
      'Thus dEᵧ=kλa dx/(a²+x²)^(3/2). Integrate x from −L to L.',
      'Using x=a tanθ: dx=a sec²θdθ and (a²+x²)^(3/2)=a³sec³θ, so dEᵧ=(kλ/a)cosθ dθ.',
      'The limits are θ=±tan⁻¹(L/a). Therefore Eᵧ=(kλ/a)[sinθ]₋θ₀^θ₀=(2kλ/a)sinθ₀.',
      'Since sinθ₀=L/√(a²+L²), E=2kλL/[a√(a²+L²)]. As L→∞, E→2kλ/a=λ/(2πε0a).'
    ],['E=2kλL/(a√(a²+L²))','L→∞: E=2kλ/a=λ/(2πε0a)'])
    key_page(c,8,total,'8  Potential-energy graph','Lennard-Jones model; power-law terms; derivative; stability; point-charge comparison','The graph is determined by competing powers of separation. At very small r, the positive r⁻¹² term dominates and produces a steep repulsive wall. At intermediate r, the negative r⁻⁶ term can dominate, making U negative and creating an attractive well. At large r both terms vanish, so U approaches the chosen zero. Force depends on slope: the minimum is not special because U is negative; it is special because the slope is zero and the curvature is positive, making the equilibrium stable to small radial displacements.',[
      'Differentiate term by term: dU/dr=−12C₁₂/r¹³+6C₆/r⁷.',
      'Therefore F=−dU/dr=12C₁₂/r¹³−6C₆/r⁷.',
      'Equilibrium requires F=0, so 12C₁₂/r¹³=6C₆/r⁷ and r⁶=2C₁₂/C₆.',
      'The minimum is stable because the curve bends upward there: a small displacement creates a restoring force.',
      'The point-charge potential kq₁q₂/r has no short-range repulsive wall by itself; realistic ions and molecules require extra structure.'
    ],['U=C₁₂/r¹²−C₆/r⁶','F=12C₁₂/r¹³−6C₆/r⁷','r_eq=(2C₁₂/C₆)^(1/6)'])
    key_page(c,9,total,'9  Atomic models and dielectric derivation','Bohr model; electron cloud; ionization; valence electrons; dipole moment; polarization; susceptibility; permittivity','The atomic portion tests model selection. Bohr orbits are a useful quantized picture for simple atoms, but the electron-cloud model is more accurate because it describes probability rather than a definite track. Ion formation follows electron counting: losing negative charge makes an ion positive, while gaining it makes an ion negative. The dielectric derivation then moves from microscopic to macroscopic description. A dipole moment describes one separated pair; polarization averages many dipoles per volume; D packages the free-charge field and material response. For a linear isotropic medium, P is parallel and proportional to E, which permits the definition of ε.',[
      'Bohr force balance: ke²/r²=mₑv²/r. Quantum restrictions determine allowed states; the force balance alone is classical.',
      'Na loses one valence electron → Na⁺. Cl gains one electron → Cl⁻. Ionization of a neutral atom removes an electron and leaves a positive ion.',
      'p=qd and P=(1/V)Σpᵢ. Then D=ε₀E+P.',
      'Insert P=ε₀χₑE: D=ε₀E+ε₀χₑE=ε₀(1+χₑ)E.',
      'Define ε=ε₀(1+χₑ), giving D=εE. In the isotropic sketch E, P, and D are collinear.'
    ],['p=qd','P=(1/V)Σpᵢ','D=ε₀E+P','P=ε₀χₑE','D=ε₀(1+χₑ)E=εE'])
    key_page(c,10,total,'10  Sound pressure and Snell law','rms pressure; intensity; logarithms; decibels; refractive index; phase continuity','The sound calculation uses two linked ideas. Sound-pressure level is defined from pressure relative to a reference, while intensity is proportional to the square of rms pressure. Taking the difference between two levels cancels the reference and leaves a pressure ratio. Refraction is separate but uses the same disciplined ratio reasoning: frequency is continuous across the boundary, so speed and wavelength change. Snell’s law expresses tangential phase matching. Since n₂ is larger, the second medium is slower and the ray bends toward the normal.',[
      'Pressure ratio=60/20=3, so ΔL_p=20log₁₀3=9.54 dB.',
      'Because I∝p², I₂/I₁=(3)²=9; equivalently 10log₁₀9=19.08 dB for intensity level, consistent with the pressure-level factor 20.',
      'Snell: 1.00 sin40°=1.50 sinθ₂, so sinθ₂=0.4285 and θ₂=25.4°.',
      'The ray bends toward the normal because θ₂<θ₁. The frequency stays fixed; v and λ decrease in the larger-index medium.',
      'A correct drawing includes the interface, normal, incident angle from the normal, and the smaller refracted angle.'
    ],['ΔL_p=20log₁₀(p₂/p₁)','I₂/I₁=(p₂/p₁)²','n₁sinθ₁=n₂sinθ₂','θ₂=sin⁻¹[(1.00/1.50)sin40°]=25.4°'])
    key_page(c,11,total,'11  Derivation synthesis','Hooke law; Newton law; partial derivatives; wave translation; phase continuity; refractive index; linear assumptions','This final item checks whether the equations can be rebuilt from physical laws. For SHM, the crucial assumption is a linear restoring force: Hooke law. For a traveling wave, the crucial assumption is a sinusoidal shape with constant propagation speed, and differentiation reveals that spatial curvature and temporal acceleration have the same shape with a scale factor. For Snell law, the interface must preserve phase along its tangent: the tangential component of the wave vector is continuous. These are not memorization tricks. Each derivation connects a local physical rule to a global equation and exposes the assumptions that would fail for nonlinear springs, dispersive media, or an interface that does not maintain a common frequency.',[
      'SHM: F=−kx and F=mx″ imply mx″=−kx. Divide by m and define ω²=k/m: x″+ω²x=0. The assumption is linear restoring behavior.',
      'Wave: y=A cos(kx−ωt). Two x derivatives give yₓₓ=−k²y; two t derivatives give yₜₜ=−ω²y. Since v=ω/k, yₓₓ=(1/v²)yₜₜ.',
      'The wave equation assumes a constant v and small enough behavior for linear superposition; it is a verification of the proposed solution.',
      'Snell: in equal time dt, phase fronts advance v₁dt and v₂dt. Tangential phase matching gives v₁dt sinθ₁=v₂dt sinθ₂.',
      'Cancel dt and substitute v=c/n: sinθ₁/sinθ₂=v₂/v₁=n₁/n₂, hence n₁sinθ₁=n₂sinθ₂.'
    ],['mx″=−kx → x″+ω²x=0','yₓₓ=−k²y; yₜₜ=−ω²y → yₓₓ=(1/v²)yₜₜ','v₁sinθ₁=v₂sinθ₂ → n₁sinθ₁=n₂sinθ₂'])
    key_page(c,12,total,'12  Point charges in 1D and 2D','Coulomb law; electric-field definition; source/test roles; attraction and repulsion; vector components; superposition; inverse-square scaling','The one-dimensional part is a signed-direction problem: q1 and q2 have opposite signs, so the force is attractive and points from q2 toward q1. The two-dimensional part is a field problem: the test charge is not included when computing E, and the equal perpendicular source charges make the x and y components equal. Only after the vector components are found should magnitude and angle be calculated. This distinction is essential: force depends on the test charge, while electric field is a property of the source arrangement at the point.',['a. r=0.40 m. The magnitude is F=k|q1q2|/r²=(8.99×10^9)(3.0×10^-6)(2.0×10^-6)/(0.40)²=0.337 N. The force is attractive, so it points left.','b. For q1, E1=k(4.0×10^-6)/(0.30)²=3.996×10^5 N/C in the negative x direction. For q2, the same magnitude points in negative y. Thus Ex=−3.996×10^5 N/C and Ey=−3.996×10^5 N/C.','The net field magnitude is E=√(Ex²+Ey²)=5.65×10^5 N/C and points 45 degrees below the negative x-axis, or 225 degrees from +x.','c. If the test charge is q0=+1.0 μC, F=q0E, so the force magnitude would be 0.565 N in the same direction. A negative test charge would reverse the force direction.','The inverse-square factor applies separately to each source distance; vector addition is required because the sources are not collinear.'], ['F = k m1m2/r² toward the other mass.','F = k|q1q2|/r² with direction set by signs and geometry.','E = F/q_test, independent of the small test charge.','Φ_E = closed integral E dot dA = Q_enc/eps0.','U = qV or U = kq1q2/r for point charges.','y_xx = (1/v²)y_tt.','For a stationary observer and moving source: f_obs=f_s v/(v∓v_s), with approach using the denominator v-v_s and increasing the observed frequency.','Approaching source or observer means wavefront arrival rate increases. For a line charge, doubling r halves E. A tangential conductor field would move free charge, contradicting electrostatic equilibrium.'])
    c.setFillColor(MUTED); c.setFont('Arial',7); c.drawString(.65*inch,.58*inch,'Sources: supplied Physics 2 scans; Young and Freedman, University Physics; OpenStax University Physics Volumes 1 and 2.'); c.save()
draw_test(); draw_key(); print(TEST); print(KEY)

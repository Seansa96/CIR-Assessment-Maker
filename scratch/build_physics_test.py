from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, math

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
OUT=os.path.join(ROOT,'output','pdf'); os.makedirs(OUT,exist_ok=True)
TEST=os.path.join(OUT,'Physics 2 Test 1 - Scanned Questions.pdf')
KEY=os.path.join(OUT,'Physics 2 Test 1 - Detailed Answer Key.pdf')
W,H=letter; NAVY=HexColor('#17324D'); TEAL=HexColor('#137C8B'); GOLD=HexColor('#D9942A'); INK=HexColor('#203040'); PALE=HexColor('#EAF3F5'); CREAM=HexColor('#F7F2E8'); MUTED=HexColor('#667786')
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf')); pdfmetrics.registerFont(TTFont('Arial-Bold',r'C:\Windows\Fonts\arialbd.ttf'))
styles=getSampleStyleSheet(); body=ParagraphStyle('body',fontName='Arial',fontSize=9.5,leading=12,textColor=INK); tiny=ParagraphStyle('tiny',fontName='Arial',fontSize=8.5,leading=10.2,textColor=INK); eq=ParagraphStyle('eq',fontName='Arial-Bold',fontSize=12,leading=15,textColor=NAVY,alignment=TA_CENTER); ans=ParagraphStyle('ans',fontName='Arial',fontSize=9,leading=11,textColor=INK)
def clean(s):
    for a,b in {'⃗':'','∮':'∫','∇':'grad','∂':'d','ₓ':'x','ₜ':'t','Δ':'d','ᵣ':'r','ₘ':'m','ₛ':'s','ₚ':'p','ᵢ':'i','ᵥ':'v','ₙ':'n','⁺':'<super>+</super>','⁻':'<super>-</super>','ₑ':'<sub>e</sub>'}.items(): s=s.replace(a,b)
    for sub,d in zip('₀₁₂₃₄₅₆₇₈₉','0123456789'): s=s.replace(sub,f'<sub>{d}</sub>')
    return s
def para(c,s,x,y,w,style=body):
    q=Paragraph(clean(s),style); _,h=q.wrap(w,1000); q.drawOn(c,x,y-h); return h
def header(c,title,page,total):
    c.setFillColor(NAVY); c.rect(0,H-.34*inch,W,.34*inch,0,1); c.setFillColor(white); c.setFont('Arial-Bold',8); c.drawString(.58*inch,H-.23*inch,'PHYSICS 2  |  SCANNED QUESTION SET')
    c.setFillColor(NAVY); c.setFont('Arial-Bold',16); c.drawString(.58*inch,H-.72*inch,title); c.setFillColor(TEAL); c.rect(.58*inch,H-.84*inch,.52*inch,.035*inch,0,1)
    c.setStrokeColor(HexColor('#D7E0E4')); c.line(.58*inch,.43*inch,W-.58*inch,.43*inch); c.setFillColor(MUTED); c.setFont('Arial',7); c.drawString(.58*inch,.25*inch,'Physics 2 Test 1'); c.drawRightString(W-.58*inch,.25*inch,f'{page} / {total}')
def box(c,x,y,w,h,fill=PALE): c.setFillColor(fill); c.roundRect(x,y,w,h,7,0,1)
def linecharge(c,x,y,w):
    c.setStrokeColor(INK); c.setLineWidth(1.2); c.line(x,y,x+w,y); c.setFillColor(GOLD); c.circle(x+w*.25,y,6,0,1); c.setFillColor(NAVY); c.circle(x+w*.55,y,6,0,1); c.setFillColor(GOLD); c.circle(x+w*.85,y,6,0,1); c.setFillColor(INK); c.setFont('Arial',8); c.drawCentredString(x+w*.25,y+12,'+4 μC'); c.drawCentredString(x+w*.55,y+12,'−6 μC'); c.drawCentredString(x+w*.85,y+12,'+8 μC'); c.drawString(x+w*.38,y-17,'a = 0.02 m     b = 0.07 m')
def fieldlines(c,x,y,w,h,irregular=False):
    c.setFillColor(PALE); c.setStrokeColor(INK); c.setLineWidth(1.2)
    if irregular:
        path=c.beginPath(); path.moveTo(x+w*.22,y+h*.32); path.curveTo(x+w*.42,y+h*.18,x+w*.68,y+h*.22,x+w*.86,y+h*.50); path.curveTo(x+w*.68,y+h*.77,x+w*.42,y+h*.82,x+w*.22,y+h*.68); path.close(); c.drawPath(path,0,1)
        left=x+w*.22; right=x+w*.86
    else:
        c.ellipse(x+w*.28,y+h*.28,x+w*.72,y+h*.72,0,1); left=x+w*.28; right=x+w*.72
    c.setStrokeColor(TEAL); c.setLineWidth(1)
    for i,yy in enumerate([y+h*.34,y+h*.43,y+h*.57,y+h*.66]):
        if irregular:
            c.line(x+6,yy,left,yy+8*(i-1)); c.line(right,yy+8*(i-1),x+w-6,yy+3*(1-i))
        else:
            c.line(x+6,yy,left,yy+8*(i-1)); c.line(right,yy+8*(i-1),x+w-6,yy+3*(1-i))
    c.setFillColor(INK); c.setFont('Arial',8); c.drawCentredString(x+w/2,y+10,'field lines meet the surface at 90°')
def banddiagram(c,x,y,w,h):
    c.setStrokeColor(TEAL); c.setLineWidth(1); c.line(x+25,y+25,x+25,y+h-15); c.line(x+25,y+25,x+w-8,y+25); c.setStrokeColor(NAVY); c.line(x+45,y+h*.72,x+w-10,y+h*.72); c.line(x+45,y+h*.53,x+w-10,y+h*.53); c.line(x+45,y+h*.38,x+w-10,y+h*.38); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(x+w*.55,y+5,'separation →'); c.drawString(x+30,y+h*.75,'E'); c.drawString(x+30,y+h*.56,'E'); c.drawString(x+30,y+h*.4,'E')
def plate(c,x,y,w,h):
    c.setStrokeColor(NAVY); c.line(x,y+h,x+w,y+h); c.line(x,y,x+w,y); c.setFillColor(GOLD); c.circle(x+w*.2,y+h*.55,5,0,1); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(x+w*.02,y+h+8,'+Q'); c.drawString(x+w*.02,y-15,'−Q'); c.setStrokeColor(TEAL); c.line(x+w*.2,y+h*.55,x+w*.8,y+h*.55); c.setFillColor(INK); c.drawString(x+w*.72,y+h*.55+8,'v'); c.drawString(x+w*.48,y+h*.55-16,'q, m')
def atomdiagram(c,x,y,w,h):
    c.setStrokeColor(TEAL); c.circle(x+w*.28,y+h*.56,18,1,0); c.circle(x+w*.28,y+h*.56,32,1,0); c.setFillColor(GOLD); c.circle(x+w*.28,y+h*.56,7,0,1); c.setFillColor(INK); c.setFont('Arial',8); c.drawCentredString(x+w*.28,y+h*.56-3,'+'); c.drawString(x+w*.05,y+h*.22,'nucleus + allowed orbits')
    c.setStrokeColor(NAVY); c.line(x+w*.58,y+h*.28,x+w*.95,y+h*.28); c.line(x+w*.58,y+h*.48,x+w*.95,y+h*.48); c.line(x+w*.58,y+h*.68,x+w*.95,y+h*.68); c.setFillColor(INK); c.drawString(x+w*.6,y+h*.77,'energy'); c.drawString(x+w*.67,y+h*.18,'discrete levels')
def dielectricdiagram(c,x,y,w,h):
    c.setStrokeColor(TEAL); c.roundRect(x+12,y+18,w-24,h-36,8,1,0); c.setFillColor(GOLD); c.circle(x+w*.30,y+h*.52,5,0,1); c.setFillColor(NAVY); c.circle(x+w*.46,y+h*.52,5,0,1); c.setStrokeColor(TEAL); c.line(x+w*.34,y+h*.52,x+w*.42,y+h*.52); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(x+15,y+7,'−  →  + dipoles'); c.drawString(x+w*.60,y+h*.7,'E, P, D →')
def potentialdiagram(c,x,y,w,h):
    c.setStrokeColor(TEAL); c.line(x+15,y+24,x+w-10,y+24); c.line(x+15,y+24,x+15,y+h-12); pts=[]
    for i in range(100):
        r=.48+2.52*i/99; u=1.0/(r**10)-1.8/(r**5); pts.append((x+15+(w-25)*i/99,max(y+28,min(y+h-22,y+47+u*9))))
    c.setStrokeColor(GOLD); c.lines([(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]) for i in range(99)]); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(x+20,y+h-12,'repulsive wall'); c.drawString(x+w*.55,y+31,'minimum: F = 0')
def draw_test():
    c=canvas.Canvas(TEST,pagesize=letter); c.setTitle('Physics 2 Test 1 - Scanned Questions'); total=8
    # page 1
    header(c,'Physics 2 Test 1',1,total); para(c,'Short test reconstructed from the supplied worksheet scans. Show diagrams, sign conventions, intermediate equations, and units. Use k = 8.99 × 10⁹ N·m²/C² and ε₀ = 8.85 × 10⁻¹² C²/(N·m²).',.58*inch,H-1.05*inch,7.2*inch,body)
    y=H-1.55*inch; c.setFillColor(NAVY); c.setFont('Arial-Bold',12); c.drawString(.58*inch,y,'1. Conductors in electrostatics  [12 points]'); y-=.25*inch
    qs=['a. Explain three characteristics of a conductor in electrostatic equilibrium.','b. Draw a spherical conductor in a constant external electric field and show how the field lines bend at the surface.','c. Draw the electric-field lines for an irregularly shaped conductor, including the stronger crowding near a sharp point.','d. Explain how the result is related to electrostatic shielding.']
    for q in qs: y-=para(c,q,.75*inch,y,6.7*inch,body)+.1*inch
    fieldlines(c,4.35*inch,3.85*inch,2.45*inch,1.8*inch); fieldlines(c,.8*inch,1.55*inch,2.45*inch,1.8*inch,True)
    c.showPage()
    # page 2
    header(c,'Electric Fields and Band Diagrams',2,total); y=H-1.02*inch; c.setFillColor(NAVY); c.setFont('Arial-Bold',12); c.drawString(.58*inch,y,'2. Direct field and energy questions  [18 points]'); y-=.28*inch
    para(c,'a. Three point charges lie on a line in the order shown. Calculate the net electric force on the +8 μC charge.',.75*inch,y,6.7*inch,body); linecharge(c,1.2*inch,5.55*inch,5.2*inch)
    para(c,'b. For the rectangular charge arrangement below, give a symbolic solution for the electric field at P, the force on a charge q₄ placed at P, and the electric potential at P. Let q₁=(0,0), q₂=(0,b), q₃=(a,0), and P=(a,b).',.75*inch,4.95*inch,6.7*inch,body)
    c.setStrokeColor(TEAL); c.setLineWidth(1.4); c.rect(1.1*inch,2.85*inch,2.1*inch,1.2*inch,0,0); c.setFillColor(GOLD); c.circle(1.1*inch,2.85*inch,5,0,1); c.circle(1.1*inch,4.05*inch,5,0,1); c.circle(3.2*inch,2.85*inch,5,0,1); c.setFillColor(NAVY); c.circle(3.2*inch,4.05*inch,5,0,1); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(1.0*inch,2.62*inch,'q1'); c.drawString(1.0*inch,4.17*inch,'q2'); c.drawString(3.1*inch,2.62*inch,'q3'); c.drawString(3.1*inch,4.17*inch,'P')
    para(c,'c. Draw the Bohr model of an isolated atom and its corresponding discrete energy-level diagram. Then sketch the energy levels of three identical atoms as their separation decreases, and one periodic crystal model showing valence and conduction bands.',.75*inch,2.35*inch,6.7*inch,body); banddiagram(c,4.4*inch,1.05*inch,2.1*inch,1.1*inch); c.showPage()
    # page 3
    header(c,'Gauss Law and Charge Distributions',3,total); y=H-1.02*inch; c.setFillColor(NAVY); c.setFont('Arial-Bold',12); c.drawString(.58*inch,y,'3. Symmetry and field derivations  [16 points]'); y-=.28*inch
    para(c,'a. A charged particle enters midway between parallel plates of area L². The plates carry +Q and −Q. The particle has charge q, mass m, horizontal speed v, and spends time L/v between the plates. Derive the vertical acceleration and vertical deflection.',.75*inch,y,6.7*inch,body); plate(c,1.0*inch,5.15*inch,5.5*inch,1.1*inch)
    para(c,'b. A solid sphere of radius R has volume charge density ρ(r)=ρ₀(r/R)². Find its total charge by integrating spherical shells.',.75*inch,4.55*inch,6.7*inch,body)
    c.setStrokeColor(TEAL); c.circle(2.0*inch,2.65*inch,.55*inch,0,0); c.circle(2.0*inch,2.65*inch,.27*inch,0,0); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(2.75*inch,2.6*inch,'shell radius r′, thickness dr′'); c.showPage()
    # page 4
    header(c,'Oscillation and Sound',4,total); y=H-1.02*inch; c.setFillColor(NAVY); c.setFont('Arial-Bold',12); c.drawString(.58*inch,y,'4. Mass-spring oscillator  [12 points]'); y-=.28*inch
    para(c,'A 3.3 kg mass is attached to a spring with spring constant 100 N/m. The mass oscillates with amplitude 0.40 m. Calculate: (a) the maximum total mechanical energy, (b) the maximum speed, (c) the speed when x=0.03 m, and (d) draw the energy-versus-position curves for kinetic and spring potential energy.',.75*inch,y,6.7*inch,body)
    c.setStrokeColor(TEAL); c.line(1.0*inch,4.3*inch,3.3*inch,4.3*inch); c.line(1.4*inch,4.3*inch,1.4*inch,4.8*inch); c.line(1.4*inch,4.55*inch,1.7*inch,4.7*inch); c.line(1.7*inch,4.7*inch,2.0*inch,4.4*inch); c.rect(2.0*inch,4.3*inch,.5*inch,.35*inch,0,0); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(2.58*inch,4.42*inch,'m')
    c.setStrokeColor(TEAL); c.line(4.3*inch,2.1*inch,7.2*inch,2.1*inch); c.line(5.0*inch,1.3*inch,5.0*inch,3.0*inch); c.setStrokeColor(GOLD); c.bezier(5.0*inch,1.3*inch,5.5*inch,3.3*inch,6.5*inch,3.3*inch,7.0*inch,1.3*inch); c.setStrokeColor(NAVY); c.bezier(5.0*inch,3.0*inch,5.5*inch,1.0*inch,6.5*inch,1.0*inch,7.0*inch,3.0*inch); c.setFillColor(INK); c.drawString(6.2*inch,3.08*inch,'E'); c.drawString(6.2*inch,1.05*inch,'U')
    c.showPage()
    # page 5
    header(c,'Sound Pressure Level',5,total); y=H-1.02*inch; c.setFillColor(NAVY); c.setFont('Arial-Bold',12); c.drawString(.58*inch,y,'5. Sound pressure level  [10 points]'); y-=.28*inch
    para(c,'Define sound-pressure level in terms of rms pressure, using p₀ = 20 μPa. Then determine the change in level when the rms pressure changes from p₁ to 2p₁ and from p₁ to ½p₁. Explain why doubling pressure does not produce a 2 dB change.',.75*inch,y,6.7*inch,body)
    c.setFillColor(PALE); c.roundRect(1.0*inch,4.3*inch,5.8*inch,1.15*inch,8,0,1); para(c,'Reminder: intensity for a sinusoidal sound satisfies I ∝ p<sub>rms</sub>².',1.2*inch,5.15*inch,5.4*inch,eq); c.setStrokeColor(TEAL); c.line(1.0*inch,2.45*inch,6.9*inch,2.45*inch); c.setStrokeColor(GOLD); c.bezier(1.1*inch,2.45*inch,2.2*inch,3.15*inch,3.4*inch,1.75*inch,4.4*inch,2.45*inch); c.bezier(4.4*inch,2.45*inch,5.5*inch,3.1*inch,6.1*inch,1.8*inch,6.8*inch,2.45*inch); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(6.05*inch,2.62*inch,'pressure wave'); c.showPage()
    header(c,'Atomic Models and Molecules',6,total); y=H-1.02*inch; c.setFillColor(NAVY); c.setFont('Arial-Bold',12); c.drawString(.58*inch,y,'6. Bohr model, ions, and molecules  [12 points]'); y-=.28*inch
    para(c,'a. Draw a hydrogen atom using the Bohr picture and a corresponding discrete energy-level diagram. Write the force balance used for a circular electron orbit.',.75*inch,y,6.7*inch,body); atomdiagram(c,1.0*inch,4.85*inch,5.8*inch,1.55*inch)
    para(c,'b. Explain what changes when an atom is ionized. Predict the common ions formed by sodium and chlorine and justify each using valence electrons.',.75*inch,4.42*inch,6.7*inch,body)
    para(c,'c. Replace the orbit picture with an electron-cloud picture. Draw one diatomic molecule and one triatomic molecule, labeling the atoms represented.',.75*inch,3.48*inch,6.7*inch,body); c.setStrokeColor(TEAL); c.ellipse(1.2*inch,1.45*inch,2.0*inch,2.15*inch,0,0); c.setFillColor(GOLD); c.circle(1.6*inch,1.8*inch,6,0,1); c.setFillColor(NAVY); c.circle(4.5*inch,1.8*inch,6,0,1); c.circle(5.05*inch,1.8*inch,6,0,1); c.circle(6.15*inch,1.8*inch,6,0,1); c.setFillColor(INK); c.setFont('Arial',8); c.drawString(1.05*inch,1.2*inch,'electron cloud'); c.drawString(4.3*inch,1.2*inch,'diatomic'); c.drawString(5.9*inch,1.2*inch,'triatomic'); c.showPage()
    header(c,'Dielectrics and Displacement',7,total); y=H-1.02*inch; c.setFillColor(NAVY); c.setFont('Arial-Bold',12); c.drawString(.58*inch,y,'7. Polarization and displacement vector  [10 points]'); y-=.28*inch
    para(c,'A dielectric of volume V contains microscopic dipoles pᵢ. (a) Define the dipole moment and polarization. (b) Starting from D = ε₀E + P and P = ε₀χₑE, derive D = εE for a linear isotropic dielectric. (c) Draw the relative directions of E, P, and D and show aligned molecular dipoles.',.75*inch,y,6.7*inch,body); dielectricdiagram(c,1.0*inch,4.15*inch,5.8*inch,1.55*inch)
    box(c,1.0*inch,2.05*inch,5.8*inch,1.25*inch,CREAM); para(c,'Use standard SI units and identify which quantities describe free charge versus material response.',1.2*inch,3.0*inch,5.4*inch,body); para(c,'p = qd    ;    P = (1/V)Σpᵢ    ;    D = ε₀E + P    ;    P = ε₀χₑE    ;    D = εE',1.15*inch,2.68*inch,5.5*inch,eq); c.showPage()
    header(c,'Interaction Potentials',8,total); y=H-1.02*inch; c.setFillColor(NAVY); c.setFont('Arial-Bold',12); c.drawString(.58*inch,y,'8. Ions and molecular potential energy  [12 points]'); y-=.28*inch
    para(c,'For two interacting particles: (a) state the point-charge potential energy and the force–potential relation; (b) sketch and label U(r) for a realistic ionic or molecular interaction, including repulsive, attractive, equilibrium, and large-r regions; (c) write the Lennard–Jones form and explain why Na⁺ and Cl⁻ are composite particles rather than literal point charges.',.75*inch,y,6.7*inch,body); potentialdiagram(c,1.0*inch,4.25*inch,5.8*inch,1.7*inch)
    box(c,1.0*inch,2.05*inch,5.8*inch,1.25*inch,CREAM); para(c,'Remember: the force is determined by the slope, not directly by whether U is positive or negative.',1.2*inch,3.0*inch,5.4*inch,body); para(c,'U = kq₁q₂/r    ;    F(r) = −dU/dr    ;    U_LJ = C₁₂/r¹² − C₆/r⁶',1.15*inch,2.68*inch,5.5*inch,eq); c.save()
def key_section(c,page,total,heading,concept,steps,equations):
    header(c,'Detailed Answer Key',page,total); y=H-1.02*inch
    c.setFillColor(TEAL); c.setFont('Arial-Bold',11); c.drawString(.68*inch,y,heading.upper()); y-=.25*inch
    box(c,.65*inch,y-2.42*inch,7.0*inch,2.42*inch,PALE); para(c,'Concepts needed: <b>'+concept+'</b>',.85*inch,y-.18*inch,6.6*inch,ans)
    yy=y-.48*inch
    for n,s in enumerate(steps,1): yy-=para(c,f'<b>{n}.</b> {s}',.85*inch,yy,6.5*inch,ans)+.08*inch
    ey=y-3.35*inch; box(c,.65*inch,ey-1.08*inch,7.0*inch,1.08*inch,CREAM); c.setFillColor(NAVY); c.setFont('Arial-Bold',8); c.drawString(.85*inch,ey-.18*inch,'EQUATIONS AND CHECKS'); yy=ey-.32*inch
    for s in equations: yy-=para(c,s,.85*inch,yy,6.5*inch,eq)+.04*inch
    if page < total: c.showPage()
def draw_key():
    c=canvas.Canvas(KEY,pagesize=letter); c.setTitle('Physics 2 Test 1 - Detailed Answer Key'); total=10
    key_section(c,1,total,'1a–d  Conductor concepts','electrostatic equilibrium; free-charge motion; conductor equipotential; surface charge; shielding',[
      'Assume a nonzero electric field remains inside the metal. A mobile charge would feel F=qE and continue to move, so equilibrium is impossible.',
      'Therefore the rearranged charges create a canceling field and the net interior field is zero. A Gaussian surface wholly inside the metal then encloses zero net charge.',
      'The conductor is an equipotential: a tangential potential difference would drive charge along the surface. Thus the field just outside is normal to the surface.',
      'Excess charge resides on the outer surface unless a cavity contains charge. Near a sharp point, surface charge density is larger and field lines crowd.',
      'Shielding follows directly: induced surface charge cancels the static field in a closed conducting interior.'
    ],['E<sub>metal</sub> = 0','E<sub>outside</sub> = σ/ε₀'])
    key_section(c,2,total,'1b–c  Clean field-line drawings','field-line geometry; surface normal; surface charge density',[
      'Draw the conductor outline first and leave the interior blank; no field line should pass through the conducting material.',
      'At every intersection with the surface, draw the line perpendicular to the local tangent. This enforces zero tangential field.',
      'For a spherical conductor in a uniform field, use straight lines far away and smoothly bent lines around the sphere, with larger crowding on the sides where induced charge is concentrated.',
      'For the irregular conductor, spread lines over broad regions and compress them near the pointed end. Lines never cross, and line density represents field magnitude.'
    ],['E<sub>⊥</sub> = σ/ε₀','field-line density ∝ |E|'])
    key_section(c,3,total,'2a  Net force on +8 μC','Coulomb law; one-dimensional sign convention; superposition',[
      'Set rightward force positive. The distance from q₁ to q₃ is a+b=0.09 m.',
      'Because q₁ and q₃ are both positive, q₁ repels q₃ to the right: F₃₁ = k|q₁q₃|/(a+b)² = 35.5 N.',
      'Because q₂ is negative and q₃ positive, q₂ attracts q₃ to the left: F₃₂ = k|q₂q₃|/b² = 88.1 N.',
      'Add signed components: F₃ = +35.5−88.1 = −52.6 N. The negative sign means 52.6 N left.'
    ],['F = k|q<sub>i</sub>q<sub>j</sub>|/r²','F<sub>net</sub> = ΣF<sub>i</sub>'])
    key_section(c,4,total,'2b–c  Symbolic fields and band diagrams','vector superposition; scalar potential; atomic levels; band formation',[
      'At P=(a,b), the source-to-point distances are r₁=√(a²+b²), r₂=a, and r₃=b.',
      'Resolve each electric field into x and y components. The diagonal charge contributes to both components; the left and bottom charges contribute along one axis each.',
      'Add components to obtain Eₚ. A charge q₄ at P experiences F₄=q₄Eₚ, so a negative q₄ reverses the field direction.',
      'Potential is scalar: add kq/r for each source without component resolution.',
      'For the drawing, show discrete levels for one atom, splitting into many nearby levels as atoms approach, then broad valence and conduction bands separated by a gap in the crystal.'
    ],['Eₚ = [kq₁a/(a²+b²)<sup>3/2</sup> + kq₂/a²]i + [kq₁b/(a²+b²)<sup>3/2</sup> + kq₃/b²]j','Vₚ = kq₁/√(a²+b²) + kq₂/a + kq₃/b'])
    key_section(c,5,total,'3a–b  Parallel plates and nonuniform sphere','Gauss law; planar symmetry; Newton’s second law; kinematics; spherical-shell integration',[
      'For plate area A=L², symmetry gives E=Q/(ε₀A)=Q/(ε₀L²). The particle’s vertical force is qE, so aᵧ=qQ/(ε₀mL²).',
      'The horizontal crossing time is t=L/v. With zero initial vertical velocity, Δy=½aᵧt²=qQ/(2ε₀mv²).',
      'For the sphere, a shell at radius r′ has dV=4πr′²dr′. Substitute ρ(r′)=ρ₀(r′/R)² to get dq=4πρ₀r′⁴dr′/R².',
      'Integrate from 0 to R: Q=(4πρ₀/R²)[r′⁵/5]₀ᴿ=4πρ₀R³/5. The radial dependence is why multiplying one density by total volume would be wrong.'
    ],['E = Q/(ε₀L²);  aᵧ = qQ/(ε₀mL²);  Δy = qQ/(2ε₀mv²)','Q = ∫ρ dV = 4πρ₀R³/5'])
    key_section(c,6,total,'4a–d  Mass-spring oscillator','Hooke law; mechanical energy conservation; turning points; graph interpretation',[
      'At maximum displacement x=A, speed is zero and all mechanical energy is spring potential: E=½kA²=½(100)(0.40)²=8.0 J.',
      'At equilibrium x=0, spring potential is zero, so ½mvₘₐₓ²=8.0. Thus vₘₐₓ=√(16/3.3)=2.20 m/s.',
      'At x=0.03 m, solve ½mv²+½kx²=E. This gives v=√[(16−100(0.03)²)/3.3]=2.20 m/s.',
      'Plot Uₛ=½kx² upward and K=E−Uₛ downward. Both meet at x=±A; K is largest and Uₛ smallest at x=0.'
    ],['E = ½kA² = 8.0 J','v(x) = √[(k/m)(A²−x²)] = 2.20 m/s'])
    key_section(c,7,total,'5  Sound-pressure level','rms pressure; intensity; logarithmic decibels; spherical spreading',[
      'Define sound-pressure level relative to the reference pressure p₀=20 μPa: Lₚ=20 log₁₀(pᵣₘₛ/p₀) dB.',
      'For a change, subtract the two levels so the reference cancels: ΔLₚ=20 log₁₀(p₂/p₁).',
      'If p₂=2p₁, ΔLₚ=20 log₁₀2=+6.02 dB. If p₂=½p₁, ΔLₚ=20 log₁₀(½)=−6.02 dB.',
      'The result is not ±2 dB because intensity scales as pressure squared: doubling pressure quadruples intensity, and 10 log₁₀4=6.02.',
      'The worksheet’s spherical-wave context also gives I=P/(4πr²), so intensity falls as 1/r² when no energy is absorbed.'
    ],['Lₚ = 20 log₁₀(pᵣₘₛ/p₀) dB','I ∝ pᵣₘₛ²;  I₂/I₁ = (p₂/p₁)²','I₂ = I₁(r₁/r₂)²'])
    key_section(c,8,total,'6  Bohr model, ions, and molecules','Bohr model; Coulomb force; centripetal acceleration; quantized states; ionization; valence electrons; electron clouds; molecular formulas',[
      'Draw the nucleus and allowed electron states. The classical force balance for hydrogen is an attraction toward the nucleus equal in magnitude to the required centripetal force.',
      'The balance is k e²/r² = mₑv²/r. It determines the speed for a chosen circular radius, while the quantum model adds the rule that only certain states are allowed.',
      'Ionization requires enough energy to move an electron from a bound state to an unbound state. The remaining atom has a deficit of negative charge and is positive.',
      'Sodium has one valence electron and commonly loses it to form Na⁺. Chlorine is one electron short of a filled outer shell and commonly gains one to form Cl⁻.',
      'An electron cloud shows probability rather than a fixed track. H₂ is diatomic; H₂O is triatomic. In multi-electron atoms, nucleus attraction and electron repulsion must be vector-added.'
    ],['k e²/r² = mₑv²/r','ionization: bound electron + energy → free electron + positive ion','molecular subscript = number of atoms'])
    key_section(c,9,total,'7  Polarization and displacement vector','electric dipole; polarization density; susceptibility; permittivity; free and bound charge',[
      'For charges ±q separated by vector d, define the dipole moment p=qd, directed from negative to positive charge. This is the microscopic building block.',
      'Sum all dipoles in volume V and divide by volume: P=(1/V)Σpᵢ. Aligned dipoles give a macroscopic polarization vector; random orientations can cancel.',
      'Start with the definition D=ε₀E+P. For a linear isotropic dielectric, the material response is P=ε₀χₑE, with dimensionless susceptibility χₑ.',
      'Substitute and factor: D=ε₀E+ε₀χₑE=ε₀(1+χₑ)E. Define ε=ε₀(1+χₑ), so D=εE.',
      'Draw E, P, and D collinear for the isotropic case, with dipoles aligned from negative toward positive. Keep E as the physical field and P as material response.'
    ],['p=qd','P=(1/V)Σpᵢ','D=ε₀E+P','P=ε₀χₑE','D=ε₀(1+χₑ)E=εE'])
    key_section(c,10,total,'8  Ions and molecular potential energy','potential energy; point-charge model; force as negative slope; Lennard–Jones terms; equilibrium stability',[
      'For point charges, write U(r)=kq₁q₂/r with U=0 at infinite separation. Like charges give positive U; opposite charges give negative U under this convention.',
      'Use F(r)=−dU/dr. Read the graph by its slope: a negative slope corresponds to outward positive radial force, a positive slope to inward force, and a horizontal minimum to F=0.',
      'Sketch a steep positive short-range wall, a negative attractive well at intermediate r, and an approach toward U=0 as r becomes large. Label the minimum as the equilibrium separation.',
      'The Lennard–Jones expression combines repulsion and attraction: C₁₂/r¹² dominates at short range, while −C₆/r⁶ supplies longer-range attraction.',
      'Na⁺ and Cl⁻ contain nuclei and electrons, so they are composite. A point-charge approximation is useful outside the charge distribution, but a realistic short-range model needs additional repulsive physics.'
    ],['U=kq₁q₂/r','F(r)=−dU/dr','U_LJ=C₁₂/r¹²−C₆/r⁶','at equilibrium: dU/dr=0'])
    c.setFillColor(MUTED); c.setFont('Arial',7); c.drawString(.65*inch,.58*inch,'Sources consulted: supplied worksheet scans; Young and Freedman, University Physics; OpenStax University Physics Volumes 1 and 2, Chapters 5–7, 15–17.'); c.save()
draw_test(); draw_key(); print(TEST); print(KEY)

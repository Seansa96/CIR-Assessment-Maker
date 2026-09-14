from pathlib import Path
import runpy
src=Path(r'C:\Users\SeanS\Downloads\cir_app\scratch\build_conceptual_focus_test_v2.py')
text=src.read_text(encoding='utf-8')
# Replace the compressed paragraph with a scan-friendly word-bank panel and one blank per line.
marker='def draw_test():'
wordbank=r'''def wordbank_page(c):
    header(c,'1. Electric-field word bank',2,12); y=H-1.03*inch
    p(c,'Fill each blank using the word bank. Terms may be used more than once; several are distractors. Cross out each term as you use it.',.75*inch,y,6.7*inch); y-=.62*inch
    box(c,.82*inch,y-1.02*inch,6.35*inch,1.02*inch,CREAM)
    p(c,'<b>WORD BANK</b><br/>source &nbsp;&nbsp; test &nbsp;&nbsp; enclosed &nbsp;&nbsp; external &nbsp;&nbsp; scalar &nbsp;&nbsp; vector<br/>tangent &nbsp;&nbsp; perpendicular &nbsp;&nbsp; inverse-square &nbsp;&nbsp; conserved &nbsp;&nbsp; canceled<br/>reinforced &nbsp;&nbsp; zero &nbsp;&nbsp; nonzero &nbsp;&nbsp; frequency &nbsp;&nbsp; wavelength',1.03*inch,y-.16*inch,5.95*inch,small); y-=1.37*inch
    qs=['a. The electric field is force per unit ______ charge.','b. Field direction is defined using a positive ______ charge.','c. The net electric field from several charges is a ______ sum.','d. In a conductor at electrostatic equilibrium, E inside the metal is ______.','e. Gauss flux depends on ______ charge.','f. Field lines meet a conductor surface ______.','g. Coulomb magnitude has an ______ dependence on distance.','h. Charge is ______ in an isolated system.','i. At a midpoint, symmetric components may be ______ or ______.','j. A field-line arrow tells the force direction for a ______ test charge.','k. If the system is not isolated, charge can cross the boundary but the enlarged system still has ______ charge.']
    for q in qs: y-=p(c,q,.9*inch,y,6.25*inch,body)+.12*inch
    box(c,.9*inch,1.0*inch,6.25*inch,.72*inch,PALE); p(c,'Briefly explain one answer: identify the physical principle, not just the vocabulary word.',1.1*inch,1.5*inch,5.85*inch,small); c.showPage()

'''
text=text.replace(marker,wordbank+marker)
old="test_page(c,2,'1. Electric-field word bank','Fill each blank using the word bank. Terms may be used more than once; several are distractors. Word bank: <b>source, test, enclosed, external, scalar, vector, tangent, perpendicular, inverse-square, conserved, canceled, reinforced, zero, nonzero, frequency, wavelength</b><br/><br/>a. The electric field is force per unit ______ charge. b. Field direction is defined using a positive ______ charge. c. The net electric field from several charges is a ______ sum. d. In a conductor at electrostatic equilibrium, E inside the metal is ______. e. Gauss flux depends on ______ charge. f. Field lines meet a conductor surface ______. g. Coulomb magnitude has an ______ dependence on distance. h. Charge is ______ in an isolated system. i. At a midpoint, symmetric components may be ______ or ______.')"
text=text.replace(old,'wordbank_page(c)')
tmp=Path(r'C:\Users\SeanS\Downloads\cir_app\scratch\_generated_conceptual_test_v5.py'); tmp.write_text(text,encoding='utf-8'); runpy.run_path(str(tmp))
# Compact the visual gap in every test page: draw the figure just after the question block.
old="""def test_page(c,n,title,content,visual=None):
    header(c,title,n,12); y=H-1.03*inch; p(c,content,.75*inch,y,6.7*inch)
    if visual: visual(c)
    c.showPage()"""
new="""def test_page(c,n,title,content,visual=None):
    header(c,title,n,12); y=H-1.03*inch; used=p(c,content,.75*inch,y,6.7*inch)
    if visual:
        # The drawing functions use a common 2-inch baseline; translate it upward
        # when the question block is short so the page does not have a dead zone.
        c.saveState(); c.translate(0, max(-0.25*inch, min(1.75*inch, 5.55*inch-used-3.05*inch)))
        visual(c); c.restoreState()
    c.showPage()"""
text=text.replace(old,new)
adds={
"i. At a midpoint, symmetric components may be ______ or ______.":"i. At a midpoint, symmetric components may be ______ or ______. j. A field line arrow tells the force direction for a ______ test charge. k. If the system is not isolated, charge can cross the boundary but the enlarged system still has ______ charge.",
"d. Explain why an external charge can change field values on a Gaussian surface without changing the net flux through it.":"d. Explain why an external charge can change field values on a Gaussian surface without changing the net flux through it. e. What is the difference between a field existing and a test charge experiencing a force? f. Why is E measured in N/C rather than newtons alone?",
"Then draw U<sub>s</sub>(x) and K(x) for an ideal mass-spring oscillator.":"Then draw U<sub>s</sub>(x) and K(x) for an ideal mass-spring oscillator. Also identify the sign of a and the direction of the restoring force at x<0. Explain why the period does not depend on amplitude in ideal SHM.",
"Select all correct statements and draw a labeled snapshot showing λ and A.":"Select all correct statements and draw a labeled snapshot showing λ and A. Then state what a fixed point on the medium does as the wave passes, and explain why a crest is not a material object moving through the medium.",
"Describe the qualitative amplitude trend.":"Describe the qualitative amplitude trend. Define resonance in terms of energy transfer, explain what damping changes, and state whether the natural frequency is set by the driving frequency or by the system.",
"Explain why changing source loudness does not necessarily change sound speed.":"Explain why changing source loudness does not necessarily change sound speed. Also distinguish amplitude, intensity, pitch, loudness, and timbre, and identify which of these a spectrum displays.",
"including the role of a medium.":"including the role of a medium. Explain why an electromagnetic wave can travel through vacuum while sound cannot, and state which quantities change and which stay continuous at a stationary boundary.",
"Draw vector contributions for (iii) and (iv).":"Draw vector contributions for (iii) and (iv). Then state what happens if the observation point is moved slightly off the midpoint, and explain why the inverse-square law alone cannot determine the answer for the two-charge cases.",
"e. For a sound wave, pitch is associated mainly with ______, while timbre depends on waveform and ______.":"e. For a sound wave, pitch is associated mainly with ______, while timbre depends on waveform and ______. f. Capacitance describes ______ per unit ______. g. A dipole in a uniform field can have zero net force but nonzero ______.",
"C. Explain how a sinusoidal wave’s mathematical form encodes amplitude, phase, wavelength, frequency, and direction.":"C. Explain how a sinusoidal wave’s mathematical form encodes amplitude, phase, wavelength, frequency, and direction. For every response, add one limiting-case prediction: far from a charge, at a conductor interior, at a turning point, or after entering a slower medium."
}
for a,b in adds.items(): text=text.replace(a,b)
# The question-page replacement above should not expand the dedicated word-bank
# list; keep each item in that list as its own separate line.
text=text.replace("i. At a midpoint, symmetric components may be ______ or ______. j. A field line arrow tells the force direction for a ______ test charge. k. If the system is not isolated, charge can cross the boundary but the enlarged system still has ______ charge.", "i. At a midpoint, symmetric components may be ______ or ______.")
keyadds={
"The repeated use of “test” and the two symmetry outcomes are deliberate checks against guessing from word frequency.":"The repeated use of “test” and the two symmetry outcomes are deliberate checks against guessing from word frequency. j. positive; k. conserved. A field is a source-created property of space; force is the interaction qE when a charge is placed there. N/C is force per charge, so newtons alone would omit the test-charge dependence.",
"Gauss law says external charge contributes as much inward and outward flux in aggregate": "Gauss law says external charge contributes as much inward and outward flux in aggregate. e. The field can exist with no test charge; the force is defined only after a charge is placed. f. Field is force divided by charge, so its unit must be N/C.",
"At x=0: speed is maximum, Us=0, and acceleration is zero.":"At x=0: speed is maximum, Us=0, and acceleration is zero. For x<0, acceleration and restoring force point right, toward equilibrium. Ideal SHM has an amplitude-independent period because the linear equation has a fixed omega; amplitude changes energy, not omega.",
"The particle’s transverse velocity can be larger or smaller than the wave speed": "The particle’s transverse velocity can be larger or smaller than the wave speed. A medium point oscillates about equilibrium while the pattern carries phase and energy; a crest is a location of the pattern, not a marked piece of matter.",
"the exact peak depends on damping.":"the exact peak depends on damping. Resonance is especially effective energy transfer when driving is near the system’s natural frequency. Damping lowers and broadens the response; natural frequency belongs to the system, not the driver.",
"Source loudness changes amplitude, not the medium’s stiffness": "Source loudness changes amplitude, not the medium’s stiffness. Amplitude is maximum displacement or pressure variation; intensity is power per area; pitch tracks frequency; loudness is perception; timbre tracks waveform and harmonic content. A spectrum displays amplitude versus frequency.",
"sound in air is longitudinal and requires a material medium.":"sound in air is longitudinal and requires a material medium. Electromagnetic waves do not require matter. At a stationary boundary, frequency remains source-set while speed and wavelength can change.",
"A zero result can arise from cancellation even though each individual contribution is nonzero.":"A zero result can arise from cancellation even though each individual contribution is nonzero. Off the midpoint, the exact symmetry cancellation is lost, so the geometry and component calculation are needed; inverse-square scaling alone is insufficient.",
"Timbre depends on waveform and harmonic spectrum": "Timbre depends on waveform and harmonic spectrum. f. Capacitance describes charge per unit potential difference. g. A dipole can have nonzero torque even when its uniform-field net force is zero.",
"Award full credit when the response states assumptions and checks direction or limiting behavior.":"Award full credit when the response states assumptions and checks direction or limiting behavior. Strong responses should also connect the requested limiting case to a concrete prediction rather than merely naming it."
}
for a,b in keyadds.items(): text=text.replace(a,b)
text=text.replace("Physics 2 Conceptual Focus Test - Version 2","Physics 2 Comprehensive Conceptual Test - Dense Version")
text=text.replace("Physics 2 | Version 2","Physics 2 | Dense Version")
text=text.replace("TEST=os.path.join(OUT,'Physics 2 Conceptual Focus Test - Version 2.pdf')","TEST=os.path.join(OUT,'Physics 2 Comprehensive Conceptual Test - Dense Version.pdf')")
text=text.replace("KEY=os.path.join(OUT,'Physics 2 Conceptual Focus Test - Version 2 Detailed Answer Key.pdf')","KEY=os.path.join(OUT,'Physics 2 Comprehensive Conceptual Test - Dense Version - Detailed Answer Key.pdf')")
tmp=Path(r'C:\Users\SeanS\Downloads\cir_app\scratch\_generated_conceptual_test_v4.py'); tmp.write_text(text,encoding='utf-8'); runpy.run_path(str(tmp))

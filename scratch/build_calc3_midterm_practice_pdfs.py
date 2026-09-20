from pathlib import Path
from xml.sax.saxutils import escape
import json

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, PageBreak, Spacer, Table,
    TableStyle, KeepTogether,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_B = Path(r"C:\Windows\Fonts\arialbd.ttf")
pdfmetrics.registerFont(TTFont("Arial", str(FONT)))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_B)))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ExamTitle", parent=styles["Title"], fontName="Arial-Bold", fontSize=22, leading=27, alignment=TA_CENTER, textColor=colors.HexColor("#17324d"), spaceAfter=14))
styles.add(ParagraphStyle(name="ExamSub", parent=styles["Normal"], fontName="Arial", fontSize=12, leading=17, alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle(name="ProblemTitle", parent=styles["Heading1"], fontName="Arial-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#17324d"), spaceAfter=10))
styles.add(ParagraphStyle(name="Question", parent=styles["BodyText"], fontName="Arial", fontSize=10.5, leading=15, spaceAfter=7))
styles.add(ParagraphStyle(name="Solution", parent=styles["BodyText"], fontName="Arial", fontSize=9.7, leading=13.4, spaceAfter=5))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName="Arial", fontSize=8.5, leading=11, textColor=colors.HexColor("#4a5560"), spaceAfter=5))


def P(text, style="Question"):
    return Paragraph(text.replace("\n", "<br/>"), styles[style])


EXAMS = {
    1: {
        "title": "Practice Exam 1",
        "problems": [
            ("Vectors and displacement", [
                "A survey drone travels from P=(-2,1,0) to Q=(1,5,-2), then to R=(4,2,3), with coordinates in meters.",
                "(a) Find the displacement vector for each leg and the net displacement. (b) Find the total path length and the straight-line distance from P to R. Explain why they differ. (c) Give a unit vector pointing in the net-displacement direction. (d) A map reports only the net displacement. State one piece of route information it cannot recover.",
            ], [
                "(a) PQ=<3,4,-2>, QR=<3,-3,5>, and PR=<6,1,3>; indeed PQ+QR=PR. (b) The traveled length is |PQ|+|QR|=sqrt(29)+sqrt(43) m. The endpoint distance is |PR|=sqrt(46) m. Path length accumulates both legs; displacement depends only on endpoints. (c) <6,1,3>/sqrt(46). (d) It does not determine the intermediate waypoint or the traveled path length.",
                "Partial credit (10): 3 for leg vectors; 2 for net vector; 2 for both lengths; 1 for explaining route vs endpoint; 1 for unit vector; 1 for a valid limitation.",
            ]),
            ("Dot products, projection, and work", [
                "A constant force F=<6,8,0> N acts on a crate while it moves through displacement d=<3,4,12> m. Resolve the force relative to the motion.",
                "(a) Find the work and explain its sign. (b) Find the scalar component of F along d and the vector projection of F onto d. (c) Determine cos(theta), where theta is the angle between F and d. Explain why the projection magnitude is not the work.",
            ], [
                "|d|=13, |F|=10, and F·d=18+32=50, so W=50 J (positive: force has a component along the motion). The scalar component is (F·d)/|d|=50/13 N. The vector projection is ((F·d)/(d·d))d=(50/169)<3,4,12> N. Finally cos(theta)=50/(10·13)=5/13. Work multiplies the along-motion force component by the displacement length; the projection is force, not energy.",
                "Partial credit (10): 2 for dot product/work and sign; 2 for scalar projection; 3 for vector projection; 1 for cosine; 2 for distinguishing units and meanings.",
            ]),
            ("Cross products and plane equations", [
                "Three noncollinear survey markers are A=(1,2,0), B=(3,1,1), and C=(0,4,2). A fourth marker is D=(2,2,4).",
                "(a) Find a normal to the plane through A, B, C and derive a Cartesian equation. (b) Find the area of parallelogram ABC formed by AB and AC. (c) Decide whether D lies in the plane, showing a test. (d) Explain how reversing the order in the cross product changes the geometry and what it does not change.",
            ], [
                "AB=<2,-1,1>, AC=<-1,2,2>. AB×AC=<-4,-5,3>, so a normal is <4,5,-3>. Through A: 4(x-1)+5(y-2)-3z=0, or 4x+5y-3z=14. The parallelogram area is |AB×AC|=sqrt(16+25+9)=5sqrt(2). At D, 4(2)+5(2)-3(4)=6, not 14, so D is not on the plane. Reversing the order negates the normal and orientation, but preserves its magnitude and the plane it determines.",
                "Partial credit (10): 2 for vectors; 2 for cross-product normal; 2 for plane; 1 for area; 1 for membership test; 2 for order interpretation.",
            ]),
            ("First and second partial derivatives", [
                "Let H(x,y)=2x²y-xy²+3x+5y model a local response surface. At (1,2), determine Hx, Hy, Hxx, Hxy, Hyx, and Hyy. Then state the local first-order change estimate for a small move (dx,dy)=(0.02,-0.01).",
            ], [
                "Holding y fixed: Hx=4xy-y²+3. Holding x fixed: Hy=2x²-2xy+5. Thus at (1,2), Hx=7 and Hy=3. Differentiate again: Hxx=4y=8, Hxy=4x-2y=0, Hyx=4x-2y=0, Hyy=-2x=-2. The first-order change is dH≈Hx dx+Hy dy=7(0.02)+3(-0.01)=0.11 response units. The mixed partials agree here.",
                "Partial credit (10): 2 for first partials; 4 for second/mixed partials; 2 for holding the other variable fixed; 2 for differential estimate.",
            ]),
            ("Differentials and approximation", [
                "A closed cylinder has total surface area S(r,h)=2πr²+2πrh. At r=3 cm and h=10 cm, manufacturing changes the radius by dr=0.02 cm and height by dh=-0.05 cm.",
                "(a) Estimate the change in surface area using the differential. (b) Estimate the relative percent change. (c) State whether the area rises or falls and explain why this is a local estimate rather than an exact change.",
            ], [
                "S_r=4πr+2πh and S_h=2πr. At (3,10), these are 32π and 6π. Therefore dS≈32π(0.02)+6π(-0.05)=0.34π cm²≈1.068 cm². Since S=78π, estimated relative change is (0.34π)/(78π)·100%≈0.436%. It rises because the radius increase effect exceeds the height decrease effect. The differential omits higher-order terms in dr and dh.",
                "Partial credit (10): 3 for partials; 2 for substitution and dS; 2 for relative percent; 1 for direction; 2 for explaining linearization.",
            ]),
            ("Multivariable chain rule", [
                "A response is C(x,y)=x²eʸ+sin(xy), where x=1+t² and y=2-t. Find dC/dt at t=1 using the multivariable chain rule. Show the point, partial derivatives, and inner derivatives. Check your result by differentiating C(x(t),y(t)) directly at t=1.",
            ], [
                "At t=1, (x,y)=(2,1), x'=2, y'=-1. Cx=2xeʸ+y cos(xy), Cy=x²eʸ+x cos(xy), so at (2,1) they are 4e+cos 2 and 4e+2cos 2. Thus dC/dt=2(4e+cos2)-(4e+2cos2)=4e. Direct check: x²eʸ=(1+t²)²e^(2-t), whose derivative at 1 is e(8-4)=4e. Also xy=(1+t²)(2-t), whose derivative at 1 is 2-2=0, so d/dt[sin(xy)]=cos(2)·0=0. Both routes give 4e.",
                "Partial credit (10): 2 for inner values/rates; 3 for correct partials; 2 for chain combination; 2 for direct check; 1 for identifying cancellation in the sinusoidal term.",
            ]),
            ("Gradient and directional derivative", [
                "An elevation model is Z(x,y)=100-x²-2xy-2y². At P=(1,-1), determine (a) the gradient, (b) the directional derivative toward Q=(4,3), (c) the unit direction of steepest increase and its rate, and (d) the direction of steepest decrease. Interpret the directional derivative in context.",
            ], [
                "∇Z=< -2x-2y,-2x-4y >, so ∇Z(1,-1)=<0,2>. The direction P→Q is <3,4>, hence u=<3/5,4/5>. D_u Z=∇Z·u=8/5 elevation units per horizontal unit, so elevation rises in that direction. Steepest increase points along ∇Z/|∇Z|=<0,1> at rate |∇Z|=2. Steepest decrease is <0,-1> at rate -2.",
                "Partial credit (10): 3 for gradient; 2 for normalizing the requested direction; 2 for directional rate and interpretation; 2 for steepest increase; 1 for steepest decrease.",
            ]),
            ("Critical points and optimization", [
                "A two-product shop models daily net profit by P(x,y)=32x+36y-2x²-2xy-3y², where x,y≥0 are production levels in units of 100 items and P is dollars in hundreds.",
                "(a) Find and classify the interior critical point using the second derivative test. (b) Explain why it is the unique global maximum on the feasible quadrant. (c) Compute and interpret the maximum modeled profit.",
            ], [
                "Px=32-4x-2y; Py=36-2x-6y. Setting both to zero gives 2x+y=16 and x+3y=18, hence (x,y)=(6,4), feasible. Hessian entries are Pxx=-4, Pxy=-2, Pyy=-6; D=24-4=20>0 and Pxx<0, so strict local maximum. The Hessian is negative definite everywhere (leading minor -4<0, determinant 20>0), so P is strictly concave and this critical point is the unique global maximum on the convex quadrant. P(6,4)=168, i.e. $16,800 at 600 and 400 items in the model's units.",
                "Partial credit (10): 3 for solving gradient equations; 2 for second derivative test; 2 for global argument; 2 for value; 1 for units/context.",
            ]),
            ("Optional bonus — variable-force work", [
                "A particle moves on the x-axis from x=0 m to x=2 m under force F(x)=<x eˣ,0,0> N. Find the work. Explain why a dot product with the displacement vector alone is not enough when the force varies, and show the integration method.",
            ], [
                "W=∫₀² F·dr=∫₀² xeˣ dx. Integration by parts with u=x, dv=eˣdx gives du=dx, v=eˣ, so W=[xeˣ]₀²-∫₀²eˣdx=2e²-(e²-1)=e²+1 J. A single constant-force dot product does not apply because F changes along the path.",
                "Partial credit (10): 2 for work integral; 3 for integration-by-parts setup; 3 for evaluation; 2 for explaining variable force.",
            ]),
        ],
    },
    2: {
        "title": "Practice Exam 2",
        "problems": [
            ("Vectors and displacement", [
                "An underwater robot travels from A=(0,2,1) to B=(3,-1,4), then to C=(-1,3,6), in meters.",
                "(a) Compute each leg displacement and net displacement. (b) Compare total path length with endpoint distance. (c) Give the net direction as a unit vector. (d) If the robot returns directly from C to A, what is the new displacement and what is the total distance of the closed trip? Explain the difference between a zero net displacement and zero distance.",
            ], [
                "AB=<3,-3,3>; BC=<-4,4,2>; AC=<-1,1,5>. Their sum is AC. |AB|=3sqrt(3), |BC|=6, |AC|=3sqrt(3). Path length A→B→C is 3sqrt(3)+6, while endpoint distance is 3sqrt(3). The unit net direction is <-1,1,5>/(3sqrt(3)). Returning C→A has displacement <1,-1,-5> and length 3sqrt(3), so the closed-trip distance is 6sqrt(3)+6. Net displacement is zero for the full loop, while distance is positive because motion occurred.",
                "Partial credit (10): 3 for displacements; 2 for length/distance; 1 for unit direction; 2 for return vector and distance; 2 for interpretation.",
            ]),
            ("Dot products, projection, and work", [
                "A force F=<-2,5,4> N acts during displacement d=<2,-1,2> m.",
                "(a) Compute the work and determine whether the force is mostly aligned or opposed to motion. (b) Find the scalar and vector projections of F onto d. (c) Find cos(theta) and classify the angle. (d) Explain how negative work can occur even though the force is nonzero.",
            ], [
                "F·d=-4-5+8=-1, so W=-1 J: the net component along motion opposes it. |d|=3 and d·d=9. Scalar projection is (F·d)/|d|=-1/3 N; vector projection is ((F·d)/(d·d))d=(-1/9)<2,-1,2>=<-2/9,1/9,-2/9> N. |F|=sqrt(45)=3sqrt(5), so cos(theta)=-1/(9sqrt(5))<0 and theta is obtuse. Nonzero force can have an opposing component, which removes energy from motion.",
                "Partial credit (10): 2 for work/sign; 2 scalar projection; 3 vector projection; 1 cosine/angle; 2 interpretation.",
            ]),
            ("Cross products and plane equations", [
                "A laser sheet is intended to pass through A=(0,1,2), B=(2,0,1), and C=(1,3,0). A sensor at D=(1,1,1) may be in the sheet.",
                "(a) Construct a normal and plane equation. (b) Find both the parallelogram and triangle areas determined by the three markers. (c) Test whether D lies in the plane. (d) Explain how you would detect if the first three markers were collinear using the same method.",
            ], [
                "AB=<2,-1,-1>, AC=<1,2,-2>. AB×AC=<4,3,5>, a normal. Through A gives 4x+3(y-1)+5(z-2)=0, or 4x+3y+5z=13. The parallelogram area is sqrt(16+9+25)=5sqrt(2); triangle area is half, 5sqrt(2)/2. At D, 4+3+5=12≠13, so D is outside the sheet. If the cross product were zero, the direction vectors would be parallel and the points collinear, so they would not define a unique plane.",
                "Partial credit (10): 2 vectors; 2 cross product; 2 plane; 2 areas; 1 membership; 1 collinearity criterion.",
            ]),
            ("First and second partial derivatives", [
                "Let f(s,t)=eˢ sin(t)+s t² describe a response surface. At (0,π/2), find fs, ft, fss, fst, fts, and ftt. State the estimated first-order response change for (ds,dt)=(0.01,-0.02).",
            ], [
                "fs=eˢsin t+t²; ft=eˢcos t+2st. Second derivatives: fss=eˢsin t; fst=eˢcos t+2t; fts=eˢcos t+2t; ftt=-eˢsin t+2s. At (0,π/2): fs=1+π²/4, ft=0, fss=1, fst=fts=π, ftt=-1. Thus df≈fs ds+ft dt=(1+π²/4)(0.01)≈0.0347 response units. The dt term is zero to first order at the specified point.",
                "Partial credit (10): 2 first partials; 4 second/mixed partials; 2 point evaluation; 2 differential estimate.",
            ]),
            ("Differentials and approximation", [
                "A cylindrical tank's full outside surface area is S(r,h)=2πr²+2πrh. At r=4 cm and h=7 cm, a redesign changes dr=-0.03 cm and dh=0.04 cm.",
                "(a) Estimate dS and its sign. (b) Estimate the relative percent change. (c) Explain which dimensional change dominates, and identify why multiplying the separate percentage changes would not correctly estimate the area change.",
            ], [
                "S_r=4πr+2πh=30π and S_h=2πr=8π at the given point. dS≈30π(-0.03)+8π(0.04)=-0.58π cm²≈-1.822 cm². Since S=88π, relative change≈-0.58/88·100%=-0.659%. The radius reduction dominates because its weighted contribution (-0.90π) exceeds the height contribution (+0.32π). Area depends jointly and nonlinearly on r,h, so combine partial-derivative contributions; multiplying dimension percentages ignores the model's sensitivities and cross terms.",
                "Partial credit (10): 3 for partials; 2 for dS; 2 relative change; 1 sign; 2 sensitivity explanation.",
            ]),
            ("Multivariable chain rule", [
                "Let T(x,y,z)=x²y+yz, where x=t²+1, y=3-t, and z=2t. Find dT/dt at t=1 by the multivariable chain rule. Then substitute first to obtain a single-variable expression and verify the result.",
            ], [
                "At t=1, x=y=z=2 and (x',y',z')=(2,-1,2). Tx=2xy=8, Ty=x²+z=6, Tz=y=2. Therefore dT/dt=8(2)+6(-1)+2(2)=14. Direct substitution: T=(t²+1)²(3-t)+2t(3-t). Differentiating and evaluating at 1 gives 14, matching the chain rule. The three paths contribute 16, -6, and 4.",
                "Partial credit (10): 2 point/rates; 3 partial derivatives; 2 chain sum; 2 direct check; 1 interpretation of paths.",
            ]),
            ("Gradient and directional derivative", [
                "A cost field is c(x,y)=3x²+y²-2xy. At P=(1,1), evaluate how cost changes toward Q=(-2,5). Also find the direction and rate of fastest local increase and the direction of fastest decrease.",
            ], [
                "∇c=<6x-2y,2y-2x>, so ∇c(1,1)=<4,0>. The direction toward Q is <-3,4>, giving unit vector u=<-3/5,4/5>. Directional derivative is ∇c·u=-12/5 units per distance, so cost locally decreases toward Q. Fastest increase is <1,0> at rate 4; fastest decrease is <-1,0> at rate -4. The target direction is not a descent direction because it has a negative dot product with the gradient.",
                "Partial credit (10): 3 gradient; 2 normalized direction; 2 directional rate/interpretation; 2 steepest directions; 1 max/min rates.",
            ]),
            ("Constrained optimization", [
                "A workshop's profit model is P(x,y)=22x+35y-x²-2xy-3y², with production x,y≥0 and capacity x+y≤10. Units of P are hundreds of dollars.",
                "(a) Find the unconstrained interior critical point and determine whether it is feasible. (b) Optimize P on the capacity edge x+y=10. (c) Check the other edges and vertices sufficiently to identify the constrained maximum. Explain why the unconstrained answer cannot simply be accepted.",
            ], [
                "Px=22-2x-2y and Py=35-2x-6y. Solving gives 2x+2y=22 and 2x+6y=35, so (x,y)=(31/4,13/4), whose sum is 11; it is infeasible. On y=10-x, 0≤x≤10: P=-2x²+27x+50. The vertex is x=27/4, y=13/4, with P=1129/8=141.125. Other edges: y=0 gives 22x-x², max 120 at x=10; x=0 gives 35y-3y², max 1225/12≈102.083 at y=35/6. Capacity-edge endpoints have values 50 and 50. Thus the constrained maximum is at (27/4,13/4), with modeled profit $14,112.50. Unconstrained calculus ignores feasibility and can select a prohibited production plan.",
                "Partial credit (10): 2 unconstrained solve/feasibility; 3 edge reduction/vertex; 2 other boundaries; 2 compare/classify maximum; 1 contextual value.",
            ]),
            ("Optional bonus — variable-force work", [
                "Along the x-axis from x=0 to x=π/2 m, a particle experiences force F(x)=<sin(x)cos(x),0,0> N. Find the work using substitution. Explain why the displacement vector alone does not determine work here.",
            ], [
                "W=∫₀^(π/2) sin(x)cos(x)dx. Let u=sin x, du=cos x dx; limits change from 0 to 1. Then W=∫₀¹u du=1/2 J. The force varies with position, so work accumulates as the along-path force component changes; a single constant-force dot product is not valid.",
                "Partial credit (10): 2 work integral; 3 substitution and limits; 3 evaluation; 2 explanation.",
            ]),
        ],
    },
}


def page_chrome(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setStrokeColor(colors.HexColor("#b8c3cc"))
    canvas.setLineWidth(0.5)
    canvas.line(0.65 * inch, h - 0.48 * inch, w - 0.65 * inch, h - 0.48 * inch)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#506070"))
    canvas.drawString(0.68 * inch, h - 0.38 * inch, "MAC-2313  |  MIDTERM PRACTICE")
    canvas.drawRightString(w - 0.68 * inch, 0.35 * inch, f"{doc.page}")
    canvas.restoreState()


def doc_for(path):
    doc = BaseDocTemplate(str(path), pagesize=letter, leftMargin=0.72 * inch, rightMargin=0.72 * inch, topMargin=0.68 * inch, bottomMargin=0.62 * inch, title=path.stem.replace("-", " ").title(), author="Original study material")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=page_chrome)])
    return doc


def cover(title, subtitle):
    story = [Spacer(1, 1.15 * inch), P("MAC-2313  |  CALCULUS III", "ExamSub"), P(title, "ExamTitle"), P(subtitle, "ExamSub"), Spacer(1, 0.45 * inch)]
    table = Table([["Name", "Date", "Score"] , ["________________________________", "____________", "________"]], colWidths=[3.4*inch, 1.8*inch, 1.4*inch], rowHeights=[0.32*inch, 0.42*inch])
    table.setStyle(TableStyle([("FONTNAME",(0,0),(-1,-1),"Arial"),("FONTSIZE",(0,0),(-1,-1),10),("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#506070")),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    story += [table, Spacer(1, 0.5 * inch), P("Eight core problems, 10 points each. One optional bonus problem is worth up to 10 additional points. Show your reasoning: a correct method with a small arithmetic error may earn partial credit.", "Question"), P("No formula sheet is provided. Assume the single-variable derivative and integral skills from Calculus I and substitution/integration by parts from Calculus II are available when useful. Exact answers are preferred unless an estimate is requested.", "Question"), P("Suggested practice: attempt the exam without notes, then use the separate answer key to diagnose method choices and reasoning. No time limit is specified.", "Question")]
    return story


def exam_story(number, exam):
    story = cover(exam["title"], "Original paper-style practice • no formula sheet")
    for i, (title, prompts, solution) in enumerate(exam["problems"], start=1):
        story.append(PageBreak())
        label = f"Problem {i}  |  {title}" if i <= 8 else f"{title}  |  10 optional points"
        story.append(P(label, "ProblemTitle"))
        story.append(P("Show enough work for partial credit. State units and interpret your result when relevant.", "Small"))
        for prompt in prompts:
            story.append(P(prompt))
        story.append(Spacer(1, 0.08*inch))
        for _ in range(9 if len(prompts) < 2 else 7):
            story.append(Spacer(1, 0.25*inch))
            line = Table([[""]], colWidths=[6.95*inch], rowHeights=[0.01*inch])
            line.setStyle(TableStyle([("LINEBELOW",(0,0),(-1,-1),0.35,colors.HexColor("#b5bdc5"))]))
            story.append(line)
    return story


def key_story():
    story = cover("Worked Answer Key", "Ordered reasoning and partial-credit checkpoints")
    for exam_num, exam in EXAMS.items():
        for i, (title, prompts, solution) in enumerate(exam["problems"], start=1):
            story.append(PageBreak())
            if i == 1:
                story.append(P(exam["title"], "ProblemTitle"))
            label = f"Problem {i}  |  {title}" if i <= 8 else f"{title}  |  Bonus"
            story.append(P(label, "ProblemTitle"))
            story.append(P("Solution:", "Small"))
            story.append(P(solution[0]))
            story.append(P("Partial-credit guidance:", "Small"))
            story.append(P(solution[1]))
    story.append(PageBreak())
    story += [P("Source and scope notes", "ProblemTitle"), P("The topic scope and format follow the supplied MAC-2313 Midterm Exam Details and Study Guide. Method alignment was checked against the locally imported OpenStax Calculus, Volume 3 (Chapter 2 and Sections 4.3–4.7) and the existing Stewart Calculus: Early Transcendentals, Sixth Edition source (Sections 12.2–12.5 and 14.3–14.7). The two optional work problems use standard substitution and integration by parts (Stewart §§5.5, 7.1). Problems and solutions here are original; no textbook exercise wording is reproduced.", "Solution"), P("Suggested point breakdowns support self-review and are not a substitute for an instructor's grading rubric.", "Solution")]
    return story


for n, exam in EXAMS.items():
    path = OUT / f"calc3-midterm-practice-exam-{n}.pdf"
    doc_for(path).build(exam_story(n, exam))

key_path = OUT / "calc3-midterm-practice-answer-key.pdf"
doc_for(key_path).build(key_story())

print("Created:")
for p in [OUT / "calc3-midterm-practice-exam-1.pdf", OUT / "calc3-midterm-practice-exam-2.pdf", key_path]:
    print(f"{p} ({p.stat().st_size} bytes)")

topic_sources = {
    "Vectors and displacement": ["src-20260919140119-6feec9e9e6:page-0130"],
    "Dot products, projection, and work": ["src-20260919140119-6feec9e9e6:page-0141", "src-20260919140119-6feec9e9e6:page-0148", "src-20260919140119-6feec9e9e6:page-0152"],
    "Cross products and plane equations": ["src-20260919140119-6feec9e9e6:page-0164", "src-20260919140119-6feec9e9e6:page-0186"],
    "First and second partial derivatives": ["src-20260919140119-6feec9e9e6:page-0340", "src-20260919140119-6feec9e9e6:page-0346"],
    "Differentials and approximation": ["src-20260919140119-6feec9e9e6:page-0365"],
    "Multivariable chain rule": ["src-20260919140119-6feec9e9e6:page-0376"],
    "Gradient and directional derivative": ["src-20260919140119-6feec9e9e6:page-0385"],
    "Critical points and optimization": ["src-20260919140119-6feec9e9e6:page-0399", "src-20260919140119-6feec9e9e6:page-0407"],
    "Constrained optimization": ["src-20260919140119-6feec9e9e6:page-0399", "src-20260919140119-6feec9e9e6:page-0407"],
}
stewart_bonus = ["src-20260719182540-a40fdcd443:page-0429", "src-20260719182540-a40fdcd443:page-0483"]
blueprints = []
for exam_num, exam in EXAMS.items():
    for i, (title, prompts, solution) in enumerate(exam["problems"], start=1):
        sources = stewart_bonus if i == 9 else topic_sources[title]
        blueprints.append({
            "id": f"calc3-midterm-practice-exam-{exam_num}-q{i:03d}-blueprint",
            "assessmentId": f"calc3-midterm-practice-exam-{exam_num}",
            "questionId": f"q{i:03d}",
            "topic": title,
            "sourceChunkIds": sources,
            "reviewState": "approved",
            "difficultyTier": "hard",
            "difficultyDimensions": ["modelOrDerivation", "representationTransfer", "interpretationOrErrorDiagnosis"],
            "transferObjective": "Choose and connect calculus methods in an unfamiliar applied setting; interpret the result and justify the method.",
            "prompt": " ".join(prompts),
            "solutionEvidence": solution[0],
            "partialCredit": solution[1],
            "verification": "Independently recomputed algebra, derivatives, integrals, units, feasibility, and interpretation against the prompt.",
            "variationAxes": ["scenario and coordinate data", "requested interpretation", "method comparison or constraint"],
            "originalityNote": "Original scenario and wording; source used for concept scope and method alignment only."
        })
blueprint_doc = {
    "schemaVersion": 1,
    "id": "calc3-midterm-practice-v1",
    "categoryId": "calculus-3",
    "topicId": "calc3-comprehensive-review",
    "packetId": "packet-calc3-midterm-practice-v1",
    "reviewState": "approved",
    "blueprints": blueprints,
}
blueprint_path = ROOT / "docs" / "assessment-reference" / "question-blueprints" / "calc3-midterm-practice-v1.yaml"
blueprint_path.parent.mkdir(parents=True, exist_ok=True)
blueprint_path.write_text(json.dumps(blueprint_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{blueprint_path} ({len(blueprints)} blueprints)")

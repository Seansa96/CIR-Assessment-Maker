"""Build the original 150-item Chapter 9 circle question bank."""
from pathlib import Path
from fractions import Fraction
import math, yaml

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'docs/assessment-reference/aops-volume-1/chapter-09-circles-introduction-question-bank.yaml'
items=[]

def add(concept,difficulty,prompt,answer,outline,trap,archetype):
    n=len(items)+1
    items.append({'id':f'aops-v1-ch09-q{n:03d}','concept':concept,'skillIds':[concept],
                  'archetype':archetype,'difficulty':difficulty,'questionType':'multipleChoice',
                  'source':'original-authoring','prompt':prompt,'answer':str(answer),
                  'solutionOutline':outline,'commonTrap':str(trap),
                  'intendedAssessmentUse':['quiz','test']})

# Foundational: ten deliberately varied instances of five core representations.
radii=[3,4,5,6,7,8,9,10,12,15]
for i,r in enumerate(radii):
    stems=[f'A circle has radius {r}. Determine its diameter.',f'A compass is opened to {r} cm. What diameter will the circle have?',f'The distance from center O to boundary point A is {r}. Find a diameter length.',f'A wheel has radius {r} units. How far apart are opposite endpoints of a diameter?',f'Circle O has OA={r}. If AB passes through O and both endpoints lie on the circle, find AB.']
    add('circle-definitions','foundational',stems[i%5],2*r,'A diameter consists of two collinear radii, so d=2r.',r,'radius-diameter')
for i,r in enumerate(radii):
    stems=[f'Find the circumference of a radius-{r} circle in exact form.',f'A circular track has radius {r} m. What is one lap length?',f'Circle O has diameter {2*r}. Compute its circumference.',f'A disk has boundary radius {r}. Give the boundary length in terms of pi.',f'What exact length of wire surrounds a circular frame of radius {r}?']
    add('circumference-and-area','foundational',stems[i%5],f'{2*r} pi',f'Use C=2*pi*r: 2*pi*{r}={2*r}*pi.',f'{r*r} pi','circumference')
for i,r in enumerate(radii):
    stems=[f'Find the area of a disk with radius {r}.',f'A circular tile has radius {r} cm. What surface area does it cover?',f'Circle O bounds a region with OA={r}. Find the region area.',f'A radius-{r} sprinkler covers a full disk. Give its exact coverage area.',f'Compute the area enclosed by a circle of diameter {2*r}.']
    add('circumference-and-area','foundational',stems[i%5],f'{r*r} pi',f'Use A=pi*r^2: pi*{r}^2={r*r}*pi.',f'{2*r} pi','disk-area')
angles=[30,45,60,72,90,120,135,144,150,180]
for i,(r,a) in enumerate(zip(radii,angles)):
    num=Fraction(a,360)*2*r
    coeff=f'{num.numerator}/{num.denominator}' if num.denominator>1 else str(num.numerator)
    stems=[f'A radius-{r} circle has a {a}-degree central angle. Find its arc length in terms of pi.',f'What fraction and exact length of a radius-{r} circumference is subtended by {a} degrees?',f'Minor arc AB belongs to central angle {a} degrees in a circle of radius {r}. Find arc AB.',f'A wheel of radius {r} turns through {a} degrees. How far does a rim point travel?',f'Find the curved boundary of a {a}-degree sector of radius {r}.']
    add('arcs-and-sectors','foundational',stems[i%5],f'{coeff} pi',f'Multiply circumference 2*pi*{r} by {a}/360.',f'{a*r} pi','arc-length')
for i,(r,a) in enumerate(zip(radii,angles)):
    num=Fraction(a,360)*r*r
    coeff=f'{num.numerator}/{num.denominator}' if num.denominator>1 else str(num.numerator)
    stems=[f'Find the area of a {a}-degree sector in a radius-{r} circle.',f'A {a}-degree slice is cut from a disk of radius {r}. What is its exact area?',f'Central angle {a} degrees bounds a sector of radius {r}. Determine the sector area.',f'What fraction of a radius-{r} disk, and hence what area, belongs to {a} degrees?',f'A circular panel of radius {r} is painted over a {a}-degree sector. Find the painted area.']
    add('arcs-and-sectors','foundational',stems[i%5],f'{coeff} pi',f'Multiply disk area pi*{r}^2 by {a}/360.',f'{2*r} pi','sector-area')

# Intermediate: scaling, regions, chords, tangents, and equal tangent algebra.
scales=[(2,18),(3,7),(4,5),(1.5,32),(2.5,16),(0.5,80),(1.2,50),(0.75,64),(5,3),(10,2)]
for i,(k,a) in enumerate(scales):
    val=a*k*k
    add('circle-similarity-and-scaling','intermediate',f'A circle with area {a} square units is dilated by linear factor {k}. Find the image area.',f'{val:g}',f'Area uses the square factor: {a}*({k})^2={val:g}.',f'{a*k:g}','area-scaling')
outer=[(5,3),(7,4),(10,6),(13,5),(15,9),(9,8),(12,10),(20,16),(25,7),(11,2)]
for R,r in outer:
    val=R*R-r*r
    add('circumference-and-area','intermediate',f'Concentric circles have radii {R} and {r}. Find the area between them in terms of pi.',f'{val} pi',f'Subtract disk areas: pi({R}^2-{r}^2)={val}*pi.',f'{R*R+r*r} pi','annulus-area')
chords=[(5,6),(10,16),(13,10),(13,24),(15,18),(17,16),(17,30),(25,14),(25,40),(26,20)]
for R,c in chords:
    half=c//2
    d=int(math.isqrt(R*R-half*half))
    add('chords-and-center','intermediate',f'In a radius-{R} circle, a chord of length {c} is perpendicular to a segment from the center. Find the center-to-chord distance.',d,f'The perpendicular bisects the chord. Use d^2+{half}^2={R}^2, giving d={d}.',R-half,'chord-distance')
tans=[(5,13),(7,25),(8,17),(9,15),(12,13),(12,37),(15,17),(16,20),(20,29),(24,25)]
for r,h in tans:
    t=int(math.isqrt(h*h-r*r))
    add('tangents-and-radius','intermediate',f'Point P is {h} units from center O of a radius-{r} circle. Tangent PT touches at T. Find PT.',t,f'OT is perpendicular to PT, so PT=sqrt({h}^2-{r}^2)={t}.',h-r,'tangent-length')
eqs=[(2,3,4,9),(3,1,5,9),(4,2,6,12),(5,7,8,19),(6,1,9,13),(7,5,10,20),(8,2,12,18),(9,4,11,14),(10,3,15,23),(12,8,16,24)]
for a,b,c,d in eqs:
    x=Fraction(d-b,a-c)
    add('equal-tangents','intermediate',f'Two tangents from one external point have lengths {a}x+{b} and {c}x+{d}. Find x.',str(x),f'Equal tangents give {a}x+{b}={c}x+{d}; solving yields x={x}.',str(Fraction(d+b,a+c)),'equal-tangent-equation')

# Advanced: synthesis and proof selection.
ext=[22,34,40,46,50,58,64,70,76,88]
for a in ext:
    add('tangent-central-angle','advanced',f'Two tangents from P touch a circle at A and B. If angle APB is {a} degrees, find minor central angle AOB.',180-a,f'Radii OA and OB create two right angles in OAPB, so the remaining angles are supplementary: AOB=180-{a}.',360-a,'two-tangent-angle')
for r in radii:
    add('chords-and-center','advanced',f'Among all chords of a radius-{r} circle, what is the greatest possible chord length, and when is it attained?',f'{2*r}, when the chord is a diameter',f'A chord is longest when its distance from the center is zero; then it is a diameter of length {2*r}.',f'{r}, for every chord','maximum-chord')
proofs=[
('A segment from center O is perpendicular to chord AB. What conclusion is justified?','It bisects AB','The perpendicular-from-center chord theorem gives equal half-chords.','It makes AB a diameter'),
('M is the midpoint of chord AB in a circle centered O. What conclusion is justified?','OM is perpendicular to AB','Use the converse center-to-chord theorem.','OM is a tangent'),
('A line through circle point T is perpendicular to radius OT. What conclusion follows?','The line is tangent at T','Use the converse tangent-radius theorem.','The line is a diameter'),
('Tangents PA and PB leave the same external point. What equality can be proved?','PA=PB','Right triangles OAP and OBP are congruent by hypotenuse-leg.','OA=PB'),
('Why do radii OA and OB make triangle AOB isosceles?','OA and OB are radii of the same circle','All chords have equal length.','The diagram is symmetric'),
('Which auxiliary line is best when a tangent touches at T and a right triangle is needed?','Draw radius OT','Draw an unrelated chord.','Assume the tangent is a diameter'),
('What missing hypothesis is needed before saying a center-to-chord segment bisects the chord?','The segment is perpendicular to the chord','The chord is horizontal.','The segment is shorter than the radius'),
('A chord appears to pass through the center but has no incidence mark. What may be concluded?','Nothing about it being a diameter','It is a diameter.','It is tangent'),
('Which check rejects a claimed tangent length greater than the center-to-external-point distance?','A leg of a right triangle must be shorter than its hypotenuse','Tangents always equal radii.','Arc measures must sum to 180'),
('A proof establishes a line meets a circle at one point and is perpendicular to the contact radius. What is the exact conclusion?','The line is tangent at that contact point','The radius is a chord.','The circle is a disk')]
for p,a,o,t in proofs: add('circle-proof-strategy','advanced',p,a,o,t,'theorem-selection')
coords=[(3,4,5),(5,12,13),(8,15,17),(7,24,25),(9,12,15),(12,16,20),(20,21,29),(10,24,26),(18,24,30),(16,30,34)]
for x,y,r in coords:
    add('coordinate-circle','advanced',f'Point A=({x},{y}) lies on a circle centered at the origin. Find the circle radius and area.',f'r={r}; area={r*r} pi',f'Radius is OA=sqrt({x}^2+{y}^2)={r}; area is pi*{r}^2.',f'r={x+y}; area={(x+y)**2} pi','coordinate-radius-area')
composite=[(6,60),(8,90),(10,120),(12,150),(14,180),(15,72),(18,200),(20,225),(21,240),(24,300)]
for r,a in composite:
    rem=Fraction(360-a,360)*r*r
    coeff=f'{rem.numerator}/{rem.denominator}' if rem.denominator>1 else str(rem.numerator)
    add('arcs-and-sectors','advanced',f'A radius-{r} disk has a {a}-degree sector removed. Find the remaining area in terms of pi.',f'{coeff} pi',f'The remaining fraction is (360-{a})/360; multiply by {r*r}*pi.',f'{Fraction(a,360)*r*r} pi','removed-sector')

assert len(items)==150
data={'metadata':{'id':'aops-v1-ch09-circles-introduction-bank','chapter':9,'topicIds':['aops-circles-introduction'],'status':'complete','minimumRequiredItems':150,'sourcePageRange':'pdf 95-97; printed 81-83','difficultyDistribution':{'foundational':50,'intermediate':50,'advanced':50}},'items':items}
TARGET.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=1000),encoding='utf-8')
print(f'wrote {len(items)} items to {TARGET}')

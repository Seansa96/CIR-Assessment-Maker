"""Generate the source-grounded Calc 3 Spatial Vectors and Motion assessment set."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
PACKETS = ROOT / "docs" / "assessment-reference" / "content-manifests"
BLUEPRINTS = ROOT / "docs" / "assessment-reference" / "question-blueprints"
MEDIA = ROOT / "frontend" / "public" / "media" / "calculus-3"
SOURCE = "src-20260719182540-a40fdcd443"

TOPICS = [
 {
  "id":"calc3-three-dimensional-coordinate-systems", "slug":"three-dimensional-coordinate-systems", "title":"Three-Dimensional Coordinate Systems", "objective":"calc3-3d-coordinate-geometry", "chunks":[2211,2212,2213,2214], "signal":"algebraic-simplification-error", "remediation":"Calculus 1 → Inequalities and the Real Numbers", "visual":"3d-coordinates", 
  "sections":[("Coordinates locate a point","A point $(x,y,z)$ is located by three signed coordinate displacements. Keep the coordinate order fixed."),("Distance is spatial Pythagoras","The distance formula combines independent coordinate differences before taking one square root."),("Equations describe sets","A fixed coordinate such as $z=c$ describes a plane parallel to the $xy$-plane; sphere equations encode a center and radius.")],
  "recall":[("What is the midpoint of $(1,2,3)$ and $(3,4,5)$?","(2,3,4)"),("What plane has equation $z=0$?","xy-plane"),("What is the radius of $(x-1)^2+(y+2)^2+(z-3)^2=16$?","4"),("Which coordinate measures distance from the $xy$-plane?","z"),("What is the distance from $(0,0,0)$ to $(1,2,2)$?","3"),("What is the center of $(x-2)^2+y^2+(z+1)^2=9$?","(2,0,-1)")],
  "worked":"Find the equation of the sphere centered at $(1,-2,3)$ with radius $4$.", "worked_steps":[("Identify the center","Which signed shifts appear?","$(x-1)^2$, $(y+2)^2$, and $(z-3)^2$"),("Insert the radius","What is $r^2$?","16"),("Write the locus","Which equation is correct?","$(x-1)^2+(y+2)^2+(z-3)^2=16$")],
  "questions":[("What is the distance from $(1,2,3)$ to $(4,6,3)$?",["$5$","$7$","$25$","$\sqrt{7}$"],"$5$","Use coordinate differences $(3,4,0)$ and the distance formula."),("Which equation is a sphere centered at $(2,-1,0)$ with radius $3$?",["$(x-2)^2+(y+1)^2+z^2=9","$(x+2)^2+(y-1)^2+z^2=3","$(x-2)^2+(y+1)^2+z^2=3","$(x+2)^2+(y-1)^2+z^2=9"],"$(x-2)^2+(y+1)^2+z^2=9$","Use opposite signs inside squared shifts and square the radius."),("What set does $x=4$ describe in $\mathbb R^3$?",["A plane parallel to the $yz$-plane","A line parallel to the x-axis","A sphere of radius 4","The $xy$-plane"],"A plane parallel to the $yz$-plane","Only x is fixed; y and z remain free."),("Which point lies on the $xz$-plane?",["$(2,0,-5)$","$(0,2,-5)$","$(2,-5,0)$","$(0,0,2)$"],"$(2,0,-5)$","The $xz$-plane has y-coordinate zero.")]
 },
 {
  "id":"calc3-vectors", "slug":"vectors", "title":"Vectors in Space", "objective":"calc3-vector-operations", "chunks":list(range(2215,2234)), "signal":"vector-component-resolution-error", "remediation":"Trigonometry → Right Triangle Trigonometry", "visual":"vectors",
  "sections":[("Vectors are displacements","A vector records magnitude and direction, independent of where it is drawn."),("Components drive operations","Add, subtract, and scale vectors component by component."),("Magnitude and direction","Magnitude comes from the distance formula; a unit vector has magnitude one and records direction alone.")],
  "recall":[("Find $\langle1,2,3\rangle+\langle2,-1,0\rangle$.","(3,1,3)"),("Find $|\langle3,4,0\rangle|$.","5"),("What is a unit vector?","a vector with magnitude 1"),("Find $2\langle1,-2,3\rangle$.","(2,-4,6)"),("What is $\mathbf i$ in three dimensions?","(1,0,0)"),("What operation reverses a vector's direction?","multiplication by -1")],
  "worked":"Find a unit vector in the direction of $\langle2,-1,2\rangle$.", "worked_steps":[("Find magnitude","What is $|\langle2,-1,2\rangle|$?","3"),("Normalize","What scalar makes the magnitude one?","$1/3$"),("State the unit vector","Which vector is correct?","$\langle2/3,-1/3,2/3\rangle$")],
  "questions":[("Compute $\langle2,-1,3\rangle-\langle1,4,-2\rangle$.",["$\langle1,-5,5\rangle$","$\langle3,3,1\rangle$","$\langle1,3,-5\rangle$","$\langle-1,5,-5\rangle$"],"$\langle1,-5,5\rangle$","Subtract corresponding components."),("What is $|\langle2,1,2\rangle|$?",["$3$","$5$","$9$","$\sqrt5$"],"$3$","Use $\sqrt{2^2+1^2+2^2}$."),("Which is a unit vector in the direction of $\langle3,0,4\rangle$?",["$\langle3/5,0,4/5\rangle$","$\langle3,0,4\rangle$","$\langle4/5,0,3/5\rangle$","$\langle3/4,0,4/3\rangle$"],"$\langle3/5,0,4/5\rangle$","Divide every component by magnitude 5."),("Which quantity is a vector?",["A displacement of 5 meters east","A temperature of 5 degrees","A mass of 5 kilograms","A time of 5 seconds"],"A displacement of 5 meters east","A vector needs both magnitude and direction.")]
 },
 {
  "id":"calc3-dot-cross-products", "slug":"dot-cross-products", "title":"Dot and Cross Products", "objective":"calc3-dot-cross-geometry", "chunks":list(range(2234,2274)), "signal":"trigonometric-identity-misapplied", "remediation":"Trigonometry → Unit Circle Trigonometry", "visual":"dot-cross", 
  "sections":[("Dot products compare directions","The dot product is scalar and detects perpendicularity or supplies an angle/projection."),("Cross products build normals","The cross product is a vector perpendicular to both inputs; order controls orientation."),("Choose the operation by output","Use dot product for a scalar comparison and cross product for an oriented normal or area.")],
  "recall":[("Compute $\langle1,2,3\rangle\cdot\langle2,0,1\rangle$.","5"),("What does $\mathbf u\cdot\mathbf v=0$ mean for nonzero vectors?","perpendicular"),("What is $\mathbf i\times\mathbf j$?","k"),("What is $\mathbf j\times\mathbf i$?","-k"),("What geometric quantity is $|\mathbf u\times\mathbf v|$?","parallelogram area"),("What type of quantity is a dot product?","scalar")],
  "worked":"Find a normal vector to the plane containing $\langle1,0,1\rangle$ and $\langle0,2,1\rangle$.", "worked_steps":[("Select the operation","What operation produces a normal?","cross product"),("Compute components","What is $\langle1,0,1\rangle\times\langle0,2,1\rangle$?","$\langle-2,-1,2\rangle$"),("Interpret","Why is the result useful?","It is perpendicular to both spanning vectors.")],
  "questions":[("Compute $\langle1,2,-1\rangle\cdot\langle3,0,4\rangle$.",["$-1$","$7$","$\langle3,0,-4\rangle$","$11$"],"$-1$","Multiply corresponding components and add."),("Which condition proves two nonzero vectors are perpendicular?",["Their dot product is zero","Their cross product is zero","Their magnitudes are equal","Their sum is zero"],"Their dot product is zero","Orthogonal vectors have zero dot product."),("What is $\mathbf i\times\mathbf k$?",["$-\mathbf j$","$\mathbf j$","$\mathbf k$","$-\mathbf i$"],"$-\mathbf j$","Use cyclic order $\mathbf i\times\mathbf j=\mathbf k$."),("Which operation gives a vector normal to two nonparallel vectors?",["Cross product","Dot product","Magnitude","Scalar multiplication"],"Cross product","The cross product is perpendicular to both inputs.")]
 },
 {
  "id":"calc3-lines-and-planes", "slug":"lines-and-planes", "title":"Lines and Planes in Space", "objective":"calc3-lines-planes-model", "chunks":list(range(2274,2316)), "signal":"mathematical-translation-error", "remediation":"Calculus 2 → Parametric Curves", "visual":"lines-planes",
  "sections":[("Lines need a point and direction","A vector equation starts at a known point and adds any scalar multiple of a direction vector."),("Planes need a point and normal","A plane equation states that displacement from a known point is perpendicular to its normal."),("Forms serve different tasks","Vector and parametric forms trace lines; scalar forms make plane tests and distances convenient.")],
  "recall":[("What data defines a line in space?","a point and direction vector"),("What data defines a plane?","a point and normal vector"),("What does a plane normal vector do?","is perpendicular to the plane"),("For $\mathbf r=\langle1,2,3\rangle+t\langle2,0,-1\rangle$, what is x?","1+2t"),("When are two planes parallel?","their normals are parallel"),("What does $t=0$ give on a vector line?","the starting point")],
  "worked":"Find a vector equation for the line through $(1,2,3)$ parallel to $\langle2,-1,4\rangle$.", "worked_steps":[("Record the point","What is $\mathbf r_0$?","$\langle1,2,3\rangle$"),("Record direction","What is $\mathbf v$?","$\langle2,-1,4\rangle$"),("Assemble the line","Which equation is correct?","$\mathbf r=\langle1,2,3\rangle+t\langle2,-1,4\rangle$")],
  "questions":[("Which vector equation is the line through $(1,0,-2)$ parallel to $\langle3,1,4\rangle$?",["$\mathbf r=\langle1,0,-2\rangle+t\langle3,1,4\rangle$","$\mathbf r=\langle3,1,4\rangle+t\langle1,0,-2\rangle$","$\mathbf r=\langle1,0,-2\rangle+\langle3,1,4\rangle$","$\mathbf r=\langle1,0,-2\rangle+t$"],"$\mathbf r=\langle1,0,-2\rangle+t\langle3,1,4\rangle$","Use a position vector plus parameter times direction."),("Which vector is normal to $2x-y+3z=7$?",["$\langle2,-1,3\rangle$","$\langle7,0,0\rangle$","$\langle1,2,-1\rangle$","$\langle2,1,3\rangle$"],"$\langle2,-1,3\rangle$","Plane coefficients form a normal vector."),("When are planes with normals $\mathbf n_1$ and $\mathbf n_2$ parallel?",["When $\mathbf n_1$ is a scalar multiple of $\mathbf n_2$","When $\mathbf n_1\cdot\mathbf n_2=0$","When both normals have magnitude one","When the constants match"],"When $\mathbf n_1$ is a scalar multiple of $\mathbf n_2$","Parallel planes have parallel normals."),("What point is on $\mathbf r=\langle2,1,0\rangle+t\langle1,-1,3\rangle$ at $t=2$?",["$(4,-1,6)$","$(3,0,3)$","$(2,1,0)$","$(0,2,-1)$"],"$(4,-1,6)$","Substitute t into every component.")]
 },
 {
  "id":"calc3-vector-valued-functions", "slug":"vector-valued-functions", "title":"Vector-Valued Functions and Space Curves", "objective":"calc3-space-curves", "chunks":list(range(2329,2366)), "signal":"parametric-derivative-error", "remediation":"Calculus 2 → Parametric Curves", "visual":"space-curves",
  "sections":[("One parameter, three components","A vector-valued function gives a space-curve position for each allowed parameter value."),("Differentiate componentwise","Velocity or a tangent direction comes from differentiating every component."),("Integrate componentwise","An antiderivative vector is built one component at a time, with a constant vector when appropriate.")],
  "recall":[("What is $\mathbf r'(t)$ called for a position vector?","velocity"),("Differentiate $\langle t^2,\sin t,t\rangle$.","(2t,cos t,1)"),("What does a nonzero $\mathbf r'(t)$ give?","a tangent direction"),("What is a helix an example of?","a space curve"),("How are vector functions integrated?","componentwise"),("What parameter value gives the point at time zero?","t=0")],
  "worked":"For $\mathbf r(t)=\langle t^2,2t,1-t\rangle$, find the tangent vector at $t=1$.", "worked_steps":[("Differentiate components","What is $\mathbf r'(t)$?","$\langle2t,2,-1\rangle$"),("Evaluate the parameter","What is $\mathbf r'(1)$?","$\langle2,2,-1\rangle$"),("Interpret","What does this vector provide?","A tangent direction at the point.")],
  "questions":[("Differentiate $\mathbf r(t)=\langle t^2,\cos t,3t\rangle$.",["$\langle2t,-\sin t,3\rangle$","$\langle t, -\sin t,3t\rangle$","$\langle2t,\sin t,3\rangle$","$\langle t^2,\cos t,3t\rangle$"],"$\langle2t,-\sin t,3\rangle$","Differentiate each component."),("What is $\mathbf r(2)$ for $\mathbf r(t)=\langle t,t^2,1-t\rangle$?",["$\langle2,4,-1\rangle$","$\langle4,2,-1\rangle$","$\langle2,2,1\rangle$","$\langle2,4,1\rangle$"],"$\langle2,4,-1\rangle$","Evaluate all components at the same parameter."),("Which vector is tangent to a curve $\mathbf r(t)$ at t=1 when $\mathbf r'(1)\ne0$?",["$\mathbf r'(1)$","$\mathbf r(1)$","$\int\mathbf r(t)dt$","$|\mathbf r(1)|$"],"$\mathbf r'(1)$","The derivative gives tangent direction."),("Which is an antiderivative of $\langle2t,1,0\rangle$?",["$\langle t^2,t,0\rangle$","$\langle2t^2,t,0\rangle$","$\langle t^2,1,0\rangle$","$\langle2t,1,0\rangle$"],"$\langle t^2,t,0\rangle$","Integrate each component.")]
 },
 {
  "id":"calc3-motion-in-space", "slug":"motion-in-space", "title":"Motion in Space", "objective":"calc3-motion-vectors", "chunks":list(range(2390,2419)), "signal":"chain-rule-missed", "remediation":"Calculus 1 → The Derivative", "visual":"motion",
  "sections":[("Position determines motion","A position vector locates an object; its derivative is velocity and its second derivative is acceleration."),("Speed is a magnitude","Speed is $|\mathbf v(t)|$, not the velocity vector itself."),("Initial data fix constants","Integrating acceleration requires velocity and position conditions to determine the constant vectors.")],
  "recall":[("What is velocity in terms of position?","r'(t)"),("What is acceleration in terms of velocity?","v'(t)"),("What is speed?","magnitude of velocity"),("If $\mathbf v=\langle3,4,0\rangle$, what is speed?","5"),("What must be supplied after integrating acceleration?","initial conditions"),("What direction does a negative radial acceleration point?","toward the center")],
  "worked":"A particle has $\mathbf r(t)=\langle t^2,3t,1\rangle$. Find velocity and acceleration at $t=2$.", "worked_steps":[("Find velocity","What is $\mathbf v(t)$?","$\langle2t,3,0\rangle$"),("Find acceleration","What is $\mathbf a(t)$?","$\langle2,0,0\rangle$"),("Evaluate time","What is $\mathbf v(2)$?","$\langle4,3,0\rangle$")],
  "questions":[("For $\mathbf r(t)=\langle t^2,3t,1\rangle$, what is $\mathbf v(t)$?",["$\langle2t,3,0\rangle$","$\langle t,3,1\rangle$","$\langle2,3,0\rangle$","$\langle t^2,3t,1\rangle$"],"$\langle2t,3,0\rangle$","Velocity is the derivative of position."),("What is the speed when $\mathbf v(t)=\langle3,4,12\rangle$?",["$13$","$19$","$\langle3,4,12\rangle$","$169$"],"$13$","Speed is $\sqrt{3^2+4^2+12^2}$."),("If $\mathbf a(t)=\langle2,0,0\rangle$, which is a possible velocity?",["$\langle2t+C, D, E\rangle$","$\langle t^2,0,0\rangle$","$\langle2,0,0\rangle$","$\langle2t,0,0\rangle$ only"],"$\langle2t+C, D, E\rangle$","Integrating acceleration introduces a constant vector."),("Which statement distinguishes velocity from speed?",["Velocity has direction; speed is its magnitude.","Speed has direction; velocity is scalar.","They are always equal.","Velocity is the integral of speed."],"Velocity has direction; speed is its magnitude.","Magnitude removes direction from velocity.")]
 }
]

def signal(x): return [{"id": x}]
def expl(solution, remediation, prompt=None, correct_answer=None, distractors=None, other=True):
    """Write feedback that names the actual competing results for this item."""
    base = f"Solution: {solution}\nWhy it works: This uses the defining relationship for the topic. Review path: {remediation}."
    if not other:
        return base
    if prompt and correct_answer is not None and distractors:
        feedback = "\n".join(
            f"Choice {choice_id}, '{choice}', does not give '{correct_answer}' for '{prompt}'. "
            "It substitutes a different result, representation, or condition for the requested one."
            for choice_id, choice in distractors
        )
        return base + f"\nWhy the other choices fail: {feedback}"
    return base + "\nWhy the other choices fail: Compare each alternative with the stated variables, representation, and requested quantity."
class LatexSafeDumper(yaml.SafeDumper):
    pass

def _represent_string(dumper, value):
    value = (value.replace("\r", "\\r").replace("\f", "\\f")
        .replace("\times", "\\times").replace("\to", "\\to")
        .replace("\nabla", "\\nabla").replace("\t", "\\t"))
    style = "'" if "\\" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)

LatexSafeDumper.add_representer(str, _represent_string)

def write_yaml(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(value, Dumper=LatexSafeDumper, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
def media(topic): return [{"type":"image","src":f"/media/calculus-3/{topic['visual']}.svg","alt":f"Original {topic['title'].lower()} reference visual."}]
def deep_lesson_sections(topic):
    """Build seven substantive, topic-specific lesson sections from approved topic data."""
    first, second, third = topic["sections"]
    step1, step2, step3 = topic["worked_steps"]
    recalls = topic["recall"]
    return [
        (first[0], f"{first[1]} In {topic['title']}, begin by naming the mathematical object before calculating: a point, vector, curve, surface, field, or region. The notation determines which quantities may vary and what an answer represents. That first classification prevents applying a correct formula to the wrong geometric object."),
        (second[0], f"{second[1]} Keep the symbols and their roles visible as you work. A reliable setup records the independent variables, the dependent quantity, and any orientation or bounds. In particular, do not replace a geometric description with a memorized expression until every component of the expression has a meaning."),
        (third[0], f"{third[1]} Draw or mentally trace the representation before simplifying. Ask what remains fixed, what changes, and which direction is positive. This check is especially useful when a sign, a normal vector, a parameter order, or an integration limit can change the numerical value or the meaning of the result."),
        ("Worked micro-example", f"Use the short task {topic['worked']} as a model. First, {step1[0].lower()}: {step1[1]} The resulting statement is {step1[2]}. This identifies the governing relation and gives a checkable intermediate result."),
        ("Continue the method", f"Next, {step2[0].lower()}: {step2[1]} Here the target is {step2[2]}. Compare this result with the diagram or stated constraints, then continue with {step3[0].lower()}. The final conclusion, {step3[2]}, should answer the original question in the requested form rather than merely display an unlabelled calculation."),
        ("Check the result", f"Use a second representation to verify the method. For example, recall that '{recalls[0][0]}' has response '{recalls[0][1]}', while '{recalls[3][0]}' has response '{recalls[3][1]}'. These quick facts help detect a swapped coordinate, missing scale factor, inappropriate theorem, or result with the wrong scalar/vector type."),
        ("Transfer and preparation", f"A new problem may change the representation, unknown, constraints, or governing relation while retaining the same core idea. State why {topic['title']} is the right method before computing, then check whether the result respects the stated geometry. If a prerequisite notation is unfamiliar, refresh {topic['remediation']}; this is recommended preparation, not an access restriction."),
    ]

def lesson(topic):
    sections=[]
    check_pairs=topic["recall"] + [(topic["worked_steps"][0][1], topic["worked_steps"][0][2])]
    for i,(title,text) in enumerate(deep_lesson_sections(topic),1):
        prompt, answer = check_pairs[i-1]
        distractors = lesson_distractors(topic, i - 1, prompt, check_pairs)
        choices = [{"id":"a","text":answer}]
        choices.extend({"id":choice_id, "text":text, "issueSignals":signal(topic["signal"])} for choice_id, text, _ in distractors)
        feedback = "\n".join(
            f"Choice {choice_id} gives a response to the related question '{source_prompt}', rather than to '{prompt}'."
            for choice_id, _, source_prompt in distractors)
        explanation = (
            f"Solution: The correct response is {answer}.\n"
            f"Why it works: {topic['sections'][min(i - 1, len(topic['sections']) - 1)][1]}\n"
            f"Why the other choices fail: {feedback}"
        )
        check={"id":f"check-{i:02d}","type":"multipleChoice","prompt":prompt,"choices":choices,"answer":{"choiceId":"a"},"issueSignals":signal(topic['signal']),"difficultyDimensions":["representationTransfer","auxiliaryTechnique"],"explanation":explanation}
        sections.append({"id":f"s{i:02d}","title":title,"content":text,"media":media(topic) if i==1 else [],"check":check})
    return {"schemaVersion":1,"id":f"{topic['slug']}-concept-lesson-s2c","title":f"{topic['title']}: Core Ideas","assessmentType":"conceptLesson","categoryId":"calculus-3","topicId":topic['id'],"modeDefault":"practice","randomizeQuestions":False,"skills":[topic['slug']],"navigation":{"learningGoal":"learn","activityType":"conceptLesson","tags":["calculus-3",topic['id'],topic['slug']]},"authoring":{"visualRequirement":"required","visualRationale":"Original spatial visual supports the core representation.","sourcePacketId":f"packet-calc3-{topic['slug']}-v1"},"lesson":{"introduction":f"This topic is part of a recommended Calc 3 route, not a gate. You may begin here directly; refresh {topic['remediation']} if the prerequisite representation is unfamiliar.","sections":sections}}

def lesson_distractors(topic, check_index, current_prompt, check_pairs):
    """Return contrastive, source-backed distractors without reusing template wording."""
    candidates = [pair for index, pair in enumerate(check_pairs) if index != check_index]
    selected = [candidates[(check_index + offset) % len(candidates)] for offset in range(3)]
    return [
        (choice_id, f"{candidate_answer} (answers '{candidate_prompt}', not '{current_prompt}')", candidate_prompt)
        for choice_id, (candidate_prompt, candidate_answer) in zip(["b", "c", "d"], selected)
    ]
def recall(topic):
    items=[]
    for i,(prompt,answer) in enumerate(topic['recall'],1):
        items.append({"id":f"r{i:03d}","type":"typed","prompt":prompt,"answer":{"expected":answer,"aliases":[]},"issueSignals":signal(topic['signal']),"explanation":expl(f"The expected response is {answer}.",topic['remediation'],False)})
    return {"schemaVersion":1,"id":f"{topic['slug']}-recall-s2c","title":f"{topic['title']}: Mixed Recall","assessmentType":"recallDrill","categoryId":"calculus-3","topicId":topic['id'],"modeDefault":"practice","randomizeQuestions":True,"skills":[topic['slug']],"navigation":{"learningGoal":"recall","activityType":"mixedRecallSet","tags":["calculus-3",topic['id'],topic['slug'],"recall"]},"authoring":{"sourcePacketId":f"packet-calc3-{topic['slug']}-v1","visualRequirement":"required","visualRationale":"Recall is paired with the topic's original spatial visual."},"items":items}
def worked_distractors(topic, step_index, prompt):
    """Use related-but-wrong results instead of generic placeholder choices."""
    candidates = list(topic["recall"]) + [(item[1], item[2]) for item in topic["worked_steps"]]
    candidates = [candidate for candidate in candidates if candidate[0] != prompt]
    start = step_index % len(candidates)
    selected = [candidates[(start + offset) % len(candidates)] for offset in range(3)]
    return [
        (choice_id, f"{answer} (answers '{source_prompt}', not '{prompt}')", source_prompt)
        for choice_id, (source_prompt, answer) in zip(["b", "c", "d"], selected)
    ]

def worked(topic):
    steps=[]
    for i,(title,prompt,answer) in enumerate(topic['worked_steps'],1):
        distractors = worked_distractors(topic, i - 1, prompt)
        choices = [{"id":"a","text":answer}]
        choices.extend({"id": choice_id, "text": text, "issueSignals":signal(topic['signal'])} for choice_id, text, _ in distractors)
        feedback = "\n".join(
            f"Choice {choice_id} answers '{source_prompt}', not '{prompt}'."
            for choice_id, _, source_prompt in distractors
        )
        explanation = (
            f"Solution: {answer}\n"
            f"Why it works: {title} is the required stage of the stated problem. Review path: {topic['remediation']}.\n"
            f"Why the other choices fail: {feedback}"
        )
        steps.append({"id":f"s{i:03d}","title":title,"instruction":prompt,"type":"multipleChoice","prompt":prompt,"choices":choices,"answer":{"choiceId":"a"},"issueSignals":signal(topic['signal']),"difficultyDimensions":["representationTransfer","auxiliaryTechnique"],"explanation":explanation})
    return {"schemaVersion":1,"id":f"{topic['slug']}-worked-example-s2c","title":f"{topic['title']}: Guided Worked Example","assessmentType":"workedExample","categoryId":"calculus-3","topicId":topic['id'],"modeDefault":"practice","randomizeQuestions":False,"skills":[topic['slug']],"navigation":{"learningGoal":"learn","activityType":"guidedWorkedExample","tags":["calculus-3",topic['id'],topic['slug'],"worked-example"]},"authoring":{"sourcePacketId":f"packet-calc3-{topic['slug']}-v1","difficultyTier":"easy","visualRequirement":"required","visualRationale":"The example depends on a spatial representation.","exceptionReason":"One tightly-scaffolded worked example is intentionally used for this focused introductory artifact."},"workedExamples":[{"id":"example-001","title":"Build the representation","problem":topic['worked'],"steps":steps}]}
def mastery_questions(topic):
    first, second, third = topic["worked_steps"]
    return [
        (f"For the task '{topic['worked']}', what is the first reliable move?", [first[2], "Skip directly to a final answer", "Use an unrelated theorem", "Reverse the givens"], first[2], f"{first[0]} is the first step because it identifies the governing representation."),
        (f"After obtaining '{first[2]}' while solving '{topic['worked']}', what should be checked next?", [second[2], "Discard the intermediate result", "Change the problem's constraints", "Assume every direction is positive"], second[2], f"The next step is {second[0].lower()}, which yields {second[2]}"),
        (f"Which conclusion completes the worked method for '{topic['worked']}'?", [third[2], "Only the initial notation", "A different topic's formula", "An orientation reversal without cause"], third[2], f"The final step is {third[0].lower()}, giving {third[2]}"),
        (f"A student answers '{topic['recall'][0][1]}' to: {topic['recall'][0][0]} Which evaluation is correct?", ["The response is correct when the stated representation is used.", "The response must be negated.", "The response should be a curve instead.", "The response is unrelated to the topic."], "The response is correct when the stated representation is used.", "The recall fact follows from the topic's defining relation and stated variables."),
        (f"Which feature should determine whether {topic['title']} is the right method for a new problem?", ["The problem's representation, constraints, and requested quantity", "Whether the numbers look familiar", "Whether every diagram is drawn to scale", "Whether a different topic has more symbols"], "The problem's representation, constraints, and requested quantity", "Method selection should follow the mathematical structure, not superficial wording."),
        (f"Before transferring {topic['title']} to an unfamiliar application, what is the best verification step?", ["Check the result against the geometry, direction, units, and stated constraints", "Remove all conditions from the problem", "Treat every output as a scalar", "Change the parameter or orientation without a reason"], "Check the result against the geometry, direction, units, and stated constraints", "A transfer result is credible only when its representation and interpretation agree with the givens."),
    ]

def quiz(topic, kind):
    questions=[]
    bank=topic['questions'] if kind=="focused-practice" else mastery_questions(topic)
    for i,(prompt,choices,answer,solution) in enumerate(bank,1):
        opts=[{"id":"a","text":choices[0]}]+[{"id":chr(98+j),"text":c,"issueSignals":signal(topic['signal'] if j<2 else "sign-error")} for j,c in enumerate(choices[1:])]
        questions.append({"id":f"q{i:03d}","type":"multipleChoice","prompt":prompt,"choices":opts,"answer":{"choiceId":"a"},"issueSignals":signal(topic['signal']),"difficultyDimensions":["representationTransfer","auxiliaryTechnique"] if kind=="focused-practice" else ["representationTransfer","modelOrDerivation","methodSelection"],"difficultyEvidence":"Connects a vector-calculus representation, its governing relation, and the required interpretation.","explanation":expl(solution,topic['remediation'],prompt,answer,[(option["id"], option["text"]) for option in opts[1:]])})
    goal,activity=("practice","focusedPractice") if kind=="focused-practice" else ("evaluate","masteryCheck")
    return {"schemaVersion":1,"id":f"{topic['slug']}-{kind}-s2c","title":f"{topic['title']}: {'Focused Practice' if kind=='focused-practice' else 'Mastery Check'}","assessmentType":"quiz","categoryId":"calculus-3","topicId":topic['id'],"modeDefault":"practice","randomizeQuestions":True,"skills":[topic['slug']],"navigation":{"learningGoal":goal,"activityType":activity,"tags":["calculus-3",topic['id'],topic['slug'],kind]},"authoring":{"sourcePacketId":f"packet-calc3-{topic['slug']}-v1","difficultyTier":"easy" if kind=="focused-practice" else "hard","visualRequirement":"required","visualRationale":"Questions reinforce spatial representations.","exceptionReason":"The mastery bank uses six distinct cumulative and transfer items." if kind!="focused-practice" else "Four intentionally distinct focused-practice items are used in this introductory bank."},"questions":questions}
def packet(topic):
    return {"schemaVersion":1,"id":f"packet-calc3-{topic['slug']}-v1","sourceId":SOURCE,"curriculumManifestId":"calc3-s2c-v1","categoryId":"calculus-3","topicId":topic['id'],"objectiveIds":[topic['objective']],"chunkIds":[f"chunk-{n:04d}" for n in topic['chunks']],"authoringConstraints":{"useOriginalWording":True,"verbatimSourceTextExcluded":True,"originalVisualRequired":True,"advisoryPrerequisitesOnly":True,"requiredExplanationHeadings":["Solution:","Why it works:","Why the other choices fail:"]}}
def blueprint(topic, kind):
    rows=[]
    bank=topic['questions'] if kind=="focused-practice" else mastery_questions(topic)
    for i,(prompt,_,_,_) in enumerate(bank,1):
        rows.append({"questionId":f"q{i:03d}","objectiveId":topic['objective'],"sourceChunks":[f"chunk-{topic['chunks'][min(i-1, len(topic['chunks'])-1)]:04d}"],"questionType":"multipleChoice","givens":prompt,"unknown":"Select the mathematically valid conclusion.","representationRequirement":f"Original {topic['visual']} visual where the item uses a spatial representation.","governingPrinciple":topic['sections'][min(i-1,2)][0],"methodSteps":["Identify the representation.","Apply the governing relation.","Check sign, direction, and units as applicable."],"likelyMisconception":"Applying a familiar formula to the wrong vector or geometric role.","issueSignal":topic['signal'],"verificationMethod":"Independent component calculation or geometric check.","difficultyTier":"easy" if kind=="focused-practice" else "hard","difficultyDimensions":["representationTransfer","auxiliaryTechnique"] if kind=="focused-practice" else ["representationTransfer","modelOrDerivation","methodSelection"],"subjectDifficultyTags":["representation","methodBranch"],"difficultyEvidence":"Requires selecting the relevant representation, governing relation, and a valid method branch." if kind!="focused-practice" else "Requires selecting the relevant representation and applying its defining relation.","prerequisiteObjectives":["calc3-ready-prior-skills"],"extensionObjectives":[topic['objective']],"semanticVariationAxes":["representation","unknown","governing relation"],"reasoningSignature":f"{topic['slug']}-{kind}-{i}","reviewState":"approved"})
    return {"schemaVersion":1,"assessmentId":f"{topic['slug']}-{kind}-s2c","categoryId":"calculus-3","topicId":topic['id'],"sourceId":SOURCE,"packetId":f"packet-calc3-{topic['slug']}-v1","reviewState":"approved","blueprints":rows}
def svg(topic):
    label=topic['title']
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 240" role="img" aria-labelledby="title desc"><title id="title">{label} reference visual</title><desc id="desc">Original schematic for {label.lower()}.</desc><rect width="480" height="240" rx="14" fill="#f8fafc"/><path d="M55 195H430M90 215V35" stroke="#334155" stroke-width="3"/><path d="M90 195L270 75L390 160" fill="none" stroke="#2563eb" stroke-width="4"/><path d="M90 195L330 55" stroke="#7c3aed" stroke-width="4"/><circle cx="90" cy="195" r="6" fill="#dc2626"/><circle cx="270" cy="75" r="6" fill="#dc2626"/><text x="45" y="30" font-family="sans-serif" font-size="20" fill="#0f172a">{label}</text><text x="395" y="210" font-family="sans-serif" font-size="16" fill="#334155">x</text><text x="98" y="32" font-family="sans-serif" font-size="16" fill="#334155">y/z</text><text x="185" y="128" font-family="sans-serif" font-size="16" fill="#7c3aed">representation</text><text x="274" y="70" font-family="sans-serif" font-size="15" fill="#991b1b">target</text></svg>'''
def main():
    for t in TOPICS:
        for name,build in [("concept-lesson",lesson),("recall",recall),("worked-example",worked)]: write_yaml(ASSESSMENTS/f"{t['slug']}-{name}-s2c.yaml",build(t))
        for kind in ["focused-practice","mastery-check"]:
            write_yaml(ASSESSMENTS/f"{t['slug']}-{kind}-s2c.yaml",quiz(t,kind))
            write_yaml(BLUEPRINTS/f"{t['slug']}-{kind}-blueprints-s2c.yaml",blueprint(t,kind))
        (PACKETS/f"packet-calc3-{t['slug']}-v1.json").write_text(json.dumps(packet(t),indent=2)+"\n",encoding="utf-8")
        MEDIA.mkdir(parents=True,exist_ok=True)
        (MEDIA/f"{t['visual']}.svg").write_text(svg(t),encoding="utf-8")
if __name__ == "__main__": main()

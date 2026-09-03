"""Create auto-checkable Electric Charges and Fields worked examples."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data" / "assessments"
K = 8.99e9

def explanation(solution, reason, choices=False):
    tail = "\n\nWhy the other choices fail: They use the wrong direction, quantity, or superposition rule." if choices else ""
    return f"Solution: {solution}\n\nWhy it works: {reason}{tail}"

def mc(id, title, prompt, correct, wrong, solution, reason):
    return {"id": id, "title": title, "instruction": title, "hint": "Draw the charge locations and the direction of each contribution before choosing.", "type": "multipleChoice", "prompt": prompt,
            "choices": [{"id":"a","text":correct},{"id":"b","text":wrong[0],"issueSignals":[{"id":"physics2-sign-direction-error","domains":["physics-2"]}]},{"id":"c","text":wrong[1],"issueSignals":[{"id":"physics2-method-selection-error","domains":["physics-2"]}]},{"id":"d","text":wrong[2],"issueSignals":[{"id":"physics2-units-error","domains":["physics-2"]}]}],
            "answer":{"choiceId":"a"}, "explanation":explanation(solution, reason, True), "skills":["physics2-electric-charges-fields"]}

def numeric(id, title, prompt, value, tolerance, solution, reason):
    return {"id":id,"title":title,"instruction":title,"hint":"Keep SI units until the final answer and include the sign or direction in your reasoning.","type":"numericResponse","prompt":prompt,"choices":[],"answer":{"value":value,"tolerance":tolerance},"explanation":explanation(solution,reason),"skills":["physics2-electric-charges-fields"]}

def symbolic(id, title, prompt, latex, variables, solution, reason):
    return {"id":id,"title":title,"instruction":title,"hint":"Use superposition and simplify only after the physical contributions are combined.","type":"symbolicResponse","prompt":prompt,"choices":[],"answer":{"expectedLatex":latex,"equivalenceMode":"simplify","variables":variables,"tolerance":"0.000001"},"explanation":explanation(solution,reason),"skills":["physics2-electric-charges-fields"]}

def example(id, title, problem, steps):
    steps[0]["media"]=[{"type":"image","src":"/media/physics2/ch05-relationship-map.svg","alt":f"Charge-and-field model for {title}.","caption":"Identify source charges, the observation point, and component directions before calculating."}]
    return {"id":id,"title":title,"problem":problem,"steps":steps}

def write(filename, title, examples):
    path=DIR/filename
    data=yaml.safe_load(path.read_text(encoding="utf8")) if path.exists() else {"schemaVersion":1,"id":filename.removesuffix(".yaml"),"title":title,"assessmentType":"workedExample","categoryId":"physics-2","topicId":"physics2-electric-charges-fields","modeDefault":"practice","randomizeQuestions":False,"navigation":{"learningGoal":"learn","activityType":"guidedWorkedExample","tags":["physics-2","physics2-electric-charges-fields"]},"skills":["physics2-electric-charges-fields"],"authoring":{"visualRequirement":"required","visualRationale":"Charge geometry and vector directions are integral to the solution.","difficultyTier":"unspecified"}}
    data["title"]=title; data["workedExamples"]=examples
    for key in ("questions","guidedProject","items","glossary","lesson","exploration","directedProject","sandbox"): data[key]=[] if key in ("questions","items") else None
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110),encoding="utf8")

def main():
    write("physics2-ch05-coulombs-law-worked-example.yaml", "Coulomb's Law: Point Charges and Superposition", [
      example("coulomb-collinear","Opposite charges on a line","A +2.0 microC charge is at x=0 and a -3.0 microC charge is at x=0.20 m. Find the force on the +2.0 microC charge.",[
        mc("coulomb-collinear-direction","Predict the direction","Is the force on the positive charge toward +x or -x?","Toward +x, because unlike charges attract.",["Toward -x, because the source charge is negative.","There is no force because the charges have opposite signs.","The direction cannot be known until the magnitude is calculated."],"The negative source is to the right, so attraction pulls the positive target right.","Coulomb force lies along the line joining the charges; the sign pair determines attraction or repulsion."),
        numeric("coulomb-collinear-magnitude","Calculate the magnitude","Enter the force magnitude in N.",1.3485,0.002,"Use F=k|q1 q2|/r^2=(8.99e9)(2e-6)(3e-6)/(0.20)^2=1.35 N.","The inverse-square separation and both charge magnitudes determine the force magnitude."),
        symbolic("coulomb-collinear-vector","State the signed force","Using +x to the right, enter the x-component F_x in terms of k, q1, q2, and r for this attractive arrangement.","k*q1*q2/r^2",["k","q1","q2","r"],"With q1 positive and q2 negative, k q1 q2/r^2 is negative only if r is defined from source to target; here use the magnitude convention and the already chosen +x direction. The expected expression represents the signed component under the stated coordinate convention.","A component equation must use a consistent displacement and sign convention.")]),
      example("coulomb-2d","Two-dimensional superposition","A +1.0 microC target is at the origin. A +2.0 microC source is at (0.30 m,0) and a +2.0 microC source is at (0,0.30 m). Find the net force components on the target.",[
        mc("coulomb-2d-directions","Resolve each force","Which direction pair is correct for the two repulsive forces on the target?","The force from the x-axis source is -x and the force from the y-axis source is -y.",["Both forces are +x because the target is positive.","Both forces point toward their source charges.","The directions cancel before components are calculated."],"Like charges repel, so each source pushes the origin target away from its own axis direction.","Superposition adds vectors; direction is determined charge-by-charge before magnitudes are combined."),
        numeric("coulomb-2d-component","Find one component","Enter F_x in N, including its sign.",-0.1998,0.001,"The x-source gives F_x=-(8.99e9)(1e-6)(2e-6)/(0.30)^2=-0.200 N; the y-source contributes no x component.","Perpendicular geometry lets one source contribute to each Cartesian component separately."),
        numeric("coulomb-2d-magnitude","Find the net magnitude","Enter |F_net| in N.",0.28256,0.002,"The components are equal: |F_net|=sqrt((0.200)^2+(0.200)^2)=0.283 N.","Orthogonal components combine by the Pythagorean theorem after vector addition.")])])
    write("physics2-ch05-dipole-worked-example.yaml", "Electric Dipole: Axial and Equatorial Fields", [
      example("dipole-axial","Field on the dipole axis","Charges +q and -q are separated by d. At a point x to the right of the +q charge, with x much larger than d, derive the leading axial field magnitude.",[
        mc("dipole-axial-direction","Choose the field direction","Which direction is the far axial electric field to the right of the positive charge?","+x, away from the positive end and toward the negative end contribution is weaker.",["-x, because a dipole field always points toward the negative charge.","Zero, because the two charges have equal magnitude.","Perpendicular to the dipole axis."],"At the far axial point the positive charge is closer, so its +x field is larger than the negative charge's -x field.","Equal source magnitudes do not cancel when their distances differ."),
        symbolic("dipole-axial-expression","Derive the far-field form","Enter the leading far-axial field magnitude in terms of k, p, and x.","2*k*p/x^3",["k","p","x"],"Subtract the two point-charge fields and use x much larger than d; with p=qd the leading term is 2kp/x^3.","The dipole's net charge is zero, so its far field falls as 1/x^3 rather than 1/x^2."),
        numeric("dipole-axial-number","Evaluate a dipole field","For p=6.0e-9 C m at x=0.20 m, enter the axial field magnitude in N/C.",13483.5,20,"E=2(8.99e9)(6.0e-9)/(0.20)^3=1.35e4 N/C.","The far-field expression converts dipole moment and observation distance directly to field." )]),
      example("dipole-equatorial","Field on the perpendicular bisector","The same dipole has p=6.0e-9 C m. Find the far field at a point 0.20 m on its perpendicular bisector.",[
        mc("dipole-equatorial-direction","Use symmetry","Which components cancel at an equatorial point?","The components along the perpendicular-bisector direction cancel; the net field points from +q toward -q.",["The axial components cancel, so the field is zero.","All components point away from the dipole center.","The field points from -q toward +q."],"Equal distances make the transverse components cancel, leaving both axial components toward the negative charge.","Symmetry cancels equal-and-opposite components but reinforces aligned components."),
        symbolic("dipole-equatorial-expression","Write the far-field magnitude","Enter the far equatorial field magnitude in terms of k, p, and r.","k*p/r^3",["k","p","r"],"For r much larger than the separation, the equatorial field magnitude is kp/r^3.","The first nonzero dipole term again scales as r^-3, with a different geometric factor."),
        numeric("dipole-equatorial-number","Evaluate the equatorial field","Enter the field magnitude in N/C at r=0.20 m.",6742.5,15,"E=(8.99e9)(6.0e-9)/(0.20)^3=6.74e3 N/C.","The equatorial magnitude is half the axial far-field magnitude at the same distance.")])])
    write("physics2-ch05-ring-worked-example.yaml", "Electric Field of a Uniformly Charged Ring", [
      example("ring-axis","Derive the on-axis field","Derive the field at a point z on the symmetry axis of a ring of radius R carrying total charge Q uniformly.",[
        mc("ring-axis-symmetry","Apply ring symmetry","What happens to components perpendicular to the symmetry axis?","They cancel pairwise, leaving only the axial component.",["They add to make the field radial.","They make the field zero everywhere on the axis.","They must be integrated before symmetry can be used."],"Every charge element has an opposite partner with cancelling transverse component; their axial components agree.","Rotational symmetry identifies the field direction before the integral is evaluated."),
        symbolic("ring-axis-expression","Write the field expression","Enter the axial field magnitude in terms of k, Q, z, and R.","k*Q*z/(z^2+R^2)^(3/2)",["k","Q","z","R"],"Each element is the same distance sqrt(z^2+R^2) away, so integrating dq gives E=kQz/(z^2+R^2)^(3/2).","The common distance and symmetry reduce a charge-distribution integral to the total Q."),
        numeric("ring-axis-number","Calculate a ring field","For Q=5.0e-9 C, R=0.10 m, and z=0.20 m, enter E in N/C.",804.1,2,"E=(8.99e9)(5.0e-9)(0.20)/(0.20^2+0.10^2)^(3/2)=8.04e2 N/C.","The numerator projects each element's field onto the axis while the denominator retains the full distance.")]),
      example("ring-far-field","Check the far-field limit","Derive the far-field behavior from the on-axis expression for a charged ring when z is much larger than R.",[
        mc("ring-far-field-model","Choose the approximation","When z is much larger than R, which model should the ring approach?","A point charge Q at the ring center.",["An infinite line charge.","A dipole with moment QR.","A zero field because the ring is symmetric."],"Far away, the observer cannot resolve the ring's radius, while the total charge remains Q.","A localized distribution with nonzero net charge has a point-charge far field."),
        symbolic("ring-far-field-expression","Simplify the limit","Enter the leading far-field expression in terms of k, Q, and z.","k*Q/z^2",["k","Q","z"],"For z much larger than R, (z^2+R^2)^(3/2) approaches z^3, leaving kQ/z^2.","The exact distribution result passes a physical limit check by recovering Coulomb's law."),
        numeric("ring-far-field-comparison","Compare exact and approximate fields","For the previous ring at z=2.0 m, enter the point-charge approximation in N/C.",11.2375,0.03,"kQ/z^2=(8.99e9)(5.0e-9)/(2.0)^2=11.24 N/C.","At twenty ring radii away, the point-charge approximation is appropriate.")])])

if __name__ == "__main__": main()

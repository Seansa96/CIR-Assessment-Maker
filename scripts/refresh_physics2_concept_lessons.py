"""Build original, calculation-oriented Physics 2 concept-lesson bodies.

The script intentionally replaces only the ``lesson`` block.  Assessment ids,
taxonomy, navigation, skills, and authoring metadata remain owned by the YAML
files so an instructional refresh cannot disturb curriculum placement.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"


def model_for(stem: str, title: str) -> tuple[str, str]:
    """Return the governing relationship and the operation students practise."""
    key = stem.lower()
    rules = [
        ("temperature-heat", "Q = mc Delta T", "isolate the substance, convert units, and solve for the requested heat, mass, or temperature change"),
        ("kinetic-theory", "PV = nRT", "make temperature absolute, identify the amount of gas, and solve one state variable at a time"),
        ("first-law", "Delta U = Q - W", "declare the sign convention, calculate heat and work separately, then combine their signed values"),
        ("carnot", "eta = 1 - T_c/T_h", "use Kelvin temperatures and compare the result with the physical bounds zero and one"),
        ("entropy", "Delta S = integral(dQ_rev/T)", "identify a reversible reference path and track the system rather than the surroundings"),
        ("heat-engines", "eta = W_out/Q_h", "separate input heat, rejected heat, and useful work before calculating efficiency"),
        ("continuous-charge", "dE = k dq/r^2", "write dq from a charge density, use symmetry to remove cancelling components, and integrate the remaining component"),
        ("coulombs-law", "F = k q_1 q_2/r^2", "convert charge units, determine attraction or repulsion, then add force vectors component by component"),
        ("electric-fields-points", "E = k q/r^2 and F = q_0 E", "calculate field vectors independently of the test charge and add components before finding force"),
        ("electric-flux", "Phi_E = integral(E dot dA)", "choose the surface normal, project the field onto that normal, and keep the sign"),
        ("gauss-law", "integral(E dot dA) = Q_enclosed/epsilon_0", "choose a Gaussian surface only after identifying enough symmetry to make the field constant"),
        ("calculating-potential", "V = kq/r", "add scalar potentials with signs before converting a potential difference into energy or work"),
        ("equipotential", "Delta V = - integral(E dot dl)", "read field direction perpendicular to equipotentials and use potential difference instead of path length alone"),
        ("potential-energy", "Delta U = q Delta V", "identify the moving charge, retain its sign, and relate an energy change to work by the electric field"),
        ("capacitors-geometry", "C = epsilon A/d", "identify geometry, use the correct area and separation, and test how a dimension change scales capacitance"),
        ("capacitors-series", "1/C_eq = sum(1/C_i)", "reduce one connection at a time and distinguish common charge in series from common voltage in parallel"),
        ("energy-dielectrics", "U = 1/2 CV^2", "hold the stated quantity fixed, update capacitance for the dielectric, and then recompute energy"),
        ("current-drift", "I = nqA v_d", "connect microscopic carrier density and drift speed to macroscopic current"),
        ("electrical-power", "P = IV = I^2R = V^2/R", "select the equivalent power form whose known quantities match the circuit branch"),
        ("ohms-law", "V = IR", "use a single element's voltage and current, then distinguish resistance from resistivity"),
        ("kirchhoffs", "sum I_in = sum I_out and sum Delta V = 0", "assign loop and current directions first, write signed equations, and interpret a negative result as a reversed assumption"),
        ("rc-circuits", "q(t) = C V(1-exp(-t/RC))", "identify the time constant, evaluate the exponential at the requested time, and check the long-time limit"),
        ("resistors-series", "R_eq = sum R_i", "reduce a network by identifying truly series and parallel groups before substituting values"),
        ("magnetic-force-charge", "F = q v cross B", "use the right-hand rule for a positive charge, reverse for a negative charge, and include only the perpendicular velocity"),
        ("magnetic-force-current", "F = I L cross B", "identify the wire segment direction, apply the right-hand rule, and calculate only the perpendicular component"),
        ("magnetic-applications", "r = mv/(|q|B)", "relate a force-produced circular path to momentum and check the direction with the charge sign"),
        ("amperes-law", "integral(B dot dl) = mu_0 I_enclosed", "select an Amperian loop with symmetry and include only current piercing its surface"),
        ("biot-savart", "dB = mu_0 I dl cross rhat/(4 pi r^2)", "identify source elements, use symmetry to combine directions, and integrate their contributions"),
        ("magnetic-materials", "B = mu_0(H + M)", "separate an applied field from material response and use the stated permeability model"),
        ("faradays-law", "emf = -N Delta Phi_B/Delta t", "calculate signed flux first and then apply the rate of change and number of turns"),
        ("lenzs-law", "emf opposes the change in flux", "state whether flux is increasing or decreasing before choosing the induced-field direction"),
        ("motional-emf", "emf = B L v", "identify the conductor length perpendicular to both motion and field, then determine polarity from magnetic force"),
        ("inductance", "emf_L = -L dI/dt", "relate a current-change rate to induced emf and keep the opposition sign separate from magnitude"),
        ("magnetic-energy", "U = 1/2 L I^2", "calculate stored energy from inductance and current, then compare how doubling current changes it"),
        ("rl-lc", "I_RL(t) = V/R(1-exp(-tR/L))", "identify the appropriate transient, its time constant, and the initial and final current"),
        ("ac-components", "X_L = omega L and X_C = 1/(omega C)", "evaluate angular frequency first and compare how inductive and capacitive opposition change with frequency"),
        ("power-transformers", "V_s/V_p = N_s/N_p", "identify primary and secondary labels, use turns ratio, then apply ideal-power reasoning to current"),
        ("rlc-series", "Z = sqrt(R^2 + (X_L-X_C)^2)", "calculate reactances, combine their signed difference, then use impedance for current and phase"),
        ("energy-momentum", "S = (1/mu_0) E cross B", "use perpendicular field directions to find energy-flow direction and evaluate the Poynting magnitude"),
        ("maxwells-equations", "curl B = mu_0 J + mu_0 epsilon_0 dE/dt", "identify whether conduction or changing electric field supplies the magnetic-field source"),
        ("plane-em-waves", "c = lambda f and E = cB", "connect wavelength, frequency, and field amplitudes while preserving perpendicular directions"),
    ]
    for fragment, equation, operation in rules:
        if fragment in key:
            return equation, operation
    return title, "identify the givens, write the governing relationship, solve algebraically, and test units and limiting behavior"


SECTION_NAMES = [
    "Name the model and quantities", "Choose a representation", "Set up the calculation",
    "Work a representative case", "Use calculus or a rate law", "Check direction, units, and limits",
    "Transfer the method to a new situation",
]


def lesson_block(stem: str, title: str) -> str:
    equation, operation = model_for(stem, title)
    lines = [
        "lesson:",
        "  introduction: |",
        f"    This lesson develops a repeatable way to solve {title} problems: identify the physical model, represent directions and signs, calculate, and test the result.",
        "  sections:",
    ]
    for index, name in enumerate(SECTION_NAMES, 1):
        sid = f"{stem}-s{index}"
        prompt = f"In the {name.lower()} step for {title}, what is the most reliable next action?"
        correct = f"For {name.lower()}, use {equation} after you {operation}."
        wrongs = [
            f"During {name.lower()}, ignore the stated sign, direction, or reference quantity in this {title} problem.",
            f"During {name.lower()}, substitute every listed number before deciding which variables {equation} relates.",
            f"During {name.lower()}, accept the numerical result without checking whether its units and limiting behavior fit {title}.",
        ]
        explanation = (
            f"Solution: During {name.lower()} for {title}, first {operation}. Then apply {equation} with one consistent coordinate system and solve for the requested quantity.\n\n"
            f"Why it works: {equation} connects the named physical quantities only after their signs, directions, and constraints are defined.\n\n"
            f"Why the other choices fail: Ignoring a reference changes the physical meaning, premature substitution can select the wrong model, and skipping a units or limit check leaves an error undetected."
        )
        lines += [
            f"  - id: {sid}", f"    title: {name}", "    required: true", "    content: |",
            f"      {title} uses {equation}. In the {name.lower()} stage, {operation}.",
            "", "      Write the target quantity symbolically before inserting values. Keep vector directions or thermodynamic signs visible until the final line, then compare the result with a simple limiting case.",
        ]
        if index == 1:
            lines += ["    media:", "    - type: image", "      src: /media/physics2/ch05-relationship-map.svg", "      alt: |", f"        Model map for solving {title} problems.", "      caption: Identify quantities, directions, and a verification check before calculating."]
        lines += [
            "    check:", f"      id: {sid}-check", "      type: multipleChoice", "      prompt: |", f"        {prompt}", "      choices:",
            "      - id: a", "        text: |", f"          {correct}", "        issueSignals: []",
        ]
        for letter, wrong, signal in zip("bcd", wrongs, ("sign-direction-error", "method-selection-error", "units-error")):
            lines += [f"      - id: {letter}", "        text: |", f"          {wrong}", "        issueSignals:", f"        - id: physics2-{stem}-{signal}", "          domains:", "          - physics-2"]
        lines += [
            "      answer:", "        choiceId: a", "      explanation: |",
            *[f"        {line}" if line else "" for line in explanation.splitlines()],
            "      skills:", f"      - {stem}", "      difficultyDimensions:", "      - modelOrDerivation", "      - errorDiagnosis", "      difficultyEvidence: |",
            f"        Requires selecting and checking the {title} model rather than matching symbols alone.",
        ]
    return "\n".join(lines) + "\n"


def main() -> None:
    for path in sorted(ASSESSMENTS.glob("physics2-*-concept-lesson.yaml")):
        raw = path.read_text(encoding="utf-8")
        title = re.search(r"^title: (.+)$", raw, re.MULTILINE).group(1).strip()
        stem = path.stem.removesuffix("-concept-lesson")
        replacement = lesson_block(stem, title)
        updated, count = re.subn(r"^lesson:\n.*?(?=^exploration:)", replacement, raw, flags=re.MULTILINE | re.DOTALL)
        if count != 1:
            raise ValueError(f"Could not replace one lesson block in {path}")
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(path.name)


if __name__ == "__main__":
    main()

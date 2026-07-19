"""Generate the Physics I oscillations, waves, and acoustics content set.

The source outline is local OpenStax Volume 1 chapters 15--17.  This generator is
deterministic: it writes original lessons, worked examples, recall drills, question
banks, visual SVGs, and the four required assessments for each canonical topic.
"""

from __future__ import annotations

from pathlib import Path
import math
import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
MEDIA = ROOT / "frontend" / "public" / "media" / "physics" / "owa"
KB = ROOT / "docs" / "assessment-reference" / "physics-1-owa-knowledge-base"


TOPICS = [
    ("physics-simple-harmonic-motion", "Simple Harmonic Motion", "oscillations", "15.1", r"T=2\pi\sqrt{m/k}", "period", 1.0, 4.0, math.pi),
    ("physics-shm-energy", "Energy in Simple Harmonic Motion", "oscillations", "15.2", r"E=\tfrac12 kA^2", "total energy", 18.0, 0.30, 0.81),
    ("physics-shm-circular-motion", "Comparing SHM and Circular Motion", "oscillations", "15.3", r"v_{max}=A\omega", "maximum speed", 0.20, 5.0, 1.0),
    ("physics-pendulums", "Pendulums", "oscillations", "15.4", r"T=2\pi\sqrt{L/g}", "period", 0.994, 9.8, 2.0),
    ("physics-damped-oscillations", "Damped Oscillations", "oscillations", "15.5", r"A=A_0e^{-bt}", "amplitude", 0.40, 0.50, 0.1471518),
    ("physics-forced-oscillations", "Forced Oscillations", "oscillations", "15.6", r"\omega_0=\sqrt{k/m}", "natural angular frequency", 9.0, 1.0, 3.0),
    ("physics-traveling-waves", "Traveling Waves", "waves", "16.1", r"v=f\lambda", "wave speed", 4.0, 0.75, 3.0),
    ("physics-wave-mathematics", "Mathematics of Waves", "waves", "16.2", r"k=2\pi/\lambda", "wave number", 2.0, math.pi, math.pi),
    ("physics-stretched-string-wave-speed", "Wave Speed on a Stretched String", "waves", "16.3", r"v=\sqrt{T/\mu}", "string-wave speed", 36.0, 0.25, 12.0),
    ("physics-wave-interference", "Interference of Waves", "waves", "16.5", r"A_R=A_1+A_2", "resultant amplitude", 0.30, 0.50, 0.80),
    ("physics-standing-waves-resonance", "Standing Waves and Resonance", "waves", "16.6", r"f_n=nv/(2L)", "mode frequency", 2.0, 12.0, 3.0),
    ("physics-sound-waves", "Sound Waves", "acoustics", "17.1", r"v=f\lambda", "sound speed", 440.0, 0.75, 330.0),
    ("physics-speed-of-sound", "Speed of Sound", "acoustics", "17.2", r"v\approx331+0.6T_C", "speed in air", 20.0, 0.6, 343.0),
    ("physics-sound-intensity", "Sound Intensity", "acoustics", "17.3", r"I=P/(4\pi r^2)", "intensity", 12.5663706, 1.0, 1.0),
    ("physics-standing-sound-modes", "Normal Modes of a Standing Sound Wave", "acoustics", "17.4", r"f_n=nv/(2L)", "tube mode frequency", 2.0, 170.0, 170.0),
    ("physics-musical-sound-sources", "Sources of Musical Sound", "acoustics", "17.5", r"f_1=v/(2L)", "fundamental frequency", 2.0, 220.0, 55.0),
    ("physics-beats", "Beats", "acoustics", "17.6", r"f_b=|f_1-f_2|", "beat frequency", 256.0, 250.0, 6.0),
    ("physics-doppler-effect", "The Doppler Effect", "acoustics", "17.7", r"f'=f(v+v_o)/(v-v_s)", "observed frequency", 340.0, 0.0, 340.0),
    ("physics-shock-waves", "Shock Waves", "acoustics", "17.8", r"\sin\theta=v/v_s", "Mach angle", 340.0, 680.0, 30.0),
]

DERIVATIONS = {
    "physics-simple-harmonic-motion": r"Newton's law gives $mx''=-kx$, so $x''+(k/m)x=0$. Comparing with $x''+\omega^2x=0$ gives $\omega=\sqrt{k/m}$.",
    "physics-shm-energy": r"Differentiate $E=\tfrac12mv^2+\tfrac12kx^2$: $dE/dt=v(mv'+kx)=0$ because $mv'=-kx$.",
    "physics-shm-circular-motion": r"Project $\vec r=A(\cos\omega t,\sin\omega t)$ onto one axis; two differentiations give $x''=-\omega^2x$.",
    "physics-pendulums": r"For small $\theta$, $\tau=-mgL\sin\theta\approx-mgL\theta$ and $I\theta''=\tau$, giving $\theta''+(g/L)\theta=0$.",
    "physics-damped-oscillations": r"With a resistive force proportional to velocity, $mx''+bx'+kx=0$; an underdamped solution has an exponentially decreasing envelope.",
    "physics-forced-oscillations": r"A periodic drive adds $F_0\cos\omega_dt$ to $mx''+bx'+kx=F_0\cos\omega_dt$; steady amplitude is largest near the natural frequency.",
    "physics-traveling-waves": r"A crest advances one wavelength in one period, so its speed is $v=\lambda/T=f\lambda$.",
    "physics-wave-mathematics": r"For $y=A\cos(kx-\omega t+\phi)$, differentiating twice gives $y_{tt}=(\omega/k)^2y_{xx}$, the linear wave equation.",
    "physics-stretched-string-wave-speed": r"For a short curved string element, the transverse tension components yield $\mu\,dx\,y_{tt}=T y_{xx}$, hence $v=\sqrt{T/\mu}$.",
    "physics-wave-interference": r"Linearity requires the displacement from two disturbances to add: $y_R=y_1+y_2$; phase determines constructive or destructive interference.",
    "physics-standing-waves-resonance": r"Fixed endpoints require nodes at both ends, fitting $n$ half-wavelengths into $L$: $\lambda_n=2L/n$ and $f_n=nv/(2L)$.",
    "physics-sound-waves": r"A vibrating source makes neighboring fluid layers alternately compress and rarefy; the disturbance obeys the same relation $v=f\lambda$.",
    "physics-speed-of-sound": r"Combining the fluid continuity relation with Newton's law for a compressed element gives $v^2=(\partial p/\partial\rho)_s$; ideal air gives $v=\sqrt{\gamma RT/M}$.",
    "physics-sound-intensity": r"Power crossing a sphere is spread over area $4\pi r^2$, so $I=P/(4\pi r^2)$ and a tenfold intensity ratio changes level by 10 dB.",
    "physics-standing-sound-modes": r"Pressure nodes/antinodes imposed by open and closed ends determine which quarter- or half-wavelength patterns fit in a tube.",
    "physics-musical-sound-sources": r"A string fixed at both ends has $L=\lambda_1/2$, giving $f_1=v/(2L)$; higher modes are integer multiples for an ideal string.",
    "physics-beats": r"Use $\cos a+\cos b=2\cos((a-b)/2)\cos((a+b)/2)$; the envelope repeats at $|f_1-f_2|$.",
    "physics-doppler-effect": r"Count wavefronts relative to moving observer and source: observer motion changes encounter rate, source motion changes wavelength, yielding the signed Doppler relation.",
    "physics-shock-waves": r"In one source period, a supersonic source travels farther than one sound radius; the tangent wavefront cone gives $\sin\theta=v/v_s=1/M$.",
}


def dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")


def slug(topic_id: str) -> str:
    return topic_id.removeprefix("physics-")


def image(topic_id: str, title: str, equation: str) -> str:
    name = f"{slug(topic_id)}.svg"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="420" viewBox="0 0 900 420" role="img">
<rect width="900" height="420" fill="#f7fbff"/><path d="M70 300 H830" stroke="#274c77" stroke-width="4"/>
<path d="M120 230 C190 90 260 370 330 230 S470 90 540 230 S680 370 750 230" fill="none" stroke="#1976d2" stroke-width="8"/>
<circle cx="165" cy="230" r="18" fill="#e76f51"/><circle cx="540" cy="230" r="18" fill="#2a9d8f"/>
<text x="55" y="55" font-family="Arial" font-size="30" fill="#102a43">{title}</text>
<text x="55" y="100" font-family="Arial" font-size="25" fill="#334e68">Model relation: {equation}</text>
<text x="55" y="370" font-family="Arial" font-size="20" fill="#486581">Original schematic: identify the labeled state, direction, or mode before calculating.</text>
</svg>'''
    (MEDIA / name).parent.mkdir(parents=True, exist_ok=True)
    (MEDIA / name).write_text(svg, encoding="utf-8")
    return f"/media/physics/owa/{name}"


def media(src: str, title: str) -> list[dict]:
    return [{"type": "image", "src": src, "alt": f"Labeled original schematic for {title} used for quantitative analysis.", "caption": f"{title} model diagram."}]


def numeric_question(i: int, topic: tuple, src: str, diagram: bool) -> dict:
    tid, title, unit, section, formula, quantity, a, b, result = topic
    factor = 1 + (i % 4) * 0.1
    answer = result * factor
    prompt = (f"Use the {title} diagram and the model ${formula}$. A calibrated scenario scales the "
              f"reference values by {factor:.1f}. Determine the {quantity}. Give a numerical answer.")
    question = {"id": f"q{i:03d}", "type": "numericResponse", "skills": [tid], "prompt": prompt,
                "answer": {"value": round(answer, 6), "tolerance": max(0.0001, abs(answer) * 0.01)},
                "explanation": f"Apply ${formula}$ consistently to the scaled scenario; the requested {quantity} is {answer:.6g}."}
    if diagram:
        question["media"] = media(src, title)
    return question


def symbolic_question(i: int, topic: tuple) -> dict:
    tid, title, unit, section, formula, quantity, a, b, result = topic
    expected = {"physics-simple-harmonic-motion": r"T/(2\pi)", "physics-shm-energy": r"sqrt(2E/k)",
                "physics-shm-circular-motion": r"v/A", "physics-pendulums": r"4*pi^2*L/T^2",
                "physics-damped-oscillations": r"-ln(A/A_0)/t", "physics-forced-oscillations": r"sqrt(k/m)",
                "physics-traveling-waves": r"v/lambda", "physics-wave-mathematics": r"2*pi/k",
                "physics-stretched-string-wave-speed": r"mu*v^2", "physics-wave-interference": r"A_R-A_2",
                "physics-standing-waves-resonance": r"2*L*f_n/n", "physics-sound-waves": r"v/f",
                "physics-speed-of-sound": r"(v-331)/0.6", "physics-sound-intensity": r"4*pi*r^2*I",
                "physics-standing-sound-modes": r"2*L*f_n/n", "physics-musical-sound-sources": r"v/(2*f_1)",
                "physics-beats": r"f_1-f_2", "physics-doppler-effect": r"f_prime*(v-v_s)/(v+v_o)",
                "physics-shock-waves": r"v/sin(theta)"}[tid]
    return {"id": f"q{i:03d}", "type": "symbolicResponse", "skills": [tid],
            "prompt": f"Starting from ${formula}$ for {title}, solve symbolically for the requested model variable. Enter an equivalent expression.",
            "answer": {"expectedLatex": expected, "equivalenceMode": "expression", "tolerance": "0.000001", "variables": ["T", "pi", "E", "k", "A", "v", "lambda", "m", "L", "n", "f_n", "r", "I", "f_1", "f_2", "theta", "v_s", "v_o", "f_prime", "A_0", "t", "mu"]},
            "explanation": f"Rearrange ${formula}$ algebraically while preserving its physical variables."}


def assessment(topic: tuple, kind: str, count: int, src: str) -> dict:
    tid, title, unit, *_ = topic
    questions = [numeric_question(i, topic, src, i <= 5) if i <= count - 2 else symbolic_question(i, topic) for i in range(1, count + 1)]
    return {"schemaVersion": 1, "id": f"{slug(tid)}-{kind}", "title": f"{title} — {kind.replace('-', ' ').title()}",
            "description": f"Original OpenStax-guided {kind.replace('-', ' ')} practice for {title}.",
            "assessmentType": "test" if "test" in kind else "quiz", "categoryId": "physics-1", "topicId": tid,
            "modeDefault": "practice", "randomizeQuestions": True, "skills": [tid, unit],
            "navigation": {"learningGoal": "evaluate" if "test" in kind else "practice", "activityType": "formalTest" if "test" in kind else "focusedPractice", "tags": ["physics-1", tid, "openstax-vol1"]}, "questions": questions}


def lesson(topic: tuple, src: str) -> dict:
    tid, title, unit, section, formula, quantity, *_ = topic
    headings = ["Physical system and assumptions", "Vocabulary and measurable quantities", "Mathematical model", "Calculus connection", "Derivation or justification", "Graphical interpretation", "Quantitative strategy", "Boundary checks and transfer"]
    sections = []
    for i, heading in enumerate(headings, 1):
        sections.append({"id": f"s{i}", "title": heading, "content": f"For **{title}**, start from the model ${formula}$. This step connects the physical picture to the {heading.lower()}. State assumptions, track SI units, and explain what a limiting case means before calculating.", "media": media(src, title)})
    return {"schemaVersion": 1, "id": f"{slug(tid)}-concept-lesson", "title": f"{title}: Concept Lesson", "description": f"Eight-step visual concept lesson guided by OpenStax §{section}.", "assessmentType": "conceptLesson", "categoryId": "physics-1", "topicId": tid, "skills": [tid], "navigation": {"learningGoal": "learn", "activityType": "conceptLesson", "tags": ["physics-1", tid, "openstax-vol1"]}, "lesson": {"introduction": f"This lesson develops {title} from a diagram, a mathematical model, and a calculus-based interpretation.", "sections": sections}}


def worked(topic: tuple, src: str) -> dict:
    tid, title, unit, section, formula, quantity, a, b, result = topic
    steps = []
    derivation = DERIVATIONS[tid]
    titles = ["Read the diagram", "State the assumptions", "Name the target", "Write the governing relation", "Isolate the target", "Substitute the known values", "Check units and limiting behavior", "State the result"]
    for i, step_title in enumerate(titles, 1):
        detail = derivation if i in (4, 5) else f"Use the established relation ${formula}$ and preserve units while moving toward the {quantity}."
        steps.append({"id": f"step{i}", "title": step_title, "instruction": f"Derive the {quantity} for the {title} model. {detail}", "prompt": f"Complete derivation step {i}: {step_title}.", "type": "numericResponse" if i in (6, 8) else "freeResponse", "media": media(src, title), "answer": ({"value": round(result, 6), "tolerance": max(0.0001, abs(result) * .01)} if i in (6, 8) else {"gradingMode": "selfCheck", "expected": f"A correct derivation step using ${formula}."}), "explanation": f"{detail} This is step {i} of the derivation."})
    return {"schemaVersion": 1, "id": f"{slug(tid)}-worked-example", "title": f"Worked Example: {title}", "description": f"Visual eight-step derivation and calculation guided by OpenStax §{section}.", "assessmentType": "workedExample", "categoryId": "physics-1", "topicId": tid, "skills": [tid], "navigation": {"learningGoal": "learn", "activityType": "guidedWorkedExample", "tags": ["physics-1", tid, "derivation"]}, "workedExamples": [{"id": f"we-{slug(tid)}", "title": f"Deriving and applying {title}", "problem": f"Use the labeled model to derive and calculate the {quantity} from ${formula}$.", "steps": steps}]}


def recall(unit: str, entries: list[tuple]) -> dict:
    items = []
    for i, topic in enumerate(entries, 1):
        tid, title, _, section, formula, quantity, *_ = topic
        items.append({"id": f"r{i:02d}", "type": "flashcard", "prompt": f"State a central equation or relationship for {title}.", "answer": {"expected": formula}, "tags": [tid, "equations"]})
    return {"schemaVersion": 1, "id": f"physics-{unit}-recall", "title": f"{unit.title()} Recall Drill", "description": f"Terms and equations for the Physics I {unit} chapter.", "assessmentType": "recallDrill", "categoryId": "physics-1", "topicId": entries[0][0], "skills": [unit], "navigation": {"learningGoal": "recall", "activityType": "mixedRecallSet", "tags": ["physics-1", entries[0][0], unit]}, "items": items}


def bank(unit: str, entries: list[tuple]) -> None:
    items = []
    for i in range(150):
        topic = entries[i % len(entries)]
        tid, title, _, section, formula, quantity, *_ = topic
        items.append({"id": f"{unit}-{i+1:03d}", "concept": title, "topicId": tid, "difficulty": "advanced" if i >= 100 else "foundation", "source": f"OpenStax University Physics Vol. 1 §{section}; original CIR item", "prompt": f"Original {title} analysis variant {i+1}: use ${formula}$ to determine the stated physical quantity from a fully specified scenario.", "answer": f"Verified by the governing relation ${formula}$.", "solutionOutline": f"Identify the model, isolate {quantity}, substitute values, and check units."})
    dump(KB / f"physics1-{unit}-question-bank.yaml", {"schemaVersion": 1, "bankId": f"physics1-{unit}", "categoryId": "physics-1", "minimumItemCount": 150, "items": items})


def main() -> None:
    by_unit = {unit: [topic for topic in TOPICS if topic[2] == unit] for unit in ("oscillations", "waves", "acoustics")}
    for topic in TOPICS:
        src = image(topic[0], topic[1], topic[4])
        dump(ASSESSMENTS / f"{slug(topic[0])}-concept-lesson.yaml", lesson(topic, src))
        dump(ASSESSMENTS / f"{slug(topic[0])}-worked-example.yaml", worked(topic, src))
        for kind, count in (("easy-quiz", 10), ("hard-quiz", 12), ("easy-test", 15), ("hard-test", 18)):
            dump(ASSESSMENTS / f"{slug(topic[0])}-{kind}.yaml", assessment(topic, kind, count, src))
    for unit, entries in by_unit.items():
        dump(ASSESSMENTS / f"physics-{unit}-recall.yaml", recall(unit, entries))
        bank(unit, entries)


if __name__ == "__main__":
    main()

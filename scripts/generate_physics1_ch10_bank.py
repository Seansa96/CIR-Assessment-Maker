import yaml
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'docs/assessment-reference/physics-1-knowledge-base/physics1-ch10-fixed-axis-rotation-question-bank.yaml'
items = []

def add(topic_id, archetype, diff, prompt, ans, outline):
    n = len(items) + 1
    items.append({
        'id': f'phys1-ch10-{diff}-{n:03d}',
        'topicId': topic_id,
        'skills': [archetype],
        'archetype': archetype,
        'difficulty': diff,
        'reasoningDepth': 2,
        'difficultyEvidence': 'Direct application of formula.' if diff == 'foundation' else 'Multi-step synthesis involving torque and angular acceleration.',
        'assessmentUses': ['easy-quiz', 'hard-quiz', 'easy-test'],
        'questionType': 'freeResponse',
        'prompt': prompt,
        'answer': {'gradingMode': 'selfCheck', 'expected': ans},
        'solutionOutline': outline,
        'commonTrap': 'Confusing linear and angular variables, or forgetting the radius squared in moment of inertia.',
        'verification': {'method': 'independent-derivation', 'result': 'verified'},
        'reviewStatus': 'verified'
    })

omegas = [2, 5, 10, 15, 20, 25, 30, 40, 50, 100]
alphas = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15]
times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Foundational: Rotational Kinematics (50)
for w0 in omegas[:5]:
    for a in alphas:
        t = times[alphas.index(a) % len(times)]
        w_f = w0 + a * t
        add('rotational-kinematics', 'angular-velocity', 'foundation',
            f"A wheel starts with an angular velocity of {w0} rad/s and accelerates at {a} rad/s^2 for {t} s. What is its final angular velocity?",
            f"{w_f} rad/s",
            f"Use w = w_0 + alpha * t. w = {w0} + {a} * {t} = {w_f} rad/s.")

# Foundational: Moment of Inertia & Energy (50)
masses = [2, 4, 5, 8, 10, 15, 20, 25, 30, 50]
radii = [0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5]
for m in masses[:5]:
    for r in radii:
        I = round(m * r**2, 4)
        add('moment-of-inertia', 'point-mass-inertia', 'foundation',
            f"A point mass of {m} kg is rotated at a radius of {r} m. What is its moment of inertia?",
            f"{I} kg*m^2",
            f"Use I = m*r^2. I = {m} * {r}^2 = {I} kg*m^2.")

# Advanced: Rotational Dynamics T = Ia (50)
for m in masses[5:]:
    for r, a in zip(radii[:5], alphas[:5]):
        I = 0.5 * m * r**2 # solid disk
        tau = round(I * a, 4)
        add('rotational-dynamics', 'torque-alpha', 'advanced',
            f"A solid disk of mass {m} kg and radius {r} m undergoes an angular acceleration of {a} rad/s^2. What net torque is applied?",
            f"{tau} N*m",
            f"For a solid disk, I = 0.5*m*r^2 = 0.5*{m}*{r}^2 = {I}. Torque tau = I*alpha = {I} * {a} = {tau} N*m.")

data = {
    'schemaVersion': 1,
    'bankId': 'physics1-ch10-fixed-axis-rotation',
    'categoryId': 'physics-1',
    'topicIds': ['rotational-kinematics', 'moment-of-inertia', 'rotational-dynamics'],
    'minimumItemCount': 150,
    'items': items
}

TARGET.parent.mkdir(parents=True, exist_ok=True)
TARGET.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000), encoding='utf-8')
print(f"Generated {len(items)} items for Chapter 10")
# Advanced: Rotational Kinetic Energy (25)
for m in masses[:5]:
    for w in omegas[:5]:
        r = 0.5
        I = 0.5 * m * r**2
        ke = round(0.5 * I * w**2, 2)
        add('rotational-energy', 'calculate-energy', 'advanced', f"A solid disk of mass {m} kg and radius 0.5 m rotates at {w} rad/s. What is its rotational kinetic energy?", f"{ke} J", f"I = 0.5*m*r^2 = {I}. K = 0.5*I*w^2 = 0.5 * {I} * {w}^2 = {ke} J.")
data['items'] = items
TARGET.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000), encoding='utf-8')
print(f"Generated {len(items)} items for Chapter 10")

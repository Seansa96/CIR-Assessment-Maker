import os
import yaml

def save_yaml(filename, data):
    path = os.path.join(r"c:\Users\SeanS\Downloads\cir_app\data\assessments", filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

################################################################################
# 1. MOTION 2D (RELATIVE MOTION & FRAMES)
################################################################################

# 1A. Language Decoding & Translation Only (Motion 2D)
m2d_lang_items = []
for i in range(1, 11):
    m2d_lang_items.append({
        "id": f"m2d-lang-rel-{i}",
        "type": "multipleChoice",
        "prompt": f"[First Three Steps] A river flows due east at {i} m/s. A boat that can travel {i+2} m/s in still water is pointed due north. What are the known vectors?",
        "choices": [
            {"id": "a", "text": f"$\\vec{{v}}_{{river/ground}}$ = {i} m/s East, $\\vec{{v}}_{{boat/river}}$ = {i+2} m/s North"},
            {"id": "b", "text": f"$\\vec{{v}}_{{boat/ground}}$ = {i+2} m/s North, $\\vec{{v}}_{{river/ground}}$ = {i} m/s East"},
            {"id": "c", "text": f"$\\vec{{v}}_{{boat/ground}}$ = {i+2} m/s North, $\\vec{{v}}_{{boat/river}}$ = {i} m/s East"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Students often confuse 'speed in still water' with the final ground speed. 'Still water' means velocity relative to the medium (the river). Thus, $\\vec{v}_{boat/river}$ is known, NOT $\\vec{v}_{boat/ground}$."
    })
    m2d_lang_items.append({
        "id": f"m2d-lang-rain-{i}",
        "type": "multipleChoice",
        "prompt": f"[Language Decoding] A person runs at {i+1} m/s. Rain is falling vertically relative to the ground. The person observes the rain hitting them at an angle. Identify the target quantity.",
        "choices": [
            {"id": "a", "text": "The angle of $\\vec{v}_{rain/person}$"},
            {"id": "b", "text": "The magnitude of $\\vec{v}_{rain/ground}$"},
            {"id": "c", "text": "The angle of $\\vec{v}_{person/ground}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** 'Observes the rain hitting them' implies the frame of reference of the person. The requested quantity is the direction of the rain relative to the person."
    })

m2d_lang_data = {
    "schemaVersion": 1, "id": "phys-m2d-lang-decoding-quiz", "title": "Relative Motion - Language Decoding",
    "assessmentType": "quiz", "categoryId": "physics-1", "subcategoryIds": ["physics-motion-2d"],
    "navigation": {"learningGoal": "practice", "activityType": "focusedPractice", "tags": ["translation-only"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10, "questions": m2d_lang_items
}

# 1B. Frame ID Drill
m2d_frame_items = []
for i in range(1, 16):
    m2d_frame_items.append({
        "id": f"m2d-frame-chain-{i}",
        "type": "multipleChoice",
        "prompt": "[Translation Chain] Frame A moves relative to B. Frame B moves relative to C. To find the velocity of A relative to C, write the vector chain.",
        "choices": [
            {"id": "a", "text": "$\\vec{v}_{A/C} = \\vec{v}_{A/B} + \\vec{v}_{B/C}$"},
            {"id": "b", "text": "$\\vec{v}_{A/C} = \\vec{v}_{A/B} - \\vec{v}_{B/C}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** The 'inner' subscripts must match and cancel out. A/B + B/C leaves A/C."
    })
    m2d_frame_items.append({
        "id": f"m2d-frame-inv-{i}",
        "type": "multipleChoice",
        "prompt": "[Frame Identification] An airplane (A) feels a wind (W) blowing from the North relative to the ground (G). Express the wind velocity vector mathematically.",
        "choices": [
            {"id": "a", "text": "$\\vec{v}_{W/G}$ points South"},
            {"id": "b", "text": "$\\vec{v}_{W/G}$ points North"},
            {"id": "c", "text": "$\\vec{v}_{A/W}$ points North"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** 'Blowing FROM the North' means the vector points South. Students commonly invert meteorological directions."
    })

m2d_frame_data = {
    "schemaVersion": 1, "id": "phys-m2d-frame-id-drill", "title": "Relative Motion - Frame Identification",
    "assessmentType": "quiz", "categoryId": "physics-1", "subcategoryIds": ["physics-motion-2d"],
    "navigation": {"learningGoal": "practice", "activityType": "focusedPractice", "tags": ["translation-only"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 15, "questions": m2d_frame_items
}

# 1C. Diagram Interpretation
m2d_diag_items = []
for i in range(1, 11):
    m2d_diag_items.append({
        "id": f"m2d-diag-plane-{i}",
        "type": "multipleChoice",
        "prompt": "[Diagram Interpretation] A vector triangle shows $\\vec{A}$ pointing East, $\\vec{B}$ pointing North, and $\\vec{C}$ acting as the hypotenuse from the tail of A to the tip of B. If this represents relative motion, which equation applies?",
        "choices": [
            {"id": "a", "text": "$\\vec{C} = \\vec{A} + \\vec{B}$"},
            {"id": "b", "text": "$\\vec{B} = \\vec{A} + \\vec{C}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Head-to-tail addition means the sum is drawn from the first tail to the final head."
    })
    m2d_diag_items.append({
        "id": f"m2d-diag-boat-{i}",
        "type": "multipleChoice",
        "prompt": "[Diagram Interpretation] A boat's velocity relative to water is drawn perpendicular to the river's velocity. The resultant vector $\\vec{v}_{boat/ground}$ points diagonally. Does the boat reach the exact opposite point on the bank?",
        "choices": [
            {"id": "a", "text": "No, it drifts downstream."},
            {"id": "b", "text": "Yes, its heading guarantees it."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** To reach the exact opposite point, the *resultant* vector must be perpendicular to the bank, meaning the boat must head *upstream*."
    })

m2d_diag_data = {
    "schemaVersion": 1, "id": "phys-m2d-diagram-mastery", "title": "Relative Motion - Diagram Interpretation",
    "assessmentType": "quiz", "categoryId": "physics-1", "subcategoryIds": ["physics-motion-2d"],
    "navigation": {"learningGoal": "practice", "activityType": "focusedPractice", "tags": ["diagrams"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10, "questions": m2d_diag_items
}

# 1D. Tiered Setup Test
m2d_test_items = []
for i in range(1, 11):
    m2d_test_items.append({
        "id": f"m2d-test-t1-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 1: Direct] Set up the equation for a plane flying East at $V$ through a wind blowing North at $W$. Find the ground speed magnitude $v_g$.",
        "choices": [
            {"id": "a", "text": "$v_g = \\sqrt{V^2 + W^2}$"},
            {"id": "b", "text": "$v_g = V + W$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Direct Pythagorean theorem setup for perpendicular vectors."
    })
    m2d_test_items.append({
        "id": f"m2d-test-t2-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 2: Disguised] Set up the equation for the heading angle $\\theta$ (relative to the bank) a boat must take to cross a river straight across. Boat speed is $V_b$, river speed is $V_r$.",
        "choices": [
            {"id": "a", "text": "$\\cos(\\theta) = V_r / V_b$"},
            {"id": "b", "text": "$\\tan(\\theta) = V_r / V_b$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** The resultant must be perpendicular to the bank, meaning the upstream component of the boat's velocity ($V_b \\cos\\theta$) must perfectly cancel the river velocity ($V_r$)."
    })
    m2d_test_items.append({
        "id": f"m2d-test-t3-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 3: Exam-Style] Two cars approach an intersection. Car A moves North at $v_A$. Car B moves East at $v_B$. Set up the vector $\\vec{v}_{A/B}$.",
        "choices": [
            {"id": "a", "text": "$v_A \\hat{j} - v_B \\hat{i}$"},
            {"id": "b", "text": "$v_A \\hat{j} + v_B \\hat{i}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** $\\vec{v}_{A/B} = \\vec{v}_A - \\vec{v}_B$. This is subtraction of vectors in a shared frame (ground)."
    })
    m2d_test_items.append({
        "id": f"m2d-test-t4-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 4: Novel] A passenger on a train moving at $V$ throws a ball forward at $v$. The train is accelerating at $a$. Set up the acceleration of the ball relative to the ground while it is in the air.",
        "choices": [
            {"id": "a", "text": "$\\vec{a}_{ball/ground} = -g \\hat{j}$"},
            {"id": "b", "text": "$\\vec{a}_{ball/ground} = a \\hat{i} - g \\hat{j}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Once the ball leaves the hand, it is no longer interacting with the train. Its only acceleration is gravity. Frame translation applies to velocity, but acceleration requires an interacting force!"
    })

m2d_test_data = {
    "schemaVersion": 1, "id": "phys-m2d-tiered-setup-test", "title": "Relative Motion - Tiered Setup Test",
    "assessmentType": "test", "categoryId": "physics-1", "subcategoryIds": ["physics-motion-2d"],
    "navigation": {"learningGoal": "evaluate", "activityType": "formalTest", "tags": ["translation-only"]},
    "modeDefault": "evaluate", "randomizeQuestions": True, "attemptQuestionCount": 20, "questions": m2d_test_items
}

################################################################################
# 2. NEWTON'S LAWS (FBDs & FORCE ID)
################################################################################

n2_lang_items = []
for i in range(1, 11):
    n2_lang_items.append({
        "id": f"n2-lang-fbd-{i}",
        "type": "multipleChoice",
        "prompt": "[First Three Steps] 'A block of mass m is held against a vertical wall by a horizontal applied force P.' Identify the system to isolate and the target unknown if asked for the minimum force P to prevent slipping.",
        "choices": [
            {"id": "a", "text": "System: Block. Target: P, assuming static friction $f_s = \\mu_s N$ points UP."},
            {"id": "b", "text": "System: Wall. Target: N."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** To prevent slipping down, friction must point up. The normal force is provided by the wall, horizontal."
    })
    n2_lang_items.append({
        "id": f"n2-lang-pulley-{i}",
        "type": "multipleChoice",
        "prompt": "[Language Decoding] 'Two masses are connected by a light string over a frictionless pulley. M1 is on a smooth table, M2 hangs vertically.' What does 'smooth' and 'light' imply?",
        "choices": [
            {"id": "a", "text": "Smooth = zero friction. Light = massless string (tension is uniform)."},
            {"id": "b", "text": "Smooth = constant velocity. Light = massless pulley."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** 'Smooth' is standard physics code for frictionless. 'Light' means massless."
    })

n2_lang_data = {
    "schemaVersion": 1, "id": "phys-n2-lang-decoding-quiz", "title": "Newton's Laws - Language Decoding",
    "assessmentType": "quiz", "categoryId": "physics-1", "subcategoryIds": ["physics-newton-laws"],
    "navigation": {"learningGoal": "practice", "activityType": "focusedPractice", "tags": ["translation-only"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10, "questions": n2_lang_items
}

n2_frame_items = []
for i in range(1, 16):
    n2_frame_items.append({
        "id": f"n2-frame-3rd-{i}",
        "type": "multipleChoice",
        "prompt": "[Force Identification] A horse pulls a cart. What is the Newton's Third Law reaction pair to the force of the horse pulling the cart?",
        "choices": [
            {"id": "a", "text": "The cart pulling back on the horse."},
            {"id": "b", "text": "The friction of the ground on the cart."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Third Law pairs ALWAYS act on different objects and involve the exact same interaction type."
    })
    n2_frame_items.append({
        "id": f"n2-frame-norm-{i}",
        "type": "multipleChoice",
        "prompt": "[Force Identification] You are standing in an elevator accelerating upward. Which force is strictly larger in magnitude than gravity?",
        "choices": [
            {"id": "a", "text": "The normal force from the floor."},
            {"id": "b", "text": "The tension in the elevator cable."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** FBD on the PERSON: N (up) and mg (down). Since a is UP, N > mg. FBD on the ELEVATOR involves tension, but tension doesn't directly act on the person."
    })

n2_frame_data = {
    "schemaVersion": 1, "id": "phys-n2-force-id-drill", "title": "Newton's Laws - Force Identification",
    "assessmentType": "quiz", "categoryId": "physics-1", "subcategoryIds": ["physics-newton-laws"],
    "navigation": {"learningGoal": "practice", "activityType": "focusedPractice", "tags": ["translation-only"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 15, "questions": n2_frame_items
}

n2_diag_items = []
for i in range(1, 11):
    n2_diag_items.append({
        "id": f"n2-diag-ramp-{i}",
        "type": "multipleChoice",
        "prompt": "[Diagram Interpretation] In a standard inclined plane FBD tilted at angle $\\theta$, the gravity vector $mg$ points straight down. What is the component of gravity perpendicular to the plane?",
        "choices": [
            {"id": "a", "text": "$mg \\cos\\theta$"},
            {"id": "b", "text": "$mg \\sin\\theta$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Students must memorize or quickly derive the geometry: perpendicular is cosine, parallel is sine for the standard ramp."
    })
    n2_diag_items.append({
        "id": f"n2-diag-atwood-{i}",
        "type": "multipleChoice",
        "prompt": "[Diagram Interpretation] In an Atwood machine diagram, $m_1 < m_2$. If we assign 'up' as positive for $m_1$, what MUST be the positive direction for $m_2$ to write a coupled system of equations $a_1 = a_2 = a$?",
        "choices": [
            {"id": "a", "text": "Down"},
            {"id": "b", "text": "Up"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** The coordinate system must 'bend' around the pulley. If $m_1$ accelerating up is positive, $m_2$ accelerating down must also be positive."
    })

n2_diag_data = {
    "schemaVersion": 1, "id": "phys-n2-diagram-mastery", "title": "Newton's Laws - Diagram Interpretation",
    "assessmentType": "quiz", "categoryId": "physics-1", "subcategoryIds": ["physics-newton-laws"],
    "navigation": {"learningGoal": "practice", "activityType": "focusedPractice", "tags": ["diagrams"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10, "questions": n2_diag_items
}

n2_test_items = []
for i in range(1, 11):
    n2_test_items.append({
        "id": f"n2-test-t1-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 1: Direct] Set up Newton's Second Law for a block of mass $m$ pushed horizontally with force $F$ on a frictionless surface.",
        "choices": [
            {"id": "a", "text": "$\\Sigma F_x = F = m a_x$"},
            {"id": "b", "text": "$\\Sigma F_x = F - mg = m a_x$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** The simplest direct application. Gravity and normal force cancel in the y-direction."
    })
    n2_test_items.append({
        "id": f"n2-test-t2-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 2: Disguised] Set up the y-equation for a block of mass $m$ pulled by a rope at an upward angle $\\theta$ with tension $T$. The block does not leave the floor.",
        "choices": [
            {"id": "a", "text": "$\\Sigma F_y = N + T\\sin\\theta - mg = 0$"},
            {"id": "b", "text": "$\\Sigma F_y = N - mg = 0$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** The normal force is reduced because the tension provides some upward lift."
    })
    n2_test_items.append({
        "id": f"n2-test-t3-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 3: Exam-Style] Two blocks $m_1$ and $m_2$ are in contact on a frictionless table. A force $F$ pushes on $m_1$. Set up the equation to find the contact force $F_c$ between them.",
        "choices": [
            {"id": "a", "text": "Treat as a system to find $a = F / (m_1+m_2)$, then isolate $m_2$: $F_c = m_2 a$."},
            {"id": "b", "text": "$F_c = F$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** The internal contact force depends entirely on the mass being accelerated by that specific boundary."
    })
    n2_test_items.append({
        "id": f"n2-test-t4-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 4: Novel] A pendulum hangs from the ceiling of a train accelerating horizontally at $a$. Set up the equations to find the angle $\\theta$ it hangs at equilibrium relative to the train.",
        "choices": [
            {"id": "a", "text": "$T\\sin\\theta = ma$ and $T\\cos\\theta = mg$"},
            {"id": "b", "text": "$T = ma$ and $mg = 0$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** In the ground frame, the tension must provide the horizontal acceleration $ma$ while balancing gravity $mg$."
    })

n2_test_data = {
    "schemaVersion": 1, "id": "phys-n2-tiered-setup-test", "title": "Newton's Laws - Tiered Setup Test",
    "assessmentType": "test", "categoryId": "physics-1", "subcategoryIds": ["physics-newton-laws"],
    "navigation": {"learningGoal": "evaluate", "activityType": "formalTest", "tags": ["translation-only"]},
    "modeDefault": "evaluate", "randomizeQuestions": True, "attemptQuestionCount": 20, "questions": n2_test_items
}

################################################################################
# 3. FRICTION
################################################################################

fric_lang_items = []
for i in range(1, 11):
    fric_lang_items.append({
        "id": f"fric-lang-{i}",
        "type": "multipleChoice",
        "prompt": "[First Three Steps] 'A block is sliding down a rough incline at a constant velocity.' What are the immediate mathematical translations?",
        "choices": [
            {"id": "a", "text": "$a = 0$, $f_k = \\mu_k N$, and $f_k$ points UP the incline."},
            {"id": "b", "text": "$a > 0$, $f_s = \\mu_s N$, and $f_s$ points DOWN the incline."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** 'Constant velocity' means zero acceleration. 'Sliding' means kinetic friction. Friction opposes motion."
    })
    fric_lang_items.append({
        "id": f"fric-lang-static-{i}",
        "type": "multipleChoice",
        "prompt": "[Language Decoding] 'Determine the maximum force P before the block begins to move.' Which friction regime applies?",
        "choices": [
            {"id": "a", "text": "Max static friction: $f_s = \\mu_s N$"},
            {"id": "b", "text": "Kinetic friction: $f_k = \\mu_k N$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** 'Before it begins to move' or 'on the verge of slipping' requires exactly the maximum static friction limit."
    })

fric_lang_data = {
    "schemaVersion": 1, "id": "phys-fric-lang-decoding-quiz", "title": "Friction - Language Decoding",
    "assessmentType": "quiz", "categoryId": "physics-1", "subcategoryIds": ["physics-friction"],
    "navigation": {"learningGoal": "practice", "activityType": "focusedPractice", "tags": ["translation-only"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10, "questions": fric_lang_items
}

fric_frame_items = []
for i in range(1, 16):
    fric_frame_items.append({
        "id": f"fric-frame-dir-{i}",
        "type": "multipleChoice",
        "prompt": "[Force Identification] A car accelerates forward. What force is pushing the car forward?",
        "choices": [
            {"id": "a", "text": "Static friction from the road pushing forward on the tires."},
            {"id": "b", "text": "The engine pushing the car."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** The tires attempt to slide backwards relative to the road. Static friction opposes this by pushing the tires FORWARD."
    })
    fric_frame_items.append({
        "id": f"fric-frame-stack-{i}",
        "type": "multipleChoice",
        "prompt": "[Force Identification] Block A sits on Block B. You pull Block B to the right, and Block A moves with it without slipping. What force accelerates Block A?",
        "choices": [
            {"id": "a", "text": "Static friction from Block B pointing to the right."},
            {"id": "b", "text": "Static friction from Block B pointing to the left."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** A tends to stay at rest (relative to the ground). Relative to B, A tends to slide left. Friction opposes this relative slipping by pushing A to the right."
    })

fric_frame_data = {
    "schemaVersion": 1, "id": "phys-fric-force-id-drill", "title": "Friction - Force Identification",
    "assessmentType": "quiz", "categoryId": "physics-1", "subcategoryIds": ["physics-friction"],
    "navigation": {"learningGoal": "practice", "activityType": "focusedPractice", "tags": ["translation-only"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 15, "questions": fric_frame_items
}

fric_diag_items = []
for i in range(1, 11):
    fric_diag_items.append({
        "id": f"fric-diag-ramp-{i}",
        "type": "multipleChoice",
        "prompt": "[Diagram Interpretation] In a diagram of a block pushed UP a rough ramp by a force parallel to the ramp, how many forces point DOWN the ramp?",
        "choices": [
            {"id": "a", "text": "Two: the parallel component of gravity ($mg\\sin\\theta$) and kinetic friction."},
            {"id": "b", "text": "One: just gravity."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Since motion is UP the ramp, friction points DOWN the ramp, combining with the gravity component."
    })
    fric_diag_items.append({
        "id": f"fric-diag-wall-{i}",
        "type": "multipleChoice",
        "prompt": "[Diagram Interpretation] A diagram shows a book held against a wall by a diagonal force pushing up and in. Which direction does friction point?",
        "choices": [
            {"id": "a", "text": "It depends on whether the vertical component of the push is greater or less than gravity."},
            {"id": "b", "text": "Always up."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Static friction opposes *intended* motion. If the push is strong enough, the book tends to slide UP, so friction points DOWN."
    })

fric_diag_data = {
    "schemaVersion": 1, "id": "phys-fric-diagram-mastery", "title": "Friction - Diagram Interpretation",
    "assessmentType": "quiz", "categoryId": "physics-1", "subcategoryIds": ["physics-friction"],
    "navigation": {"learningGoal": "practice", "activityType": "focusedPractice", "tags": ["diagrams"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10, "questions": fric_diag_items
}

fric_test_items = []
for i in range(1, 11):
    fric_test_items.append({
        "id": f"fric-test-t1-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 1: Direct] Set up the equation for a block sliding to a stop on a horizontal surface.",
        "choices": [
            {"id": "a", "text": "$-\\mu_k mg = m a_x$"},
            {"id": "b", "text": "$\\mu_k mg = 0$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Normal force equals mg. Friction is the only horizontal force, pointing opposite to velocity."
    })
    fric_test_items.append({
        "id": f"fric-test-t2-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 2: Disguised] Set up the equation to find the minimum coefficient of static friction to park a car on a hill of angle $\\theta$.",
        "choices": [
            {"id": "a", "text": "$\\mu_s (mg\\cos\\theta) = mg\\sin\\theta \\implies \\mu_s = \\tan\\theta$"},
            {"id": "b", "text": "$\\mu_s mg = mg\\sin\\theta$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Normal force is $mg\\cos\\theta$. The required friction must balance $mg\\sin\\theta$."
    })
    fric_test_items.append({
        "id": f"fric-test-t3-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 3: Exam-Style] A block $m_1$ on a rough horizontal table ($\\mu_k$) is pulled by a hanging mass $m_2$ via a pulley. Set up the system of equations.",
        "choices": [
            {"id": "a", "text": "$T - \\mu_k m_1 g = m_1 a$ and $m_2 g - T = m_2 a$"},
            {"id": "b", "text": "$m_2 g - \\mu_k m_1 g = 0$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** Coupled system. $T$ pulls $m_1$ forward, friction opposes. For $m_2$, gravity pulls down, $T$ pulls up."
    })
    fric_test_items.append({
        "id": f"fric-test-t4-{i}",
        "type": "multipleChoice",
        "prompt": "[Tier 4: Novel] A rotating cylindrical space station creates artificial gravity. A person leans against a vertical wall. Set up the friction equation preventing them from sliding down the wall.",
        "choices": [
            {"id": "a", "text": "$f_s = mg \\le \\mu_s (m \\frac{v^2}{R})$"},
            {"id": "b", "text": "$f_s = \\mu_s mg$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "**Instructor Notes:** The 'Normal' force is the centripetal force $mv^2/R$. Friction must balance actual gravity $mg$."
    })

fric_test_data = {
    "schemaVersion": 1, "id": "phys-fric-tiered-setup-test", "title": "Friction - Tiered Setup Test",
    "assessmentType": "test", "categoryId": "physics-1", "subcategoryIds": ["physics-friction"],
    "navigation": {"learningGoal": "evaluate", "activityType": "formalTest", "tags": ["translation-only"]},
    "modeDefault": "evaluate", "randomizeQuestions": True, "attemptQuestionCount": 20, "questions": fric_test_items
}

# SAVE ALL FILES
save_yaml("phys-m2d-lang-decoding-quiz.yaml", m2d_lang_data)
save_yaml("phys-m2d-frame-id-drill.yaml", m2d_frame_data)
save_yaml("phys-m2d-diagram-mastery.yaml", m2d_diag_data)
save_yaml("phys-m2d-tiered-setup-test.yaml", m2d_test_data)

save_yaml("phys-n2-lang-decoding-quiz.yaml", n2_lang_data)
save_yaml("phys-n2-force-id-drill.yaml", n2_frame_data)
save_yaml("phys-n2-diagram-mastery.yaml", n2_diag_data)
save_yaml("phys-n2-tiered-setup-test.yaml", n2_test_data)

save_yaml("phys-fric-lang-decoding-quiz.yaml", fric_lang_data)
save_yaml("phys-fric-force-id-drill.yaml", fric_frame_data)
save_yaml("phys-fric-diagram-mastery.yaml", fric_diag_data)
save_yaml("phys-fric-tiered-setup-test.yaml", fric_test_data)

print("Generated massive Physics translation suites (12 files).")

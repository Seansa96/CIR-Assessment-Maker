import os
import yaml

def save_yaml(filename, data):
    path = os.path.join(r"c:\Users\SeanS\Downloads\cir_app\data\assessments", filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

# 1. Advanced Concept Lesson (Disk/Washer)
lesson_dw_data = {
    "schemaVersion": 1,
    "id": "calc2-disk-washer-advanced-concept-lesson",
    "title": "Volumes by Disk and Washer - Advanced Concept Lesson",
    "assessmentType": "conceptLesson",
    "categoryId": "calculus-2",
    "subcategoryIds": ["volumes-of-solids"],
    "navigation": {"learningGoal": "learn", "activityType": "conceptLesson", "tags": ["advanced"]},
    "lesson": {
        "introduction": "This lesson explores advanced applications of the disk and washer methods, focusing on shifted axes and interpreting complex cross sections.",
        "sections": [
            {
                "id": "sec-1",
                "title": "The Geometric Derivation of the Washer",
                "content": "The volume of a washer is simply the volume of a large disk minus the volume of a smaller inner disk: $V = \\pi R^2 h - \\pi r^2 h = \\pi (R^2 - r^2) h$. Crucially, it is NOT $\\pi (R - r)^2 h$.",
                "check": {
                    "id": "check-1",
                    "type": "multipleChoice",
                    "prompt": "Why is the integrand in the washer method $R(x)^2 - r(x)^2$ and not $(R(x) - r(x))^2$?",
                    "choices": [
                        {"id": "a", "text": "Because you are subtracting areas (Area of outer circle minus Area of inner circle)."},
                        {"id": "b", "text": "Because $(R - r)^2 = R^2 - r^2$."}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "The area of the cross section is $\\pi R^2 - \\pi r^2$. Thus, we integrate $\\pi (R^2 - r^2)$."
                }
            },
            {
                "id": "sec-2",
                "title": "Shifted Horizontal Axes",
                "content": "When revolving around $y = k$ (instead of $y = 0$), the radius is the distance from the curve $y = f(x)$ to the line $y = k$. This distance is $|f(x) - k|$.",
                "check": {
                    "id": "check-2",
                    "type": "multipleChoice",
                    "prompt": "If $f(x) = x^2$ and you revolve around $y = -3$, what is the radius $R(x)$?",
                    "choices": [
                        {"id": "a", "text": "$x^2 + 3$"},
                        {"id": "b", "text": "$x^2 - 3$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "The distance is $f(x) - (-3) = x^2 + 3$."
                }
            },
            {
                "id": "sec-3",
                "title": "Shifted Vertical Axes",
                "content": "When revolving around $x = k$, slices are horizontal (using $dy$). You must solve your equations for $x$. The radius is $|x(y) - k|$.",
                "check": {
                    "id": "check-3",
                    "type": "multipleChoice",
                    "prompt": "If revolving $y = \\sqrt{x}$ around $x = 5$, what is the radius function in terms of $y$?",
                    "choices": [
                        {"id": "a", "text": "$5 - y^2$"},
                        {"id": "b", "text": "$y^2 - 5$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "First, solve for $x$: $x = y^2$. Since $x=5$ is to the right of the curve (assuming $x < 5$), the distance is $5 - y^2$."
                }
            },
            {
                "id": "sec-4",
                "title": "Cross Sections: Base vs Height",
                "content": "When volume is defined by cross sections (not revolution), you integrate the Area formula of that shape. If cross sections are squares, $A = s^2$. The side $s$ is the distance across the base region.",
                "check": {
                    "id": "check-4",
                    "type": "multipleChoice",
                    "prompt": "If the base is a circle $x^2 + y^2 = 9$ and cross sections $\\perp$ to the $x$-axis are squares, what is $s$?",
                    "choices": [
                        {"id": "a", "text": "$2\\sqrt{9-x^2}$"},
                        {"id": "b", "text": "$\\sqrt{9-x^2}$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "The side stretches from the bottom of the circle $y = -\\sqrt{9-x^2}$ to the top $y = \\sqrt{9-x^2}$. The length is top minus bottom: $2\\sqrt{9-x^2}$."
                }
            },
            {
                "id": "sec-5",
                "title": "Cross Sections: Equilateral Triangles",
                "content": "For equilateral triangles, the area is $A = \\frac{\\sqrt{3}}{4}s^2$.",
                "check": {
                    "id": "check-5",
                    "type": "multipleChoice",
                    "prompt": "If $s = 2\\sqrt{1-x^2}$, what is the Area function $A(x)$ for an equilateral triangle cross section?",
                    "choices": [
                        {"id": "a", "text": "$\\sqrt{3}(1-x^2)$"},
                        {"id": "b", "text": "$\\frac{\\sqrt{3}}{4}(1-x^2)$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Square $s$ to get $4(1-x^2)$. Multiply by $\\frac{\\sqrt{3}}{4}$ to get $\\sqrt{3}(1-x^2)$."
                }
            },
            {
                "id": "sec-6",
                "title": "Determining 'Inner' vs 'Outer'",
                "content": "The outer radius $R(x)$ is always the distance from the axis of revolution to the curve FURTHEST from it. The inner radius $r(x)$ is the distance to the CLOSEST curve.",
                "check": {
                    "id": "check-6",
                    "type": "multipleChoice",
                    "prompt": "If region bounded by $y = 2$ and $y = 5$ is revolved around $y = 0$, what is $R(x)$?",
                    "choices": [
                        {"id": "a", "text": "5"},
                        {"id": "b", "text": "2"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "$y=5$ is further from $y=0$ than $y=2$."
                }
            }
        ]
    }
}

# 2. Advanced Concept Lesson (Shells)
lesson_shell_data = {
    "schemaVersion": 1,
    "id": "calc2-shells-advanced-concept-lesson",
    "title": "Volumes by Cylindrical Shells - Advanced Concept Lesson",
    "assessmentType": "conceptLesson",
    "categoryId": "calculus-2",
    "subcategoryIds": ["cylindrical-shells"],
    "navigation": {"learningGoal": "learn", "activityType": "conceptLesson", "tags": ["advanced"]},
    "lesson": {
        "introduction": "This lesson deepens the understanding of cylindrical shells, particularly why they are used when functions are non-invertible.",
        "sections": [
            {
                "id": "sec-1",
                "title": "The Geometry of a Shell",
                "content": "A shell is a hollow cylinder. Its volume is roughly its surface area multiplied by its thickness: $V \\approx (2\\pi r h) \\Delta x$.",
                "check": {
                    "id": "check-1",
                    "type": "multipleChoice",
                    "prompt": "Why does the shell method formula include a $2\\pi$ instead of a $\\pi$?",
                    "choices": [
                        {"id": "a", "text": "Because it derives from the circumference of a circle ($2\\pi r$)."},
                        {"id": "b", "text": "Because it is twice the volume of a disk."}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "If you unroll a cylindrical shell, it forms a rectangular slab with length $2\\pi r$, height $h$, and thickness $dx$."
                }
            },
            {
                "id": "sec-2",
                "title": "When to Use Shells",
                "content": "Shells are sliced PARALLEL to the axis of revolution. If revolving around a vertical axis ($y$-axis), shells use $dx$. If revolving around a horizontal axis ($x$-axis), shells use $dy$.",
                "check": {
                    "id": "check-2",
                    "type": "multipleChoice",
                    "prompt": "Revolving around $x = 4$ using Shells requires integrating with respect to:",
                    "choices": [
                        {"id": "a", "text": "$x$"},
                        {"id": "b", "text": "$y$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "The axis $x=4$ is vertical. Shells slice parallel to the vertical axis, meaning slices are vertical. Vertical slices have thickness $dx$."
                }
            },
            {
                "id": "sec-3",
                "title": "The Non-Invertible Problem",
                "content": "Consider $y = x^3 - 3x^2 + 2x$ revolved around the $y$-axis. Washers would require horizontal slices ($dy$), forcing us to solve this cubic for $x$ in terms of $y$. This is practically impossible. Shells save us by using $dx$!",
                "check": {
                    "id": "check-3",
                    "type": "multipleChoice",
                    "prompt": "True or False: Shells allow us to find volumes of revolution for functions that cannot be explicitly inverted.",
                    "choices": [
                        {"id": "a", "text": "True"},
                        {"id": "b", "text": "False"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Yes. By slicing parallel to the axis of revolution, we integrate with respect to the independent variable of the given function."
                }
            },
            {
                "id": "sec-4",
                "title": "Radius for Shifted Axes",
                "content": "If revolving around $x = k$, the radius of a shell at position $x$ is the distance between $x$ and $k$. This is $|x - k|$.",
                "check": {
                    "id": "check-4",
                    "type": "multipleChoice",
                    "prompt": "Revolving the region $[1, 3]$ around the axis $x = -2$. What is $r(x)$?",
                    "choices": [
                        {"id": "a", "text": "$x + 2$"},
                        {"id": "b", "text": "$x - 2$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "The distance from a point $x$ (which is positive) to $-2$ is $x - (-2) = x + 2$."
                }
            },
            {
                "id": "sec-5",
                "title": "Height of the Shell",
                "content": "The height of the shell $h(x)$ is simply the top boundary minus the bottom boundary at position $x$.",
                "check": {
                    "id": "check-5",
                    "type": "multipleChoice",
                    "prompt": "If bounded by $y = e^x$ and $y = 0$, what is $h(x)$?",
                    "choices": [
                        {"id": "a", "text": "$e^x$"},
                        {"id": "b", "text": "$e^x - x$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Top minus bottom is $e^x - 0 = e^x$."
                }
            },
            {
                "id": "sec-6",
                "title": "Volume by Shells vs Washers",
                "content": "Both methods will yield the exact same numerical volume if set up correctly. Choosing between them is a matter of algebraic convenience.",
                "check": {
                    "id": "check-6",
                    "type": "multipleChoice",
                    "prompt": "Which method always yields a larger volume?",
                    "choices": [
                        {"id": "a", "text": "Shells"},
                        {"id": "b", "text": "Washers"},
                        {"id": "c", "text": "Neither, they yield the exact same volume."}
                    ],
                    "answer": {"choiceId": "c"},
                    "explanation": "They are simply two different ways of accumulating the exact same 3D space."
                }
            }
        ]
    }
}

# 3. Recall Drills
recall_dw_items = []
recall_sh_items = []
for i in range(1, 16):
    # Disk/Washer recognition
    recall_dw_items.append({
        "id": f"dw-recall-{i}",
        "type": "multipleChoice",
        "prompt": f"Revolve region bounded by $y = x^{{{i}}}$ and $y = 0$ around $x$-axis. Identify the method and setup.",
        "choices": [
            {"id": "a", "text": f"Disk: $\\pi \\int (x^{{{i}}})^2 \\, dx$"},
            {"id": "b", "text": f"Shell: $2\\pi \\int x(x^{{{i}}}) \\, dx$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "Revolving around a horizontal axis with functions in terms of x requires vertical slices, which are perpendicular to the axis. This implies Disk/Washer."
    })
    recall_dw_items.append({
        "id": f"dw-recall-shift-{i}",
        "type": "multipleChoice",
        "prompt": f"Revolve region $y = x^{{{i}}}$ around $y = -{i}$. What is the outer radius $R(x)$?",
        "choices": [
            {"id": "a", "text": f"$x^{{{i}}} + {i}$"},
            {"id": "b", "text": f"$x^{{{i}}} - {i}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"Distance is $x^{{{i}}} - (-{i}) = x^{{{i}}} + {i}$."
    })
    
    # Shell recognition
    recall_sh_items.append({
        "id": f"sh-recall-{i}",
        "type": "multipleChoice",
        "prompt": f"Revolve region bounded by $y = \\sin({i}x)$ and $y = 0$ around $y$-axis. Identify the most efficient method and setup.",
        "choices": [
            {"id": "a", "text": f"Shell: $2\\pi \\int x \\sin({i}x) \\, dx$"},
            {"id": "b", "text": f"Disk: $\\pi \\int (\\arcsin(y/{i}))^2 \\, dy$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "Solving for $x$ involves inverse trig functions which are awful to integrate. Shells use $dx$ and avoid this entirely."
    })
    recall_sh_items.append({
        "id": f"sh-recall-shift-{i}",
        "type": "multipleChoice",
        "prompt": f"Revolve region $[0, 1]$ around $x = {i+2}$. What is the shell radius $r(x)$?",
        "choices": [
            {"id": "a", "text": f"${i+2} - x$"},
            {"id": "b", "text": f"$x + {i+2}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"Since $x$ is between 0 and 1, the axis $x={i+2}$ is to the right. Distance is Right - Left = ${i+2} - x$."
    })

recall_dw_data = {
    "schemaVersion": 1,
    "id": "calc2-disk-washer-setup-recall",
    "title": "Volumes by Disk/Washer - Setup Recall Drill",
    "assessmentType": "recallDrill",
    "categoryId": "calculus-2",
    "subcategoryIds": ["volumes-of-solids"],
    "navigation": {"learningGoal": "recall", "activityType": "mixedRecallSet", "tags": ["drill"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10,
    "items": recall_dw_items
}

recall_sh_data = {
    "schemaVersion": 1,
    "id": "calc2-volume-method-duel-recall",
    "title": "Volumes by Shells - Setup Recall Drill",
    "assessmentType": "recallDrill",
    "categoryId": "calculus-2",
    "subcategoryIds": ["cylindrical-shells"],
    "navigation": {"learningGoal": "recall", "activityType": "mixedRecallSet", "tags": ["drill"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10,
    "items": recall_sh_items
}

# 4. Hard Tests (40 questions procedurally generated via templates)
hard_test_dw_questions = []
hard_test_sh_questions = []

for i in range(1, 21):
    hard_test_dw_questions.append({
        "id": f"hard-dw-{i}",
        "type": "multipleChoice",
        "prompt": f"Find the volume generated by revolving $y = {i}x$ and $y = {i}x^2$ around the $x$-axis.",
        "choices": [
            {"id": "a", "text": f"$\\frac{{2\\pi {i**2}}}{{15}}$"},
            {"id": "b", "text": f"$\\frac{{\\pi {i**2}}}{{15}}$"},
            {"id": "c", "text": f"$\\frac{{4\\pi {i**2}}}{{15}}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"Intersection at $x=0, 1$. Washers: $V = \\pi \\int_0^1 [({i}x)^2 - ({i}x^2)^2] \\, dx = \\pi {i**2} \\int_0^1 (x^2 - x^4) \\, dx = \\pi {i**2} [1/3 - 1/5] = \\pi {i**2} (2/15) = \\frac{{2\\pi {i**2}}}{{15}}$."
    })
    prompt_dw_cross = "The base of a solid is the circle $x^2 + y^2 = C^2$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.".replace("C", str(i))
    ans_dw_cross = "$\\frac{16}{3} " + str(i**3) + "$"
    expl_dw_cross = "Base $s = 2\\sqrt{C^2-x^2}$. Area $A(x) = 4(C^2-x^2)$. Volume = $\\int_{-C}^{C} 4(C^2-x^2) \\, dx = 8 \\int_0^{C} (C^2-x^2) \\, dx = 8[xC^2 - x^3/3]_0^{C} = 8(C^3 - C^3/3) = 8(2C^3/3) = \\frac{16}{3} C^3$."
    expl_dw_cross = expl_dw_cross.replace("C^3", str(i**3)).replace("C^2", str(i**2)).replace("C", str(i))
    
    hard_test_dw_questions.append({
        "id": f"hard-dw-cross-{i}",
        "type": "multipleChoice",
        "prompt": prompt_dw_cross,
        "choices": [
            {"id": "a", "text": ans_dw_cross},
            {"id": "b", "text": f"$\\frac{{8}}{{3}} {i**3}$"},
            {"id": "c", "text": f"$\\frac{{4}}{{3}} \\pi {i**3}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": expl_dw_cross
    })
    
    hard_test_sh_questions.append({
        "id": f"hard-sh-{i}",
        "type": "multipleChoice",
        "prompt": f"Use shells to find the volume generated by revolving $y = {i}\\sqrt{{x}}$ and $y = 0, x = 1$ around the $y$-axis.",
        "choices": [
            {"id": "a", "text": f"$\\frac{{4\\pi {i}}}{5}$"},
            {"id": "b", "text": f"$\\frac{{2\\pi {i}}}{5}$"},
            {"id": "c", "text": f"$\\frac{{4\\pi {i}}}{3}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"Shells around y-axis: $V = 2\\pi \\int_0^1 x({i}\\sqrt{{x}}) \\, dx = 2\\pi {i} \\int_0^1 x^{{3/2}} \\, dx = 2\\pi {i} [\\frac{{2}}{{5}} x^{{5/2}}]_0^1 = \\frac{{4\\pi {i}}}{5}$."
    })
    hard_test_sh_questions.append({
        "id": f"hard-sh-shift-{i}",
        "type": "multipleChoice",
        "prompt": f"Set up the shell integral for revolving $y = {i}x - x^2$ and $y=0$ around $x = -{i}$.",
        "choices": [
            {"id": "a", "text": f"$2\\pi \\int_0^{{{i}}} (x + {i})({i}x - x^2) \\, dx$"},
            {"id": "b", "text": f"$2\\pi \\int_0^{{{i}}} (x - {i})({i}x - x^2) \\, dx$"},
            {"id": "c", "text": f"$\\pi \\int_0^{{{i}}} (x + {i})^2 ({i}x - x^2) \\, dx$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"Radius is $x - (-{i}) = x + {i}$. Height is ${i}x - x^2$. Integral is $2\\pi \\int_0^{{{i}}} (x + {i})({i}x - x^2) \\, dx$."
    })

hard_test_dw_data = {
    "schemaVersion": 1, "id": "calc2-disk-washer-hard-test", "title": "Disk/Washer Volumes - Formal Hard Test",
    "assessmentType": "test", "categoryId": "calculus-2", "subcategoryIds": ["volumes-of-solids"],
    "navigation": {"learningGoal": "evaluate", "activityType": "formalTest", "tags": ["advanced"]},
    "modeDefault": "evaluate", "randomizeQuestions": True, "attemptQuestionCount": 15, "questions": hard_test_dw_questions
}

hard_test_sh_data = {
    "schemaVersion": 1, "id": "calc2-shells-hard-test", "title": "Cylindrical Shells - Formal Hard Test",
    "assessmentType": "test", "categoryId": "calculus-2", "subcategoryIds": ["cylindrical-shells"],
    "navigation": {"learningGoal": "evaluate", "activityType": "formalTest", "tags": ["advanced"]},
    "modeDefault": "evaluate", "randomizeQuestions": True, "attemptQuestionCount": 15, "questions": hard_test_sh_questions
}

# Save all
save_yaml("calc2-disk-washer-advanced-concept-lesson.yaml", lesson_dw_data)
save_yaml("calc2-shells-advanced-concept-lesson.yaml", lesson_shell_data)
save_yaml("calc2-disk-washer-setup-recall.yaml", recall_dw_data)
save_yaml("calc2-volume-method-duel-recall.yaml", recall_sh_data)
save_yaml("calc2-disk-washer-hard-test.yaml", hard_test_dw_data)
save_yaml("calc2-shells-hard-test.yaml", hard_test_sh_data)

print("Generated Volumes massive suites.")

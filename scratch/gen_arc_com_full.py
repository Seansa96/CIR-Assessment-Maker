import os
import yaml

def save_yaml(filename, data):
    path = os.path.join(r"c:\Users\SeanS\Downloads\cir_app\data\assessments", filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

# 1. Advanced Concept Lesson (Arc Length / Surface Area)
lesson_arc_data = {
    "schemaVersion": 1,
    "id": "calc2-arc-surface-advanced-concept-lesson",
    "title": "Arc Length & Surface Area - Advanced Concept Lesson",
    "assessmentType": "conceptLesson",
    "categoryId": "calculus-2",
    "subcategoryIds": ["arc-length-surface-area"],
    "navigation": {"learningGoal": "learn", "activityType": "conceptLesson", "tags": ["advanced"]},
    "lesson": {
        "introduction": "This lesson deeply explores the ds element, the algebraic tricks used to evaluate these integrals, and the geometric origins of the formulas.",
        "sections": [
            {
                "id": "sec-1",
                "title": "The Origin of ds",
                "content": "The arc length element $ds$ comes from the Pythagorean theorem: $ds = \\sqrt{dx^2 + dy^2}$. Factoring out $dx$ gives $ds = \\sqrt{1 + (dy/dx)^2} \\, dx$. Factoring out $dy$ gives $ds = \\sqrt{(dx/dy)^2 + 1} \\, dy$.",
                "check": {
                    "id": "check-1",
                    "type": "multipleChoice",
                    "prompt": "If $x = \\ln(y)$, what is $ds$ in terms of $dy$?",
                    "choices": [
                        {"id": "a", "text": "$\\sqrt{1/y^2 + 1} \\, dy$"},
                        {"id": "b", "text": "$\\sqrt{1 + y^2} \\, dy$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "$dx/dy = 1/y$. Squaring it gives $1/y^2$."
                }
            },
            {
                "id": "sec-2",
                "title": "The Frustum of a Cone",
                "content": "Surface area of revolution uses the formula for the lateral area of a frustum: $S = 2\\pi r L$. In calculus, this becomes $S = \\int 2\\pi r \\, ds$. The radius $r$ depends on the axis of revolution.",
                "check": {
                    "id": "check-2",
                    "type": "multipleChoice",
                    "prompt": "If revolving $y = x^3$ around the $y$-axis, what is $r$?",
                    "choices": [
                        {"id": "a", "text": "$x$"},
                        {"id": "b", "text": "$y$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "The distance from the curve to the $y$-axis is the $x$-coordinate."
                }
            },
            {
                "id": "sec-3",
                "title": "The Perfect Square Trick",
                "content": "Many arc length problems are rigged. The expression $1 + (f'(x))^2$ will often simplify perfectly into a binomial squared, $(g(x))^2$, allowing the square root to cancel out.",
                "check": {
                    "id": "check-3",
                    "type": "multipleChoice",
                    "prompt": "If $1 + (y')^2 = 1 + (\\frac{1}{2}x^2 - \\frac{1}{2x^2})^2$, what does it simplify to?",
                    "choices": [
                        {"id": "a", "text": "$(\\frac{1}{2}x^2 + \\frac{1}{2x^2})^2$"},
                        {"id": "b", "text": "It requires trig substitution."}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Expanding gives $1 + (\\frac{1}{4}x^4 - \\frac{1}{2} + \\frac{1}{4x^4}) = \\frac{1}{4}x^4 + \\frac{1}{2} + \\frac{1}{4x^4}$. This perfectly factors back into $(\\frac{1}{2}x^2 + \\frac{1}{2x^2})^2$."
                }
            },
            {
                "id": "sec-4",
                "title": "Choosing dx vs dy",
                "content": "Sometimes $ds$ in terms of $dx$ results in an impossible integral, but $ds$ in terms of $dy$ is trivial. For instance, if $y = \\int_1^x \\sqrt{t^3 - 1} \\, dt$, then $dy/dx = \\sqrt{x^3 - 1}$ by the FTC. Then $1 + (y')^2 = 1 + x^3 - 1 = x^3$.",
                "check": {
                    "id": "check-4",
                    "type": "multipleChoice",
                    "prompt": "If $1 + (y')^2 = x^3$, what is $ds$?",
                    "choices": [
                        {"id": "a", "text": "$x^{3/2} \\, dx$"},
                        {"id": "b", "text": "$x^3 \\, dx$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Take the square root: $\\sqrt{x^3} = x^{3/2}$."
                }
            },
            {
                "id": "sec-5",
                "title": "Gabriel's Horn",
                "content": "The region $y = 1/x$ for $x \\ge 1$ revolved around the $x$-axis has a finite volume ($\\pi$) but an infinite surface area. This paradox shows that improper integrals can converge for volume but diverge for area.",
                "check": {
                    "id": "check-5",
                    "type": "multipleChoice",
                    "prompt": "Why does the surface area of Gabriel's horn diverge?",
                    "choices": [
                        {"id": "a", "text": "Because $\\int 2\\pi (1/x) \\sqrt{1 + x^{-4}} \\, dx$ is greater than $\\int 2\\pi (1/x) \\, dx$, which diverges."},
                        {"id": "b", "text": "Because the volume formula squares the $1/x$ making it $1/x^2$."}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "By comparison test, since $\\sqrt{1+x^{-4}} > 1$, the integral is strictly greater than the integral of $1/x$, the harmonic series analog."
                }
            },
            {
                "id": "sec-6",
                "title": "Surface Area Pitfalls",
                "content": "A common mistake is confusing $r$ in $2\\pi r$. If revolving around $y=-2$, the radius is $y+2$. Also, do NOT forget the $\\sqrt{1+(y')^2}$ term. If you just write $2\\pi r$, you are finding the area of a cylinder, not following the curve.",
                "check": {
                    "id": "check-6",
                    "type": "multipleChoice",
                    "prompt": "Revolving $x = y^2$ around $y = 4$. What is the setup using $dy$?",
                    "choices": [
                        {"id": "a", "text": "$\\int 2\\pi(4-y)\\sqrt{1+(2y)^2} \\, dy$"},
                        {"id": "b", "text": "$\\int 2\\pi(y-4)\\sqrt{1+(2y)^2} \\, dy$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Radius is distance to axis. $4-y$ ensures positive radius if $y < 4$."
                }
            }
        ]
    }
}

# 2. Advanced Concept Lesson (Center of Mass)
lesson_com_data = {
    "schemaVersion": 1,
    "id": "calc2-com-average-advanced-concept-lesson",
    "title": "Center of Mass & Average Value - Advanced Concept Lesson",
    "assessmentType": "conceptLesson",
    "categoryId": "calculus-2",
    "subcategoryIds": ["center-of-mass-average-value"],
    "navigation": {"learningGoal": "learn", "activityType": "conceptLesson", "tags": ["advanced"]},
    "lesson": {
        "introduction": "This lesson covers the principles of moments, centroids, and exploiting symmetry to avoid integration entirely.",
        "sections": [
            {
                "id": "sec-1",
                "title": "Moments and Balance",
                "content": "A moment measures the tendency of a mass to cause rotation about an axis. $M_y = \\int x \\rho f(x) \\, dx$ is the moment about the y-axis, summing the (distance $x$) $\\times$ (mass of slice).",
                "check": {
                    "id": "check-1",
                    "type": "multipleChoice",
                    "prompt": "If a region is perfectly symmetric across the y-axis, what is $M_y$?",
                    "choices": [
                        {"id": "a", "text": "0"},
                        {"id": "b", "text": "Area"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "For every mass at positive $x$, there is an equal mass at negative $x$. They cancel out, meaning the system balances at $x=0$."
                }
            },
            {
                "id": "sec-2",
                "title": "Centroid Coordinates",
                "content": "The coordinates $(\\bar{x}, \\bar{y})$ are found by dividing the moments by the total area (assuming constant density $\\rho$). $\\bar{x} = M_y / A$ and $\\bar{y} = M_x / A$.",
                "check": {
                    "id": "check-2",
                    "type": "multipleChoice",
                    "prompt": "What does $M_x$ calculate?",
                    "choices": [
                        {"id": "a", "text": "The moment about the x-axis, used to find $\\bar{y}$."},
                        {"id": "b", "text": "The moment about the x-axis, used to find $\\bar{x}$."}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Moment about the x-axis depends on the y-distance. So it is used to calculate the average y-coordinate."
                }
            },
            {
                "id": "sec-3",
                "title": "The $1/2$ in $M_x$",
                "content": "When using vertical slices ($dx$), the center of mass of a rectangular slice is halfway up its height. Its height is $f(x) - g(x)$, so its center is $\\frac{f(x)+g(x)}{2}$. When multiplied by the height to get area, we get $\\frac{1}{2}(f(x)^2 - g(x)^2)$.",
                "check": {
                    "id": "check-3",
                    "type": "multipleChoice",
                    "prompt": "Why is $M_x = \\int \\frac{1}{2}(f(x)^2 - g(x)^2) \\, dx$?",
                    "choices": [
                        {"id": "a", "text": "Because it is derived from $(y_{avg}) \\times (Area) = \\frac{f(x)+g(x)}{2} \\times (f(x)-g(x))$. "},
                        {"id": "b", "text": "Because you are integrating a circle."}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Difference of squares: $(f+g)(f-g) = f^2 - g^2$."
                }
            },
            {
                "id": "sec-4",
                "title": "Average Value of a Function",
                "content": "The average value $f_{avg} = \\frac{1}{b-a} \\int_a^b f(x) \\, dx$. Geometrically, this is the height of a rectangle whose base is $(b-a)$ and whose area equals the area under the curve.",
                "check": {
                    "id": "check-4",
                    "type": "multipleChoice",
                    "prompt": "If $f_{avg} = 10$ on $[0, 5]$, what is $\\int_0^5 f(x) \\, dx$?",
                    "choices": [
                        {"id": "a", "text": "50"},
                        {"id": "b", "text": "2"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "$10 = \\frac{1}{5} \\int f(x) \\, dx \\implies \\int f(x) \\, dx = 50$."
                }
            },
            {
                "id": "sec-5",
                "title": "Mean Value Theorem for Integrals",
                "content": "If $f(x)$ is continuous, there is at least one point $c$ in $[a,b]$ such that $f(c) = f_{avg}$.",
                "check": {
                    "id": "check-5",
                    "type": "multipleChoice",
                    "prompt": "For $f(x) = x^2$ on $[0, 3]$, $f_{avg} = 3$. What is $c$?",
                    "choices": [
                        {"id": "a", "text": "$\\sqrt{3}$"},
                        {"id": "b", "text": "1.5"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Set $f(c) = 3$. $c^2 = 3 \\implies c = \\sqrt{3}$."
                }
            },
            {
                "id": "sec-6",
                "title": "Exploiting Symmetry",
                "content": "If you are asked for the centroid of a semi-circle $y = \\sqrt{R^2 - x^2}$, you know immediately that $\\bar{x} = 0$. You only need to calculate $\\bar{y}$.",
                "check": {
                    "id": "check-6",
                    "type": "multipleChoice",
                    "prompt": "What is the centroid of a circle centered at $(4, 5)$?",
                    "choices": [
                        {"id": "a", "text": "(4, 5)"},
                        {"id": "b", "text": "(0, 0)"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "The centroid of any completely symmetric shape is its geometric center."
                }
            }
        ]
    }
}

# 3. Recall Drills
recall_arc_items = []
recall_com_items = []
for i in range(1, 16):
    # Arc / Surface Area Recognition
    recall_arc_items.append({
        "id": f"arc-recall-{i}",
        "type": "multipleChoice",
        "prompt": f"Identify the integral for the arc length of $y = {i}x^{{3/2}}$ from $x=0$ to $x=1$.",
        "choices": [
            {"id": "a", "text": f"$\\int_0^1 \\sqrt{{1 + ({i*1.5} x^{{1/2}})^2}} \\, dx$"},
            {"id": "b", "text": f"$\\int_0^1 \\sqrt{{1 + {i}x^{{3/2}}}} \\, dx$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "$y' = 1.5 \\cdot {i} x^{1/2}$. Substitute into $\\sqrt{1 + (y')^2}$."
    })
    recall_arc_items.append({
        "id": f"sa-recall-{i}",
        "type": "multipleChoice",
        "prompt": f"Identify the integral for surface area revolving $y = \\sqrt{{{i}x}}$ around the $x$-axis.",
        "choices": [
            {"id": "a", "text": f"$\\int 2\\pi \\sqrt{{{i}x}} \\sqrt{{1 + (\\frac{{{i}}}{{2\\sqrt{{{i}x}}}})^2}} \\, dx$"},
            {"id": "b", "text": f"$\\int 2\\pi x \\sqrt{{1 + (\\frac{{{i}}}{{2\\sqrt{{{i}x}}}})^2}} \\, dx$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "Radius is distance to x-axis, which is $y = \\sqrt{{{i}x}}$."
    })
    
    # COM / Average Value Recognition
    recall_com_items.append({
        "id": f"com-recall-{i}",
        "type": "multipleChoice",
        "prompt": f"Set up $M_y$ for the region between $y={i}x$ and $y=x^2$.",
        "choices": [
            {"id": "a", "text": f"$\\int x ({i}x - x^2) \\, dx$"},
            {"id": "b", "text": f"$\\int \\frac{{1}}{{2}} (({i}x)^2 - (x^2)^2) \\, dx$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "$M_y = \\int x (top - bottom) \\, dx$."
    })
    recall_com_items.append({
        "id": f"avg-recall-{i}",
        "type": "multipleChoice",
        "prompt": f"Set up the average value of $f(x) = \\sin({i}x)$ on $[0, \\pi]$.",
        "choices": [
            {"id": "a", "text": f"$\\frac{{1}}{{\\pi}} \\int_0^\\pi \\sin({i}x) \\, dx$"},
            {"id": "b", "text": f"$\\int_0^\\pi \\sin({i}x) \\, dx$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "$f_{avg} = \\frac{1}{b-a} \\int_a^b f(x) \\, dx$."
    })

recall_arc_data = {
    "schemaVersion": 1, "id": "calc2-arc-surface-formula-recall", "title": "Arc Length / Surface Area - Recall Drill",
    "assessmentType": "recallDrill", "categoryId": "calculus-2", "subcategoryIds": ["arc-length-surface-area"],
    "navigation": {"learningGoal": "recall", "activityType": "mixedRecallSet", "tags": ["drill"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10, "items": recall_arc_items
}

recall_com_data = {
    "schemaVersion": 1, "id": "calc2-com-average-intuition-recall", "title": "Center of Mass - Recall Drill",
    "assessmentType": "recallDrill", "categoryId": "calculus-2", "subcategoryIds": ["center-of-mass-average-value"],
    "navigation": {"learningGoal": "recall", "activityType": "mixedRecallSet", "tags": ["drill"]},
    "modeDefault": "practice", "randomizeQuestions": True, "attemptQuestionCount": 10, "items": recall_com_items
}


# 4. Hard Tests (40 questions)
hard_test_arc_questions = []
hard_test_com_questions = []

for i in range(1, 21):
    prompt_arc = "Find the arc length of the curve $y = \\ln(\\cos(x))$ from $x=0$ to $x=\\pi/C$.".replace("C", str(i+2))
    hard_test_arc_questions.append({
        "id": f"hard-arc-{i}",
        "type": "multipleChoice",
        "prompt": prompt_arc,
        "choices": [
            {"id": "a", "text": f"$\\ln|\\sec(\\pi/{i+2}) + \\tan(\\pi/{i+2})|$"},
            {"id": "b", "text": f"$\\ln|\\sec(\\pi/{i+2})|$"},
            {"id": "c", "text": "1"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"$y' = \\frac{{-\\sin(x)}}{{\\cos(x)}} = -\\tan(x)$. $1 + (y')^2 = 1 + \\tan^2(x) = \\sec^2(x)$. $ds = \\sqrt{{\\sec^2(x)}} = \\sec(x) dx$. $\\int_0^{{\\pi/{i+2}}} \\sec(x) dx = \\ln|\\sec(x) + \\tan(x)|_0^{{\\pi/{i+2}}}$."
    })
    
    prompt_com = "Find $\\bar{y}$ for the region bounded by $y=C\\sqrt{x}$ and $y=Cx^3$.".replace("C", str(i))
    expl_com = "Intersection at $x=1$. Area = $\\int_0^1 (C x^{1/2} - C x^3) dx = C(2/3 - 1/4) = C(5/12)$. $M_x = \\int_0^1 \\frac{1}{2} ((C x^{1/2})^2 - (C x^3)^2) dx = \\frac{C^2}{2} \\int_0^1 (x - x^6) dx = \\frac{C^2}{2} (1/2 - 1/7) = \\frac{C^2}{2} (5/14) = \\frac{5C^2}{28}$. $\\bar{y} = M_x / A = \\frac{5C^2}{28} / \\frac{5C}{12} = \\frac{C*12}{28} = \\frac{C*3}{7}$."
    expl_com = expl_com.replace("C^2", str(i**2)).replace("C*12", str(i*12)).replace("C*3", str(i*3)).replace("C", str(i)).replace("y", "y")
    
    hard_test_com_questions.append({
        "id": f"hard-com-{i}",
        "type": "multipleChoice",
        "prompt": prompt_com,
        "choices": [
            {"id": "a", "text": f"$\\frac{{{i*3}}}{{7}}$"},
            {"id": "b", "text": f"$\\frac{{{i*5}}}{{14}}$"},
            {"id": "c", "text": f"$\\frac{{{i*2}}}{{5}}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": expl_com
    })

hard_test_arc_data = {
    "schemaVersion": 1, "id": "calc2-arc-surface-hard-test", "title": "Arc Length / Surface Area - Formal Hard Test",
    "assessmentType": "test", "categoryId": "calculus-2", "subcategoryIds": ["arc-length-surface-area"],
    "navigation": {"learningGoal": "evaluate", "activityType": "formalTest", "tags": ["advanced"]},
    "modeDefault": "evaluate", "randomizeQuestions": True, "attemptQuestionCount": 15, "questions": hard_test_arc_questions
}

hard_test_com_data = {
    "schemaVersion": 1, "id": "calc2-com-average-hard-test", "title": "Center of Mass - Formal Hard Test",
    "assessmentType": "test", "categoryId": "calculus-2", "subcategoryIds": ["center-of-mass-average-value"],
    "navigation": {"learningGoal": "evaluate", "activityType": "formalTest", "tags": ["advanced"]},
    "modeDefault": "evaluate", "randomizeQuestions": True, "attemptQuestionCount": 15, "questions": hard_test_com_questions
}

# Save all
save_yaml("calc2-arc-surface-advanced-concept-lesson.yaml", lesson_arc_data)
save_yaml("calc2-com-average-advanced-concept-lesson.yaml", lesson_com_data)
save_yaml("calc2-arc-surface-formula-recall.yaml", recall_arc_data)
save_yaml("calc2-com-average-intuition-recall.yaml", recall_com_data)
save_yaml("calc2-arc-surface-hard-test.yaml", hard_test_arc_data)
save_yaml("calc2-com-average-hard-test.yaml", hard_test_com_data)

print("Generated Arc/COM massive suites.")

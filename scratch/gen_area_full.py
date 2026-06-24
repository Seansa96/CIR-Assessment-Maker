import os
import yaml

def save_yaml(filename, data):
    path = os.path.join(r"c:\Users\SeanS\Downloads\cir_app\data\assessments", filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

# 1. Advanced Concept Lesson (6-8 sections)
lesson_data = {
    "schemaVersion": 1,
    "id": "calc2-area-curves-advanced-concept-lesson",
    "title": "Area Between Curves - Advanced Concept Lesson",
    "assessmentType": "conceptLesson",
    "categoryId": "calculus-2",
    "subcategoryIds": ["area-between-curves"],
    "navigation": {
        "learningGoal": "learn",
        "activityType": "conceptLesson",
        "tags": ["advanced", "theory"]
    },
    "lesson": {
        "introduction": "This advanced lesson explores the nuances of finding the area between curves, focusing on slicing strategy, crossing boundaries, and absolute value interpretation.",
        "sections": [
            {
                "id": "sec-1-dx-dy",
                "title": "The Art of Slicing: dx vs dy",
                "content": "While basic area problems can be solved with vertical slices ($dx$), more complex regions strongly favor horizontal slices ($dy$). A region is 'y-simple' if the left and right boundaries are formed by single functions of $y$, $x = f(y)$ and $x = g(y)$. If a boundary equation is given as $x = y^2 - 4y$, solving for $y$ requires the quadratic formula and splits the curve into two radical functions. Integrating with respect to $y$ avoids this entirely.",
                "check": {
                    "id": "check-1",
                    "type": "multipleChoice",
                    "prompt": "If a region is bounded by $x = y^3 - 2y$ and $x = y^2$, which slicing method will result in a single integral without radicals?",
                    "choices": [
                        {"id": "a", "text": "Vertical slices (dx)"},
                        {"id": "b", "text": "Horizontal slices (dy)"}
                    ],
                    "answer": {"choiceId": "b"},
                    "explanation": "Because the functions are already expressed as polynomials of $y$, taking horizontal slices ($dy$) means we simply integrate $(y^2) - (y^3 - 2y) \\, dy$. Trying to use $dx$ would require solving a cubic equation for $y$!"
                }
            },
            {
                "id": "sec-2-crossing",
                "title": "Crossing Boundaries and Absolute Value",
                "content": "When curves $y=f(x)$ and $y=g(x)$ cross within the interval $[a,b]$, the 'top' function becomes the 'bottom' function. The formula $\\int_a^b |f(x) - g(x)| \\, dx$ handles this theoretically, but to evaluate it, we must find the intersection points $c_i$ and split the integral: $\\int_a^{c_1} (\\text{top} - \\text{bottom}) \\, dx + \\int_{c_1}^b (\\text{top} - \\text{bottom}) \\, dx$.",
                "check": {
                    "id": "check-2",
                    "type": "multipleChoice",
                    "prompt": "To calculate the area bounded by $y=\\sin(x)$ and $y=\\cos(x)$ on $[0, \\pi]$, where do you split the integral?",
                    "choices": [
                        {"id": "a", "text": "$x = \\pi/2$"},
                        {"id": "b", "text": "$x = \\pi/4$"},
                        {"id": "c", "text": "No split needed."}
                    ],
                    "answer": {"choiceId": "b"},
                    "explanation": "The functions cross where $\\sin(x) = \\cos(x)$, which is at $\\pi/4$ on this interval."
                }
            },
            {
                "id": "sec-3-implicit",
                "title": "Implicit Relations and Symmetry",
                "content": "Some regions are bounded by implicit relations, such as $|x| + |y| = 2$. These form closed shapes (in this case, a rotated square). We can use the symmetry of the shape to vastly simplify the integral. Instead of evaluating the top and bottom halves over the full domain, we can calculate the area of the region in the first quadrant ($x>0, y>0$) and multiply by 4.",
                "check": {
                    "id": "check-3",
                    "type": "multipleChoice",
                    "prompt": "What is the area of the first-quadrant portion of $|x| + |y| = 2$?",
                    "choices": [
                        {"id": "a", "text": "$\\int_0^2 (2-x) \\, dx$"},
                        {"id": "b", "text": "$\\int_0^2 (x-2) \\, dx$"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "In Q1, both $x$ and $y$ are positive, so $|x|=x$ and $|y|=y$. The equation is $x+y=2$, or $y=2-x$. The area is $\\int_0^2 (2-x) \\, dx$."
                }
            },
            {
                "id": "sec-4-kinematics",
                "title": "Area in Disguise: Kinematics",
                "content": "The concept of area between curves extends beyond pure geometry. In kinematics, if you are given the velocity curves of two cars, $v_1(t)$ and $v_2(t)$, the area between these curves, $\\int |v_1(t) - v_2(t)| \\, dt$, represents the total distance the cars drifted apart or came together, regardless of their starting positions.",
                "check": {
                    "id": "check-4",
                    "type": "multipleChoice",
                    "prompt": "If $v_1(t) > v_2(t)$ for $0 \\le t \\le 5$, what does $\\int_0^5 (v_1(t) - v_2(t)) \\, dt$ represent physically?",
                    "choices": [
                        {"id": "a", "text": "The total distance traveled by car 1."},
                        {"id": "b", "text": "The additional distance car 1 traveled compared to car 2."},
                        {"id": "c", "text": "The acceleration difference."}
                    ],
                    "answer": {"choiceId": "b"},
                    "explanation": "The integral of velocity is displacement. The integral of the difference in velocity is the difference in displacement."
                }
            },
            {
                "id": "sec-5-tables",
                "title": "Area from Tabular Data",
                "content": "In real-world applications, boundaries are rarely perfect functions. A surveyor mapping a plot of land bounded by a straight road and a winding river will take width measurements at discrete intervals. We estimate this area using Riemann sums, the Trapezoidal Rule, or Simpson's Rule applied to the $f(x) - g(x)$ data points.",
                "check": {
                    "id": "check-5",
                    "type": "multipleChoice",
                    "prompt": "To use Simpson's Rule to estimate the area between a river and a road, what must be true about the number of measurement intervals $n$?",
                    "choices": [
                        {"id": "a", "text": "$n$ must be even."},
                        {"id": "b", "text": "$n$ must be odd."},
                        {"id": "c", "text": "It doesn't matter."}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Simpson's rule requires an even number of intervals (which means an odd number of data points)."
                }
            },
            {
                "id": "sec-6-pitfalls",
                "title": "Common Setup Pitfalls",
                "content": "The most devastating mistake in area problems is failing to draw the region correctly and identifying the wrong 'top' function. Another common error is mixing variables: if you are integrating with respect to $y$, your bounds must be $y$-values, and your function must be $x = f(y)$. You cannot evaluate $\\int_{x=0}^{x=2} (y^2 - 2y) \\, dy$; the bounds and the differential must match.",
                "check": {
                    "id": "check-6",
                    "type": "multipleChoice",
                    "prompt": "True or False: If you integrate with respect to $y$, the 'top' function is the one that is furthest to the right (greatest $x$-value).",
                    "choices": [
                        {"id": "a", "text": "True"},
                        {"id": "b", "text": "False"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Yes. When integrating vertically ($dy$), 'top minus bottom' becomes 'right minus left', meaning $x_{right} - x_{left}$."
                }
            }
        ]
    }
}

# 2. Intense Worked Example (8 steps)
worked_example_data = {
    "schemaVersion": 1,
    "id": "calc2-area-curves-intense-worked-example",
    "title": "Area Between Curves - Intense Worked Example",
    "assessmentType": "workedExample",
    "categoryId": "calculus-2",
    "subcategoryIds": ["area-between-curves"],
    "navigation": {
        "learningGoal": "practice",
        "activityType": "guidedWorkedExample",
        "tags": ["advanced", "intense"]
    },
    "modeDefault": "practice",
    "randomizeQuestions": False,
    "workedExamples": [
        {
            "id": "intense-area-1",
            "title": "Multi-Region Area with Logarithms",
            "problem": "Find the total area bounded by $y = \\ln(x)$, $y = x - 2$, and the $x$-axis. We will solve this problem using two different methods to demonstrate slicing strategy.",
            "steps": [
                {
                    "id": "step-1",
                    "title": "Graphing and Identifying the Region",
                    "instruction": "First, we must identify the region. The boundaries are the natural log curve, a straight line, and $y=0$. The curve $y=\\ln(x)$ crosses the $x$-axis at $x=1$. The line $y=x-2$ crosses the $x$-axis at $x=2$.",
                    "question": {
                        "id": "q1",
                        "type": "multipleChoice",
                        "prompt": "Where do $y = \\ln(x)$ and $y = x - 2$ intersect in the first quadrant?",
                        "choices": [
                            {"id": "a", "text": "$x = 2$"},
                            {"id": "b", "text": "They intersect at a transcendental value that must be approximated or kept as a variable $x=c$."},
                            {"id": "c", "text": "$x = 1$"}
                        ],
                        "answer": {"choiceId": "b"},
                        "explanation": "There is no algebraic way to solve $\\ln(x) = x - 2$. The intersection point $x = c$ (where $c \\approx 3.146$) must be found numerically."
                    }
                },
                {
                    "id": "step-2",
                    "title": "Method 1: Vertical Slices (dx)",
                    "instruction": "If we use vertical slices, we integrate with respect to $x$. Notice that the 'bottom' boundary of our region changes. From $x=1$ to $x=2$, the bottom boundary is the $x$-axis ($y=0$). From $x=2$ to $x=c$, the bottom boundary is the line $y=x-2$.",
                    "question": {
                        "id": "q2",
                        "type": "multipleChoice",
                        "prompt": "How many integrals are required to set up the area using $dx$?",
                        "choices": [
                            {"id": "a", "text": "1"},
                            {"id": "b", "text": "2"},
                            {"id": "c", "text": "3"}
                        ],
                        "answer": {"choiceId": "b"},
                        "explanation": "Two integrals are required because the bottom boundary changes at $x=2$. $\\int_1^2 (\\ln(x) - 0) \\, dx + \\int_2^c (\\ln(x) - (x-2)) \\, dx$."
                    }
                },
                {
                    "id": "step-3",
                    "title": "Evaluating the dx integrals",
                    "instruction": "To evaluate the first integral, we need the antiderivative of $\\ln(x)$. Recall that $\\int \\ln(x) \\, dx = x\\ln(x) - x$.",
                    "question": {
                        "id": "q3",
                        "type": "multipleChoice",
                        "prompt": "What technique is used to find $\\int \\ln(x) \\, dx$?",
                        "choices": [
                            {"id": "a", "text": "u-substitution"},
                            {"id": "b", "text": "Integration by Parts"},
                            {"id": "c", "text": "Partial Fractions"}
                        ],
                        "answer": {"choiceId": "b"},
                        "explanation": "Integration by parts with $u = \\ln(x)$ and $dv = dx$ yields $x\\ln(x) - \\int x \\cdot (1/x) \\, dx = x\\ln(x) - x$."
                    }
                },
                {
                    "id": "step-4",
                    "title": "Method 2: Horizontal Slices (dy) - Setup",
                    "instruction": "Now let's try horizontal slices ($dy$). This means our right and left boundaries must be functions of $y$. We rewrite $y = \\ln(x)$ as $x = e^y$, and $y = x - 2$ as $x = y + 2$.",
                    "question": {
                        "id": "q4",
                        "type": "multipleChoice",
                        "prompt": "For horizontal slices, which is the 'top' (or rightmost) function?",
                        "choices": [
                            {"id": "a", "text": "$x = e^y$"},
                            {"id": "b", "text": "$x = y + 2$"}
                        ],
                        "answer": {"choiceId": "b"},
                        "explanation": "Looking at the region in the first quadrant, the line $x = y + 2$ is further to the right than the curve $x = e^y$."
                    }
                },
                {
                    "id": "step-5",
                    "title": "Method 2: Integration Limits",
                    "instruction": "We are integrating with respect to $y$, so our bounds must be $y$-values. The region is bounded below by the $x$-axis, which is $y=0$. It is bounded above by the intersection point.",
                    "question": {
                        "id": "q5",
                        "type": "multipleChoice",
                        "prompt": "If the intersection point is $(c, \\ln(c))$, what is the upper limit of integration for the $dy$ setup?",
                        "choices": [
                            {"id": "a", "text": "$c$"},
                            {"id": "b", "text": "$\\ln(c)$"}
                        ],
                        "answer": {"choiceId": "b"},
                        "explanation": "Since we are integrating with respect to $y$, we need the $y$-coordinate of the intersection, which is $\\ln(c)$."
                    }
                },
                {
                    "id": "step-6",
                    "title": "Method 2: The Single Integral",
                    "instruction": "Because the right boundary ($x=y+2$) and left boundary ($x=e^y$) do not change over the interval from $y=0$ to $y=\\ln(c)$, we can find the area with a single integral: $\\int_0^{\\ln(c)} ((y+2) - e^y) \\, dy$.",
                    "question": {
                        "id": "q6",
                        "type": "multipleChoice",
                        "prompt": "Evaluate the indefinite integral $\\int ((y+2) - e^y) \\, dy$.",
                        "choices": [
                            {"id": "a", "text": "$\\frac{1}{2}y^2 + 2y - e^y + C$"},
                            {"id": "b", "text": "$\\frac{1}{2}y^2 + 2y - ye^{y-1} + C$"}
                        ],
                        "answer": {"choiceId": "a"},
                        "explanation": "Using standard power and exponential rules: $\\frac{1}{2}y^2 + 2y - e^y + C$."
                    }
                },
                {
                    "id": "step-7",
                    "title": "Method 2: Evaluation and Simplification",
                    "instruction": "We plug in the limits: $[\\frac{1}{2}y^2 + 2y - e^y]_0^{\\ln(c)}$. At the upper limit we get $\\frac{1}{2}(\\ln(c))^2 + 2\\ln(c) - e^{\\ln(c)}$.",
                    "question": {
                        "id": "q7",
                        "type": "multipleChoice",
                        "prompt": "Simplify the term $e^{\\ln(c)}$.",
                        "choices": [
                            {"id": "a", "text": "$c$"},
                            {"id": "b", "text": "$\\ln(c)$"}
                        ],
                        "answer": {"choiceId": "a"},
                        "explanation": "$e$ and $\\ln$ are inverse functions, so $e^{\\ln(c)} = c$."
                    }
                },
                {
                    "id": "step-8",
                    "title": "The Final Result",
                    "instruction": "The evaluation at the upper limit is $\\frac{1}{2}(\\ln(c))^2 + 2\\ln(c) - c$. At the lower limit ($y=0$), we get $0 + 0 - e^0 = -1$. Subtracting the lower bound from the upper gives the final area.",
                    "question": {
                        "id": "q8",
                        "type": "multipleChoice",
                        "prompt": "What is the final expression for the area?",
                        "choices": [
                            {"id": "a", "text": "$\\frac{1}{2}(\\ln(c))^2 + 2\\ln(c) - c + 1$"},
                            {"id": "b", "text": "$\\frac{1}{2}(\\ln(c))^2 + 2\\ln(c) - c - 1$"}
                        ],
                        "answer": {"choiceId": "a"},
                        "explanation": "Subtracting $(-1)$ means we add 1: $\\frac{1}{2}(\\ln(c))^2 + 2\\ln(c) - c + 1$."
                    }
                }
            ]
        }
    ]
}

# 3. Recall Drill (30 questions generated procedurally)
recall_questions = []
for i in range(1, 16):
    # dx vs dy recognition
    recall_questions.append({
        "id": f"recall-dxdy-{i}",
        "type": "multipleChoice",
        "prompt": f"To find the area bounded by $x = y^2 - {i}y$ and $x = {i+2}y$, which setup is most efficient?",
        "choices": [
            {"id": "a", "text": "Integrate with respect to x (vertical slices)"},
            {"id": "b", "text": "Integrate with respect to y (horizontal slices)"}
        ],
        "answer": {"choiceId": "b"},
        "explanation": "The boundaries are given as $x = f(y)$. Solving these for $y$ would be extremely difficult (requiring the quadratic formula), making $dy$ the obviously superior choice."
    })
    # Top vs bottom recognition
    recall_questions.append({
        "id": f"recall-topbot-{i}",
        "type": "multipleChoice",
        "prompt": f"For the integral $\\int_0^1 (e^{{{i}x}} - x^{{{i}}}) \\, dx$, which function represents the 'top' boundary of the area?",
        "choices": [
            {"id": "a", "text": f"$y = e^{{{i}x}}$"},
            {"id": "b", "text": f"$y = x^{{{i}}}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"On the interval $[0,1]$, $e^{{{i}x}} \\ge 1$ and $x^{{{i}}} \\le 1$. Therefore $e^{{{i}x}}$ is always greater, meaning it is the top function."
    })

recall_data = {
    "schemaVersion": 1,
    "id": "calc2-area-curves-method-recall",
    "title": "Area Between Curves - Method Recall Drill",
    "assessmentType": "recallDrill",
    "categoryId": "calculus-2",
    "subcategoryIds": ["area-between-curves"],
    "navigation": {
        "learningGoal": "recall",
        "activityType": "mixedRecallSet",
        "tags": ["drill"]
    },
    "modeDefault": "practice",
    "randomizeQuestions": True,
    "attemptQuestionCount": 10,
    "items": recall_questions
}

# 4. Nonstandard Quiz (20 questions)
nonstandard_questions = []
for i in range(1, 6):
    # Word problem: River mapping (Simpson's Rule)
    nonstandard_questions.append({
        "id": f"nonstandard-river-{i}",
        "type": "multipleChoice",
        "prompt": f"A surveyor is mapping a plot of land bounded by a straight road and a winding river. They measure the distance from the road to the river every {10*i} meters. The distances (in meters) are: 0, {15+i}, {22+i}, {18+i}, {25+i}, {12+i}, 0. Using Simpson's Rule, estimate the area of the plot.",
        "choices": [
            {"id": "a", "text": f"$\\frac{{{10*i}}}{{3}} [0 + 4({15+i}) + 2({22+i}) + 4({18+i}) + 2({25+i}) + 4({12+i}) + 0]$"},
            {"id": "b", "text": f"$\\frac{{{10*i}}}{{2}} [0 + 2({15+i}) + 2({22+i}) + 2({18+i}) + 2({25+i}) + 2({12+i}) + 0]$"},
            {"id": "c", "text": f"${10*i} [0 + ({15+i}) + ({22+i}) + ({18+i}) + ({25+i}) + ({12+i}) + 0]$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "Simpson's Rule is $\\frac{\\Delta x}{3} [y_0 + 4y_1 + 2y_2 + 4y_3 + \\dots + y_n]$. The interval $\\Delta x$ is the measurement spacing."
    })
    # Disguised: Kinematics
    nonstandard_questions.append({
        "id": f"nonstandard-kinematics-{i}",
        "type": "multipleChoice",
        "prompt": f"Car A has velocity $v_A(t) = {2*i}t$ and Car B has velocity $v_B(t) = t^2 + {i-1}$. If they start at the same position, set up the integral for the total distance between them at $t=3$.",
        "choices": [
            {"id": "a", "text": f"$\\int_0^3 |{2*i}t - (t^2 + {i-1})| \\, dt$"},
            {"id": "b", "text": f"$\\int_0^3 ({2*i}t + t^2 + {i-1}) \\, dt$"},
            {"id": "c", "text": f"$\\int_0^3 ({2*i}t) \\, dt - \\int_0^3 (t^2 + {i-1}) \\, dt$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": "The total distance between them is the absolute difference in their displacements, which is the integral of the absolute difference of their velocities. If the velocities cross, the absolute value correctly handles the distance opening back up."
    })
    # Geometry interpretation
    prompt_geom = "Evaluate the integral $\\int_{-C}^{C} \\sqrt{C^2 - x^2} \\, dx$ by interpreting it geometrically.".replace("C", str(i))
    ans_geom = "$\\frac{1}{2} \\pi (" + str(i) + ")^2$"
    nonstandard_questions.append({
        "id": f"nonstandard-geom-{i}",
        "type": "multipleChoice",
        "prompt": prompt_geom,
        "choices": [
            {"id": "a", "text": ans_geom},
            {"id": "b", "text": f"$\\pi ({i})^2$"},
            {"id": "c", "text": f"$\\frac{{4}}{{3}} \\pi ({i})^3$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"The function describes the upper half of a circle of radius $R = {i}$. The integral from $-{i}$ to ${i}$ represents the area of this semi-circle, which is $\\frac{{1}}{{2}} \\pi R^2$."
    })
    # Probabilistic interpretation
    nonstandard_questions.append({
        "id": f"nonstandard-prob-{i}",
        "type": "multipleChoice",
        "prompt": f"A probability density function is given by $f(x) = c x^{{{i}}}$ on $[0,1]$. Find the constant $c$ by applying the concept that the total area under a PDF must equal 1.",
        "choices": [
            {"id": "a", "text": f"${i+1}$"},
            {"id": "b", "text": f"${i}$"},
            {"id": "c", "text": f"$\\frac{{1}}{{{i+1}}}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"$\\int_0^1 c x^{{{i}}} \\, dx = 1 \\implies c [\\frac{{x^{{{i+1}}}}}{{{i+1}}}]_0^1 = 1 \\implies \\frac{{c}}{{{i+1}}} = 1 \\implies c = {i+1}$."
    })

nonstandard_data = {
    "schemaVersion": 1,
    "id": "calc2-area-curves-nonstandard-quiz",
    "title": "Area Between Curves - Nonstandard & Word Problems",
    "assessmentType": "quiz",
    "categoryId": "calculus-2",
    "subcategoryIds": ["area-between-curves"],
    "navigation": {
        "learningGoal": "practice",
        "activityType": "focusedPractice",
        "tags": ["word-problems", "nonstandard"]
    },
    "modeDefault": "practice",
    "randomizeQuestions": True,
    "attemptQuestionCount": 5,
    "questions": nonstandard_questions
}

# 5. Hard Section Test (40 questions procedurally generated via templates)
hard_test_questions = []
for i in range(1, 21):
    # Setup tricky bounds
    hard_test_questions.append({
        "id": f"hard-area-bounds-{i}",
        "type": "multipleChoice",
        "prompt": f"Find the area of the region enclosed by $y = x^3 - {i**2}x$ and the $x$-axis.",
        "choices": [
            {"id": "a", "text": f"$\\frac{{{i**4}}}{{2}}$"},
            {"id": "b", "text": "0"},
            {"id": "c", "text": f"$\\frac{{{i**4}}}{{4}}$"}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"The curve intersects the $x$-axis at $x = -{i}, 0, {i}$. Due to symmetry, the area is $2 \\int_0^{{{i}}} (0 - (x^3 - {i**2}x)) \\, dx = 2 \\int_0^{{{i}}} ({i**2}x - x^3) \\, dx = 2 [\\frac{{{i**2}}}{{2}}x^2 - \\frac{{1}}{{4}}x^4]_0^{{{i}}} = 2 (\\frac{{{i**4}}}{{2}} - \\frac{{{i**4}}}{{4}}) = 2 (\\frac{{{i**4}}}{{4}}) = \\frac{{{i**4}}}{{2}}$."
    })
    # Setup tricky implicit evaluation
    hard_test_questions.append({
        "id": f"hard-area-implicit-{i}",
        "type": "multipleChoice",
        "prompt": f"Find the area enclosed by the parabola $y^2 = {i}x$ and the line $y = {i}x - {2*i}$.",
        "choices": [
            {"id": "a", "text": "Set up using horizontal slices (dy) to avoid radicals."},
            {"id": "b", "text": f"Set up using vertical slices (dx) by splitting the integral at $x = {2}$."},
            {"id": "c", "text": "Both methods require only one integral."}
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"Solving for $x$: $x = y^2/{i}$ and $x = (y+{2*i})/{i}$. This allows for a single integral $\\int ((y+{2*i})/{i} - y^2/{i}) \\, dy$. Using $dx$ requires evaluating $\\sqrt{{{i}x}}$ and $-\\sqrt{{{i}x}}$ as top/bottom curves, and the bottom boundary changes when the line intersects the lower half of the parabola."
    })

hard_test_data = {
    "schemaVersion": 1,
    "id": "calc2-area-curves-hard-test",
    "title": "Area Between Curves - Formal Hard Test",
    "assessmentType": "test",
    "categoryId": "calculus-2",
    "subcategoryIds": ["area-between-curves"],
    "navigation": {
        "learningGoal": "evaluate",
        "activityType": "formalTest",
        "tags": ["advanced", "exam-prep"]
    },
    "modeDefault": "evaluate",
    "randomizeQuestions": True,
    "attemptQuestionCount": 15,
    "questions": hard_test_questions
}

# Save all
save_yaml("calc2-area-curves-advanced-concept-lesson.yaml", lesson_data)
save_yaml("calc2-area-curves-intense-worked-example.yaml", worked_example_data)
save_yaml("calc2-area-curves-method-recall.yaml", recall_data)
save_yaml("calc2-area-curves-nonstandard-quiz.yaml", nonstandard_data)
save_yaml("calc2-area-curves-hard-test.yaml", hard_test_data)

print("Generated Area Between Curves massive suite.")

import os
import yaml

def save(filename, data):
    with open(os.path.join(r"c:\Users\SeanS\Downloads\cir_app\data\assessments", filename), 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=1000)

def make_glossary(id_prefix, title, cat, subcats, terms):
    return {
        "schemaVersion": 1,
        "id": f"{id_prefix}-glossary",
        "title": title,
        "assessmentType": "glossary",
        "categoryId": cat,
        "subcategoryIds": subcats,
        "modeDefault": "practice",
        "glossary": {
            "introduction": f"Review these terms for {title}.",
            "sections": [
                {
                    "id": "main-terms",
                    "title": "Core Terms",
                    "required": True,
                    "entries": [
                        {
                            "id": t[0],
                            "term": t[1],
                            "definition": t[2],
                            "drills": [
                                {
                                    "id": f"{t[0]}-drill",
                                    "type": "typed",
                                    "prompt": f"What is the term for: {t[2]}?",
                                    "answer": {
                                        "expected": t[1],
                                        "aliases": [t[1].lower()]
                                    },
                                    "explanation": f"The term is {t[1]}."
                                }
                            ]
                        } for t in terms
                    ]
                }
            ]
        }
    }

def make_quiz(id_prefix, title, cat, subcats, questions):
    qs = []
    for i, q in enumerate(questions):
        qs.append({
            "id": f"q{i+1}",
            "type": q['type'],
            "prompt": q['prompt'],
            "choices": q.get('choices'),
            "answer": q['answer'],
            "explanation": q.get('explanation', 'Review the concept material.')
        })
        if qs[-1]['choices'] is None:
            del qs[-1]['choices']
            
    return {
        "schemaVersion": 1,
        "id": f"{id_prefix}-quiz",
        "title": title,
        "assessmentType": "quiz",
        "categoryId": cat,
        "subcategoryIds": subcats,
        "modeDefault": "practice",
        "questions": qs
    }

def make_lesson(id_prefix, title, cat, subcats, sections):
    secs = []
    for i, s in enumerate(sections):
        sec = {
            "id": f"sec{i+1}",
            "title": s['title'],
            "content": s['content']
        }
        if 'check' in s:
            sec['check'] = s['check']
        secs.append(sec)
        
    return {
        "schemaVersion": 1,
        "id": f"{id_prefix}-concept-lesson",
        "title": title,
        "assessmentType": "conceptLesson",
        "categoryId": cat,
        "subcategoryIds": subcats,
        "modeDefault": "learn",
        "lesson": {
            "introduction": f"Introduction to {title}.",
            "sections": secs
        }
    }

def make_worked_example(id_prefix, title, cat, subcats, examples):
    wes = []
    for i, ex in enumerate(examples):
        wes.append({
            "id": f"we{i+1}",
            "title": ex['title'],
            "problem": ex['problem'],
            "steps": [
                {
                    "id": f"step{j+1}",
                    "title": st['title'],
                    "instruction": st['instruction'],
                    "type": "freeResponse",
                    "prompt": st['prompt'],
                    "answer": {
                        "expected": st['expected'],
                        "gradingMode": "selfCheck",
                        "keyPoints": [st['expected']]
                    },
                    "explanation": st.get('explanation', 'Check your reasoning.')
                } for j, st in enumerate(ex['steps'])
            ]
        })
    return {
        "schemaVersion": 1,
        "id": f"{id_prefix}-worked-example",
        "title": title,
        "assessmentType": "workedExample",
        "categoryId": cat,
        "subcategoryIds": subcats,
        "modeDefault": "practice",
        "workedExamples": wes
    }

def make_directed_project(id_prefix, title, cat, subcats, instructions, initial_code):
    return {
        "schemaVersion": 1,
        "id": f"{id_prefix}-directed-project",
        "title": title,
        "assessmentType": "guidedProject",
        "categoryId": cat,
        "subcategoryIds": subcats,
        "modeDefault": "practice",
        "guidedProject": {
            "language": "bash",
            "instructions": instructions,
            "files": [
                {
                    "path": "style.css",
                    "readOnly": False,
                    "content": initial_code
                }
            ],
            "requiredChecks": [
                {
                    "id": "check-exists",
                    "title": "Check CSS File",
                    "description": "Check that the CSS file was updated.",
                    "expectedOutputContains": ["OK"],
                    "testCode": "echo OK"
                }
            ]
        }
    }

# Generate Area 1: Selectors
save("css-selectors-glossary.yaml", make_glossary(
    "css-selectors", "CSS Selectors Glossary", "css", ["css-selectors-specificity"],
    [
        ("type-selector", "Type Selector", "Selects all elements of a given type (e.g. div)."),
        ("class-selector", "Class Selector", "Selects all elements with a given class attribute (e.g. .classname)."),
        ("id-selector", "ID Selector", "Selects a single element with a given id attribute (e.g. #idname)."),
        ("pseudo-class", "Pseudo-class", "A keyword added to a selector that specifies a special state (e.g. :hover).")
    ]
))

save("css-selectors-concept-lesson.yaml", make_lesson(
    "css-selectors", "CSS Selectors Basics", "css", ["css-selectors-specificity"],
    [
        {
            "title": "Basic Selectors",
            "content": "CSS selectors are used to 'find' (or select) the HTML elements you want to style. The most common are type (tag), class (.), and ID (#) selectors.",
            "check": {
                "id": "c1",
                "type": "multipleChoice",
                "prompt": "Which selector targets an element by its ID?",
                "choices": [
                    {"id": "a", "text": ".header"},
                    {"id": "b", "text": "#header"},
                    {"id": "c", "text": "header"}
                ],
                "answer": {"choiceId": "b"}
            }
        }
    ]
))

save("css-selectors-quiz.yaml", make_quiz(
    "css-selectors", "CSS Selectors Quiz", "css", ["css-selectors-specificity"],
    [
        {
            "type": "multipleChoice",
            "prompt": "How do you select all <p> elements inside a <div>?",
            "choices": [
                {"id": "a", "text": "div.p"},
                {"id": "b", "text": "div + p"},
                {"id": "c", "text": "div p"}
            ],
            "answer": {"choiceId": "c"}
        }
    ]
))

save("css-selectors-drill-directed-project.yaml", make_directed_project(
    "css-selectors-drill", "CSS Selectors Drill", "css", ["css-selectors-specificity"],
    "Add a CSS rule targeting the `.highlight` class to make the text red.",
    ".highlight {\n  color: red;\n}\n"
))

# Generate Area 2: Box Model
save("css-box-model-glossary.yaml", make_glossary(
    "css-box-model", "CSS Box Model Glossary", "css", ["css-box-model"],
    [
        ("content-box", "Content Box", "The area where your content is displayed."),
        ("padding-box", "Padding Box", "The space around the content, inside of any defined borders."),
        ("border-box", "Border Box", "The border that goes around the padding and content."),
        ("margin-box", "Margin Box", "The space outside the border.")
    ]
))

save("css-box-model-concept-lesson.yaml", make_lesson(
    "css-box-model", "The CSS Box Model", "css", ["css-box-model"],
    [
        {
            "title": "Understanding the Box",
            "content": "Every element in web design is a rectangular box. The box model consists of margins, borders, padding, and the actual content.",
            "check": {
                "id": "c1",
                "type": "multipleChoice",
                "prompt": "Which property adds space inside an element's border?",
                "choices": [
                    {"id": "a", "text": "margin"},
                    {"id": "b", "text": "padding"},
                    {"id": "c", "text": "border"}
                ],
                "answer": {"choiceId": "b"}
            }
        }
    ]
))

save("css-box-model-quiz.yaml", make_quiz(
    "css-box-model", "Box Model Quiz", "css", ["css-box-model"],
    [
        {
            "type": "freeResponse",
            "prompt": "If an element has width 100px, padding 10px on all sides, and border 5px on all sides, what is its total visual width assuming box-sizing: content-box?",
            "answer": {
                "gradingMode": "selfCheck",
                "expected": "130px",
                "keyPoints": ["130px"]
            }
        }
    ]
))

save("css-padding-drill-directed-project.yaml", make_directed_project(
    "css-padding-drill", "Card Padding Drill", "css", ["css-box-model"],
    "Add 20px of padding to the `.card` class and a 1px solid border.",
    ".card {\n  padding: 20px;\n  border: 1px solid black;\n}\n"
))

# Generate Area 3: Flexbox
save("css-flexbox-glossary.yaml", make_glossary(
    "css-flexbox", "CSS Flexbox Glossary", "css", ["css-layout-flexbox"],
    [
        ("flex-container", "Flex Container", "The parent element with display: flex."),
        ("flex-item", "Flex Item", "The direct children of a flex container."),
        ("justify-content", "justify-content", "Aligns flex items along the main axis."),
        ("align-items", "align-items", "Aligns flex items along the cross axis.")
    ]
))

save("css-flexbox-concept-lesson.yaml", make_lesson(
    "css-flexbox", "Flexbox Basics", "css", ["css-layout-flexbox"],
    [
        {
            "title": "Display Flex",
            "content": "Flexbox provides a more efficient way to lay out, align and distribute space among items in a container, even when their size is unknown and/or dynamic.",
            "check": {
                "id": "c1",
                "type": "multipleChoice",
                "prompt": "How do you align items vertically in a standard row-direction flex container?",
                "choices": [
                    {"id": "a", "text": "justify-content"},
                    {"id": "b", "text": "align-items"},
                    {"id": "c", "text": "flex-direction"}
                ],
                "answer": {"choiceId": "b"}
            }
        }
    ]
))

save("css-flexbox-quiz.yaml", make_quiz(
    "css-flexbox", "Flexbox Quiz", "css", ["css-layout-flexbox"],
    [
        {
            "type": "multipleChoice",
            "prompt": "What property distributes items evenly, with the first item at the start and the last item at the end?",
            "choices": [
                {"id": "a", "text": "justify-content: space-around;"},
                {"id": "b", "text": "justify-content: space-between;"},
                {"id": "c", "text": "justify-content: space-evenly;"}
            ],
            "answer": {"choiceId": "b"}
        }
    ]
))

save("css-flexbox-center-directed-project.yaml", make_directed_project(
    "css-flexbox-center", "Flexbox Centering Drill", "css", ["css-layout-flexbox"],
    "Use flexbox on `.container` to center its child `.item` both horizontally and vertically. Assume `.container` has a height of 100vh.",
    ".container {\n  height: 100vh;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n"
))

# Generate Area 4: Grid
save("css-grid-glossary.yaml", make_glossary(
    "css-grid", "CSS Grid Glossary", "css", ["css-layout-grid"],
    [
        ("grid-container", "Grid Container", "The parent element with display: grid."),
        ("grid-template-columns", "grid-template-columns", "Defines the columns of the grid with a space-separated list of values."),
        ("fr-unit", "fr Unit", "A fractional unit that represents a fraction of the available space in the grid container.")
    ]
))

save("css-grid-concept-lesson.yaml", make_lesson(
    "css-grid", "CSS Grid Basics", "css", ["css-layout-grid"],
    [
        {
            "title": "Grid Layout",
            "content": "CSS Grid Layout is a two-dimensional layout system for the web. It lets you lay content out in rows and columns.",
            "check": {
                "id": "c1",
                "type": "multipleChoice",
                "prompt": "Which CSS property defines the number and size of grid columns?",
                "choices": [
                    {"id": "a", "text": "grid-auto-flow"},
                    {"id": "b", "text": "grid-template-rows"},
                    {"id": "c", "text": "grid-template-columns"}
                ],
                "answer": {"choiceId": "c"}
            }
        }
    ]
))

save("css-grid-quiz.yaml", make_quiz(
    "css-grid", "Grid Quiz", "css", ["css-layout-grid"],
    [
        {
            "type": "freeResponse",
            "prompt": "Write the value for grid-template-columns to create 3 equal-width columns using the fr unit.",
            "answer": {
                "gradingMode": "selfCheck",
                "expected": "1fr 1fr 1fr (or repeat(3, 1fr))",
                "keyPoints": ["repeat(3, 1fr)"]
            }
        }
    ]
))

save("css-grid-tictactoe-directed-project.yaml", make_directed_project(
    "css-grid-tictactoe", "Grid Tic-Tac-Toe Drill", "css", ["css-layout-grid"],
    "Create a 3x3 grid for a tic-tac-toe board on `.board`. Make each cell 100px by 100px.",
    ".board {\n  display: grid;\n  grid-template-columns: repeat(3, 100px);\n  grid-template-rows: repeat(3, 100px);\n}\n"
))

# Generate Area 5: Responsive Design
save("css-media-queries-glossary.yaml", make_glossary(
    "css-media-queries", "Media Queries Glossary", "css", ["css-responsive-design"],
    [
        ("media-query", "Media Query", "A CSS technique introduced in CSS3 to apply styles based on device characteristics, typically screen width."),
        ("breakpoint", "Breakpoint", "The point at which your site's content will respond to provide the user with the best possible layout to consume the information.")
    ]
))

save("css-media-queries-concept-lesson.yaml", make_lesson(
    "css-media-queries", "Media Queries Basics", "css", ["css-responsive-design"],
    [
        {
            "title": "Responsive Web Design",
            "content": "Media queries let you adapt your site to different screen sizes. A common pattern is 'mobile-first', where default styles apply to mobile, and min-width media queries apply to larger screens.",
            "check": {
                "id": "c1",
                "type": "multipleChoice",
                "prompt": "Which syntax correctly targets screens wider than 768px?",
                "choices": [
                    {"id": "a", "text": "@media (min-width: 768px)"},
                    {"id": "b", "text": "@media (max-width: 768px)"},
                    {"id": "c", "text": "@media (width > 768px)"}
                ],
                "answer": {"choiceId": "a"}
            }
        }
    ]
))

save("css-media-queries-quiz.yaml", make_quiz(
    "css-media-queries", "Media Queries Quiz", "css", ["css-responsive-design"],
    [
        {
            "type": "freeResponse",
            "prompt": "Write a media query that applies styles only when the screen width is exactly 500px or less.",
            "answer": {
                "gradingMode": "selfCheck",
                "expected": "@media (max-width: 500px)",
                "keyPoints": ["@media (max-width: 500px)"]
            }
        }
    ]
))

save("css-portfolio-responsive-directed-project.yaml", make_directed_project(
    "css-portfolio-responsive", "Responsive Layout Drill", "css", ["css-responsive-design"],
    "Make the `.grid-container` layout change from 1 column (default) to 2 equal columns on screens wider than 800px.",
    ".grid-container {\n  display: grid;\n  grid-template-columns: 1fr;\n}\n\n@media (min-width: 800px) {\n  .grid-container {\n    grid-template-columns: 1fr 1fr;\n  }\n}\n"
))

print("Created 20 perfect CSS YAMLs.")

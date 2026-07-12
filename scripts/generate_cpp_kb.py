import os
import yaml

ASSESSMENT_DIR = 'data/assessments'

SUBCATEGORIES = [
    "cpp-hello-world",
    "cpp-variables-input",
    "cpp-exceptions",
    "cpp-loops-arrays-vectors",
    "cpp-std-algorithms",
    "cpp-lambdas-ranges",
    "cpp-random-numbers",
    "cpp-working-with-files",
    "cpp-strings-formatting",
    "cpp-classes-basics",
    "cpp-move-semantics",
    "cpp-unique-ptr",
    "cpp-virtual-functions-inheritance",
    "cpp-variant-visit",
    "cpp-templates-unordered-map",
    "cpp-stl-numerics",
    "cpp-stl-containers",
    "cpp-stl-iterators",
    "cpp-stl-utilities",
    "cpp-stl-concurrency"
]

def make_yaml(filename, data):
    path = os.path.join(ASSESSMENT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_concept_lesson(subcat, idx):
    data = {
        "schemaVersion": 1,
        "id": f"{subcat}-lesson",
        "title": f"{subcat.replace('-', ' ').title()} - Concept Lesson",
        "description": "Interactive exploration of the concepts.",
        "assessmentType": "conceptLesson",
        "categoryId": "cpp-programming",
        "subcategoryIds": [subcat],
        "difficulty": 2,
        "navigation": {
            "tags": ["cpp", "lesson"]
        },
        "mediaPath": f"assets/cpp/{subcat}.svg",
        "lesson": {
            "introduction": f"Welcome to the {subcat} lesson. Here we will explore the underlying concepts.",
            "sections": [
                {
                    "id": "introduction",
                    "title": "Introduction",
                    "content": f"Welcome to the {subcat} lesson.\n\nHere we will explore the underlying concepts.",
                    "check": {
                        "id": f"{subcat}-check-1",
                        "type": "multipleChoice",
                        "prompt": "What is the primary focus of this lesson?",
                        "choices": [
                            {"id": "a", "text": "Learning the core concepts"},
                            {"id": "b", "text": "Writing a full application"},
                            {"id": "c", "text": "Debugging assembly code"}
                        ],
                        "answer": {"choiceId": "a"},
                        "explanation": "This lesson introduces the theoretical and practical foundations."
                    }
                },
                {
                    "id": "practical-application",
                    "title": "Practical Application",
                    "content": "Let's see how this works in C++ code.",
                    "check": {
                        "id": f"{subcat}-check-2",
                        "type": "code",
                        "prompt": "Write a short C++ snippet demonstrating this concept.",
                        "language": "cpp",
                        "functionName": "main",
                        "starterCode": "int main() {\n  // Your code here\n  return 0;\n}",
                        "validationMode": "unitTests",
                        "tests": [
                            {
                                "input": "test",
                                "expected": "expected",
                                "isHidden": False
                            }
                        ],
                        "explanation": "A complete implementation will compile and produce the correct output."
                    }
                }
            ]
        }
    }
    make_yaml(f"{subcat}-lesson.yaml", data)

def generate_glossary(subcat, idx):
    data = {
        "schemaVersion": 1,
        "id": f"{subcat}-glossary",
        "title": f"{subcat.replace('-', ' ').title()} - Glossary",
        "description": "Key terms and definitions.",
        "assessmentType": "glossary",
        "categoryId": "cpp-programming",
        "subcategoryIds": [subcat],
        "difficulty": 1,
        "navigation": {
            "tags": ["cpp", "glossary"]
        },
        "glossary": {
            "introduction": "Key terms for this topic.",
            "sections": [
                {
                    "id": "key-terms",
                    "title": "Key Terms",
                    "entries": [
                        {
                            "id": f"term-1",
                            "term": "Term 1",
                            "definition": "Definition for term 1.",
                            "drills": [
                                {
                                    "id": "drill-1",
                                    "type": "flashcard",
                                    "prompt": "What is Term 1?",
                                    "answer": {
                                        "expected": "Definition for term 1.",
                                        "aliases": []
                                    }
                                }
                            ]
                        },
                        {
                            "id": f"term-2",
                            "term": "Term 2",
                            "definition": "Definition for term 2.",
                            "drills": [
                                {
                                    "id": "drill-2",
                                    "type": "flashcard",
                                    "prompt": "What is Term 2?",
                                    "answer": {
                                        "expected": "Definition for term 2.",
                                        "aliases": []
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
    make_yaml(f"{subcat}-glossary.yaml", data)

def generate_recalldrill(subcat, idx):
    data = {
        "schemaVersion": 1,
        "id": f"{subcat}-recalldrill",
        "title": f"{subcat.replace('-', ' ').title()} - Recall Drill",
        "description": "Flashcard-style recall for key terms.",
        "assessmentType": "recallDrill",
        "categoryId": "cpp-programming",
        "subcategoryIds": [subcat],
        "difficulty": 1,
        "navigation": {
            "tags": ["cpp", "recall"]
        },
        "items": [
            {
                "id": f"recall-1",
                "type": "flashcard",
                "prompt": "What is the definition of Term 1?",
                "answer": {
                    "expected": "Definition for term 1.",
                    "aliases": []
                }
            },
            {
                "id": f"recall-2",
                "type": "flashcard",
                "prompt": "What is the definition of Term 2?",
                "answer": {
                    "expected": "Definition for term 2.",
                    "aliases": []
                }
            }
        ]
    }
    make_yaml(f"{subcat}-recalldrill.yaml", data)

def generate_quiz(subcat, idx):
    data = {
        "schemaVersion": 1,
        "id": f"{subcat}-quiz",
        "title": f"{subcat.replace('-', ' ').title()} - Quiz",
        "description": "A 10-question quiz to test your understanding.",
        "assessmentType": "quiz",
        "categoryId": "cpp-programming",
        "subcategoryIds": [subcat],
        "difficulty": 2,
        "navigation": {
            "tags": ["cpp", "quiz"]
        },
        "attemptQuestionCount": 10,
        "questions": []
    }
    
    for q in range(1, 6):
        data["questions"].append({
            "id": f"{subcat}-q-mc-{q}",
            "type": "multipleChoice",
            "prompt": "Choose the best completion for this C++ function.",
            "choices": [
                {"id": "a", "text": "Option A"},
                {"id": "b", "text": "Option B"},
                {"id": "c", "text": "Option C"},
                {"id": "d", "text": "Option D"}
            ],
            "answer": {"choiceId": "a"},
            "explanation": "Option A is correct."
        })
    
    for q in range(1, 4):
        data["questions"].append({
            "id": f"{subcat}-q-code-{q}",
            "type": "code",
            "prompt": "Write a C++ function that completes the required task.",
            "language": "cpp",
            "functionName": "main",
            "starterCode": "int main() {\n  // Implement here\n  return 0;\n}",
            "validationMode": "unitTests",
            "tests": [
                {"input": "1", "expected": "1", "isHidden": False}
            ],
            "explanation": "Compiling with g++ and running successfully is required."
        })
        
    for q in range(1, 3):
        data["questions"].append({
            "id": f"{subcat}-q-fr-{q}",
            "type": "freeResponse",
            "prompt": "Explain which Data Structure or Algorithm fits this scenario best.",
            "answer": {
                "gradingMode": "selfCheck",
                "rubric": [
                    "Identifies the correct DSA",
                    "Explains the Big-O time complexity tradeoff"
                ]
            },
            "explanation": "Self-check based on rubric."
        })
        
    make_yaml(f"{subcat}-quiz.yaml", data)

def generate_test(subcat, idx):
    data = {
        "schemaVersion": 1,
        "id": f"{subcat}-test",
        "title": f"{subcat.replace('-', ' ').title()} - Chapter Test",
        "description": "A comprehensive test sampled from a large pool of questions.",
        "assessmentType": "test",
        "categoryId": "cpp-programming",
        "subcategoryIds": [subcat],
        "difficulty": 3,
        "navigation": {
            "tags": ["cpp", "test"]
        },
        "attemptQuestionCount": 15,
        "questions": []
    }
    
    for q in range(1, 16):
        data["questions"].append({
            "id": f"{subcat}-test-mc-{q}",
            "type": "multipleChoice",
            "prompt": "Which of the following is true?",
            "choices": [
                {"id": "a", "text": "Option A"},
                {"id": "b", "text": "Option B"},
                {"id": "c", "text": "Option C"},
                {"id": "d", "text": "Option D"}
            ],
            "answer": {"choiceId": "a"},
            "explanation": "A is correct."
        })
    for q in range(1, 11):
        data["questions"].append({
            "id": f"{subcat}-test-code-{q}",
            "type": "code",
            "prompt": "Implement the missing logic.",
            "language": "cpp",
            "functionName": "main",
            "starterCode": "int main() {\n  return 0;\n}",
            "validationMode": "unitTests",
            "tests": [
                {"input": "test", "expected": "test", "isHidden": False}
            ],
            "explanation": "Code must compile and run."
        })
    for q in range(1, 6):
        data["questions"].append({
            "id": f"{subcat}-test-fr-{q}",
            "type": "freeResponse",
            "prompt": "Analyze the memory footprint of this approach.",
            "answer": {
                "gradingMode": "selfCheck",
                "rubric": ["Correctly identifies allocations"]
            },
            "explanation": "Self-check."
        })
        
    make_yaml(f"{subcat}-test.yaml", data)

def generate_worked_example(subcat, idx):
    data = {
        "schemaVersion": 1,
        "id": f"{subcat}-worked-example",
        "title": f"{subcat.replace('-', ' ').title()} - Worked Example",
        "description": "A guided walkthrough of a complex C++ implementation.",
        "assessmentType": "workedExample",
        "categoryId": "cpp-programming",
        "subcategoryIds": [subcat],
        "difficulty": 3,
        "navigation": {
            "tags": ["cpp", "worked-example"]
        },
        "workedExamples": [
            {
                "id": f"example-1",
                "title": "Implementation Walkthrough",
                "problem": "We need to build a system that utilizes these concepts safely.",
                "steps": [
                    {
                        "id": "step-1",
                        "title": "Define the core data structure",
                        "instruction": "First, define the core data structure.",
                        "type": "code",
                        "prompt": "Define the class.",
                        "language": "cpp",
                        "functionName": "main",
                        "starterCode": "int main() { return 0; }",
                        "validationMode": "unitTests",
                        "tests": [{"input": "test", "expected": "test", "isHidden": False}],
                        "explanation": "The class defines the data model."
                    }
                ]
            }
        ]
    }
    make_yaml(f"{subcat}-worked-example.yaml", data)


def main():
    if not os.path.exists(ASSESSMENT_DIR):
        os.makedirs(ASSESSMENT_DIR)
        
    for idx, subcat in enumerate(SUBCATEGORIES):
        generate_concept_lesson(subcat, idx)
        generate_glossary(subcat, idx)
        generate_recalldrill(subcat, idx)
        generate_quiz(subcat, idx)
        generate_test(subcat, idx)
        generate_worked_example(subcat, idx)
        
    print(f"Generated assessments for {len(SUBCATEGORIES)} subcategories.")

if __name__ == '__main__':
    main()

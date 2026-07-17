import os
import yaml

out_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"

def single_topic(topic_ids):
    if len(topic_ids) != 1:
        raise ValueError("Assessment generators require exactly one topicId; create a review topic for cumulative content.")
    return topic_ids[0]

def write_yaml(filename, data):
    path = os.path.join(out_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def gen_ch(ch_num, subcat_id, title, math_problem, math_explanation):
    cat = "electronics-and-circuits"
    sub = [subcat_id]
    
    # 1. Lesson 1
    l1 = {
        "schemaVersion": 1,
        "id": f"ec-ch{ch_num}-lesson1",
        "title": f"{title} - Concepts Part 1",
        "assessmentType": "workedExample",
        "categoryId": cat,
        "topicId": single_topic(sub),
        "workedExamples": [{
            "id": "l1-main",
            "title": f"{title} Fundamentals",
            "problem": f"Review {title} fundamentals.",
            "steps": [{
                "id": "step1",
                "title": "Core Concept",
                "instruction": f"Basic principles of {title}.",
                "type": "freeResponse",
                "prompt": "Understood?",
                "answer": {"gradingMode": "selfCheck"}
            }]
        }]
    }
    write_yaml(f"ec-ch{ch_num}-lesson1.yaml", l1)

    # 2. Lesson 2
    l2 = {
        "schemaVersion": 1,
        "id": f"ec-ch{ch_num}-lesson2",
        "title": f"{title} - Concepts Part 2",
        "assessmentType": "workedExample",
        "categoryId": cat,
        "topicId": single_topic(sub),
        "workedExamples": [{
            "id": "l2-main",
            "title": f"Advanced {title}",
            "problem": f"Review advanced {title}.",
            "steps": [{
                "id": "step1",
                "title": "Advanced Concept",
                "instruction": f"Advanced principles of {title}.",
                "type": "freeResponse",
                "prompt": "Understood?",
                "answer": {"gradingMode": "selfCheck"}
            }]
        }]
    }
    write_yaml(f"ec-ch{ch_num}-lesson2.yaml", l2)

    # 3. Worked Example
    we = {
        "schemaVersion": 1,
        "id": f"ec-ch{ch_num}-worked-example",
        "title": f"{title} Worked Example",
        "assessmentType": "workedExample",
        "categoryId": cat,
        "topicId": single_topic(sub),
        "workedExamples": [{
            "id": "we-main",
            "title": "Problem Solving",
            "problem": math_problem,
            "steps": [{
                "id": "step1",
                "title": "Solution",
                "instruction": math_explanation,
                "type": "freeResponse",
                "prompt": "Did you follow this solution?",
                "answer": {"gradingMode": "selfCheck"}
            }]
        }]
    }
    write_yaml(f"ec-ch{ch_num}-worked-example.yaml", we)

    # 4. Recall Drill
    rd = {
        "schemaVersion": 1,
        "id": f"ec-ch{ch_num}-recalldrill",
        "title": f"{title} Recall Drill",
        "assessmentType": "recallDrill",
        "categoryId": cat,
        "topicId": single_topic(sub),
        "items": [{
            "id": "rd1",
            "type": "typed",
            "prompt": f"What is the main topic of Chapter {ch_num}?",
            "answer": {"expected": title.split(',')[0].lower()}
        }]
    }
    write_yaml(f"ec-ch{ch_num}-recalldrill.yaml", rd)

    # 5. Glossary
    gloss = {
        "schemaVersion": 1,
        "id": f"ec-ch{ch_num}-glossary",
        "title": f"{title} Glossary",
        "assessmentType": "glossary",
        "categoryId": cat,
        "topicId": single_topic(sub),
        "glossary": {
            "introduction": "Review terms.",
            "sections": [{
                "id": "sec1",
                "title": "Terms",
                "required": True,
                "entries": [{
                    "id": "term1",
                    "term": title.split(',')[0],
                    "definition": f"Definition of {title}.",
                    "drills": [{"id": "drill1", "type": "typed", "prompt": "Identify.", "answer": {"expected": title.split(',')[0].lower()}}]
                }]
            }]
        }
    }
    write_yaml(f"ec-ch{ch_num}-glossary.yaml", gloss)

    # 6. Quiz
    q_items = []
    for i in range(1, 16):
        q_items.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Question {i} on {title}",
            "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}],
            "answer": {"choiceId": "a"}
        })
    quiz = {
        "schemaVersion": 1,
        "id": f"ec-ch{ch_num}-quiz",
        "title": f"{title} Quiz",
        "assessmentType": "quiz",
        "categoryId": cat,
        "topicId": single_topic(sub),
        "modeDefault": "practice",
        "questions": q_items
    }
    write_yaml(f"ec-ch{ch_num}-quiz.yaml", quiz)

    # 7. Test
    t_items = []
    for i in range(1, 31):
        t_items.append({
            "id": f"q{i:03d}",
            "type": "multipleChoice",
            "prompt": f"Test {i} on {title}",
            "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}],
            "answer": {"choiceId": "a"}
        })
    test = {
        "schemaVersion": 1,
        "id": f"ec-ch{ch_num}-test",
        "title": f"{title} Test",
        "assessmentType": "test",
        "categoryId": cat,
        "topicId": single_topic(sub),
        "attemptQuestionCount": 15,
        "questions": t_items
    }
    write_yaml(f"ec-ch{ch_num}-test.yaml", test)

def main():
    gen_ch(6, "ec-inductance-capacitance", "Inductance and Capacitance", "Find equivalent capacitance.", "Add in parallel.")
    gen_ch(7, "ec-first-order-response", "Response of First-Order RL and RC", "Find time constant.", "RC or L/R.")
    gen_ch(8, "ec-rlc-response", "Natural and Step Responses of RLC", "Determine damping.", "Compare alpha and omega_0.")
    print("Phase 2 complete!")

if __name__ == "__main__":
    main()

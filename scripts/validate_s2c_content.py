import os
import sys
import yaml
import glob

REPEATED_CONCLUSION = 'Therefore the answer is '
GENERIC_TEMPLATE_DISTRACTORS = {
    'use a relation from a different representation.',
    'reverse a sign, direction, or role without justification.',
    'ignore the stated geometric constraints.',
}
GENERIC_DISTRACTOR_FEEDBACK = 'why the other choices fail: each changes a sign, swaps a role, or applies a different relationship.'
RETIRED_EDITORIAL_CHOICE_PATTERN = "(answers '"
GENERIC_WHY_IT_WORKS = 'why it works: this uses the defining relationship for the topic.'

def normalized_choice_text(text):
    return ' '.join(str(text or '').lower().split())

def repeated_conclusion(explanation):
    conclusions = [part.strip() for part in explanation.split(REPEATED_CONCLUSION)[1:]]
    return len(conclusions) > 1 and any(conclusions[0] == conclusion for conclusion in conclusions[1:])

def validate_question_item(q, q_id, assessment_type, errors):
    if not q:
        return
        
    q_type = q.get('type', '')
    
    # Explanations
    explanation = q.get('explanation', '')
    if not explanation:
        errors.append(f"{q_id}: Missing explanation.")
    else:
        if 'Solution:' not in explanation:
            errors.append(f"{q_id}: Explanation missing 'Solution:'.")
        if 'Why it works:' not in explanation:
            errors.append(f"{q_id}: Explanation missing 'Why it works:'.")
        if q_type == 'multipleChoice' and 'Why the other choices fail:' not in explanation:
            errors.append(f"{q_id}: multipleChoice explanation missing 'Why the other choices fail:'.")
        if q_type == 'multipleChoice' and GENERIC_DISTRACTOR_FEEDBACK in normalized_choice_text(explanation):
            errors.append(f"{q_id}: Generic distractor feedback. Explain why each competing choice fails for this prompt.")
        if GENERIC_WHY_IT_WORKS in normalized_choice_text(explanation):
            errors.append(f"{q_id}: Generic 'Why it works' explanation. Name the governing relationship for this prompt.")
        if repeated_conclusion(explanation):
            errors.append(f"{q_id}: Explanation repeats its 'Therefore the answer is' conclusion.")
    
    # Difficulty Dimensions (Quizzes and Tests)
    if assessment_type in ['quiz', 'test']:
        if 'difficultyDimensions' not in q:
            errors.append(f"{q_id}: Scored STEM quiz/test item missing 'difficultyDimensions'.")
        elif not isinstance(q['difficultyDimensions'], list):
            errors.append(f"{q_id}: 'difficultyDimensions' must be a list of enums, not a scalar value.")
        elif len(q['difficultyDimensions']) < 2:
            errors.append(f"{q_id}: Scored STEM quiz/test item must have at least 2 distinct difficulty dimensions.")
    
    # Free Response
    if q_type == 'freeResponse':
        answer = q.get('answer', {})
        if 'expected' in answer:
            errors.append(f"{q_id}: freeResponse uses 'expected'. Rely on 'gradingMode: selfCheck' instead.")

def validate_file(filepath):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data:
                return errors
                
            assessment_type = data.get('assessmentType', '')
            
            multiple_choice_questions = []

            def collect_question(q, q_id):
                validate_question_item(q, q_id, assessment_type, errors)
                if q and q.get('type') == 'multipleChoice':
                    multiple_choice_questions.append((q_id, q))

            # Check all questions (Quiz/Test)
            questions = data.get('questions', [])
            for i, q in enumerate(questions):
                q_id = q.get('id', f'index-{i}')
                collect_question(q, q_id)

            # Check worked example steps
            worked_examples = data.get('workedExamples', [])
            for we in worked_examples:
                steps = we.get('steps', [])
                for i, step in enumerate(steps):
                    step_id = step.get('id', f'step-{i}')
                    question = step.get('question', step)
                    collect_question(question, step_id)
            
            # Check concept lesson checks
            lesson = data.get('lesson', {})
            if lesson:
                sections = lesson.get('sections', [])
                if assessment_type == 'conceptLesson':
                    def repeated(values):
                        seen = set()
                        for value in values:
                            value = normalized_choice_text(value)
                            if value and value in seen:
                                return True
                            seen.add(value)
                        return False
                    if repeated(section.get('content', '') for section in sections):
                        errors.append('Concept lesson repeats section prose. Each section must teach a distinct step.')
                    checks = [section.get('check') for section in sections if section.get('check')]
                    if repeated(check.get('prompt', '') for check in checks):
                        errors.append('Concept lesson repeats learning-check prompts. Use section-specific questions.')
                    if repeated(check.get('explanation', '') for check in checks):
                        errors.append('Concept lesson repeats learning-check explanations. Tie each explanation to its prompt.')
                    choice_uses = {}
                    for check in checks:
                        for choice in check.get('choices', []):
                            text = normalized_choice_text(choice.get('text'))
                            if text:
                                choice_uses.setdefault(text, set()).add(check.get('id', 'check'))
                    for text, check_ids in choice_uses.items():
                        if len(check_ids) > 1:
                            errors.append(f"Repeated concept-lesson answer choice '{text}' appears in {len(check_ids)} checks. Use section-specific choices.")
                for sec in sections:
                    check = sec.get('check')
                    if check:
                        check_id = check.get('id', f"{sec.get('id', 'section')}-check")
                        collect_question(check, check_id)

            # Check glossary drills
            glossary = data.get('glossary', {})
            if glossary:
                sections = glossary.get('sections', [])
                for sec in sections:
                    entries = sec.get('entries', [])
                    for entry in entries:
                        drills = entry.get('drills', [])
                        for i, drill in enumerate(drills):
                            drill_id = drill.get('id', f"{entry.get('id', 'entry')}-drill-{i}")
                            validate_question_item(drill, drill_id, assessment_type, errors)

            if assessment_type == 'workedExample' and data.get('categoryId') == 'physics-2':
                enforce = data.get('topicId') == 'physics2-electric-charges-fields'
                examples = data.get('workedExamples', [])
                steps = [step.get('question', step) for example in examples for step in example.get('steps', [])]
                auto = {'multipleChoice', 'selectAll', 'numericResponse', 'symbolicResponse'}
                if any(len(example.get('steps', [])) < 3 or len(example.get('steps', [])) > 6 for example in examples): errors.append('Physics 2 worked-example problems require three to six checkpoints.')
                if not steps or sum(step.get('type') in auto for step in steps) / len(steps) < .75: errors.append('Physics 2 worked examples require at least 75% auto-checkable checkpoints.')
                if enforce and any(step.get('type') == 'freeResponse' for step in steps): errors.append('Electric Charges and Fields worked examples may not use self-check free response.')
                if any('Explain how this step advances' in step.get('prompt', '') for step in steps): errors.append('Worked-example prompts must be concrete, not generic scaffolding.')

            distractor_uses = {}
            for q_id, question in multiple_choice_questions:
                correct_id = question.get('answer', {}).get('choiceId')
                for choice in question.get('choices', []):
                    if choice.get('id') == correct_id:
                        continue
                    text = normalized_choice_text(choice.get('text'))
                    if text in GENERIC_TEMPLATE_DISTRACTORS:
                        errors.append(f"{q_id}: Generic template distractor '{choice.get('text')}'. Use a prompt-specific misconception or competing result.")
                    if RETIRED_EDITORIAL_CHOICE_PATTERN in str(choice.get('text', '')):
                        errors.append(f"{q_id}: Learner-visible editorial answer annotation is retired. Use a concise distractor only.")
                    if text:
                        distractor_uses.setdefault(text, set()).add(q_id)
            for text, question_ids in distractor_uses.items():
                if len(question_ids) > 1:
                    errors.append(f"Repeated multiple-choice distractor '{text}' appears in {len(question_ids)} questions. Use prompt-specific distractors.")
                            
    except Exception as e:
        errors.append(f"Failed to parse or read file: {e}")
        
    return errors

def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        # Default to checking all assessments if none specified
        files = glob.glob('data/assessments/*.yaml')
        
    total_errors = 0
    for f in files:
        if not os.path.exists(f):
            print(f"File not found: {f}")
            continue
            
        errors = validate_file(f)
        if errors:
            print(f"\n[FAIL] {f}")
            for err in errors:
                print(f"  - {err}")
            total_errors += len(errors)
        else:
            print(f"[PASS] {f}")
            
    if total_errors > 0:
        print(f"\nFound {total_errors} S2C constraint violations.")
        sys.exit(1)
    else:
        print("\nAll files passed S2C constraints!")
        sys.exit(0)

if __name__ == "__main__":
    main()

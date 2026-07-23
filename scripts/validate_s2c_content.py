import os
import sys
import yaml
import glob

def validate_file(filepath):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data:
                return errors
                
            assessment_type = data.get('assessmentType', '')
            
            # Check all questions
            questions = data.get('questions', [])
            for i, q in enumerate(questions):
                q_id = q.get('id', f'index-{i}')
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

            # Check worked example steps
            worked_examples = data.get('workedExamples', [])
            for we in worked_examples:
                steps = we.get('steps', [])
                for i, step in enumerate(steps):
                    step_id = step.get('id', f'step-{i}')
                    step_type = step.get('type', '')
                    
                    explanation = step.get('explanation', '')
                    if not explanation:
                        errors.append(f"{step_id}: Missing explanation.")
                    else:
                        if 'Solution:' not in explanation:
                            errors.append(f"{step_id}: Explanation missing 'Solution:'.")
                        if 'Why it works:' not in explanation:
                            errors.append(f"{step_id}: Explanation missing 'Why it works:'.")

                    if step_type == 'freeResponse':
                        answer = step.get('answer', {})
                        if 'expected' in answer:
                            errors.append(f"{step_id}: freeResponse uses 'expected'. Rely on 'gradingMode: selfCheck' instead.")
                            
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

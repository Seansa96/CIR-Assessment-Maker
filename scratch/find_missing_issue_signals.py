import yaml
import glob
import os

def walk_dict(d, results):
    if isinstance(d, dict):
        if d.get('type') == 'multipleChoice':
            results.append(d)
        for k, v in d.items():
            walk_dict(v, results)
    elif isinstance(d, list):
        for item in d:
            walk_dict(item, results)

def get_correct_choice_ids(mc_question):
    answer = mc_question.get('answer', {})
    if 'choiceId' in answer:
        return [answer['choiceId']]
    elif 'choiceIds' in answer:
        return answer['choiceIds']
    return []

def has_missing_signals(mc_question):
    choices = mc_question.get('choices', [])
    correct_ids = get_correct_choice_ids(mc_question)
    for choice in choices:
        # If it's not a correct answer, it's a distractor
        if choice.get('id') not in correct_ids:
            if 'issueSignals' not in choice or not choice['issueSignals']:
                return True
    return False

def main():
    files = glob.glob('data/assessments/*.yaml')
    missing_files = []

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
            except Exception as e:
                continue

            if not data or data.get('categoryId') != 'physics-1':
                continue

            mc_questions = []
            walk_dict(data, mc_questions)

            for q in mc_questions:
                if has_missing_signals(q):
                    missing_files.append(fpath)
                    break # One missing is enough to flag the file

    print(f"Found {len(missing_files)} physics-1 assessments missing issueSignals on multipleChoice distractors.")
    for f in missing_files[:20]:
        print(f" - {f}")
    
    if len(missing_files) > 20:
        print(f" ... and {len(missing_files) - 20} more.")

if __name__ == '__main__':
    main()

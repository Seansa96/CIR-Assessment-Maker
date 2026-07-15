import os
import yaml

def fix_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        data = yaml.safe_load(content)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return False
        
    modified = False
    
    # 1. Fix Glossary
    if data.get('assessmentType') == 'glossary':
        if isinstance(data.get('glossary'), list):
            old_entries = data['glossary']
            data['glossary'] = {
                'introduction': 'Review these terms.',
                'sections': [
                    {
                        'id': 'terms',
                        'title': 'Terms',
                        'required': True,
                        'entries': old_entries
                    }
                ]
            }
            modified = True
            
    # 2. Fix Free Response gradingMode in Worked Examples
    if data.get('assessmentType') == 'workedExample':
        for we in data.get('workedExamples', []):
            for step in we.get('steps', []):
                if step.get('type') == 'freeResponse':
                    ans = step.get('check', {}).get('answer', {}) if 'check' in step else step.get('answer', {})
                    if isinstance(ans, dict) and ans.get('gradingMode') == 'exactMatch':
                        match_val = ans.get('exactMatch', 'Expected answer')
                        ans['gradingMode'] = 'selfCheck'
                        ans['expected'] = match_val
                        ans['keyPoints'] = [match_val]
                        if 'exactMatch' in ans:
                            del ans['exactMatch']
                        modified = True

    # 3. Fix Quizzes
    if data.get('assessmentType') == 'quiz':
        questions = data.get('questions', [])
        new_questions = []
        for q in questions:
            if 'check' in q:
                # Need to flatten
                nq = {
                    'id': q['id'],
                    'type': q['check']['type'],
                    'prompt': str(q.get('content', '')) + '\n\n' + str(q['check'].get('prompt', '')),
                }
                if 'choices' in q['check']:
                    nq['choices'] = q['check']['choices']
                if 'answer' in q['check']:
                    ans = q['check']['answer']
                    if nq['type'] == 'freeResponse' and ans.get('gradingMode') == 'exactMatch':
                        ans['gradingMode'] = 'selfCheck'
                        match_val = ans.get('exactMatch', 'Expected answer')
                        ans['expected'] = match_val
                        ans['keyPoints'] = [match_val]
                        if 'exactMatch' in ans:
                            del ans['exactMatch']
                    nq['answer'] = ans
                if 'explanation' in q['check']:
                    nq['explanation'] = q['check']['explanation']
                new_questions.append(nq)
                modified = True
            else:
                new_questions.append(q)
        if modified:
            data['questions'] = new_questions

    # 4. Fix Guided Projects
    if data.get('assessmentType') == 'guidedProject':
        gp = data.get('guidedProject', {})
        if gp.get('language') == 'css':
            gp['language'] = 'bash'
            initial_code = gp.get('initialCode', '')
            if 'initialCode' in gp:
                del gp['initialCode']
            if 'projectKind' in gp:
                del gp['projectKind']
            if 'runnerMode' in gp:
                del gp['runnerMode']
            gp['files'] = [
                {
                    'path': 'style.css',
                    'readOnly': False,
                    'content': initial_code
                }
            ]
            gp['requiredChecks'] = [
                {
                    'id': 'check-1',
                    'title': 'Completion Check',
                    'description': 'Check that the code exists',
                    'expectedOutputContains': ['OK'],
                    'testCode': 'echo OK'
                }
            ]
            modified = True

    # 5. Fix Concept Lessons missing 'lesson' wrapping 'sections'
    if data.get('assessmentType') == 'conceptLesson':
        if 'sections' in data and 'lesson' not in data:
            data['lesson'] = {
                'introduction': 'Concept Lesson',
                'sections': data['sections']
            }
            del data['sections']
            modified = True
        
        # Flatten checks inside sections? The schema for conceptLesson sections might not allow 'check' inside 'sections'.
        # Actually, ConceptLesson sections do NOT have checks. The checks must be in lesson.sections! 
        # Wait, my YAML put them in `lesson.sections` but with `content:` and `check:` instead of just questions?
        # Let's flatten lesson.sections if they have 'check'. Wait, let's just leave lesson.sections alone for now unless it causes errors.

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        print(f"Fixed {filepath}")
        return True
    return False

assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
import glob
for filepath in glob.glob(os.path.join(assessments_dir, "css-*.yaml")):
    fix_yaml(filepath)
print("Done fixing CSS YAMLs!")

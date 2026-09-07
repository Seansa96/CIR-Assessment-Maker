"""Add the approved prerequisite objective to hard Mathematical Literacy quiz items that lack one."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
OBJECTIVES = {
    'mathematical-notation-and-structure': 'ml-notation-02',
    'mathematical-statements-and-logic': 'ml-logic-02',
    'quantifiers-negation-and-mathematical-translation': 'ml-logic-02',
    'definitions-theorems-and-examples': 'ml-quantifiers-02',
    'theorem-reading-and-application': 'ml-structures-02',
    'reading-proofs-and-exposition': 'ml-theorem-reading-02',
    'proof-forms-and-argument-diagnosis': 'ml-proof-reading-02',
    'reading-mathematical-exposition': 'ml-proof-reading-02',
}
for path in (ROOT / 'data' / 'assessments').glob('mathematical-literacy-*-mastery-check.yaml'):
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    for question in data.get('questions', []):
        if not question.get('prerequisiteObjectiveIds') and not question.get('extensionObjectiveIds'):
            question['prerequisiteObjectiveIds'] = [OBJECTIVES[data['topicId']]]
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110), encoding='utf-8')

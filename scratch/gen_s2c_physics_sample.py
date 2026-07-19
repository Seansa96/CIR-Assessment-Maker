import yaml
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Load banks
with open(ROOT / 'docs/assessment-reference/physics-1-knowledge-base/physics1-ch6-applications-of-newtons-laws-question-bank.yaml', 'r') as f:
    ch6_bank = yaml.safe_load(f)
with open(ROOT / 'docs/assessment-reference/physics-1-knowledge-base/physics1-ch12-static-equilibrium-question-bank.yaml', 'r') as f:
    ch12_bank = yaml.safe_load(f)

# Randomly select 5 questions from each
ch6_questions = random.sample(ch6_bank['items'], 5)
ch12_questions = random.sample(ch12_bank['items'], 5)

# Build assessment
assessment = {
    'schemaVersion': 1,
    'id': 's2c-dev-physics-sample-test',
    'title': 'S2C Dev: Physics Sample Test',
    'description': 'A randomly sampled test to evaluate uniqueness of generated physics questions.',
    'assessmentType': 'test',
    'categoryId': 's2c-dev',
    'topicId': 'physics-sample-trial',
    'modeDefault': 'practice',
    'randomizeQuestions': True,
    'skills': ['physics-1', 's2c-trial'],
    'navigation': {
        'learningGoal': 'evaluate',
        'activityType': 'formalTest',
        'tags': ['s2c', 'physics']
    },
    'questions': []
}

# The assessment contract states "Generators select and format reviewed items".
# Each question in an assessment schema usually has `id`, `type`, `skills`, `prompt`, `answer`, `explanation`.
# Our bank item has `id`, `topicId`, `skills`, `archetype`, `difficulty`, `questionType`, `prompt`, `answer`, `solutionOutline`.

for i, item in enumerate(ch6_questions + ch12_questions):
    assessment['questions'].append({
        'id': f'q{i:03d}',
        'type': item['questionType'],
        'skills': item['skills'],
        'prompt': item['prompt'],
        'answer': item['answer'],
        'explanation': item['solutionOutline']
    })

target_path = ROOT / 'data/assessments/s2c-dev-physics-sample-test.yaml'
target_path.write_text(yaml.safe_dump(assessment, sort_keys=False, allow_unicode=True, width=1000), encoding='utf-8')
print("Successfully wrote sample test.")

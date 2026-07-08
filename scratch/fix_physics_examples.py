import yaml
import glob
import os

files = [
    "data/assessments/physics-newtons-laws-hanging-mass-worked-example.yaml",
    "data/assessments/physics-newtons-laws-static-equilibrium-worked-example.yaml",
    "data/assessments/physics-potential-energy-conservation-rollercoaster-worked-example.yaml",
    "data/assessments/physics-work-energy-atwood-worked-example.yaml"
]

for file in files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    data['categoryId'] = 'physics-1'
    data['modeDefault'] = 'study'
    
    if 'navigation' in data:
        data['navigation']['activityType'] = 'mixedPractice'
        data['navigation']['learningGoal'] = 'practice'

    for we in data.get('workedExamples', []):
        for i, step in enumerate(we.get('steps', [])):
            step['id'] = f"step-{we['id']}-{i+1}"
            step['type'] = 'freeResponse'
            step['prompt'] = 'Did you understand this step?'
            step['answer'] = {'gradingMode': 'selfCheck'}
            
            # Move explanation to instruction
            if 'explanation' in step:
                step['instruction'] = step.pop('explanation')

    with open(file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True, width=1000)
    print(f"Fixed {file}")

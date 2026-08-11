import os, glob, yaml

base = 'c:/Users/SeanS/Downloads/cir_app/data/assessments'
geo_topics = ['angles', 'triangles', 'circles-introduction', 'quadrilaterals', 'polygons', 'angle-chasing', 'areas', 'coordinate-geometry', 'power-of-a-point', 'three-dimensional-geometry', 'transformations', 'geometry-potpourri']

for topic in geo_topics:
    prefix = f'{base}/aops-{topic}'
    patterns = [f'{prefix}-quiz.yaml', f'{prefix}-test.yaml', f'{prefix}-hard-quiz.yaml', f'{prefix}-hard-test.yaml', f'{prefix}-olympiad-quiz.yaml', f'{prefix}-olympiad-test.yaml']
    files = []
    for p in patterns:
        files.extend(glob.glob(p))
    files.sort()
    print(f'=== aops-{topic} ===')
    for f in files:
        fname = os.path.basename(f)
        try:
            with open(f, encoding='utf-8') as fh:
                data = yaml.safe_load(fh)
            qs = data.get('questions', [])
            if not qs:
                print(f'  {fname}: 0 questions')
                continue
            has_diff_dims = any('difficultyDimensions' in q for q in qs)
            first_prompt = qs[0].get('prompt', '')
            is_boilerplate = 'problem pattern' in first_prompt.lower() or ('which statement best' in first_prompt.lower())
            has_issue_signals = any(
                any('issueSignals' in str(c) for c in q.get('choiceOptions', q.get('choices', [])))
                for q in qs
            )
            has_solution_heading = any('Solution:' in str(q.get('explanation','')) for q in qs)
            print(f'  {fname}: {len(qs)} Qs | diffDims={has_diff_dims} | issueSignals={has_issue_signals} | "Solution:" heading={has_solution_heading} | boilerplate={is_boilerplate}')
        except Exception as e:
            print(f'  {fname}: ERROR {e}')
    print()

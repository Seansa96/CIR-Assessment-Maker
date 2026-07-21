import requests

baseUrl = 'http://localhost:5000/api'

try:
    r = requests.post(f'{baseUrl}/attempts', json={'assessmentId': 'cpp-basics-worked-example', 'mode': 'practice'})
    attempt = r.json()
    attempt_id = attempt['id']

    step1_id = 'cpp-basics-output-step-1'
    requests.post(f'{baseUrl}/attempts/{attempt_id}/answers', json={
        'questionId': step1_id,
        'freeResponseText': 'blah'
    })
    requests.post(f'{baseUrl}/attempts/{attempt_id}/answers/{step1_id}/override', json={
        'isCorrect': True
    })

    step2_id = 'cpp-basics-output-step-2'
    r = requests.post(f'{baseUrl}/attempts/{attempt_id}/answers', json={
        'questionId': step2_id,
        'codeText': 'void printer() { std::cout << "Build\\nRun"; }'
    })
    print("Submit step 2 status:", r.status_code)
    print("Submit step 2 body:", r.text)

    r = requests.get(f'{baseUrl}/attempts/{attempt_id}/results')
    results = r.json()
    q_result = next((q for q in results['questions'] if q['questionId'] == step2_id), None)
    import json
    print("Code Feedback:", json.dumps(q_result.get('codeFeedback'), indent=2))
except Exception as e:
    print(e)

import requests

baseUrl = 'http://localhost:5000/api'

# Start attempt
r = requests.post(f'{baseUrl}/attempts', json={'assessmentId': 'cpp-basics-worked-example', 'mode': 'practice'})
attempt = r.json()
attempt_id = attempt['id']

# Submit wrong code to step 2
step2_id = 'cpp-basics-output-step-2'
r = requests.post(f'{baseUrl}/attempts/{attempt_id}/answers', json={
    'questionId': step2_id,
    'codeText': 'void printer() { std::cout << "Build\nRun"; }'
})

# Get results
r = requests.get(f'{baseUrl}/attempts/{attempt_id}/results')
results = r.json()

# Find step 2 result
q_result = next((q for q in results['questions'] if q['questionId'] == step2_id), None)
print(q_result)

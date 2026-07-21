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
print("Submit answer status:", r.status_code)
print("Submit answer body:", r.text)

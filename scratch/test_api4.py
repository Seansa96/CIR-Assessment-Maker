import requests

baseUrl = 'http://localhost:5000/api'

# Start attempt
r = requests.post(f'{baseUrl}/attempts', json={'assessmentId': 'cpp-basics-worked-example', 'mode': 'practice'})
attempt = r.json()
attempt_id = attempt['id']

# Submit step 1
step1_id = 'cpp-basics-output-step-1'
r = requests.post(f'{baseUrl}/attempts/{attempt_id}/answers', json={
    'questionId': step1_id,
    'freeResponseText': 'blah'
})
# Override step 1 as correct
r = requests.post(f'{baseUrl}/attempts/{attempt_id}/answers/{step1_id}/override', json={
    'isCorrect': True
})

# Submit wrong code to step 2
step2_id = 'cpp-basics-output-step-2'
r = requests.post(f'{baseUrl}/attempts/{attempt_id}/answers', json={
    'questionId': step2_id,
    'codeText': 'void printer() { std::cout << "Build\nRun"; }'
})
print("Submit step 2 status:", r.status_code)
print("Submit step 2 body:", r.text)

import requests
import json

baseUrl = 'http://localhost:2000/api/v2'

r = requests.post(f'{baseUrl}/execute', json={
    'language': 'cpp',
    'version': '10.2.0',
    'files': [{
        'name': 'main.cpp',
        'content': '''#include <bits/stdc++.h>
using namespace std;
void printer() { std::cout << "Build\\nRun"; }
int main()
{
    cout << main(test);
    return 0;
}'''
    }]
})

print(json.dumps(r.json(), indent=2))

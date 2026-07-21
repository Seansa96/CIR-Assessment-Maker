import json
import re

with open(r'C:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260721024701-fa0a84f6c8\chunks.json', encoding='utf8') as f:
    data = json.load(f)

output = []
for c in data:
    text = c['text']
    if 'network' in text.lower() or 'distributed' in text.lower():
        output.append(f"Chunk ID: {c['id']}\nText:\n{text[:200]}...\n{'-'*40}")

with open(r'C:\Users\SeanS\Downloads\cir_app\scratch\network_chunks.txt', 'w', encoding='utf8') as f:
    f.write('\n'.join(output))

print(f"Found {len(output)} chunks.")

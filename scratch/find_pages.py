import json
with open('data/source-library/sources/src-20260810144616-0dc6e2835b/chunks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ranges = {}
for chunk in data:
    text = chunk.get('text', '').lower()
    page = chunk.get('metadata', {}).get('pageNumber', 0)
    for topic in ['hash', 'tree', 'heap', 'graph']:
        if topic in text:
            if topic not in ranges:
                ranges[topic] = {'min': page, 'max': page}
            else:
                ranges[topic]['min'] = min(ranges[topic]['min'], page)
                ranges[topic]['max'] = max(ranges[topic]['max'], page)

for topic, r in ranges.items():
    print(f'{topic}: {r["min"]} - {r["max"]}')

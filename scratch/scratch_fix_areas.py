import yaml

with open('data/areas.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# The bad ones are the last 6 areas which have 'subcategories' instead of 'categoryIds' and 'subcategoryIds'
bad_areas = data['areas'][-6:]
data['areas'] = data['areas'][:-6]

for area in bad_areas:
    new_area = {
        "id": area["id"],
        "title": area["title"],
        "description": area["description"],
        "categoryIds": ["cpp-programming"],
        "subcategoryIds": [sub["id"] for sub in area.get("subcategories", [])]
    }
    data['areas'].append(new_area)

with open('data/areas.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)

print("Fixed areas.yaml")

import yaml
import os
import glob
import json

areas_path = 'data/areas.yaml'
cats_path = 'data/categories/*.yaml'

with open(areas_path, 'r', encoding='utf-8') as f:
    areas_data = yaml.safe_load(f)

areas = areas_data.get('areas', [])

cat_files = glob.glob(cats_path)
categories = []
for cf in cat_files:
    with open(cf, 'r', encoding='utf-8') as f:
        cat_data = yaml.safe_load(f)
        if cat_data and 'id' in cat_data:
            categories.append(cat_data['id'])

paths = {}
for cat in categories:
    cat_areas = [a for a in areas if a.get('categoryIds') and cat in a['categoryIds']]
    # If no areas explicitly have this cat in categoryIds, it might be older schema where category ID was something else, or maybe it doesn't have areas.
    if not cat_areas:
        continue
    
    steps = []
    for a in cat_areas:
        title = a.get('title', a.get('id', ''))
        desc = a.get('description', f"Topics related to {title}")
        steps.append({
            "label": title,
            "desc": desc
        })
    paths[cat] = steps

print("const RECOMMENDED_PATHS: Record<string, { label: string; desc: string }[]> = {")
for cat, steps in paths.items():
    print(f'  "{cat}": [')
    for idx, step in enumerate(steps):
        desc = step["desc"].replace('"', '\\"').replace('\n', ' ')
        label = step["label"].replace('"', '\\"')
        comma = "," if idx < len(steps) - 1 else ""
        print(f'    {{ label: "{label}", desc: "{desc}" }}{comma}')
    print("  ],")
print("};")

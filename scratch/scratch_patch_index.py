import yaml
import glob
import re

areas_path = 'data/areas.yaml'
cats_path = 'data/categories/*.yaml'
index_path = 'frontend/src/pages/index.astro'

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
    if not cat_areas:
        continue
    
    steps = []
    for a in cat_areas:
        title = a.get('title', a.get('id', ''))
        desc = a.get('description', f"Topics related to {title}")
        steps.append({"label": title, "desc": desc})
    paths[cat] = steps

new_code = ["      const RECOMMENDED_PATHS: Record<string, { label: string; desc: string }[]> = {"]
for cat, steps in paths.items():
    new_code.append(f'        "{cat}": [')
    for idx, step in enumerate(steps):
        desc = step["desc"].replace('"', '\\"').replace('\n', ' ')
        label = step["label"].replace('"', '\\"')
        comma = "," if idx < len(steps) - 1 else ""
        new_code.append(f'          {{ label: "{label}", desc: "{desc}" }}{comma}')
    new_code.append("        ],")
new_code.append("      };")
new_code_str = "\n".join(new_code)

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the block
pattern = re.compile(r'^\s*const RECOMMENDED_PATHS: Record<string, { label: string; desc: string }\[\]> = \{.*?\n\s*\};\s*$', re.MULTILINE | re.DOTALL)
match = pattern.search(content)

if match:
    new_content = content[:match.start()] + new_code_str + "\n" + content[match.end():]
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched index.astro with new RECOMMENDED_PATHS")
else:
    print("Could not find RECOMMENDED_PATHS block in index.astro")

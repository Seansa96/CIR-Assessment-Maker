import os
import yaml

areas_path = r"c:\Users\SeanS\Downloads\cir_app\data\areas.yaml"
with open(areas_path, 'r', encoding='utf-8') as f:
    areas_data = yaml.safe_load(f)

# Add CSS areas
new_areas = [
    {
        "id": "css-core-mechanics",
        "title": "CSS Core Mechanics",
        "description": "Selectors, Specificity, and the Box Model.",
        "categoryIds": ["css"],
        "subcategoryIds": [
            "css-selectors-specificity",
            "css-box-model"
        ]
    },
    {
        "id": "css-modern-layouts",
        "title": "CSS Modern Layouts",
        "description": "Flexbox and Grid systems.",
        "categoryIds": ["css"],
        "subcategoryIds": [
            "css-layout-flexbox",
            "css-layout-grid"
        ]
    },
    {
        "id": "css-responsive-design-area",
        "title": "Responsive Design",
        "description": "Media queries and responsive techniques.",
        "categoryIds": ["css"],
        "subcategoryIds": [
            "css-responsive-design"
        ]
    }
]

# Avoid duplicates
existing_ids = [a['id'] for a in areas_data.get('areas', [])]
for a in new_areas:
    if a['id'] not in existing_ids:
        areas_data['areas'].append(a)

with open(areas_path, 'w', encoding='utf-8') as f:
    yaml.dump(areas_data, f, default_flow_style=False, sort_keys=False, width=1000)

# Update categories/css.yaml to ensure these subcategories exist
cat_path = r"c:\Users\SeanS\Downloads\cir_app\data\categories\css.yaml"
with open(cat_path, 'r', encoding='utf-8') as f:
    cat_data = yaml.safe_load(f)

subcats = cat_data.get('subcategories', [])
existing_sub_ids = [s['id'] for s in subcats]

for needed_id in ["css-selectors-specificity", "css-box-model", "css-layout-flexbox", "css-layout-grid", "css-responsive-design"]:
    if needed_id not in existing_sub_ids:
        subcats.append({
            "id": needed_id,
            "title": needed_id.replace('-', ' ').title()
        })

cat_data['subcategories'] = subcats
with open(cat_path, 'w', encoding='utf-8') as f:
    yaml.dump(cat_data, f, default_flow_style=False, sort_keys=False, width=1000)

print("Updated areas.yaml and categories/css.yaml")

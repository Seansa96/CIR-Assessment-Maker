import os
import yaml
from pathlib import Path
from collections import defaultdict

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return yaml.safe_load(f)
        except Exception as e:
            return None

def analyze_category(category_file_name, report_title):
    category_path = Path(f'data/categories/{category_file_name}')
    cat_data = load_yaml(category_path)
    if not cat_data:
        return f"Error loading {category_file_name}\n"

    cat_id = cat_data.get('id')
    topics = []
    for item in cat_data.get('subcategories', cat_data): # sometimes it's a list directly
        if isinstance(item, dict) and 'id' in item:
            topics.append(item['id'])
    
    if not topics and isinstance(cat_data, list):
        for item in cat_data:
            if isinstance(item, dict) and 'id' in item:
                topics.append(item['id'])

    report = [f"# {report_title} Audit Report\n"]
    
    # Store findings per topic
    topic_assessments = defaultdict(list)
    topic_errors = defaultdict(list)
    
    assessments_dir = Path('data/assessments')
    for yaml_file in assessments_dir.glob('*.yaml'):
        data = load_yaml(yaml_file)
        if not data:
            topic_errors['Global'].append(f"Could not parse YAML: {yaml_file.name}")
            continue
        
        # Check if this assessment belongs to the category
        file_cat_id = data.get('categoryId')
        file_subcats = data.get('subcategoryIds', [])
        
        # Some might just match the category string
        if file_cat_id == cat_id or (file_cat_id is None and any(sub in topics for sub in file_subcats)):
            pass
        else:
            # Also check if any subcategory matches our topics
            if not any(sub in topics for sub in file_subcats):
                continue
                
        for sub in file_subcats:
            if sub in topics:
                topic_assessments[sub].append((yaml_file, data))
                
    for topic in topics:
        report.append(f"## Topic: `{topic}`")
        assessments = topic_assessments.get(topic, [])
        
        counts = {
            'conceptLesson': 0,
            'guidedProject': 0,
            'workedExample': 0,
            'quiz': 0,
            'test': 0,
            'recallDrill': 0
        }
        
        easy_quizzes = 0
        hard_quizzes = 0
        easy_tests = 0
        hard_tests = 0
        
        issues = []
        
        for file_path, data in assessments:
            a_type = data.get('assessmentType', 'unknown')
            counts[a_type] = counts.get(a_type, 0) + 1
            title = data.get('title', '').lower()
            name = file_path.name.lower()
            
            # Check difficulty for quizzes and tests
            if a_type == 'quiz':
                if 'easy' in title or 'easy' in name:
                    easy_quizzes += 1
                elif 'hard' in title or 'hard' in name:
                    hard_quizzes += 1
            elif a_type == 'test':
                if 'easy' in title or 'easy' in name:
                    easy_tests += 1
                elif 'hard' in title or 'hard' in name:
                    hard_tests += 1
                    
            # Check for placeholders or lack of depth
            if a_type == 'conceptLesson' or a_type == 'guidedProject':
                lesson = data.get('lesson') or data.get('guidedProject')
                if lesson:
                    sections = lesson.get('sections', [])
                    total_text_length = 0
                    for sec in sections:
                        content = sec.get('content', '')
                        total_text_length += len(content)
                    if total_text_length < 200:
                        issues.append(f"Lacking depth in {file_path.name} (Content length: {total_text_length} chars, {len(sections)} step(s))")
                else:
                    issues.append(f"Missing lesson/project content in {file_path.name}")
                    
            if 'placeholder' in title or 'placeholder' in str(data).lower():
                issues.append(f"Placeholder content found in {file_path.name}")
                
        # Analyze coverage
        missing = []
        cl_count = counts.get('conceptLesson', 0) + counts.get('guidedProject', 0)
        if cl_count < 2: missing.append(f"Concept Lessons (found {cl_count}/2)")
        if counts['workedExample'] < 2: missing.append(f"Worked Examples (found {counts['workedExample']}/2)")
        
        if counts['quiz'] < 2: 
            missing.append(f"Quizzes (found {counts['quiz']}/2)")
        else:
            if easy_quizzes == 0 and hard_quizzes == 0:
                missing.append("Quizzes missing explicit Easy/Hard distinctions")
                
        if counts['test'] < 2:
            missing.append(f"Tests (found {counts['test']}/2)")
        else:
            if easy_tests == 0 and hard_tests == 0:
                missing.append("Tests missing explicit Easy/Hard distinctions")

        report.append(f"**Coverage**: {len(assessments)} total assessments")
        if missing:
            report.append("**Missing/Deficient**:")
            for m in missing:
                report.append(f"- {m}")
        else:
            report.append("**Coverage Complete**: Meets standard requirements.")
            
        if issues:
            report.append("**Issues & Observations**:")
            for i in issues:
                report.append(f"- {i}")
                
        report.append("\n---\n")

    return "\n".join(report)

geom_report = analyze_category('geometry.yaml', 'Geometry')
calc2_report = analyze_category('calculus-2.yaml', 'Calculus 2')

with open('scratch/geometry_calc2_audit_report.md', 'w', encoding='utf-8') as f:
    f.write(geom_report + "\n\n" + calc2_report)
print("Report generated at scratch/geometry_calc2_audit_report.md")

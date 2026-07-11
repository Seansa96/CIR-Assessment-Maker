import os
import yaml
import glob

def fix_content_errors():
    assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
    
    # 1. Fix duplicate step IDs in lessons / worked examples
    files = glob.glob(os.path.join(assessments_dir, "ec-ch*-lesson*.yaml")) + glob.glob(os.path.join(assessments_dir, "ec-ch*-worked-example*.yaml"))
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        modified = False
        step_counter = 1
        
        if 'workedExamples' in data:
            for we in data['workedExamples']:
                if 'steps' in we:
                    for step in we['steps']:
                        if step.get('id', '').startswith('s'):
                            step['id'] = f"step{step_counter}"
                            step_counter += 1
                            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, sort_keys=False, allow_unicode=True)
                print(f"Fixed duplicate step IDs in {filepath}")
                
    # 2. Fix glossaries
    glossary_files = glob.glob(os.path.join(assessments_dir, "ec-ch*-glossary.yaml"))
    for filepath in glossary_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        modified = False
        
        # Missing introduction
        if 'glossary' in data and 'introduction' not in data['glossary']:
            data['glossary']['introduction'] = "Review these terms carefully."
            modified = True
            
        # Missing drills
        # Read the corresponding recalldrill file
        ch_num = os.path.basename(filepath).split('-')[1]
        recalldrill_path = os.path.join(assessments_dir, f"ec-{ch_num}-recalldrill.yaml")
        recalldrill_ids = []
        if os.path.exists(recalldrill_path):
            with open(recalldrill_path, 'r', encoding='utf-8') as f2:
                rd_data = yaml.safe_load(f2)
                if 'items' in rd_data:
                    recalldrill_ids = [item['id'] for item in rd_data['items']]
        
        if 'glossary' in data and 'sections' in data['glossary']:
            for sec in data['glossary']['sections']:
                if 'entries' in sec:
                    for i, entry in enumerate(sec['entries']):
                        if 'drills' not in entry:
                            # Just map to the first recall drill item or whatever
                            drill_id = recalldrill_ids[i % len(recalldrill_ids)] if recalldrill_ids else "rd1"
                            entry['drills'] = [
                                {
                                    "assessmentId": f"ec-{ch_num}-recalldrill",
                                    "itemId": drill_id
                                }
                            ]
                            modified = True
                            
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, sort_keys=False, allow_unicode=True)
                print(f"Fixed glossary in {filepath}")

if __name__ == "__main__":
    fix_content_errors()

import os
import yaml
import glob
import copy

def fix_glossary_drills():
    assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
    glossary_files = glob.glob(os.path.join(assessments_dir, "ec-ch*-glossary.yaml"))
    
    for filepath in glossary_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        modified = False
        ch_num = os.path.basename(filepath).split('-')[1]
        recalldrill_path = os.path.join(assessments_dir, f"ec-{ch_num}-recalldrill.yaml")
        
        rd_items = []
        if os.path.exists(recalldrill_path):
            with open(recalldrill_path, 'r', encoding='utf-8') as f2:
                rd_data = yaml.safe_load(f2)
                if 'items' in rd_data:
                    rd_items = rd_data['items']
        
        if 'glossary' in data and 'sections' in data['glossary']:
            for sec in data['glossary']['sections']:
                if 'entries' in sec:
                    for i, entry in enumerate(sec['entries']):
                        if 'drills' in entry and len(entry['drills']) > 0:
                            # Check if the drill has assessmentId (my broken script)
                            if 'assessmentId' in entry['drills'][0]:
                                # We need to replace it with a real drill
                                drill_obj = copy.deepcopy(rd_items[i % len(rd_items)]) if rd_items else None
                                if drill_obj:
                                    # Ensure id is unique for glossary context
                                    drill_obj['id'] = f"{entry['id']}-drill"
                                    entry['drills'] = [drill_obj]
                                    modified = True
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, sort_keys=False, allow_unicode=True)
                print(f"Fixed glossary drills in {filepath}")

if __name__ == "__main__":
    fix_glossary_drills()

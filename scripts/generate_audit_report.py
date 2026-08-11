import os
import yaml
import glob
import subprocess

def audit():
    files = glob.glob('data/assessments/*.yaml')
    failed_files = {}
    
    for f in files:
        result = subprocess.run(
            ['python', r'scripts\validate_s2c_content.py', f],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            lines = result.stdout.split('\n') + result.stderr.split('\n')
            errors = [line.strip() for line in lines if line.strip().startswith('-')]
            if not errors:
                errors = [line for line in lines if 'Failed' in line]
            failed_files[f] = errors
            
    with open('audit_report.md', 'w') as out:
        out.write("# Assessment S2C Audit Report\n\n")
        
        # Check against areas
        with open('data/areas.yaml', 'r', encoding='utf-8') as area_f:
            areas_data = yaml.safe_load(area_f)
            
        topics = set()
        for f in files:
            with open(f, 'r', encoding='utf-8') as yf:
                try:
                    data = yaml.safe_load(yf)
                    if data and 'topicId' in data:
                        topics.add(data['topicId'])
                except:
                    pass
                    
        # Check if topics exist in areas (simplified check, usually we'd parse categories but topics belong to subcategories or category directly? The schema says area has categoryIds and subcategoryIds, topics belong to subcategories or categories. Wait, in CIR, areas contain categories and subcategories, but topics are just ids inside assessments. Let's just list failing files first.)
        
        out.write(f"Total files audited: {len(files)}\n")
        out.write(f"Files failing S2C validation: {len(failed_files)}\n\n")
        
        if failed_files:
            out.write("## Non-Compliant Files\n\n")
            for f, errs in failed_files.items():
                out.write(f"### `{f}`\n")
                for err in errs:
                    out.write(f"{err}\n")
                out.write("\n")
        else:
            out.write("All files pass S2C validation!\n")

if __name__ == '__main__':
    audit()

import yaml
import glob
import sys

for f in glob.glob('data/assessments/*.yaml'):
    try:
        with open(f, encoding='utf-8') as file:
            yaml.safe_load(file)
    except Exception as e:
        print(f"Error in {f}: {e}")

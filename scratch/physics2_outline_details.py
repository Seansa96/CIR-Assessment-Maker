import json
import sys

outline_file = r'c:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260806094518-3f5d8d0e38\outline.json'
with open(outline_file, 'r', encoding='utf-8') as f:
    outline = json.load(f)

with open(r'c:\Users\SeanS\Downloads\cir_app\scratch\physics2_outline.txt', 'w', encoding='utf-8') as out:
    def print_sections(node, depth=0):
        if node.get('kind') in ['chapter', 'section']:
            indent = '  ' * depth
            out.write(f"{indent}- {node.get('title')}\n")
        if 'children' in node:
            for child in node['children']:
                if child.get('kind') in ['chapter', 'section']:
                    print_sections(child, depth + 1)
                else:
                    print_sections(child, depth)

    if 'root' in outline:
        print_sections(outline['root'])

import os

scripts_dir = r"c:\Users\SeanS\Downloads\cir_app\scripts"

for i in range(1, 5):
    filepath = os.path.join(scripts_dir, f"generate_ch{i}.py")
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We need to replace:
    # "glossary": [
    #     {
    #         "term": ...
    
    # With:
    # "glossary": {
    #     "sections": [
    #         {
    #             "id": "main-section",
    #             "title": "Main Glossary",
    #             "entries": [
    #                 {
    #                     "id": "entry-X", # Generate an ID based on term or index
    #                     "term": ...

    # Actually, the python structure in the script is:
    # "glossary": [
    #     {
    #         "term": ...
    
    # Let's just modify the scripts using regex or string replacement.
    import re
    # Find the glossary list definition
    
    # In my scripts, it looks like:
    #         "glossary": [
    #             {
    #                 "term": "Current",
    
    new_content = re.sub(
        r'"glossary": \[\s*\{\s*"term":',
        r'"glossary": {\n            "sections": [\n                {\n                    "id": "main-section",\n                    "title": "Terms",\n                    "entries": [\n                        {\n                            "id": "term1",\n                            "term":',
        content
    )
    
    # This naive replace won't add IDs to all terms. The schema requires `id` for each entry.
    # It's better to just write a script that loads the YAML, fixes it, and saves it.
    

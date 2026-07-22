import json

with open(r"c:\Users\SeanS\Downloads\cir_app\data\source-library\sources\src-20260721050516-3b19f1c4b6\chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Kirchhoff")
for chunk in chunks:
    text = chunk.get("text", "").lower()
    if "kirchhoff's current law" in text and "frequency domain" not in text:
        print(f"ID: {chunk.get('id')} - {text[:80].replace(chr(10), ' ')}")
        break

print("Ohm's Law")
for chunk in chunks:
    text = chunk.get("text", "").lower()
    if "ohm's law" in text and "frequency domain" not in text:
        print(f"ID: {chunk.get('id')} - {text[:80].replace(chr(10), ' ')}")
        break

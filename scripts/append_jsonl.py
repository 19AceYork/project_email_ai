import os
import json

folder = 'data'
if not os.path.exists(folder):
    os.makedirs(folder)

jsonl_path = os.path.join(folder, 'knowledge_base.jsonl')

def append_to_jsonl(file_path, details, content):
    entry = {
        "details": details,
        "content": content
    }
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

append_to_jsonl(jsonl_path, "Example details", "Example content")

print(f"Appended data to {jsonl_path}")
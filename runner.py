import json

def parse_object_pairs(pairs):
    return {key.replace("'", '"'): value for key, value in pairs}

# Read raw content from "pit.txt" file
with open("pit.txt", "r") as f:
    raw_content = f.read()

# Parse JSON data using json.loads() with object_hook
subject_matter_data = json.loads(raw_content, object_hook=parse_object_pairs)

print(subject_matter_data)

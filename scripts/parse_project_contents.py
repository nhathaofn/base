import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with open('flow-research/observations/project_contents_raw.json', 'r', encoding='utf-8') as f:
    contents = json.load(f)

print(f"Top-level keys / sections: {len(contents)}")
for i, section in enumerate(contents):
    if section is None:
        print(f"Section {i}: None")
    elif isinstance(section, list):
        print(f"Section {i}: List with {len(section)} items")
    elif isinstance(section, dict):
        print(f"Section {i}: Dict with keys {list(section.keys())}")
    else:
        print(f"Section {i}: {type(section)} ({section})")

# Section 1 is Scenes
scenes = contents[1] if len(contents) > 1 and isinstance(contents[1], list) else []
print(f"\n=== SCENES ({len(scenes)}) ===")
for s in scenes[:5]:
    scene_id = s[0]
    meta = s[3] if len(s) > 3 else []
    proj_id = s[4] if len(s) > 4 else None
    print(f"Scene ID: {scene_id}")
    print(f"  Title: {meta[0] if len(meta) > 0 else 'N/A'}")
    print(f"  Asset ID: {meta[4] if len(meta) > 4 else 'N/A'}")
    print(f"  Task/Job ID: {meta[5] if len(meta) > 5 else 'N/A'}")
    print(f"  Project ID: {proj_id}")

# Section 2 is Workflows
workflows = contents[2] if len(contents) > 2 and isinstance(contents[2], list) else []
print(f"\n=== WORKFLOWS ({len(workflows)}) ===")
for w in workflows[:5]:
    wf_id = w[0]
    proj_id = w[1] if len(w) > 1 else None
    scene_id = w[2] if len(w) > 2 else None
    payload = w[5] if len(w) > 5 else []
    print(f"Workflow ID: {wf_id}")
    print(f"  Project ID: {proj_id}")
    print(f"  Scene ID: {scene_id}")
    if isinstance(payload, list) and len(payload) > 1:
        prompt = payload[1] if len(payload) > 1 else None
        print(f"  Prompt: {str(prompt)[:120]}...")
    print(f"  Full workflow schema snippet: {json.dumps(w, ensure_ascii=False)[:300]}...")

# Section 3 is Media / Assets
if len(contents) > 3 and isinstance(contents[3], list):
    media_items = contents[3]
    print(f"\n=== MEDIA ASSETS ({len(media_items)}) ===")
    for m in media_items[:5]:
        print(f"Media: {json.dumps(m, ensure_ascii=False)[:300]}...")

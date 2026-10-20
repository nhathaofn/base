import json
import os
import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

bundle_dir = 'flow-research/observations/bundles'
rpc_table = {}

pattern = re.compile(r'\{Wa:\s*"([^"]+)",\s*hb:\s*"([^"]+)"')
alt_pattern = re.compile(r'\{hb:\s*"([^"]+)",\s*Wa:\s*"([^"]+)"')

for fname in sorted(os.listdir(bundle_dir)):
    if not fname.endswith('.js'):
        continue
    fpath = os.path.join(bundle_dir, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    matches = pattern.findall(content)
    for rpc_id, service_method in matches:
        if rpc_id not in rpc_table:
            rpc_table[rpc_id] = {
                'rpc_id': rpc_id,
                'service_method': service_method,
                'source_bundle': fname
            }

    alt_matches = alt_pattern.findall(content)
    for service_method, rpc_id in alt_matches:
        if rpc_id not in rpc_table:
            rpc_table[rpc_id] = {
                'rpc_id': rpc_id,
                'service_method': service_method,
                'source_bundle': fname
            }

# Sort by service name and method name
sorted_rpcs = sorted(rpc_table.values(), key=lambda x: (x['service_method'], x['rpc_id']))

print(f"Extracted {len(sorted_rpcs)} total unique RPC definitions:")
print(f"{'RPC ID':<10} | {'Service & Method':<55} | {'Source Bundle'}")
print("-" * 85)
for item in sorted_rpcs:
    print(f"{item['rpc_id']:<10} | {item['service_method']:<55} | {item['source_bundle']}")

os.makedirs('flow-research/verified/api', exist_ok=True)
with open('flow-research/verified/api/rpc_registry.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_rpcs, f, indent=2, ensure_ascii=False)

print(f"\nSaved full RPC registry to flow-research/verified/api/rpc_registry.json")

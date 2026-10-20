import json
import os
import re
import urllib.request

bundle_dir = 'flow-research/observations/bundles'

new_chunk_urls = [
    "https://www.gstatic.com/_/mss/boq-labs-ai-sandbox/_/js/k=boq-labs-ai-sandbox.AiSandboxAngularFrontend.vi.1dcxrhzrvVk.2018.O/ck=boq-labs-ai-sandbox.AiSandboxAngularFrontend.lY61RRYx2Hs.L.B1.O/d=1/exm=_b,wO1vlb/excm=_b/ed=1/br=1/wt=2/ujg=1/rs=APwUF7yDJDHoeElqUFAgCbt-QF_TkkCYtQ/ee=Pjplud:PoEs9b;QGR0gd:Mlhmy;ScI3Yc:e7Hzgb;YIZmRd:A1yn5d;cEt90b:ws9Tlc;dowIGb:ebZ3mb/dti=1/m=XRV0Af",
    "https://www.gstatic.com/_/mss/boq-labs-ai-sandbox/_/js/k=boq-labs-ai-sandbox.AiSandboxAngularFrontend.vi.1dcxrhzrvVk.2018.O/ck=boq-labs-ai-sandbox.AiSandboxAngularFrontend.lY61RRYx2Hs.L.B1.O/d=1/exm=_b/excm=_b/ed=1/br=1/wt=2/ujg=1/rs=APwUF7yDJDHoeElqUFAgCbt-QF_TkkCYtQ/ee=Pjplud:PoEs9b;QGR0gd:Mlhmy;ScI3Yc:e7Hzgb;YIZmRd:A1yn5d;cEt90b:ws9Tlc;dowIGb:ebZ3mb/dti=1/m=wO1vlb"
]

for i, url in enumerate(new_chunk_urls):
    name = f"chunk_studio_{i}.js"
    path = os.path.join(bundle_dir, name)
    if not os.path.exists(path):
        print(f"Downloading {path}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp, open(path, 'wb') as f:
            f.write(resp.read())
        print(f"Downloaded {os.path.getsize(path)} bytes.")

# Now scan all bundles for rpc definitions
pattern = re.compile(r'\{Wa:\s*"([^"]+)",\s*hb:\s*"([^"]+)"')
alt_pattern = re.compile(r'\{hb:\s*"([^"]+)",\s*Wa:\s*"([^"]+)"')

rpc_table = {}
for fname in sorted(os.listdir(bundle_dir)):
    if not fname.endswith('.js'):
        continue
    fpath = os.path.join(bundle_dir, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    for rpc_id, service_method in pattern.findall(content):
        rpc_table[rpc_id] = {'rpc_id': rpc_id, 'service_method': service_method, 'source_bundle': fname}
    for service_method, rpc_id in alt_pattern.findall(content):
        rpc_table[rpc_id] = {'rpc_id': rpc_id, 'service_method': service_method, 'source_bundle': fname}

print(f"Total RPC definitions after adding studio chunks: {len(rpc_table)}")

# Check our newly observed RPC IDs
studio_ids = ['mrlkwd', 'HTrJv', 'yBhWQ', 'ngNC2', 'tRARke', 'qJcgMc', 'LPzVkd']
for sid in studio_ids:
    print(f"  {sid:<10}: {rpc_table.get(sid, {}).get('service_method', 'NOT_IN_WA_PATTERN')}")

# Save updated registry
sorted_rpcs = sorted(rpc_table.values(), key=lambda x: (x['service_method'], x['rpc_id']))
with open('flow-research/verified/api/rpc_registry.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_rpcs, f, indent=2, ensure_ascii=False)

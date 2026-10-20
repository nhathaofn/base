import os
import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

known_rpcs = ["UpteDb", "cPZSdc", "nzlxg", "Yizz8d", "xI9TVb", "NfrxTb", "KV2T2d"]

bundles = [
    'flow-research/observations/bundles/bundle_0.js',
    'flow-research/observations/bundles/bundle_1.js',
    'flow-research/observations/bundles/bundle_2.js',
    'flow-research/observations/bundles/bundle_3.js',
]

for bpath in bundles:
    print(f"\n--- Scanning {bpath} ---")
    with open(bpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find context for each known RPC
    for rpc in known_rpcs:
        pos = 0
        while True:
            idx = content.find(rpc, pos)
            if idx == -1:
                break
            start = max(0, idx - 150)
            end = min(len(content), idx + 150)
            snippet = content[start:end].replace('\n', ' ')
            print(f"Match [{rpc}] at {idx}:")
            print(f"  ... {snippet} ...")
            pos = idx + len(rpc)

    # Search for patterns where RPC IDs are defined or registered
    # Frequently: "rpc_name" followed or preceded by protobuf service path or endpoint
    proto_matches = re.findall(r'([a-zA-Z0-9_\.]*(?:aisandbox|creative|flow|video|image|project)[a-zA-Z0-9_\.]*)', content, re.IGNORECASE)
    unique_protos = sorted(list(set(m for m in proto_matches if len(m) > 8 and '.' in m)))
    if unique_protos:
        print(f"Protobuf / Service references in {bpath}:")
        for p in unique_protos[:20]:
            print("  ", p)

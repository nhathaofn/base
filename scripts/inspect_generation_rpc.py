import os
import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

bundle_dir = 'flow-research/observations/bundles'

def find_rpc_class(rpc_id):
    print(f"\n=== Investigating RPC ID: {rpc_id} ===")
    for fname in sorted(os.listdir(bundle_dir)):
        if not fname.endswith('.js'):
            continue
        fpath = os.path.join(bundle_dir, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        idx = content.find(f'"{rpc_id}"')
        if idx != -1:
            snippet = content[max(0, idx-200):min(len(content), idx+400)].replace('\n', ' ')
            print(f"Found in {fname}:")
            print(f"  {snippet}")
            
            # Find the Xa (request class) and kb (response class)
            m = re.search(r'\{Wa:\s*"' + rpc_id + r'",\s*hb:\s*"([^"]+)",\s*Za:\s*([^,]+),\s*Xa:\s*([^,]+),\s*kb:\s*([^}]+)\}', content)
            if m:
                hb, za, xa, kb = m.groups()
                print(f"  Service.Method: {hb}")
                print(f"  Request Class: {xa.strip()}")
                print(f"  Response Class: {kb.strip()}")

for rpc in ['L2jnw', 'agJzFb', 'Z9cAtf', 'ogiZ0b', 'xNyCid', 'Z8KLDf', 'cNQB4b']:
    find_rpc_class(rpc)

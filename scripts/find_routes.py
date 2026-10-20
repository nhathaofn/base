import os
import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

bundle_dir = 'flow-research/observations/bundles'

for fname in sorted(os.listdir(bundle_dir)):
    if not fname.endswith('.js'):
        continue
    fpath = os.path.join(bundle_dir, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Search for route definitions
    routes = re.findall(r'path:\s*["\']([^"\']+)["\']', content)
    if routes:
        print(f"Routes found in {fname}:", sorted(list(set(routes))))

    # Search for project URL patterns
    url_patterns = re.findall(r'["\'](/project/[^"\']+)["\']', content)
    if url_patterns:
        print(f"Project URL patterns in {fname}:", sorted(list(set(url_patterns))))

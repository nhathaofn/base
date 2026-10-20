import json
import os
import sys
from urllib.parse import urlparse, parse_qs

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def analyze_capture(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    print(f"Total items in {file_path}: {len(items)}")

    endpoints = []
    batchexecute_calls = []

    for item in items:
        url = item.get('url', '')
        if not url:
            continue
        parsed = urlparse(url)
        method = item.get('method', 'GET')
        status = item.get('status', 'unknown')
        mime = item.get('mimeType', 'unknown')
        is_api = item.get('is_api_candidate', False)

        endpoint_info = {
            'method': method,
            'host': parsed.netloc,
            'path': parsed.path,
            'query_keys': list(parse_qs(parsed.query).keys()),
            'status': status,
            'mime': mime,
            'has_post_data': bool(item.get('postData')),
            'has_response_body': bool(item.get('response_body'))
        }
        endpoints.append(endpoint_info)

        # Inspect Google batchexecute RPCs
        if 'batchexecute' in parsed.path:
            post_data = item.get('postData', '')
            # Parse f.req
            rpc_ids = []
            if 'f.req=' in post_data:
                # Extract RPC names
                import re
                # Pattern: [["rpc_name", ...
                matches = re.findall(r'\["([A-Za-z0-9_]+)",', post_data)
                rpc_ids = list(set(matches))
            
            resp_body = item.get('response_body', '')
            batchexecute_calls.append({
                'url': url,
                'rpc_ids': rpc_ids,
                'postData_preview': post_data[:400],
                'response_preview': resp_body[:400] if resp_body else '[EMPTY]'
            })

        # Inspect other JSON/REST APIs
        elif ('/api/' in parsed.path or '/v1/' in parsed.path or '/v2/' in parsed.path or 'flow.google.com/_/' in url) and method == 'POST':
            print("\n--- NON-BATCHEXECUTE POST API FOUND ---")
            print(f"URL: {url}")
            print(f"Method: {method}, Status: {status}")
            print(f"PostData: {item.get('postData')[:500] if item.get('postData') else 'None'}")
            print(f"Response: {item.get('response_body')[:500] if item.get('response_body') else 'None'}")

    print("\n=== BATCHEXECUTE RPC CALLS ===")
    for b in batchexecute_calls:
        print(f"RPC IDs: {b['rpc_ids']}")
        print(f"Payload preview: {b['postData_preview']}")
        print(f"Response preview: {b['response_preview']}")
        print("-" * 50)

    print("\n=== ALL DISTINCT PATHS ===")
    unique_paths = sorted(list(set((e['method'], e['host'], e['path']) for e in endpoints)))
    for m, h, p in unique_paths:
        print(f"{m:6} https://{h}{p}")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'flow-research/observations/raw_network/page_load.json'
    analyze_capture(path)

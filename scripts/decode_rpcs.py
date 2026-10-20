import json
import re
import sys
import urllib.parse

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def parse_batchexecute(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    items = data.get('network', data) if isinstance(data, dict) else data

    for item in items:
        url = item.get('url', '')
        if 'batchexecute' not in url:
            continue
        
        print("\n" + "=" * 70)
        print("URL:", url)
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        print("RPCIDs param:", query.get('rpcids'))
        print("bl (build label):", query.get('bl'))
        print("f.sid (session id):", query.get('f.sid'))

        post = item.get('postData', '')
        if 'f.req=' in post:
            post_params = urllib.parse.parse_qs(post)
            f_req = post_params.get('f.req', [''])[0]
            at_token = post_params.get('at', [''])[0]
            print(f"CSRF Token ('at'): {at_token[:15]}... (length {len(at_token)})")
            
            # f_req is typically JSON string
            try:
                decoded_req = json.loads(f_req)
                print(f"Decoded f.req structure: {len(decoded_req)} calls")
                for call in decoded_req:
                    # call structure: [ [rpc_id, payload_str, null, "generic"] ]
                    for subcall in call:
                        rpc_name = subcall[0]
                        payload_raw = subcall[1]
                        print(f"  -> RPC Method: {rpc_name}")
                        try:
                            parsed_payload = json.loads(payload_raw)
                            print(f"     Payload JSON: {json.dumps(parsed_payload, ensure_ascii=False)}")
                        except Exception:
                            print(f"     Payload Raw: {payload_raw}")
            except Exception as e:
                print(f"Could not parse f.req JSON: {e}")

        resp = item.get('response_body', '')
        if resp:
            print("\nResponse Structure:")
            # Google batchexecute format starts with )]}'\n<num>\n
            lines = resp.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('[[') and 'wrb.fr' in line:
                    try:
                        resp_json = json.loads(line)
                        for envelope in resp_json:
                            if envelope[0] == 'wrb.fr':
                                rpc_id = envelope[1]
                                data_str = envelope[2]
                                print(f"  <- RPC Response for: {rpc_id}")
                                if data_str:
                                    try:
                                        data_json = json.loads(data_str)
                                        formatted = json.dumps(data_json, indent=4, ensure_ascii=False)
                                        if len(formatted) > 1000:
                                            print(f"     Data (truncated): {formatted[:1000]}...\n     [Total length: {len(formatted)} chars]")
                                        else:
                                            print(f"     Data:\n{formatted}")
                                    except Exception:
                                        print(f"     Raw data: {data_str[:500]}")
                                else:
                                    print("     Data: null / empty")
                    except Exception as e:
                        print(f"Error parsing response line: {e}")

if __name__ == '__main__':
    parse_batchexecute('flow-research/observations/raw_network/page_load.json')

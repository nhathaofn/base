import asyncio
import json
import os
import sys
import time
import urllib.request
import websockets

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class PageLoadRecorder:
    def __init__(self, port=9222, output_path='flow-research/observations/raw_network/page_load.json'):
        self.port = port
        self.output_path = output_path
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.ws = None
        self.req_id = 0
        self.pending_requests = {}
        self.captured_items = []
        self.body_requests = {}

    def find_flow_target(self):
        req = urllib.request.urlopen(f'http://127.0.0.1:{self.port}/json')
        tabs = json.loads(req.read().decode('utf-8'))
        for tab in tabs:
            if 'flow.google.com' in tab.get('url', ''):
                return tab['webSocketDebuggerUrl']
        raise RuntimeError("No flow.google.com tab found")

    async def send(self, method, params=None):
        self.req_id += 1
        msg = {'id': self.req_id, 'method': method}
        if params:
            msg['params'] = params
        await self.ws.send(json.dumps(msg))
        return self.req_id

    def sanitize_headers(self, headers):
        sanitized = {}
        sensitive_keys = {'cookie', 'authorization', 'x-goog-api-key', 'set-cookie', 'x-csrf-token'}
        for k, v in headers.items():
            if k.lower() in sensitive_keys:
                sanitized[k] = '[REDACTED_SENSITIVE_AUTH]'
            else:
                sanitized[k] = v
        return sanitized

    async def run(self, wait_sec=12):
        ws_url = self.find_flow_target()
        self.ws = await websockets.connect(ws_url, max_size=50 * 1024 * 1024)
        print("Connected to CDP.")

        await self.send('Network.enable', {
            'maxTotalBufferSize': 50000000,
            'maxResourceBufferSize': 25000000
        })
        await self.send('Page.enable')

        # Trigger reload
        print("Triggering page reload...")
        await self.send('Page.reload', {'ignoreCache': True})

        start_time = time.time()
        while time.time() - start_time < wait_sec:
            try:
                raw = await asyncio.wait_for(self.ws.recv(), timeout=1.0)
                msg = json.loads(raw)

                if 'id' in msg and msg['id'] in self.body_requests:
                    req_id = self.body_requests.pop(msg['id'])
                    body = msg.get('result', {}).get('body', '')
                    is_base64 = msg.get('result', {}).get('base64Encoded', False)
                    if req_id in self.pending_requests:
                        self.pending_requests[req_id]['response_body'] = body
                        self.pending_requests[req_id]['response_base64'] = is_base64
                        self.captured_items.append(self.pending_requests.pop(req_id))
                    continue

                method = msg.get('method', '')
                params = msg.get('params', {})

                if method == 'Network.requestWillBeSent':
                    rid = params.get('requestId')
                    req = params.get('request', {})
                    url = req.get('url', '')
                    is_api = any(kw in url for kw in [
                        '/batchexecute', '/api/', '/v1/', '/v2/', 'boq-labs-ai-sandbox',
                        'flow.google.com/_/', 'labs-ai', 'aitestkitchen', 'play.google.com/log'
                    ]) or req.get('method') == 'POST'

                    self.pending_requests[rid] = {
                        'requestId': rid,
                        'url': url,
                        'method': req.get('method'),
                        'headers': self.sanitize_headers(req.get('headers', {})),
                        'postData': req.get('postData'),
                        'timestamp': params.get('timestamp'),
                        'type': params.get('type'),
                        'is_api_candidate': is_api
                    }

                elif method == 'Network.responseReceived':
                    rid = params.get('requestId')
                    resp = params.get('response', {})
                    if rid in self.pending_requests:
                        self.pending_requests[rid]['status'] = resp.get('status')
                        self.pending_requests[rid]['statusText'] = resp.get('statusText')
                        self.pending_requests[rid]['responseHeaders'] = self.sanitize_headers(resp.get('headers', {}))
                        self.pending_requests[rid]['mimeType'] = resp.get('mimeType')

                elif method == 'Network.loadingFinished':
                    rid = params.get('requestId')
                    if rid in self.pending_requests:
                        req_meta = self.pending_requests[rid]
                        if req_meta.get('is_api_candidate'):
                            call_id = await self.send('Network.getResponseBody', {'requestId': rid})
                            self.body_requests[call_id] = rid
                        else:
                            self.captured_items.append(self.pending_requests.pop(rid))

            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"Error: {e}")
                break

        for rid, item in self.pending_requests.items():
            self.captured_items.append(item)

        await self.ws.close()
        print(f"Captured {len(self.captured_items)} network items.")

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(self.captured_items, f, indent=2, ensure_ascii=False)
        print(f"Saved to {self.output_path}")

if __name__ == '__main__':
    asyncio.run(PageLoadRecorder().run(15))

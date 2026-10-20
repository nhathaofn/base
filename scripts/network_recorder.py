import asyncio
import json
import os
import sys
import time
import urllib.request
import websockets

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class NetworkRecorder:
    def __init__(self, port=9222, output_dir='flow-research/observations/raw_network'):
        self.port = port
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.ws = None
        self.req_id = 0
        self.pending_requests = {}
        self.captured_items = []
        self.running = True

    def find_flow_target(self):
        req = urllib.request.urlopen(f'http://127.0.0.1:{self.port}/json')
        tabs = json.loads(req.read().decode('utf-8'))
        for tab in tabs:
            if 'flow.google.com' in tab.get('url', ''):
                return tab['webSocketDebuggerUrl']
        raise RuntimeError(f"No flow.google.com tab found on port {self.port}")

    async def send(self, method, params=None):
        self.req_id += 1
        msg = {'id': self.req_id, 'method': method}
        if params:
            msg['params'] = params
        await self.ws.send(json.dumps(msg))
        return self.req_id

    async def get_response_body(self, request_id):
        call_id = await self.send('Network.getResponseBody', {'requestId': request_id})
        # Note: Handled in message loop
        return call_id

    def sanitize_headers(self, headers):
        sanitized = {}
        sensitive_keys = {'cookie', 'authorization', 'x-goog-api-key', 'set-cookie', 'x-csrf-token'}
        for k, v in headers.items():
            if k.lower() in sensitive_keys:
                sanitized[k] = '[REDACTED_SENSITIVE_AUTH]'
            else:
                sanitized[k] = v
        return sanitized

    async def listen(self, duration_sec=10):
        ws_url = self.find_flow_target()
        self.ws = await websockets.connect(ws_url, max_size=50 * 1024 * 1024)
        print("Connected to CDP on target tab.")

        await self.send('Network.enable', {
            'maxTotalBufferSize': 50000000,
            'maxResourceBufferSize': 25000000
        })
        await self.send('Page.enable')

        body_requests = {}
        start_time = time.time()

        print(f"Recording network traffic for {duration_sec}s...")

        while time.time() - start_time < duration_sec and self.running:
            try:
                raw = await asyncio.wait_for(self.ws.recv(), timeout=1.0)
                msg = json.loads(raw)
                
                # Check for responses to getResponseBody
                if 'id' in msg and msg['id'] in body_requests:
                    req_id = body_requests.pop(msg['id'])
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
                    # Filter out static fonts/images unless api
                    is_api = any(kw in url for kw in ['/batchexecute', '/api/', '/v1/', '/v2/', 'flow.google.com/_/', 'labs-ai', 'aitestkitchen']) or req.get('method') == 'POST'
                    
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
                        # Request body
                        req_meta = self.pending_requests[rid]
                        if req_meta.get('is_api_candidate'):
                            call_id = await self.send('Network.getResponseBody', {'requestId': rid})
                            body_requests[call_id] = rid
                        else:
                            self.captured_items.append(self.pending_requests.pop(rid))

                elif method == 'Network.webSocketCreated':
                    self.captured_items.append({
                        'event': 'webSocketCreated',
                        'url': params.get('url')
                    })

                elif method == 'Network.webSocketFrameSent':
                    self.captured_items.append({
                        'event': 'webSocketFrameSent',
                        'payload': params.get('response', {}).get('payloadData')
                    })

                elif method == 'Network.webSocketFrameReceived':
                    self.captured_items.append({
                        'event': 'webSocketFrameReceived',
                        'payload': params.get('response', {}).get('payloadData')
                    })

            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"Error in loop: {e}")
                break

        # Flush any remaining
        for rid, item in self.pending_requests.items():
            self.captured_items.append(item)

        await self.ws.close()
        print(f"Finished recording. Captured {len(self.captured_items)} items.")
        
        timestamp_str = int(time.time())
        out_file = os.path.join(self.output_dir, f'capture_{timestamp_str}.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(self.captured_items, f, indent=2, ensure_ascii=False)
        print(f"Saved capture to {out_file}")
        return out_file

if __name__ == '__main__':
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    recorder = NetworkRecorder()
    asyncio.run(recorder.listen(duration))

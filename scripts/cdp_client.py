import asyncio
import json
import os
import sys
import urllib.request
import websockets

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class FlowCDP:
    def __init__(self, port=9222):
        self.port = port
        self.ws = None
        self.msg_id = 0
        self.callbacks = {}
        self.events = []
        self.target_id = None
        self.ws_url = None

    def find_flow_target(self):
        req = urllib.request.urlopen(f'http://127.0.0.1:{self.port}/json')
        tabs = json.loads(req.read().decode('utf-8'))
        for tab in tabs:
            if 'flow.google.com' in tab.get('url', ''):
                self.target_id = tab['id']
                self.ws_url = tab['webSocketDebuggerUrl']
                return tab
        raise RuntimeError("No flow.google.com tab found on port " + str(self.port))

    async def connect(self):
        self.find_flow_target()
        self.ws = await websockets.connect(self.ws_url, max_size=50 * 1024 * 1024)

    async def send(self, method, params=None):
        self.msg_id += 1
        call_id = self.msg_id
        payload = {'id': call_id, 'method': method}
        if params is not None:
            payload['params'] = params
        await self.ws.send(json.dumps(payload))
        
        while True:
            raw = await self.ws.recv()
            data = json.loads(raw)
            if data.get('id') == call_id:
                if 'error' in data:
                    raise RuntimeError(f"CDP Error ({method}): {data['error']}")
                return data.get('result', {})
            else:
                self.events.append(data)

    async def evaluate(self, expr):
        res = await self.send('Runtime.evaluate', {
            'expression': expr,
            'returnByValue': True,
            'awaitPromise': True
        })
        return res.get('result', {}).get('value')

    async def close(self):
        if self.ws:
            await self.ws.close()

if __name__ == '__main__':
    async def main():
        client = FlowCDP()
        await client.connect()
        print(f"Connected to target: {client.target_id}")
        info = await client.evaluate('''(() => {
            return {
                url: location.href,
                title: document.title,
                localStorage: Object.keys(localStorage),
                sessionStorage: Object.keys(sessionStorage),
                scripts: Array.from(document.querySelectorAll('script')).map(s => s.src).filter(Boolean),
                appElement: document.body.innerHTML.substring(0, 500)
            };
        })()''')
        print(json.dumps(info, indent=2, ensure_ascii=False))
        await client.close()

    asyncio.run(main())

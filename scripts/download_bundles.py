import os
import re
import sys
import urllib.request

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

bundle_urls = [
    "https://www.gstatic.com/_/mss/boq-labs-ai-sandbox/_/js/k=boq-labs-ai-sandbox.AiSandboxAngularFrontend.vi.1dcxrhzrvVk.2018.O/d=1/excm=_b/ed=1/dg=0/br=1/wt=2/ujg=1/rs=APwUF7y5PfzfaJTnxZzZbSrW5M6KbUrklg/ee=Pjplud:PoEs9b;QGR0gd:Mlhmy;ScI3Yc:e7Hzgb;YIZmRd:A1yn5d;cEt90b:ws9Tlc;dowIGb:ebZ3mb/dti=1/m=_b",
    "https://www.gstatic.com/_/mss/boq-labs-ai-sandbox/_/js/k=boq-labs-ai-sandbox.AiSandboxAngularFrontend.vi.1dcxrhzrvVk.2018.O/ck=boq-labs-ai-sandbox.AiSandboxAngularFrontend.lY61RRYx2Hs.L.B1.O/d=1/exm=_b,zxMy9c/excm=_b/ed=1/br=1/wt=2/ujg=1/rs=APwUF7yDJDHoeElqUFAgCbt-QF_TkkCYtQ/ee=Pjplud:PoEs9b;QGR0gd:Mlhmy;ScI3Yc:e7Hzgb;YIZmRd:A1yn5d;cEt90b:ws9Tlc;dowIGb:ebZ3mb/dti=1/m=rZcQQd",
    "https://www.gstatic.com/_/mss/boq-labs-ai-sandbox/_/js/k=boq-labs-ai-sandbox.AiSandboxAngularFrontend.vi.1dcxrhzrvVk.2018.O/ck=boq-labs-ai-sandbox.AiSandboxAngularFrontend.lY61RRYx2Hs.L.B1.O/d=1/exm=_b/excm=_b/ed=1/br=1/wt=2/ujg=1/rs=APwUF7yDJDHoeElqUFAgCbt-QF_TkkCYtQ/ee=Pjplud:PoEs9b;QGR0gd:Mlhmy;ScI3Yc:e7Hzgb;YIZmRd:A1yn5d;cEt90b:ws9Tlc;dowIGb:ebZ3mb/dti=1/m=GK5kFd",
    "https://www.gstatic.com/_/mss/boq-labs-ai-sandbox/_/js/k=boq-labs-ai-sandbox.AiSandboxAngularFrontend.vi.1dcxrhzrvVk.2018.O/ck=boq-labs-ai-sandbox.AiSandboxAngularFrontend.lY61RRYx2Hs.L.B1.O/d=1/exm=_b/excm=_b/ed=1/br=1/wt=2/ujg=1/rs=APwUF7yDJDHoeElqUFAgCbt-QF_TkkCYtQ/ee=Pjplud:PoEs9b;QGR0gd:Mlhmy;ScI3Yc:e7Hzgb;YIZmRd:A1yn5d;cEt90b:ws9Tlc;dowIGb:ebZ3mb/dti=1/m=zxMy9c"
]

os.makedirs('flow-research/observations/bundles', exist_ok=True)

for i, url in enumerate(bundle_urls):
    name = f"bundle_{i}.js"
    path = os.path.join('flow-research/observations/bundles', name)
    if not os.path.exists(path):
        print(f"Downloading {url[:60]}... to {path}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp, open(path, 'wb') as f:
            f.write(resp.read())
        print(f"Downloaded {os.path.getsize(path)} bytes.")
    else:
        print(f"Exists: {path} ({os.path.getsize(path)} bytes)")

print("All bundles ready.")

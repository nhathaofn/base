import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with open('flow-research/observations/raw_network/project_studio.json', 'r', encoding='utf-8') as f:
    items = json.load(f)['network']

for item in items:
    url = item.get('url', '')
    if 'batchexecute' not in url:
        continue
    resp = item.get('response_body', '')
    if not resp:
        continue
    
    # Check if HTrJv is in response
    if 'HTrJv' in resp:
        for line in resp.split('\n'):
            line = line.strip()
            if line.startswith('[[') and 'HTrJv' in line:
                envelope = json.loads(line)
                for env in envelope:
                    if env[0] == 'wrb.fr' and env[1] == 'HTrJv':
                        model_data = json.loads(env[2])
                        print("=== HTrJv: GetModels Response ===")
                        print(json.dumps(model_data, indent=2, ensure_ascii=False)[:3000])
                        with open('flow-research/observations/models_raw.json', 'w', encoding='utf-8') as mf:
                            json.dump(model_data, mf, indent=2, ensure_ascii=False)
                        print("Saved full models_raw.json")

    # Check if yBhWQ is in response
    if 'yBhWQ' in resp:
        for line in resp.split('\n'):
            line = line.strip()
            if line.startswith('[[') and 'yBhWQ' in line:
                envelope = json.loads(line)
                for env in envelope:
                    if env[0] == 'wrb.fr' and env[1] == 'yBhWQ':
                        status_data = json.loads(env[2])
                        print("=== yBhWQ: ListModelStatuses Response ===")
                        print(json.dumps(status_data, indent=2, ensure_ascii=False))

    # Check if ngNC2 is in response (GetProject)
    if 'ngNC2' in resp:
        for line in resp.split('\n'):
            line = line.strip()
            if line.startswith('[[') and 'ngNC2' in line:
                envelope = json.loads(line)
                for env in envelope:
                    if env[0] == 'wrb.fr' and env[1] == 'ngNC2':
                        project_data = json.loads(env[2])
                        print("=== ngNC2: GetProject Response ===")
                        print(json.dumps(project_data, indent=2, ensure_ascii=False)[:2000])
                        with open('flow-research/observations/project_raw.json', 'w', encoding='utf-8') as pf:
                            json.dump(project_data, pf, indent=2, ensure_ascii=False)
                        print("Saved full project_raw.json")

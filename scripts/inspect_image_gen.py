import sys

with open('flow-research/observations/bundles/chunk_studio_1.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

idx = content.find('["GENERATE_IMAGE"]')
if idx != -1:
    print('GENERATE_IMAGE at:', idx)
    print(content[idx-100:idx+600].replace('\n', ' '))

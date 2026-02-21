import json

with open('model.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print('Total cells:', len(nb['cells']))
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])[:80].replace('\n', ' ')
    print(f"Cell {i} ({c['cell_type']}): {src}")

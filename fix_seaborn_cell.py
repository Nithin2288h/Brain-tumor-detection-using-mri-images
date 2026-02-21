import json
import sys

with open('model.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

last_cell = nb['cells'][-1]
src = ''.join(last_cell['source'])

if 'classification_report' in src:
    prepend = [
        "import subprocess, sys\n",
        "subprocess.run([sys.executable, '-m', 'pip', 'install', 'seaborn'], capture_output=True)\n",
        "\n"
    ]
    last_cell['source'] = prepend + last_cell['source']
    print("Updated cell with seaborn install.")
else:
    print("Classification cell not found.")

with open('model.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Saved successfully.")

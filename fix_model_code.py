import json

notebook_path = r"c:\Users\bunny\pad project\model.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Iterate through cells to find the model building cell and fix it
for cell in data['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "model = Sequential" in source and "Dense(num_classes" in source:
            print("Found model building cell. Fixing variable reference...")
            # Replace num_classes with len(classes) for robustness
            new_source = []
            for line in cell['source']:
                if "Dense(num_classes" in line:
                    new_source.append(line.replace("num_classes", "len(classes)"))
                else:
                    new_source.append(line)
            cell['source'] = new_source
            print("Fixed 'num_classes' to 'len(classes)'.")

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Notebook code fixed.")

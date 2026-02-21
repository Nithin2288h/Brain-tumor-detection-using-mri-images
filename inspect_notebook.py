import json

notebook_path = r"c:\Users\bunny\pad project\model.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, cell in enumerate(data['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        print(f"--- Cell {i} ---")
        if "train_test_split" in source:
            print("Found train_test_split")
        if "to_categorical" in source:
            print("Found to_categorical")
        if "compile" in source:
            print(f"Found compile: {source.split('compile')[1][:100]}") # Print args
        if "fit" in source:
            print("Found fit")
        if "images" in source and "append" in source:
             print("Found image loading loop")
        if "np.array" in source:
             print("Found np.array conversion")

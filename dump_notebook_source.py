import json

notebook_path = r"c:\Users\bunny\pad project\model.ipynb"
output_path = r"c:\Users\bunny\pad project\notebook_source.txt"

with open(notebook_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(output_path, 'w', encoding='utf-8') as out:
    for i, cell in enumerate(data['cells']):
        out.write(f"--- Cell {i} ({cell['cell_type']}) ---\n")
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            out.write(source)
            out.write("\n\n")
        else:
            out.write("(Markdown cell)\n\n")

print(f"Dumped notebook source to {output_path}")

import json, os
app_dir = os.path.join("D:/", "codexspace", [d for d in os.listdir("D:/codexspace") if chr(20803) in d][0])
app_path = os.path.join(app_dir, "app.py")
with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

dt_start = next(i for i, l in enumerate(lines) if "def download_template" in l)
ex_start = next(i for i, l in enumerate(lines) if "def export_excel" in l)

dt_lines = lines[dt_start:ex_start]
for i, line in enumerate(dt_lines):
    if "row=1, column=col_idx, value=h" in line:
        dt_lines[i] = line.replace("row=1", "row=2")
        break
    if "# Row 2:" in line:
        dt_lines[i] = "# Headers\n"

for i, line in enumerate(dt_lines):
    if "bio = io.BytesIO()" in line:
        dv_block = [
            "    # Category dropdown (helper column K)\n",
            "    from openpyxl.worksheet.datavalidation import DataValidation\n",
            '    cats_path = os.path.join(DATA_DIR, "categories.json")\n',
            '    if os.path.exists(cats_path):\n',
            '        with open(cats_path, "r", encoding="utf-8-sig") as f:\n',
            "            cats_data = json.load(f)\n",
            "    else:\n",
            '        cats_data = [{"key": "other", "name": "其他", "parent": None, "icon": "?"}]\n',
            '    cat_names = [x["name"] for x in cats_data]\n',
            "    for i_, name_ in enumerate(cat_names):\n",
            "        ws.cell(row=4+i_, column=11, value=name_)\n",
            '    ws.column_dimensions["K"].hidden = True\n',
            '    last_row = 3 + len(cat_names)\n',
            '    dv = DataValidation(type="list", formula1="$K$4:$K$" + str(last_row), allow_blank=True)\n',
            '    dv.add("F4:F104")\n',
            "    ws.add_data_validation(dv)\n",
            "\n",
        ]
        dt_lines = dt_lines[:i] + dv_block + dt_lines[i:]
        break

lines = lines[:dt_start] + dt_lines + lines[ex_start:]

for i, line in enumerate(lines):
    if b"\xe6\xb3\xa8\xe6\x84\x8f\xef\xbc\x9a" in line.encode() and b"\xe7\xac\xac\xe4\xb8\x80\xe8\xa1\x8c" in line.encode():
        lines[i] = '    cell = ws.cell(row=1, column=1, value="注意：第一行为说明行，不可删除。表头在第二行。从第四行开始填写数据。货架名称填实际名称（如A、B），不要加货架二字。如果不填货位（货架名称、行号、列号都留空），系统会自动分配货位。")\n'
        break

with open(app_path, "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Fix applied OK")

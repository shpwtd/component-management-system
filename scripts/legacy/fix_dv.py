import sys, os
BASE = os.path.dirname(os.path.abspath(__file__))

# Build the correct DataValidation formula
sys.path.insert(0, BASE)
from classifier import load_categories
cats = load_categories()
cat_names = [c["name"] for c in cats]
q = chr(34)
formula = q + ",".join(cat_names) + q

# Read app.py
with open(os.path.join(BASE, "app.py"), "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the column_dimensions line
insert_after = None
for i, l in enumerate(lines):
    if "ws.column_dimensions['A'].width" in l:
        insert_after = i
        break

if insert_after is not None:
    dv_lines = [
        "    # Add category dropdown for \u7c7b\u522b column\n",
        "    from openpyxl.worksheet.datavalidation import DataValidation\n",
        "    cats = load_categories()\n",
        '    cat_names = [c["name"] for c in cats]\n',
        "    dv = DataValidation(type=\"list\", formula1=" + repr(formula) + ", allow_blank=True)\n",
        "    dv.error = \"\u8bf7\u9009\u62e9\u6709\u6548\u7684\u7c7b\u522b\"\n",
        "    dv.errorTitle = \"\u7c7b\u522b\u9519\u8bef\"\n",
        "    dv.prompt = \"\u8bf7\u4ece\u4e0b\u62c9\u5217\u8868\u4e2d\u9009\u62e9\u7c7b\u522b\"\n",
        "    dv.promptTitle = \"\u7c7b\u522b\u9009\u62e9\"\n",
        "    ws.add_data_validation(dv)\n",
        '    dv.add("F3:F1048576")\n',
    ]
    for j, line in enumerate(dv_lines):
        lines.insert(insert_after + 1 + j, line)
    
    with open(os.path.join(BASE, "app.py"), "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("DataValidation code inserted successfully at line", insert_after + 1)
else:
    print("ERROR: Could not find insertion point")

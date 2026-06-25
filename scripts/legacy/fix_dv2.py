# Fix: Replace DataValidation inline formula with helper column reference
with open("app.py","r",encoding="utf-8") as f:
    c = f.read()

# Find the block to replace
start = c.index("# Add category dropdown")
end = c.index("ws.add_data_validation(dv)")
end = c.index("\n", end) + 1

new_block = """    # Add category dropdown for F column (using hidden helper column K)
    from openpyxl.worksheet.datavalidation import DataValidation
    cats = load_categories()
    cat_names = [c["name"] for c in cats]
    # Write category names to hidden helper column K
    for i, name in enumerate(cat_names):
        ws.cell(row=3+i, column=11, value=name)
    ws.column_dimensions["K"].hidden = True
    last_row = 2 + len(cat_names)
    dv = DataValidation(type="list", formula1="K3:K" + str(last_row), allow_blank=True)
    dv.add("F3:F1048576")
    ws.add_data_validation(dv)
"""

c = c[:start] + new_block + c[end:]

with open("app.py","w",encoding="utf-8") as f:
    f.write(c)
print("DataValidation fixed with helper column reference")

import sys
sys.path.insert(0, ".")
from app import app
print("OK, routes:", len(list(app.url_map.iter_rules())))

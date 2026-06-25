import os
# Read file
with open("app.py", "r", encoding="utf-8") as f:
    c = f.read()

# Fix 1: Column read - first 5 lines
c = c.replace(
    '            name = str(row[0] or "").strip()\n            model = str(row[1] or "").strip()\n            pkg = str(row[2] or "").strip()\n            specs = str(row[3] or "").strip()\n            qty_str = str(row[4] or "0").strip()',
    '            name = str(row[0] or "").strip()\n            specs = str(row[1] or "").strip()\n            pkg = str(row[2] or "").strip()\n            qty_str = str(row[3] or "0").strip()\n            min_stock_str = str(row[4] or "0").strip()\n            cat_from_excel = str(row[5] or "").strip()'
)
print("Fix 1a: Column read updated")

# Fix 2: Shelf/row/col indices
c = c.replace(
    'if len(row) > 5 and row[5] is not None: shelf_name = str(row[5]).strip()\n            if len(row) > 6 and row[6] is not None: row_num_str = str(row[6]).strip()\n            if len(row) > 7 and row[7] is not None: col_str = str(row[7]).strip()',
    'if len(row) > 6 and row[6] is not None: shelf_name = str(row[6]).strip()\n            if len(row) > 7 and row[7] is not None: row_num_str = str(row[7]).strip()\n            if len(row) > 8 and row[8] is not None: col_str = str(row[8]).strip()'
)
print("Fix 1b: Shelf/row/col indices fixed")

# Fix 3: classify call
c = c.replace(
    'cat = classify(name, model, specs, pkg)',
    'cat = cat_from_excel if cat_from_excel else classify(name, "", specs, pkg)'
)
print("Fix 1c: classify call fixed")

# Fix 4: Component list sort
c = c.replace(
    '    return render_template("component_list.html", components=components, shelf_map=shelf_map,',
    '    components.sort(key=lambda c: (c.get("shelf_id") or 9999, c.get("row") or 9999, c.get("col") or 9999))\n    return render_template("component_list.html", components=components, shelf_map=shelf_map,'
)
print("Fix 2: Component list sort added")

# Fix 5: Import description in import.html
with open("templates/import.html", "r", encoding="utf-8") as f:
    imp = f.read()
imp = imp.replace(
    "先下载模板填写数据，然后上传。模板包含：名称、规格参数、封装、数量、最低库存、类别、货架名称、行号、列号。不填货位信息则自动分配空货位",
    "先下载模板填写数据，然后上传。模板第1行为说明（不可删除），第2行为表头，从第3行开始填写数据。货架名称填实际名称（如A、B），不加货架二字。不填货位信息则自动分配空货位"
)
with open("templates/import.html", "w", encoding="utf-8") as f:
    f.write(imp)
print("Fix 3: Import description updated")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(c)
print("All fixes applied!")

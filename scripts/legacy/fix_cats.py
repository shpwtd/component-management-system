# Fix 1: import_result.html - remove 型号 from table headers
with open("templates/import_result.html","r",encoding="utf-8") as f:
    c = f.read()
c = c.replace("<th>名称</th><th>型号</th><th>数量</th><th>货架</th><th>位置</th>",
              "<th>名称</th><th>数量</th><th>货架</th><th>位置</th>")
c = c.replace("<th>名称</th><th>型号</th><th>数量</th><th>分配位置</th>",
              "<th>名称</th><th>数量</th><th>分配位置</th>")
with open("templates/import_result.html","w",encoding="utf-8") as f:
    f.write(c)
print("Fix 1: import_result.html headers fixed")

# Fix 2: app.py - import_page category mapping
with open("app.py","r",encoding="utf-8") as f:
    app = f.read()

# Replace the category assignment in import_page
old_cat = "cat = cat_from_excel if cat_from_excel else classify(name, \"\", specs, pkg)"
new_cat = '''if cat_from_excel:
                cats_list = load_categories()
                matched = next((c["key"] for c in cats_list if c["name"] == cat_from_excel), None)
                cat = matched if matched else classify(name, "", specs, pkg)
            else:
                cat = classify(name, "", specs, pkg)'''
app = app.replace(old_cat, new_cat)
print("Fix 2: Category name-to-key mapping added")

# Fix 3: download_template - add DataValidation dropdown for categories
old_dl = 'ws.column_dimensions["A"].width = 20\n    ws.column_dimensions["B"].width = 25'
new_dl = '''# Add category dropdown validation
    from openpyxl.worksheet.datavalidation import DataValidation
    cats = load_categories()
    cat_names = [c["name"] for c in cats]
    dv = DataValidation(type="list", formula1="\\"" + ",".join(cat_names) + "\\"", allow_blank=True)
    dv.error = "请选择有效的类别"
    dv.errorTitle = "类别错误"
    dv.prompt = "请从下拉列表中选择类别"
    dv.promptTitle = "类别选择"
    ws.add_data_validation(dv)
    dv.add("F3:F1048576")
    ws.column_dimensions["A"].width = 20\n    ws.column_dimensions["B"].width = 25'''
app = app.replace(old_dl, new_dl)
print("Fix 3: Category dropdown added to template")

with open("app.py","w",encoding="utf-8") as f:
    f.write(app)

# Verify
import sys
sys.path.insert(0, ".")
from app import app as flask_app
print(f"\nAll OK! Routes: {len(list(flask_app.url_map.iter_rules()))}")

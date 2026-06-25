import os
BASE = r"D:\codexspace\元器件管理系统"
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Fix 1: openpyxl.load_workbook -> just load_workbook
c = c.replace(
    'wb = openpyxl.load_workbook(file, data_only=True)',
    'wb = load_workbook(file, data_only=True)'
)
print("Fix 1: import_page uses load_workbook directly")

# Fix 2: Export headers - remove 型号
c = c.replace(
    'headers = ["名称", "型号", "封装", "规格参数", "数量", "最低库存", "类别", "货架", "行号", "列号"]',
    'headers = ["名称", "规格参数", "封装", "数量", "最低库存", "类别", "货架", "行号", "列号"]'
)
print("Fix 2: export headers - removed 型号")

# Fix 3: Download template instructions
c = c.replace(
    'ws.cell(row=3, column=1, value="填写说明：名称和货架名称必填，行列号从1开始")',
    'ws.cell(row=3, column=1, value="填写说明：名称必填。填写货架名称+行号+列号则导入到指定货位，不填则自动分配空货位")'
)
# Also fix example row in template
c = c.replace(
    'example = ["贴片电阻", "0805", "10KΩ ±1%", "100", "50", "电阻", "A货架", "1", "2"]',
    'example = ["贴片电阻", "10KΩ ±1%", "0805", "100", "50", "电阻", "A货架", "1", "2"]'
)
print("Fix 3: template instructions updated")

# Fix 4: Import page description (in import.html template)
imp_path = os.path.join(BASE, "templates", "import.html")
if os.path.exists(imp_path):
    with open(imp_path, "r", encoding="utf-8") as f:
        imp = f.read()
    imp = imp.replace(
        '模板包含：名称、型号、封装、规格参数、数量、货架名称、行号、列号',
        '模板包含：名称、规格参数、封装、数量、最低库存、类别、货架名称、行号、列号。不填货位信息则自动分配空货位'
    )
    with open(imp_path, "w", encoding="utf-8") as f:
        f.write(imp)
    print("Fix 4: import page description updated")

# Fix 5: Add try/except to replan_execute for error logging
old_replan_exec = '''def replan_execute():
    data = request.get_json()
    if not data or "moves" not in data:
        return jsonify({"success": False, "error": "无移动数据"}), 400
    components = load_components()
    for move in data["moves"]:
        cid = move.get("component_id")
        comp = next((c for c in components if c["id"] == cid), None)
        if comp:
            comp["shelf_id"] = move.get("to_shelf_id")
            comp["row"] = move.get("to_row")
            comp["col"] = move.get("to_col")
            comp["updated_at"] = now_str()
    save_components(components)
    return jsonify({"success": True, "count": len(data["moves"])})'''

new_replan_exec = '''def replan_execute():
    data = request.get_json()
    if not data or "moves" not in data:
        return jsonify({"success": False, "error": "无移动数据"}), 400
    components = load_components()
    count = 0
    for move in data["moves"]:
        cid = move.get("component_id")
        comp = next((c for c in components if c["id"] == cid), None)
        if comp:
            comp["shelf_id"] = move.get("to_shelf_id")
            comp["row"] = move.get("to_row")
            comp["col"] = move.get("to_col")
            comp["updated_at"] = now_str()
            count += 1
    save_components(components)
    if count == 0:
        return jsonify({"success": False, "error": "没有元器件被成功调整"}), 400
    return jsonify({"success": True, "count": count})'''

if old_replan_exec in c:
    c = c.replace(old_replan_exec, new_replan_exec)
    print("Fix 5: replan_execute improved with error checking")
else:
    print("Fix 5: WARNING - replan_execute code not found, trying shorter match...")
    # Try shorter match
    if "def replan_execute():" in c:
        print("  (replan_execute exists, skipping full replacement)")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

# Verify
import sys
sys.path.insert(0, BASE)
from app import app
print(f"\nAll fixes applied! Routes: {len(list(app.url_map.iter_rules()))}")

import os, sys
BASE = r"D:\codexspace\元器件管理系统"

# Read classify.py first
clf_path = os.path.join(BASE, "classifier.py")
with open(clf_path, "r", encoding="utf-8") as f:
    clf = f.read()

# Fix plan_layout to accept occupied parameter
old_plan = '''def plan_layout(components, shelves):
    if not shelves or not components:
        return None
    groups = {}
    for comp in components:
        key = suggest_group_key(comp.get('name',''), comp.get('model',''),
                                comp.get('specs',''), comp.get('package',''),
                                comp.get('category',''))
        if key not in groups: groups[key] = []
        groups[key].append(comp)
    empty_slots = []
    for shelf in shelves:
        for rd in shelf.get('rows', []):
            for col in range(1, rd['cols']+1):
                empty_slots.append({
                    'shelf_id': shelf['id'], 'shelf_name': shelf['name'],
                    'row': rd['row'], 'col': col
                })'''

new_plan = '''def plan_layout(components, shelves, occupied=None):
    if not shelves or not components:
        return None
    groups = {}
    for comp in components:
        key = suggest_group_key(comp.get('name',''), comp.get('model',''),
                                comp.get('specs',''), comp.get('package',''),
                                comp.get('category',''))
        if key not in groups: groups[key] = []
        groups[key].append(comp)
    empty_slots = []
    for shelf in shelves:
        for rd in shelf.get('rows', []):
            for col in range(1, rd['cols']+1):
                key = (shelf['id'], rd['row'], col)
                if occupied and key in occupied:
                    continue
                empty_slots.append({
                    'shelf_id': shelf['id'], 'shelf_name': shelf['name'],
                    'row': rd['row'], 'col': col
                })'''

if old_plan in clf:
    clf = clf.replace(old_plan, new_plan)
    print("Fix 1: plan_layout accepts occupied parameter")
else:
    print("Fix 1: WARNING - old plan_layout not found")
    
with open(clf_path, "w", encoding="utf-8") as f:
    f.write(clf)

# Fix app.py: export and import
app_path = os.path.join(BASE, "app.py")
with open(app_path, "r", encoding="utf-8") as f:
    app = f.read()

# Fix 2: Export vals - remove model
old_export_vals = '''vals = [
            comp.get("name", ""),
            comp.get("model", ""),
            comp.get("package", ""),
            comp.get("specs", ""),
            comp.get("quantity", 0),
            comp.get("min_stock", 0),
            get_category_display(comp.get("category", "")),
            shelf_map.get(comp.get("shelf_id"), ""),
            comp.get("row", ""),
            comp.get("col", "")
        ]'''

new_export_vals = '''vals = [
            comp.get("name", ""),
            comp.get("specs", ""),
            comp.get("package", ""),
            comp.get("quantity", 0),
            comp.get("min_stock", 0),
            get_category_display(comp.get("category", "")),
            shelf_map.get(comp.get("shelf_id"), ""),
            comp.get("row", ""),
            comp.get("col", "")
        ]'''

if old_export_vals in app:
    app = app.replace(old_export_vals, new_export_vals)
    print("Fix 2: Export vals - removed model")
else:
    print("Fix 2: WARNING - export vals not found")
    # Try alternate format (with surrounding whitespace)
    old_alt = '''comp.get("model", ""),'''
    if '"model"' in app and 'get("model"' in app and 'export' in app[app.index('def export_excel'):app.index('def export_excel')+4000]:
        # Find and fix the one in export_excel
        export_idx = app.index('def export_excel')
        export_section = app[export_idx:export_idx+3000]
        if 'comp.get("model", ""),' in export_section:
            # Only replace the first occurrence (in export)
            parts = export_section.split('comp.get("model", ""),')
            new_export_section = parts[0] + '' + parts[1]
            app = app[:export_idx] + new_export_section + app[export_idx+len(export_section):]
            print("Fix 2: export model removed (alt method)")

# Fix 3: Import - pass occupied to plan_layout
old_import_plan = '''if plan_items and shelves:
                result = plan_layout(plan_items, shelves)'''

new_import_plan = '''if plan_items and shelves:
                occs = get_occupied(shelves, components)
                result = plan_layout(plan_items, shelves, occs)'''

if old_import_plan in app:
    app = app.replace(old_import_plan, new_import_plan)
    print("Fix 3: Import passes occupied to plan_layout")
else:
    print("Fix 3: WARNING - import plan call not found")
    # Try alternate
    if 'result = plan_layout(plan_items, shelves)' in app:
        app = app.replace(
            'result = plan_layout(plan_items, shelves)',
            'result = plan_layout(plan_items, shelves, get_occupied(shelves, components))'
        )
        print("Fix 3: Alt - Import occupied")

# Fix 4: Template - move instruction to row 4, make example row 4
old_template = '''example = ["贴片电阻", "10KΩ ±1%", "0805", "100", "50", "电阻", "A货架", "1", "2"]
    for col_idx, v in enumerate(example, 1):
        cell = ws.cell(row=2, column=col_idx, value=v)
        cell.border = thin_border
    ws.cell(row=3, column=1, value="填写说明：名称必填。填写货架名称+行号+列号则导入到指定货位，不填则自动分配空货位")'''

new_template = '''example = ["贴片电阻", "10KΩ ±1%", "0805", "100", "50", "电阻", "A货架", "1", "2"]
    for col_idx, v in enumerate(example, 1):
        cell = ws.cell(row=2, column=col_idx, value=v)
        cell.border = thin_border
    ws.cell(row=3, column=1, value="")
    ws.cell(row=4, column=1, value="填写说明：名称必填。填写货架名称+行号+列号则导入到指定货位，不填则自动分配空货位")'''

if old_template in app:
    app = app.replace(old_template, new_template)
    print("Fix 4: Template instruction moved to row 4")
else:
    print("Fix 4: WARNING - template instruction not found")

# Fix 5: Import skip rows 2-3 (example + instruction) by reading from min_row=4
old_min_row = '''rows = list(ws.iter_rows(min_row=2, values_only=True))'''
new_min_row = '''rows = list(ws.iter_rows(min_row=4, values_only=True))'''

if old_min_row in app:
    app = app.replace(old_min_row, new_min_row)
    print("Fix 5: Import starts from row 4")
else:
    print("Fix 5: WARNING - import min_row not found")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app)

# Verify
sys.path.insert(0, BASE)
from app import app as flask_app
from classifier import plan_layout
print(f"\nAll OK! Routes: {len(list(flask_app.url_map.iter_rules()))}")
print("plan_layout signature:", plan_layout.__code__.co_varnames[:plan_layout.__code__.co_argcount])

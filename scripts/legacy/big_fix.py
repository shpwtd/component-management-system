import sys, os
BASE = "."

# ─── STEP 1: Simple app.py fixes ─────────────────────────
with open(os.path.join(BASE, "app.py"), "r", encoding="utf-8") as f:
    app = f.read()

# 1a. DataValidation range
app = app.replace('dv.add("F3:F1048576")', 'dv.add("F3:F100")')
print("1a: DV range F3:F100")

# 1b. Skip empty names silently
app = app.replace(
    '            if not name:\n                error_items.append({"row": row_idx, "reason": "\u540d\u79f0\u4e3a\u7a7a"})\n                continue',
    '            if not name:\n                continue'
)
print("1b: Empty rows skipped silently")

# 1c. Add shelf_name to direct_items
app = app.replace(
    '"shelf_id": shelf["id"], "row": rn, "col": cn, "category": cat,',
    '"shelf_id": shelf["id"], "shelf_name": shelf["name"], "row": rn, "col": cn, "category": cat,'
)
print("1c: shelf_name added to direct_items")

# 1d. Add locked field handling
# In component_add
app = app.replace(
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n            comp["category"] = request.form.get("category", "other")',
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n        comp["locked"] = 1 if request.form.get("locked") else 0\n            comp["category"] = request.form.get("category", "other")'
)
# Fix: the above might have wrong indentation. Let me check.
# Actually, in component_add, the line is indented differently than component_edit.
# Let me just add the locked field in both functions separately.

# For component_add (deeper indent):
app = app.replace(
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n            comp["category"]',
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n            comp["locked"] = 1 if request.form.get("locked") else 0\n            comp["category"]'
)

# For component_edit (less indent because it has old_qty handling):
app = app.replace(
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n        comp["category"]',
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n        comp["locked"] = 1 if request.form.get("locked") else 0\n        comp["category"]'
)
print("1d: locked field added to component_add and component_edit")

with open(os.path.join(BASE, "app.py"), "w", encoding="utf-8") as f:
    f.write(app)

# ─── STEP 2: Template updates ───────────────────────────
# 2a. import_result.html: shelf_id -> shelf_name
ir_path = os.path.join(BASE, "templates", "import_result.html")
with open(ir_path, "r", encoding="utf-8") as f:
    ir = f.read()
ir = ir.replace("{{ s.shelf_id }}", "{{ s.shelf_name }}")
with open(ir_path, "w", encoding="utf-8") as f:
    f.write(ir)
print("2a: import_result shelf_id -> shelf_name")

# 2b. component_form.html: add locked checkbox
cf_path = os.path.join(BASE, "templates", "component_form.html")
with open(cf_path, "r", encoding="utf-8") as f:
    cf = f.read()
locked_html = """
<div class="form-group">
<label>库位锁定</label>
<div>
<label style="font-weight:normal;font-size:14px">
<input type="checkbox" name="locked" value="1" {{ "checked" if comp and comp.locked else "" }}>
 锁定此元器件位置（重规划时不会被调整）
</label>
</div>
</div>
"""
cf = cf.replace('<div class="form-group">\n<label>最低库存阈值</label>', locked_html + '<div class="form-group">\n<label>最低库存阈值</label>')
with open(cf_path, "w", encoding="utf-8") as f:
    f.write(cf)
print("2b: locked checkbox added to component_form")

# 2c. replan.html: show locked count
rp_path = os.path.join(BASE, "templates", "replan.html")
with open(rp_path, "r", encoding="utf-8") as f:
    rp = f.read()
rp = rp.replace(
    '<div class="alert alert-info">共 {{ plan|length }} 个元器件需要调整位置</div>',
    '<div class="alert alert-info">共 {{ plan|length }} 个元器件需要调整位置{% if locked_count %}（{{ locked_count }} 个已被锁定跳过）{% endif %}</div>'
)
with open(rp_path, "w", encoding="utf-8") as f:
    f.write(rp)
print("2c: replan.html locked count display")

# ─── STEP 3: Rewrite replan algorithm ────────────────────
# Read the current app.py again since we modified it
with open(os.path.join(BASE, "app.py"), "r", encoding="utf-8") as f:
    app = f.read()

# Find the replan_page function and replace it
old_start = app.index("def replan_page():")
old_end_text = "def replan_execute("
old_end = app.index(old_end_text, old_start)

new_replan = """def replan_page():
    shelves = load_shelves()
    all_components = load_components()
    components = [c for c in all_components if c.get("shelf_id") and not c.get("locked")]
    locked_list = [c for c in all_components if c.get("shelf_id") and c.get("locked")]
    occ = get_occupied(shelves, all_components)
    if not components:
        flash("没有可调整的元器件（" + str(len(locked_list)) + "个已被锁定）", "info")
        return render_template("replan.html", shelves=shelves, components=all_components, plan=None,
                               locked_count=len(locked_list), get_cat=get_category_display, cats=get_category_list())
    # Group by (category, package, specs)
    groups = {}
    for c in components:
        key = suggest_group_key(c.get("name",""), c.get("model",""),
                                c.get("specs",""), c.get("package",""),
                                c.get("category",""))
        if key not in groups: groups[key] = []
        groups[key].append(c)
    # Build col_count -> rows map
    col_rows = {}
    for s in shelves:
        for rd in s.get("rows", []):
            cc = rd["cols"]
            if cc not in col_rows: col_rows[cc] = []
            col_rows[cc].append({"shelf_id": s["id"], "shelf_name": s["name"], "row": rd["row"], "cols": cc})
    plan_items = []
    moved = set()
    reserved_slots = set()  # Margin slots, not for reassignment
    for gk, comps in sorted(groups.items(), key=lambda x: (-len(x[1]), x[0])):
        if not comps: continue
        sample = comps[0]
        target_cc = None
        for s in shelves:
            match = [rd for rd in s.get("rows", []) if rd["row"] == sample.get("row") and s["id"] == sample.get("shelf_id")]
            if match: target_cc = match[0]["cols"]; break
        if not target_cc or target_cc not in col_rows: continue
        # Score rows: prefer rows with same-group items, then most available slots, avoid full rows
        scored = []
        for ri in col_rows[target_cc]:
            g_in = sum(1 for c in comps if not c.get("locked") and c.get("shelf_id")==ri["shelf_id"] and c.get("row")==ri["row"])
            available = 0
            for col in range(1, ri["cols"]+1):
                key = (ri["shelf_id"], ri["row"], col)
                if key not in occ and key not in reserved_slots:
                    available += 1
            # Leave 1 slot margin: subtract 1 from effective available if >0
            effective = max(0, available - 1) if available > 0 else 0
            scored.append((ri, g_in, effective, available))
        scored.sort(key=lambda x: (-x[1], -x[2]))
        target = scored[0][0]
        margin_taken = False
        for c in comps:
            if c["id"] in moved: continue
            cs, cr, ccol = c.get("shelf_id"), c.get("row"), c.get("col")
            # Already in target with company -> skip
            if cs == target["shelf_id"] and cr == target["row"] and len(comps) > 1:
                has_company = any(o["id"]!=c["id"] and o.get("shelf_id")==cs and o.get("row")==cr for o in comps if not o.get("locked"))
                if has_company: moved.add(c["id"]); continue
            # Find empty slot (skip the last one for margin)
            tc = None
            cols_in_row = target["cols"]
            for col in range(1, cols_in_row+1):
                key = (target["shelf_id"], target["row"], col)
                if key not in occ and key not in reserved_slots:
                    # Reserve last slot as margin if not already taken
                    if not margin_taken and available > 0:
                        # Check if this is the last available slot
                        remaining = sum(1 for c2 in range(col+1, cols_in_row+1) if (target["shelf_id"], target["row"], c2) not in occ and (target["shelf_id"], target["row"], c2) not in reserved_slots)
                        if remaining == 0:
                            reserved_slots.add(key)
                            margin_taken = True
                            continue
                    tc = col
                    break
            if not tc: continue
            plan_items.append({
                "component_id": c["id"], "component_name": c.get("name",""),
                "from_shelf": next((s["name"] for s in shelves if s["id"]==cs), ""),
                "from_row": cr, "from_col": ccol,
                "to_shelf": target["shelf_name"], "to_row": target["row"], "to_col": tc,
                "to_shelf_id": target["shelf_id"], "group": gk, "cols": target_cc
            })
            moved.add(c["id"])
            occ[(target["shelf_id"], target["row"], tc)] = c
    # Sort plan items by group, then by target shelf/row/col
    plan_items.sort(key=lambda p: (p["group"], p["to_shelf"], p["to_row"], p["to_col"]))
    return render_template("replan.html", shelves=shelves, components=all_components, plan=plan_items,
                           locked_count=len(locked_list), get_cat=get_category_display, cats=get_category_list())
"""

app = app[:old_start] + new_replan + app[old_end:]

with open(os.path.join(BASE, "app.py"), "w", encoding="utf-8") as f:
    f.write(app)
print("3: Replan algorithm rewritten with locking + margin")

# ─── STEP 4: classifier.py plan_layout margin ───────────
with open(os.path.join(BASE, "classifier.py"), "r", encoding="utf-8") as f:
    clf = f.read()

old_assign = """    assignments = []
    idx = 0
    for gk in sorted(groups.keys()):
        for comp in groups[gk]:
            if idx >= len(empty_slots): break
            slot = empty_slots[idx]
            assignments.append({
                'component': comp, 'shelf_id': slot['shelf_id'],
                'shelf_name': slot['shelf_name'], 'row': slot['row'],
                'col': slot['col'], 'group': gk
            })
            idx += 1"""

new_assign = """    assignments = []
    idx = 0
    margin_per_group = {}
    for gk in sorted(groups.keys()):
        margin_per_group[gk] = False
        for comp in groups[gk]:
            if idx >= len(empty_slots): break
            slot = empty_slots[idx]
            # Leave 1 slot margin per group per row
            if not margin_per_group[gk]:
                # Check if this is the last available slot in this row
                remaining = sum(1 for j in range(idx+1, len(empty_slots)) if empty_slots[j]["shelf_id"]==slot["shelf_id"] and empty_slots[j]["row"]==slot["row"])
                if remaining == 0 and len([a for a in assignments if a["shelf_id"]==slot["shelf_id"] and a["row"]==slot["row"]]) > 0:
                    idx += 1
                    continue
            assignments.append({
                'component': comp, 'shelf_id': slot['shelf_id'],
                'shelf_name': slot['shelf_name'], 'row': slot['row'],
                'col': slot['col'], 'group': gk
            })
            idx += 1"""

if old_assign in clf:
    clf = clf.replace(old_assign, new_assign)
    print("4: plan_layout margin added")
else:
    print("4: WARNING - old assignment block not found in classifier.py")

with open(os.path.join(BASE, "classifier.py"), "w", encoding="utf-8") as f:
    f.write(clf)

# ─── Verify ─────────────────────────────────────────────
sys.path.insert(0, BASE)
from app import app as flask_app
print(f"\nAll done! Routes: {len(list(flask_app.url_map.iter_rules()))}")

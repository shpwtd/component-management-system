import os, sys
BASE = "."

# Read current app.py
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    app = f.read()

# ─── Fix 1: iter_rows max_col=9 ──────────────────────
app = app.replace("iter_rows(min_row=3, values_only=True)", "iter_rows(min_row=3, max_col=9, values_only=True)")
print("1: iter_rows max_col=9")

# ─── Fix 2: Export sorting ──────────────────────────
old_export = 'components = load_components()\n    shelves = load_shelves()\n    shelf_map = {s["id"]: s["name"] for s in shelves}\n    wb = Workbook()'
new_export = 'components = load_components()\n    components.sort(key=lambda c: (c.get("shelf_id") or 9999, c.get("row") or 9999, c.get("col") or 9999))\n    shelves = load_shelves()\n    shelf_map = {s["id"]: s["name"] for s in shelves}\n    wb = Workbook()'
app = app.replace(old_export, new_export)
print("2: Export sorting added")

# ─── Fix 3: Logging config ─────────────────────────
app = app.replace(
    'from classifier import classify, detect_package, get_category_list, get_category_display, plan_layout, load_categories, suggest_group_key',
    'import logging\nlogging.basicConfig(filename="data/error.log", level=logging.ERROR, format="%(asctime)s %(levelname)s: %(message)s", encoding="utf-8")\nfrom classifier import classify, detect_package, get_category_list, get_category_display, plan_layout, load_categories, suggest_group_key'
)
print("3: Logging configured")

# ─── Fix 4: toggle_lock route ──────────────────────
toggle_route = '\n\n@app.route("/components/<int:cid>/toggle_lock", methods=["POST"])\ndef component_toggle_lock(cid):\n    components = load_components()\n    comp = next((c for c in components if c["id"] == cid), None)\n    if not comp:\n        return jsonify({"success": False, "error": "\u5143\u5668\u4ef6\u4e0d\u5b58\u5728"}), 404\n    comp["locked"] = 0 if comp.get("locked") else 1\n    comp["updated_at"] = now_str()\n    save_components(components)\n    return jsonify({"success": True, "locked": comp["locked"]})'
app = app.replace('@app.route("/uploads/<filename>")', toggle_route + '\n@app.route("/uploads/<filename>")')
print("4: toggle_lock route added")

# ─── Fix 5: replan_execute decorator ────────────────
app = app.replace("def replan_execute():", '@app.route("/replan/execute", methods=["POST"])\ndef replan_execute():')
print("5: replan_execute decorator restored")

# ─── Fix 6: Empty names skip in import ──────────────
app = app.replace(
    'if not name:\n                error_items.append({"row": row_idx, "reason": "\u540d\u79f0\u4e3a\u7a7a"})\n                continue',
    'if not name:\n                continue'
)
print("6: Empty rows skipped silently")

# ─── Fix 7: shelf_name in direct_items ─────────────
app = app.replace(
    '"shelf_id": shelf["id"], "row": rn, "col": cn, "category": cat',
    '"shelf_id": shelf["id"], "shelf_name": shelf["name"], "row": rn, "col": cn, "category": cat'
)
print("7: shelf_name added to direct_items")

# ─── Fix 8: locked field in component_add/edit ─────
app = app.replace(
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n            comp["category"]',
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n            comp["locked"] = 1 if request.form.get("locked") else 0\n            comp["category"]'
)
app = app.replace(
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n        comp["category"]',
    'comp["min_stock"] = int(request.form.get("min_stock", 0))\n        comp["locked"] = 1 if request.form.get("locked") else 0\n        comp["category"]'
)
print("8: locked field added")

with open(path, "w", encoding="utf-8") as f:
    f.write(app)

# ─── Template fixes ──────────────────────────────────
# import_result.html: shelf_id -> shelf_name
p = os.path.join(BASE, "templates", "import_result.html")
with open(p, "r", encoding="utf-8") as f:
    t = f.read()
t = t.replace("{{ s.shelf_id }}", "{{ s.shelf_name }}")
with open(p, "w", encoding="utf-8") as f:
    f.write(t)
print("T1: import_result shelf_name")

# component_form.html: locked checkbox
p = os.path.join(BASE, "templates", "component_form.html")
with open(p, "r", encoding="utf-8") as f:
    t = f.read()
locked_html = '\n<div class="form-group">\n<label>\u5e93\u4f4d\u9501\u5b9a</label>\n<div>\n<label style="font-weight:normal;font-size:14px">\n<input type="checkbox" name="locked" value="1" {{ "checked" if comp and comp.locked else "" }}>\n \u9501\u5b9a\u6b64\u5143\u5668\u4ef6\u4f4d\u7f6e\uff08\u91cd\u89c4\u5212\u65f6\u4e0d\u4f1a\u88ab\u8c03\u6574\uff09\n</label>\n</div>\n</div>\n'
t = t.replace('<div class="form-group">\n<label>\u6700\u4f4e\u5e93\u5b58\u9608\u503c</label>', locked_html + '<div class="form-group">\n<label>\u6700\u4f4e\u5e93\u5b58\u9608\u503c</label>')
with open(p, "w", encoding="utf-8") as f:
    f.write(t)
print("T2: locked checkbox added")

# replan.html: locked count display
p = os.path.join(BASE, "templates", "replan.html")
with open(p, "r", encoding="utf-8") as f:
    t = f.read()
t = t.replace(
    '<div class="alert alert-info">\u5171 {{ plan|length }} \u4e2a\u5143\u5668\u4ef6\u9700\u8981\u8c03\u6574\u4f4d\u7f6e</div>',
    '<div class="alert alert-info">\u5171 {{ plan|length }} \u4e2a\u5143\u5668\u4ef6\u9700\u8981\u8c03\u6574\u4f4d\u7f6e{% if locked_count %}\uff08{{ locked_count }} \u4e2a\u5df2\u88ab\u9501\u5b9a\u8df3\u8fc7\uff09{% endif %}</div>'
)
with open(p, "w", encoding="utf-8") as f:
    f.write(t)
print("T3: replan locked count")

# component_list.html: lock column
p = os.path.join(BASE, "templates", "component_list.html")
with open(p, "r", encoding="utf-8") as f:
    t = f.read()
if "\u9501\u5b9a</th>" not in t:
    t = t.replace("<th>\u64cd\u4f5c</th>", "<th>\u9501\u5b9a</th><th>\u64cd\u4f5c</th>")
    t = t.replace(
        '<td style="white-space:nowrap">\n<a href="/components/{{ c.id }}" class="btn btn-sm btn-secondary">\u67e5\u770b</a>',
        '<td><span class="lock-toggle" data-cid="{{ c.id }}" data-locked="{{ 1 if c.locked else 0 }}" onclick="toggleLock(this)">{{ "\\U0001F512" if c.locked else "\\U0001F513" }}</span></td>\n<td style="white-space:nowrap">\n<a href="/components/{{ c.id }}" class="btn btn-sm btn-secondary">\u67e5\u770b</a>'
    )
    # Add JS
    t = t.replace("{% endblock %}", '\n<script>\nfunction toggleLock(el) {\n    var cid = el.getAttribute("data-cid");\n    fetch("/components/" + cid + "/toggle_lock", {method: "POST"})\n        .then(function(r) { return r.json(); })\n        .then(function(data) {\n            if (data.success) {\n                el.textContent = data.locked ? "\\U0001F512" : "\\U0001F513";\n                el.setAttribute("data-locked", data.locked ? "1" : "0");\n            }\n        });\n}\n</script>\n{% endblock %}')
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    print("T4: component_list lock column added")
else:
    print("T4: lock column already present")

# CSS: lock-toggle
css_path = os.path.join(BASE, "static", "style.css")
with open(css_path, "a", encoding="utf-8") as f:
    f.write('\n.lock-toggle { cursor: pointer; font-size: 18px; user-select: none; display:inline-block; padding:2px 4px; }\n.lock-toggle:hover { background:#dfe6e9; border-radius:4px; }\n')
print("T5: CSS added")

# Verify
sys.path.insert(0, BASE)
from app import app as fa
print(f"\nAll done! Routes: {len(list(fa.url_map.iter_rules()))}")

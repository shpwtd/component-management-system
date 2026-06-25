import os, sys
BASE = "."
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    app = f.read()

# 1. Add logging
app = app.replace(
    "from classifier import classify, detect_package, get_category_list, get_category_display, plan_layout",
    'import logging\nlogging.basicConfig(filename="data/error.log", level=logging.ERROR, format="%(asctime)s %(levelname)s: %(message)s", encoding="utf-8")\nfrom classifier import classify, detect_package, get_category_list, get_category_display, plan_layout'
)

# 2. Add toggle_lock route before uploads
toggle = '''
@app.route("/components/<int:cid>/toggle_lock", methods=["POST"])
def component_toggle_lock(cid):
    components = __import__("app", fromlist=[""]).load_components() if False else __import__("json").load(open("data/components.json","r",encoding="utf-8"))
    # Error: cannot use app module. Use direct file access instead.
    import json
    try:
        comps = json.load(open("data/components.json","r",encoding="utf-8"))
        comp = next((c for c in comps if c["id"] == cid), None)
        if not comp:
            return {"success": False, "error": "not found"}, 404
        comp["locked"] = 0 if comp.get("locked") else 1
        from datetime import datetime
        comp["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json.dump(comps, open("data/components.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
        return {"success": True, "locked": comp["locked"]}
    except Exception as e:
        return {"success": False, "error": str(e)}, 500
'''
app = app.replace('@app.route("/uploads/<filename>")', toggle + '\n@app.route("/uploads/<filename>")')

# 3. Add categories route before if __name__
cat_route = """
@app.route("/categories", methods=["GET", "POST"])
def categories_page():
    cats = __import__("classifier").load_categories()
    tree = __import__("classifier").get_category_tree()
    if __import__("flask").request.method == "POST":
        key = __import__("flask").request.form.get("key", "").strip()
        name = __import__("flask").request.form.get("name", "").strip()
        parent = __import__("flask").request.form.get("parent", "").strip() or None
        if not key or not name:
            __import__("flask").flash("\u8bf7\u586b\u5199\u7c7b\u522b\u6807\u8bc6\u548c\u540d\u79f0", "danger")
            return __import__("flask").render_template("categories.html", cat_list=cats, tree=tree)
        key = __import__("re").sub(r"[^a-z0-9_]", "", key.lower())
        if not key:
            __import__("flask").flash("\u7c7b\u522b\u6807\u8bc6\u53ea\u80fd\u5305\u542b\u5b57\u6bcd\u3001\u6570\u5b57\u548c\u4e0b\u5212\u7ebf", "danger")
            return __import__("flask").render_template("categories.html", cat_list=cats, tree=tree)
        if any(c["key"] == key for c in cats):
            __import__("flask").flash(f"\u7c7b\u522b\u6807\u8bc6\u300c{key}\u300d\u5df2\u5b58\u5728", "danger")
            return __import__("flask").render_template("categories.html", cat_list=cats, tree=tree)
        cats.append({"key": key, "name": name, "parent": parent, "icon": "?"})
        __import__("json").dump(cats, open("data/categories.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
        __import__("flask").flash(f"\u7c7b\u522b\u300c{name}\u300d\u5df2\u6dfb\u52a0", "success")
        return __import__("flask").redirect("/categories")
    return __import__("flask").render_template("categories.html", cat_list=cats, tree=tree)

@app.route("/categories/<cat_key>/delete", methods=["POST"])
def category_delete(cat_key):
    import json
    cats = __import__("classifier").load_categories()
    if cat_key in ("other",):
        __import__("flask").flash("\u4e0d\u80fd\u5220\u9664\u300c\u5176\u4ed6\u300d\u7c7b\u522b", "danger")
        return __import__("flask").redirect("/categories")
    cat = next((c for c in cats if c["key"] == cat_key), None)
    if not cat:
        __import__("flask").flash("\u7c7b\u522b\u4e0d\u5b58\u5728", "danger")
        return __import__("flask").redirect("/categories")
    cats[:] = [c for c in cats if c["key"] != cat_key]
    comps = json.load(open("data/components.json","r",encoding="utf-8"))
    for comp in comps:
        if comp.get("category") == cat_key:
            comp["category"] = "other"
    json.dump(comps, open("data/components.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(cats, open("data/categories.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    __import__("flask").flash(f"\u7c7b\u522b\u300c{cat['name']}\u300d\u5df2\u5220\u9664", "success")
    return __import__("flask").redirect("/categories")
"""
app = app.replace('if __name__ == "__main__":', cat_route + '\nif __name__ == "__main__":')

# 4. Fix export headers
app = app.replace(
    'headers = ["名称", "型号", "封装", "规格参数", "数量", "最低库存", "类别", "货架", "行号", "列号"]',
    'headers = ["名称", "规格参数", "封装", "数量", "最低库存", "类别", "货架", "行号", "列号"]'
)
# 5. Fix template headers
app = app.replace(
    'headers = ["名称", "型号", "封装", "规格参数", "数量", "货架名称", "行号", "列号"]',
    'headers = ["名称", "规格参数", "封装", "数量", "最低库存", "类别", "货架名称", "行号", "列号"]'
)
# 6. Add iter_rows max_col=9
app = app.replace(
    "iter_rows(min_row=3, values_only=True)",
    "iter_rows(min_row=3, max_col=9, values_only=True)"
)
# 7. Add export sorting
app = app.replace(
    "components = load_components()\n    shelves = load_shelves()\n    shelf_map = {s[\"id\"]: s[\"name\"] for s in shelves}\n    wb = Workbook()",
    "components = load_components()\n    components.sort(key=lambda c: (c.get(\"shelf_id\") or 9999, c.get(\"row\") or 9999, c.get(\"col\") or 9999))\n    shelves = load_shelves()\n    shelf_map = {s[\"id\"]: s[\"name\"] for s in shelves}\n    wb = Workbook()"
)
# 8. DataValidation range F3:F100
app = app.replace(
    'dv.add("F3:F1048576")',
    'dv.add("F3:F100")'
)

with open(path, "w", encoding="utf-8") as f:
    f.write(app)

# Verify
sys.path.insert(0, BASE)
from app import app as fa
print(f"OK! Routes: {len(list(fa.url_map.iter_rules()))}")

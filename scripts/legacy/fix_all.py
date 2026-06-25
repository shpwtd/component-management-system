import sys, os
BASE = "."

path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    app = f.read()

# 1. Add get_category_tree to import
old_import = "from classifier import classify, detect_package, get_category_list, get_category_display, plan_layout, load_categories, suggest_group_key"
new_import = "from classifier import classify, detect_package, get_category_list, get_category_display, plan_layout, load_categories, suggest_group_key, get_category_tree"
app = app.replace(old_import, new_import)
print("1: get_category_tree imported")

# 2. Add save_categories function
old_after = app.index("def save_logs")  # find save_logs position
# save_logs is before save_categories, find the right spot
idx = app.index("def save_logs")
end_of_func = idx + app[idx:].index("\ndef ")
app = app[:end_of_func] + '\ndef save_categories(data):\n    _save_json("categories.json", data)\n' + app[end_of_func:]
print("2: save_categories added")

# 3. Add categories routes before @app.route("/search")
categories_routes = '''
@app.route("/categories", methods=["GET", "POST"])
def categories_page():
    tree = get_category_tree()
    cats = load_categories()
    if request.method == "POST":
        key = request.form.get("key", "").strip()
        name = request.form.get("name", "").strip()
        parent = request.form.get("parent", "").strip() or None
        if not key or not name:
            flash("\u8bf7\u586b\u5199\u7c7b\u522b\u6807\u8bc6\u548c\u540d\u79f0", "danger")
            return render_template("categories.html", cats=cats, tree=tree)
        key = re.sub(r"[^a-z0-9_]", "", key.lower())
        if not key:
            flash("\u7c7b\u522b\u6807\u8bc6\u53ea\u80fd\u5305\u542b\u5b57\u6bcd\u3001\u6570\u5b57\u548c\u4e0b\u5212\u7ebf", "danger")
            return render_template("categories.html", cats=cats, tree=tree)
        if any(c["key"] == key for c in cats):
            flash(f"\u7c7b\u522b\u6807\u8bc6\u300c{key}\u300d\u5df2\u5b58\u5728", "danger")
            return render_template("categories.html", cats=cats, tree=tree)
        cats.append({"key": key, "name": name, "parent": parent, "icon": "?"})
        _save_json("categories.json", cats)
        flash(f"\u7c7b\u522b\u300c{name}\u300d\u5df2\u6dfb\u52a0", "success")
        return redirect(url_for("categories_page"))
    return render_template("categories.html", cats=cats, tree=tree)

@app.route("/categories/<cat_key>/delete", methods=["POST"])
def category_delete(cat_key):
    cats = load_categories()
    if cat_key in ("other",):
        flash("\u4e0d\u80fd\u5220\u9664\u300c\u5176\u4ed6\u300d\u7c7b\u522b", "danger")
        return redirect(url_for("categories_page"))
    cat = next((c for c in cats if c["key"] == cat_key), None)
    if not cat:
        flash("\u7c7b\u522b\u4e0d\u5b58\u5728", "danger")
        return redirect(url_for("categories_page"))
    cats[:] = [c for c in cats if c["key"] != cat_key]
    components = load_components()
    for comp in components:
        if comp.get("category") == cat_key:
            comp["category"] = "other"
    save_components(components)
    _save_json("categories.json", cats)
    flash(f"\u7c7b\u522b\u300c{cat['name']}\u300d\u5df2\u5220\u9664\uff0c\u76f8\u5173\u5143\u5668\u4ef6\u5df2\u5f52\u5165\u300c\u5176\u4ed6\u300d", "success")
    return redirect(url_for("categories_page"))
'''

app = app.replace('@app.route("/search")', categories_routes + '@app.route("/search")', 1)
print("3: Categories routes inserted")

# 4. Fix export headers
app = app.replace(
    'headers = ["名称", "\u578b\u53f7", "\u5c01\u88c5", "\u89c4\u683c\u53c2\u6570", "\u6570\u91cf", "\u6700\u4f4e\u5e93\u5b58", "\u7c7b\u522b", "\u8d27\u67b6", "\u884c\u53f7", "\u5217\u53f7"]',
    'headers = ["名称", "\u89c4\u683c\u53c2\u6570", "\u5c01\u88c5", "\u6570\u91cf", "\u6700\u4f4e\u5e93\u5b58", "\u7c7b\u522b", "\u8d27\u67b6", "\u884c\u53f7", "\u5217\u53f7"]'
)
print("4: Export headers fixed")

# 5. Fix template headers
app = app.replace(
    'headers = ["名称", "\u578b\u53f7", "\u5c01\u88c5", "\u89c4\u683c\u53c2\u6570", "\u6570\u91cf", "\u8d27\u67b6\u540d\u79f0", "\u884c\u53f7", "\u5217\u53f7"]',
    'headers = ["名称", "\u89c4\u683c\u53c2\u6570", "\u5c01\u88c5", "\u6570\u91cf", "\u6700\u4f4e\u5e93\u5b58", "\u7c7b\u522b", "\u8d27\u67b6\u540d\u79f0", "\u884c\u53f7", "\u5217\u53f7"]'
)
print("5: Template headers fixed")

with open(path, "w", encoding="utf-8") as f:
    f.write(app)

# Verify
sys.path.insert(0, BASE)
from app import app as fa
routes = [r.rule for r in fa.url_map.iter_rules()]
print(f"\nOK! Routes: {len(routes)}")
[print(r) for r in sorted(routes) if 'categor' in r or 'import' in r or 'export' in r or 'download' in r]

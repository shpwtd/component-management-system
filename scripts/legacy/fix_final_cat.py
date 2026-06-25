import os
BASE = "."
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the categories route section to remove
start = None
end = None
for i, l in enumerate(lines):
    if '@app.route("/categories", methods=' in l:
        start = i
    if start and i > start and 'def category_delete(cat_key):' in l:
        end = i
        break

if start and end:
    print(f"Removing lines {start+1} to {end}")
    # Keep the @app.route and def lines, rebuild the function body
    # Actually, let's just remove the corrupted section and add clean code
    
    # Build clean categories route
    clean_code = '''@app.route("/categories", methods=["GET", "POST"])
def categories_page():
    clf = __import__("classifier")
    cats = clf.load_categories()
    tree = clf.get_category_tree()
    if request.method == "POST":
        key = request.form.get("key", "").strip()
        name = request.form.get("name", "").strip()
        parent = request.form.get("parent", "").strip() or None
        if not key or not name:
            flash("请填写类别标识和名称", "danger")
            return render_template("categories.html", cat_list=cats, tree=tree)
        key = __import__("re").sub(r"[^a-z0-9_]", "", key.lower())
        if not key:
            flash("类别标识只能包含字母、数字和下划线", "danger")
            return render_template("categories.html", cat_list=cats, tree=tree)
        if any(cat["key"] == key for cat in cats):
            flash(f"类别标识「{key}」已存在", "danger")
            return render_template("categories.html", cat_list=cats, tree=tree)
        cats.append({"key": key, "name": name, "parent": parent, "icon": "?"})
        _save_json("categories.json", cats)
        flash(f"类别「{name}」已添加", "success")
        return __import__("flask").redirect(url_for("categories_page"))
    return render_template("categories.html", cat_list=cats, tree=tree)
'''
    
    # Replace lines from start to end-1 with clean code
    lines[start:end] = clean_code.split("\n")
    # Add newline after each line
    for i in range(start, len(lines)):
        if i < len(lines) and not lines[i].endswith("\n"):
            lines[i] += "\n"
    
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Categories route rebuilt")

import sys; sys.path.insert(0, BASE)
from app import app
print(f"OK! Routes: {len(list(app.url_map.iter_rules()))}")

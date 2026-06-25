import sys, os
BASE = "."
path = os.path.join(BASE, "app.py")

with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Replace tree = get_category_tree() with inline tree building code
old = "    tree = get_category_tree()\n    if request.method"
new = """    tree = {}
    for c in cats:
        if c.get("parent") is None:
            tree[c["key"]] = {"key": c["key"], "name": c["name"], "children": []}
    for c in cats:
        if c.get("parent") and c["parent"] in tree:
            tree[c["parent"]]["children"].append({"key": c["key"], "name": c["name"]})
    for k in tree:
        tree[k]["children"].sort(key=lambda x: x["name"])
    if request.method"""

c = c.replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

sys.path.insert(0, BASE)
from app import app
routes = len(list(app.url_map.iter_rules()))
print(f"OK! Routes: {routes}")
print("/categories in routes:", any("categories" in r.rule for r in app.url_map.iter_rules()))

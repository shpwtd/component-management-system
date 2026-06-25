import re, sys

with open("app.py","r",encoding="utf-8") as f:
    c = f.read()

# Fix 1: component_add - tree= with __import__
c = c.replace("tree=get_category_tree(),", "tree=__import__(\"classifier\").get_category_tree(),")
print("Fix 1: component_add tree=")

# Fix 2: shelf_add - add shelves=
c = c.replace('shelf=None)', 'shelf=None, shelves=load_shelves())')
print("Fix 2: shelf_add shelves=")

# Fix 3: Add toggle_lock route if missing
if '/components/<int:cid>/toggle_lock' not in c:
    toggle_code = '''
@app.route("/components/<int:cid>/toggle_lock", methods=["POST"])
def component_toggle_lock(cid):
    components = load_components()
    comp = next((c for c in components if c["id"] == cid), None)
    if not comp:
        return __import__("flask").jsonify({"success": False, "error": "\u5143\u5668\u4ef6\u4e0d\u5b58\u5728"}), 404
    comp["locked"] = 0 if comp.get("locked") else 1
    comp["updated_at"] = __import__("app").now_str() if False else __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    __import__("json").dump(load_components(), open("data/components.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    # Actually need to save properly
    import json as _json
    comps = _json.load(open("data/components.json","r",encoding="utf-8"))
    for c_ in comps:
        if c_["id"] == cid:
            c_["locked"] = 0 if c_.get("locked") else 1
            c_["updated_at"] = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    _json.dump(comps, open("data/components.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    return __import__("flask").jsonify({"success": True, "locked": [c_["locked"] for c_ in comps if c_["id"] == cid][0]})
'''
    c = c.replace('if __name__ == "__main__":', toggle_code + '\n\nif __name__ == "__main__":')
    print("Fix 3: toggle_lock route added")

with open("app.py","w",encoding="utf-8") as f:
    f.write(c)

sys.path.insert(0, ".")
from app import app
routes = [str(r) for r in app.url_map.iter_rules()]
print(f"OK! Routes: {len(routes)}")
for r in routes:
    if "toggle" in r or "replan" in r:
        print(f"  {r}")

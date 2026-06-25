import os, sys
BASE = "."

# Fix 1: Categories route: cat_list=cats -> cats=cats
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    app = f.read()
app = app.replace('cat_list=cats, tree=tree)', 'cats=cats, tree=tree)')
with open(path, "w", encoding="utf-8") as f:
    f.write(app)
print("Fix 1: categories route uses cats=cats")

# Fix 2: import_result.html: shelf_id -> shelf_name
tpl_path = os.path.join(BASE, "templates", "import_result.html")
with open(tpl_path, "r", encoding="utf-8") as f:
    tpl = f.read()
tpl = tpl.replace("{{ s.shelf_id }}", "{{ s.shelf_name }}")
with open(tpl_path, "w", encoding="utf-8") as f:
    f.write(tpl)
print("Fix 2: import_result uses shelf_name")

# Fix 3: components page - export headers match
# Check current export headers
if "\u578b\u53f7" in app[app.index("def export_excel"):app.index("def export_excel")+1500]:
    print("Fix 3: Export still has \u578b\u53f7!")
else:
    print("Fix 3: Export headers OK (no \u578b\u53f7)")

# Check template headers
idx = app.index("def download_template")
section = app[idx:idx+2000]
if "\u578b\u53f7" in section and "headers" in section[:section.index("\n")]:
    print("Fix 3b: Template still has \u578b\u53f7!")
else:
    print("Fix 3b: Template headers OK (no \u578b\u53f7)")

# Fix 4: component_list.html - add lock JS if missing
cl_path = os.path.join(BASE, "templates", "component_list.html")
with open(cl_path, "r", encoding="utf-8") as f:
    cl = f.read()
if "toggleLock" not in cl:
    # Add lock column
    cl = cl.replace("<th>\u64cd\u4f5c</th>", "<th>\u9501\u5b9a</th><th>\u64cd\u4f5c</th>")
    cl = cl.replace(
        '<td style="white-space:nowrap">\n<a href="/components/{{ c.id }}" class="btn btn-sm btn-secondary">\u67e5\u770b</a>',
        '<td><span class="lock-toggle" data-cid="{{ c.id }}" data-locked="{{ 1 if c.locked else 0 }}" onclick="toggleLock(this)">{{ "\U0001F512" if c.locked else "\U0001F513" }}</span></td>\n<td style="white-space:nowrap">\n<a href="/components/{{ c.id }}" class="btn btn-sm btn-secondary">\u67e5\u770b</a>'
    )
    # Add JS
    js = "\n<script>\nfunction toggleLock(el) {\n    var cid = el.getAttribute(\"data-cid\");\n    fetch(\"/components/\" + cid + \"/toggle_lock\", {method: \"POST\"})\n        .then(function(r) { return r.json(); })\n        .then(function(data) {\n            if (data.success) {\n                el.textContent = data.locked ? \"\U0001F512\" : \"\U0001F513\";\n                el.setAttribute(\"data-locked\", data.locked ? \"1\" : \"0\");\n            }\n        });\n}\n</script>\n"
    cl = cl.replace("{% endblock %}", js + "{% endblock %}")
    with open(cl_path, "w", encoding="utf-8") as f:
        f.write(cl)
    print("Fix 4: component_list lock toggle added")
else:
    print("Fix 4: lock toggle already present")

sys.path.insert(0, BASE)
from app import app as fa
print(f"\nOK! Routes: {len(list(fa.url_map.iter_rules()))}")

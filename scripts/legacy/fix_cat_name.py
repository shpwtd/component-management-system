import os
BASE = "."

# Fix categories route: cats=cats -> cat_list=cats in render call
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Only replace inside categories_page
idx = c.index("def categories_page():")
end = c.index("def category_delete", idx)
section = c[idx:end]

section = section.replace(
    'return render_template("categories.html", cats=cats, tree=tree)',
    'return render_template("categories.html", cat_list=cats, tree=tree)'
)

c = c[:idx] + section + c[end:]

with open(path, "w", encoding="utf-8") as f:
    f.write(c)
print("Route: cats -> cat_list in template call")

# Fix categories.html template
tpl_path = os.path.join(BASE, "templates", "categories.html")
with open(tpl_path, "r", encoding="utf-8") as f:
    tpl = f.read()
tpl = tpl.replace("{% for c in cats %}", "{% for c in cat_list %}")
with open(tpl_path, "w", encoding="utf-8") as f:
    f.write(tpl)
print("Template: cats -> cat_list")

import sys
sys.path.insert(0, BASE)
from app import app
print(f"OK! Routes: {len(list(app.url_map.iter_rules()))}")

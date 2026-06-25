with open("app.py","r",encoding="utf-8") as f:
    c = f.read()

old = '    return render_template("component_form.html", comp=comp, shelves=shelves, cats=get_category_list(), stock_logs=logs, detail_view=True)'
new = '    return render_template("component_form.html", comp=comp, shelves=shelves, cats=get_category_list(), stock_logs=logs, detail_view=True, tree=__import__("classifier").get_category_tree())'

if old in c:
    c = c.replace(old, new)
    with open("app.py","w",encoding="utf-8") as f:
        f.write(c)
    print("Fix: tree= added to component_detail")
else:
    print("Pattern not found!")
    import re
    for m in re.finditer(r'component_detail', c):
        print(f"Found at pos {m.start()}: ...{c[max(0,m.start()-50):m.start()+50]}...")

import sys; sys.path.insert(0,".")
from app import app
print(f"OK, routes: {len(list(app.url_map.iter_rules()))}")

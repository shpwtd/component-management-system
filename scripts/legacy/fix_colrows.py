with open("app.py","r",encoding="utf-8") as f:
    c = f.read()

old = 'for gk, grp in sorted(groups.items(), key=lambda x: (-len(x[1]), x[0])):'
new = '''    col_rows = {}
    for s in shelves:
        for rd in s.get("rows", []):
            cc = rd["cols"]
            if cc not in col_rows: col_rows[cc] = []
            col_rows[cc].append({"shelf_id": s["id"], "shelf_name": s["name"], "row": rd["row"], "cols": cc})

    ''' + old

if old in c:
    c = c.replace(old, new)
    with open("app.py","w",encoding="utf-8") as f:
        f.write(c)
    print("col_rows added to replan_page")
else:
    print("Pattern not found!")

import sys; sys.path.insert(0,".")
from app import app
print("Routes:", len(list(app.url_map.iter_rules())))

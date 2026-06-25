import re
# 3. Fix component_add to auto-assign position
with open("app.py","r",encoding="utf-8") as f:
    c = f.read()
old = "        if comp[\"category\"] == \"other\":\n            auto_cat = classify(comp[\"name\"], comp[\"model\"], comp[\"specs\"], comp[\"package\"])\n            cats_list = load_categories()\n            if any(c[\"key\"] == auto_cat for c in cats_list):\n                comp[\"category\"] = auto_cat\n        components = load_components()\n        comp[\"id\"] = next_id(components)\n        components.append(comp)"
new = "        if comp[\"category\"] == \"other\":\n            auto_cat = classify(comp[\"name\"], comp[\"model\"], comp[\"specs\"], comp[\"package\"])\n            cats_list = load_categories()\n            if any(c[\"key\"] == auto_cat for c in cats_list):\n                comp[\"category\"] = auto_cat\n        if comp[\"shelf_id\"] is None:\n            shelves_all = load_shelves()\n            if shelves_all:\n                occ = get_occupied(shelves_all, [c for c in load_components() if c[\"id\"] != comp[\"id\"]])\n                for s in shelves_all:\n                    for rd in s.get(\"rows\", []):\n                        for col in range(1, rd[\"cols\"]+1):\n                            if (s[\"id\"], rd[\"row\"], col) not in occ:\n                                comp[\"shelf_id\"] = s[\"id\"]\n                                comp[\"row\"] = rd[\"row\"]\n                                comp[\"col\"] = col\n                                break\n                        if comp[\"shelf_id\"]: break\n                    if comp[\"shelf_id\"]: break\n        components = load_components()\n        comp[\"id\"] = next_id(components)\n        components.append(comp)"
if old in c:
    c = c.replace(old, new)
    print("3. Component add auto-assign added")
else:
    print("3. Could not find block to replace")
with open("app.py","w",encoding="utf-8") as f:
    f.write(c)

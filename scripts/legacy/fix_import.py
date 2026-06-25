import sys
c = open(sys.argv[1], 'r', encoding='utf-8-sig').read()
c = c.replace('            cat = classify(name, model, specs, pkg)', '            cat_list = get_category_list()\n            cat_lookup = {cn: ck for ck, cn in cat_list}\n            if cat_name in cat_lookup:\n                cat_key = cat_lookup[cat_name]\n            else:\n                cat_key = classify(name, "", specs, pkg)')
old_auto = '            if not shelf_name or not row_num_str or not col_str:\n                error_items.append({"row": row_idx, "reason": "\u8d27\u4f4d\u4fe1\u606f\u4e0d\u5b8c\u6574", "name": name})\n                continue'
new_auto = '            if not shelf_name or not row_num_str or not col_str:\n                assigned = False\n                for s in shelves:\n                    for rd in s.get("rows", []):\n                        for c in range(1, rd["cols"]+1):\n                            if (s["id"], rd["row"], c) not in occupied:\n                                item = {"name": name, "model": "", "package": pkg, "specs": specs, "quantity": qty,\n                                        "shelf_id": s["id"], "row": rd["row"], "col": c, "category": cat_key,\n                                        "min_stock": min_stock, "locked": 0}\n                                success_items.append(item)\n                                occupied[(s["id"], rd["row"], c)] = {"name": name}\n                                assigned = True\n                                break\n                        if assigned: break\n                    if assigned: break\n                if not assigned:\n                    error_items.append({"row": row_idx, "reason": "\u65e0\u53ef\u7528\u7684\u8d27\u4f4d", "name": name})\n                continue'
c = c.replace(old_auto, new_auto)
c = c.replace('"model": model,', '"model": "",')
c = c.replace('"category": cat,', '"category": cat_key,')
c = c.replace('"min_stock": 0', '"min_stock": min_stock, "locked": 0')
c = c.replace('"model": item.get("model", ""),', '"model": "",')
open(sys.argv[1], 'w', encoding='utf-8').write(c)
print('OK')

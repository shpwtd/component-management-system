# 4. Fix shelf_add to support copy from existing
with open("app.py","r",encoding="utf-8") as f:
    c = f.read()
old = '        rows_data = []\n        row_idx = 1\n        while True:\n            cols_str = request.form.get(f"cols_{row_idx}")\n            if cols_str is None:\n                break\n            try:\n                cols = int(cols_str)\n                if cols > 0:\n                    rows_data.append({"row": row_idx, "cols": cols})\n            except ValueError:\n                pass\n            row_idx += 1\n        if not rows_data:\n            flash("请至少添加一行", "danger")\n            return render_template("shelf_form.html", shelf=None)\n        shelves = load_shelves()\n        shelves.append({"id": next_id(shelves), "name": name, "rows": rows_data})'
new = '        copy_from = request.form.get("copy_from", "").strip()\n        rows_data = []\n        if copy_from:\n            try:\n                cid = int(copy_from)\n                src = next((s for s in load_shelves() if s["id"] == cid), None)\n                if src:\n                    rows_data = [{"row": rd["row"], "cols": rd["cols"]} for rd in src.get("rows", [])]\n            except ValueError:\n                pass\n        if not rows_data:\n            row_idx = 1\n            while True:\n                cols_str = request.form.get(f"cols_{row_idx}")\n                if cols_str is None:\n                    break\n                try:\n                    cols = int(cols_str)\n                    if cols > 0:\n                        rows_data.append({"row": row_idx, "cols": cols})\n                except ValueError:\n                    pass\n                row_idx += 1\n        if not rows_data:\n            flash("请至少添加一行", "danger")\n            return render_template("shelf_form.html", shelf=None, shelves=load_shelves())\n        shelves = load_shelves()\n        shelves.append({"id": next_id(shelves), "name": name, "rows": rows_data})'
if old in c:
    c = c.replace(old, new)
    print("4. Shelf add copy feature added")
else:
    print("4. WARNING: Could not find shelf_add block")
with open("app.py","w",encoding="utf-8") as f:
    f.write(c)

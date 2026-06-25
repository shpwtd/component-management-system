import os, sys
BASE = "."

# Clear old error log
log_path = os.path.join(BASE, "data", "error.log")
if os.path.exists(log_path):
    open(log_path, "w").close()

# Fix app.py
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    app = f.read()

# 1. Export: sort components by shelf/row/col
old_export = 'components = load_components()\n    shelves = load_shelves()\n    shelf_map = {s["id"]: s["name"] for s in shelves}\n    wb = Workbook()'
new_export = 'components = load_components()\n    components.sort(key=lambda c: (c.get("shelf_id") or 9999, c.get("row") or 9999, c.get("col") or 9999))\n    shelves = load_shelves()\n    shelf_map = {s["id"]: s["name"] for s in shelves}\n    wb = Workbook()'
app = app.replace(old_export, new_export)
print("1: Export sorting added")

# 2. Wrap entire import_page POST in try/except
old_import_start = '    if request.method == "POST":\n        file = request.files.get("file")'
new_import_start = '    if request.method == "POST":\n        try:\n            file = request.files.get("file")'
app = app.replace(old_import_start, new_import_start)

# Find the render_template at the end of POST and close the try block
old_import_end = '    return render_template("import.html")'
new_import_end = '        except Exception as e:\n            import traceback\n            logging.error(f"Import error: {traceback.format_exc()}")\n            flash(f"\u5bfc\u5165\u5931\u8d25\uff1a{e}", "danger")\n            return render_template("import.html")\n    return render_template("import.html")'
app = app.replace(old_import_end, new_import_end)
print("2: Import POST wrapped in try/except")

with open(path, "w", encoding="utf-8") as f:
    f.write(app)

# Verify
sys.path.insert(0, BASE)
from app import app as fa
print(f"\nOK! Routes: {len(list(fa.url_map.iter_rules()))}")

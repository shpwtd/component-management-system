import sys, os
BASE = "."
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    app = f.read()

# 1. iter_rows max_col=9
app = app.replace(
    "iter_rows(min_row=3, values_only=True)",
    "iter_rows(min_row=3, max_col=9, values_only=True)"
)

# 2. Logging config
app = app.replace(
    "from classifier import classify, detect_package",
    'import logging\nlogging.basicConfig(filename="data/error.log", level=logging.ERROR, format="%(asctime)s %(levelname)s: %(message)s", encoding="utf-8")\nfrom classifier import classify, detect_package'
)

# 3. toggle_lock route
toggle = """
@app.route("/components/<int:cid>/toggle_lock", methods=["POST"])
def component_toggle_lock(cid):
    components = load_components()
    comp = next((c for c in components if c["id"] == cid), None)
    if not comp:
        return jsonify({"success": False, "error": "\u5143\u5668\u4ef6\u4e0d\u5b58\u5728"}), 404
    comp["locked"] = 0 if comp.get("locked") else 1
    comp["updated_at"] = now_str()
    save_components(components)
    return jsonify({"success": True, "locked": comp["locked"]})
"""
app = app.replace("@app.route(\"/uploads/<filename>\")", toggle + "\n@app.route(\"/uploads/<filename>\")")

# 4. Log import errors
app = app.replace(
    "except Exception as e:\n            flash(f\"\u6587\u4ef6\u89e3\u6790\u5931\u8d25\uff1a{e}\", \"danger\")",
    "except Exception as e:\n            logging.error(f\"Import failed: {e}\", exc_info=True)\n            flash(f\"\u6587\u4ef6\u89e3\u6790\u5931\u8d25\uff1a{e}\", \"danger\")"
)

with open(path, "w", encoding="utf-8") as f:
    f.write(app)
print("Step 1: app.py updated")
sys.path.insert(0, BASE)
from app import app as fa
print("  Routes:", len(list(fa.url_map.iter_rules())))

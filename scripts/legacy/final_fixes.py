import sys, os
BASE = "."

# ─── 1. Fix import: limit to 9 columns ────────────────
with open(os.path.join(BASE, "app.py"), "r", encoding="utf-8") as f:
    app = f.read()

app = app.replace(
    "iter_rows(min_row=3, values_only=True)",
    "iter_rows(min_row=3, max_col=9, values_only=True)"
)
print("1: import iter_rows limited to 9 columns")

# ─── 2. Add logging configuration ─────────────────────
# Add logging import and setup after existing imports
logging_code = """
import logging
logging.basicConfig(filename="data/error.log", level=logging.ERROR,
                    format="%(asctime)s %(levelname)s: %(message)s",
                    encoding="utf-8")
"""

app = app.replace(
    'from classifier import classify, detect_package',
    logging_code + 'from classifier import classify, detect_package'
)
# Replace the first occurrence only
first = app.index(logging_code)
app = app[:first] + logging_code + app[first + len(logging_code):]
# Remove duplicate
second = app.index(logging_code, first + len(logging_code))
app = app[:second] + app[second + len(logging_code):]
print("2: logging configured")

# ─── 3. Add toggle_lock route ─────────────────────────
# Insert before the last route (serve_image or if __name__)
toggle_route = '''

@app.route("/components/<int:cid>/toggle_lock", methods=["POST"])
def component_toggle_lock(cid):
    components = load_components()
    comp = next((c for c in components if c["id"] == cid), None)
    if not comp:
        return jsonify({"success": False, "error": "元器件不存在"}), 404
    comp["locked"] = 0 if comp.get("locked") else 1
    comp["updated_at"] = now_str()
    save_components(components)
    return jsonify({"success": True, "locked": comp["locked"]})
'''

app = app.replace(
    '@app.route("/uploads/<filename>")',
    toggle_route + '\n@app.route("/uploads/<filename>")'
)
print("3: toggle_lock route added")

# Also add logging to import_page error handler
# Find the except block in import_page
app = app.replace(
    'except Exception as e:\n            flash(f"文件解析失败：{e}", "danger")',
    'except Exception as e:\n            import logging\n            logging.error(f"Import file parse error: {e}", exc_info=True)\n            flash(f"文件解析失败：{e}", "danger")'
)
print("3b: import error logging added")

with open(os.path.join(BASE, "app.py"), "w", encoding="utf-8") as f:
    f.write(app)

# ─── 4. Update component_list.html with lock column ───
cl_path = os.path.join(BASE, "templates", "component_list.html")
with open(cl_path, "r", encoding="utf-8") as f:
    cl = f.read()

# Add lock column header
cl = cl.replace(
    "<th>操作</th>",
    "<th>锁定</th><th>操作</th>"
)

# Add lock toggle cell before action cell
cl = cl.replace(
    '<td style="white-space:nowrap">\n<a href="/components/{{ c.id }}" class="btn btn-sm btn-secondary">查看</a>',
    '<td><span class="lock-toggle" data-cid="{{ c.id }}" data-locked="{{ c.locked if c.locked else 0 }}" onclick="toggleLock(this)">{{ "\\U0001f512" if c.locked else "\\U0001f513" }}</span></td>\n<td style="white-space:nowrap">\n<a href="/components/{{ c.id }}" class="btn btn-sm btn-secondary">查看</a>'
)

# Add JavaScript for lock toggle
cl = cl.replace(
    "</table>",
    "</table>\n<script>\nfunction toggleLock(el) {\n    var cid = el.dataset.cid;\n    fetch('/components/' + cid + '/toggle_lock', {method: 'POST'})\n        .then(r => r.json())\n        .then(data => {\n            if (data.success) {\n                el.textContent = data.locked ? '\\U0001f512' : '\\U0001f513';\n                el.dataset.locked = data.locked ? '1' : '0';\n            }\n        });\n}\n</script>"
)

with open(cl_path, "w", encoding="utf-8") as f:
    f.write(cl)
print("4: component_list lock toggle added")

# ─── 5. Add CSS for lock toggle ───────────────────────
css_path = os.path.join(BASE, "static", "style.css")
with open(css_path, "a", encoding="utf-8") as f:
    f.write('\n.lock-toggle { cursor: pointer; font-size: 18px; user-select: none; }\n')
print("5: CSS for lock toggle added")

# ─── Verify ───────────────────────────────────────────
sys.path.insert(0, BASE)
from app import app as flask_app
print(f"\nAll done! Routes: {len(list(flask_app.url_map.iter_rules()))}')

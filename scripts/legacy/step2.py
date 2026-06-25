import os
BASE = "."

# Update component_list.html
cl_path = os.path.join(BASE, "templates", "component_list.html")
with open(cl_path, "r", encoding="utf-8") as f:
    cl = f.read()

# Add lock column header
cl = cl.replace("<th>操作</th>", "<th>\u9501\u5b9a</th><th>\u64cd\u4f5c</th>")

# Add lock toggle cell
cl = cl.replace(
    '<td style="white-space:nowrap">\n<a href="/components/{{ c.id }}" class="btn btn-sm btn-secondary">\u67e5\u770b</a>',
    '<td><span class="lock-toggle" data-cid="{{ c.id }}" data-locked="{{ 1 if c.locked else 0 }}" onclick="toggleLock(this)">{{ "\U0001F512" if c.locked else "\U0001F513" }}</span></td>\n<td style="white-space:nowrap">\n<a href="/components/{{ c.id }}" class="btn btn-sm btn-secondary">\u67e5\u770b</a>'
)

# Add JavaScript
js_code = """
<script>
function toggleLock(el) {
    var cid = el.getAttribute("data-cid");
    fetch("/components/" + cid + "/toggle_lock", {method: "POST"})
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.success) {
                el.textContent = data.locked ? "\U0001F512" : "\U0001F513";
                el.setAttribute("data-locked", data.locked ? "1" : "0");
            }
        });
}
</script>"""
cl = cl.replace("{% endblock %}", js_code + "\n{% endblock %}")

with open(cl_path, "w", encoding="utf-8") as f:
    f.write(cl)
print("component_list.html: lock column + JS added")

# Add CSS
with open(os.path.join(BASE, "static", "style.css"), "a", encoding="utf-8") as f:
    f.write('\n.lock-toggle { cursor: pointer; font-size: 18px; user-select: none; display:inline-block; padding:2px 4px; }\n.lock-toggle:hover { background:#dfe6e9; border-radius:4px; }\n')
print("CSS added")

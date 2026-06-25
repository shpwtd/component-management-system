import os
BASE = r"D:\codexspace\元器件管理系统"

# 5a. shelf_form.html - add copy from existing dropdown
path = os.path.join(BASE, "templates", "shelf_form.html")
with open(path, "r", encoding="utf-8") as f:
    sf = f.read()

insert = """{% if not shelf %}
<div class="form-group">
<label>套用已有货架规格（可选）</label>
<select name="copy_from" class="form-control" onchange="onCopyChange(this)">
<option value="">不套用，手动设置</option>
{% for s in shelves %}
<option value="{{ s.id }}">{{ s.name }}（{{ s.rows|length }}行）</option>
{% endfor %}
</select>
</div>
{% endif %}
"""

sf = sf.replace('<div class="form-group">\n<label>货架名称</label>\n<input', 
                '<div class="form-group">\n<label>货架名称</label>\n<input')
# Insert after the name input group closing </div>
sf = sf.replace(
    '<input type="text" name="name" class="form-control" value="{{ shelf.name if shelf else \'\' }}" required placeholder="例如：A货架、主动元件架">\n</div>',
    '<input type="text" name="name" class="form-control" value="{{ shelf.name if shelf else \'\' }}" required placeholder="例如：A货架、主动元件架">\n</div>' + insert
)

with open(path, "w", encoding="utf-8") as f:
    f.write(sf)
print("5a. shelf_form.html updated")

# 5b. component_form.html - remove model field
path2 = os.path.join(BASE, "templates", "component_form.html")
with open(path2, "r", encoding="utf-8") as f:
    cf = f.read()

old_model = """<div class="form-row">
<div class="form-group">
<label>名称 *</label>
<input type="text" name="name" class="form-control" value="{{ comp.name if comp else "" }}" required>
</div>
<div class="form-group">
<label>型号</label>
<input type="text" name="model" class="form-control" value="{{ comp.model if comp else "" }}" placeholder="如 0805-10K">
</div>
</div>"""

new_no_model = """<div class="form-group">
<label>名称 *</label>
<input type="text" name="name" class="form-control" value="{{ comp.name if comp else "" }}" required>
</div>"""

if old_model in cf:
    cf = cf.replace(old_model, new_no_model)
    with open(path2, "w", encoding="utf-8") as f:
        f.write(cf)
    print("5b. Model field removed from component_form.html")
else:
    print("5b. WARNING: model field not found")

# 5c. component_list.html - remove model column
path3 = os.path.join(BASE, "templates", "component_list.html")
if os.path.exists(path3):
    with open(path3, "r", encoding="utf-8") as f:
        cl = f.read()
    cl = cl.replace("<th>名称</th><th>型号</th><th>封装</th>", "<th>名称</th><th>封装</th>")
    cl = cl.replace("<td><strong>{{ c.name }}</strong></td>\n<td>{{ c.model }}</td>", "<td><strong>{{ c.name }}</strong></td>")
    cl = cl.replace('colspan="8"', 'colspan="7"')
    with open(path3, "w", encoding="utf-8") as f:
        f.write(cl)
    print("5c. component_list.html updated")
else:
    print("5c. not found")

# 5d. index.html - remove model line
path4 = os.path.join(BASE, "templates", "index.html")
if os.path.exists(path4):
    with open(path4, "r", encoding="utf-8") as f:
        ix = f.read()
    ix = ix.replace('<span class="cell-pos" style="color:#636e72;font-size:10px">{{ comp.model or \'\' }}</span>', '')
    with open(path4, "w", encoding="utf-8") as f:
        f.write(ix)
    print("5d. index.html updated")
else:
    print("5d. not found")

# 5e. categories.html - add parent selector
path5 = os.path.join(BASE, "templates", "categories.html")
if os.path.exists(path5):
    with open(path5, "r", encoding="utf-8") as f:
        ct = f.read()
    
    old_form = """<div class="form-row">
<div class="form-group">
<label>类别标识（英文）</label>
<input type="text" name="key" class="form-control" required placeholder="如 resistor">
<div class="hint">只能包含字母、数字和下划线</div>
</div>
<div class="form-group">
<label>类别名称</label>
<input type="text" name="name" class="form-control" required placeholder="如 电阻">
</div>
</div>"""
    
    new_form = """<input type="text" name="key" class="form-control" required placeholder="如 resistor_smd">
<div class="hint">只能包含字母、数字和下划线</div>
</div>
<div class="form-group">
<label>类别名称</label>
<input type="text" name="name" class="form-control" required placeholder="如 贴片电阻">
</div>
</div>
<div class="form-group">
<label>父级类别</label>
<select name="parent" class="form-control">
<option value="">顶级类别</option>
{% for k, v in tree.items() %}
<option value="{{ k }}">{{ v.name }}</option>
{% endfor %}
</select>
</div>"""
    
    # Replace form fields but keep the row structure
    ct = ct.replace(
        '<input type="text" name="key" class="form-control" required placeholder="如 resistor">',
        '<input type="text" name="key" class="form-control" required placeholder="如 resistor_smd">'
    )
    ct = ct.replace(
        '<input type="text" name="name" class="form-control" required placeholder="如 电阻">',
        '<input type="text" name="name" class="form-control" required placeholder="如 贴片电阻">'
    )
    
    # Add parent selector after the form-row
    parent_html = """<div class="form-group">
<label>父级类别</label>
<select name="parent" class="form-control">
<option value="">顶级类别</option>
{% for k, v in tree.items() %}
<option value="{{ k }}">{{ v.name }}</option>
{% endfor %}
</select>
</div>
"""
    ct = ct.replace('</div>\n<div class="form-actions">', parent_html + '</div>\n<div class="form-actions">')
    
    with open(path5, "w", encoding="utf-8") as f:
        f.write(ct)
    print("5e. categories.html updated")
else:
    print("5e. not found")

# Add onCopyChange JS to the base template
path6 = os.path.join(BASE, "templates", "base.html")
if os.path.exists(path6):
    with open(path6, "r", encoding="utf-8") as f:
        bt = f.read()
    
    js = """
function onCopyChange(sel) {
    if (!sel.value) return;
    fetch('/api/shelf/' + sel.value + '/rows')
        .then(r => r.json())
        .then(rows => {
            var list = document.getElementById('row-list');
            if (!list) return;
            list.innerHTML = '';
            var rc = 1;
            rows.forEach(function(r) {
                var d = document.createElement('div');
                d.className = 'row-config';
                d.innerHTML = '<span class="row-label">第' + rc + '行</span>' +
                    '<input type="number" name="cols_' + rc + '" class="form-control" value="' + r.cols + '" min="1" max="50" required style="width:80px">' +
                    '<span>列</span>' +
                    '<button type="button" class="btn btn-sm btn-danger" onclick="this.parentElement.remove()">删除</button>';
                list.appendChild(d);
                rc++;
            });
            rowCounter = rc;
        });
}
"""
    # Add the function before closing </script>
    bt = bt.replace('</script>', js + '\n</script>')
    
    with open(path6, "w", encoding="utf-8") as f:
        f.write(bt)
    print("5f. base.html JS function added")

print("\nAll template updates complete!")

import sys

# Read index.html
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    c = f.read()

# === Template changes ===

# 1. Replace opening pattern
old_open = '''{% for shelf in shelves %}
<div class="shelf-grid-container">
<div class="shelf-title">
<span>{{ shelf.name }}</span>'''

new_open = '''{% for shelf in shelves %}
{% set total = shelf.rows | sum(attribute="cols") %}
{% set used = namespace(n=0) %}
{% for row_def in shelf.rows %}
{% for col in range(1, row_def.cols + 1) %}
{% if occupied.get((shelf.id, row_def.row, col)) %}{% set used.n = used.n + 1 %}{% endif %}
{% endfor %}
{% endfor %}
{% set pct = (used.n / total * 100) | int if total > 0 else 0 %}
<div class="shelf-cabinet">
<div class="cabinet-face" onclick="toggleCabinet(this)">
<div class="cabinet-box">
<div class="cabinet-label">{{ shelf.name }}</div>
<div class="cabinet-grip"></div>
<div class="cabinet-grid">
{% for row_def in shelf.rows %}
<div class="cabinet-mini-row">
{% for col in range(1, row_def.cols + 1) %}
<div class="cabinet-mini-cell {{ "on" if occupied.get((shelf.id, row_def.row, col)) else "" }}"></div>
{% endfor %}
</div>
{% endfor %}
</div>
</div>
<div class="cabinet-stats">
<div class="cabinet-bar"><div class="cabinet-fill" style="width:{{ pct }}%"></div></div>
<div class="cabinet-count">{{ used.n }}/{{ total }}</div>
</div>
</div>
<div class="cabinet-expanded">
<div class="shelf-title">
<span>{{ shelf.name }}</span>
<span class="btn btn-sm btn-secondary" onclick="closeCabinet(this)">收起</span>'''

c = c.replace(old_open, new_open, 1)

# 2. Replace closing pattern
old_close = '''</div>
</div>
{% else %}'''

new_close = '''</div>
</div>
</div>
{% else %}'''

c = c.replace(old_close, new_close)

# 3. Add JavaScript
old_js = '''<script>
function toggleLock'''

new_js = '''<script>
function toggleCabinet(el) {
    var cab = el.closest(".shelf-cabinet");
    if (!cab) return;
    document.querySelectorAll(".shelf-cabinet.open").forEach(function(c) {
        c.classList.remove("open");
    });
    cab.classList.add("open");
}
function closeCabinet(el) {
    var cab = el.closest(".shelf-cabinet");
    if (!cab) return;
    cab.classList.remove("open");
}
function toggleLock'''

c = c.replace(old_js, new_js)

with open(sys.argv[1], 'w', encoding='utf-8') as f:
    f.write(c)

print('Template OK')

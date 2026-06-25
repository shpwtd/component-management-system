with open("templates/component_form.html","r",encoding="utf-8") as f:
    t = f.read()

# Wrap tree section with {% if tree is defined %}
old = '{% for k, v in tree.items() %}'
new = '{% if tree is defined %}\n{% for k, v in tree.items() %}'

t = t.replace(old, new)

# Add {% endif %} at the end of the tree section
old_end = '{% endfor %}\n            </optgroup>\n            {% endfor %}'
new_end = '{% endfor %}\n            </optgroup>\n            {% endfor %}\n            {% endif %}'
t = t.replace(old_end, new_end)

with open("templates/component_form.html","w",encoding="utf-8") as f:
    f.write(t)
print("Template fixed: tree is defined check added")

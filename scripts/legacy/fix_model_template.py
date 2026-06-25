with open("templates/import_result.html","r",encoding="utf-8") as f:
    c = f.read()
c = c.replace("<td>{{ s.name }}</td><td>{{ s.model }}</td>", "<td>{{ s.name }}</td>")
c = c.replace("<td><strong>{{ a.component.name }}</strong></td><td>{{ a.component.model }}</td>",
              "<td><strong>{{ a.component.name }}</strong></td>")
c = c.replace("        model: {{ s.model|tojson }},\n", "")
c = c.replace("        model: {{ a.component.model|tojson }},\n", "")
with open("templates/import_result.html","w",encoding="utf-8") as f:
    f.write(c)
print("import_result.html model references removed")

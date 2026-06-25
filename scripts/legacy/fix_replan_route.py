with open("app.py","r",encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    "def replan_execute():",
    "@app.route(\"/replan/execute\", methods=[\"POST\"])\ndef replan_execute():"
)
with open("app.py","w",encoding="utf-8") as f:
    f.write(c)
import sys; sys.path.insert(0,".")
from app import app
for r in app.url_map.iter_rules():
    if "replan" in r.rule:
        print(r.methods, r.rule)
print("Total:", len(list(app.url_map.iter_rules())))

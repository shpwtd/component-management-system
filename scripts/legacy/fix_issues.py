import sys
with open("app.py","r",encoding="utf-8") as f:
    c = f.read()
# Add missing decorator before def replan_execute
c = c.replace(
    "def replan_execute():",
    '@app.route("/replan/execute", methods=["POST"])\ndef replan_execute():'
)
with open("app.py","w",encoding="utf-8") as f:
    f.write(c)
print("replan_execute decorator restored")
# Verify
sys.path.insert(0, ".")
from app import app
for r in app.url_map.iter_rules():
    if "replan" in r.rule:
        print(" ", r.methods, r.rule)

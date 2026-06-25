import os, sys
BASE = "."
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    app = f.read()

# 1. Fix template instruction text
old_instr = "填写说明：名称和货架名称必填，行列号从1开始"
new_instr = "填写说明：名称必填。填写货架名称+行号+列号则导入到指定货位，不填则自动分配空货位"
app = app.replace(old_instr, new_instr)
print("1. Template instruction updated")

# 2. Fix replan route (re-add to end of file)
# Find the replan route boundaries
start_marker = '@app.route("/replan")'
end_marker = 'def replan_execute('

if start_marker in app and end_marker in app:
    idx_start = app.index(start_marker)
    idx_end = app.index(end_marker, idx_start)
    # Extract the replan route
    route_code = app[idx_start:idx_end]
    # Remove from original position
    app = app[:idx_start] + app[idx_end:]
    # Append before if __name__
    app = app.replace('if __name__ == "__main__":', route_code + '\n\nif __name__ == "__main__":')
    print("2. Replan route re-added to end of file")
else:
    print("2. Replan route markers not found, skipping")

with open(path, "w", encoding="utf-8") as f:
    f.write(app)

# Verify
sys.path.insert(0, BASE)
from app import app as fa
routes = [r.rule for r in fa.url_map.iter_rules()]
print(f"\nRoutes: {len(routes)}")
for r in sorted(routes):
    if "replan" in r:
        print(f"  {r}")

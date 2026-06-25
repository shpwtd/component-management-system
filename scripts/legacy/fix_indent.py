with open("app.py","r",encoding="utf-8") as f:
    lines = f.readlines()

# Find the removed try line and fix indentation
# After removing try: at line 558 (0-indexed 557), lines 558+ are over-indented
# Remove 4 spaces from all lines inside the if block (between if POST and GET return)

in_fix_zone = False
for i, l in enumerate(lines):
    s = l.rstrip()
    if 'if request.method == "POST":' in s:
        in_fix_zone = True
        continue
    if in_fix_zone:
        # Hit the GET handler line (outside if block) 
        if s.startswith("return render_template"):
            break
        # Hit another def outside
        if s.startswith("def ") and l[:4] != "    ":
            break
        # Remove 4 spaces from over-indented lines (was inside try:)
        if s.startswith("            "):  # 12 spaces
            lines[i] = l[4:]  # Remove 4 spaces -> 8 spaces

with open("app.py","w",encoding="utf-8") as f:
    f.writelines(lines)
print("Indentation fixed")

import sys
sys.path.insert(0, ".")
from app import app
print(f"OK! Routes: {len(list(app.url_map.iter_rules()))}")

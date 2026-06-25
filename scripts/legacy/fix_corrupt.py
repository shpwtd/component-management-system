with open("app.py","r",encoding="utf-8") as f:
    lines = f.readlines()

# Find lines to remove
remove = set()
for i, l in enumerate(lines):
    s = l.strip()
    # Remove try: right after if POST
    if s == "try:" and i > 0 and "if request.method" in lines[i-1]:
        remove.add(i)
        print(f"Remove try: at line {i+1}")
    # Remove malformed except block at wrong indentation
    if s.startswith("except Exception as e:") and l.startswith("    ") and not l.startswith("        "):
        remove.add(i)
        print(f"Remove except at line {i+1}")
        # Remove the next 4 lines
        for j in range(i+1, min(i+5, len(lines))):
            if lines[j].strip() and lines[j].startswith("        "):
                remove.add(j)
                print(f"  Remove {lines[j].strip()[:40]}")

for i in sorted(remove, reverse=True):
    del lines[i]

with open("app.py","w",encoding="utf-8") as f:
    f.writelines(lines)

import sys
sys.path.insert(0, ".")
from app import app
print(f"\nOK! Routes: {len(list(app.url_map.iter_rules()))}")

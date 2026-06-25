with open("app.py","r",encoding="utf-8") as f:
    lines = f.readlines()

# Fix broken line 446 first
for i, l in enumerate(lines):
    if 'def category_delete(cat_key):' in l and 'return' in l:
        # Line 446 has return and def on same line - split them
        idx = l.index("def category_delete")
        lines[i] = l[:idx] + "\n" + l[idx:]
        print(f"Split line {i+1}")
        break

# Remove line 418 (    try:)
for i, l in enumerate(lines):
    if l.strip() == "try:" and l.startswith("    ") and not l.startswith("        "):
        del lines[i]
        print(f"Removed try: at line {i+1}")
        break

# Remove the except block (around line 443)
for i, l in enumerate(lines):
    if "except Exception as e:" in l:
        end = min(i + 4, len(lines))
        del lines[i:end]
        print(f"Removed except block at lines {i+1} to {end}")
        break

with open("app.py","w",encoding="utf-8") as f:
    f.writelines(lines)

import sys; sys.path.insert(0,"."); from app import app
print("OK, routes:", len(list(app.url_map.iter_rules())))

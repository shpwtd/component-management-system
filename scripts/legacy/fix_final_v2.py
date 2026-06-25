import os, sys
BASE = "."

# Fix component_add
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace('tree=get_category_tree(),', 'tree=__import__("classifier").get_category_tree(),')

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

# Delete __pycache__
import shutil
pycache = os.path.join(BASE, "__pycache__")
if os.path.exists(pycache):
    shutil.rmtree(pycache, ignore_errors=True)
    print("Deleted __pycache__")

sys.path.insert(0, BASE)
from app import app
print(f"OK! Routes: {len(list(app.url_map.iter_rules()))}")

import re
with open("app.py","r",encoding="utf-8") as f:
    c = f.read()
# Use simple replace - avoid regex to prevent escaping issues
c = c.replace('tree=__import__("classifier").get_category_tree()', 'tree={}')
with open("app.py","w",encoding="utf-8") as f:
    f.write(c)
import sys; sys.path.insert(0,".")
from app import app
print(f"OK! Routes: {len(list(app.url_map.iter_rules()))}")

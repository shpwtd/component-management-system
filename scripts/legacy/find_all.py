with open("app.py","r",encoding="utf-8") as f:
    c = f.read()

# Find all categories_page and category_delete occurrences
import re
for m in re.finditer(r'(def categories_page|def category_delete)', c):
    start = max(0, m.start()-100)
    end = min(len(c), m.end()+50)
    snippet = c[start:end]
    print(f"Line ~{c[:m.start()].count(chr(10))+1}: {m.group()}")
    print(f"  Context: {snippet[:150]}...")
    print()

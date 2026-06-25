with open("app.py","r",encoding="utf-8") as f:
    lines = f.readlines()

# Find ALL occurrences of categories_page
for i, l in enumerate(lines):
    if 'def categories_page' in l or '@app.route("/categories"' in l:
        print(f'{i+1}: {l.rstrip()}')

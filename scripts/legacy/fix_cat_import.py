with open("app.py","r",encoding="utf-8") as f:
    c = f.read()

# Replace local import + function call with __import__
c = c.replace(
    "    from classifier import get_category_tree\n    tree = get_category_tree()",
    '    tree = __import__("classifier").get_category_tree()'
)

with open("app.py","w",encoding="utf-8") as f:
    f.write(c)
print("Local import replaced with __import__")

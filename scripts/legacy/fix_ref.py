with open("app.py","r",encoding="utf-8") as f:
    c = f.read()
c = c.replace('formula1="K3:K"', 'formula1="$K$3:$K$"')
with open("app.py","w",encoding="utf-8") as f:
    f.write(c)
import sys; sys.path.insert(0,"."); from app import app
print("OK, routes:", len(list(app.url_map.iter_rules())))

with open("app.py","r",encoding="utf-8") as f:
    c = f.read()
c = c.replace('"name": name, "model": model, "package": pkg, "specs": specs, "quantity": qty,',
              '"name": name, "package": pkg, "specs": specs, "quantity": qty,')
c = c.replace('"name": name, "model": model, "package": pkg, "specs": specs,',
              '"name": name, "package": pkg, "specs": specs,')
with open("app.py","w",encoding="utf-8") as f:
    f.write(c)
print("Fixed model references")

with open("save_version.py","r",encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    '            if os.path.exists(dst): shutil.rmtree(dst)\n            shutil.copytree(src, dst)',
    '            shutil.copytree(src, dst, dirs_exist_ok=True)'
)
with open("save_version.py","w",encoding="utf-8") as f:
    f.write(c)
print("Fixed save_version.py: rmtree -> dirs_exist_ok")

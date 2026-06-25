"""版本保存工具"""
import os, sys, shutil, re
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(BASE, "VERSION")
VERSIONS_DIR = os.path.join(BASE, "versions")
SOURCE_FILES = ["app.py","classifier.py","requirements.txt","start_server.py","save_version.py","VERSION","static/style.css","data/categories.json"]
SOURCE_DIRS = ["templates"]

def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE,"r",encoding="utf-8") as f:
            return f.read().strip()
    return "v0.0.0"

def parse_version(v):
    m = re.match(r"v?(\d+)\.(\d+)\.(\d+)", v)
    return (int(m.group(1)),int(m.group(2)),int(m.group(3))) if m else (0,0,0)

def bump_version(v, part="patch"):
    maj,min,pat = parse_version(v)
    if part=="major": maj+=1; min=0; pat=0
    elif part=="minor": min+=1; pat=0
    else: pat+=1
    return f"v{maj}.{min}.{pat}"

def save_version(new_version=None, bump_part=None, force=False):
    current = get_current_version()
    if new_version:
        target = new_version if new_version.startswith("v") else "v"+new_version
    elif bump_part:
        target = bump_version(current, bump_part)
    else:
        target = bump_version(current, "patch")
    
    target_dir = os.path.join(VERSIONS_DIR, target)
    if os.path.exists(target_dir) and not force:
        print(f"版本 {target} 已存在。使用 -y 参数覆盖或指定其他版本号")
        return False
    
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir, ignore_errors=True)
    os.makedirs(target_dir, exist_ok=True)
    
    for f in SOURCE_FILES:
        src = os.path.join(BASE, f)
        dst = os.path.join(target_dir, f)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
    
    for d in SOURCE_DIRS:
        src = os.path.join(BASE, d)
        dst = os.path.join(target_dir, d)
        if os.path.exists(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
    
    with open(VERSION_FILE,"w",encoding="utf-8") as f:
        f.write(target+"\n")
    
    print(f"版本 {target} 已保存到 versions/{target}/")
    print(f"当前版本: {target}")
    return True

if __name__ == "__main__":
    force = "-y" in sys.argv or "--force" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    
    if "-h" in sys.argv or "--help" in sys.argv:
        print("用法: python save_version.py [版本号 | --minor | --major] [-y]")
        print("  默认: patch 版本 +1")
        print("  -y: 覆盖已存在的版本目录")
        sys.exit(0)
    
    if args:
        a = args[0]
        if a.startswith("--"):
            save_version(bump_part=a[2:], force=force)
        else:
            save_version(new_version=a, force=force)
    else:
        save_version(force=force)

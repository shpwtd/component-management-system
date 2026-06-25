with open("app.py","r",encoding="utf-8") as f:
    c = f.read()

# 1. 模板检查
idx = c.index("def download_template")
s = c[idx:idx+3000]
print("=== 模板检查 ===")
print("DataValidation:", "DataValidation" in s)
print("K列隐藏:", 'column_dimensions["K"]' in s)
# 检查说明在第几行
for line in s.split(chr(10)):
    if "\u8bf4\u660e" in line and "cell" in line:
        print("说明行:", line.strip())

# 2. 导出检查
idx = c.index("def export_excel")
s = c[idx:idx+2000]
print("\n=== 导出检查 ===")
h_lines = [l.strip() for l in s.split(chr(10)) if "headers" in l and "[" in l]
if h_lines:
    print("表头:", h_lines[0])
v_start = s.index("vals = [")
v_end = s.index("]", v_start)+1
vals = s[v_start:v_end]
for l in vals.split(chr(10)):
    if "comp.get" in l or "get_category" in l or "shelf_map" in l:
        print("  数据:", l.strip())
print(f"表头列数: {h_lines[0].count(chr(44))+1}")
print(f"数据列数: {vals.count(chr(44))+1}")

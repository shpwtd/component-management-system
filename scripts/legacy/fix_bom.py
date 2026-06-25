import json, os
path = r'D:\codexspace\元器件管理系统\data\categories.json'
cats = json.loads(open(path, 'r', encoding='utf-8-sig').read())
print(f'Read {len(cats)} categories')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(cats, f, ensure_ascii=False, indent=2)
print('Fixed categories.json BOM')

# Update classifier encoding
cf_path = r'D:\codexspace\元器件管理系统\classifier.py'
content = open(cf_path, 'r', encoding='utf-8').read()
content = content.replace('encoding="utf-8"', 'encoding="utf-8-sig"')
with open(cf_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated classifier.py encoding')

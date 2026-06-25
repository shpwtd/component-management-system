with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix import to include all needed functions
old_import = 'from classifier import classify, detect_package, get_category_list, get_category_display, plan_layout'
new_import = 'from classifier import classify, detect_package, get_category_list, get_category_display, get_category_display, plan_layout, load_categories, suggest_group_key'
content = content.replace(old_import, new_import)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed imports')

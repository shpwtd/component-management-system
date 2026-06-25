with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: Add to_shelf_id to plan items in replan route
old_item = '"cols": target_cc'
new_item = '"to_shelf_id": target_row["shelf_id"], "cols": target_cc'
content = content.replace(old_item, new_item)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed replan route')

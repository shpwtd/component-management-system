with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix the main block
old_end = "if __name__ == \"__main__\":\n"
new_end = """if __name__ == \"__main__\":
    app.run(host=\"127.0.0.1\", port=5000, debug=True)
"""
content = content.replace(old_end, new_end)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed main block')

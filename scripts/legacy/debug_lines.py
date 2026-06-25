with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(890, min(915, len(lines))):
    print(f'{i+1}: {repr(lines[i])}')

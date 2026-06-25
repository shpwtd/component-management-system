with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(895, min(920, len(lines))):
    print(f'{i+1}: {repr(lines[i])}')

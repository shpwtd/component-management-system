import sys, traceback
sys.path.insert(0, '.')
try:
    from classifier import classify, load_categories, suggest_group_key
    print('classifier OK')
    from app import app
    print('app OK, routes:', len(list(app.url_map.iter_rules())))
except SyntaxError as e:
    print(f'SYNTAX ERROR at line {e.lineno}: {e.msg}')
    print(f'Text: {e.text}')
except Exception as e:
    print(f'ERROR: {e}')
    traceback.print_exc()

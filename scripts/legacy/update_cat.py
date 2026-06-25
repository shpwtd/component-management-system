import json, os
DATA_DIR = r'D:\codexspace\元器件管理系统\data'

def load_categories():
    path = os.path.join(DATA_DIR, 'categories.json')
    if not os.path.exists(path):
        return [{'key':'other','name':'其他','parent':None,'icon':'?'}]
    with open(path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def get_category_tree():
    cats = load_categories()
    tree = {}
    for c in cats:
        if c['parent'] is None:
            tree[c['key']] = {'key':c['key'],'name':c['name'],'icon':c.get('icon','?'),'children':[]}
    for c in cats:
        if c['parent'] and c['parent'] in tree:
            tree[c['parent']]['children'].append({'key':c['key'],'name':c['name']})
    # Sort children by name
    for k in tree:
        tree[k]['children'].sort(key=lambda x: x['name'])
    return tree

def get_category_list():
    \"\"\"Return flat list of (key, name) for template use\"\"\"
    cats = load_categories()
    return [(c['key'], c['name']) for c in cats]

def get_category_display(cat_key):
    cats = load_categories()
    m = {c['key']: c['name'] for c in cats}
    return m.get(cat_key, cat_key)

# The rest of classifier.py stays the same

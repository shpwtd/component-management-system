import os, json, re

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

KEYWORD_RULES = [
    # IC 类提前，避免“LED驱动器”被误判为二极管
    (r'(IC|芯片|单片机|MCU|运放|OPAMP|比较器|存储器|FLASH|EEPROM|驱动|LDO|DC.DC|U\d+)', 'ic'),
    (r'(电阻|resistor|res|贴片电阻|R\d+)', 'resistor'),
    (r'(电容|capacitor|cap|贴片电容|电解电容|C\d+)', 'capacitor'),
    (r'(电感|inductor|ind|贴片电感|磁珠|bead|L\d+)', 'inductor'),
    # LED 单独处理（归为二极管子类）
    (r'(LED|发光二极管|指示灯|led)', 'diode'),
    (r'(二极管|diode|整流管|稳压管|肖特基|TVS|D\d+)', 'diode'),
    (r'(三极管|transistor|NPN|PNP|S8050|S8550|9012|9013|9014|9018|2N\d+)', 'transistor'),
    (r'(MOSFET|mos|场效应管|MOS管|IRF\d+|AO\d+|SI\d+)', 'mosfet'),
    (r'(连接器|connector|排针|排母|接插件|接线端子|USB|HDMI|RJ45|DB9|J\d+)', 'connector'),
    (r'(传感器|sensor|温度|湿度|压力|霍尔|红外|超声波|光电|S\d+)', 'sensor'),
    (r'(晶振|crystal|振荡器|oscillator|Y\d+|\d+\.\d+[MK]?Hz)', 'crystal'),
    (r'(继电器|relay|K\d+)', 'relay'),
    (r'(光耦|optocoupler|photocoupler|PC\d+)', 'optocoupler'),
    (r'(保险丝|fuse|保险管|F\d+)', 'fuse'),
    (r'(电位器|potentiometer|pot|可调电阻|VR\d+)', 'potentiometer'),
    (r'(变压器|transformer|T\d+)', 'transformer'),
    (r'(电池|battery|锂电|纽扣电池|CR\d+)', 'battery'),
    (r'(开关|switch|按键|按钮|拨码|SW\d+)', 'switch'),
]

# 类别缓存：避免 get_category_display 在模板循环中反复读文件
_cat_cache = {}

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
        if c.get('parent') is None:
            tree[c['key']] = {'key':c['key'],'name':c['name'],'icon':c.get('icon','?'),'children':[]}
    for c in cats:
        if c.get('parent') and c['parent'] in tree:
            tree[c['parent']]['children'].append({'key':c['key'],'name':c['name']})
    for k in tree:
        tree[k]['children'].sort(key=lambda x: x['name'])
    return tree

def get_category_list():
    cats = load_categories()
    return [(c['key'], c['name']) for c in cats]

def get_category_display(cat_key):
    if not _cat_cache:
        cats = load_categories()
        _cat_cache.update({c['key']: c['name'] for c in cats})
    return _cat_cache.get(cat_key, cat_key)

def refresh_category_cache():
    """类别增删后调用此函数刷新缓存。"""
    _cat_cache.clear()

def classify(name='', model='', specs='', package=''):
    text = f'{name} {model} {specs} {package}'
    for pattern, cat_key in KEYWORD_RULES:
        if re.search(pattern, text, re.UNICODE):
            return cat_key
    return 'other'

def detect_package(text):
    """检测封装类型，返回标准化后的分类（'SMD' 或 '插件'）。"""
    patterns = [
        (r'\b(0402|0603|0805|1206|1210|1812|2512)\b', 'SMD'),
        (r'\b(SOT-?23|SOT23|SOT-?89|SOT89|SOT-?223|SOT223)\b', 'SMD'),
        (r'\b(SOIC-?8|SOIC8|SOIC-?14|SOIC14)\b', 'SMD'),
        (r'\b(TSSOP|MSOP|QFN|QFP|BGA|LQFP|PLCC|SOP|DIP)\d*\b', 'SMD'),
        (r'\b(TO-?92|TO92|TO-?220|TO220)\b', '插件'),
        (r'\b(DIP-?\d+|DIP\d+|插件|直插)\b', '插件'),
    ]
    for pat, pkg_type in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return pkg_type
    return ''

def suggest_group_key(name='', model='', specs='', package='', category=''):
    pkg = (package or '').strip()
    text = f'{(model or "").strip()} {(specs or "").strip()}'
    cat = category or classify(name, model, specs, package)
    group = cat
    if pkg:
        group += f'|{pkg}'
    res = _extract_resistance(text)
    if res:
        if res < 100: group += '|<100'
        elif res < 1000: group += '|100-1K'
        elif res < 10000: group += '|1K-10K'
        elif res < 100000: group += '|10K-100K'
        else: group += '|>100K'
        return group
    cap = _extract_capacitance(text)
    if cap:
        if cap < 1000: group += '|<1nF'
        elif cap < 1000000: group += '|1nF-1uF'
        else: group += '|>1uF'
        return group
    return group

def _extract_resistance(text):
    m = re.search(r'(\d+(?:\.\d+)?)\s*([KkMm]?)\s*[Ω欧]?', text)
    if m:
        val = float(m.group(1))
        u = m.group(2).upper()
        if u == 'K': val *= 1000
        elif u == 'M': val *= 1000000
        return val
    return None

def _extract_capacitance(text):
    m = re.search(r'(\d+(?:\.\d+)?)\s*([pPnNμuMm]?)\s*[Ff]', text)
    if not m: return None
    val = float(m.group(1))
    u = m.group(2).lower()
    if u == 'n': val *= 1000
    elif u in ('μ','u'): val *= 1000000
    elif u == 'm': val *= 1000000000
    return val

def plan_layout(components, shelves, occupied=None):
    if not shelves or not components:
        return None
    groups = {}
    for comp in components:
        key = suggest_group_key(comp.get('name',''), comp.get('model',''),
                                comp.get('specs',''), comp.get('package',''),
                                comp.get('category',''))
        if key not in groups: groups[key] = []
        groups[key].append(comp)
    empty_slots = []
    for shelf in shelves:
        for rd in shelf.get('rows', []):
            for col in range(1, rd['cols']+1):
                key = (shelf['id'], rd['row'], col)
                if occupied and key in occupied:
                    continue
                empty_slots.append({
                    'shelf_id': shelf['id'], 'shelf_name': shelf['name'],
                    'row': rd['row'], 'col': col
                })
    if not empty_slots:
        return None
    assignments = []
    idx = 0
    margin_per_group = {}
    for gk in sorted(groups.keys()):
        margin_per_group[gk] = False
        for comp in groups[gk]:
            if idx >= len(empty_slots): break
            slot = empty_slots[idx]
            # Leave 1 slot margin per group per row
            if not margin_per_group[gk]:
                # Check if this is the last available slot in this row
                remaining = sum(1 for j in range(idx+1, len(empty_slots)) if empty_slots[j]["shelf_id"]==slot["shelf_id"] and empty_slots[j]["row"]==slot["row"])
                if remaining == 0 and len([a for a in assignments if a["shelf_id"]==slot["shelf_id"] and a["row"]==slot["row"]]) > 0:
                    idx += 1
                    continue
            assignments.append({
                'component': comp, 'shelf_id': slot['shelf_id'],
                'shelf_name': slot['shelf_name'], 'row': slot['row'],
                'col': slot['col'], 'group': gk
            })
            idx += 1
    return {
        'assignments': assignments, 'total': len(assignments),
        'unassigned': len(components) - len(assignments),
        'groups': {k: len(v) for k, v in sorted(groups.items())}
    }

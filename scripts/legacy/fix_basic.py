import sys
c = open(sys.argv[1], 'r', encoding='utf-8-sig').read()
c = c.replace('cats=get_category_list(), stock_logs=[])', 'cats=get_category_list(), tree=get_category_tree(), stock_logs=[])')
c = c.replace(', tree={}, stock_logs=[])', ', tree=get_category_tree(), stock_logs=[])')
c = c.replace('stock_logs=logs, detail_view=True)', 'stock_logs=logs, detail_view=True, tree=get_category_tree())')
es = c.find('def export_excel')
ee = c.find('\ndef ', es + 1)
if ee < 0: ee = len(c)
ep = c[es:ee]
ep = ep.replace('ws.cell(row=2, column=col_idx, value=h)', 'ws.cell(row=1, column=col_idx, value=h)')
c = c[:es] + ep + c[ee:]
old = '            name = str(row[0] or "").strip()\n            model = str(row[1] or "").strip()\n            pkg = str(row[2] or "").strip()\n            specs = str(row[3] or "").strip()\n            qty_str = str(row[4] or "0").strip()\n            shelf_name = str(row[5] or "").strip()\n            row_num_str = str(row[6] or "").strip()\n            col_str = str(row[7] or "").strip()'
new = '            name = str(row[0] or "").strip()\n            specs = str(row[1] or "").strip()\n            pkg = str(row[2] or "").strip()\n            qty_str = str(row[3] or "0").strip()\n            min_stock_str = str(row[4] or "0").strip()\n            cat_name = str(row[5] or "").strip()\n            shelf_name = str(row[6] or "").strip()\n            row_num_str = str(row[7] or "").strip()\n            col_str = str(row[8] or "").strip()'
c = c.replace(old, new)
c = c.replace('            except ValueError:\n                qty = 0\n            if not name:', '            except ValueError:\n                qty = 0\n            try:\n                min_stock = int(float(min_stock_str))\n            except ValueError:\n                min_stock = 0\n            if not name:')
open(sys.argv[1], 'w', encoding='utf-8').write(c)
print('OK')

import sys
c = open(sys.argv[1], 'r', encoding='utf-8').read()

# Blueprint-style major+minor grid
c = c.replace('background-image: linear-gradient(rgba(99,110,114,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(99,110,114,0.08) 1px, transparent 1px); background-size: 20px 20px;',
'background-image:\n  linear-gradient(rgba(243,156,18,0.06) 1px, transparent 1px),\n  linear-gradient(90deg, rgba(243,156,18,0.06) 1px, transparent 1px),\n  linear-gradient(rgba(99,110,114,0.04) 1px, transparent 1px),\n  linear-gradient(90deg, rgba(99,110,114,0.04) 1px, transparent 1px);\nbackground-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;\nbackground-position: -1px -1px, -1px -1px, -1px -1px, -1px -1px;')

c = c.replace('background: #1a1a2e;', 'background: #141425;')

# Corner bracket on cards via pseudo-elements
old_card = '.card { background: #2d3436; border-radius: 6px; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.3); margin-bottom: 20px; border: 1px solid #4a4a5a; border-top: 3px solid #f39c12; }'
new_card = '.card { background: #2d3436; border-radius: 6px; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.3); margin-bottom: 20px; border: 1px solid #4a4a5a; position: relative; }\n.card::before { content: ""; position: absolute; top: -1px; left: -1px; width: 24px; height: 24px; border-top: 2px solid #f39c12; border-left: 2px solid #f39c12; border-radius: 4px 0 0 0; pointer-events: none; }\n.card::after { content: ""; position: absolute; bottom: -1px; right: -1px; width: 24px; height: 24px; border-bottom: 2px solid #f39c12; border-right: 2px solid #f39c12; border-radius: 0 0 4px 0; pointer-events: none; }'
c = c.replace(old_card, new_card)

# Stat card corner brackets
old_stat = '.stat-card { background: #2d3436; border-radius: 6px; padding: 20px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.3); border: 1px solid #4a4a5a; border-top: 3px solid #00b894; }'
new_stat = '.stat-card { background: #2d3436; border-radius: 6px; padding: 20px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.3); border: 1px solid #4a4a5a; position: relative; }\n.stat-card::before { content: ""; position: absolute; top: -1px; left: -1px; width: 18px; height: 18px; border-top: 2px solid #00b894; border-left: 2px solid #00b894; border-radius: 4px 0 0 0; pointer-events: none; }\n.stat-card::after { content: ""; position: absolute; bottom: -1px; right: -1px; width: 18px; height: 18px; border-bottom: 2px solid #00b894; border-right: 2px solid #00b894; border-radius: 0 0 4px 0; pointer-events: none; }'
c = c.replace(old_stat, new_stat)

open(sys.argv[1], 'w', encoding='utf-8').write(c)
print('OK')

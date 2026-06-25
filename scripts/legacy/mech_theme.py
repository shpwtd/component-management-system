import sys
c = open(sys.argv[1], 'r', encoding='utf-8').read()

c = c.replace('background: #f5f6fa', 'background: #1a1a2e')
c = c.replace('color: #2d3436; min-height: 100vh; }', 'color: #dfe6e9; min-height: 100vh; }')

# Grid overlay
c = c.replace('radial-gradient(circle, rgba(9,132,227,0.06) 1px, transparent 1px); background-size: 24px 24px', 'linear-gradient(rgba(99,110,114,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(99,110,114,0.08) 1px, transparent 1px); background-size: 20px 20px')

# Nav
c = c.replace('background: rgba(255,255,255,0.85); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-bottom: 1px solid rgba(255,255,255,0.3);', 'background: #16213e; border-bottom: 2px solid #f39c12; padding: 0 20px; position: sticky; top: 0; z-index: 100;')
c = c.replace('.nav a { color: #636e72; padding: 8px 16px; border-radius: 8px; font-size: 14px; font-weight: 500; transition: all 0.15s; }', '.nav a { color: #b2bec3; padding: 12px 16px; border-radius: 0; font-size: 14px; font-weight: 500; transition: all 0.2s; border-bottom: 2px solid transparent; }')
c = c.replace('.nav a:hover, .nav a.active { background: #dfe6e9; color: #2d3436; text-decoration: none; }', '.nav a:hover, .nav a.active { background: transparent; color: #f39c12; border-bottom-color: #f39c12; text-decoration: none; }')
c = c.replace('.nav .nav-brand { font-size: 18px; font-weight: 700; color: #2d3436; margin-right: 16px; }', '.nav .nav-brand { font-size: 18px; font-weight: 700; color: #f39c12; margin-right: 16px; }')

# Card
c = c.replace('.card { background: rgba(255,255,255,0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 12px; padding: 20px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.5); }', '.card { background: #2d3436; border-radius: 6px; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.3); margin-bottom: 20px; border: 1px solid #4a4a5a; border-top: 3px solid #f39c12; }')
c = c.replace('.card h2 { font-size: 18px; font-weight: 600; margin-bottom: 16px; }', '.card h2 { font-size: 18px; font-weight: 600; margin-bottom: 16px; color: #f39c12; }')
c = c.replace('.card h3 { font-size: 15px; font-weight: 600; margin-bottom: 10px; color: #636e72; }', '.card h3 { font-size: 15px; font-weight: 600; margin-bottom: 10px; color: #b2bec3; }')

# Stat card
c = c.replace('.stat-card { background: rgba(255,255,255,0.85); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 4px 24px rgba(0,0,0,0.06); border: 1px solid rgba(255,255,255,0.5); }', '.stat-card { background: #2d3436; border-radius: 6px; padding: 20px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.3); border: 1px solid #4a4a5a; border-top: 3px solid #00b894; }')
c = c.replace('.stat-card .stat-value { font-size: 36px; font-weight: 700; color: #0984e3; }', '.stat-card .stat-value { font-size: 36px; font-weight: 700; color: #f39c12; }')
c = c.replace('.stat-card .stat-label { font-size: 13px; color: #636e72; margin-top: 4px; }', '.stat-card .stat-label { font-size: 13px; color: #b2bec3; margin-top: 4px; }')
c = c.replace('.stat-card.warning .stat-value { color: #d63031; }', '.stat-card.warning .stat-value { color: #e74c3c; }')

# Buttons
c = c.replace('.btn-primary { background: #0984e3; color: #fff; }', '.btn-primary { background: #f39c12; color: #1a1a2e; font-weight: 600; }')
c = c.replace('.btn-danger { background: #d63031; color: #fff; }', '.btn-danger { background: #e74c3c; color: #fff; }')
c = c.replace('.btn-secondary { background: #dfe6e9; color: #2d3436; }', '.btn-secondary { background: transparent; color: #b2bec3; border: 1px solid #4a4a5a; }')
c = c.replace('.btn-outline { background: transparent; border: 1px solid #b2bec3; color: #636e72; }', '.btn-outline { background: transparent; border: 1px solid #4a4a5a; color: #b2bec3; }')
c = c.replace('.btn:hover { text-decoration: none; opacity: 0.9; }', '.btn:hover { text-decoration: none; opacity: 0.9; transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.3); }')

# Tables
c = c.replace('th, td { padding: 10px 12px; text-align: left; border: 1px solid #dfe6e9; white-space: nowrap; }', 'th, td { padding: 10px 12px; text-align: left; border: 1px solid #4a4a5a; white-space: nowrap; color: #dfe6e9; }')
c = c.replace('th { font-weight: 600; color: #636e72; background: #fafafa; position: sticky; top: 0; }', 'th { font-weight: 600; color: #f39c12; background: #1a1a2e; position: sticky; top: 0; border-bottom: 2px solid #f39c12; }')
c = c.replace('tr:hover td { background: #f8f9fa; }', 'tr:hover td { background: #353b48; }')

# Forms
c = c.replace('.form-group label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 4px; color: #2d3436; }', '.form-group label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 4px; color: #dfe6e9; }')
c = c.replace('.form-control { width: 100%; padding: 8px 12px; border: 1px solid #dfe6e9; border-radius: 8px; font-size: 14px; transition: border-color 0.15s; }', '.form-control { width: 100%; padding: 8px 12px; border: 1px solid #4a4a5a; border-radius: 4px; font-size: 14px; transition: border-color 0.15s; background: #1a1a2e; color: #dfe6e9; }')
c = c.replace('.form-control:focus { outline: none; border-color: #0984e3; box-shadow: 0 0 0 3px rgba(9,132,227,0.1); }', '.form-control:focus { outline: none; border-color: #f39c12; box-shadow: 0 0 0 3px rgba(243,156,18,0.2); }')
c = c.replace('select.form-control { background: #fff; }', 'select.form-control { background: #1a1a2e; color: #dfe6e9; }')
c = c.replace('.form-actions { display: flex; gap: 8px; margin-top: 20px; padding-top: 16px; border-top: 1px solid #dfe6e9; }', '.form-actions { display: flex; gap: 8px; margin-top: 20px; padding-top: 16px; border-top: 1px solid #4a4a5a; }')

# Alerts
c = c.replace('.alert-danger { background: #ffeaa7; color: #d63031; border-left: 4px solid #d63031; }', '.alert-danger { background: rgba(231,76,60,0.15); color: #e74c3c; border: 1px solid #e74c3c; border-left: 4px solid #e74c3c; }')
c = c.replace('.alert-info { background: #dfe6e9; color: #2d3436; border-left: 4px solid #0984e3; }', '.alert-info { background: rgba(9,132,227,0.15); color: #74b9ff; border: 1px solid #0984e3; border-left: 4px solid #0984e3; }')
c = c.replace('.alert-success { background: #55efc4; color: #00b894; border-left: 4px solid #00b894; }', '.alert-success { background: rgba(0,184,148,0.15); color: #00b894; border: 1px solid #00b894; border-left: 4px solid #00b894; }')

# Shelf cells
c = c.replace('border: 1px dashed #b2bec3; border-radius: 6px; font-size: 11px; color: #b2bec3;', 'border: 1px dashed #4a4a5a; border-radius: 4px; font-size: 11px; color: #636e72;')
c = c.replace('.shelf-cell:hover { border-color: #0984e3; background: rgba(9,132,227,0.04); }', '.shelf-cell:hover { border-color: #f39c12; background: rgba(243,156,18,0.06); }')
c = c.replace('.shelf-cell.occupied { border-style: solid; border-color: #0984e3; background: rgba(9,132,227,0.06); cursor: pointer; padding: 0; }', '.shelf-cell.occupied { border-style: solid; border-color: #4a4a5a; background: #2d3436; cursor: pointer; padding: 0; }')
c = c.replace('.shelf-cell.occupied.low-stock { border-color: #d63031; background: rgba(214,48,49,0.06); }', '.shelf-cell.occupied.low-stock { border-color: #e74c3c; background: rgba(231,76,60,0.1); }')

# Category badges
c = c.replace('.cat-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; }', '.cat-badge { display: inline-block; padding: 2px 8px; border-radius: 2px; font-size: 11px; font-weight: 500; }')

# Page header
c = c.replace('.page-header h1 { font-size: 24px; font-weight: 700; }', '.page-header h1 { font-size: 24px; font-weight: 700; color: #f39c12; }')

# Filter bar
c = c.replace('border: 1px solid #dfe6e9; border-radius: 8px;', 'border: 1px solid #4a4a5a; border-radius: 4px; background: #1a1a2e; color: #dfe6e9;')

# Page-header action buttons area - fix link colors
c = c.replace('.page-header a { color: #0984e3; }', '.page-header a { color: #74b9ff; }' if '.page-header a { color: #0984e3; }' in c else c)

# Shelf grid title
c = c.replace('.shelf-title span { font-size: 16px; font-weight: 600; }', '.shelf-title span { font-size: 16px; font-weight: 600; color: #f39c12; }' if '.shelf-title span { font-size: 16px; font-weight: 600; }' in c else c)

# Dashboard grid
c = c.replace('.dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }', '.dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }')

# Add some padding to nav button area
c = c.replace('.nav a { color: #b2bec3; padding: 12px 16px;', '.nav a { color: #b2bec3; padding: 14px 18px;')

# Low stock animation for shelf cells
old_low = '.shelf-cell.occupied.low-stock { border-color: #e74c3c; background: rgba(231,76,60,0.1); }'
new_low = '.shelf-cell.occupied.low-stock { border-color: #e74c3c; background: rgba(231,76,60,0.1); animation: pulse-alert 1.5s infinite; }'
if old_low in c:
    c = c.replace(old_low, new_low)

# Add keyframe animation
anim = '\n@keyframes pulse-alert {\n  0%, 100% { box-shadow: 0 0 0 0 rgba(231,76,60,0.3); }\n  50% { box-shadow: 0 0 0 6px rgba(231,76,60,0); }\n}'
c += anim

open(sys.argv[1], 'w', encoding='utf-8').write(c)
print('OK')

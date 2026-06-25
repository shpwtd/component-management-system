import sys, os
sys.stdout = open('server.log', 'w', encoding='utf-8')
sys.stderr = sys.stdout
os.chdir(r'D:\codexspace\元器件管理系统')
from app import app
app.run(host='127.0.0.1', port=5000, debug=False)

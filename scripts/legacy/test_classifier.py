import sys
sys.path.insert(0, '.')
from classifier import *
t = get_category_tree()
for k, v in sorted(t.items()):
    print(k, '-', v.get('name'), 'subs:', len(v.get('children',[])))

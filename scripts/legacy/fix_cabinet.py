import sys
c = open(sys.argv[1], "r", encoding="utf-8").read()

# 1. Move box close after stats (remove before stats, add after stats)
c = c.replace("</div>\n</div>\n<div class=\"cabinet-stats\">", "</div>\n<div class=\"cabinet-stats\">")
c = c.replace("</div>\n</div>\n<div class=\"cabinet-expanded\">", "</div>\n</div>\n</div>\n<div class=\"cabinet-expanded\">")

# 2. Change for-else to if-for-endfor-else-endif + shelf-fleet
c = c.replace("{% for shelf in shelves %}\n{% set sdata", "{% if shelves %}\n<div class=\"shelf-fleet\">\n{% for shelf in shelves %}\n{% set sdata")
c = c.replace("{% else %}\n<div class=\"empty-state\"><p>\u8fd8\u6ca1\u6709\u8d27\u67b6</p><a href=\"/shelves/add\" class=\"btn btn-primary\">\u6dfb\u52a0\u8d27\u67b6</a></div>\n{% endfor %}", "{% endfor %}\n</div>\n{% else %}\n<div class=\"empty-state\"><p>\u8fd8\u6ca1\u6709\u8d27\u67b6</p><a href=\"/shelves/add\" class=\"btn btn-primary\">\u6dfb\u52a0\u8d27\u67b6</a></div>\n{% endif %}")

# 3. Add shelf-fleet CSS
css = open(sys.argv[2], "r", encoding="utf-8").read()
css = css.replace(".cabinet-face:hover .cabinet-box { border-color: #f39c12; }", ".cabinet-face:hover .cabinet-box { border-color: #f39c12; }\n.shelf-fleet { display: flex; flex-wrap: wrap; gap: 16px; }")
open(sys.argv[2], "w", encoding="utf-8").write(css)

open(sys.argv[1], "w", encoding="utf-8").write(c)
print("OK")

import os
BASE = "."
path = os.path.join(BASE, "app.py")
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Add try/except to categories_page
idx = c.index("def categories_page():")
end = c.index("def category_delete", idx)
section = c[idx:end]

# Add try after the def line
def_line = "def categories_page():"
try_line = "def categories_page():\n    try:"
section = section.replace(def_line, try_line)

# Find the final return and add except before it
last_return = section.rindex("return render_template")
# Add except after the last line of the function
section = section + "\n    except Exception as e:\n        import logging,traceback\n        logging.error(f\"Categories error: {traceback.format_exc()}\")\n        return f\"<pre>{traceback.format_exc()}</pre>\", 500, {\"Content-Type\": \"text/html\"}"

c = c[:idx] + section + c[end:]

with open(path, "w", encoding="utf-8") as f:
    f.write(c)
print("Categories route try/except added")

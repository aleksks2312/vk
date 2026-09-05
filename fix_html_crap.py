import re

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the python syntax
html = html.replace('import base64\n\nhtml_template = """', '')

if html.endswith('"""'):
    html = html[:-3]

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

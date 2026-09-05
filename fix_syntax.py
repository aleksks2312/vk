import re
with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Убираем дубликат
parts = html.split('let starShowerTime = 0;')
if len(parts) > 2:
    html = parts[0] + 'let starShowerTime = 0;' + parts[1] + parts[2]

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

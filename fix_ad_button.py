import os

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_btn = '<button class="btn-small" onclick="showAd()">Смотреть (+100 <svg class="dust-inline" viewBox="0 0 24 24"><path d="M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9L12 2Z"/></svg>)</button>'
new_btn = '<button class="btn-small" onclick="showAd()">Смотреть (x10 <svg class="dust-inline" viewBox="0 0 24 24"><path d="M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9L12 2Z"/></svg> на 30с)</button>'

html = html.replace(old_btn, new_btn)

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Button text replaced successfully.")

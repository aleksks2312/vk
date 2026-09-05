import base64

with open('tarot_app.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Встраиваем гадалку
try:
    with open('fortune_teller.jpg', 'rb') as img:
        b64 = base64.b64encode(img.read()).decode('utf-8')
        html = html.replace("IMG_TELLER_PLACEHOLDER", f"data:image/jpeg;base64,{b64}")
except:
    pass

# 2. Встраиваем колоду
images = {
    "IMG_FOOL": "fool.jpg",
    "IMG_MAGICIAN": "magician.jpg",
    "IMG_PRIESTESS": "priestess.jpg",
    "IMG_EMPRESS": "empress.jpg",
    "IMG_CHARIOT": "chariot.jpg",
    "IMG_SUN": "sun.jpg"
}

for placeholder, filename in images.items():
    try:
        with open(filename, 'rb') as img_file:
            b64 = base64.b64encode(img_file.read()).decode('utf-8')
            html = html.replace(placeholder, f"data:image/jpeg;base64,{b64}")
    except:
        pass

with open('tarot_app.html', 'w', encoding='utf-8') as f:
    f.write(html)

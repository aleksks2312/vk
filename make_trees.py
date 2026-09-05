from PIL import Image, ImageEnhance
import os

os.makedirs('tarot-app/images/optimized', exist_ok=True)

def process_tree(src, dst):
    try:
        img = Image.open(src).convert('RGB')
        # Обрезаем квадрат по центру
        size = min(img.width, img.height)
        left = (img.width - size) / 2
        top = (img.height - size) / 2
        img = img.crop((left, top, left + size, top + size))
        img = img.resize((400, 400), Image.Resampling.LANCZOS)
        
        # Усиливаем контраст, чтобы фон стал идеально черным (нужно для режима смешивания CSS)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.4)
        
        img.save(dst, quality=90)
        print(f"✅ Готово: {dst}")
    except Exception as e:
        print(f"❌ Ошибка с {src}: {e}")

process_tree('tarot-app/images/v2_lvl1.jpg', 'tarot-app/images/optimized/tree_1.jpg')
process_tree('tarot-app/images/v2_lvl5.jpg', 'tarot-app/images/optimized/tree_5.jpg')
process_tree('tarot-app/images/v2_lvl10.jpg', 'tarot-app/images/optimized/tree_10.jpg')
process_tree('tarot-app/images/v2_lvl15.jpg', 'tarot-app/images/optimized/tree_15.jpg')
process_tree('tarot-app/images/v2_lvl20.jpg', 'tarot-app/images/optimized/tree_20.jpg')

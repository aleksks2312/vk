from PIL import Image
import os

def resize_image(src, dst, size):
    try:
        img = Image.open(src).convert('RGB')
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(dst, quality=85)
        print(f"✅ {dst} -> {size}")
    except Exception as e:
        print(f"Error {src}: {e}")

resize_image('tarot-app/images/bg_bronze.jpg', 'tarot-app/images/optimized/bg_bronze.jpg', (1080, 1920))
resize_image('tarot-app/images/bg_silver.jpg', 'tarot-app/images/optimized/bg_silver.jpg', (1080, 1920))
resize_image('tarot-app/images/bg_gold.jpg', 'tarot-app/images/optimized/bg_gold.jpg', (1080, 1920))

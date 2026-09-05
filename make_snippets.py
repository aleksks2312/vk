from PIL import Image
import os

def resize_crop(src, dst, size):
    try:
        img = Image.open(src).convert('RGB')
        img_ratio = img.width / img.height
        target_ratio = size[0] / size[1]
        
        if img_ratio > target_ratio:
            new_height = size[1]
            new_width = int(new_height * img_ratio)
        else:
            new_width = size[0]
            new_height = int(new_width / img_ratio)
            
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        left = (img.width - size[0]) / 2
        top = (img.height - size[1]) / 2
        right = (img.width + size[0]) / 2
        bottom = (img.height + size[1]) / 2
        
        img = img.crop((left, top, right, bottom))
        img.save(dst, quality=95)
        print(f"✅ Создан {dst} ({size[0]}x{size[1]})")
    except Exception as e:
        print(f"❌ Ошибка {src}: {e}")

# Создаем все форматы сниппетов из базового raw_snippet
base_snippet = "tarot-app/images/raw_snippet.jpg"
resize_crop(base_snippet, "tarot-app/images/vk_snippet_537x240.jpg", (537, 240))
resize_crop(base_snippet, "tarot-app/images/vk_snippet_1080x400.jpg", (1080, 400))
resize_crop(base_snippet, "tarot-app/images/vk_snippet_1120x630.jpg", (1120, 630))

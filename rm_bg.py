import numpy as np
from PIL import Image

def remove_black_background(src, dst):
    try:
        img = Image.open(src).convert('RGBA')
        data = np.array(img)
        
        # Берем RGB каналы
        r = data[:,:,0].astype(float)
        g = data[:,:,1].astype(float)
        b = data[:,:,2].astype(float)
        
        # Альфа-канал рассчитываем на основе яркости (свечения)
        a = np.maximum(np.maximum(r, g), b)
        
        # Защита от деления на ноль
        a_safe = np.where(a == 0, 1, a)
        
        # Восстанавливаем оригинальные цвета (компенсируя прозрачность)
        r = np.clip(r * 255.0 / a_safe, 0, 255)
        g = np.clip(g * 255.0 / a_safe, 0, 255)
        b = np.clip(b * 255.0 / a_safe, 0, 255)
        
        # Обновляем пиксели
        data[:,:,0] = r
        data[:,:,1] = g
        data[:,:,2] = b
        data[:,:,3] = a  # Свечение становится полупрозрачностью
        
        out_img = Image.fromarray(data.astype(np.uint8), 'RGBA')
        out_img.save(dst)
        print(f"✅ Успешно удален фон: {dst}")
    except Exception as e:
        print(f"❌ Ошибка с {src}: {e}")

# Обрабатываем все 5 картинок
levels = [1, 5, 10, 15, 20]
for lvl in levels:
    remove_black_background(f'tarot-app/images/optimized/tree_{lvl}.jpg', f'tarot-app/images/optimized/tree_{lvl}.png')

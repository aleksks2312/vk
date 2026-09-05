import os

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Исправляем CSS экрана (убираем z-index: 10 и position: relative, которые ломали слои)
old_screen = ".screen { display: none; flex-direction: column; align-items: center; padding: 0 20px 100px 20px; animation: fadeIn 0.5s ease; width: 100%; box-sizing: border-box; position: relative; z-index: 10;}"
new_screen = ".screen { display: none; flex-direction: column; align-items: center; padding: 0 20px 100px 20px; width: 100%; box-sizing: border-box; }"
content = content.replace(old_screen, new_screen)

# Убираем анимацию, чтобы она тоже не создавала временных конфликтов слоев
content = content.replace("@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }", "")

# 2. Исправляем подсветку обучения (убираем темный фон, оставляем только свечение)
old_highlight = ".tut-highlight { position: relative !important; z-index: 99995 !important; border-radius: 12px; animation: pulseTut 2s infinite !important; background: rgba(26,15,36, 0.9); pointer-events: auto !important; }"
new_highlight = ".tut-highlight { position: relative !important; z-index: 99995 !important; border-radius: 12px; animation: pulseTut 2s infinite !important; background: transparent !important; pointer-events: auto !important; }"
content = content.replace(old_highlight, new_highlight)

# 3. Убираем костыль с pointerEvents (который мешал нажимать)
old_js_step = """            else if(tutStep === 2) {
                title.innerText = "Нить Судьбы";
                text.innerHTML = `Отлично! Твой вопрос отправлен в астрал. Теперь <b>коснись колоды</b>, чтобы вытянуть Карту Дня и услышать ответ духов.`;
                btn.style.display = 'none'; 
                skipBtn.style.display = 'none'; 
                document.getElementById('tutOverlay').style.pointerEvents = 'none'; 
                document.getElementById('card').classList.add('tut-highlight');
            }
            else if(tutStep === 3) {
                document.getElementById('tutOverlay').style.pointerEvents = 'auto';
                btn.style.display = 'block';"""

new_js_step = """            else if(tutStep === 2) {
                title.innerText = "Нить Судьбы";
                text.innerHTML = `Отлично! Твой вопрос отправлен в астрал. Теперь <b>коснись колоды</b>, чтобы вытянуть Карту Дня и услышать ответ духов.`;
                btn.style.display = 'none'; 
                skipBtn.style.display = 'none'; 
                document.getElementById('card').classList.add('tut-highlight');
            }
            else if(tutStep === 3) {
                btn.style.display = 'block';"""
content = content.replace(old_js_step, new_js_step)

old_js_skip = """            document.querySelectorAll('.tut-highlight').forEach(el => el.classList.remove('tut-highlight'));
            document.getElementById('tutOverlay').style.pointerEvents = 'all'; // Возвращаем как было
            switchTab('divination', document.getElementById('navItem_divination'));"""
            
new_js_skip = """            document.querySelectorAll('.tut-highlight').forEach(el => el.classList.remove('tut-highlight'));
            switchTab('divination', document.getElementById('navItem_divination'));"""
content = content.replace(old_js_skip, new_js_skip)

# 4. Меняем ключ, чтобы туториал 100% запустился у пользователя сейчас для проверки
content = content.replace("tutorialDone_v3", "tutorialDone_v4")

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Код успешно пропатчен!")
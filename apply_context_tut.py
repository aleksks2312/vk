import os

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. FIX THE BACKGROUND IMAGES IN GRIMOIRE
bg_gallery_old = """        <div class="bg-gallery" id="bgGallery">
            <div class="bg-item active-bg" id="bg_vk_story_bg.jpg" style="background-image: url('/images/optimized/vk_story_bg.jpg')" onclick="previewBg(1, 'vk_story_bg.jpg', 'Космос')">
                <div class="bg-label">Космос (Ур. 1)</div>
            </div>
            <div class="bg-item" id="bg_bg_bronze.jpg" style="background-image: url('/images/optimized/vk_story_bg.jpg')" onclick="previewBg(5, 'bg_bronze.jpg', 'Бронза')">
                <div class="bg-lock" id="lock_bg_bronze.jpg">🔒</div><div class="bg-label">Бронза (Ур. 5)</div>
            </div>
            <div class="bg-item" id="bg_bg_silver.jpg" style="background-image: url('/images/optimized/vk_story_bg.jpg')" onclick="previewBg(10, 'bg_silver.jpg', 'Серебро')">
                <div class="bg-lock" id="lock_bg_silver.jpg">🔒</div><div class="bg-label">Серебро (Ур. 10)</div>
            </div>
            <div class="bg-item" id="bg_bg_gold.jpg" style="background-image: url('/images/optimized/vk_story_bg.jpg')" onclick="previewBg(20, 'bg_gold.jpg', 'Золото')">
                <div class="bg-lock" id="lock_bg_gold.jpg">🔒</div><div class="bg-label">Золото (Ур. 20)</div>
            </div>
        </div>"""

bg_gallery_new = """        <div class="bg-gallery" id="bgGallery">
            <div class="bg-item active-bg" id="bg_vk_story_bg.jpg" style="background-image: url('/images/optimized/vk_story_bg.jpg')" onclick="previewBg(1, 'vk_story_bg.jpg', 'Космос')">
                <div class="bg-label">Космос (Ур. 1)</div>
            </div>
            <div class="bg-item" id="bg_bg_bronze.jpg" style="background-image: url('/images/optimized/bg_bronze.jpg')" onclick="previewBg(5, 'bg_bronze.jpg', 'Бронза')">
                <div class="bg-lock" id="lock_bg_bronze.jpg">🔒</div><div class="bg-label">Бронза (Ур. 5)</div>
            </div>
            <div class="bg-item" id="bg_bg_silver.jpg" style="background-image: url('/images/optimized/bg_silver.jpg')" onclick="previewBg(10, 'bg_silver.jpg', 'Серебро')">
                <div class="bg-lock" id="lock_bg_silver.jpg">🔒</div><div class="bg-label">Серебро (Ур. 10)</div>
            </div>
            <div class="bg-item" id="bg_bg_gold.jpg" style="background-image: url('/images/optimized/bg_gold.jpg')" onclick="previewBg(20, 'bg_gold.jpg', 'Золото')">
                <div class="bg-lock" id="lock_bg_gold.jpg">🔒</div><div class="bg-label">Золото (Ур. 20)</div>
            </div>
        </div>"""

html = html.replace(bg_gallery_old, bg_gallery_new)


# 2. FIX CSS - REMOVE HIGHLIGHT ANIMATION AND TUTORIAL CLASSES
css_start = html.find('/* --- ИНТЕРАКТИВНЫЙ ТУТОРИАЛ --- */')
css_end = html.find('/* Обычные модалки */')

new_css = """/* --- ТУТОРИАЛ (КОНТЕКСТНЫЙ) --- */
        .tutorial-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); z-index: 99990; display: none; flex-direction: column; align-items: center; justify-content: center; box-sizing: border-box; opacity: 0; transition: opacity 0.3s; pointer-events: none;}
        .tutorial-overlay.active { display: flex; opacity: 1; pointer-events: auto;}
        .tutorial-dialog { background: linear-gradient(180deg, #170a24 0%, #0a0410 100%); border: 2px solid var(--gold); border-radius: 15px; padding: 25px; width: 90%; max-width: 340px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.8); z-index: 99999; pointer-events: auto; }
        .tutorial-dialog h3 { color: var(--gold); font-family: 'Cinzel', serif; margin: 0 0 15px 0; font-size: 22px; }
        .tutorial-dialog p { color: #d8cce6; font-size: 15px; line-height: 1.4; margin: 0 0 20px 0; }
        
        /* Свечение элементов */
        .tut-highlight { position: relative; border-radius: 12px; animation: pulseTut 2s infinite !important; }
        @keyframes pulseTut { 0% { box-shadow: 0 0 10px rgba(212,175,55,0.4); } 50% { box-shadow: 0 0 30px rgba(212,175,55,1); } 100% { box-shadow: 0 0 10px rgba(212,175,55,0.4); } }

        """
html = html[:css_start] + new_css + html[css_end:]


# 3. FIX HTML TUTORIAL MODAL
tut_html_start = html.find('<!-- ТУТОРИАЛ -->')
tut_html_end = html.find('<div class="smoke-container">')

new_tut_html = """<!-- КОНТЕКСТНЫЙ ТУТОРИАЛ -->
    <div class="tutorial-overlay" id="tutOverlay">
        <div class="tutorial-dialog">
            <h3 id="tutTitle">Привет, Путник!</h3>
            <p id="tutText">Текст обучения...</p>
            <button class="btn" id="tutNextBtn" style="margin: 0 auto;">Понятно</button>
        </div>
    </div>

    """
html = html[:tut_html_start] + new_tut_html + html[tut_html_end:]


# 4. FIX JS TUTORIAL LOGIC
js_tut_start = html.find('// --- ЛОГИКА ТУТОРИАЛА ---')
js_tut_end = html.find('initGrimoire();')

new_js_tut = """// --- ЛОГИКА КОНТЕКСТНОГО ТУТОРИАЛА ---

        function checkTutorial() {
            // Проверяем туториал для текущего активного таба
            const activeTab = document.querySelector('.screen.active').id.replace('screen-', '');
            
            if(activeTab === 'divination' && !localStorage.getItem('tut_divination')) {
                showTutDialog(
                    "Голос Вселенной", 
                    `Приветствую, <b>${userName}</b>! Я — дух этого Гримуара. Впиши свой сокровенный вопрос в подсвеченное поле, а затем коснись колоды, чтобы вытянуть Карту Дня.`,
                    () => {
                        hideTutDialog();
                        localStorage.setItem('tut_divination', '1');
                        document.getElementById('stepQuestion').classList.add('tut-highlight');
                        document.getElementById('card').classList.add('tut-highlight');
                    }
                );
            } 
            else if(activeTab === 'altar' && !localStorage.getItem('tut_altar')) {
                showTutDialog(
                    "Алтарь Судьбы", 
                    "Это сердце твоей магии. Кликай по кристаллу, чтобы собирать ✨ Звездную пыль. Чем выше уровень Алтаря, тем больше ежедневная награда и тем круче фоны для Историй ВК!",
                    () => {
                        hideTutDialog();
                        localStorage.setItem('tut_altar', '1');
                        document.getElementById('altarCrystal').classList.add('tut-highlight');
                        setTimeout(() => document.getElementById('altarCrystal').classList.remove('tut-highlight'), 3000);
                    }
                );
            }
            else if(activeTab === 'grimoire' && !localStorage.getItem('tut_grimoire')) {
                showTutDialog(
                    "Великие Артефакты", 
                    "Здесь хранится твоя коллекция Арканов. Повышай свой ранг и открывай новые фоны для Историй. Пусть все увидят твой статус!",
                    () => {
                        hideTutDialog();
                        localStorage.setItem('tut_grimoire', '1');
                        document.getElementById('bgGallery').classList.add('tut-highlight');
                        setTimeout(() => document.getElementById('bgGallery').classList.remove('tut-highlight'), 3000);
                    }
                );
            }
            else if(activeTab === 'rituals' && !localStorage.getItem('tut_rituals')) {
                showTutDialog(
                    "Жертва Магии", 
                    "Гадание расходует твою ⚡ Энергию. Здесь ты можешь восстановить её: выполняй ежедневные ритуалы, смотри видения или приглашай друзей.",
                    () => {
                        hideTutDialog();
                        localStorage.setItem('tut_rituals', '1');
                    }
                );
            }
        }

        function showTutDialog(title, text, action) {
            document.getElementById('tutTitle').innerText = title;
            document.getElementById('tutText').innerHTML = text;
            const btn = document.getElementById('tutNextBtn');
            btn.onclick = action;
            
            const overlay = document.getElementById('tutOverlay');
            overlay.style.display = 'flex';
            setTimeout(() => overlay.classList.add('active'), 10);
        }

        function hideTutDialog() {
            const overlay = document.getElementById('tutOverlay');
            overlay.classList.remove('active');
            setTimeout(() => overlay.style.display = 'none', 300);
        }

        // Обновляем switchTab, чтобы при переходе чекался туториал
        const originalSwitchTab = switchTab;
        window.switchTab = function(tabId, element) {
            originalSwitchTab(tabId, element);
            // Удаляем старые подсветки
            document.querySelectorAll('.tut-highlight').forEach(el => el.classList.remove('tut-highlight'));
            setTimeout(checkTutorial, 300);
        }

        function replayTutorial() {
            localStorage.removeItem('tut_divination');
            localStorage.removeItem('tut_altar');
            localStorage.removeItem('tut_grimoire');
            localStorage.removeItem('tut_rituals');
            energy = 1;
            updateStatsUI();
            if(isFlipped) resetCardManual();
            switchTab('divination', document.getElementById('navItem_divination'));
        }

        """
html = html[:js_tut_start] + new_js_tut + html[js_tut_end:]

# 5. FIX THE DRAW CARD API HIGHLIGHT REMOVAL + SUCCESS DIALOG
draw_start = html.find('const question = document.getElementById(\'userQuestion\').value;')
draw_end = html.find('if(!collectedCards.includes(randomIndex)) {')

new_draw_middle = """const question = document.getElementById('userQuestion').value;
            const aiRespElem = document.getElementById('aiResponse');
            
            // Убираем подсветку обучения
            document.getElementById('stepQuestion').classList.remove('tut-highlight');
            document.getElementById('card').classList.remove('tut-highlight');
            
            if(question.trim() !== '') {
                aiRespElem.style.display = 'block';
                aiRespElem.innerText = "✨ Духи читают твой вопрос...";
                fetch('/api/draw', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ vk_sign: window.location.search.substring(1), vk_id: 1, card_index: randomIndex, question: question })
                })
                .then(res => res.json())
                .then(data => { 
                    aiRespElem.innerText = data.ai_text ? data.ai_text : "Ответ скрыт в тумане..."; 
                    checkDrawTutorial();
                })
                .catch(e => { 
                    aiRespElem.innerText = "Астральная связь прервалась..."; 
                    checkDrawTutorial();
                });
            } else { 
                aiRespElem.style.display = 'none'; 
                checkDrawTutorial();
            }

            function checkDrawTutorial() {
                if(!localStorage.getItem('tut_draw_done')) {
                    localStorage.setItem('tut_draw_done', '1');
                    setTimeout(() => {
                        showTutDialog(
                            "Судьба открыта",
                            "Магия свершилась! Но помни, Энергия ⚡ истощилась. Загляни во вкладку <b>Ритуалы</b> или <b>Алтарь</b>, чтобы продолжить путь.",
                            "Ясно",
                            () => hideTutDialog()
                        );
                    }, 500);
                }
            }

            """
html = html[:draw_start] + new_draw_middle + html[draw_end:]

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

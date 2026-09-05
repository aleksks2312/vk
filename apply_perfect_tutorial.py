import re

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ЧИСТИМ CSS ТУТОРИАЛА
css_start = html.find('/* --- ИНТЕРАКТИВНЫЙ ТУТОРИАЛ --- */')
css_end = html.find('/* Обычные модалки */')

new_css = """/* --- ИНТЕРАКТИВНЫЙ ТУТОРИАЛ --- */
        .tutorial-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); z-index: 99990; display: none; flex-direction: column; justify-content: center; align-items: center; padding-bottom: 50px; box-sizing: border-box; opacity: 0; transition: opacity 0.3s;}
        .tutorial-overlay.active { display: flex; opacity: 1; }
        .tutorial-dialog { background: linear-gradient(180deg, #170a24 0%, #0a0410 100%); border: 2px solid var(--gold); border-radius: 15px; padding: 25px; width: 90%; max-width: 340px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.8); position: relative; z-index: 99999;}
        .tutorial-dialog h3 { color: var(--gold); font-family: 'Cinzel', serif; margin: 0 0 15px 0; font-size: 22px; }
        .tutorial-dialog p { color: #d8cce6; font-size: 15px; line-height: 1.4; margin: 0 0 20px 0; }
        .tut-buttons { display: flex; flex-direction: column; align-items: center;}
        
        .tut-highlight { position: relative; border-radius: 12px; animation: pulseTut 2s infinite !important; }
        @keyframes pulseTut { 0% { box-shadow: 0 0 10px rgba(212,175,55,0.4), 0 0 0px rgba(212,175,55,0.4); } 50% { box-shadow: 0 0 30px rgba(212,175,55,1), 0 0 10px rgba(212,175,55,0.8); } 100% { box-shadow: 0 0 10px rgba(212,175,55,0.4), 0 0 0px rgba(212,175,55,0.4); } }

        """
html = html[:css_start] + new_css + html[css_end:]

# Убираем старый класс body.tut-mode
html = html.replace("body.tut-mode { pointer-events: none; }", "")
html = html.replace("body.tut-mode .tutorial-overlay { pointer-events: auto; }", "")
html = html.replace("body.tut-mode .tut-highlight { pointer-events: auto !important; position: relative !important; z-index: 99995 !important; }", "")

# 2. МЕНЯЕМ HTML ТУТОРИАЛА
tut_html_start = html.find('<!-- ИНТЕРАКТИВНОЕ ОБУЧЕНИЕ -->')
tut_html_end = html.find('<div class="smoke-container">')

new_tut_html = """<!-- ИНТЕРАКТИВНОЕ ОБУЧЕНИЕ -->
    <div class="tutorial-overlay" id="tutOverlay">
        <div class="tutorial-dialog">
            <h3 id="tutTitle">Привет, Путник!</h3>
            <p id="tutText">Я — дух этого Гримуара. Позволь мне открыть для тебя мир магии Таро...</p>
            <div class="tut-buttons">
                <button class="btn" id="tutNextBtn">Продолжить</button>
                <button class="btn-small" style="border:none; margin-top:15px; font-size:12px; opacity:0.7;" onclick="skipTutorialBtn()">Пропустить обучение</button>
            </div>
        </div>
    </div>

    <!-- МОДАЛКА ПРОПУСКА -->
    <div class="modal-overlay" id="tutSkipModal" onclick="closeModal('tutSkipModal', event)">
        <div class="info-box" style="text-align: center;" onclick="event.stopPropagation()">
            <h2 style="font-family: 'Cinzel', serif; color: var(--gold); margin-top:0;">Ты уверен?</h2>
            <p style="color: #d8cce6; font-size: 15px; margin-bottom: 20px;">Мир магии невероятно сложен. Без проводника ты можешь заблудиться в астрале...</p>
            <button class="btn" style="margin-bottom: 15px;" onclick="forceSkipTutorial()">Да, я справлюсь сам</button>
            <button class="btn-small" style="background: transparent; border: 1px solid var(--gold); color: var(--gold); display: inline-block;" onclick="closeModal('tutSkipModal')">Остаться с духом</button>
        </div>
    </div>

    """
html = html[:tut_html_start] + new_tut_html + html[tut_html_end:]


# 3. МЕНЯЕМ JS ФУНКЦИЮ drawCardApi (Добавляем вызов туториала ПОСЛЕ ответа ИИ)
js_draw_start = html.find('function drawCardApi() {')
js_draw_end = html.find('function publishStoryVK() {')

new_draw_js = """function drawCardApi() {
            if(isFlipped) return;
            if(energy <= 0) {
                alert("У вас нет Энергии ⚡! Выполните Ритуал (пригласите друга или опубликуйте историю), чтобы получить попытку.");
                switchTab('rituals', document.getElementById('navItem_rituals'));
                return;
            }
            
            energy--;
            initGrimoire();
            
            const randomIndex = Math.floor(Math.random() * tarotDeck.length);
            const randomCard = tarotDeck[randomIndex];
            currentDrawnCardImg = randomCard.img;

            document.getElementById('cardNumber').innerText = randomCard.num;
            document.getElementById('cardName').innerText = randomCard.name;
            document.getElementById('cardDesc').innerText = randomCard.desc;
            document.getElementById('cardBack').style.backgroundImage = `linear-gradient(180deg, rgba(23, 10, 36, 0.75) 0%, rgba(10, 4, 16, 0.95) 100%), url('https://tarot-app-pearl-five.vercel.app${randomCard.img}')`;
            document.getElementById('cardBack').style.backgroundSize = 'cover';

            document.getElementById('card').classList.add('flipped');

            const question = document.getElementById('userQuestion').value;
            const aiRespElem = document.getElementById('aiResponse');
            
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
                    if(isTutorialActive && tutStep === 2) setTimeout(continueTutorialAfterDraw, 1500);
                })
                .catch(e => { 
                    aiRespElem.innerText = "Астральная связь прервалась..."; 
                    if(isTutorialActive && tutStep === 2) setTimeout(continueTutorialAfterDraw, 1500);
                });
            } else { 
                aiRespElem.style.display = 'none'; 
                if(isTutorialActive && tutStep === 2) setTimeout(continueTutorialAfterDraw, 1500);
            }

            if(!collectedCards.includes(randomIndex)) {
                collectedCards.push(randomIndex);
                document.getElementById('instruction').innerText = "✨ Открыт новый Аркан!";
            } else {
                dust += 10;
                document.getElementById('instruction').innerText = "Повтор. Получено 10 звездной пыли.";
            }
            initGrimoire();

            setTimeout(() => {
                document.getElementById('shareBtnContainer').style.display = 'flex';
                setTimeout(() => { document.getElementById('shareBtnContainer').style.opacity = 1; }, 50);
            }, 1200);
            
            isFlipped = true;
        }

        """
html = html[:js_draw_start] + new_draw_js + html[js_draw_end:]

# 4. МЕНЯЕМ САМУ ЛОГИКУ ТУТОРИАЛА
tut_js_start = html.find('// --- ЛОГИКА ТУТОРИАЛА ---')

new_tut_js_logic = """// --- ЛОГИКА ТУТОРИАЛА ---
        let tutStep = 0;
        let isTutorialActive = false;

        function checkTutorial() {
            try {
                if(!localStorage.getItem('tutorialDone_v6')) {
                    isTutorialActive = true;
                    startTutorial();
                }
            } catch(e) { console.log(e); }
        }

        function replayTutorial() {
            try { localStorage.removeItem('tutorialDone_v6'); } catch(e) {}
            isTutorialActive = true;
            energy = 1; 
            updateStatsUI();
            if(isFlipped) resetCardManual();
            startTutorial();
        }

        function startTutorial() {
            tutStep = 1;
            switchTab('divination', document.getElementById('navItem_divination'));
            showTutDialog(
                "Врата открыты", 
                `Приветствую тебя, <b>${userName}</b>! Я — Хранитель этого Гримуара. Позволь мне стать твоим проводником. Сейчас я научу тебя читать Судьбу.`,
                "Понятно",
                () => step2()
            );
        }

        function step2() {
            tutStep = 2;
            showTutDialog(
                "Голос Вселенной",
                "Для начала впиши свой вопрос в подсвеченное поле, а затем <b>коснись колоды</b>. Я скроюсь, чтобы не мешать тебе.",
                "Я готов",
                () => {
                    hideTutDialog();
                    document.getElementById('stepQuestion').classList.add('tut-highlight');
                    document.getElementById('card').classList.add('tut-highlight');
                }
            );
        }

        function continueTutorialAfterDraw() {
            if (!isTutorialActive || tutStep !== 2) return;
            tutStep = 3;
            document.getElementById('stepQuestion').classList.remove('tut-highlight');
            document.getElementById('card').classList.remove('tut-highlight');
            
            showTutDialog(
                "Жертва Магии",
                "Потрясающе! Духи ответили тебе. Но магия требует жертв: твоя <b>⚡ Энергия</b> истощилась. Чтобы получать новые попытки, делись картой в Истории ВК или зови друзей.",
                "Понятно",
                () => step4()
            );
        }

        function step4() {
            tutStep = 4;
            switchTab('altar', document.getElementById('navItem_altar'));
            showTutDialog(
                "Древний Алтарь",
                "Это Алтарь Судьбы! Кликай по кристаллу, чтобы собирать <b>✨ Звездную пыль</b>. За нее ты будешь улучшать Алтарь и получать больше ежедневной награды.",
                "Круто!",
                () => step5()
            );
            document.getElementById('altarCrystal').classList.add('tut-highlight');
        }

        function step5() {
            tutStep = 5;
            document.getElementById('altarCrystal').classList.remove('tut-highlight');
            switchTab('grimoire', document.getElementById('navItem_grimoire'));
            showTutDialog(
                "Великие Артефакты",
                "Улучшенный Алтарь открывает эксклюзивные <b>фоны для Историй ВК</b>. Твой статус увидят все! На этом мое обучение окончено. Стань Магистром Таро!",
                "Завершить обучение",
                () => finishTutorial()
            );
            document.getElementById('bgGallery').classList.add('tut-highlight');
        }

        function showTutDialog(title, text, btnText, btnAction) {
            document.getElementById('tutTitle').innerText = title;
            document.getElementById('tutText').innerHTML = text;
            const btn = document.getElementById('tutNextBtn');
            btn.innerText = btnText;
            btn.onclick = btnAction;
            
            const overlay = document.getElementById('tutOverlay');
            overlay.style.display = 'flex';
            setTimeout(() => overlay.classList.add('active'), 10);
        }

        function hideTutDialog() {
            const overlay = document.getElementById('tutOverlay');
            overlay.classList.remove('active');
            setTimeout(() => overlay.style.display = 'none', 300);
        }

        function finishTutorial() {
            isTutorialActive = false;
            try { localStorage.setItem('tutorialDone_v6', '1'); } catch(e) {}
            hideTutDialog();
            document.querySelectorAll('.tut-highlight').forEach(el => el.classList.remove('tut-highlight'));
            switchTab('divination', document.getElementById('navItem_divination'));
        }

        function skipTutorialBtn() {
            openModal('tutSkipModal');
        }

        function forceSkipTutorial() {
            closeModal('tutSkipModal');
            finishTutorial();
        }

        initGrimoire();
    </script>
</body>
</html>"""

html = html[:tut_js_start] + new_tut_js_logic

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

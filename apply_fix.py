import os

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Заменяем CSS для туториала на абсолютное позиционирование, чтобы можно было двигать окно
old_tut_css = """        .tutorial-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); z-index: 99990; display: none; flex-direction: column; justify-content: flex-end; align-items: center; padding-bottom: 100px; box-sizing: border-box; opacity: 0; transition: opacity 0.5s; pointer-events: none;}
        .tutorial-overlay.active { display: flex; opacity: 1; pointer-events: auto;}
        .tutorial-dialog { background: linear-gradient(180deg, #170a24 0%, #0a0410 100%); border: 2px solid var(--gold); border-radius: 15px; padding: 25px; width: 90%; max-width: 340px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.8); position: relative; z-index: 99999; pointer-events: auto;}"""

new_tut_css = """        .tutorial-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); z-index: 99990; display: none; flex-direction: column; align-items: center; box-sizing: border-box; opacity: 0; transition: opacity 0.5s; pointer-events: none;}
        .tutorial-overlay.active { display: flex; opacity: 1; pointer-events: auto;}
        .tutorial-dialog { background: linear-gradient(180deg, #170a24 0%, #0a0410 100%); border: 2px solid var(--gold); border-radius: 15px; padding: 25px; width: 90%; max-width: 340px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.8); position: absolute; z-index: 99999; pointer-events: auto; transition: top 0.5s, bottom 0.5s;}"""

html = html.replace(old_tut_css, new_tut_css)

# 2. Обновляем ссылки на фоны (чтобы не было старого абсолютного домена)
html = html.replace("url('https://tarot-app-pearl-five.vercel.app/images/optimized/vk_story_bg.jpg')", "url('/images/optimized/vk_story_bg.jpg')")
html = html.replace("url('https://tarot-app-pearl-five.vercel.app/images/bg_bronze.jpg')", "url('/images/bg_bronze.jpg')")
html = html.replace("url('https://tarot-app-pearl-five.vercel.app/images/bg_silver.jpg')", "url('/images/bg_silver.jpg')")
html = html.replace("url('https://tarot-app-pearl-five.vercel.app/images/bg_gold.jpg')", "url('/images/bg_gold.jpg')")

# 3. Переписываем логику и историю туториала
old_tut_js = """        // --- ЛОГИКА ТУТОРИАЛА ---
        let tutStep = 0;
        let isTutorialActive = false;

        function checkTutorial() {
            try {
                if(!localStorage.getItem('tutorialDone_v4')) {
                    isTutorialActive = true;
                    startTutorial();
                }
            } catch(e) { console.log(e); }
        }

        function replayTutorial() {
            try { localStorage.removeItem('tutorialDone_v4'); } catch(e) {}
            isTutorialActive = true;
            startTutorial();
        }

        function startTutorial() {
            tutStep = 0;
            const overlay = document.getElementById('tutOverlay');
            document.body.classList.add('tut-mode');
            overlay.style.display = 'flex';
            setTimeout(() => overlay.classList.add('active'), 10);
            renderTutStep();
        }

        function renderTutStep() {
            document.querySelectorAll('.tut-highlight').forEach(el => el.classList.remove('tut-highlight'));
            
            const title = document.getElementById('tutTitle');
            const text = document.getElementById('tutText');
            const btn = document.getElementById('tutNextBtn');
            const skipBtn = document.getElementById('tutSkipBtn');
            
            if(tutStep === 0) {
                switchTab('divination', document.getElementById('navItem_divination'));
                title.innerText = "Врата открыты";
                text.innerHTML = `Привет, <b>${userName}</b>! Я — дух этого древнего Гримуара. Позволь мне открыть для тебя мир магии Таро и показать твою истинную Судьбу...`;
                btn.style.display = 'block';
                btn.innerText = "Продолжить";
                btn.onclick = () => nextTutStep();
            }
            else if(tutStep === 1) {
                title.innerText = "Голос Вселенной";
                text.innerHTML = `Для начала <b>задай свой вопрос</b>. Сосредоточься и впиши в подсвеченное поле то, что тебя по-настоящему тревожит.`;
                btn.innerText = "Я вписал вопрос";
                document.getElementById('stepQuestion').classList.add('tut-highlight');
                document.getElementById('userQuestion').focus();
            }
            else if(tutStep === 2) {
                title.innerText = "Нить Судьбы";
                text.innerHTML = `Отлично! Твой вопрос отправлен в астрал. Теперь <b>коснись колоды</b>, чтобы вытянуть Карту Дня и услышать ответ духов.`;
                btn.style.display = 'none'; 
                skipBtn.style.display = 'none'; 
                document.getElementById('card').classList.add('tut-highlight');
            }
            else if(tutStep === 3) {
                btn.style.display = 'block';
                skipBtn.style.display = 'inline-block';
                title.innerText = "Энергия и Ритуалы";
                text.innerHTML = `Магия свершилась! Обрати внимание: гадание расходует <b>⚡ Энергию</b>. Чтобы восстановить её, поделись картой в Истории или позови друга в разделе Ритуалы.`;
                btn.innerText = "Понятно";
                btn.onclick = () => nextTutStep();
            }
            else if(tutStep === 4) {
                switchTab('altar', document.getElementById('navItem_altar'));
                title.innerText = "Алтарь Судьбы";
                text.innerHTML = `Но истинная сила кроется здесь! Кликай по сфере, чтобы собирать <b>✨ Звездную пыль</b>. За пыль ты сможешь улучшать Алтарь. Чем выше уровень, тем больше награды!`;
                btn.innerText = "Вау!";
                document.getElementById('altarCrystal').classList.add('tut-highlight');
                btn.onclick = () => nextTutStep();
            }
            else if(tutStep === 5) {
                switchTab('grimoire', document.getElementById('navItem_grimoire'));
                title.innerText = "Награды и Фоны";
                text.innerHTML = `Улучшенный Алтарь открывает великие награды! Здесь ты сможешь выбрать эксклюзивные <b>фоны для Историй ВК</b>.`;
                btn.innerText = "Начать игру!";
                document.getElementById('bgGallery').classList.add('tut-highlight');
                btn.onclick = () => skipTutorial();
            }
        }

        function nextTutStep() {
            tutStep++;
            if(tutStep > 5) {
                skipTutorial();
            } else {
                renderTutStep();
            }
        }"""

new_tut_js = """        // --- ЛОГИКА ТУТОРИАЛА ---
        let tutStep = 0;
        let isTutorialActive = false;

        function checkTutorial() {
            try {
                if(!localStorage.getItem('tutorialDone_v5')) {
                    isTutorialActive = true;
                    startTutorial();
                }
            } catch(e) { console.log(e); }
        }

        function replayTutorial() {
            try { localStorage.removeItem('tutorialDone_v5'); } catch(e) {}
            isTutorialActive = true;
            startTutorial();
        }

        function startTutorial() {
            tutStep = 0;
            const overlay = document.getElementById('tutOverlay');
            document.body.classList.add('tut-mode');
            overlay.style.display = 'flex';
            setTimeout(() => overlay.classList.add('active'), 10);
            renderTutStep();
        }

        function renderTutStep() {
            document.querySelectorAll('.tut-highlight').forEach(el => el.classList.remove('tut-highlight'));
            
            const dialog = document.querySelector('.tutorial-dialog');
            const title = document.getElementById('tutTitle');
            const text = document.getElementById('tutText');
            const btn = document.getElementById('tutNextBtn');
            const skipBtn = document.getElementById('tutSkipBtn');
            
            // Сбрасываем позицию
            dialog.style.top = 'auto';
            dialog.style.bottom = 'auto';

            if(tutStep === 0) {
                switchTab('divination', document.getElementById('navItem_divination'));
                dialog.style.top = '30%';
                title.innerText = "Зов Астрала";
                text.innerHTML = `Приветствую тебя, <b>${userName}</b>... Я — Хранитель этого древнего Гримуара. Ты здесь не случайно. Нити судьбы истончились, и мне нужна твоя помощь, чтобы восстановить баланс.`;
                btn.style.display = 'block';
                btn.innerText = "Я готов";
                btn.onclick = () => nextTutStep();
            }
            else if(tutStep === 1) {
                dialog.style.bottom = '15%'; // Окно снизу, чтобы не закрывать поле
                title.innerText = "Голос Вселенной";
                text.innerHTML = `Твой разум — ключ. <b>Впиши в светящееся поле</b> свой самый сокровенный вопрос. Спроси о том, что тревожит твою душу. Вселенная готова слушать...`;
                btn.innerText = "Вопрос задан";
                document.getElementById('stepQuestion').classList.add('tut-highlight');
                btn.onclick = () => nextTutStep();
            }
            else if(tutStep === 2) {
                dialog.style.top = '10%'; // Окно сверху, чтобы не закрывать карту
                title.innerText = "Нить Судьбы";
                text.innerHTML = `Астрал откликнулся! Теперь <b>коснись колоды</b>. Вытяни свой Аркан, и духи прошепчут тебе ответ сквозь пелену времени...`;
                btn.style.display = 'none'; 
                skipBtn.style.display = 'none'; 
                document.getElementById('card').classList.add('tut-highlight');
            }
            else if(tutStep === 3) {
                dialog.style.top = '25%';
                btn.style.display = 'block';
                skipBtn.style.display = 'inline-block';
                title.innerText = "Жертва Магии";
                text.innerHTML = `Карты заговорили... Но магия требует жертв. Твоя <b>⚡ Энергия</b> истощилась. Чтобы продолжить читать судьбу, тебе нужна помощь. Поделись своим знаком в Истории или призови друзей — это восстановит твои силы.`;
                btn.innerText = "Ясно";
                btn.onclick = () => nextTutStep();
            }
            else if(tutStep === 4) {
                switchTab('altar', document.getElementById('navItem_altar'));
                dialog.style.bottom = '15%'; // Окно снизу, чтобы не закрывать алтарь
                title.innerText = "Древний Алтарь";
                text.innerHTML = `А теперь — самое главное. Алтарь Судьбы! Его свет почти угас. <b>Касайся кристалла</b>, собирай Звездную Пыль ✨ и восстанавливай его мощь. Чем сильнее Алтарь, тем больше магии он отдаст тебе каждый день!`;
                btn.innerText = "Восстановить!";
                document.getElementById('altarCrystal').classList.add('tut-highlight');
                btn.onclick = () => nextTutStep();
            }
            else if(tutStep === 5) {
                switchTab('grimoire', document.getElementById('navItem_grimoire'));
                dialog.style.top = '10%'; // Окно сверху, чтобы не закрывать фоны
                title.innerText = "Великие Артефакты";
                text.innerHTML = `Возроди Алтарь, и Гримуар вознаградит тебя! Ты откроешь легендарные артефакты — Бронзовые, Серебряные и ослепительные Золотые фоны для своих Историй. Твой статус увидят все. Стань Магистром Таро!`;
                btn.innerText = "Вступить на Путь!";
                document.getElementById('bgGallery').classList.add('tut-highlight');
                btn.onclick = () => skipTutorial();
            }
        }

        function nextTutStep() {
            tutStep++;
            if(tutStep > 5) {
                skipTutorial();
            } else {
                renderTutStep();
            }
        }"""

html = html.replace(old_tut_js, new_tut_js)

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Файл index.html успешно обновлен с новым сюжетом и правильными слоями!")

    
        const loader = document.getElementById('loader');
        function hideLoader() {
            if(loader && loader.style.display !== 'none') {
                loader.style.opacity = '0';
                loader.style.pointerEvents = 'none';
                setTimeout(() => { loader.style.display = 'none'; }, 500);
            }
        }

        // Если ВК-бридж зависнет, убираем лоадер принудительно через 3 секунды
        setTimeout(hideLoader, 3000);

        let userName = "Путник";

        try {
            vkBridge.send('VKWebAppInit').then(() => {
                vkBridge.send('VKWebAppGetUserInfo').then(data => {
                    if(data.first_name) userName = data.first_name;
                    hideLoader();
                    checkTutorial();
                }).catch(() => { hideLoader(); checkTutorial(); });
            }).catch(() => { hideLoader(); checkTutorial(); });
        } catch(e) { 
            hideLoader(); 
            checkTutorial(); 
        }

        const tarotDeck = [
            { num: "0", name: "Шут", desc: "Спонтанный риск принесет неожиданные плоды. Шагните в неизвестность.", img: "/images/optimized/fool.jpg" },
            { num: "I", name: "Маг", desc: "У вас есть все ресурсы для созидания. Творите свою реальность.", img: "/images/optimized/magician.jpg" },
            { num: "II", name: "Жрица", desc: "Прислушайтесь к шепоту подсознания. Тайное готовится стать явным.", img: "/images/optimized/priestess.jpg" },
            { num: "III", name: "Императрица", desc: "День абсолютного изобилия. Дело, в которое вы вложите любовь, даст урожай.", img: "/images/optimized/empress.jpg" },
            { num: "VII", name: "Колесница", desc: "Триумф воли и движение вперед! Любые препятствия будут сломлены.", img: "/images/optimized/chariot.jpg" },
            { num: "XIX", name: "Солнце", desc: "Абсолютный успех и ясность ума. Вы сияете — наслаждайтесь триумфом.", img: "/images/optimized/sun.jpg" }
        ];

        let isFlipped = false;
        let collectedCards = [1]; 
        let dust = 0;
        let energy = 1;
        let currentDrawnCardImg = ""; 
        let altarLevel = 1;
        let altarCost = 100;
        let activeBgUrl = "vk_story_bg.jpg"; 

        function getRank(count) {
            if(count >= 22) return "Магистр Таро";
            if(count >= 15) return "Адепт";
            if(count >= 5) return "Искатель";
            return "Неофит";
        }

        function updateStatsUI() {
            document.getElementById('energyCountHeader').innerText = energy;
            document.getElementById('dustCountHeader').innerText = dust;
        }

        function updateAltarUI() {
            document.getElementById('altarLevel').innerText = altarLevel;
            document.getElementById('altarCost').innerText = altarCost;
            document.getElementById('altarMultiplier').innerText = altarLevel;
            document.getElementById('dailyRewardAmount').innerText = 50 * altarLevel;
            document.getElementById('altarProgress').style.width = Math.min((dust / altarCost) * 100, 100) + '%';

            const crystal = document.getElementById('altarSvg');
            if(altarLevel >= 20) crystal.style.filter = "drop-shadow(0 0 20px #d4af37)";
            else if(altarLevel >= 10) crystal.style.filter = "drop-shadow(0 0 15px #e6e6fa)";
            else if(altarLevel >= 5) crystal.style.filter = "drop-shadow(0 0 10px #cd7f32)";
            else crystal.style.filter = "none";

            if(altarLevel >= 5) unlockBg('bgItem2');
            if(altarLevel >= 10) unlockBg('bgItem3');
            if(altarLevel >= 20) unlockBg('bgItem4');
        }

        function unlockBg(id) {
            const el = document.getElementById(id);
            if(el && el.classList.contains('locked')) {
                el.classList.remove('locked');
                el.querySelector('.bg-lock').style.display = 'none';
            }
        }

        function selectBg(reqLevel, urlName) {
            if(altarLevel < reqLevel) {
                alert(`Этот фон откроется на ${reqLevel} уровне Алтаря!`);
                return;
            }
            activeBgUrl = urlName;
            document.querySelectorAll('.bg-item').forEach(el => el.classList.remove('active-bg'));
            event.currentTarget.classList.add('active-bg');
        }

        function initGrimoire() {
            const grid = document.getElementById('albumGrid');
            grid.innerHTML = '';
            for(let i=0; i<6; i++) { 
                const div = document.createElement('div');
                div.className = 'grid-card ' + (collectedCards.includes(i) ? 'collected' : '');
                div.innerText = tarotDeck[i].num;
                if(collectedCards.includes(i)) {
                    div.style.backgroundImage = `linear-gradient(180deg, rgba(23,10,36,0.6), rgba(10,4,16,0.9)), url('${tarotDeck[i].img}')`;
                    div.style.backgroundSize = 'cover';
                }
                grid.appendChild(div);
            }
            const rank = getRank(collectedCards.length);
            document.getElementById('rankTitle').innerText = rank;
            document.getElementById('progressBar').style.width = (collectedCards.length / 22 * 100) + '%';
            document.getElementById('cardsCount').innerText = collectedCards.length;
            updateStatsUI();
            updateAltarUI();
        }

        function tapAltar(event) {
            dust++;
            updateStatsUI();
            updateAltarUI();
            
            const floatingText = document.createElement('div');
            floatingText.innerText = '+1 ✨';
            floatingText.style.position = 'fixed';
            floatingText.style.left = event.clientX + 'px';
            floatingText.style.top = (event.clientY - 20) + 'px';
            floatingText.style.color = 'var(--gold)';
            floatingText.style.fontWeight = 'bold';
            floatingText.style.pointerEvents = 'none';
            floatingText.style.zIndex = '9999';
            floatingText.style.transition = 'all 1s ease-out';
            document.body.appendChild(floatingText);

            setTimeout(() => {
                floatingText.style.transform = 'translateY(-50px)';
                floatingText.style.opacity = '0';
            }, 10);
            setTimeout(() => { document.body.removeChild(floatingText); }, 1000);
        }

        function upgradeAltar() {
            if(dust >= altarCost) {
                dust -= altarCost;
                altarLevel++;
                altarCost = Math.floor(altarCost * 1.5);
                updateStatsUI();
                updateAltarUI();
            } else {
                alert(`Не хватает пыли. Нужно еще ${altarCost - dust} ✨`);
            }
        }

        function claimDailyBonus() { 
            const btn = document.getElementById('claimDailyBtn');
            if(btn.disabled) return;
            let reward = 50 * altarLevel;
            dust += reward; 
            initGrimoire(); 
            btn.innerText = "Собрано ✓"; 
            btn.disabled = true; 
        }

        function showAd() {
            try {
                vkBridge.send("VKWebAppCheckNativeAds", {"ad_format": "reward"})
                .then((data) => {
                    if (data.result) {
                        vkBridge.send("VKWebAppShowNativeAds", {"ad_format": "reward"})
                        .then((d) => {
                            if (d.result) { dust += 100; initGrimoire(); alert("Видение получено! +100 ✨ Пыли"); }
                        }).catch(e => console.log(e));
                    } else { alert("Видения пока недоступны. Попробуйте позже."); }
                }).catch(e => alert("Доступно только в VK."));
            } catch(e) { alert("Доступно только в VK."); }
        }

        function drawCardApi() {
            if(isFlipped) return;
            if(energy <= 0) {
                inviteFriend(); 
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
            document.getElementById('cardBack').style.backgroundImage = `linear-gradient(180deg, rgba(23, 10, 36, 0.75) 0%, rgba(10, 4, 16, 0.95) 100%), url('${randomCard.img}')`;
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
                .then(data => { aiRespElem.innerText = data.ai_text ? data.ai_text : "Ответ скрыт в тумане..."; })
                .catch(e => { aiRespElem.innerText = "Астральная связь прервалась..."; });
            } else { aiRespElem.style.display = 'none'; }

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

        function publishStoryVK() {
            try {
                let bgPath = (activeBgUrl === 'vk_story_bg.jpg') ? '/images/optimized/vk_story_bg.jpg' : '/images/' + activeBgUrl;
                const bgUrl = "https://tarot-app-pearl-five.vercel.app" + bgPath;
                const stickerUrl = "https://tarot-app-pearl-five.vercel.app" + currentDrawnCardImg.replace('/images/', '/images/optimized/');

                vkBridge.send("VKWebAppShowStoryBox", {
                  background_type: "image",
                  url: bgUrl,
                  stickers: [{ 
                      sticker_type: "renderable", 
                      sticker: { content_type: "image", url: stickerUrl, transform: { translation_y: -50 } } 
                  }]
                }).then(data => {
                    energy++; initGrimoire();
                    document.getElementById('card').classList.remove('flipped');
                    isFlipped = false;
                    document.getElementById('shareBtnContainer').style.opacity = 0;
                    setTimeout(() => { document.getElementById('shareBtnContainer').style.display = 'none'; }, 500);
                    document.getElementById('instruction').innerText = "Энергия восстановлена.";
                }).catch(e => console.log("История отменена"));
            } catch(e) { alert("Ошибка вызова историй."); }
        }

        function inviteFriend() {
            try {
                vkBridge.send("VKWebAppShowInviteBox", {}).then(data => {
                    if(data.success) { energy++; initGrimoire(); alert('Отправлено! +1 ⚡'); }
                }).catch(e => {
                    vkBridge.send("VKWebAppShare", {"link": "https://vk.com/app54632741"}).then(data => {
                        energy++; initGrimoire(); alert('Ссылка отправлена! +1 ⚡');
                    }).catch(e2 => console.log("Закрыто"));
                });
            } catch(e) { alert("Невозможно открыть вне VK."); }
        }

        function switchTab(tabId, element) {
            document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('screen-' + tabId).classList.add('active');
            if(element) element.classList.add('active');
        }

        function openModal(id) {
            const modal = document.getElementById(id);
            modal.style.display = 'flex';
            setTimeout(() => { modal.classList.add('active'); }, 10);
        }

        function closeModal(id, event) {
            if(event && event.target !== document.getElementById(id) && !event.target.classList.contains('close-btn')) return;
            const modal = document.getElementById(id);
            modal.classList.remove('active');
            setTimeout(() => { modal.style.display = 'none'; }, 300);
        }

        // --- ЛОГИКА ТУТОРИАЛА ---
        let tutStep = 0;
        const tutSteps = [
            {
                title: "Врата открыты",
                text: "Привет, {name}! Я — дух этого Гримуара. Позволь мне стать твоим проводником в мир Таро...",
                highlight: null,
                tab: "divination",
                btn: "Продолжить"
            },
            {
                title: "Спроси Вселенную",
                text: "Для начала задай свой вопрос. Сосредоточься и впиши в это поле то, что тебя по-настоящему тревожит.",
                highlight: "stepQuestion",
                tab: "divination",
                btn: "Понятно"
            },
            {
                title: "Нить Судьбы",
                text: "Вопрос задан. Теперь просто коснись колоды, чтобы вытянуть Карту Дня и услышать ответ духов.",
                highlight: "card",
                tab: "divination",
                btn: "Супер!"
            },
            {
                title: "Алтарь Судьбы",
                text: "Твоя главная миссия — собирать ✨ Звездную пыль и восстанавливать древний Алтарь! Кликай по кристаллу, чтобы получать пыль.",
                highlight: "altarCrystal",
                tab: "altar",
                btn: "Вау!"
            },
            {
                title: "Награды и Фоны",
                text: "Чем выше уровень Алтаря, тем больше ежедневная награда. А на 5, 10 и 20 уровнях в твоем профиле откроются эксклюзивные фоны для историй ВК!",
                highlight: "bgGallery",
                tab: "grimoire",
                btn: "Начать Путь!"
            }
        ];

        function checkTutorial() {
            if(!localStorage.getItem('tutorialDone')) {
                startTutorial();
            }
        }

        function startTutorial() {
            tutStep = 0;
            const overlay = document.getElementById('tutOverlay');
            overlay.style.display = 'flex';
            setTimeout(() => overlay.classList.add('active'), 10);
            renderTutStep();
        }

        function renderTutStep() {
            document.querySelectorAll('.tut-highlight').forEach(el => el.classList.remove('tut-highlight'));
            const step = tutSteps[tutStep];
            
            if(step.tab) {
                switchTab(step.tab, document.getElementById('navItem_' + step.tab));
            }

            document.getElementById('tutTitle').innerText = step.title;
            document.getElementById('tutText').innerText = step.text.replace('{name}', userName);
            document.getElementById('tutNextBtn').innerText = step.btn;

            if(step.highlight) {
                const el = document.getElementById(step.highlight);
                if(el) el.classList.add('tut-highlight');
            }
        }

        function nextTutStep() {
            tutStep++;
            if(tutStep >= tutSteps.length) {
                skipTutorial();
            } else {
                renderTutStep();
            }
        }

        function showTutSkip() {
            openModal('tutSkipModal');
        }

        function skipTutorial() {
            localStorage.setItem('tutorialDone', '1');
            const overlay = document.getElementById('tutOverlay');
            overlay.classList.remove('active');
            setTimeout(() => overlay.style.display = 'none', 500);
            document.querySelectorAll('.tut-highlight').forEach(el => el.classList.remove('tut-highlight'));
            switchTab('divination', document.getElementById('navItem_divination'));
        }

        initGrimoire();
    

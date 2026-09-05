    
        const loader = document.getElementById('loader');
        let appStarted = false;

        function startApp() {
            if (appStarted) return;
            appStarted = true;
            if(loader && loader.style.display !== 'none') {
                loader.style.opacity = '0';
                loader.style.pointerEvents = 'none';
                setTimeout(() => { loader.style.display = 'none'; }, 500);
            }
            setTimeout(checkTutorial, 100);
        }

        setTimeout(startApp, 3000);

        let userName = "Путник";
        try {
            if(window.vkBridge) {
                vkBridge.send('VKWebAppInit').then(() => {
                    vkBridge.send('VKWebAppGetUserInfo').then(data => {
                        if(data.first_name) userName = data.first_name;
                        startApp();
                    }).catch(() => startApp());
                }).catch(() => startApp());
            } else {
                startApp();
            }
        } catch(e) { startApp(); }

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
        
        let starShowerTime = 0;
        let starShowerInterval = null;

        function safeStorageGet(key, def = null) {
            try { return localStorage.getItem(key) || def; } catch(e) { return def; }
        }
        function safeStorageSet(key, val) {
            try { localStorage.setItem(key, val); } catch(e) {}
        }
        function safeStorageRemove(key) {
            try { localStorage.removeItem(key); } catch(e) {}
        }

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

        function checkBgLock(id, reqLevel) {
            const lockElem = document.getElementById('lock_' + id);
            if(altarLevel >= reqLevel) {
                if(lockElem) lockElem.style.display = 'none';
                document.getElementById('bg_' + id).classList.remove('locked');
            } else {
                if(lockElem) lockElem.style.display = 'block';
                document.getElementById('bg_' + id).classList.add('locked');
            }
        }

        function previewBg(reqLevel, urlName, title) {
            document.getElementById('previewTitle').innerText = title;
            const bgPath = (urlName === 'vk_story_bg.jpg') ? '/images/optimized/vk_story_bg.jpg' : '/images/optimized/' + urlName;
            document.getElementById('previewImg').style.backgroundImage = `url('https://tarot-app-pearl-five.vercel.app${bgPath}')`;
            
            const btn = document.getElementById('previewSelectBtn');
            if(altarLevel < reqLevel) {
                btn.innerHTML = `🔒 Откроется на ${reqLevel} ур.`;
                btn.disabled = true;
                btn.onclick = null;
            } else {
                btn.innerHTML = "Выбрать этот фон";
                btn.disabled = false;
                btn.onclick = () => {
                    activeBgUrl = urlName;
                    document.querySelectorAll('.bg-item').forEach(el => el.classList.remove('active-bg'));
                    document.getElementById('bg_' + urlName).classList.add('active-bg');
                    closeModal('previewModal');
                };
            }
            openModal('previewModal');
        }

        function getAdCount() {
            let data = JSON.parse(safeStorageGet('adStats') || '{"date": "", "count": 0}');
            let today = new Date().toDateString();
            if (data.date !== today) { return 0; }
            return data.count;
        }

        function incrementAdCount() {
            let count = getAdCount();
            safeStorageSet('adStats', JSON.stringify({"date": new Date().toDateString(), "count": count + 1}));
        }

        function activateStarShower() {
            starShowerTime = 30;
            document.getElementById('starShowerTimer').style.display = 'block';
            document.getElementById('altarImage').style.filter = 'drop-shadow(0 0 40px #ff8c00)';
            
            if (starShowerInterval) clearInterval(starShowerInterval);
            starShowerInterval = setInterval(() => {
                starShowerTime--;
                document.getElementById('starShowerTimer').innerText = `Астральный шторм: ${starShowerTime} сек (x10 Пыли!)`;
                if (starShowerTime <= 0) {
                    clearInterval(starShowerInterval);
                    document.getElementById('starShowerTimer').style.display = 'none';
                    updateAltarUI();
                }
            }, 1000);
        }

        function updateAltarUI() {
            document.getElementById('altarLevel').innerText = altarLevel;
            document.getElementById('altarCost').innerText = altarCost;
            document.getElementById('altarMultiplier').innerText = altarLevel;
            document.getElementById('dailyRewardAmount').innerText = 50 * altarLevel;
            document.getElementById('altarProgress').style.width = Math.min((dust / altarCost) * 100, 100) + '%';

            let imgLevel = 1;
            if (altarLevel >= 20) imgLevel = 20;
            else if (altarLevel >= 15) imgLevel = 15;
            else if (altarLevel >= 10) imgLevel = 10;
            else if (altarLevel >= 5) imgLevel = 5;
            
            let imgElem = document.getElementById('altarImage');
            if(imgElem) imgElem.src = `/images/optimized/tree_${imgLevel}.png`;

            if (starShowerTime <= 0 && imgElem) {
                if(altarLevel >= 20) imgElem.style.filter = "drop-shadow(0 0 30px var(--gold))";
                else if(altarLevel >= 15) imgElem.style.filter = "drop-shadow(0 0 20px #e6e6fa)";
                else if(altarLevel >= 10) imgElem.style.filter = "drop-shadow(0 0 15px #e6e6fa)";
                else if(altarLevel >= 5) imgElem.style.filter = "drop-shadow(0 0 10px #cd7f32)";
                else imgElem.style.filter = "drop-shadow(0 0 10px rgba(212,175,55,0.3))";
            }

            const r1 = document.getElementById('altarRing1');
            const r2 = document.getElementById('altarRing2');
            if(r1 && r2) {
                if(altarLevel >= 5) { r1.style.display = 'block'; r1.style.borderColor = '#cd7f32'; } else { r1.style.display = 'none'; }
                if(altarLevel >= 10) { r1.style.borderColor = '#e6e6fa'; r2.style.display = 'block'; r2.style.borderColor = '#bfa1db'; } else { r2.style.display = 'none'; }
                if(altarLevel >= 20) { r1.style.borderColor = 'var(--gold)'; r2.style.borderColor = 'var(--gold-light)'; }
            }

            checkBgLock('bg_bronze.jpg', 5);
            checkBgLock('bg_silver.jpg', 10);
            checkBgLock('bg_gold.jpg', 20);
        }

        function initGrimoire() {
            const grid = document.getElementById('albumGrid');
            grid.innerHTML = '';
            for(let i=0; i<6; i++) { 
                const div = document.createElement('div');
                div.className = 'grid-card ' + (collectedCards.includes(i) ? 'collected' : '');
                div.innerText = tarotDeck[i].num;
                if(collectedCards.includes(i)) {
                    div.style.backgroundImage = `linear-gradient(180deg, rgba(23,10,36,0.6), rgba(10,4,16,0.9)), url('https://tarot-app-pearl-five.vercel.app${tarotDeck[i].img}')`;
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
            let reward = starShowerTime > 0 ? 10 : 1;
            dust += reward;
            updateStatsUI();
            updateAltarUI();
            
            const floatingText = document.createElement('div');
            floatingText.innerHTML = `+${reward} <svg class="dust-inline" viewBox="0 0 24 24"><path d="M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9L12 2Z"/></svg>`;
            floatingText.style.position = 'fixed';
            floatingText.style.left = event.clientX + 'px';
            floatingText.style.top = (event.clientY - 20) + 'px';
            floatingText.style.color = starShowerTime > 0 ? '#ff8c00' : 'var(--gold)';
            floatingText.style.fontWeight = 'bold';
            floatingText.style.pointerEvents = 'none';
            floatingText.style.zIndex = '9999';
            floatingText.style.transition = 'all 1s ease-out';
            document.body.appendChild(floatingText);

            setTimeout(() => {
                floatingText.style.transform = 'translateY(-50px) scale(1.5)';
                floatingText.style.opacity = '0';
            }, 10);
            setTimeout(() => { document.body.removeChild(floatingText); }, 1000);
        }

        function upgradeAltar() {
            if(dust >= altarCost) {
                dust -= altarCost;
                altarLevel++;
                altarCost = Math.floor(100 * Math.pow(1.8, altarLevel - 1));
                updateStatsUI();
                updateAltarUI();
            } else {
                alert(`Не хватает пыли. Нужно еще ${altarCost - dust} пыли.`);
            }
        }

        function claimDailyBonus() { 
            const btn = document.getElementById('claimDailyBtn');
            if(btn.disabled) return;
            let reward = 50 * altarLevel;
            dust += reward; 
            initGrimoire(); 
            btn.innerHTML = "Собрано ✓"; 
            btn.disabled = true; 
            alert(`Ежедневный ритуал выполнен! Получено ${reward} пыли.`);
        }

        function showAd() {
            if (getAdCount() >= 5) {
                alert("Астральный канал перегрет. Возвращайся завтра!");
                return;
            }
            try {
                vkBridge.send("VKWebAppCheckNativeAds", {"ad_format": "reward"})
                .then((data) => {
                    if (data.result) {
                        vkBridge.send("VKWebAppShowNativeAds", {"ad_format": "reward"})
                        .then((d) => {
                            if (d.result) { 
                                incrementAdCount();
                                activateStarShower();
                                switchTab('altar', document.getElementById('navItem_altar'));
                            }
                        }).catch(e => console.log(e));
                    } else { alert("Видения пока недоступны. Попробуйте позже."); }
                }).catch(e => {
                    incrementAdCount();
                    activateStarShower();
                    switchTab('altar', document.getElementById('navItem_altar'));
                });
            } catch(e) { 
                incrementAdCount();
                activateStarShower();
                switchTab('altar', document.getElementById('navItem_altar'));
            }
        }

        function resetCardManual() {
            document.getElementById('card').classList.remove('flipped');
            isFlipped = false;
            const btnContainer = document.getElementById('shareBtnContainer');
            btnContainer.style.opacity = 0;
            setTimeout(() => { btnContainer.style.display = 'none'; }, 500);
            document.getElementById('instruction').innerText = "Готов к новому гаданию.";
            document.getElementById('userQuestion').value = ""; 
            document.getElementById('aiResponse').style.display = 'none';
        }

        function drawCardApi() {
            if(isFlipped) return;
            if(energy <= 0) {
                alert("У вас нет Энергии! Выполните Ритуал (пригласите друга или опубликуйте историю), чтобы получить попытку.");
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
                    if(data.refund) {
                        alert("Духи не смогли разобрать твой вопрос. Энергия возвращена!");
                        energy++;
                        updateStatsUI();
                        resetCardManual();
                        if(collectedCards[collectedCards.length - 1] === randomIndex) {
                            collectedCards.pop();
                        }
                        initGrimoire();
                    } else {
                        aiRespElem.innerText = data.ai_text ? data.ai_text : "Ответ скрыт в тумане..."; 
                    }
                })
                .catch(e => { 
                    aiRespElem.innerText = "Астральная связь прервалась..."; 
                });
            } else { 
                aiRespElem.style.display = 'none'; 
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

        function publishStoryVK() {
            try {
                let bgPath = (activeBgUrl === 'vk_story_bg.jpg') ? '/images/optimized/vk_story_bg.jpg' : '/images/optimized/' + activeBgUrl;
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
                    resetCardManual();
                }).catch(e => console.log("История отменена"));
            } catch(e) { alert("Ошибка вызова историй."); }
        }

        function inviteFriend() {
            try {
                vkBridge.send("VKWebAppShowInviteBox", {}).then(data => {
                    if(data.success) { 
                        energy++; initGrimoire(); 
                        alert('Отправлено! +1 Энергия'); 
                        if(isFlipped) resetCardManual();
                    }
                }).catch(e => {
                    vkBridge.send("VKWebAppShare", {"link": "https://vk.com/app54632741"}).then(data => {
                        energy++; initGrimoire(); 
                        alert('Ссылка отправлена! +1 Энергия');
                        if(isFlipped) resetCardManual();
                    }).catch(e2 => console.log("Закрыто"));
                });
            } catch(e) { alert("Невозможно открыть вне VK."); }
        }

        const originalSwitchTab = function(tabId, element) {
            document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('screen-' + tabId).classList.add('active');
            if(element) element.classList.add('active');
        }

        window.switchTab = function(tabId, element) {
            originalSwitchTab(tabId, element);
            document.querySelectorAll('.tut-highlight').forEach(el => el.classList.remove('tut-highlight'));
            setTimeout(checkTutorial, 300);
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

        // --- ЛОГИКА КОНТЕКСТНОГО ТУТОРИАЛА ---
        function checkTutorial() {
            const activeScreen = document.querySelector('.screen.active');
            if(!activeScreen) return;
            const activeTab = activeScreen.id.replace('screen-', '');
            
            if(activeTab === 'divination' && !safeStorageGet('tut_divination_ok')) {
                showTutDialog(
                    "Голос Вселенной", 
                    `Приветствую, <b>${userName}</b>! Я — дух этого Гримуара. Впиши свой сокровенный вопрос в подсвеченное поле, а затем коснись колоды, чтобы вытянуть Карту Дня.`,
                    () => {
                        hideTutDialog();
                        safeStorageSet('tut_divination_ok', '1');
                        document.getElementById('stepQuestion').classList.add('tut-highlight');
                        document.getElementById('card').classList.add('tut-highlight');
                    }
                );
            } 
            else if(activeTab === 'altar' && !safeStorageGet('tut_altar_ok')) {
                showTutDialog(
                    "Алтарь Судьбы", 
                    "Это сердце твоей магии. Кликай по Древу, чтобы собирать ✨ Звездную пыль. Чем выше уровень Алтаря, тем больше ежедневная награда и тем круче фоны для Историй ВК!",
                    () => {
                        hideTutDialog();
                        safeStorageSet('tut_altar_ok', '1');
                        document.getElementById('altarCrystal').classList.add('tut-highlight');
                        setTimeout(() => {
                            const ac = document.getElementById('altarCrystal');
                            if(ac) ac.classList.remove('tut-highlight');
                        }, 3000);
                    }
                );
            }
            else if(activeTab === 'grimoire' && !safeStorageGet('tut_grimoire_ok')) {
                showTutDialog(
                    "Великие Артефакты", 
                    "Здесь хранится твоя коллекция Арканов. Повышай свой ранг и открывай новые фоны для Историй. Пусть все увидят твой статус!",
                    () => {
                        hideTutDialog();
                        safeStorageSet('tut_grimoire_ok', '1');
                        document.getElementById('bgGallery').classList.add('tut-highlight');
                        setTimeout(() => {
                            const bg = document.getElementById('bgGallery');
                            if(bg) bg.classList.remove('tut-highlight');
                        }, 3000);
                    }
                );
            }
            else if(activeTab === 'rituals' && !safeStorageGet('tut_rituals_ok')) {
                showTutDialog(
                    "Жертва Магии", 
                    "Гадание расходует твою ⚡ Энергию. Здесь ты можешь восстановить её: выполняй ежедневные ритуалы, смотри видения или приглашай друзей.",
                    () => {
                        hideTutDialog();
                        safeStorageSet('tut_rituals_ok', '1');
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

        function replayTutorial() {
            safeStorageRemove('tut_divination_ok');
            safeStorageRemove('tut_altar_ok');
            safeStorageRemove('tut_grimoire_ok');
            safeStorageRemove('tut_rituals_ok');
            energy = 1;
            updateStatsUI();
            if(isFlipped) resetCardManual();
            switchTab('divination', document.getElementById('navItem_divination'));
        }

        initGrimoire();
    

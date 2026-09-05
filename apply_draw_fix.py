import os

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_draw = """        function drawCardApi() {
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
                            initGrimoire();
                        }
                    } else {
                        aiRespElem.innerText = data.ai_text ? data.ai_text : "Ответ скрыт в тумане..."; 
                        checkDrawTutorial();
                    }
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
                if(!safeStorageGet('tut_draw_done')) {
                    safeStorageSet('tut_draw_done', '1');
                    setTimeout(() => {
                        showTutDialog(
                            "Судьба открыта",
                            "Магия свершилась! Но помни, Энергия истощилась. Загляни во вкладку <b>Ритуалы</b> или <b>Алтарь</b>, чтобы продолжить путь.",
                            () => hideTutDialog()
                        );
                    }, 500);
                }
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
        }"""

new_draw = """        function drawCardApi() {
            try {
                if(isFlipped) return;
                if(energy <= 0) {
                    alert("У вас нет Энергии! Выполните Ритуал (пригласите друга или опубликуйте историю), чтобы получить попытку.");
                    switchTab('rituals', document.getElementById('navItem_rituals'));
                    return;
                }
                
                energy--;
                updateStatsUI();
                
                const randomIndex = Math.floor(Math.random() * tarotDeck.length);
                const randomCard = tarotDeck[randomIndex];
                currentDrawnCardImg = randomCard.img;

                document.getElementById('cardNumber').innerText = randomCard.num;
                document.getElementById('cardName').innerText = randomCard.name;
                document.getElementById('cardDesc').innerText = randomCard.desc;
                document.getElementById('cardBack').style.backgroundImage = `linear-gradient(180deg, rgba(23, 10, 36, 0.75) 0%, rgba(10, 4, 16, 0.95) 100%), url('https://tarot-app-pearl-five.vercel.app${randomCard.img}')`;
                document.getElementById('cardBack').style.backgroundSize = 'cover';

                // Сразу переворачиваем карту
                document.getElementById('card').classList.add('flipped');

                const question = document.getElementById('userQuestion').value;
                const aiRespElem = document.getElementById('aiResponse');
                
                const qBox = document.getElementById('stepQuestion');
                const cBox = document.getElementById('card');
                if(qBox) qBox.classList.remove('tut-highlight');
                if(cBox) cBox.classList.remove('tut-highlight');
                
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
                        } else {
                            aiRespElem.innerText = data.ai_text ? data.ai_text : "Ответ скрыт в тумане..."; 
                            checkDrawTutorial();
                        }
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
                    if(!safeStorageGet('tut_draw_done')) {
                        safeStorageSet('tut_draw_done', '1');
                        setTimeout(() => {
                            showTutDialog(
                                "Судьба открыта",
                                "Магия свершилась! Но помни, Энергия истощилась. Загляни во вкладку <b>Ритуалы</b> или <b>Алтарь</b>, чтобы продолжить путь.",
                                () => hideTutDialog()
                            );
                        }, 500);
                    }
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
            } catch (err) {
                alert("Ошибка игры: " + err.message);
                console.error(err);
            }
        }"""

html = html.replace(old_draw, new_draw)

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

import os

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_fetch = """            if(question.trim() !== '') {
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
            }"""

new_fetch = """            if(question.trim() !== '') {
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
                        // Убираем последнюю добавленную карту из истории для честности
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
            }"""

html = html.replace(old_fetch, new_fetch)

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

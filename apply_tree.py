import os

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Меняем визуал Алтаря (SVG на Картинку с Древом)
old_altar_html = """        <div class="altar-container altar-lvl-1" id="altarCrystal" onclick="tapAltar(event)">
            <div class="altar-ring-1"></div>
            <div class="altar-ring-2"></div>
            <div class="altar-orb">
                <svg viewBox="0 0 24 24" id="altarSvg" style="width:40px; height:40px; stroke:rgba(255,255,255,0.8); fill:none; stroke-width:1;">
                    <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                    <polyline points="2 17 12 22 22 17"></polyline>
                    <polyline points="2 12 12 17 22 12"></polyline>
                </svg>
            </div>
        </div>
        
        <p style="color: var(--gold-light); font-size: 14px; margin-bottom: 25px;">Тапни по сфере (+1 ✨)</p>"""

new_altar_html = """        <div class="altar-container" id="altarCrystal" onclick="tapAltar(event)" style="width: 250px; height: 250px; display: flex; justify-content: center; align-items: center;">
            <img id="altarImage" src="/images/optimized/tree_1.jpg" style="width: 100%; height: 100%; object-fit: contain; mix-blend-mode: screen; pointer-events: none; transition: 0.5s;">
        </div>
        
        <p id="starShowerTimer" style="color: #ff8c00; font-weight: bold; font-size: 15px; margin-bottom: 10px; display: none; text-shadow: 0 0 10px #ff8c00;">Астральный шторм: 30 сек (x10 Пыли!)</p>
        <p style="color: var(--gold-light); font-size: 14px; margin-bottom: 25px;">Тапни по Древу Жизни</p>"""

html = html.replace(old_altar_html, new_altar_html)

# 2. Меняем текст рекламы в Ритуалах
old_ad_html = """            <div class="bonus-item">
                <div class="bonus-icon"><svg viewBox="0 0 24 24"><path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14v-4z"></path><rect x="3" y="6" width="12" height="12" rx="2" ry="2"></rect></svg></div>
                <div class="bonus-text"><h3>Видение</h3><p>Посмотри рекламу</p></div>
                <div class="bonus-action"><button class="btn-small" onclick="showAd()">Смотреть (+100 ✨)</button></div>
            </div>"""

new_ad_html = """            <div class="bonus-item">
                <div class="bonus-icon"><svg viewBox="0 0 24 24"><path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14v-4z"></path><rect x="3" y="6" width="12" height="12" rx="2" ry="2"></rect></svg></div>
                <div class="bonus-text"><h3>Астральный Шторм</h3><p>х10 Пыли на 30 сек</p></div>
                <div class="bonus-action"><button class="btn-small" onclick="showAd()">Смотреть</button></div>
            </div>"""

html = html.replace(old_ad_html, new_ad_html)

# 3. Переписываем логику Алтаря (Жесткая математика, Смена картинок, Звездопад, Лимит рекламы)
js_altar_start = html.find('function updateAltarUI() {')
js_altar_end = html.find('function claimDailyBonus() {')

new_js_altar = """
        let starShowerTime = 0;
        let starShowerInterval = null;

        function getAdCount() {
            let data = JSON.parse(localStorage.getItem('adStats') || '{"date": "", "count": 0}');
            let today = new Date().toDateString();
            if (data.date !== today) { return 0; }
            return data.count;
        }

        function incrementAdCount() {
            let count = getAdCount();
            localStorage.setItem('adStats', JSON.stringify({"date": new Date().toDateString(), "count": count + 1}));
        }

        function activateStarShower() {
            starShowerTime = 30;
            document.getElementById('starShowerTimer').style.display = 'block';
            document.getElementById('altarCrystal').style.filter = 'drop-shadow(0 0 40px #ff8c00)';
            
            if (starShowerInterval) clearInterval(starShowerInterval);
            starShowerInterval = setInterval(() => {
                starShowerTime--;
                document.getElementById('starShowerTimer').innerText = `Астральный шторм: ${starShowerTime} сек (x10 Пыли!)`;
                if (starShowerTime <= 0) {
                    clearInterval(starShowerInterval);
                    document.getElementById('starShowerTimer').style.display = 'none';
                    updateAltarUI(); // Сбрасываем свечение
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
            
            document.getElementById('altarImage').src = `https://tarot-app-pearl-five.vercel.app/images/optimized/tree_${imgLevel}.jpg`;

            if (starShowerTime <= 0) {
                const crystal = document.getElementById('altarCrystal');
                if(altarLevel >= 20) crystal.style.filter = "drop-shadow(0 0 50px var(--gold))";
                else if(altarLevel >= 15) crystal.style.filter = "drop-shadow(0 0 30px #e6e6fa)";
                else if(altarLevel >= 10) crystal.style.filter = "drop-shadow(0 0 20px #e6e6fa)";
                else if(altarLevel >= 5) crystal.style.filter = "drop-shadow(0 0 15px #cd7f32)";
                else crystal.style.filter = "none";
            }

            checkBgLock('bg_bronze.jpg', 5);
            checkBgLock('bg_silver.jpg', 10);
            checkBgLock('bg_gold.jpg', 20);
        }

        function tapAltar(event) {
            let reward = starShowerTime > 0 ? 10 : 1;
            dust += reward;
            updateStatsUI();
            updateAltarUI();
            
            const floatingText = document.createElement('div');
            floatingText.innerText = `+${reward} ✨`;
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
                // Жесткая экспоненциальная формула роста цены (до 20 уровня дойти очень сложно)
                altarCost = Math.floor(100 * Math.pow(1.8, altarLevel - 1));
                updateStatsUI();
                updateAltarUI();
            } else {
                alert(`Не хватает пыли. Нужно еще ${altarCost - dust} ✨`);
            }
        }

"""
html = html[:js_altar_start] + new_js_altar + html[js_altar_end:]

# 4. Переписываем логику рекламы (лимит + вызов Астрального Шторма)
js_ad_start = html.find('function showAd() {')
js_ad_end = html.find('function resetCardManual() {')

new_js_ad = """function showAd() {
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
                    // Fallback для браузера (чтобы мы могли протестить без ВК)
                    incrementAdCount();
                    activateStarShower();
                    switchTab('altar', document.getElementById('navItem_altar'));
                });
            } catch(e) { 
                // Fallback для браузера
                incrementAdCount();
                activateStarShower();
                switchTab('altar', document.getElementById('navItem_altar'));
            }
        }

        """
html = html[:js_ad_start] + new_js_ad + html[js_ad_end:]

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

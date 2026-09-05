import re
import os

# 1. FIX API INDEX (Korean characters and strict valid response)
with open('tarot-app/api/index.py', 'r', encoding='utf-8') as f:
    api_code = f.read()

new_is_valid = """def is_valid_response(text: str) -> bool:
    if not text: return False
    import re
    # Вырезаем <think> теги
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = text.replace('<think>', '').replace('</think>', '')
    
    # Ищем азиатские иероглифы (Китайский, Японский, Корейский)
    if re.search(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', text): 
        return False 
        
    # Проверяем соотношение кириллицы
    letters = re.sub(r'[^a-zA-Zа-яА-ЯёЁ]', '', text)
    if not letters: 
        return True
        
    ru_letters = re.findall(r'[а-яА-ЯёЁ]', letters)
    if len(ru_letters) / len(letters) < 0.8: 
        return False 
        
    return True"""

api_code = re.sub(r'def is_valid_response\(text: str\) -> bool:.*?return True', new_is_valid, api_code, flags=re.DOTALL)

with open('tarot-app/api/index.py', 'w', encoding='utf-8') as f:
    f.write(api_code)

# 2. FIX INDEX.HTML (Altar logic + Emojis)
with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS
css_addition = """
        .dust-inline { width: 14px; height: 14px; display: inline-block; vertical-align: middle; stroke: var(--gold); fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; margin: 0 2px;}
        .energy-inline { width: 14px; height: 14px; display: inline-block; vertical-align: middle; stroke: var(--gold); fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; margin: 0 2px;}
"""
if ".dust-inline" not in html:
    html = html.replace("/* --- ЭКРАНЫ --- */", css_addition + "\n        /* --- ЭКРАНЫ --- */")

# HTML Elements Replacements (✨ and ⚡)
html = html.replace("✨", '<svg class="dust-inline" viewBox="0 0 24 24"><path d="M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9L12 2Z"/></svg>')
html = html.replace("⚡", '<svg class="energy-inline" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>')

# HTML Altar Block
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
        
        <p style="color: var(--gold-light); font-size: 14px; margin-bottom: 25px;">Тапни по сфере (+1 <svg class="dust-inline" viewBox="0 0 24 24"><path d="M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9L12 2Z"/></svg>)</p>"""

new_altar_html = """        <div class="altar-container" id="altarCrystal" onclick="tapAltar(event)" style="width: 250px; height: 250px; display: flex; justify-content: center; align-items: center; position: relative; -webkit-tap-highlight-color: transparent;">
            <img id="altarImage" src="/images/optimized/tree_1.png" style="width: 100%; height: 100%; object-fit: contain; pointer-events: none; transition: 0.5s; position: relative; z-index: 10; filter: drop-shadow(0 0 20px rgba(212,175,55,0.3));">
            <div class="altar-ring-1" id="altarRing1" style="display:none; border-top: 2px solid #cd7f32; border-bottom: 2px solid #cd7f32; animation: spinRing 4s linear infinite; position: absolute; border-radius: 50%; width: 180px; height: 180px; pointer-events: none;"></div>
            <div class="altar-ring-2" id="altarRing2" style="display:none; border-left: 2px solid #bfa1db; border-right: 2px solid #bfa1db; animation: spinRingReverse 5s linear infinite; position: absolute; border-radius: 50%; width: 140px; height: 140px; pointer-events: none;"></div>
        </div>
        
        <p id="starShowerTimer" style="color: #ff8c00; font-weight: bold; font-size: 15px; margin-bottom: 10px; display: none; text-shadow: 0 0 10px #ff8c00;">Астральный шторм: 30 сек (x10 Пыли!)</p>
        <p style="color: var(--gold-light); font-size: 14px; margin-bottom: 25px;">Тапни по Древу Жизни</p>"""

if '<div class="altar-container altar-lvl-1"' in html:
    html = html.replace(old_altar_html, new_altar_html)

# Clean up JS Alerts from SVGs
html = re.sub(r'alert\([^)]+Отправлено!\+1.*?\);', "alert('Отправлено! +1 Энергия');", html)
html = re.sub(r'alert\([^)]+Ссылка отправлена!\+1.*?\);', "alert('Ссылка отправлена! +1 Энергия');", html)
html = re.sub(r'alert\([^)]+Ежедневный ритуал выполнен.*?\);', "alert(`Ежедневный ритуал выполнен! Получено ${reward} пыли.`);", html)
html = re.sub(r'alert\([^)]+Видение получено.*?\);', "alert('Видение получено! +100 Пыли');", html)
html = re.sub(r'alert\([^)]+У вас нет Энергии.*?\);', "alert('У вас нет Энергии! Выполните Ритуал (пригласите друга или опубликуйте историю), чтобы получить попытку.');", html)
html = re.sub(r'alert\([^)]+Не хватает пыли.*?\);', "alert(`Не хватает пыли. Нужно еще ${altarCost - dust} пыли.`);", html)

# JS Block updates
js_start = html.find('function updateAltarUI() {')
js_end = html.find('function claimDailyBonus() {')

new_js = """let starShowerTime = 0;
        let starShowerInterval = null;

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

        """
if html.find('function updateAltarUI() {') != -1:
    old_update = html[html.rfind('function updateAltarUI() {') : js_end]
    html = html.replace(old_update, new_js)

# Add showAd fix
js_ad_start = html.find('function showAd() {')
js_ad_end = html.find('function resetCardManual() {')
if js_ad_start != -1:
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

        """
    html = html[:js_ad_start] + new_js_ad + html[js_ad_end:]


with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

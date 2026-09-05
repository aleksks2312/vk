import re

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_invite = """        function inviteFriend() {
            try {
                vkBridge.send("VKWebAppShowInviteBox", {}).then(data => {
                    if(data.success) { energy++; initGrimoire(); alert('Отправлено! +1 Энергия'); }
                }).catch(e => {
                    vkBridge.send("VKWebAppShare", {"link": "https://vk.com/app54632741"}).then(data => {
                        energy++; initGrimoire(); alert('Ссылка отправлена! +1 Энергия');
                    }).catch(e2 => console.log("Закрыто"));
                });
            } catch(e) { alert("Невозможно открыть вне VK."); }
        }"""

new_invite = """        function inviteFriend() {
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
        }"""

html = html.replace(old_invite, new_invite)

# Fix drawCardApi refund resetting the card
old_draw = """                        if(collectedCards[collectedCards.length - 1] === randomIndex) {
                            collectedCards.pop();
                            initGrimoire();
                        }"""
new_draw = """                        if(collectedCards[collectedCards.length - 1] === randomIndex) {
                            collectedCards.pop();
                        }
                        initGrimoire();"""
html = html.replace(old_draw, new_draw)


with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

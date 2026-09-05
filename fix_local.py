import re

with open('tarot-app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix tapAltar animation visibility
old_tap = """            floatingText.style.color = starShowerTime > 0 ? '#ff8c00' : 'var(--gold)';
            floatingText.style.fontWeight = 'bold';
            floatingText.style.pointerEvents = 'none';
            floatingText.style.zIndex = '9999';
            floatingText.style.transition = 'all 1s ease-out';"""
new_tap = """            floatingText.style.color = starShowerTime > 0 ? '#ffb347' : 'var(--gold)';
            floatingText.style.fontWeight = 'bold';
            floatingText.style.fontSize = starShowerTime > 0 ? '22px' : '16px';
            floatingText.style.textShadow = '0 2px 4px rgba(0,0,0,1)';
            floatingText.style.pointerEvents = 'none';
            floatingText.style.zIndex = '9999';
            floatingText.style.transition = 'all 1s ease-out';"""
html = html.replace(old_tap, new_tap)

# Improve checkBgLock
old_bg_lock = """        function checkBgLock(id, reqLevel) {
            const lockElem = document.getElementById('lock_' + id);
            if(altarLevel >= reqLevel) {
                if(lockElem) lockElem.style.display = 'none';
                document.getElementById('bg_' + id).classList.remove('locked');
            } else {
                if(lockElem) lockElem.style.display = 'block';
                document.getElementById('bg_' + id).classList.add('locked');
            }
        }"""
new_bg_lock = """        function checkBgLock(id, reqLevel) {
            const lockElem = document.getElementById('lock_' + id);
            const bgItem = document.getElementById('bg_' + id);
            if(altarLevel >= reqLevel) {
                if(lockElem) lockElem.style.display = 'none';
                if(bgItem) bgItem.classList.remove('locked');
            } else {
                if(lockElem) lockElem.style.display = 'block';
                if(bgItem) bgItem.classList.add('locked');
            }
        }"""
html = html.replace(old_bg_lock, new_bg_lock)

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Local fixes applied.")

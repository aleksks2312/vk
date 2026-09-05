const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fs = require('fs');
const html = fs.readFileSync('tarot-app/index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously" });
dom.window.vkBridge = { send: async () => ({ success: true, first_name: "Test" }) };

setTimeout(() => {
    dom.window.eval(`
        dust = 100000;
        upgradeAltar(); // to 2
        upgradeAltar(); // to 3
        upgradeAltar(); // to 4
        upgradeAltar(); // to 5
        upgradeAltar(); // to 6
        console.log("altarLevel:", altarLevel);
        const bgBronze = document.getElementById('bg_bg_bronze.jpg');
        const lockBronze = document.getElementById('lock_bg_bronze.jpg');
        console.log("Locked class present:", bgBronze.classList.contains('locked'));
        console.log("Lock display:", lockBronze.style.display);
    `);
}, 500);

const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fs = require('fs');

const html = fs.readFileSync('tarot-app/index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously" });

// Mock VK Bridge
dom.window.vkBridge = {
    send: async () => ({ success: true, first_name: "Test" })
};

setTimeout(() => {
    try {
        dom.window.dust = 1000;
        dom.window.upgradeAltar(); // 2
        dom.window.upgradeAltar(); // 3
        dom.window.upgradeAltar(); // 4
        dom.window.upgradeAltar(); // 5
        dom.window.upgradeAltar(); // 6
        
        console.log("Altar level:", dom.window.altarLevel);
        const bgBronze = dom.window.document.getElementById('bg_bg_bronze.jpg');
        const lockBronze = dom.window.document.getElementById('lock_bg_bronze.jpg');
        console.log("Locked class present:", bgBronze.classList.contains('locked'));
        console.log("Lock display:", lockBronze.style.display);
    } catch(e) {
        console.error("Test error:", e);
    }
}, 500);

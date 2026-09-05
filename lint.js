const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('tarot-app/index.html', 'utf8');

const dom = new JSDOM(html, { runScripts: "dangerously" });
dom.window.onerror = function(msg, url, line, col, error) {
    console.log("PAGE ERROR:", msg, line);
};
console.log("JSDOM initialized.");

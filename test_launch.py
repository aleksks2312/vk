from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox'])
        page = browser.new_page()
        page.on("console", lambda msg: print(f"CONSOLE: {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        print("Navigating to app...")
        page.goto("https://tarot-app-pearl-five.vercel.app")
        page.wait_for_timeout(5000)
        
        # Checking loader status
        loader_display = page.evaluate("document.getElementById('loader').style.display")
        print(f"Loader display is: {loader_display}")
        
        body_class = page.evaluate("document.body.className")
        print(f"Body classes: {body_class}")

        overlay_display = page.evaluate("document.getElementById('tutOverlay').style.display")
        print(f"Overlay display is: {overlay_display}")

        browser.close()

run()

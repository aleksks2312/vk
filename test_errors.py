from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox'])
        page = browser.new_page()
        page.on("console", lambda msg: print(f"CONSOLE: {msg.type} {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        print("Navigating to app...")
        page.goto("https://tarot-app-pearl-five.vercel.app")
        page.wait_for_timeout(3000)
        browser.close()

run()

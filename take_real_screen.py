from playwright.sync_api import sync_playwright
import time

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox'])
        page = browser.new_page(viewport={"width": 414, "height": 896})
        page.goto("https://tarot-app-pearl-five.vercel.app")
        page.wait_for_timeout(3000)
        # Убираем лоадер
        page.evaluate("document.getElementById('loader').style.display='none';")
        page.screenshot(path="tarot-app/images/vk_screenshot_real.jpg", type="jpeg", quality=95)
        browser.close()

take_screenshot()

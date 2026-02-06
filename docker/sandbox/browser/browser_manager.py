#!/usr/bin/python3

import threading
import tempfile
from playwright.sync_api import sync_playwright

class BrowserManager:
    def __init__(self):
        self._lock = threading.RLock()
        self._browser = None
        self._page = None
        self._playwright = None

    def _ensure_browser(self):
        if self._browser is None:
            # 在当前线程启动 playwright
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=False)

    def close_browser(self):
        with self._lock:
            if self._browser is not None:
                self._browser.close()
            if self._playwright is not None:
                self._playwright.close()
            self._browser = None
            self._playwright = None
            self._page = None

    def get_page(self):
        with self._lock:
            self._ensure_browser()
            if self._page is None:
                self._page = self._browser.new_page()
        return self._page

    def navigate_to(self, url: str):
        page = self.get_page()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        page.goto(url)
        self.debug()

    def go_back(self):
        page = self.get_page()
        page.go_back()

    def wait(self, seconds: float):
        page = self.get_page()
        page.wait_for_timeout(seconds * 1e3)

    def mouse_click(self, x, y):
        page = self.get_page()
        page.mouse.click(x,y)

    def mouse_click_then_type(self, x, y, text):
        page = self.get_page()
        page.mouse.click(x,y)
        page.keyboard.type(text, delay = 100)

    def send_keys(self, keys: str):
        page = self.get_page()
        page.keyboard.press(keys)

    def switch_tab(self, page_id: int):
        page_count = len(self._browser.pages)
        if page_id >= page_count:
            raise ValueError('page id is out of bounds')
        self._page = self._browser.pages[page_id]

    def close_tab(self, page_id: int):
        page = self.get_page()
        page.close()
        self._page = None

    def scroll_down(self, amount: int):
        page = self.get_page()
        page.evaluate(f"window.scrollBy(0, {amount})")

    def scroll_up(self, amount: int):
        page = self.get_page()
        page.evaluate(f"window.scrollBy(0, {-amount})")

    def take_screenshot(self,):
        page = self.get_page()
        img_bytes = page.screenshot(type="png")
        with tempfile.NamedTemporaryFile(suffix = ".png", delete = False) as f:
            f.write(img_bytes)
            return f.name

    def drag_and_drop(self, x1, y1, x2, y2, steps = 5):
        page = self.get_page()
        page.mouse.move(x1,y1)
        page.mouse.down()
        page.mouse.move(x2,y2,steps = steps)
        page.mouse.up()

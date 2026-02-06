#!/usr/bin/python3

from playwright.sync_api import sync_playwright

class BrowserManager:
    def __init__(self):
        self._lock = threading.RLock()  # 保证线程安全
        self._browser = None
        self._page = None
        self._playwright = None

    def _ensure_browser(self):
        if self._browser is None:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=False)

    def __del__(self):
        if self._browser is not None:
            self._browser.close()
        if self._playwright is not None:
            self._playwright.close()

    def get_page(self):
        with self._lock:
            self._ensure_browser()
            if self._page is None:
                self._page = self._browser.new_page()
        return self._page

    def navigate_to(self, url: str):
        page = self.get_page()
        page.goto(url)

    def go_back(self):
        page = self.get_page()
        page.go_back()

    def wait(self, seconds: float):
        page = self.get_page()
        page.wait_for_timeout(seconds * 1e3)

    def click_element(self, index: int):
        page = self.get_page()
        page.locator('.auto-clickable').nth(index).click()

    def input_text(self, index: int, text: str):
        page = self.get_page()
        page.locator('input').nth(index).fill(text)

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

    def is_bottom(self, page):
        scroll_y = page.evaluate("window.scrollY")
        scroll_height = page.evaluate("document.body.scrollHeight")
        client_height = page.evaluate("window.innerHeight")
        return scroll_y + client_height >= scroll_height - 5

    def scroll_to_text(self, text: str):
        page = self.get_page()
        page.evaluate("window.scrollTo(0, 0)")
        while not self.is_bottom(page):
            locator = page.get_by_text(text, exact=False)
            count = locator.count()
            if count > 0:
                locator.first().scroll_into_view_if_needed()
                return
            page.evaluate("window.scrollBy(0, 500)")
            page.wait_for_timeout(500)
        return

    def get_dropdown_options(self, index: int):
        page = self.get_page()
        locator = page.locator("select").nth(index)
        options = locator.evaluate(
            """element => {
                if (!element || element.tagName !== 'SELECT') return [];
                return Array.from(element.options).map(option => option.textContent.trim());
            }"""
        )
        return options

    def select_dropdown_option(self, index: int, text: str):
        page = self.get_page()
        locator = page.locator("select").nth(index)
        locator.select_option(label=text)

    def click_coordinates(self, x: int, y: int):
        page = self.get_page()
        page.mouse.click(x, y)

    def drag_drop(self, element_source: str, element_target: str):
        page = self.get_page()
        source_element = page.locator(f"#{element_source}")
        target_element = page.locator(f"#{element_target}")
        source_element.drag_to(target_element)

#!/usr/bin/python3

import threading
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

    def get_all_text_input_selectors(self, page):
        selector_js = """
    () => {
        const elements = Array.from(
            document.querySelectorAll(
                "input[type='text'], input:not([type]), input[type='search'], "
                + "textarea, [contenteditable][role='textbox'], [role='textbox'], "
                + "[role='searchbox'], div[role='textbox'], div[role='searchbox']"
            )
        );

        return elements.map((el, idx) => {
            // 尝试用 best practice 的 selector，比如：id、[name]、[aria-label] 等
            if (el.id) return { index: idx + 1, selector: "#" + CSS.escape(el.id) };
            if (el.name) return { index: idx + 1, selector: `input[name="${CSS.escape(el.name)}"]` };
            if (el.getAttribute('aria-label'))
                return { index: idx + 1, selector: `[aria-label="${CSS.escape(el.getAttribute('aria-label'))}"]` };
            if (el.getAttribute('placeholder'))
                return { index: idx + 1, selector: `[placeholder="${CSS.escape(el.getAttribute('placeholder'))}"]` };
            // 保底：用标签 + role + index
            return {
                index: idx + 1,
                selector: `${el.tagName.toLowerCase()}[role='${CSS.escape(el.getAttribute('role') || '')}']`
            };
        });
    }
    """
        return page.evaluate(selector_js)

    def get_all_clickable_selectors(self, page):
        js = """
    () => {
        const candidates = Array.from(
            document.querySelectorAll(
                "button, a, [role='button'], [role='link'], "
                + "[onclick], [tabindex]:not([tabindex='-1']), "
                + "input[type='button'], input[type='submit'], input[type='reset'], "
                + "input[type='image']"
            )
        );

        return candidates
            .filter(el => {
                // 过滤掉 disabled、不可见、不可交互的
                if (el.disabled || el.getAttribute('disabled') != null) return false;
                if (!el.offsetParent) return false; // 不可见
                const style = window.getComputedStyle(el);
                if (style.display === 'none' || style.visibility === 'hidden') return false;
                return true;
            })
            .map((el, idx) => {
                // 优先用 id、[name]、[aria-label] 等
                if (el.id) return { index: idx + 1, selector: '#' + CSS.escape(el.id) };
                if (el.name) return { index: idx + 1, selector: `*[name="${CSS.escape(el.name)}"]` };
                const ariaLabel = el.getAttribute('aria-label');
                if (ariaLabel) return { index: idx + 1, selector: `[aria-label="${CSS.escape(ariaLabel)}"]` };
                const text = el.textContent.trim();
                if (text) return { index: idx + 1, selector: `:text("${CSS.escape(text)}")` };
                // 保底：用标签名 + role / type
                const role = el.getAttribute('role');
                const type = el.getAttribute('type');
                if (role) return { index: idx + 1, selector: `${el.tagName.toLowerCase()}[role='${CSS.escape(role)}']` };
                if (type) return { index: idx + 1, selector: `${el.tagName.toLowerCase()}[type='${CSS.escape(type)}']` };
                return { index: idx + 1, selector: el.tagName.toLowerCase() };
            });
    }
    """
        return page.evaluate(js)

    def debug(self,):
        page = self.get_page()
        clickables = self.get_all_clickable_seletors(page)
        inputs = self.get_all_text_input_selectors(page)
        selectors = page.locator('select').all()
        element_list = f"""clickables: {clickables}
inputs: {inputs}
selectors: {selectors}"""
        with open('debug.txt', 'w') as f:
          f.write(element_list)

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

    def click_element(self, index: int):
        page = self.get_page()
        selectors = self.get_all_clickable_selectors(page)
        entry = next((s for s in selectors if s['index'] == index), None)
        if entry:
            locator = page.locator(entry['selector'])
            locator.click()
        else:
            raise ValueError(f"No clickable element found with index {index}")

    def input_text(self, index: int, text: str):
        page = self.get_page()
        selectors = self.get_all_text_input_selectors(page)
        entry = next((s for s in selectors if s['index'] == index), None)
        if entry:
            locator = page.locator(entry['selector'])
            locator.fill(text)
        else:
            raise ValueError(f"No input text box found with index {index}")

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

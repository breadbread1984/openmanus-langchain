#!/usr/bin/python3

from playwright.sync_api import sync_playwright

class BrowserManager(object):
  def __init__(self,):
    self.p = sync_playwright().start()
    self.browser = self.p.chromium.launch(headless = False)
    self.page = None
  def __def__(self,):
    self.browser.close()
    self.p.close()
  def get_page(self):
    if self.page is None:
      self.page = self.browser.new_page()
    return self.page
  def navigate_to(self, url):
    page = self.get_page()
    page.goto(url)
  def go_back(self,):
    page = self.get_page()
    page.go_back()
  def wait(self, seconds):
    page = self.get_page()
    page.wait_for_timeout(seconds * 1e3)
  def click_element(self, index):
    page = self.get_page()
    page.locator('.auto-clickable').nth(index).click()
  def input_text(self, index, text):
    page = self.get_page()
    page.locator('input').nth(index).fill(text)
  def send_keys(self, keys):
    page = self.get_page()
    page.keyboard.press(keys)
  def switch_tab(self, page_id):
    if page_id >= len(self.browser.pages):
      raise Exception('page id is out of bound')
    self.page = self.browser.pages[page_id]
  def close_tab(self, page_id):
    page = self.get_page()
    page.close()
    self.page = None
  def scroll_down(self, amount):
    page = self.get_page()
    page.evaluate(f"window.scrollBy(0, {amount})")
  def scroll_up(self, amount):
    page = self.get_page()
    page.evaluate(f"window.scrollBy(0, {-amount})")
  def is_bottom(self, page):
    scroll_y = page.evaluate("window.scrollY")
    scroll_height = page.evaluate("document.body.scrollHeight")
    client_height = page.evaluate("window.innerHeight")
    return scroll_y + client_height >= scroll_height - 5
  def scroll_to_text(self, text):
    page = self.get_page()
    page.evaluate(f"window.scrollTo(0, 0)")
    while not self.is_bottom(page):
      locator = page.get_by_text(text, exact = False)
      count = locator.count()
      if count > 0:
        locator.first().scroll_into_view_if_needed()
        return
      page.evaluate("window.scrollBy(0, 500)")
      page.wait_for_timeout(500)
    return
  def get_dropdown_options(self, index):
    page = self.get_page()
    locator = page.locator("select").nth(index)
    options = locator.evaluate(
      """element => {
        if (!element || element.tagName !== 'SELECT') return [];
        return Array.from(element.options).map(option => option.textContent.trim());
      }"""
    )
    return options
  def select_dropdown_option(self, index, text):
    page = self.get_page()
    locator = page.locator("select").nth(index)
    locator.select_option(label = text)
  def click_coordinates(self, x, y):
    page = self.get_page()
    page.mouse,click(x,y)
  def drag_drop(self, element_source, element_target):
    page = self.get_page()
    source_element = page.locator(f"#{element_source}")
    target_element = page.locator(f"#{element_target}")
    source_element.drag_to(target_element)


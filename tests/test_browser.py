#!/usr/bin/python3

import sys
from os.path import join, exists, dirname, abspath
import unittest

sys.path.append(abspath(join(dirname(__file__), '..')))

from tools import load_browser_tool
import configs

class TestBrowser(unittest.TestCase):
  def test_browser(self,):
    browser_tool = load_browser_tool(configs)
    result = browser_tool.invoke({'query': 'What is the GDP per capita of Hong Kong?'})
    print('is_done:', result.is_done)
    print('is_successful:', result.is_successful)
    print('has_errors:', result.has_errors)
    print('answer:', result.answer)
    print('screenshot_path:', result.screenshot_path)

if __name__ == "__main__":
  unittest.main()

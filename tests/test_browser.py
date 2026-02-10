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
    result = browser_tool.invoke({'query': 'What is the Hang Seng Index today?'})
    print(result)

if __name__ == "__main__":
  unittest.main()

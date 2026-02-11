#!/usr/bin/python3

import sys
from os.path import join, exists, dirname, abspath
import unittest

sys.path.append(abspath(join(dirname(__file__), '..')))

from tools import load_see_image_tool
import configs

class TestSeeImage(unittest.TestCase):
  def test_see_image(self,):
    see_image_tool = load_see_image_tool(configs)
    result = see_image_tool.invoke({'file_path': 'test.png'})
    with open('test2.png', 'wb') as f:
      f.write(result.base64)

if __name__ == "__main__":
  unittest.main()


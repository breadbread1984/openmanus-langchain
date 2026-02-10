#!/usr/bin/python3

import sys
from os.path import join, exists, dirname, abspath
import unittest

sys.path.append(abspath(join(dirname(__file__), '..')))

from tools import load_shell_tool
import configs

class TestShell(unittest.TestCase):
  def test_shell(self,):
    shell_tool = load_shell_tool(configs)
    result = shell_tool.invoke({'action': 'execute_command', 'execute_command': {'command': 'cpuinfo',}})
    print(result.output)

if __name__ == "__main__":
  unittest.main()

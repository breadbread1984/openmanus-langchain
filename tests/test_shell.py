#!/usr/bin/python3

import sys
import time
from os.path import join, exists, dirname, abspath
import unittest

sys.path.append(abspath(join(dirname(__file__), '..')))

from tools import load_shell_tool
import configs

class TestShell(unittest.TestCase):
  def test_execute_command(self,):
    shell_tool = load_shell_tool(configs)
    result = shell_tool.invoke({
      'action': 'execute_command',
      'execute_command': {
        'command': 'cpuinfo',
        'blocking': True
      }
    })
    print(result.output)
  def test_check_command_output(self,):
    shell_tool = load_shell_tool(configs)
    result = shell_tool.invoke({
      'action': 'execute_command',
      'execute_command': {
        'command': """countdown=60;
while [ $countdown -gt 0 ]; do 
    echo \"countdown: $countdown seconds\";
    sleep 1;
    countdown=$((countdown-1)); 
done""",
        'blocking': False
      }
    })
    print(result.completed)
    assert result.session_name is not None
    time.sleep(4)
    result = shell_tool.invoke({
      'action': 'check_command_output',
      'check_command_output': {
        'session_name': result.session_name,
      }
    })
    print(result.output, result.completed)

if __name__ == "__main__":
  unittest.main()

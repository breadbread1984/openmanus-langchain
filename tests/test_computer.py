#!/usr/bin/python3

import sys
from os.path import join, exists, dirname, abspath
import unittest

sys.path.append(abspath(join(dirname(__file__), '..')))

import base64
from tools import load_computer_tool
import configs

class TestComputer(unittest.TestCase):
  def test_move_to(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'move_to',
      'move_to': {
        'x': 300,
        'y': 300,
      }
    })
  def test_click(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'click',
      'click': {
        'x': 400,
        'y': 400,
        'button': 'left'
      }
    })
  def test_scroll(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'scroll',
      'scroll': {
        'amount': 10
      }
    })
  def test_typing(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'typing',
      'typing': {
        'text': 'test abc'
      }
    })
  def test_press(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'press',
      'press': {
        'key': 'a'
      }
    })
  def test_wait(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'wait',
      'wait': {
        'duration': 3
      }
    })
  def test_mouse_down(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'mouse_down',
      'mouse_down': {
        'x': 400,
        'y': 400,
        'button': 'right'
      }
    })
  def test_mouse_up(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'mouse_up',
      'mouse_up': {
        'x': 400,
        'y': 400,
        'button': 'right'
      }
    })
  def test_drag_to(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'drag_to',
      'drag_to': {
        'x': 500,
        'y': 500,
      }
    })
  def test_hotkey(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'hotkey',
      'hotkey': {
        'keys': 'ctrl+c'
      }
    })
  def test_screenshot(self,):
    computer_tool = load_computer_tool(configs)
    result = computer_tool.invoke({
      'action': 'screenshot',
      'screenshot': {}
    })
    img_bytes = base64.b64decode(result.screenshot.encode('utf-8'))
    with open('screenshot.png', 'wb') as f:
      f.write(img_bytes)

if __name__ == "__main__":
  unittest.main()

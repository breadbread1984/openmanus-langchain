#!/usr/bin/python3

import sys
from os.path import join, exists, dirname, abspath
import unittest

sys.path.append(abspath(join(dirname(__file__), '..')))

from tools import load_file_management_tool
import configs

class TestFileManagement(unittest.TestCase):
  def test_copy_file(self,):
    file_tool = load_file_management_tool(configs)
    result = file_tool.invoke({
      'action': 'write_file',
      "write_file": {
        "file_path": "test.txt",
        "text": "test abc"
      }
    })
    print(result)
    result = file_tool.invoke({
      'action': 'copy_file',
      'copy_file': {
        'source_path': 'test.txt',
        'destination_path': 'test1.txt'
      }
    })
    print(result)
  def test_delete_file(self,):
    file_tool = load_file_management_tool(configs)
    result = file_tool.invoke({
      'action': 'write_file',
      "write_file": {
        "file_path": "test.txt",
        "text": "test abc"
      }
    })
    print(result)
    result = file_tool.invoke({
      'action': 'file_delete',
      'file_delete': {
        "file_path": "test.txt"
      }
    })
    print(result)
  def test_search_file(self,):
    file_tool = load_file_management_tool(configs)
    result = file_tool.invoke({
      'action': 'write_file',
      "write_file": {
        "file_path": "test.txt",
        "text": "test abc"
      }
    })
    print(result)
    result = file_tool.invoke({
      'action': 'file_search',
      'file_search': {
        'dir_path': '.',
        'pattern': 'tes*'
      }
    })
    print(result)
  def test_list_dir(self,):
    file_tool = load_file_management_tool(configs)
    result = file_tool.invoke({
      'action': 'write_file',
      "write_file": {
        "file_path": "test.txt",
        "text": "test abc"
      }
    })
    print(result)
    result = file_tool.invoke({
      'action': 'list_directory',
      'list_directory': {
        'dir_path': '.'
      }
    })
    print(result)
  def test_move_file(self,):
    file_tool = load_file_management_tool(configs)
    result = file_tool.invoke({
      'action': 'write_file',
      "write_file": {
        "file_path": "test.txt",
        "text": "test abc"
      }
    })
    print(result)
    result = file_tool.invoke({
      'action': 'move_file',
      'move_file': {
        'source_path': 'test.txt',
        'destination_path': 'test1.txt'
      }
    })
    print(result)
  def test_read_file(self,):
    file_tool = load_file_management_tool(configs)
    result = file_tool.invoke({
      'action': 'write_file',
      "write_file": {
        "file_path": "test.txt",
        "text": "test abc"
      }
    })
    print(result)
    result = file_tool.invoke({
      'action': 'read_file',
      'read_file': {
        'file_path': 'test.txt'
      }
    })
    print(result)
  def test_write_file(self,):
    file_tool = load_file_management_tool(configs)
    result = file_tool.invoke({
      'action': 'write_file',
      "write_file": {
        "file_path": "test.txt",
        "text": "test abc"
      }
    })
    print(result)

if __name__ == "__main__":
  unittest.main()

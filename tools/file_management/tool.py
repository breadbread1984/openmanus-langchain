#!/usr/bin/python3

from typing import List
from langchain_core.tools import BaseTool
from langchain_community.agent_toolkits import FileManagementToolkit

def load_file_management_tools(configs) -> List[BaseTool]:
  tools = FileManagementToolkit(
    root_dir = configs.workspace_dir,
    selected_tools = ["copy_file", "file_delete", "file_search", "list_directory", "move_file", "read_file", "write_file"]
  ).get_tools()
  return tools

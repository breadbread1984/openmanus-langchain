#!/usr/bin/python3

from typing import List
from pydantic import BaseModel, Field, ValidationError, model_validator
from langchain_core.tools import BaseTool
from langchain_core.tools.structured import StructuredTool
from langchain_community.agent_toolkits import FileManagementToolkit

def load_file_management_tool(configs):
  class CopyFile(BaseModel):
    source_path: str = Field(..., description = "Path of the file to copy")
    destination_path: str = Field(..., description = "Path to save the copied file")
  class FileDelete(BaseModel):
    file_path: str = Field(..., description = "Path of the file to delete")
  class FileSearch(BaseModel):
    dir_path: str = Field(default = ".", description = "Subdirectory to search in.")
    pattern: str = Field(..., description = "Unix shell regex, where * matches everything.")
  class ListDirectory(BaseModel):
    dir_path: str = Field(default = ".", description = "Subdirectory to list.")
  class MoveFile(BaseModel):
    source_path: str = Field(..., description = "Path of the file to move")
    destination_path: str = Field(..., description = "New path for the moved file")
  class ReadFile(BaseModel):
    file_path: str = Field(..., description = "name of file")
  class WriteFile(BaseModel):
    file_path: str = Field(..., description = "name of file")
    text: str = Field(..., description="text to write to file")
    append: bool = Field(default=False, description="Whether to append to an existing file.")
  class FileManagementInput(BaseModel):
    action: Literal["copy_file", "file_delete", "file_search", "list_directory", "move_file", "read_file", "write_file"] = Field(..., description = "a file management action")
    copy_file: Optional[CopyFile] = Field(None, description = "parameters for action 'copy_file'")
    file_delete: Optional[FileDelete] = Field(None, description = "parameters for action 'file_delete'")
    file_search: Optional[FileSearch] = Field(None, description = "parameters for action 'file_search'")
    list_directory: Optional[ListDirectory] = Field(None, description = "parameters for action 'list_directory'")
    move_file: Optional[MoveFile] = Field(None, description = "parameters for action 'move_file'")
    read_file: Optional[ReadFile] = Field(None, description = "parameters for action 'read_file'")
    write_file: Optional[WriteFile] = Field(None, description = "parameters for action 'write_file'")
    @model_validator(mode = "after")
    @classmethod
    def require_action_specific_field(cls, self):
      if self.action == "copy_file" and self.copy_file is None:
        raise ValueError("copy_file must be provided when action is 'copy_file'")
      elif self.action == "file_delete" and self.file_delete is None:
        raise ValueError("file_delete must be provided when action is 'file_delete'")
      elif self.action == "file_search" and self.file_search is None:
        raise ValueError("file_search must be provided when action is 'file_search'")
      elif self.action == "list_directory" and self.list_directory is None:
        raise ValueError("list_directory must be provided when action is 'list_directory'")
      elif self.action == "move_file" and self.move_file is None:
        raise ValueError("move_file must be provided when action is 'move_file'")
      elif self.action == "read_file" and self.read_file is None:
        raise ValueError("read_file must be provided when action is 'read_file'")
      elif self.action == "write_file" and self.write_file is None:
        raise ValueError("write_file must be provided when action is 'write_file'")
      return self
  class FileManagementOutput(BaseModel):
    result: str = Field(description = "file management process result")
  class FileManagementConfig(BaseModel):
    class Config:
      arbitrary_types_allowed = True
    tools: Dict[str, BaseModel]
  class FileManagementTool(StructuredTool):
    name: str = "file_management"
    description: str = "This toolkit provides methods to interact with local files. available actions are copy_file, file_delete, file_search, list_directory, move_file, read_file and write_file."
    args_schema: Type[BaseModel] = FileManagementInput
    config: FileManagementConfig
    def _run(self, action, copy_file = None, file_delete = None, file_search = None, list_directory = None, move_file = None, read_file = None, write_file = None, run_manager: Optional[CallbackManagerForToolRun] = None):
      if action == "copy_file":
        assert copy_file is not None, "copy_file is None!"
        result = self.config.tools['copy_file'].invoke({'source_path': copy_file.source_path, 'destination_path': copy_file.destination_path})
      elif action == "file_delete":
        assert file_delete is not None, "file_delete is None!"
        result = self.config.tools['file_delete'].invoke({'file_path': file_delete.file_path})
      elif action == "file_search":
        assert file_search is not None, "file_search is None!"
        result = self.config.tools['file_search'].invoke({'pattern': file_search.pattern, 'dir_path': file_search.dir_path})
      elif action == "list_directory":
        assert list_directory is not None, "list_directory is None!"
        result = self.config.tools['list_directory'].invoke({'dir_path': list_directory.dir_path})
      elif action == "move_file":
        assert move_file is not None, "move_file is None!"
        result = self.config.tools['move_file'].invoke({'source_path': move_file.source_path, 'destination_path': move_file.destination_path})
      elif action == "read_file":
        assert read_file is not None, "read_file is None!"
        result = self.config.tools['read_file'].invoke({'file_path': read_file.file_path})
      elif action == "write_file":
        assert write_file is not None, "write_file is None!"
        result = self.config.tools['write_file'].invoke({'file_path': write_file.file_path, 'text': write_file.text, 'append': write_file.append})
      else:
        raise Exception('unknown action!')
      return FileManagementOutput(result = result)
    async def _arun(self, action, copy_file = None, file_delete = None, file_search = None, list_directory = None, move_file = None, read_file = None, write_file = None, run_manager: Optional[CallbackManagerForToolRun] = None):
      raise NotImplementedError("Async execution is not supported!")
  return FileManagementTool(config = FileManagementConfig(tools = {t.name: t for t in FileManagementToolkit(root_dir = configs.workspace_dir).get_tools()}))

#!/usr/bin/python3

from typing import Type, List, Optional, Annotated, Literal, Union
from pydantic import BaseModel, Field, ValidationError, model_validator
from langchain_core.tools.structured import StructuredTool
from langchain_core.callbacks.manager import CallbackManagerForToolRun
from langgraph.prebuilt import InjectedState
import libtmux

def load_shell_tool(configs):
  class ExecuteCommand(BaseModel):
    command: str = Field(description = "The shell command to execute. Use this for running CLI tools, installing packages, or system operations. Commands can be chained using &&, ||, and | operators.")
    folder: Optional[str] = Field(None, description = "Optional relative path to a subdirectory of /workspace where the command should be executed. Example: 'data/pdfs'")
    session_name: Optional[str] = Field(None, description = "Optional name of the tmux session to use. Use named sessions for related commands that need to maintain state. Defaults to a random session name.")
    blocking: Optional[bool] = Field(False, description = "Whether to wait for the command to complete. Defaults to false for non-blocking execution.")
    timeout: Optional[int] = Field(60, description = "Optional timeout in seconds for blocking commands. Defaults to 60. Ignored for non-blocking commands.")
  class CheckCommandOutput(BaseModel):
    session_name: Optional[str] = Field(None, description = "Optional name of the tmux session to use. Use named sessions for related commands that need to maintain state. Defaults to a random session name.")
    kill_session: Optional[bool] = Field(False, description = "Whether to terminate the tmux session after checking. Set to true when you're done with the command.")
  class TerminateCommand(BaseModel):
    session_name: Optional[str] = Field(None, description = "Optional name of the tmux session to use. Use named sessions for related commands that need to maintain state. Defaults to a random session name.")
  class ListCommands(BaseModel):
    pass
  class ShellInput(BaseModel):
    action: Literal['execute_command', 'check_command_output', 'terminate_command', 'list_commands'] = Field(description = "the shell action to perform")
    execute_command: Optional[ExecuteCommand] = Field(None, description = "parameters for action 'execute_command'")
    check_command_output: Optional[CheckCommandOutput] = Field(None, description = "parameters for action 'check_command_output'")
    terminate_command: Optional[TerminateCommand] = Field(None, description = "parameters for action 'terminate_command'")
    list_commands: Optional[ListCommands] = Field(None, description = "parameters for action 'list_commands'")
    @model_validator(mode = "after")
    def require_action_specific_field(self,)->ShellInput:
      action = self.action
      if action == "execute_command":
        if self.execute_command is None:
          raise ValueError("execute_command must be provided when action is 'execute_command'")
      elif action == "check_command_output":
        if self.check_command_output is None:
          raise ValueError("check_command_output must be provided when action is 'check_command_output'")
      elif action == "terminate_command":
        if self.terminate_command is None:
          raise ValueError("terminate_command must be provided when action is 'terminate_command'")
      elif action == "list_commands":
        if self.list_commands is None:
          raise ValueError("list_commands must be provided when action is 'list_commands'")
      return self
  class ShellOutput(BaseModel):
    output: Optional[str] = Field(None, description = "output string")
    error: Optional[str] = Field(None, description = "error message")
  class ShellConfig(BaseModel):
    class Config:
      arbitrary_types_allowed = True
    server: libtmux.Server
  class ShellTool(StructuredTool):
    name: str = "shell"
    description: str = """Execute a shell command in the workspace directory.
IMPORTANT: Commands are non-blocking by default and run in a tmux session.
This is ideal for long-running operations like starting servers or build processes.
Uses sessions to maintain state between commands.
This tool is essential for running CLI tools, installing packages, and managing system operations."""
    args_schema: Type[BaseModel] = ShellInput
    config: ShellConfig
    async def _arun(self, action, execute_command = None, check_command_output = None, terminate_command = None, list_commands = None, state: Annotated[dict, InjectedState], run_manager: Optional[CallbackManagerForToolRun] = None):
      if action == "execute_command":
        assert execute_command is not None, "execute_command is None!"
        # TODO
      elif action == "check_command_output":
        assert check_command_output is not None, "check_command_output is None!"
        # TODO
      elif action == "terminate_command":
        assert terminate_command is not None, "terminate_command is None!"
        # TODO
      elif action == "list_commands":
        assert list_commands is not None, "list_commands is None!"
        # TODO
      else:
        raise Exception("unknown action!")
    def _run(self, action, execute_command = None, check_command_output = None, terminate_command = None, list_commands = None, state: Annotated[dict, InjectedState], run_manager: Optional[CallbackManagerForToolRun] = None):
      

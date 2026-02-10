#!/usr/bin/python3

from uuid import uuid4
import time
from os import makedirs
from os.path import join, exists
from typing import Type, List, Optional, Annotated, Literal, Union
from pydantic import BaseModel, Field, ValidationError, model_validator
from langchain_core.tools.structured import StructuredTool
from langchain_core.callbacks.manager import CallbackManagerForToolRun
import libtmux

# NOTE: langchain-community has ShellTool which provide shell execution, but it cannot handle commands which blocks terminal

def load_shell_tool(configs):
  class ExecuteCommand(BaseModel):
    command: str = Field(description = "The shell command to execute. Use this for running CLI tools, installing packages, or system operations. Commands can be chained using &&, ||, and | operators.")
    folder: Optional[str] = Field(None, description = "Optional relative path to a subdirectory of /workspace where the command should be executed. Example: 'data/pdfs'")
    session_name: Optional[str] = Field(None, description = "Optional name of the tmux session to use. Use named sessions for related commands that need to maintain state.")
    blocking: Optional[bool] = Field(False, description = "Whether to wait for the command to complete. Defaults to false for non-blocking execution.")
    timeout: Optional[int] = Field(60, description = "Optional timeout in seconds for blocking commands. Defaults to 60. Ignored for non-blocking commands.")
  class CheckCommandOutput(BaseModel):
    session_name: str = Field(description = "name of the tmux session to use. Use named sessions for related commands that need to maintain state.")
  class TerminateCommand(BaseModel):
    session_name: str = Field(description = "name of the tmux session to use. Use named sessions for related commands that need to maintain state.")
  class ListSessions(BaseModel):
    pass
  class ShellInput(BaseModel):
    action: Literal['execute_command', 'check_command_output', 'terminate_command', 'list_sessions'] = Field(description = "the shell action to perform")
    execute_command: Optional[ExecuteCommand] = Field(None, description = "parameters for action 'execute_command'")
    check_command_output: Optional[CheckCommandOutput] = Field(None, description = "parameters for action 'check_command_output'")
    terminate_command: Optional[TerminateCommand] = Field(None, description = "parameters for action 'terminate_command'")
    list_sessions: Optional[ListSessions] = Field(None, description = "parameters for action 'list_sessions'")
    @model_validator(mode = "after")
    @classmethod
    def require_action_specific_field(cls, self):
      if self.action == "execute_command":
        if self.execute_command is None:
          raise ValueError("execute_command must be provided when action is 'execute_command'")
      elif self.action == "check_command_output":
        if self.check_command_output is None:
          raise ValueError("check_command_output must be provided when action is 'check_command_output'")
      elif self.action == "terminate_command":
        if self.terminate_command is None:
          raise ValueError("terminate_command must be provided when action is 'terminate_command'")
      elif self.action == "list_sessions":
        if self.list_sessions is None:
          raise ValueError("list_sessions must be provided when action is 'list_sessions'")
      return self
  class ShellOutput(BaseModel):
    session_name: Optional[str] = Field(None, description = "Optional name of the tmux session to use.")
    output: Optional[str] = Field(None, description = "output of the input command or a list of available session names")
    completed: bool = Field(False, description = "whether the command completed?")
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
    workspace_path: str = Field(default = "/workspace")
    done_marker: str = Field(default = f"DONE_{str(uuid4())}")
    def _run(self, action, execute_command = None, check_command_output = None, terminate_command = None, list_sessions = None, run_manager: Optional[CallbackManagerForToolRun] = None):
      if action == "execute_command":
        assert execute_command is not None, "execute_command is None!"
        # 1) create session or get session
        session_name = f"session_{str(uuid4())[:8]}" if execute_command.session_name is None else execute_command.session_name
        matches = list(filter(lambda s:s.session_name == session_name, self.config.server.sessions))
        if len(matches) == 0:
          session = self.config.server.new_session(session_name = session_name)
        else:
          session = matches[0]
        # 2) goto working dir
        cwd = self.workspace_path
        if execute_command.folder is not None:
          cwd = join(self.workspace_path, execute_command.folder)
          if not exists(cwd): makedirs(cwd)
        # 3) execute command
        command = f""" cd {cwd} ; {execute_command.command} ; echo "{self.done_marker}" """
        window = session.active_window
        pane = window.active_pane
        pane.send_keys(command)
        # 4) block or not
        if execute_command.blocking == True:
          start_time = time.time()
          while (time.time() - start_time) < execute_command.timeout:
            time.sleep(2)
            lines = pane.capture_pane()
            # watch for done marker in output
            if any(self.done_marker == line.strip() for line in lines):
              # 5) capture output, kill session and return
              output = "\n".join(pane.capture_pane()[:-1])
              session.kill()
              return ShellOutput(session_name = session_name, output = output, completed = True)
        # 5) return session_name
        return ShellOutput(session_name = session_name, completed = False)
      elif action == "check_command_output":
        assert check_command_output is not None, "check_command_output is None!"
        matches = list(filter(lambda s:s.session_name == check_command_output.session_name, self.config.server.sessions))
        assert len(matches) != 0, "cannot find session with given session_name"
        session = matches[0]
        window = session.active_window
        pane = window.active_pane
        lines = pane.capture_pane()
        if any(self.done_marker == line.strip() for line in lines):
          output = "\n".join(pane.capture_pane())
          return ShellOutput(session_name = check_command_output.session_name, output = output, completed = True)
        else:
          output = "\n".join(pane.capture_pane())
          return ShellOutput(session_name = check_command_output.session_name, output = output, completed = False)
      elif action == "terminate_command":
        assert terminate_command is not None, "terminate_command is None!"
        matches = list(filter(lambda s:s.session_name == terminate_command.session_name, self.config.server.sessions))
        assert len(matches) != 0, "cannot find session with given session_name"
        session = matches[0]
        session.kill()
        return ShellOutput(completed = True)
      elif action == "list_sessions":
        assert list_sessions is not None, "list_sessions is None!"
        sessions = [s.session_name for s in self.config.server.sessions]
        return ShellOutput(output = json.dumps(sessions, indent = 2, ensure_ascii = False), completed = True)
      else:
        raise Exception("unknown action!")
    async def _arun(self, action, execute_command = None, check_command_output = None, terminate_command = None, list_sessions = None, run_manager: Optional[CallbackManagerForToolRun] = None):
      raise NotImplementedError("Async execution is not supported!")
  return ShellTool(config = ShellConfig(server = libtmux.Server()))

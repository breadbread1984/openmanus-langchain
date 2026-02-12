#!/usr/bin/python3

import time
import tempfile
import base64
from typing import Type, List, Optional, Annotated, Literal, Union
from pydantic import BaseModel, Field, model_validator
from langchain_core.tools.structured import StructuredTool
from langchain_core.callbacks.manager import CallbackManagerForToolRun
import pyautogui

KEYBOARD_KEYS = [
  "a", "b", "c", "d", "e", "f", "g", "h", "i",
  "j", "k", "l", "m", "n", "o", "p", "q", "r",
  "s", "t", "u", "v", "w", "x", "y", "z", "0",
  "1", "2", "3", "4", "5", "6", "7", "8", "9",
  "enter", "esc", "backspace", "tab", "space",
  "delete", "ctrl", "alt", "shift", "win", "up",
  "down", "left", "right", "f1", "f2", "f3",
  "f4", "f5", "f6", "f7", "f8", "f9", "f10",
  "f11", "f12"]
HOT_KEYS = ["ctrl+c", "ctrl+v", "ctrl+x",
  "ctrl+z", "ctrl+a", "ctrl+s", "alt+tab",
  "alt+f4", "ctrl+alt+delete",
]

def load_computer_tool(configs):
  class MoveTo(BaseModel):
    x: int = Field(description = "X coordinate for mouse actions")
    y: int = Field(description = "Y coordinate for mouse actions")
  class Click(BaseModel):
    x: Optional[int] = Field(None, description = "X coordinate for mouse actions")
    y: Optional[int] = Field(None, description = "Y coordinate for mouse actions")
    button: Optional[Literal['left', 'right', 'middle']] = Field(None, description = "Mouse button for click/drag actions")
    num_clicks: Optional[Literal[1,2]] = Field(default = 1, description = "Number of clicks to perform")
  class Scroll(BaseModel):
    amount: int = Field(description = "scroll amount (positive for up, negative for down)", ge = -10, le = 10)
  class Typing(BaseModel):
    text: str = Field(description = "Text to type")
  class Press(BaseModel):
    key: Literal[*KEYBOARD_KEYS] = Field(description = "Key to press")
  class Wait(BaseModel):
    duration: int = Field(description = "Duration in seconds to wait")
  class MouseDown(BaseModel):
    x: Optional[int] = Field(None, description = "X coordinate for mouse actions")
    y: Optional[int] = Field(None, description = "Y coordinate for mouse actions")
    button: Optional[Literal['left', 'right', 'middle']] = Field(None, description = "Mouse button for click/drag actions")
  class MouseUp(BaseModel):
    x: Optional[int] = Field(None, description = "X coordinate for mouse actions")
    y: Optional[int] = Field(None, description = "Y coordinate for mouse actions")
    button: Optional[Literal['left', 'right', 'middle']] = Field(None, description = "Mouse button for click/drag actions")
  class DragTo(BaseModel):
    x: int = Field(description = "X coordinate for mouse actions")
    y: int = Field(description = "Y coordinate for mouse actions")
  class HotKey(BaseModel):
    keys: Literal[*HOT_KEYS] = Field(description = "Key combination to press")
  class Screenshot(BaseModel):
    pass
  class ComputerInput(BaseModel):
    action: Literal['move_to', 'click', 'scroll', 'typing', 'press', 'wait', 'mouse_down', 'mouse_up', 'drag_to', 'hotkey', 'screenshot'] = Field(description = "The compute action to perform")
    move_to: Optional[MoveTo] = Field(None, "parameters for action 'move_to'")
    click: Optional[Click] = Field(None, "parameters for action 'click'")
    scroll: Optional[Scroll] = Field(None, "parameters for action 'scroll'")
    typing: Optional[Typing] = Field(None, "parameters for action 'typing'")
    press: Optional[Press] = Field(None, "parameters for action 'press'")
    wait: Optional[Wait] = Field(None, "parameters for action 'wait'")
    mouse_down: Optional[MouseDown] = Field(None, "parameters for action 'mouse_down'")
    mouse_up: Optional[MouseUp] = Field(None, "parameters for action 'mouse_up'")
    drag_to: Optional[DragTo] = Field(None, "parameters for action 'drag_to'")
    hotkey: Optional[HotKey] = Field(None, "parameters for action 'hotkey'")
    screenshot: Optional[Screenshot] = Field(None, "parameter for action 'screenshot'")
    @model_validator(mode = "after")
    @classmethod
    def require_action_specific_field(cls, self):
      if self.action == "move_to" and self.move_to is None:
        raise ValueError("move_to must be provided when action is 'move_to'")
      elif self.action == "click" and self.click is None:
        raise ValueError("click must be provided when action is 'click'")
      elif self.action == "scroll" and self.scroll is None:
        raise ValueError("scroll must be provided when action is 'scroll'")
      elif self.action == "typing" and self.typing is None:
        raise ValueError("typing must be provided when action is 'typing'")
      elif self.action == "press" and self.press is None:
        raise ValueError("press must be provided when action is 'press'")
      elif self.action == "wait" and self.wait is None:
        raise ValueError("wait must be provided when action is 'wait'")
      elif self.action == "mouse_down" and self.mouse_down is None:
        raise ValueError("mouse_down must be provided when action is 'mouse_down'")
      elif self.action == "mouse_up" and self.mouse_up is None:
        raise ValueError("mouse_up must be provided when action is 'mouse_up'")
      elif self.action == "drag_to" and self.drag_to is None:
        raise ValueError("drag_to must be provided when action is 'drag_to'")
      elif self.action == "hotkey" and self.hotkey is None:
        raise ValueError("hotkey must be provided when action is 'hotkey'")
      elif self.action == "screenshot" and self.screenshot is None:
        raise ValueError("screenshot must be provided when action is 'screenshot'")
      return self
  class ComputerOutput(BaseModel):
    screenshot: Optional[str] = Field(None, description = "optional screenshot (png format) in base64 format of action 'screenshot'")
  class ComputerTool(StructuredTool):
    name: str = "computer_use"
    description: str = "Computer automation tool for controlling the desktop environment."
    args_schema: Type[BaseModel] = ComputerInput
    def _run(self, action, move_to = None, click = None, scroll = None, typing = None, press = None, wait = None, mouse_down = None, mouse_up = None, drag_to = None, hotkey = None, screenshot = None, run_manager: Optional[CallbackManagerForToolRun] = None):
      if action == "move_to":
        assert move_to is not None, "move_to is None!"
        pyautogui.moveTo(move_to.x, move_to.y)
        return ComputerTool()
      elif action == "click":
        assert click is not None, "click is None!"
        if click.num_clicks == 1:
          pyautogui.click(x = click.x, y = click.y, button = click.button)
        elif click.num_clicks == 2:
          pyautogui.doubleClick(x = click.x, y = click.y, button = click.button)
        else:
          raise "unknown number of mouse clicks!"
        return ComputerTool()
      elif action == "scroll":
        assert scroll is not None, "scroll is None!"
        pyautogui.scroll(scroll.amount)
        return ComputerTool()
      elif action == "typing":
        assert typing is not None, "typing is None!"
        pyautogui.typewrite(typing.text, interval = 0.01)
        return ComputerTool()
      elif action == "press":
        assert press is not None, "press is None!"
        pyautogui.press(press.key)
        return ComputerTool()
      elif action == "wait":
        assert wait is not None, "wait is None!"
        time.sleep(wait.duration)
        return ComputerTool()
      elif action == "mouse_down":
        assert mouse_down is not None, "mouse_down is None!"
        pyautogui.mouseDown(x = mouse_down.x, y = mouse_down.y, button = mouse_down.button)
        return ComputerTool()
      elif action == "mouse_up":
        assert mouse_up is not None, "mouse_up is None!"
        pyautogui.mouseUp(x = mouse_up.x, y = mouse_up.y, button = mouse_up.button)
        return ComputerTool()
      elif action == "drag_to":
        assert drag_to is not None, "drag_to is None!"
        pyautogui.dragTo(x = drag_to.x, y = drag_to.y, duration = 0.3, button = 'left')
        return ComputerTool()
      elif action == "hotkey":
        assert hotkey is not None, "hotkey is None!"
        keys = hotkey.keys.split('+')
        pyautogui.hotkey(*keys, interval = 0.01)
        return ComputerTool()
      elif action == "screenshot":
        assert screenshot is not None, "screenshot is None!"
        img = pyautogui.screenshot()
        with tempfile.NamedTemporaryFile(suffix = ".png", delete = True) as f:
          temp_path = f.name
          f.close()
        img.save(temp_path, format = 'PNG')
        with open(temp_path, 'rb') as f:
          img_bytes = f.read()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return ComputerTool(screenshot = img_base64)
      else:
        raise Exception('unknown action!')
  return ComputerTool()


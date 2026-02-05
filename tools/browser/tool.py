#!/usr/bin/python3

from typing import Type, List, Optional, Annotated, Literal, Union
from pydantic import BaseModel, Field, validator, root_validator
from langchain_core.tools.structured import StructuredTool

def load_browswer_tool():
  class NavigateTo(BaseModel):
    url: str = Field(description = "URL for 'navigate_to' action")
  class GoBack(BaseModel):
    pass
  class Wait(BaseModel):
    seconds: int = Field(description = "Seconds to wait for load")
  class ClickElement(BaseModel):
    index: int = Field(description = "Element index for interaction actions")
  class InputText(BaseModel):
    index: int = Field(description = "Element index for interaction actions")
    text: str = Field(description = "Text for input or scroll actions")
  class SendKeys(BaseModel):
    keys: str = Field(description = "Keys to send for keyboard actions")
  class SwitchTab(BaseModel):
    page_id: int = Field(description = "Tab ID for tab management actions")
  class CloseTab(BaseModel):
    page_id: int = Field(description = "Tab ID for tab management actions")
  class ScrollDown(BaseModel):
    amount: int = Field(description = "Pixel amount to scroll")
  class ScrollUp(BaseModel):
    amount: int = Field(description = "Pixel amount to scroll")
  class ScrollToText(BaseModel):
    text: str = Field(description = "Text for input or scroll actions")
  class GetDropdownOptions(BaseModel):
    index: int = Field(description = "Element index for interaction actions")
  class SelectDropdownOption(BaseModel):
    index: int = Field(description = "Element index for interaction actions")
    text: str = Field(description = "Text for input or scroll actions")
  class ClickCoordinates(BaseModel):
    x: int = Field(description = "X coordinate for click or drag actions")
    y: int = Field(description = "Y coordinate for click or drag actions")
  class DragDrop(BaseModel):
    element_source: str = Field(description = "Source element for drag and drop")
    element_target: str = Field(description = "Target element for drag and drop")

  class BrowserInput(BaseModel):
    action: Literal["navigate_to", "go_back", "wait", "click_element", "input_text",
                    "send_keys", "switch_tab", "close_tab", "scroll_down", "scroll_up",
                    "scroll_to_text", "get_dropdown_options", "select_dropdown_option", "click_coordinates", "drag_drop",] = Field(description = "The browser action to perform")
    navigate_to: Optional[NavigateTo] = Field(None, description = "parameters for action navigate_to")
    go_back: Optional[GoBack] = Field(None, description = "parameters for action go_back")
    wait: Optional[Wait] = Field(None, description = "parameters for action wait")
    click_element: Optional[ClickElement] = Field(None, description = "paramters for action click_element")
    input_text: Optional[InputText] = Field(None, description = "parameters for action input_text")
    send_keys: Optional[SendKeys] = Field(None, description = "parameters for action send_keys")
    switch_tab: Optional[SwitchTab] = Field(None, description = "parameters for action switch_tab")
    close_tab: Optional[CloseTab] = Field(None, description = "paramters for action close_tab")
    scroll_down: Optional[ScrollDown] = Field(None, description = "parameters for action scroll_down")
    scroll_up: Optional[ScrollUp] = Field(None, description = "parameters for action scroll_up")
    scroll_to_text: Optional[ScrollToText] = Field(None, description = "parameters for action scroll_to_text")
    get_dropdown_options: Optional[GetDropdownOptions] = Field(None, description = "parameters for action get_dropdown_options")
    select_dropdown_option: Optional[SelectDropdownOption] = Field(None, description = "parameters for action select_dropdown_option")
    click_coordinates: Optional[ClickCoordinates] = Field(None, description = "parameters for action click_coordinates")
    drag_drop = Optional[DragDrop] = Field(None, description = "parameters for action drag_drop")

    @root_validator
    def validate_action_and_parameters(cls, values):
      action = values.get('action')
      required_fields = {
        "navigate_to": "navigate_to",
        "go_back": "go_back",
        "wait": "wait",
        "click_element": "click_element",
        "input_text": "input_text",
        "send_keys": "send_keys",
        "switch_tab": "switch_tab",
        "close_tab": "close_tab",
        "scroll_down": "scroll_down",
        "scroll_up": "scroll_up",
        "scroll_to_text": "scroll_to_text",
        "get_dropdown_options": "get_dropdown_options",
        "select_dropdown_option": "select_dropdown_option",
        "click_coordinates": "click_coordinates",
        "drag_drop": "drag_drop",
      }
      if action in required_fields:
        field_name = required_fields[action]
        if values.get(field_name) is None:
          raise ValueError(f"When action is '{action}', the field '{field_name}' must not be None.")
      return values

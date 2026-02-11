#!/usr/bin/python3

import asyncio
from typing import Type, List, Optional, Annotated, Literal, Union
from pydantic import BaseModel, Field, validator, root_validator
from langchain_core.tools.structured import StructuredTool
from langchain_core.callbacks.manager import CallbackManagerForToolRun
from browser_use import Agent, ChatOpenAI

def load_browser_tool(configs):
  class BrowserInput(BaseModel):
    query: str = Field(description = "a task to assign to a browser agent in natural language")
  class BrowserOutput(BaseModel):
    is_done: bool = Field(description = "whether browser agent is done")
    is_successful: bool = Field(description = "whether browser agent complete task successfully")
    has_errors: bool = Field(description = "wether agent has any non-None errors")
    answer: str = Field(description = "the answer in text")
    screenshot_path: str = Field(description = "the path to the image of the last browser screenshot")
  class BrowserConfig(BaseModel):
    class Config:
      arbitrary_types_allowed = True
    llm: ChatOpenAI
  class BrowserTool(StructuredTool):
    name: str = "browser"
    description: str = "a tool to execute web task. Input should be a natural language task like 'find out which country leads medal table of winter olympic games 2026'."
    args_schema: Type[BaseModel] = BrowserInput
    config: BrowserConfig
    async def _arun(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None):
      agent = Agent(
        task = query,
        llm = self.config.llm
      )
      history_list = await agent.run()

      is_done = history_list.is_done()
      is_successful = history_list.is_successful()
      has_errors = history_list.has_errors()
      extracted = history_list.extracted_content() # List[str]
      screenshot_paths = history_list.screenshot_paths() # List[str] image path
      screenshots = history_list.screenshots() # List[str] image bytes base64
      return BrowserOutput(
        is_done = is_done,
        is_successful = is_successful,
        has_errors = has_errors,
        answer = extracted[-1],
        screenshot_path = screenshot_paths[-1]
      )
    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None):
      return asyncio.run(self._arun(query, run_manager = run_manager))
  return BrowserTool(config = BrowserConfig(llm = ChatOpenAI(api_key = configs.dashscope_key, base_url = configs.dashscope_url, model = configs.dashscope_llm_model)))


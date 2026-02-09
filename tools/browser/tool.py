#!/usr/bin/python3

import asyncio
from typing import Type, List, Optional, Annotated, Literal, Union
from pydantic import BaseModel, Field, validator, root_validator
from langchain_openai import ChatOpenAI
from langchain_core.tools.structured import StructuredTool
from langgraph.prebuilt import InjectedState
from browser_use import Agent

def load_browser_tool(configs):
  class BrowserInput(BaseModel):
    query: str = Field(description = "a task to assign to a browser agent in natural language")
  class BrowserOutput(BaseModel):
    result: str = Field(description = "search result")
  class BrowserConfig(BaseModel):
    class Config:
      arbitrary_types_allowed = True
    llm: ChatOpenAI
  class BrowserTool(StructuredTool):
    name: str = "browser"
    description: str = "a tool to execute web task. Input should be a natural language task like 'find out which country leads medal table of winter olympic games 2026'."
    args_schema: Type[BaseModel] = BrowserInput
    config: BrowserConfig
    def _arun(self, query: str, state: Annotated[dict, InjectedState], run_manager: Optional[CallbackManagerForToolRun] = None):
      agent = Agent(
        task = query,
        llm = self.config.llm
      )
      result = await self.config.agent.run()
      return BrowserOutput(result = result)
    def _run(self, query: str, state: Annotated[dict, InjectedState], run_manager: Optional[CallbackManagerForToolRun] = None):
      return asyncio.run(self._arun(query, state = state, run_manager = run_manager))
  return BrowserTool(config = BrowserConfig(llm = ChatOpenAI(api_key = configs.dashscope_key, base_url = configs.dashscope_url, model_name = configs.dashscope_model)))


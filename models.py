#!/usr/bin/python3

from openai import OpenAI
from langchain_openai import ChatOpenAI
from prompt import Prompt

class LLM(ChatOpenAI):
  def __init__(self, configs, tags = None):
    super(Tongyi, self).__init__(
      api_key = configs.dashscope_key,
      base_url = configs.dashscope_url,
      model_name = configs.dashscope_llm_model,
      top_p = 0.8,
      temperature = 0.7,
      presence_penalty = 1.5,
      extra_body = {
        "top_k": 20,
        "enable_thinking": False
      },
      tags = tags
    )

class VLM(object):
  def __init__(self, configs):
    self.client = OpenAI(
      api_key = configs.dashscope_key,
      base_url = configs.dashscope_url
    )
  def inference(self, prompt: Prompt):
    messages = prompt.to_json()
    response = self.client.chat.completions.create(
      model = configs.dashscope_vlm_model,
      messages = messages,
    )
    return response.choices[0].message.content

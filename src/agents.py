"""
Folder that holds base classes for the different AI agents
"""
import os
import json

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

from utils import function_to_schema

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class _Agent(BaseModel):
    """
    Base class for all AI agents
    """
    def __init__(self, 
                 system_prompt: dict, 
                 model: str, 
                 functions: list) -> None:
        self.openai = OpenAI(api_key=api_key)
        self.messages = []
        self.system_prompt = system_prompt
        self.model = model
        self.tools = [function_to_schema(func) 
                      for func in functions]

    def _run_full_turn(self, user_message: str):
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        completion=self.openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "developer",
                        "content": self.system_prompt}] + [self.messages],
            tools=self.tools
        ).choices[0]

        # if model returns response, process this
        if completion.content:
            model_message = completion.content.message.content
            self.messages.append({
                "role": "assistant",
                "content": model_message
            })
            return model_message
        
        # if it executes a function call, run through all of them
    def _execute_tool_call(self, tool_call, tools_map):
        name = tool_call.function.name
        args = json.loads(tool_call.function.args)

        # better way to put your own spin on this?
        return tools_map[name](**args)






"""
Folder that holds base classes for the different AI agents
"""
import os
import json

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
        self.tool_schemas = [function_to_schema(func)
                            for func in functions]
        self.tool_map = {func.__name__: func for func in functions}

    def _run_full_turn(self, user_message: str):
        """
        Top to bottom execution of OpenAI API Call
        """
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        completion = self.openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "developer",
                    "content": self.system_prompt}] + [self.messages],
            tools=self.tools
        ).choices[0].message

        # if model returns response, process this
        if completion.content:
            self.messages.append({
                "role": "assistant",
                "content": completion.content
            })

            print(f"Assistant: {completion.content}")

        if completion.tool_calls:
            for tool_call in completion.tool_calls:
                result = self._execute_tool_call(tool_call)
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
      
    # if it executes a function call, run through all of them

    def _execute_tool_call(self, tool_call):
        name = tool_call.function.name
        args = json.loads(tool_call.function.args)

        # better way to put your own spin on this?
        return self.tools_map[name](**args)
    
    def run_agent(self):
        print("Beginning agent.  Type 'exit' to quit")

        while True:
            user_message = input()
            if user_message == 'exit':
                break
            self._run_full_turn(user_message)

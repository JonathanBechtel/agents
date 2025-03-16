"""
Folder that holds base classes for the different AI agents
"""

from openai import OpenAI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class _Agent(BaseModel):
    """
    Base class for all AI agents
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._openai = OpenAI()
        

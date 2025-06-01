"""
Types for Agent
"""

from typing import List, Literal, Union, Dict
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """AI Msg class"""

    role: Literal["user", "assistant", "system"]
    content: str


class History(BaseModel):
    """supposed to req a List... ???"""

    _: List[ChatMessage]


class UserMessage(BaseModel):
    """AI Msg class"""

    role: Literal["user"]
    content: str


class AgentInit(BaseModel):
    """obj to init an Agent"""

    system_prompt: Union[List[ChatMessage], None]
    messages: Union[List[ChatMessage], None]


class Tool(BaseModel):
    name: str
    description: str
    args: List[Dict]

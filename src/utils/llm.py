"""
LLM action lib
"""

import os
from dotenv import load_dotenv
from litellm import completion
from projectTypes import History

# from agent import ChatMessage

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def llm_complete(messages: History) -> str:
    """Call LLM to get response"""
    # print("Called LLM COMPLETE")
    # print(messages)
    response = completion(model="openai/gpt-4o", messages=messages, max_tokens=1024)
    return response.choices[0].message.content

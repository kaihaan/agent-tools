"""
Agent Class
"""

from typing import List, Dict
import json
from utils import llm_complete, ChatMessage, extract_md_blocks

class Agent:
    """AI Agent"""

    history: List[ChatMessage]
    system_prompt: List[ChatMessage]
    tool_lookup: Dict

    def __init__(self, sys_prompt: str, tools: Dict):

        if sys_prompt is not None:
            self.system_prompt = [{"role": "system", "content": sys_prompt}]
            self.history = self.system_prompt
            # print("Sys prompt initialised")
        else:
            self.system_prompt = []
            self.history = []

        self.tool_lookup = tools

    def reply(self, msg: str):
        """print agent response"""
        print("Agent: ", msg)

    def complete(self):
        """return LLM completion"""
        res = llm_complete(self.history)
        self.history.append({"role": "assistant", "content": res})
        return res

    def respond(self, msg: str):
        """enter user input"""
        if len(self.system_prompt) > 0 and len(self.history) == 0:
            self.history.append(self.system_prompt)
        self.history.append({"role": "user", "content": msg})
        res = self.complete()
        action = self.parse_action(res)
        tool_name = action["tool_name"]
        # print("Tool called: ", tool_name)
        if tool_name:
            self.act(action)
        self.reply(res)

    def get_history_length(self):
        """check history length"""
        return len(self.history)

    def set_instructions(self, msg: str) -> int:
        """update or set system prompt"""
        self.system_prompt.append({"role": "system", "content": msg})
        return len(self.system_prompt)

    def act(self, action: Dict):
        """take action"""
        result = self.tool_lookup[action["tool_name"]].run(**action["args"])
        print(result)
        # add result to history
        # call another response...

    def parse_action(self, response: str) -> Dict:
        """Parse the LLM response into a structured action dictionary."""
        try:
            response = extract_md_blocks(response, "action")
            response_json = json.loads(response[0])
            if "tool_name" in response_json and "args" in response_json:
                return response_json
            else:
                return {
                    "tool_name": "error",
                    "args": {
                        "message": "You must respond with a JSON tool invocation."
                    },
                }
        except json.JSONDecodeError:
            return {
                "tool_name": "error",
                "args": {
                    "message": "Invalid JSON response. You must respond with a JSON tool invocation."
                },
            }

"""
System Prompt
"""

import json
from ..tools import tool_list


def format_tool_prompt(tool):
    """ string manipulation for 'Inputs' in prompt  """

    inputs = "Inputs: \n```json\n"
    args = tool.parameters.get("args")
    if args:
        inputs += json.dumps(tool.parameters)
        inputs += "\n```"
    else:
        inputs = "Inputs: None"

    base = f"""Tool name: {tool.name} 
Description: {tool.description} 
{ inputs } 
"""

    return base


SYS_PROMPT = f"""
You are an AI agent that can perform tasks by using available tools.
You must ONLY choose to 'terminate' IF the user asks to stop.

Available tools:
{"\n".join(format_tool_prompt(tool) for tool in tool_list)}

If a user asks about files, list them before reading.

Every response MUST have an action.
Respond in this format:
```action
{{
    "reasoning" : "fill in your reasoning here",
    "prompt": "Fill in a prompt for the user here",
    "tool_name": "insert tool_name",
    "args": {{...fill in any required arguments here...}}
}}```
"""

print(SYS_PROMPT)

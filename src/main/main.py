"""
Agent implimentation
"""

from agent import Agent
from file_tools_json import tool_lookup
from file_sys_prompt_json import SYS_PROMPT

print(SYS_PROMPT)

agent = Agent(sys_prompt=SYS_PROMPT, tools=tool_lookup)

# agent loop
iterations: int = 0
while iterations < 10:
    print(f"{agent.get_history_length()}:User:", end="")
    query = input()
    agent.respond(query)
    iterations += 1

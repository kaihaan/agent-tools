"""
Agent implimentation
"""

from agent import Agent
from ..agent import SYS_PROMPT
from ..agent.tools import tool_lookup

print(SYS_PROMPT)

agent = Agent(sys_prompt=SYS_PROMPT, tools=tool_lookup)

# agent loop
iterations: int = 0
while iterations < 10:
    print(f"{agent.get_history_length()}:User:", end="")
    query = input()
    agent.respond(query)
    iterations += 1

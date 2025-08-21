#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from my_tool.math_tool import add
from rich import print
math_agent= Agent(
    name = "Assistant",
    instructions="You are helpful assistant",
    model=Model,
    tools=[add]
)
# print(agent.name)
# print(agent.tools)
#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from my_tool.math_tool import add,subtract,multiply,div
from rich import print
math_agent= Agent(
    name = "Assistant",
    instructions="You are helpful assistant",
    model=Model,
    tools=[add,subtract,multiply,div]
)
# print(agent.name)
# print(agent.tools)
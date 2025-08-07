#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from my_tool.math_tool import add,subtract
from rich import print
math_agent= Agent(
    name = "Assistant",
    instructions="You are helpful assistant",
    model=Model,
    tools=[add,subtract]
)
# print(agent.name)
# print(agent.tools)

# print(math_agent.tools)

# for s in math_agent.tools:
#     print(s.params_json_schema)
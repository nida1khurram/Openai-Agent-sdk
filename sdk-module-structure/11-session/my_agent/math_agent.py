#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from my_tool.math_tool import add
from rich import print
math_agent= Agent(
    name = "Math_Assistant",
    instructions="You are helpful  expert assistant if user query releted math use your tool otherwise if user's query any other topic you should solve user's problem with your wisdom",
    model=Model,
    tools=[add]
)
main_agent= Agent(
    name = "Assistant",
    instructions="You are helpful  expert assistant if user query releted math use your tool otherwise if user's query any other topic you should solve user's problem with your wisdom",
    model=Model
)
# print(agent.name)
# print(agent.tools)
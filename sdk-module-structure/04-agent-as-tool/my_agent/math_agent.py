#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from my_tool.math_tool import add,subtract,multiply,div
from rich import print

math_agent= Agent(
    name = "Math_Agent",
    instructions="You are helpful assistant",
    model=Model,
    tools=[add,subtract,multiply,div]
)
orchestrator_agent=Agent(
    name="Ochestrator_Agent",
    instructions = "You are helpful assistant",
    model=Model,
    tools=[
        math_agent.as_tool(
            tool_name="Math",
            tool_description="This is a math teacher"
        )
    ]
)
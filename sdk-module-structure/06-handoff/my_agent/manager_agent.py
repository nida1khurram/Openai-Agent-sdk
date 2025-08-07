#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from my_agent.eng_agent import eng_agent
from my_agent.math_agent import math_agent
from rich import print

manager_agent= Agent(
    name = "Manager_agent",
    instructions="You are helpful assistant",
    model=Model,
    handoffs=[math_agent, eng_agent], 
)


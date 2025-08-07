#type:ignore
from agents import Agent
from my_config.gemini_config import Model

agent= Agent(
    name = "Assistant",
    instructions="You are helpful assistant",
    model=Model
)
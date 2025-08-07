#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from my_tool.user_data import fetch_user_data

agent= Agent(
    name = "Assistant",
    instructions="You are a helpful assistant that can use tool fetch_user_data and give all detail from user data",
    model=Model,
    tools=[fetch_user_data]
)
 
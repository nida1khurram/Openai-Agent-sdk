#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from my_tool.my_tool import get_age
from instructions.dynamic_instruction import dynamic_instruction
from user_data_type.user_data import UserData

agent= Agent[UserData](
    name = "Assistant",
    # instructions="You are helpful assistant if user input about age use given tool",
    # dynamic instruction
    instructions=dynamic_instruction,
    model=Model,
    tools=[get_age]
)
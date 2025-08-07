from agents import RunContextWrapper, Agent
from user_data_type.user_data import UserData

def dynamic_instruction(ctx:RunContextWrapper[UserData],agent:Agent[UserData]):
    return f"User name is {ctx.context.age} ,You are helpful assistant if user input about age use given tool"


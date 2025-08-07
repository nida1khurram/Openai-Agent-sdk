from agents import function_tool,RunContextWrapper
from user_data_type.user_data import UserData

@function_tool
def get_age(ctx:RunContextWrapper[UserData]):
    """age function"""
    print('function Tool Run....')
    print('ctx ...>',ctx.context)
    # return f"your age is 40."
    # return f"Your Age is {ctx.context["age"]}"
    return f"Your age is {ctx.context.age}"


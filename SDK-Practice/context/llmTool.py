# type:ignore
from pydantic import BaseModel
from rich import print
from agents import OpenAIChatCompletionsModel,Agent,Runner,AsyncOpenAI,set_tracing_disabled,function_tool,RunContextWrapper
from dotenv import load_dotenv
import os
load_dotenv()

set_tracing_disabled(disabled=True)

API_KEY = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model =OpenAIChatCompletionsModel(
    model = 'gemini-2.0-flash',
    openai_client=client,
    
)

# llm context step 1 make class
class UserInfo(BaseModel):
    name:str
    age:int

@function_tool
def get_user_info(ctx:RunContextWrapper[UserInfo]):
    """fetch the user detail"""
    return f"The Name of user {ctx.context.name} and age is {ctx.context.age}"


agent = Agent[UserInfo](
    name = 'assistant',
    instructions='You are helpful assistant'
    'you have a tool get_user_info if someone question about user info to get the user details',
    model = model,
    tools=[get_user_info]
)

user = UserInfo(name="Ali", age=20)

result = Runner.run_sync(
    starting_agent=agent,
    # llm context: func tool
    input="what is user name and age?",
    context=user
    )
print('Agent Result: Func Tool\n')
print(result.final_output)




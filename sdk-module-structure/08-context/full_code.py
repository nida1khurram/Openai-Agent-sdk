#type:ignore
from agents import OpenAIChatCompletionsModel,Agent,Runner,AsyncOpenAI,set_tracing_disabled,function_tool,RunContextWrapper
from pydantic import BaseModel
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

class UserInfo(BaseModel):
    age:int

@function_tool
def get_age(ctx:RunContextWrapper(UserInfo)):
    """age function"""
    print('function Tool Run....')
    print('ctx ...>',ctx.context.age)
    return f"your age is 40."

agent = Agent(
    name = 'assistant',
    instructions='You are helpful assistant if user input about context use tool which you have',
    model = model,
    tools=[get_age]
)
user = UserInfo(age=40)
result = Runner.run_sync(
    agent,
    input='what is your age?',
    context=user
    )
print('Agent Result\n')
# print(result.final_output)


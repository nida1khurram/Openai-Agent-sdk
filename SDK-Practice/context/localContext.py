# type:ignore
from pydantic import BaseModel
from rich import print
from agents import OpenAIChatCompletionsModel,Agent,Runner,AsyncOpenAI,set_tracing_disabled,RunContextWrapper,function_tool
from dotenv import load_dotenv
import os
load_dotenv()
# local context step 1 make class
class UserInfo(BaseModel):
    name:str
    age:int

    def display_user_info(self):
        print(f"UserName is {self.name} and his age is {self.age}")
# user = UserInfo(name="Nida", age=40)
# print(user)

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
@function_tool
def add(wrapper: RunContextWrapper[UserInfo],a:int,b:int) ->int:
    """
    Add two num 
    Args:
        a:first num
        b:second num
    """
    print(wrapper.context.age)
    wrapper.context.display_user_info()
    return a + b

agent = Agent[UserInfo](
    name = 'assistant',
    instructions='You are helpful assistant',
    model = model,
    tools=[add]
)
# local context step 2 make obj
user = UserInfo(name="Nida", age=40)

result = Runner.run_sync(
    starting_agent=agent,
    input='what are sum 5 and 10?',
    context=user
    )
print('Agent Result\n')
print(result.final_output)

# context = RunContextWrapper(
#     context=user
# )
# print(context)
# output
# RunContextWrapper(
#     context=UserInfo(name='Nida', age=40),
#     usage=Usage(
#         requests=0,
#         input_tokens=0,
#         input_tokens_details=InputTokensDetails(cached_tokens=0),
#         output_tokens=0,
#         output_tokens_details=OutputTokensDetails(reasoning_tokens=0),
#         total_tokens=0
#     )
# )
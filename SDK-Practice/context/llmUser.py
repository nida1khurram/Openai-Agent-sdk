# type:ignore
from pydantic import BaseModel
from rich import print
from agents import OpenAIChatCompletionsModel,Agent,Runner,AsyncOpenAI,set_tracing_disabled
from dotenv import load_dotenv
import os
load_dotenv()
# llm context step 1 make class
class UserInfo(BaseModel):
    name:str
    age:int

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

agent2 = Agent[UserInfo](
    name = 'assistant',
    instructions='You are helpful assistant',
    model = model,
)
result = Runner.run_sync(
    starting_agent=agent2,
    # llm context by user prompt
    input="'Given the facts: The Capital of France is Paris.'What is the Capital of France?",
    )
print('Agent Result by User Prompt\n')
print(result.final_output)

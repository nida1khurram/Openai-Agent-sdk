#type:ignore
from agents import OpenAIChatCompletionsModel,Agent,Runner,AsyncOpenAI,set_tracing_disabled
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

agent = Agent(
    name = 'assistant',
    instructions='You are helpful assistant',
    model = model
)
result = Runner.run_sync(
    agent,
    input='who are you?')
print('Agent Result\n')
print(result.final_output)


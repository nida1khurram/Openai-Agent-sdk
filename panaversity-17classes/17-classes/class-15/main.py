#type:ignore
from agents import Agent, Runner,function_tool,set_tracing_export_api_key
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os
from decouple import config

load_dotenv()

openai_key = config("OPENAI_API_KEY")

set_tracing_export_api_key(openai_key)

Model = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

@function_tool
def get_weather(city:str)->str:
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny"

agent = Agent(
        name='Assistant',
        instructions ='you are helpful assistant',
        model=LitellmModel(model=Model, api_key=GEMINI_API_KEY),
        tools=[get_weather]
    )
    
result = Runner.run_sync(
        agent,
        'what is the weather of Karachi?'
    )
print(result.final_output)

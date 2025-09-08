#type:ignore
from agents import Agent, Runner,function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os
set_tracing_disabled(disabled=True)
load_dotenv()

Model = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

@function_tool
def get_weather(city:str)->str:
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny"

@function_tool
def get_city(city:str)->str:
    print(f"Get City")
    return f"we are talking about {city}"

agent = Agent(
        name='Assistant',
        instructions ='you are helpful assistant',
        model=LitellmModel(model=Model, api_key=GEMINI_API_KEY),
        tools=[get_weather,get_city]
    )
    
result = Runner.run_sync(
        agent,
        'what is the weather of Karachi and what are we talking about city?'
    )
print(result.final_output)

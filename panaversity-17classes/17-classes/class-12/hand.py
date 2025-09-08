#type:ignore
from agents import Agent, Runner,function_tool, set_tracing_disabled,enable_verbose_stdout_logging
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os
set_tracing_disabled(disabled=True)
load_dotenv()
# enable_verbose_stdout_logging()

Model = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

@function_tool
def get_weather(city:str)->str:
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny"

weather_agent = Agent(
        name='Weather_Agent',
        instructions ='you are helpful weather assistant',
        model=LitellmModel(model=Model, api_key=GEMINI_API_KEY),
        tools=[get_weather],
        handoff_description="you are expert in weather agent"
    )  
agent = Agent(
        name='Assistant',
        instructions ='you are helpful assistant solve user general query if user query about weather handoff weather agent',
        model=LitellmModel(model=Model, api_key=GEMINI_API_KEY),
        handoffs=[weather_agent]
    )
result = Runner.run_sync(
        agent,
        'who are you?'
        # 'what is the weather of Karachi?'
    )
print(result.last_agent.name)
print(result.final_output)

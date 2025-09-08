# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,function_tool,enable_verbose_stdout_logging,set_tracing_export_api_key,trace,ModelSettings
from rich import print
from agents.run import RunConfig
from agents.agent import StopAtTools
# enable_verbose_stdout_logging()
# Load the environment variables from the .env file
load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
openai_key = os.environ.get("OPENAI_API_KEY")
set_tracing_export_api_key(openai_key)

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)
run_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=run_model,
)
# _______Tool Calling________
@function_tool
def get_weather(city:str) -> str:
    print("Weather func call....")
    return f"The weather is {city} in raining."

@function_tool
def add(n1:int, n2:int) -> int:
    """Two no add arge:n1:first no, n2:second no"""
    print("Add func call....")
    return n1 + n2
# _______Tool Calling________

agent= Agent(
    name = "Haiku agent",
    instructions="Always response in haiku form",
    tools=[get_weather,add],
    model=gemini_model,
    
    )
with trace("Class2"):
    result = Runner.run_sync(
        starting_agent=agent,
        input="who are you?",
        # input="what is the weather of lahore? ",
        run_config=config)# test 1 run both func
    result2 = Runner.run_sync(
        starting_agent=agent,
        input=" what is the answer 2+2?",
        # run_config=config   # test 1 run both func
        )
print("Result :\n")
print(result.final_output)
print(result2.final_output)




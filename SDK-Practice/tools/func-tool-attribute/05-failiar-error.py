#type:ignore
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, function_tool
from rich import print
from dotenv import load_dotenv

import os

# enable_verbose_stdout_logging()
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-1.5-flash",
        openai_client=client
    )
)
# failure error
# agr tool me error ajae tu ya trigger ho jata hai ya ek str return krta ha jo llm k pass jati hai as a tool output 
@function_tool(failure_error_function="error")
def weather(city:str) -> str:
    """ Weather function  """
    return f"The weather of {city} is sunny"

agent = Agent(
    name="Assistant",
    instructions="You are a helpfull assistant",
    tools=[weather]
)

prompt = input('Plz enter your Question:')

result = Runner.run_sync(agent,prompt,run_config=config)

print(result.final_output)
# output return error
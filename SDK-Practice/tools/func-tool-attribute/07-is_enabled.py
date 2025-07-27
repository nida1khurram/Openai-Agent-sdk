#type:ignore
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig,enable_verbose_stdout_logging, function_tool
from rich import print
from dotenv import load_dotenv

import os

enable_verbose_stdout_logging()
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
# agr tool me is_enabled true schema llm k pass jae ga false hoga nhi jae ga
@function_tool(is_enabled=False)
def add(a: int, b:int) -> int:
    """Add two numbers"""
    return a + b

agent = Agent(
    name="Assistant",
    instructions="You are a helpfull assistant",
    tools=[add]
)

prompt = input('Plz enter your Question:')

result = Runner.run_sync(agent,prompt,run_config=config)

print(result.final_output)
# output return error
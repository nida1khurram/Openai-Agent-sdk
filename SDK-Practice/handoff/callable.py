# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,handoff
from rich import print

from typing import Callable
# classes in str int bool
# def func(a:str, b:int) -> str:
callable[[str, int] str]
from agents.run import RunConfig
# enable_verbose_stdout_logging
# enable_verbose_stdout_logging()

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent=Agent(
    name="Assistant Agent",
    instructions="You are helpful assistant"
)
result = Runner.run_sync(agent, "plz solve Solve for 2 + 2 + ", run_config=config)
print("\nCALLING AGENT\n")
# print(result.final_output)


h=handoff(
    agent=agent,
    tool_name_override="Math Assistant",
    tool_description_override="Hello",
    
)
# print(agent.name)
print(h)
# TypeError: handoff() missing 1 required positional argument: 'agent'

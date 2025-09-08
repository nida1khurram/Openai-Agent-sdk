# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,function_tool,enable_verbose_stdout_logging
from rich import print
from agents.run import RunConfig
import asyncio
# enable_verbose_stdout_logging()
# Load the environment variables from the .env file
load_dotenv()
set_tracing_disabled(disabled=True)
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
)
# _______Tool Calling________
@function_tool
async def add(a:int, b:int) -> int:
    """Add two numbers
    Args:
        a:int
        b:int
    """
    print("\nBefore Sleep")
    await asyncio.sleep(3)
    print("Wait......for 3 second")
    print("\nAfter awake")
    return a + b
# print(add)
# _______Tool Calling________
agent= Agent(
    name = "Assistant",
    instructions=add,
    tools=[add])
async def main():
    result =await Runner.run(starting_agent=agent, input="Hi what is 2 + 2 = ?",run_config=config) #test 1
    print("Result :\n")
    print(result.final_output)
asyncio.run(main())



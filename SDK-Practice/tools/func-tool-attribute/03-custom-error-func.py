#type:ignore

from rich import print
import asyncio
import os
from dotenv import load_dotenv

from agents import (
    OpenAIChatCompletionsModel, 
    function_tool, 
    Agent,
    Runner, 
    enable_verbose_stdout_logging, 
    AsyncOpenAI, 
    set_tracing_disabled, 
    RunConfig,
    RunContextWrapper
)
load_dotenv()
# enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
)

agent = Agent(
    name="Helpful Assistant", 
    instructions="You are a helpful assistant"
)
# create custom func
# def custom_error_func(ctx: RunContextWrapper, error: Exception) ->str:
#     print(error)
#     return "Error occured"

@function_tool()
def weather(location: str) -> str:
    """Tool that fetch weather."""
    raise ValueError("Error raised in weather")
    # return f"The weather in {location} is sunny."

async def main():
    weather_agent = Agent(
        name="Weather Agent",
        instructions="Only Use the weather tool to answer questions about the weather.",
        tools=[weather],
    )
    # print(weather_agent.tools)

    result = await Runner.run(
        starting_agent=weather_agent, 
        input="Tell me about weather in Karachi.",
        run_config=config
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
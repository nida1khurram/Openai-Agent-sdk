#type:ignore
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, function_tool
import asyncio
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
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
)

@function_tool
async def translate_to_spanish(text: str) -> str:
    result = await Runner.run(
        starting_agent=spanish_agent,
        input=text,
        max_turns=4,
        run_config=config
    )
    return result.final_output

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[translate_to_spanish],
)

prompt = input('Plz enter your text:')
async def main():
    result = await Runner.run(
        starting_agent=orchestrator_agent, 
        input=prompt,
        run_config=config
    )
    print()
    print(result.final_output)

asyncio.run(main())
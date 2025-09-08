# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio
from rich import print
from openai.types.responses import ResponseTextDeltaEvent
# Load the environment variables from the .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

model = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )

    # Use run_streamed and handle the raw response
    # result = Runner.run_streamed(agent, input="Please tell me 5 jokes.", run_config=config),
    result = Runner.run_streamed(agent, input="Please tell me how to make a cup of tea.", run_config=config)
    # print(type(result), result, "\n\n")
    async for event in result.stream_events():
        # print(event)
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

asyncio.run(main())
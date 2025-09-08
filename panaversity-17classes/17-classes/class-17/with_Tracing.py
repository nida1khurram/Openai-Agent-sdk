# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,trace,set_tracing_export_api_key, set_tracing_disabled
import asyncio
from agents.run import RunConfig
from decouple import config
openai_key = config("OPENAI_API_KEY")

set_tracing_export_api_key(openai_key)

# Load the environment variables from the .env file
load_dotenv()
# set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")

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
)

async def main():
    agent = Agent(name="Joke generator", instructions="Tell funny jokes.")

    with trace("Joke workflow"): 
        first_result = await Runner.run(agent, "Tell me a joke", run_config=config)
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}",run_config=config)
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")

asyncio.run(main())
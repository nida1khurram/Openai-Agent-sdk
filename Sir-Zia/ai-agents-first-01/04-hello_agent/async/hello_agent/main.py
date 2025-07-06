# uv run main.py
# type : ignore
import os
from agents import Agent, AsyncOpenAI, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.run import RunConfig
from dotenv import load_dotenv

set_tracing_disabled(disabled=True)
# for load env secret 
load_dotenv()

API_KEY =os.environ.get("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key = API_KEY,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client,
)

config = RunConfig(
    model = model,
    model_provider = external_client,
)

agent = Agent(
    name = "Assistant",
    instructions = "You're helpful assistant."
)
# agent loop             name   input
result = Runner.run_sync(agent, "Who is the founder of Pakistan?", run_config = config)

print(result.final_output)



# #type:ignore
# import asyncio
# import os
# from dotenv import load_dotenv
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig

# # Load the environment variables from the .env file
# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # Check if the API key is present; if not, raise an error
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# #Reference: https://ai.google.dev/gemini-api/docs/openai
# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True
# )



# async def main():
#     agent = Agent(
#         name="Assistant",
#         instructions="You only respond in haikus.",
#     )

#     result = await Runner.run(agent, "Tell me about recursion in programming.",run_config=config)
#     print(result.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())
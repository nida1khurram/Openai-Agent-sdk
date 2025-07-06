# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,  set_tracing_disabled,enable_verbose_stdout_logging
from agents.run import RunConfig
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
    model=model,# test 2 if runner has no model use llm this one
)


agent= Agent(
    name = "Assistant",
    instructions="You are helpful assistant.",
    model=model
    )
result = Runner.run_sync(starting_agent=agent, input="Who are you?",
    #  run_config=config #test:1 consider this one
     )
print("Result :\n")
print(result.final_output)




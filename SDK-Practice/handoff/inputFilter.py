# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent,Runner, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,handoff,HandoffInputData
# enable_verbose_stdout_logging
from rich import print

# enable_verbose_stdout_logging()

# from typing import Callable
# callable[[str, int] str]

from agents.run import RunConfig

set_tracing_disabled(disabled=True)
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
    name="Mathematicians Agent",
    instructions="You are helpful assistant"
    
)
result = Runner.run_sync(agent, "plz solve Solve for 2 + 2 + ", run_config=config)
print("\nCALLING AGENT\n")
# print(result.final_output)

# input filter
def input_filter(data:HandoffInputData) -> HandoffInputData:
    print("Input func executed")
    return data

handoff_math_agent=handoff(
    agent=agent,
    tool_description_override="Hello",
    input_filter=input_filter 
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
    ),
    handoffs=[handoff_math_agent],
    model = model,
)
result = Runner.run_sync(starting_agent=triage_agent, input="What is 2 + 2", run_config=config)
print(result.final_output)
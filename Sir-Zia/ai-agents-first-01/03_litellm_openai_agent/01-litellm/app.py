# type:ignore
from dotenv import load_dotenv
import os
from agents import Agent,set_tracing_disabled,Runner
from agents.extensions.models.litellm_model import LitellmModel
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.getenv("GEMINI_API_KEY")


agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model=LitellmModel(model="gemini/gemini-2.0-flash",api_key=API_KEY)
)

result = Runner.run_sync(starting_agent=agent, input="Hi")
print("\nCalling Agent \n")
print(result.final_output)
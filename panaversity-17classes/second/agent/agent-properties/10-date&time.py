# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,function_tool,Handoff
from rich import print
from agents.run import RunConfig

from datetime import datetime

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

# _______________________________________________
@function_tool
def show_current_time():
    """Current date aur time dikhata hai"""
    now = datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")  # DD-MM-YYYY HH:MM:SS format

# Use karne ka tarika
# print(show_current_time)
# ________________________________________
agent= Agent(
    name = "Assistant",
    tools=[show_current_time]
    )

result = Runner.run_sync(starting_agent=agent, input="Aaj ka date aur time bata den?",run_config=config) #test 1
print("\nResult :\n")
print(result.final_output)





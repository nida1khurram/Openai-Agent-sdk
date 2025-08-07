# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,  set_tracing_disabled,enable_verbose_stdout_logging,ModelSettings
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
    model=model,
)

agent= Agent(
    name = "Assistant",
    instructions="You are helpful assistant.",
    model=model,
    # 0.1 se 1 tak ki value hoti hai.0.9 mean 90% word chose kre
    model_settings=ModelSettings(top_p=0.1) 
    #top_p probability most likely word
    #top_k probability zia 70, qasim 70, ameen 50 90per
    #top_k  kon se krne hen
# top_p tab use karo jab:
# Variety chahiye, lekin bahut weird answers nahi.
# Example: Story writing, poetry, creative content.
    )
result = Runner.run_sync(starting_agent=agent, input="Tell me fairy story 50 words?",
     )
print("Result :\n")
print(result.final_output)







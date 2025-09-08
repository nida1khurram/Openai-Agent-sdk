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

history_tutor_agent = Agent(
    name="History Tutor",
    # agent handoff handoff-description k behalf pe hogi na k instrc pe
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent]
)

# result = Runner.run_sync(triage_agent, "Hello, how are you.", run_config=config)
# result = Runner.run_sync(triage_agent, "What is the capital of France?", run_config=config)
result = Runner.run_sync(triage_agent, "plz solve Solve for 2 + 2 + ", run_config=config)

print("\nCALLING AGENT\n")
print(result.final_output)



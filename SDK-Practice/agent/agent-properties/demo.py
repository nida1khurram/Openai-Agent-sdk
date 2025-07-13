# type:ignore
from dotenv import load_dotenv
import os
from agents import Agent,Runner,set_tracing_disabled,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig,enable_verbose_stdout_logging
from rich import print
enable_verbose_stdout_logging()

load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model =OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client=provider
)
run_model =OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=provider
)

run_config = RunConfig(
    model=run_model
)
agent =Agent(
    name="Assistant",
    model=model
)
# result = Runner.run_sync(starting_agent=agent, input="How are buddy?")
# print(result.final_output)

result=Runner._get_model(
    agent=agent,
    run_config=run_config
) 
print(result)

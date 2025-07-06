#type:ignore
from dotenv import load_dotenv
import os
from agents import (
    Agent,
    Runner,
    RunConfig,
    OpenAIChatCompletionsModel,AsyncOpenAI,
    set_tracing_disabled,
    enable_verbose_stdout_logging,
    

)
# enable_verbose_stdout_logging()

from agents.run import RunConfig
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
# step 1: provider
provider = AsyncOpenAI(
     api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# 2 step model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client = provider,
)
# config: define at run level
config = RunConfig(
    model=model,
    model_provider=provider,
)

agent= Agent(
    # name = "Assistant" #name is required
    name = 123   # test:1 --> name in int
    )
result = Runner.run_sync(starting_agent=agent, input="Who are you?", run_config=config)
print("Result :\n")
print(result.final_output)

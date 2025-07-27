#type:ignore
# runcontextwrapper generics men context receive krta hai
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, function_tool, enable_verbose_stdout_logging, RunContextWrapper
from dotenv import load_dotenv
import os

enable_verbose_stdout_logging()
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-1.5-flash",
        openai_client=client
    )
)

@function_tool
def add(a: int, b: str) -> int:
    """Add two numbers"""
    return a + b

agent = Agent(
    name="Assistant",
    instructions="You are a helpfull assistant",
    tools=[add]
)

result = Runner.run_sync(
    starting_agent=agent,
    input="What is 2 + 2?",
    run_config=config,
)

print(result.final_output)
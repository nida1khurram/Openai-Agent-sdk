# type: ignore
import os
from dotenv import load_dotenv
from rich import print
from agents.run import RunConfig
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,function_tool, RunHooks, RunContextWrapper,Tool
from dataclasses import dataclass
from typing import Any

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
@function_tool
def add(a:int, b:int) -> int:
    """Add two numbers
    Args:
        a:int
        b:int
    """
    return a + b
# _______Tool Calling________

# ________Run hook___________
@dataclass
class Myhook(RunHooks):
    async def on_agent_start(self, ctx:RunContextWrapper, agent:Agent):
        print(f" on_agent_start: Agent {agent.name} shuru hua!")

    async def on_agent_end(self, ctx:RunContextWrapper, agent:Agent, output:Any ):
        print(f"on_agent_end Agent: {agent.name} ne output diya: {output}")

    async def on_tool_start(self, ctx:RunContextWrapper, agent:Agent, tool:Tool ):
        print(f"on_tool_start:{agent.name} ne {tool.name} tool chala raha hai...")

    async def on_tool_end(self, ctx:RunContextWrapper, agent:Agent, tool:Tool, result:str ):
        print(f"on_tool_end:Tool {tool.name} ka result: {result}...")

my_hook = Myhook()

# ____________
agent= Agent(
    name = "Assistant",
    instructions="You are helpful assistant",
    tools=[add],
    )
    
result = Runner.run_sync(
    starting_agent=agent,
    input="2 + 2 = ?",
    run_config=config,
    hooks=my_hook
    ) 
# print("Result :\n")
# print(result.final_output)
# print(result.last_agent)




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
    async def on_agent_start(self,ctx:RunContextWrapper, agent:Agent):
        print(f" on_agent_start: Agent {agent.name} shuru hua!")

    async def on_agent_end(self,  ctx:RunContextWrapper, agent:Agent, output:Any ):
        print(f"on_agent_end Agent: {agent.name} ne output diya: {output}")

    async def on_tool_start(self, ctx:RunContextWrapper, agent:Agent, tool:Tool ):
        print(f"on_tool_start:{agent.name} ne {tool.name} tool chala raha hai...")

    async def on_tool_end(self, ctx:RunContextWrapper, agent:Agent, tool:Tool, result:str ):
        print(f"on_tool_end:Tool {tool.name} ka result: {result}...")
    async def on_handoff(self, context, from_agent, to_agent):
        print(f"{from_agent.name} handoffs to {to_agent.name}")

my_hook = Myhook()

# ____________
math_expert_agent = Agent(
    name="Mathematician", 
    instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.",
    handoff_description="Handles all mathematical questions and calculations.",
    tools=[add],
)
physics_expert_agent = Agent(
    name="Physicist", 
    instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
    handoff_description="Handles all physics-related queries and theoretical explanations."
)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
    ),
    handoffs=[math_expert_agent, physics_expert_agent],
)
# ________________
result = Runner.run_sync(
    starting_agent=triage_agent,
    input="2 + 2 = ?",    #test 1
    # input="What is the SI unit of electric current?",#test 2
    run_config=config,
    hooks=my_hook
    ) 




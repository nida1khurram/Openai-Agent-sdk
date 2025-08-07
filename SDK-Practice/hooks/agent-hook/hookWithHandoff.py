# type: ignore
import os
from dotenv import load_dotenv
from rich import print
from agents.run import RunConfig
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,function_tool,RunContextWrapper,Tool, AgentHooks
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

# ________ hook___________
@dataclass
class Myhook(AgentHooks):
    async def on_start (self, ctx:RunContextWrapper, agent:Agent):
        print(f" on_agent_start: Agent {agent.name} shuru hua!")

    async def on_end(self, ctx:RunContextWrapper, agent:Agent, output:Any ):
        print(f"on_agent_end Agent: {agent.name} ne output diya: {output}")

    async def on_tool_start(self, ctx:RunContextWrapper, agent:Agent, tool:Tool ):
        print(f"on_tool_start:{agent.name} ne {tool.name} tool chala raha hai...")

    async def on_tool_end(self, ctx:RunContextWrapper, agent:Agent, tool:Tool, result:str ):
        print(f"on_tool_end:Tool {tool.name} ka result: {result}...")
    async def on_handoff(self, ctx:RunContextWrapper, agent, source):
        print(f"{source.name} handoffs to {agent.name}")

my_hook = Myhook()
# __________

math_expert_agent = Agent(
    name="Mathematician", 
    instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.",
    handoff_description="Handles all mathematical questions and calculations.",
    hooks=my_hook,
    tools=[add],
)

history_expert_agent = Agent(
    name="History_Agent", 
    instructions="You are an expert in history. Provide clear and precise answers to history-related problems and concepts.",
    handoff_description="Handles all history-related queries and theoretical explanations.",
    hooks=my_hook
)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Analyze the user's input"
        "If they ask about maths, handoff to the maths agent."
        "If they ask about history, handoff to the history agent."
    ),
    handoffs=[math_expert_agent, history_expert_agent],
    hooks=my_hook
)
# ____________  
result = Runner.run_sync(
    starting_agent=triage_agent,
    input = "2 + 100 ?", #test 1
    # input="who is the founder of pakistan?",#test 2
    run_config=config,
    ) 





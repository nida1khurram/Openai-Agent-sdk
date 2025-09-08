# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, enable_verbose_stdout_logging,HandoffInputData
from agents.run import RunConfig
from typing import Tuple  # Add this import if HandoffInputData uses Tuple
# Assuming HandoffInputData is imported from agents or another module
# You might need to add: from agents.some_module import HandoffInputData

enable_verbose_stdout_logging()

def remove_all_tools(handoff_input_data: HandoffInputData) -> HandoffInputData:
    """Filters out all tool items: file search, web search and function calls+output."""

    history = handoff_input_data.input_history
    new_items = handoff_input_data.new_items

    filtered_history = (
        _remove_tool_types_from_input(history) if isinstance(history, tuple) else history
    )
    filtered_pre_handoff_items = _remove_tools_from_items(handoff_input_data.pre_handoff_items)
    filtered_new_items = _remove_tools_from_items(new_items)

    return HandoffInputData(
        input_history=filtered_history,
        pre_handoff_items=filtered_pre_handoff_items,
        new_items=filtered_new_items,
    )

# Load the environment variables from the .env file
load_dotenv()

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
    model_provider=external_client,
    tracing_disabled=True
)

history_tutor_agent = Agent(
    name="History Tutor",
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
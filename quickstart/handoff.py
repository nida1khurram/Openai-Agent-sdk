
# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file")

# Configure Gemini client
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

# Define your agents
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
    instructions="You determine which agent to use based on the user's question. If it's a math question, route to the math tutor. If it's history, route to history tutor.",
    handoffs=[history_tutor_agent, math_tutor_agent]
)

# Test with a math question
math_question = "4 + 4 - 2"
print(f"\nAsking math question: {math_question}")
math_result = Runner.run_sync(triage_agent, math_question, run_config=config)
print("\nMath Agent Response:")
print(math_result.final_output)

# Test with a history question
history_question = "who was the founder of Pakistan?"
print(f"\nAsking history question: {history_question}")
history_result = Runner.run_sync(triage_agent, history_question, run_config=config)
print("\nHistory Agent Response:")
print(history_result.final_output)

# Test with a non-academic question
general_question = "What is the meaning of life?"
print(f"\nAsking general question: {general_question}")
general_result = Runner.run_sync(triage_agent, general_question, run_config=config)
print("\nGeneral Response:")
print(general_result.final_output)
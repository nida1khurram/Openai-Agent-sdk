# type: ignore
from agents import Agent, AsyncOpenAI, Runner, OpenAIChatCompletionsModel, set_tracing_disabled,function_tool
from agents.run import RunConfig
import os 
from dotenv import load_dotenv

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

    
config = RunConfig(
    model=model,
    model_provider=external_client,
)
print("🔥😈  NumPy Style Docstring 🔥😈")

@function_tool
def add(a, b):
    """
    Adds two numbers.

    Parameters
    ----------
    a : int
        First number.
    b : int
        Second number.

    Returns
    -------
    int
        The sum of the two numbers.
    """
    return a + b

agent = Agent(name="Assistant", instructions="You are a helpful assistant",tools=[add])

result = Runner.run_sync(agent, "What is 2 + 3 ?", run_config=config)

print("Output:😊➕😊")
print(result.final_output)


# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,function_tool,enable_verbose_stdout_logging
from rich import print
from agents.run import RunConfig

# enable_verbose_stdout_logging()
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
def get_weather(city:str) -> str:
    print("Weather func call....")
    return f"The weather is {city} in sunny."
# _______Tool Calling________
agent= Agent(
    name = "Haiku agent",
    instructions="Always response in haiku form",
    tools=[get_weather],
    tool_use_behavior="stop_on_first_tool"#test 2/3 when tool call stop use func othe wise run
    )


# result = Runner.run_sync(
# starting_agent=agent,
# input="what is the weather in karachi?",
# run_config=config) #test 1(rum_llm_again-> by default) when tool_use_behaviour no given
# result = Runner.run_sync(
# starting_agent=agent,
# input="what is the weather in karachi?",
# run_config=config) #test 2
result = Runner.run_sync(starting_agent=agent, input="write 2 lines about life?",run_config=config)# test 3
print("Result :\n")
print(result.final_output)




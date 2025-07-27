#type:ignore
from dotenv import load_dotenv
import os
from agents import (
    Agent,
    Runner,
    RunConfig,
    OpenAIChatCompletionsModel,AsyncOpenAI,
    set_tracing_disabled,
)
# enable_verbose_stdout_logging()

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
    name = "Assistant", #name is required instance attribute/ class attribute
    )

result = Runner.run_sync(starting_agent=agent, input="Who are you?", run_config=config)
print("Result :\n")
print(result.final_output)
# print("Agent name:",agent.name)
# ____________________data class_______________________
from dataclasses import dataclass
# class Person:
#     def __init__(self,name, age):
#         self.name = name
#         self.age = age
# first_person = Person("Nida", 38)
# print(first_person)

# print(first_person.name)
# print(first_person.age)

@dataclass
class Person:
    name : str
    age : int
first_person = Person("Nida",38)
print(first_person.name)
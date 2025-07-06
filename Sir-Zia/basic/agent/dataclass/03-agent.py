#type:ignore
from agents import OpenAIChatCompletionsModel,Agent,Runner,AsyncOpenAI,set_tracing_disabled
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from typing import List

@dataclass
class Tool:
    name: str
    description: str

@dataclass
class Agent:
    name: str
    task: str
    tools: List[Tool]
    instructions: str
    active: bool = False

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model =OpenAIChatCompletionsModel(
    model = 'gemini-2.0-flash',
    openai_client=client,
    
)
# agent = Agent(
#     name = 'Assistant',
#     instructions='You are a helpful assistant',
#     model = model
# )
# Tools
tool1 = Tool(name="ImageClassifier", description="Classifies objects in images")
tool2 = Tool(name="Summarizer", description="Summarizes long texts into bullet points")

# Agent
agent = Agent(
    name="SmartBot",
    task="Assist with visual data and summarization",
    tools=[tool1, tool2],
    instructions="Use ImageClassifier for visual inputs and Summarizer for text.",
    active=True
)

print(agent)


# result = Runner.run_sync(
#     agent,
#     input='who is the last Prophet of Islam?plz full name?')
# print('Agent Result\n')
# print(result.final_output)


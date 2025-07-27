#type:ignore
import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled

load_dotenv()

set_tracing_disabled(disbaled=True)

API_KEY = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

@cl.on_message
async def main():
    agent = Agent(
        name = "Assistant",
        instructions = "You are helpful assistant.",
        model = OpenAIChatCompletionsModel(
            model = 'gemini-2.0-flash',
            openai_client = client
        )
    )
    result = await Runner.run(agent, message.content)
    await cl.Message(content=result.final_output).send()

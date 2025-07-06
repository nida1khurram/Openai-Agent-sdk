# type:ignore
import os
import chainlit as cl
from agents import Agent, Runner,RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

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
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)
#3 agent
agent1 = Agent(
    name = "Translator",
    instructions= "You are a helpful translator always translate urdu sentences into clear and simple english",
    )
#user history
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello! I'm a Translator.How can i help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    #standard Interface 
    history.append({"role":"user","content":message.content})
    result = await Runner.run(
    agent1,
    input =history,
    run_config=run_config, 
      )
    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)
    # Our custom logic goes here...
    # Send a fake response back to the user
    await cl.Message(content=result.final_output).send()
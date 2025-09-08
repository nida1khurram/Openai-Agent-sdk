# type:ignore
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig
from dotenv import load_dotenv
import os

set_tracing_disabled(disabled=True)
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Reference: https://ai.google.dev/gemini-api/docs/openai
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

# Define agents (moved outside functions to avoid re-initialization)
web_dev_agent = Agent(
    name="Web_dev_Assistant",
    instructions="You are a helpful assistant for webdev",
    handoff_description="you are expert in webdev skills")

mobile_dev_agent = Agent(
    name="Mobile_dev_Assistant",
    instructions="You are a helpful assistant for mobile dev",
    handoff_description="you are expert in mobile dev skills"
)

devops_agent = Agent( 
    name="Devops_Assistant",
    instructions="You are a helpful assistant for devops",
)

openai_agent = Agent(
    name="OpenAI_Assistant",
    instructions="You are a helpful assistant for openai")

agentic_ai_agent = Agent(
    name="Agentic_Ai_Assistant",
    instructions="You are a helpful assistant for agentic ai.you have to use tool and solve user query about devops and openai",
    handoff_description="you are expert in agenticai skills",
    tools=[
        devops_agent.as_tool(
            tool_name="Devops_Agent",
            tool_description="solve user's devops query"
        ),
        openai_agent.as_tool(
            tool_name="Openai_Agent",
            tool_description="solve user's openai query"
        )]
)

panacloud_agent = Agent(
    name="Panacloud_Assistant",
    instructions="You are a helpful assistant like manager.you have to handoff other agent depands on user queries like you have 3 handoff agent and also agenticai agent have 2 tool as agent devops and openai so use your given agent for solve user's query",
    handoffs=[web_dev_agent, mobile_dev_agent, agentic_ai_agent]
)

@cl.on_chat_start
async def start():
    await cl.Message(
        content="Hello! I'm Panacloud Assistant. I can help you with web development, mobile development, DevOps, OpenAI, and agentic AI topics. How can I assist you today?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Show loading indicator
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # Run the agent with the user's message
        result = Runner.run_sync(
            starting_agent=panacloud_agent,
            input=message.content,
            run_config=config
        )
        
        # Create response with agent information
        response = f"**{result.last_agent.name}**: {result.final_output}"
        
        # Update the message with the response
        await msg.stream_token(response)
        await msg.update()
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        await msg.stream_token(error_msg)
        await msg.update()

# To run the app, use: chainlit run your_filename.py
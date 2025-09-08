# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,ItemHelpers,function_tool
from agents.run import RunConfig
import asyncio
from rich import print
from openai.types.responses import ResponseTextDeltaEvent
import random
# Load the environment variables from the .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

model = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
def how_many_jokes()-> int:
    return random.randint(1,10)
async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the 'how_many_jokes' tool, then tell that many joke.",
        tools=[how_many_jokes]
    )

    # Use run_streamed and handle the raw response
    # result = Runner.run_streamed(agent, input="Please tell me 5 jokes.", run_config=config),
    result = Runner.run_streamed(
        agent,
        input="Hello",
        run_config=config)
    print("Run starting..." "\n")
    async for event in result.stream_events():
        # print(event) #test 2
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type =="tool_call_item":
                print("--Tool was called")
            elif event.item.type == "tool_call_output_item":
                print("f--Tool output:{event.item.output}")
            elif event.item.type =="message_output_item":
                print(f"--Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass 

asyncio.run(main())
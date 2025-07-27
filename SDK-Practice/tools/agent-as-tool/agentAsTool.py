from agents import Agent, Runner, handoff
from rich import print
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name=None,
            tool_description=None,
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
)

async def main():
    # result = await Runner.run(
    #     starting_agent=orchestrator_agent, 
    #     input="Say 'Hello, how are you?' in Spanish."
    # )
    # print(result.final_output)
    print(orchestrator_agent.tools)

asyncio.run(main())
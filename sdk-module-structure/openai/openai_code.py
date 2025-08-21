#type:ignore
from agents import Agent, Runner
from dotenv import load_dotenv
load_dotenv()

agent=Agent(
    name="Nida",
    instructions="You are helpful assistant"
)
result = Runner.run_sync(
    starting_agent=agent,
    input="who are you?"
)
print(result.final_output)


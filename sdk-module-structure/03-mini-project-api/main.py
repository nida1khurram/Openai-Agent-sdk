#type:ignore
from agents import Runner,set_tracing_disabled
from my_agent.api_agent import agent
set_tracing_disabled(True)

res = Runner.run_sync(
    starting_agent=agent,
    input="Plz give me list all user name with email"
)
print(res.final_output)
#type:ignore
from agents import Runner,set_tracing_disabled
from my_agent.manager_agent import manager_agent
set_tracing_disabled(True)
from rich import print

res = Runner.run_sync(
    starting_agent=manager_agent,
    # input="what is 2 + 2 then add 30?"
    input = "what is noun?"
)

print(f"Last agent name:{res.last_agent.name}")
print(res.final_output)
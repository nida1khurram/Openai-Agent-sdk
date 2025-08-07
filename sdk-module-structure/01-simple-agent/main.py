#type:ignore
from agents import Runner,set_tracing_disabled
from my_agent.math_agent import agent
set_tracing_disabled(True)

res = Runner.run_sync(
    starting_agent=agent,
    input="what is 2+2?"
)
print(res.final_output)
#type:ignore
from agents import Runner,set_tracing_disabled
from my_agent.math_agent import math_agent
from rich import print
set_tracing_disabled(True)


res = Runner.run_sync(
    starting_agent=math_agent,
    # input="what is 2 + 2 ?",
    # input="what is 10 - 2 ?",
    # input="what is 8 * 2 ?",
    input="what is 10 / 2 ?",
    
)
print(res.input)
print(res.final_output)
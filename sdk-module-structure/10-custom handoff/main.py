#type:ignore
from agents import Runner,set_tracing_disabled
from my_agent.math_agent import main_agent
from rich import print
set_tracing_disabled(True)
# ________________

# _______________
res = Runner.run_sync(
    starting_agent=main_agent,
    input="what is 5 + 2 ?",
    context={"name":"Nida", "age":20}
)
# print(res.input)
print(res.final_output)
# print("Last Agent",res.last_agent.name)
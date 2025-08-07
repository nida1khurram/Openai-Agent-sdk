#type:ignore
from agents import Runner,set_tracing_disabled
from my_agent.math_agent import math_agent
from rich import print
set_tracing_disabled(True)


res = Runner.run_sync(
    starting_agent=math_agent,
    # input="what is 2 + 2 multiply in answer 5 add in answer 3?", 
    input = "n1=4, n2=5" #required->  apni marzi tool cal 
   
)
print(res.input)
print(res.final_output)
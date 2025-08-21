#type:ignore
from agents import Runner,set_tracing_export_api_key
from my_agent.math_agent import math_agent
from rich import print
from decouple import config

openai_key = config("OPENAI_API_KEY")

set_tracing_export_api_key(openai_key)

res = Runner.run_sync(
    starting_agent=math_agent,
    input="what is 2 + 2 ?",
   
    
)
print(res.input)
print(res.final_output)
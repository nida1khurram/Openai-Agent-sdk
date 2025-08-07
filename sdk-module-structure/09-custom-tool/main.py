#type:ignore
from agents import Runner,set_tracing_disabled
from my_agent.math_agent import math_agent
from rich import print
set_tracing_disabled(True)
# ________________

# from pydantic import BaseModel

# class UserData(BaseModel):
#     name:str
#     age:int
#     role:str

# user_info = UserData(name="Nida",age=40, role='Student')
# _______________
res = Runner.run_sync(
    starting_agent=math_agent,
    input="what is 12 - 2 ?",
    # input="what is 5 + 2 ?",
    context={"name":"Nida", "age":20}
)
print(res.input)
print(res.final_output)
print("Last Agent",res.last_agent.name)
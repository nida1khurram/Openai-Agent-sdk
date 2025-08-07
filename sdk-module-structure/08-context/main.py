#type:ignore
from agents import Runner,set_tracing_disabled
from my_agent.math_agent import agent
from user_data_type.user_data import UserData

set_tracing_disabled(True)

user_info = UserData(name="Nida",age=40, role='Student')
res = Runner.run_sync(
    starting_agent=agent,
    # input='what is your age?',
    input = "Hello",
    context=user_info
    
)
print(res.final_output)

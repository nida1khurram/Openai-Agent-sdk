#type:ignore
#sqlite viwer extension
# session men history data save rehta hai
from agents import Runner,set_tracing_disabled,SQLiteSession
from my_agent.math_agent import math_agent, main_agent
from rich import print
set_tracing_disabled(True)

# session = SQLiteSession("user_1")#history clean while user exit
session = SQLiteSession("user_1","conversation.db")#pass 2 parameter to save all data while user exit

while True:
    prompt = input("Write Here:")

    if prompt == "exit":
        break

    res = Runner.run_sync(
        starting_agent=main_agent,
        input=prompt,
        session=session
    )
    # print(res.input)
    print(res.final_output)
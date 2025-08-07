#type:ignore
#sqlite viwer extension
# session men history data save rehta hai
from agents import Runner,set_tracing_disabled,SQLiteSession
from my_agent.math_agent import math_agent, main_agent
from rich import print
import asyncio

set_tracing_disabled(True)

# session = SQLiteSession("user_1")#history clean while user exit
session = SQLiteSession("user_1","conversation.db")#pass 2 parameter to save all data while user exit

async def main():
    user_data = await session.get_items()#all items visible in print
    # print(user_data) #test 1
    for user in user_data:  #test 2
        print(f"{user['role']}: {user['content']}")


asyncio.run(main())
#type:ignore
#sqlite viwer extension
# session men history data save rehta hai
from agents import Runner,set_tracing_disabled,SQLiteSession
from my_agent.math_agent import math_agent, main_agent
from rich import print
import asyncio

set_tracing_disabled(True)

session = SQLiteSession("user_1","conversation.db")#pass 2 parameter to save all data while user exit

async def main():
    await session.clear_session()#test 2 all clear
    user_data = await session.get_items()#all items visible in print
    # print(user_data) #test 1
 


asyncio.run(main())
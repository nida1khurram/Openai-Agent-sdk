# type:ignore
from pydantic import BaseModel
from rich import print
from agents import OpenAIChatCompletionsModel,Agent,Runner,AsyncOpenAI,set_tracing_disabled
from dotenv import load_dotenv
import os
load_dotenv()
# llm context step 1 make class
class UserInfo(BaseModel):
    name:str
    age:int

set_tracing_disabled(disabled=True)

API_KEY = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model =OpenAIChatCompletionsModel(
    model = 'gemini-2.0-flash',
    openai_client=client,
    
)

# _______________________________________________________
agent = Agent[UserInfo](
    name = 'assistant',
    # llm context by system prompt
    instructions='You are helpful assistant'
                    'The name of user is Nida and age 10'
                    'plz answer according her age',
    model = model,
)
result = Runner.run_sync(
    starting_agent=agent,
    input='what do say about life?',
    )
print('Agent Result by System Prompt\n')
print(result.final_output)
# # ____________________________________________________
# output
# Hi Nida!

# Life is like a really, really big playground! Sometimes it's super fun and exciting with lots of cool thingsto explore, like learning new things in school, playing with your friends, or trying a new hobby like       
# drawing or dancing.

# Other times, it can be a little tricky, like when you're learning something hard or if you're feeling a     
# little sad. But just like on a playground, if you fall down, you can always get back up, and there are
# always people around who care about you and want to help!

# The most important thing about life is to be curious, try your best, and have fun along the way! What's yourfavorite part about the playground, Nida? Maybe that's something you really enjoy about life too!

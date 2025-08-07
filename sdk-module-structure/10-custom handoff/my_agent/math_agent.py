#type:ignore
from agents import Agent, handoff
from my_config.gemini_config import Model
from my_tool.math_tool import add
from rich import print
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from service.service_func import service
from input_schema.input_schema import MyInputData

math_agent= Agent(
    name = "Math_Assistant",
    instructions=f"""
                {RECOMMENDED_PROMPT_PREFIX}
                 You are helpful math expert assistant.
                 """,
    model=Model,
    tools=[add],
    handoff_description="You are helpful math assistant."
    
)
# ____ customize handoff()
math_teacher_obj = handoff(
    agent=math_agent,
    tool_name_override="math_expert",
    tool_description_override="This is math expert",
    on_handoff=service,  #run first this func then main agent run
    input_type=MyInputData
)

main_agent= Agent(
    name = "Main_Assistant",
    instructions="You are helpful assistant if user query related math use your given tool",
    model=Model,
    # customize handoff
    handoffs=[math_teacher_obj]
    
)
# print(main_agent.handoffs)


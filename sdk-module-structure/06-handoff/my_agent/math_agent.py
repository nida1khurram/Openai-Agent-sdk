#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from my_tool.math_tool import add
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

math_agent= Agent(
    name = "Math_Assistant",
    instructions=f"you are helpful math assistant {RECOMMENDED_PROMPT_PREFIX}",
    model=Model,
    tools=[add],
    handoff_description="You are expert math teacher"
)
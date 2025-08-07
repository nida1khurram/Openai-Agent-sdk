#type:ignore
from agents import Agent
from my_config.gemini_config import Model
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

eng_agent= Agent(
    name = "Eng_Assistant",
    instructions=f"you are helpful eng assistant {RECOMMENDED_PROMPT_PREFIX}",
    model=Model,
    handoff_description="You are expert english teacher"
)
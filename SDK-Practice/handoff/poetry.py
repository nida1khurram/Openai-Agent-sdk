from dotenv import load_dotenv
import os
from agents import Agent,Runner,set_tracing_disabled,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig

from rich import print
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    tracing_disabled=True
)

lyric_poetry_agent=Agent(
    name="Lyrics Agent",
    instructions="Analyze the poem for personal emotions, metaphors, and song-like qualities. Describe (tashree) its themes and literary devices also introduced yourself.",
    handoff_description="Specialist in emotional/short-form poetry"
)
narrative_poetry_agent=Agent(
    name="Narrative Agent",
    instructions="You are expert Narrative poetry agent plz tell your name and summries given your task. ",
    handoff_description="Special Agent for Narrative poetry"
)
dramatic_poetry_agent=Agent(
    name="Dramatic Agent",
    instructions="You are expert Dramatic poetry agent plz tell your name and summries given your task.",
    handoff_description="Special Agent for Dramatic poetry"
)
triage_agent=Agent(
    name = "Triage Agent",
    instructions="Classify the input poem by type: \n"
                "- LYRIC if it expresses emotions (e.g., 'I feel...'). \n"
                "- NARRATIVE if it tells a story (e.g., 'Once upon a...'). \n"
                "- DRAMATIC if it's a character's speech (e.g., 'To be or not to be...'). \n"
                "Then route it to the correct analyst agent.",
    handoffs=[lyric_poetry_agent,narrative_poetry_agent,dramatic_poetry_agent],
    model=model
)

# Narrative
result = Runner.run_sync(starting_agent=triage_agent, input="Once upon a midnight dreary, while I pondered, weak and weary,Over many a quaint and curious volume of forgotten lore—",run_config=config)

# #dramatic
# result = Runner.run_sync(starting_agent=triage_agent, input="Out, out, brief candle!Life’s but a walking shadow..",run_config=config)

# #lyric
# result = Runner.run_sync(starting_agent=triage_agent, input="O my Luve is like a red, red rose,That’s newly sprung in June",run_config=config)


print(result.final_output)
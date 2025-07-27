#type:ignore
from dotenv import load_dotenv
import os
from rich import print
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,RunConfig,GuardrailFunctionOutput

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key = API_KEY,
    base_url = 'https://generativelanguage.googleapis.com/v1beta/openai/'
)
model = OpenAIChatCompletionsModel(
    model = 'gemini-2.0-flash',
    openai_client = external_client
)
config = RunConfig(
    model =model
)
english_translator = Agent(
    name = "English_Agent",
    instructions="You are expert in english language"
)

urdu_translator = Agent(
    name = "Urdu_Agent",
    instructions= "You are expert in urdu language"
)

# orchestrator_agent=Agent(
#     name="orchestrator_agent",
#     instructions=(
#         "You are a translation agent. You use the tools given to you to translate."
#         "If asked for multiple translations, you call the relevant tools."
#     ),
#     tools=[
#         english_translator.as_tool(
#             tool_name="translate_to_english",
#             tool_description="Translate the user's message to English"
#         ),
#         urdu_translator.as_tool(
#             tool_name="translate_to_urdu",
#             tool_description="Translate the user's message to Urdu",
#         )
#     ],
# )
super_agent = Agent(
    name = "super_agent",
    instructions= "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools.",
    tools=[
        english_translator.as_tool(
            tool_name = "engTranslator",
            tool_description="translate eng text"
        ),
        urdu_translator.as_tool(
            tool_name = "urduTranslator",
            tool_description="translate urdu text"
        ),
    ],
)
result = Runner.run_sync(
    starting_agent=super_agent,
    input="'tum kia kar rahy ho', translate it to english",
    run_config=config
)

print(result.final_output)
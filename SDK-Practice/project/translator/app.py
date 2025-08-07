#type:ignore
from dotenv import load_dotenv
import os
from agents import Agent,Runner,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,RunConfig

load_dotenv()

set_tracing_disabled(disabled=True)

API_KEY= os.getenv('GEMINI_API_KEY')

external_client = AsyncOpenAI(
    api_key = API_KEY,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)
config = RunConfig(
    model = model
)

english_translator_agent = Agent(
    name = "English Translator",
    instructions="You provide assistance with english language. convert text into simple english.",
    handoff_description="Specialist agent for english language",
)
urdu_translator_agent = Agent(
    name = "Urdu Translator",
    instructions = "You provide assistance with urdu language. convert text into simple urdu.",
    handoff_description="Specialist agent for urdu language",
)
triage_agent = Agent(
    name="Triage Agent",
    instructions="You are a professional bilingual translator fluent in both Urdu and English." \
    "Your task is to accurately translate text between these two languages based on user requests.",
    handoffs=[english_translator_agent, urdu_translator_agent]
)


result = Runner.run_sync(
    triage_agent,
    # input ="آج موسم خوبصورت ہے plz convert into english",
     input ="Today is sunday plz convert into urdu",
    run_config = config
    )
print("\nTranslator Result:")
print(result.final_output)

















# prompt = input('Please type the text to convert.')
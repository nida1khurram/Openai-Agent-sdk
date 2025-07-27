#type:ignore
from dotenv import load_dotenv
import os
from agents import Agent,Runner,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled

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

Summarizer_agent = Agent(
    name = "Summarizer Agent",
    instructions = "If the user gives a long paragraph, shorten it .",
    model = model
)

result = Runner.run_sync(
    Summarizer_agent,
    input = "Pakistan, officially the Islamic Republic of Pakistan, is a South Asian nation with a rich history and diverse geography. It was established in 1947 after the partition of British India, and is the world's fifth-most populous country, with a predominantly Muslim population. Islamabad is the capital, while Karachi serves as the largest city and financial hub. Key aspects of Pakistan:" \
    "Geography:Pakistan is located in South Asia, bordering Iran, Afghanistan, China, and India. It has a coastline along the Arabian Sea and the Gulf of Oman." \
    "History:Pakistan's history is intertwined with the Indian subcontinent's history, including the Indus Valley Civilization and various empires like the Mughals." \
    "Culture:Pakistan boasts a diverse culture influenced by various groups, including Aryans, Persians, Greeks, Arabs, and Mughals." \
    "Economy:Pakistan has an agricultural economy with major crops like wheat, cotton, and rice.",
    )
print()
print(result.final_output)
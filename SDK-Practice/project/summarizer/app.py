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
    input = "What is a Noun?A noun is a fundamental building block of language that serves as the name of a person, place, thing, animal, concept, or quality. As one of the primary parts of speech, nouns enable us to identify and refer to the subjects and objects in our communication. They provide the essential elements around which sentences are constructed, giving meaning and clarity to our expressions.Nouns can be categorized into several types. Common nouns refer to general items (e.g., city, book), while proper nouns denote specific names (e.g., Mumbai, The Alchemist). Concrete nouns represent tangible objects (e.g., chair, phone), whereas abstract nouns signify intangible ideas (e.g., love, courage). Collective nouns describe groups (e.g., team, flock), and possessive nouns indicate ownership (e.g., Rohan’s laptop). Additionally, nouns can be countable (e.g., apples) or uncountable (e.g., milk).In sentences, nouns function in various roles. They can act as the subject (The teacher explains), the object (She buys a dress), or the complement (He is an engineer). Nouns also form the backbone of phrases and clauses, enabling detailed descriptions and complex ideas.Without nouns, language would lose its structure and precision. They are indispensable in both spoken and written communication, allowing us to share thoughts, describe experiences, and connect with others effectively. Mastering nouns is crucial for clear and impactful expression in any language.",
    )
print()
print(result.final_output)
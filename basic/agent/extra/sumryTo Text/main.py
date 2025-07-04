# app.py
# type: ignore
import streamlit as st
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel, Agent as BaseAgent, Runner, AsyncOpenAI, set_tracing_disabled
from dataclasses import dataclass
from typing import List
import os

# --- Basic Models ---
@dataclass
class Tool:
    name: str
    description: str

@dataclass
class Agent:
    name: str
    task: str
    tools: List[Tool]
    instructions: str
    active: bool = False

# --- Load Environment ---
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.getenv('GEMINI_API_KEY')
client = AsyncOpenAI(api_key=API_KEY, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')

# --- Language Model ---
model = OpenAIChatCompletionsModel(model='gemini-2.0-flash', openai_client=client)

# --- Tools ---
tool1 = Tool("ImageClassifier", "Classifies objects in images")
tool2 = Tool("Summarizer", "Summarizes long texts into bullet points")

# --- Agent Definition ---
agent_config = Agent(
    name="SmartBot",
    task="Assist with visual data and summarization",
    tools=[tool1, tool2],
    instructions="Use ImageClassifier for visual inputs and Summarizer for text.",
    active=True
)

# --- Streamlit UI ---
st.title("🤖 AI Agent Dashboard")
st.markdown(f"**🧠 Agent Name**: {agent_config.name}")
st.markdown(f"**📌 Task**: {agent_config.task}")
st.markdown(f"**✅ Active**: {'Yes' if agent_config.active else 'No'}")
st.markdown(f"**📝 Instructions**: {agent_config.instructions}")

st.divider()
st.subheader("🧰 Tools Equipped")
for tool in agent_config.tools:
    st.markdown(f"- **{tool.name}**: {tool.description}")

st.divider()
user_input = st.text_input("🗨️ Ask the Agent Something")

if user_input and agent_config.active:
    with st.spinner("⏳ Thinking..."):
        try:
            # Your custom agent logic
            agent = BaseAgent(
                name=agent_config.name,
                instructions=agent_config.instructions,
                model=model
            )
            result = Runner.run_sync(agent, input=user_input)
            st.success("✅ Response:")
            st.write(result.final_output)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

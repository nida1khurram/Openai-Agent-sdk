# app.py
# type: ignore
import streamlit as st
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel, Agent as BaseAgent, Runner, AsyncOpenAI, set_tracing_disabled
from dataclasses import dataclass
from typing import List
import os
from PIL import Image, ImageDraw

# --- Models ---
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

# --- Env Setup ---
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.getenv("GEMINI_API_KEY")
client = AsyncOpenAI(api_key=API_KEY, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')

# --- Model ---
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

# --- Tools ---
tools = [
    Tool(name="ImageClassifier", description="Classifies objects in images"),
    Tool(name="Summarizer", description="Summarizes long texts into bullet points")
]

# --- Agent Config ---
agent_config = Agent(
    name="SmartBot",
    task="Assist with visual data and summarization",
    tools=tools,
    instructions="Use ImageClassifier for visual inputs and Summarizer for text.",
    active=True
)

# --- Utility for Circular Icon ---
def load_circular_icon(img_path, size=(60, 60)):
    try:
        img = Image.open(img_path).convert("RGBA").resize(size)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        img.putalpha(mask)
        return img
    except:
        return None

# --- UI ---
st.set_page_config(layout="centered", page_title="AI Agent Dashboard")
st.title("🤖 AI Agent Dashboard")

st.markdown(f"### 🧠 {agent_config.name}")
st.markdown(f"**📌 Task**: {agent_config.task}")
st.markdown(f"**📝 Instructions**: {agent_config.instructions}")
st.markdown(f"**✅ Active**: {'Yes' if agent_config.active else 'No'}")
st.divider()

st.subheader("🧰 Tools Equipped")
for tool in agent_config.tools:
    cols = st.columns([1, 6])
    with cols[0]:
        img = load_circular_icon(f"icons/{tool.name.lower()}.png")
        if img:
            st.image(img)
        else:
            st.markdown("🛠️")
    with cols[1]:
        st.markdown(f"**{tool.name}**\n\n{tool.description}")

st.divider()
st.subheader("🧪 Try a Tool")

tool_choice = st.selectbox("Choose Tool", [t.name for t in tools])

if tool_choice == "Summarizer":
    text = st.text_area("📄 Enter text to summarize")
    if st.button("Run Summarizer") and text:
        with st.spinner("Summarizing..."):
            agent = BaseAgent(name=agent_config.name, instructions=agent_config.instructions, model=model)
            try:
                result = Runner.run_sync(agent, input=text)
                st.success("🧠 Summary:")
                st.write(result.final_output)
            except Exception as e:
                st.error(f"❌ Error: {e}")

elif tool_choice == "ImageClassifier":
    uploaded_image = st.file_uploader("📷 Upload Image", type=["png", "jpg", "jpeg"])
    if st.button("Run Image Classifier") and uploaded_image:
        st.image(uploaded_image, width=200, caption="Uploaded Image")
        with st.spinner("Classifying..."):
            agent = BaseAgent(name=agent_config.name, instructions=agent_config.instructions, model=model)
            try:
                result = Runner.run_sync(agent, input="Classify this image")
                st.success("🔍 Classification Result:")
                st.write(result.final_output)
            except Exception as e:
                st.error(f"❌ Error: {e}")

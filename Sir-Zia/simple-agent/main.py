#type:ignore
import chainlit as cl
from chatbot import myAgent
import asyncio 
import os

# ✅ Optional: Manually set PORT for Railway (Chainlit uses this if needed)
port = int(os.environ.get("PORT", 8000))

@cl.on_chat_start
async def chat_start():
    await cl.Message("Hello How I can Help you?").send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content
    response = await myAgent(user_input)  # ✅ asyncio.run hata diya
    await cl.Message(content=f"{response}").send() 
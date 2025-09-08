# type: ignore
import os
from dotenv import load_dotenv
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled
from rich import print
from agents.run import RunConfig
from pydantic import BaseModel
import asyncio
from agents import (
    
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
   
)
# Load the environment variables from the .env file
load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
)

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str
    answer : str #answer user ques

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)
#test 1
# output = Runner.run_sync(guardrail_agent, "what is the capital of pakistan?", run_config=config)
# print(output.final_output.is_math_homework)
# print(output.final_output.reasoning)
# print(output.final_output.answer)
#test 2
# output = Runner.run_sync(guardrail_agent, "what is 2 + 2?", run_config=config)
# print(output.final_output.is_math_homework)

@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config = config)

    #to print guardrail res
    print("[Guardrail Response]", result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        # tripwire_triggered=False #result.final_output.is_math_homework,
        tripwire_triggered=result.final_output.is_math_homework,
    )
     

agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)
# This should trip the guardrail
#test 1
async def main():
    try:
        result = await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?",    run_config = config)
        print("Guardrail didn't trip - this is unexpected")
        print(result.final_output)

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

asyncio.run(main())

# #test 2
# async def main():
#     try:
#         result = await Runner.run(agent, "Hello", run_config = config)
#         print(result.final_output)

#     except InputGuardrailTripwireTriggered:
#         print("Math homework guardrail tripped")
# asyncio.run(main())








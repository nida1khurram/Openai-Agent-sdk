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
# _______________________
class CountryOutput(BaseModel):
    country :str
    reason:str
    is_country_allow:bool
    answer:str
country_guardrail_agent = Agent(
    name="Country_Guardrail_check",
    instructions="we only allow to talk about Pakistan.Don't answer question about any other country or aspect",
    output_type=CountryOutput,
)
#test 1
# output = Runner.run_sync(country_guardrail_agent, "what is the capital of india?", run_config=config)
# # print(output.final_output)
# print(output.final_output.model_dump())#output json

@output_guardrail
async def country_guardrail(
        ctx: RunContextWrapper, agent: Agent, output:CountryOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(country_guardrail_agent, output, context=ctx.context, run_config = config)

    #to print guardrail res
    print("[Guardrail Response]", result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        # tripwire_triggered=False #result.final_output.is_math_homework,
        tripwire_triggered=result.final_output.is_country_allow,
    )
# ____________________________

agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[country_guardrail]
)
# This should trip the guardrail
#test 1
async def main():
    try:
        result = await Runner.run(agent, "Hello, who is the founder of India?",run_config = config)
        # print("Guardrail didn't trip - this is unexpected")
        print(result.final_output)

    except OutputGuardrailTripwireTriggered:
        print("Country guardrail tripped")

asyncio.run(main())










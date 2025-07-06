# type: ignore
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    Guardrail,
    GuardrailTripwireTriggered,
    AsyncOpenAI,
    OpenAIChatCompletionsModel
)
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Reference: https://ai.google.dev/gemini-api/docs/openai
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
    model_provider=external_client,
    tracing_disabled=True
)

class ChurnDetectionOutput(BaseModel):
    reasoning: str
    is_churn: bool

churn_direction_agent = Agent(
    name="Churn Detection Agent",
    instructions="Identify if the user message indicates a potential customer churn risk",
    output_type=ChurnDetectionOutput,
)

@input_guardrail
async def churn_detection_tripwire(ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    result = await Runner.run(churn_direction_agent, input, context=ctx.context, config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_churn,
    )

customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[
        Guardrail(guardrail_function=churn_detection_tripwire),
    ],
)

async def main():
    # Test with a non-churn message
    await Runner.run(customer_support_agent, "Hello", config=config)
    print("Hello message passed")
    
    # Test with a potential churn message
    try:
        await Runner.run(customer_support_agent, "I think I might cancel my subscription", config=config)
        print("Guardrail didn't trip - this is unexpected")
    except GuardrailTripwireTriggered:
        print("Churn Detection guardrail tripped as expected")

if __name__ == "__main__":
    asyncio.run(main())
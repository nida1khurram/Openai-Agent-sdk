#type:ignore
import asyncio
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agents import Agent,AsyncOpenAI, OpenAIChatCompletionsModel, Runner,input_guardrail, GuardrailFunctionOutput,InputGuardrailTripwireTriggered

from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

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
    model_provider=external_client,
    tracing_disabled=True
)

class Mathcheck(BaseModel):
    is_math_homework: bool
    reasoning: str

check_agent = Agent(
    name="Homework check",
    instructions="Check if the user is asking about homework.",
    output_type=Mathcheck   ,
)
@input_guardrail
async def input_check(ctx, agent, input):
    result = await Runner.run(check_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_homework
    )
agent = Agent(
    name="Support Agent",
    instructions="help the customerin solving math problem.",
    input_guardrails=[input_check],
)
async def main():
    try:
        await Runner.run(agent, "can you solve 2 + 3 = 11?", run_config=config)
    except InputGuardrailTripwireTriggered:
        print("Input Guardrails Trigged: Math homework Blocked because its support Agent")



if __name__ == "__main__":
    asyncio.run(main())

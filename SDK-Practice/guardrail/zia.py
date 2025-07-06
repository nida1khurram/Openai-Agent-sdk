#type:ignore
from pydantic import BaseModel

from dotenv import load_dotenv
import asyncio,os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    OpenAIChatCompletionsModel,AsyncOpenAI,
    set_tracing_disabled,
    # RunConfig
)
from agents.run import RunConfig
from rich import print
load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
# step 1: provider
provider = AsyncOpenAI(
     api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# 2 step model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client = provider,
)
# config: define at run level
config = RunConfig(
    model=model,
    model_provider=provider,
)

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput, 
)

@input_guardrail
async def math_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context,run_config=config)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math_homework,  
    )
agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],  
)

async def main():
    # This should trip the guardrail
    try:
        # await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?", run_config=config)
        await Runner.run(agent, "What is the capital of paskitan", run_config=config)
        print("Guardrail didn't trip - this is unexpected")
    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

asyncio.run(main())
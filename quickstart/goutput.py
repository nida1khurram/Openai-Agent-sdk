#type:ignore
from pydantic import BaseModel
from agents import Agent, Runner,output_guardrail, GuardrailFunctionOutput,InputGuardrailTripwireTrigged

class Message(BaseModel):
    response: str

class MathDetected(BaseModel):
    reasoning: str
    is_math:bool

check_agent = Agent(
    name="Math output check",
    instructions="Check kro output me math solution hai",
    output_type=MathDetected,
)
@output_guardrail
async def output_check(ctx, agent, input:Message):
    result = await Runner.run(check_agent, output.response, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math
    )
agent = Agent(
    name="Support Agent",
    instructions="customer support does not solve math problem.",
    output_guardrails=[output_check],
    output_type=Message,
)
async def main():
    try:
        await Runner.run(agent, "can you solve 2 + 3 = 11?")
    except InputGuardrailTripwireTrigged:
        print("output Guardrails Trigged: Math solution  Blocked successfully")


if __name__ == "__main__":
    asyncio.run(main())



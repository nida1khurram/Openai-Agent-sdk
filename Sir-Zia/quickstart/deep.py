import asyncio
from pydantic import BaseModel
from typing import Union, List

# 1. Define our types (simplified versions of what might be in the agents package)
class GuardrailFunctionOutput(BaseModel):
    output_info: any
    tripwire_triggered: bool

class InputGuardrailResult:
    def __init__(self, output: GuardrailFunctionOutput):
        self.tripwire_triggered = output.tripwire_triggered

class InputGuardrailTripwireTriggered(Exception):
    pass

class Agent:
    def __init__(self, name: str, input_guardrails=None):
        self.name = name
        self.input_guardrails = input_guardrails or []

# 2. Create a guardrail function
async def profanity_guardrail(input_data: Union[str, List[str]]) -> GuardrailFunctionOutput:
    """Simple guardrail that detects bad words"""
    bad_words = ["damn", "hell", "crap"]  # Simple profanity filter
    
    if isinstance(input_data, str):
        contains_profanity = any(word in input_data.lower() for word in bad_words)
    else:
        contains_profanity = any(any(word in item.lower() for word in bad_words) 
                               for item in input_data)
    
    return GuardrailFunctionOutput(
        output_info={"message": "Profanity check complete"},
        tripwire_triggered=contains_profanity
    )

# 3. Create our agent with the guardrail
customer_service_agent = Agent(
    name="Customer Service Bot",
    input_guardrails=[profanity_guardrail]  # Add our guardrail
)

# 4. Runner function that handles the 3-step process
async def run_agent(agent: Agent, input_data: Union[str, List[str]]):
    # Step 1: Guardrail receives the input
    for guardrail in agent.input_guardrails:
        # Step 2: Run guardrail function
        guardrail_output = await guardrail(input_data)
        result = InputGuardrailResult(guardrail_output)
        
        # Step 3: Check if tripwire triggered
        if result.tripwire_triggered:
            raise InputGuardrailTripwireTriggered("Input blocked by guardrail")
    
    # If no guardrails triggered, process the input normally
    print(f"Agent processing: {input_data}")

# 5. Test our implementation
async def main():
    try:
        # This will pass through
        await run_agent(customer_service_agent, "Hello, I need help")
        print("Clean message processed successfully")
        
        # This will trigger the guardrail
        await run_agent(customer_service_agent, "This damn thing is broken!")
        print("This line won't be reached")
    except InputGuardrailTripwireTriggered as e:
        print(f"Guardrail triggered: {e}")

if __name__ == "__main__":
    asyncio.run(main())
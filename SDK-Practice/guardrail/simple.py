# type:ignore
from agents import OpenAIChatCompletionsModel,Agent,Runner,AsyncOpenAI,set_tracing_disabled,RunContextWrapper,TResponseInputItem, GuardrailFunctionOutput,input_guardrail
from dotenv import load_dotenv
import os
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model =OpenAIChatCompletionsModel(
    model = 'gemini-2.0-flash',
    openai_client=client,
    
)
# _______________________
@input_guardrail
def my_guardrail_func(
        ctx:RunContextWrapper,
        agent:Agent,
        input:str | list[TResponseInputItem]
        ) -> GuardrailFunctionOutput:
            print("Guardrail func is execute")
            return GuardrailFunctionOutput(
            output_info=None,   #result me data save ho jata ha bs
            # false kre ga tu g.fuc run hoga phir result no error
            tripwire_triggered=False
        )


# ____________________________
agent = Agent(
    name = 'Assistant',
    instructions='You are a helpful assistant',
    model = model,
    # _______guardrail___________
    input_guardrails=[my_guardrail_func]
    # __________________
)

result = Runner.run_sync(
    agent,
    input='who is the last Prophet of Islam?plz full name?')
print('Agent Result\n')
print(result.final_output)


#type:ignore
from agents import Agent, Runner,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,RunConfig
from dotenv import load_dotenv
import os

set_tracing_disabled(disabled=True)
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

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

web_dev_agent: Agent = Agent(
    name="Web_dev_Assistant",
    instructions="You are a helpful assistant for wevdev",
    handoff_description="you are expert in webdev skills")

mobile_dev_agent: Agent = Agent(
    name="Mobile_dev_Assistant",
    instructions="You are a helpful assistant for mobile dev",
     handoff_description="you are expert in mobile dev skills"
    )
devops_agent: Agent = Agent( 
    name="Devops_Assistant",
    instructions="You are a helpful assistant for devops",
    )

openai_agent: Agent = Agent(
    name="OpenAI_Assistant",
    instructions="You are a helpful assistant")

agentic_ai_agent: Agent = Agent(
    name="Agentic_Ai_Assistant",
    instructions="You are a helpful assistant for agentic ai.you have to use tool and solve user query about devops and openai",
    handoff_description="you are expert in agenticai skills",
    tools=[
        devops_agent.as_tool(
            tool_name="Devops_Agent",
            tool_description="solve user's devops query"
        ),
        openai_agent.as_tool(
            tool_name="Openai_Agent",
            tool_description="solve user's openai query"
        )]
     )

panacloud_agent: Agent = Agent(
    name="Panacloud_Assistant",
    instructions="You are a helpful assistant like manager.you have to handoff other agent depands on user queries like you have 3 handoff agent and also agenticai agent have 2 tool as agent devops and openai so use your given agent for solve user's query",
    handoffs=[web_dev_agent,mobile_dev_agent,agentic_ai_agent]
    )

result = Runner.run_sync(
    starting_agent=panacloud_agent,
    input="who are you?",
    input="what is webdev programming just 3 lines?",
    input="Do you know about mobiledev programming explain just 5 lines?",
    input="what is agenticai explain just 5 lines?",
    input="I want to know about devops programming plz explain just 1 para?",
    input="plz explain openai just 5 lines?",
    run_config=config)

print(f"Last Agent Answer...: {result.last_agent.name}")
print(result.final_output)
#type:ignore
from agents import Agent,ModelSettings
from my_config.gemini_config import Model
from my_tool.math_tool import add,subtract,multiply,div
from agents.agent import StopAtTools
from rich import print
math_agent= Agent(
    name = "Assistant",
    instructions="You are helpful assistant",
    model=Model,
    tools=[add,subtract,multiply,div],
    # test 1
    # llm ne tool call kra tool ka answer llm k pass gaya llm ne modify kr k dya
    # tool_use_behavior="run_llm_again" #llm tool answer modify 2 + 2 = 4
    # by default "run_llm_again"
    # test 2
    # tool ka answer first ane k bad llm ne aise hi dya
    # tool_use_behavior="stop_on_first_tool"#llm don't modify answer The answer is : 4

    # test 3
    # mltiply k bad agent k flow ko break kr dena
    tool_use_behavior=StopAtTools(stop_at_tool_names=["multiply","subtract"]),

    # test 4 tool choice auto/none/required
    model_settings=ModelSettings(
        tool_choice="add",  #force add tool run
        parallel_tool_calls=True   #True 2 ya ziada tool ek sath run 
        ),
    # reset_tool_choice=False
)

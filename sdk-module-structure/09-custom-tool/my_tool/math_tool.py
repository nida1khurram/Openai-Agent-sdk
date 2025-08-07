#type:ignore
from agents import function_tool, FunctionTool,RunContextWrapper
from tool_schema.sub_schema import Sub_Schema
from validator.valid_tool import tool_valid

@function_tool
def add(n1:int, n2:int) -> str:
    """Add two numbers Function:
        arg:
        n1 : first no
        n2 : second no
        return str
    """
    print("Add function call:")
    return f"The answer is : {n1+n2}"

# _______custom func ____________

async def sub_func(ctx:RunContextWrapper,arg):
    res = Sub_Schema.model_validate_json(arg)
    print("subtract func run...")
    return f"Your answer is {res.n1 - res.n2}"

subtract = FunctionTool(
    name="subtract_tool",
    description="Subtract Function",
    params_json_schema=Sub_Schema.model_json_schema(),
    on_invoke_tool=sub_func,
    # is_enabled=False #flase  mean this func unable to run
    is_enabled=tool_valid
)
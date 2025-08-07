#type:ignore
from agents import function_tool

@function_tool
def add(n1:int, n2:int)-> str:
    """Add two no of function
    args:
    n1:first no
    n2:second no
    return str
    """
    return f"The answer is {n1+n2}"


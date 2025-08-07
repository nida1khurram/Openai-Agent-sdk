#type:ignore
from agents import function_tool

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

@function_tool
def subtract(n1:int, n2:int) -> str:
    """Subtract two numbers Function:
        arg:
        n1 : first no
        n2 : second no
        return str
    """
    print("Subtract function call:")
    return f"The answer is : {n1-n2}"


@function_tool
def multiply(n1:int, n2:int) -> str:
    """Multiply two numbers Function:
        arg:
        n1 : first no
        n2 : second no
        return str
    """
    print("Multiply function call:")
    return f"The answer is : {n1 * n2}"

@function_tool
def div(n1:int, n2:int) -> str:
    """Divide two numbers Function:
        arg:
        n1 : first no
        n2 : second no
        return str
    """
    print("Divide function call:")
    return f"The answer is : {n1 / n2}"
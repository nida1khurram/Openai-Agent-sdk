# without generics
from typing import overload
@overload
def get_content(param:int) -> int:
    ...
@overload
def get_content(param:str) -> str:
    ...

def get_content(param):
    return param
print(get_content(7))
print(get_content("Nida"))



# restric in generic type 
from typing import TypeVar
T = TypeVar('T',int,str)

def get_content(param:T) -> T:
    return param
print(get_content(7))
print(get_content("Nida"))

# check return type
typeCheck = get_content("Nida")
print(type(get_content("Nida")))

print(type(get_content(7)))

# print(type(get_content(2.0)))
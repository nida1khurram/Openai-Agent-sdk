# with generics
# Typevar is a tool jo b data hum banate hen iss k liye label bana k data ha
# use func and classes as datatype
from typing import TypeVar
T = TypeVar('T')

def get_content(param:T) -> T:
    return param
print(get_content(7))
print(get_content("Nida"))

# check return type
typeCheck = get_content("Nida")

print(type(get_content("Nida")))

print(type(get_content(7)))
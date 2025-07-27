# repeat value 
from typing import TypeVar
T = TypeVar('T')

def repeat_value[T](value:T, times: int) -> list[T]:
    return [value] * times

print(repeat_value(7,3))
# output [7, 7, 7]
print(repeat_value("Nida", 2))
# output ['Nida', 'Nida']
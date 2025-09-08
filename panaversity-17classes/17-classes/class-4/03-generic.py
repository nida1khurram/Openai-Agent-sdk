#type:ignore
from typing import TypeVar
T = TypeVar('T')
def first(items: list[T]) -> T:
    """Takes a list
    Args:
    items: A list of items
    return:
    The first item in the list"""
    # return "Hello"
    return items[0]
strings=['a','b','c']
num = [1,2,3]
res = first(strings)
res2 = first(num)
print(res)
print(res2)
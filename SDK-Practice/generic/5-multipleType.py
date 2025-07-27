from typing import TypeVar, Dict

K = TypeVar('K', str, None)
V = TypeVar('V')

def get_data(d:Dict[K,V], key:K) -> V:
    return d[key]

person = {"name": "Nida", "age": 38}
print(get_data(person, "name"))
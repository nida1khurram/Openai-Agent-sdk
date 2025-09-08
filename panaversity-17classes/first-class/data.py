class StudentInfo:
    name: str
    age:int

# def st(name,age)->str:
#     return f"{name} {age}"
# print(st("nida",40))

# type error
def st(name:str)->str:
    if not isinstance(name,str):
        raise TypeError("Name must str")
    return f"{name}"

print(st("nida"))
# print(st(1))
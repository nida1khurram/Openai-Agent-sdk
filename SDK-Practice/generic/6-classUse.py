from typing import TypeVar, Generic
T = TypeVar('T')

class Student(Generic[T]):
    def __init__(self,value:T):
        self.value = value
    
    def get(self) -> T:
        return self.value
    
# runtype define
student_name : Student[str]= Student("Nida")
print(student_name.value)
print(type(student_name))
print(student_name.get)

#type:ignore
from dataclasses import dataclass, field

@dataclass
class Person:
    name:str
    age:int
    email: str | None = None
    tags : list[str] = field(default_factory=list)

def is_adult(self) -> bool:
    """Example method that use the dataclass attributes."""
    return self.age >= 18
#usage example
def demo_good_usage():
    person1 = Person(name="Nida", age=40, email="abc@gmail.com")
    person2 = Person(name="Arshman", age=6)
    person3 = Person(name="Irha", age=4, tags=["girl","sweet"])
    
    person1.tags.append("developer")

    print(f"Person1 {person1}") 
    print(f"Person2 {person2}")
    print(f"Person3 {person3}")

demo_good_usage()